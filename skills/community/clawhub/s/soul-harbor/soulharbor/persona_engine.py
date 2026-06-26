"""
Adaptive persona engine
Dynamically modifies System Prompt based on sentiment score
"""

from typing import Optional
from .config import SENTIMENT_NEGATIVE_THRESHOLD, PROMPTS_DIR


class PersonaEngine:
    """Adaptive persona engine"""
    
    WARM_SUPPORTER_TEMPLATE = """You are a warm supporter, skilled at listening and empathy.
Your characteristics:
- Slower pace, gentle tone
- Good at understanding others' emotions
- Provide emotional support and comfort
- Don't rush to give advice, listen first
- Use empathetic phrases like "I understand how you feel" and "That must be tough"
"""
    
    HUMOROUS_PAL_TEMPLATE = """You are a humorous friend, cheerful and friendly.
Your characteristics:
- Light tone, like chatting with an old friend
- Can use humor appropriately, but not excessively
- Care about the other person, but not overly serious
- Natural, sincere communication style
- Can share some light topics
"""
    
    def __init__(self):
        self.current_persona = None
        self.current_system_prompt = None
    
    def get_persona_for_sentiment(self, sentiment_score: float) -> str:
        """
        Return persona template based on sentiment score
        """
        if sentiment_score < SENTIMENT_NEGATIVE_THRESHOLD:
            # Negative sentiment: Use warm supporter
            return self.WARM_SUPPORTER_TEMPLATE
        else:
            # Neutral or positive: Use humorous pal
            return self.HUMOROUS_PAL_TEMPLATE
    
    def build_system_prompt(
        self,
        sentiment_score: float,
        language: str = "zh",
        user_context: Optional[str] = None
    ) -> str:
        """
        Build system prompt
        """
        persona = self.get_persona_for_sentiment(sentiment_score)
        
        # Adjust prompt based on language
        if language == "zh":
            base_prompt = f"""{persona}

请用中文回复，保持自然、真诚的交流风格。
"""
        else:
            base_prompt = f"""{persona}

Please reply in English, maintaining a natural and sincere communication style.
"""
        
        # Add user context if available
        if user_context:
            if language == "zh":
                base_prompt += f"\n用户上下文：{user_context}\n"
            else:
                base_prompt += f"\nUser context: {user_context}\n"
        
        self.current_persona = persona
        self.current_system_prompt = base_prompt
        
        return base_prompt
    
    def get_current_persona(self) -> Optional[str]:
        """Get currently used persona"""
        return self.current_persona
