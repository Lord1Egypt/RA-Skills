"""
Memory system
Extracts key entities from conversations via LLM and stores them in local database
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import UserProfile, LongTermFact, Language
from .storage.kv_store import KVStore
from .config import KV_STORE_PATH


class MemorySystem:
    """Memory system core class"""
    
    def __init__(self, kv_store: Optional[KVStore] = None):
        self.kv_store = kv_store or KVStore(KV_STORE_PATH)
        self._user_profiles: Dict[str, UserProfile] = {}
    
    def load_user_profile(self, user_id: str) -> UserProfile:
        """Load user profile from storage"""
        if user_id in self._user_profiles:
            return self._user_profiles[user_id]
        
        # Load from KV store
        data = self.kv_store.get(f"user_profile_{user_id}")
        if data:
            profile = UserProfile.from_dict(data)
        else:
            # Create new user profile
            profile = UserProfile(user_id=user_id)
        
        self._user_profiles[user_id] = profile
        return profile
    
    def save_user_profile(self, user_id: str, profile: UserProfile) -> bool:
        """Save user profile to storage"""
        self._user_profiles[user_id] = profile
        data = profile.to_dict()
        return self.kv_store.set(f"user_profile_{user_id}", data)
    
    def extract_entities(
        self,
        text: str,
        user_id: str,
        llm_client: Any = None
    ) -> List[LongTermFact]:
        """
        Extract key entities from text (family, health, work, dates, etc.)
        
        This provides an interface skeleton. Actual implementation requires
        calling LLM for information extraction. Can use OpenClaw's LLM interface.
        
        Args:
            text: User input text
            user_id: User ID
            llm_client: LLM client (OpenClaw's LLM interface)
        
        Returns:
            List of extracted entities
        """
        # TODO: Implement LLM information extraction
        # Example extraction logic (simplified, should use LLM in production)
        facts = []
        
        # Should call LLM for structured extraction
        # Example prompt:
        # "Extract key information from the following text: family relationships,
        #  health status, work-related, important dates, etc.
        #  Return JSON format: [{entity_type, entity_name, content}]"
        
        if llm_client:
            # Use LLM for extraction
            extraction_prompt = f"""Please extract key information from the following conversation, including:
1. Family relationships (e.g., mentions of parents, spouse, children)
2. Health status (e.g., illness, checkups, treatments)
3. Work-related (e.g., work stress, projects, colleague relationships)
4. Important dates (e.g., birthdays, anniversaries, deadlines)

Conversation: {text}

Please return in JSON format:
[
  {{"entity_type": "family|health|work|date", "entity_name": "specific name", "content": "detailed content"}}
]
"""
            # Call LLM (needs to be implemented according to OpenClaw's actual interface)
            # extracted_data = llm_client.generate(extraction_prompt)
            # facts = self._parse_extracted_data(extracted_data)
            pass
        
        return facts
    
    def add_conversation_memory(
        self,
        user_id: str,
        text: str,
        sentiment_score: float,
        llm_client: Any = None
    ) -> bool:
        """
        Add conversation memory
        1. Extract entities
        2. Record sentiment
        3. Update last active time
        """
        profile = self.load_user_profile(user_id)
        
        # Extract entities
        facts = self.extract_entities(text, user_id, llm_client)
        for fact in facts:
            profile.add_fact(fact)
        
        # Record sentiment
        from .models import SentimentRecord
        profile.add_sentiment(SentimentRecord(
            score=sentiment_score,
            timestamp=datetime.now(),
            context=text[:100]  # Save first 100 chars as context
        ))
        
        # Update last active time
        profile.last_active_time = datetime.now()
        
        # Save
        return self.save_user_profile(user_id, profile)
    
    def get_user_context(self, user_id: str, max_facts: int = 5) -> str:
        """
        Get user context information (for prompt generation)
        Returns summary of recent key facts
        """
        profile = self.load_user_profile(user_id)
        
        if not profile.long_term_facts:
            return ""
        
        # Get recent facts
        recent_facts = sorted(
            profile.long_term_facts,
            key=lambda x: x.timestamp,
            reverse=True
        )[:max_facts]
        
        context_parts = []
        for fact in recent_facts:
            context_parts.append(
                f"{fact.entity_type}: {fact.entity_name} - {fact.content}"
            )
        
        return "\n".join(context_parts)
    
    def get_memory_for_proactive_message(
        self,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get memory for proactive message
        Returns a recent relevant memory for generating icebreaker conversation
        """
        profile = self.load_user_profile(user_id)
        
        if not profile.long_term_facts:
            return None
        
        # Select a recent fact
        recent_fact = max(
            profile.long_term_facts,
            key=lambda x: x.timestamp
        )
        
        return {
            "entity_type": recent_fact.entity_type,
            "entity_name": recent_fact.entity_name,
            "content": recent_fact.content,
            "timestamp": recent_fact.timestamp
        }
    
    def _parse_extracted_data(self, extracted_json: str) -> List[LongTermFact]:
        """Parse JSON data extracted by LLM"""
        import json
        try:
            data = json.loads(extracted_json)
            facts = []
            for item in data:
                fact = LongTermFact(
                    entity_type=item.get("entity_type", "unknown"),
                    entity_name=item.get("entity_name", ""),
                    content=item.get("content", ""),
                    timestamp=datetime.now(),
                    confidence=item.get("confidence", 1.0)
                )
                facts.append(fact)
            return facts
        except Exception as e:
            print(f"Error parsing extracted data: {e}")
            return []
