import os
from openai import OpenAI
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from services.prompts import get_ai_guided_prompt
from services.thoughts import process_with_ai, add_thoughts, get_summary
from models.model import Thought, ThoughtRequest, ThinkingSession, SessionSummary

load_dotenv() 

# Initialize FastAPI app
app = FastAPI(title="Sequential Thinking API", version="1.0.0")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# In-memory storage (in production, use a database)
thinking_sessions: Dict[str, ThinkingSession] = {}

@app.post("/sessions/{session_id}/thoughts", response_model=Thought)
async def add_thought(session_id: str, thought_request: ThoughtRequest):
    """Add a new thought to a thinking session"""
    
    # Create session if it doesn't exist
    if session_id not in thinking_sessions:
        thinking_sessions[session_id] = ThinkingSession(session_id=session_id)
    
    session = thinking_sessions[session_id]
    
    thought = await add_thoughts(session_id, session, thought_request)
    
    # Add thought to session
    session.thoughts.append(thought)
    session.updated_at = datetime.now()
    
    return thought

@app.get("/sessions/{session_id}/thoughts", response_model=List[Thought])
async def get_thoughts(session_id: str):
    """Get all thoughts for a session"""
    if session_id not in thinking_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return thinking_sessions[session_id].thoughts

@app.get("/sessions/{session_id}/summary", response_model=SessionSummary)
async def get_session_summary(session_id: str, include_ai_insights: bool = True):
    """Generate a summary of the thinking session"""
    if session_id not in thinking_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = thinking_sessions[session_id]
    thoughts = session.thoughts
    
    summary = await get_summary(
        thoughts, 
        session_id=session_id, 
        client=client, 
        include_ai_insights=include_ai_insights
    )
    return summary

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear all thoughts from a session"""
    if session_id not in thinking_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    thinking_sessions[session_id].thoughts = []
    thinking_sessions[session_id].updated_at = datetime.now()
    
    return {"message": f"Session {session_id} cleared successfully"}

@app.get("/sessions")
async def get_all_sessions():
    """Get all active thinking sessions"""
    return [
        {
            "session_id": sid,
            "thought_count": len(session.thoughts),
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat()
        }
        for sid, session in thinking_sessions.items()
    ]

@app.post("/sessions/{session_id}/ai-guided-next-step")
async def get_ai_guided_next_step(session_id: str):
    """Get AI suggestion for the next thinking step"""
    if session_id not in thinking_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = thinking_sessions[session_id]
    thoughts = session.thoughts
    
    if not thoughts:
        return {"suggestion": "Start with Problem Definition stage to clearly articulate what you're trying to solve."}
    
    latest_thought = thoughts[-1]
    all_thoughts_context = "\n".join([f"Stage {t.stage.value}: {t.content}" for t in thoughts])
    
    prompt = await get_ai_guided_prompt(all_thoughts_context, latest_thought)
    
    result = await process_with_ai(
        prompt, 
        model="gpt-4",
        max_tokens=200,
        temperature=0.7,
        client=client
    )
    
    return {"suggestion": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)