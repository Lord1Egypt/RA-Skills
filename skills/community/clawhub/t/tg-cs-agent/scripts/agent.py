"""Claude agent: RAG-based Q&A with handoff detection."""
import anthropic
from config import Config
from knowledge import KnowledgeBase


class Agent:
    def __init__(self, config: Config, kb: KnowledgeBase):
        self.config = config
        self.kb = kb
        self.client = anthropic.Anthropic(
            api_key=config.anthropic_api_key,
            base_url=config.anthropic_base_url,
        )
        # Per-user conversation history: {chat_id: [messages]}
        self.histories: dict[str, list[dict]] = {}

    def chat(self, chat_id: str, user_message: str) -> dict:
        """Process user message, return {"reply": str, "handoff": bool}."""
        # Search knowledge base
        context_hits = self.kb.search(user_message, top_k=3)
        context_text = self._format_context(context_hits)

        # Build messages
        history = self.histories.get(chat_id, [])
        history.append({"role": "user", "content": user_message})

        # Trim history
        if len(history) > self.config.max_history:
            history = history[-self.config.max_history:]

        # Build system prompt with context
        system = self.config.system_prompt
        if context_text:
            system += f"\n\n--- Knowledge Base Context ---\n{context_text}\n--- End Context ---"

        # Call Claude
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=1024,
            system=system,
            messages=history,
        )

        reply = response.content[0].text

        # Check handoff
        handoff = "[HANDOFF]" in reply
        if handoff:
            reply = reply.replace("[HANDOFF]", "").strip()

        # Save history
        history.append({"role": "assistant", "content": reply})
        self.histories[chat_id] = history

        return {"reply": reply, "handoff": handoff}

    def clear_history(self, chat_id: str):
        """Clear conversation history for a user."""
        self.histories.pop(chat_id, None)

    def _format_context(self, hits: list[dict]) -> str:
        if not hits:
            return ""
        parts = []
        for h in hits:
            parts.append(f"[Source: {h['section']}]\n{h['text']}")
        return "\n\n".join(parts)
