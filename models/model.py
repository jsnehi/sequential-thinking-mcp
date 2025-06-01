from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from models.enums import ThinkingStage

class Thought(BaseModel):
    id: str
    content: str
    thought_number: int
    total_thoughts: int
    stage: ThinkingStage
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: Optional[List[str]] = []
    axioms_used: Optional[List[str]] = []
    assumptions_challenged: Optional[List[str]] = []
    next_thought_needed: bool = True
    ai_analysis: Optional[str] = None

class ThoughtRequest(BaseModel):
    content: str
    thought_number: int
    total_thoughts: int
    stage: ThinkingStage
    tags: Optional[List[str]] = []
    axioms_used: Optional[List[str]] = []
    assumptions_challenged: Optional[List[str]] = []
    next_thought_needed: bool = True
    use_ai_analysis: bool = True

class ThinkingSession(BaseModel):
    session_id: str
    thoughts: List[Thought] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class SessionSummary(BaseModel):
    session_id: str
    total_thoughts: int
    stages_used: Dict[str, int]
    timeline: List[Dict[str, Any]]
    ai_insights: Optional[str] = None

