from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemoryInput:
    content: str
    importance: str = "medium"
    topics: Optional[list] = None
    nature_code: str = "episodic"
    person_id: str = ""
    tool_codes: Optional[list] = None
    knowledge_codes: Optional[list] = None
    emotion: Optional[dict] = None
    source: str = "user"
    agent_id: str = ""
    owner_agent_id: str = ""
    team_id: str = ""
    session_id: str = ""
    memory_id: str = ""
    timestamp: Optional[float] = None
    expires_at: Optional[float] = None
    tags: Optional[list] = None
    metadata: Optional[dict] = None
    significance: float = 0.5
    is_private: bool = False
    tenant_id: str = ""
    embedding: Optional[list] = None
    temporal_context: Optional[dict] = None

    def __post_init__(self):
        if self.topics is None:
            self.topics = []
        if self.tool_codes is None:
            self.tool_codes = []
        if self.knowledge_codes is None:
            self.knowledge_codes = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
