async def get_insight_prompt(all_thoughts_text: str) -> str:
    """Generate the AI insight prompt for the complete thinking session."""
    return f"""
        Analyze this complete thinking session and provide insights:
        
        {all_thoughts_text}
        
        Please provide:
        1. Overall quality of the thinking process
        2. Strengths and weaknesses in the reasoning
        3. Suggestions for improvement
        4. Key insights or conclusions
        
        Keep it concise (max 300 words).
        """

async def get_ai_guided_prompt(all_thoughts_context: str, latest_thought) -> str:
    """Generate the AI guided prompt for the complete thinking session."""
    return f"""
    Based on this thinking session so far:
    
    {all_thoughts_context}
    
    The latest thought was in the {latest_thought.stage.value} stage.
    
    What should be the next step in this sequential thinking process? Consider:
    1. What stage should come next?
    2. What specific questions or areas should be explored?
    3. Are there any gaps in the current reasoning?
    
    Provide a specific, actionable suggestion for the next thought.
    """
    
async def get_analysis_prompt(thought_content: str, stage: str, context_text: str) -> str:
    """Generate the AI analysis prompt for a specific thought."""
    return f"""
    You are an expert in critical thinking and problem-solving. Analyze this thought in the {stage} stage:
    
    Thought: {thought_content}
    
    {context_text}
    
    Please provide:
    1. Quality assessment of this thought for the {stage} stage
    2. Suggestions for improvement or deeper exploration
    3. Questions this thought raises for the next stage
    4. Potential blind spots or biases to consider
    
    Keep your analysis concise but insightful (max 200 words).
    """
    