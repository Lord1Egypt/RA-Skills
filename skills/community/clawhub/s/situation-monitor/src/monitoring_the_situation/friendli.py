from __future__ import annotations

from openai import OpenAI

from .config import Settings


class FriendliRefiner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.friendli_token,
            base_url=settings.friendli_base_url,
        )

    @property
    def enabled(self) -> bool:
        return bool(self.settings.friendli_token)

    def rewrite_overview(self, bullet_summary: str) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.friendli_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Rewrite the situation summary for an operations user. "
                        "Keep it under 90 words, factual, and action-oriented."
                    ),
                },
                {"role": "user", "content": bullet_summary},
            ],
        )
        return response.choices[0].message.content.strip()

    def draft_reply(self, channel: str, summary: str, action_items: list[str]) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.friendli_model,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Draft a concise Discord reply. Sound calm, specific, and "
                        "operational. Keep it under 80 words."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Channel: {channel}\n"
                        f"Summary: {summary}\n"
                        f"Action items: {', '.join(action_items) or 'None'}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content.strip()
