"""
Data model definitions
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum


class Language(Enum):
    """Language preference enumeration"""
    ZH = "zh"
    EN = "en"


@dataclass
class LongTermFact:
    """Long-term memory fact"""
    entity_type: str  # e.g., family, health, work, date
    entity_name: str  # Entity name
    content: str  # Specific content
    timestamp: datetime  # Record time
    confidence: float = 1.0  # Confidence level


@dataclass
class SentimentRecord:
    """Sentiment record"""
    score: float  # -1.0 to 1.0
    timestamp: datetime
    context: Optional[str] = None  # Context text


@dataclass
class UserProfile:
    """User profile data class"""
    user_id: str
    language_pref: Language = Language.ZH
    last_active_time: datetime = field(default_factory=datetime.now)
    long_term_facts: List[LongTermFact] = field(default_factory=list)
    sentiment_trend: List[SentimentRecord] = field(default_factory=list)
    
    def add_fact(self, fact: LongTermFact) -> None:
        """Add long-term memory fact"""
        self.long_term_facts.append(fact)
    
    def add_sentiment(self, record: SentimentRecord) -> None:
        """Add sentiment record"""
        self.sentiment_trend.append(record)
        # Keep only the most recent 100 records
        if len(self.sentiment_trend) > 100:
            self.sentiment_trend = self.sentiment_trend[-100:]
    
    def get_recent_sentiment_avg(self, hours: int = 24) -> Optional[float]:
        """Get average sentiment score for the last N hours"""
        if not self.sentiment_trend:
            return None
        
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = [
            r for r in self.sentiment_trend
            if r.timestamp.timestamp() > cutoff
        ]
        
        if not recent:
            return None
        
        return sum(r.score for r in recent) / len(recent)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format (for serialization)"""
        return {
            "user_id": self.user_id,
            "language_pref": self.language_pref.value,
            "last_active_time": self.last_active_time.isoformat(),
            "long_term_facts": [
                {
                    "entity_type": f.entity_type,
                    "entity_name": f.entity_name,
                    "content": f.content,
                    "timestamp": f.timestamp.isoformat(),
                    "confidence": f.confidence
                }
                for f in self.long_term_facts
            ],
            "sentiment_trend": [
                {
                    "score": r.score,
                    "timestamp": r.timestamp.isoformat(),
                    "context": r.context
                }
                for r in self.sentiment_trend
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        """Create UserProfile from dictionary"""
        from datetime import datetime
        
        profile = cls(
            user_id=data["user_id"],
            language_pref=Language(data["language_pref"]),
            last_active_time=datetime.fromisoformat(data["last_active_time"])
        )
        
        for fact_data in data.get("long_term_facts", []):
            profile.add_fact(LongTermFact(
                entity_type=fact_data["entity_type"],
                entity_name=fact_data["entity_name"],
                content=fact_data["content"],
                timestamp=datetime.fromisoformat(fact_data["timestamp"]),
                confidence=fact_data.get("confidence", 1.0)
            ))
        
        for sent_data in data.get("sentiment_trend", []):
            profile.add_sentiment(SentimentRecord(
                score=sent_data["score"],
                timestamp=datetime.fromisoformat(sent_data["timestamp"]),
                context=sent_data.get("context")
            ))
        
        return profile
