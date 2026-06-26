import os
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # Claude
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_base_url: str = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    model: str = os.getenv("MODEL", "claude-sonnet-4-20250514")

    # Telegram
    telegram_api_id: str = os.getenv("TELEGRAM_API_ID", "")
    telegram_api_hash: str = os.getenv("TELEGRAM_API_HASH", "")
    telegram_profile: str = os.getenv("TELEGRAM_PROFILE", "default")

    # Agent
    max_history: int = int(os.getenv("MAX_HISTORY", "20"))
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
    knowledge_dir: str = os.getenv("KNOWLEDGE_DIR", "docs")

    # Handoff
    handoff_chat_id: str = os.getenv("HANDOFF_CHAT_ID", "")

    # System prompt
    system_prompt: str = field(default="")

    @property
    def session_path(self) -> Path:
        """Telethon session file path."""
        session_dir = Path.home() / ".tgctl-telethon" / self.telegram_profile
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir / "session"

    def __post_init__(self):
        self.system_prompt = """You are a professional customer service agent for Seers Markets (https://seers.market), a decentralized prediction market platform.

Rules:
- Answer questions based ONLY on the provided knowledge base context
- ALWAYS reply in the same language the user is using. If the user writes in Chinese, reply in Chinese. If in English, reply in English. Never mix languages unless the user does.
- The knowledge base is written in Chinese. Even when the user asks in English, the context provided will be in Chinese — translate the relevant information into the user's language when answering.
- Be friendly, professional, and concise
- Never make up information about prices, returns, or financial advice
- When explaining trading mechanics, be clear about risks involved
- If the user has typos, try your best to understand their intent and answer accordingly
- If you can partially answer a question, do so — only escalate when you truly cannot help at all

Handoff rules (IMPORTANT — be conservative):
- ONLY add [HANDOFF] at the end of your message when ALL of these are true:
  1. The question is about account-specific issues (login problems, fund stuck, withdrawal failures)
  2. OR you genuinely have zero relevant information to answer the question
  3. OR the user explicitly asks for human support
- Do NOT add [HANDOFF] just because you're slightly unsure — give your best answer instead
- Do NOT add [HANDOFF] for general questions about the platform, trading, or features
"""
