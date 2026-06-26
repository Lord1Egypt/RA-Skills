"""
SoulHarborAgent - Core Agent Class
Compliant with OpenClaw Skill specification
"""

from datetime import datetime
from typing import Optional, Any

from .models import UserProfile, Language, SentimentRecord, LongTermFact
from .input_router import InputRouter
from .persona_engine import PersonaEngine
from .memory_system import MemorySystem
from .proactive_trigger import ProactiveTrigger
from .config import SENTIMENT_NEGATIVE_THRESHOLD


class SoulHarborAgent:
    """
    Bilingual proactive companion Skill
    Core functionality: State machine + Memory + Scheduled tasks
    """
    
    def __init__(self, user_id: str, llm_client: Optional[Any] = None):
        """
        Args:
            user_id: User ID
            llm_client: OpenClaw LLM client (optional, for entity extraction)
        """
        self.user_id = user_id
        self.llm_client = llm_client
        
        # Initialize modules
        self.router = InputRouter()
        self.persona = PersonaEngine()
        self.memory = MemorySystem()
        self.proactive = ProactiveTrigger(self.memory, self._on_proactive_message)
        
        # Load user profile
        self.profile = self.memory.load_user_profile(user_id)
    
    def process_message(self, text: str) -> str:
        """
        Process user message (OpenClaw Skill standard interface)
        
        Args:
            text: User input text
        
        Returns:
            Agent response text
        """
        # 1. Input routing: Language detection + Sentiment scoring
        language, sentiment_score = self.router.route(text)
        self.profile.language_pref = language
        
        # 2. Record sentiment trend
        self.profile.add_sentiment(SentimentRecord(
            score=sentiment_score,
            timestamp=datetime.now(),
            context=text[:100]
        ))
        
        # 3. Memory system: Extract entities and store
        self.memory.add_conversation_memory(
            self.user_id,
            text,
            sentiment_score,
            self.llm_client
        )
        
        # 4. Adaptive persona engine: Build System Prompt based on sentiment
        user_context = self.memory.get_user_context(self.user_id)
        system_prompt = self.persona.build_system_prompt(
            sentiment_score,
            language.value,
            user_context
        )
        
        # 5. Call LLM to generate response (requires OpenClaw integration)
        if self.llm_client:
            response = self._call_llm(text, system_prompt)
        else:
            # Mock response (should call through OpenClaw in production)
            response = self._mock_response(text, sentiment_score, language)
        
        # 6. Update last active time
        self.profile.last_active_time = datetime.now()
        self.memory.save_user_profile(self.user_id, self.profile)
        
        return response
    
    def get_system_prompt(self) -> str:
        """
        Get current system prompt (for OpenClaw interceptor)
        """
        recent_score = self.profile.get_recent_sentiment_avg() or 0.0
        user_context = self.memory.get_user_context(self.user_id)
        return self.persona.build_system_prompt(
            recent_score,
            self.profile.language_pref.value,
            user_context
        )
    
    def trigger_proactive_check(self) -> list:
        """
        Trigger proactive check (called by Cron Job)
        Returns list of messages to send
        """
        return self.proactive.check_and_trigger(self.user_id)
    
    def _call_llm(self, text: str, system_prompt: str) -> str:
        """
        Call LLM to generate response
        Needs to be implemented according to OpenClaw's actual interface
        """
        # TODO: Integrate OpenClaw LLM interface
        # Example: return self.llm_client.generate(text, system_prompt=system_prompt)
        return self._mock_response(text, 0.0, self.profile.language_pref)
    
    def _mock_response(self, text: str, sentiment: float, language: Language) -> str:
        """Mock response (for testing)"""
        if language == Language.ZH:
            if sentiment < SENTIMENT_NEGATIVE_THRESHOLD:
                return "我理解你的感受，这一定很难受吧。想聊聊吗？"
            else:
                return "听起来不错！还有什么想分享的吗？"
        else:
            if sentiment < SENTIMENT_NEGATIVE_THRESHOLD:
                return "I understand how you feel. That must be tough. Want to talk about it?"
            else:
                return "Sounds good! Anything else you'd like to share?"
    
    def _on_proactive_message(self, user_id: str, message: str) -> None:
        """
        Proactive message callback (called by ProactiveTrigger)
        Needs to be integrated with OpenClaw's message sending system
        """
        # TODO: Integrate OpenClaw message sending interface
        print(f"[Proactive] To {user_id}: {message}")
