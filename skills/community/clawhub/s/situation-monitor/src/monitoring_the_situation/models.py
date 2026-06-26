from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


BucketName = Literal["urgent", "direct_asks", "decisions", "fyi"]


@dataclass(slots=True)
class MessageRecord:
    id: str
    channel: str
    author: str
    content: str
    created_at: datetime
    jump_url: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "MessageRecord":
        return cls(
            id=str(payload["id"]),
            channel=str(payload["channel"]),
            author=str(payload["author"]),
            content=str(payload["content"]),
            created_at=datetime.fromisoformat(str(payload["created_at"])),
            jump_url=str(payload["jump_url"]) if payload.get("jump_url") else None,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "channel": self.channel,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "jump_url": self.jump_url,
        }


@dataclass(slots=True)
class SituationItem:
    channel: str
    bucket: BucketName
    score: int
    summary: str
    action_items: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "SituationItem":
        return cls(
            channel=str(payload["channel"]),
            bucket=str(payload["bucket"]),
            score=int(payload["score"]),
            summary=str(payload["summary"]),
            action_items=[str(item) for item in payload.get("action_items", [])],
            citations=[str(item) for item in payload.get("citations", [])],
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "channel": self.channel,
            "bucket": self.bucket,
            "score": self.score,
            "summary": self.summary,
            "action_items": self.action_items,
            "citations": self.citations,
        }


@dataclass(slots=True)
class SituationReport:
    title: str
    generated_at: datetime
    source: str
    overview: str
    urgent: list[SituationItem] = field(default_factory=list)
    direct_asks: list[SituationItem] = field(default_factory=list)
    decisions: list[SituationItem] = field(default_factory=list)
    fyi: list[SituationItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "SituationReport":
        return cls(
            title=str(payload["title"]),
            generated_at=datetime.fromisoformat(str(payload["generated_at"])),
            source=str(payload["source"]),
            overview=str(payload["overview"]),
            urgent=[
                SituationItem.from_dict(item) for item in payload.get("urgent", [])
            ],
            direct_asks=[
                SituationItem.from_dict(item)
                for item in payload.get("direct_asks", [])
            ],
            decisions=[
                SituationItem.from_dict(item) for item in payload.get("decisions", [])
            ],
            fyi=[SituationItem.from_dict(item) for item in payload.get("fyi", [])],
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "generated_at": self.generated_at.isoformat(),
            "source": self.source,
            "overview": self.overview,
            "urgent": [item.to_dict() for item in self.urgent],
            "direct_asks": [item.to_dict() for item in self.direct_asks],
            "decisions": [item.to_dict() for item in self.decisions],
            "fyi": [item.to_dict() for item in self.fyi],
        }

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            f"_Generated: {self.generated_at.isoformat()}_",
            "",
            f"**Overview**: {self.overview}",
            "",
        ]
        lines.extend(self._render_section("Urgent", self.urgent))
        lines.extend(self._render_section("Direct Asks", self.direct_asks))
        lines.extend(self._render_section("Decisions", self.decisions))
        lines.extend(self._render_section("FYI", self.fyi))
        return "\n".join(lines).strip() + "\n"

    @staticmethod
    def _render_section(title: str, items: list[SituationItem]) -> list[str]:
        lines = [f"## {title}", ""]
        if not items:
            lines.append("- None")
            lines.append("")
            return lines
        for item in items:
            lines.append(
                f"- `{item.channel}`: {item.summary} (score {item.score})"
            )
            if item.action_items:
                lines.append(
                    f"  Actions: {'; '.join(item.action_items)}"
                )
            if item.citations:
                lines.append(
                    f"  Sources: {' | '.join(item.citations)}"
                )
        lines.append("")
        return lines
