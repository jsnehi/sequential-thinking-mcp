from typing import List
from models.model import Thought, SessionSummary
from services.prompts import get_insight_prompt, get_analysis_prompt

async def process_with_ai(prompt: str, model: str, max_tokens: int, temperature: float, client)-> str:
    """Process a prompt with AI and return the response"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI processing error: {str(e)}"

async def analyze_thought_with_ai(thought_content: str, stage: str, client, context: List[str] = None) -> str:
    """Use OpenAI to analyze and enhance the thought process"""
    
    context_text = ""
    if context:
        context_text = f"Previous thoughts in this session:\n" + "\n".join(context[-3:])  # Last 3 thoughts for context
    
    prompt = await get_analysis_prompt(thought_content, stage, context_text)
    
    response = await process_with_ai(
        prompt=prompt,
        model="gpt-4",
        max_tokens=300,
        temperature=0.7,
        client=client
    )
    
    return response


async def add_thoughts(session_id: str, session, thought_request):
    # Generate unique thought ID
    thought_id = f"{session_id}_{len(session.thoughts) + 1}"
    
    # Get context from previous thoughts for AI analysis
    context = [t.content for t in session.thoughts] if session.thoughts else None
    
    # Create thought object
    thought = Thought(
        id=thought_id,
        content=thought_request.content,
        thought_number=thought_request.thought_number,
        total_thoughts=thought_request.total_thoughts,
        stage=thought_request.stage,
        tags=thought_request.tags,
        axioms_used=thought_request.axioms_used,
        assumptions_challenged=thought_request.assumptions_challenged,
        next_thought_needed=thought_request.next_thought_needed
    )
    
    # Add AI analysis if requested
    if thought_request.use_ai_analysis:
        ai_analysis = await analyze_thought_with_ai(
            thought_request.content, 
            thought_request.stage.value,
            context
        )
        thought.ai_analysis = ai_analysis

    return thought

async def get_summary(thoughts, session_id: str, client, include_ai_insights: bool = False):
    # Calculate stage distribution
    stages_used = {}
    for thought in thoughts:
        stage = thought.stage.value
        stages_used[stage] = stages_used.get(stage, 0) + 1
    
    # Create timeline
    timeline = [
        {
            "thought_number": t.thought_number,
            "stage": t.stage.value,
            "timestamp": t.timestamp.isoformat(),
            "preview": t.content[:100] + "..." if len(t.content) > 100 else t.content
        }
        for t in thoughts
    ]
    
    summary = SessionSummary(
        session_id=session_id,
        total_thoughts=len(thoughts),
        stages_used=stages_used,
        timeline=timeline
    )
    
    # Add AI insights if requested
    if include_ai_insights and thoughts:
        all_thoughts_text = "\n\n".join([f"Stage {t.stage.value}: {t.content}" for t in thoughts])
        
        insights_prompt = await get_insight_prompt(all_thoughts_text)
        summary.ai_insights = await process_with_ai(
            insights_prompt, 
            model="gpt-4",
            max_tokens=400,
            temperature=0.7,
            client=client
        )
    return summary
    