from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int_list(raw: str | None) -> tuple[int, ...]:
    if not raw:
        return ()
    values: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        values.append(int(part))
    return tuple(values)


@dataclass(slots=True)
class Settings:
    mode: str
    state_path: Path
    redis_url: str | None
    friendli_token: str | None
    friendli_base_url: str
    friendli_model: str
    apify_token: str | None
    apify_actor_id: str | None
    contextual_api_key: str | None
    contextual_agent_id: str | None
    contextual_base_url: str
    kubeconfig: str | None
    kube_namespace: str
    discord_bot_token: str | None
    discord_guild_id: int | None
    discord_channel_ids: tuple[int, ...]
    discord_message_limit: int
    civic_enabled: bool

    @classmethod
    def from_env(cls) -> "Settings":
        guild_id_raw = os.getenv("DISCORD_GUILD_ID")
        return cls(
            mode=os.getenv("MTS_MODE", "fixture"),
            state_path=Path(os.getenv("MTS_STATE_PATH", ".local/mts_state.json")),
            redis_url=os.getenv("REDIS_URL"),
            friendli_token=os.getenv("FRIENDLI_TOKEN"),
            friendli_base_url=os.getenv(
                "FRIENDLI_BASE_URL", "https://api.friendli.ai/serverless/v1"
            ),
            friendli_model=os.getenv(
                "FRIENDLI_MODEL", "meta-llama-3.3-70b-instruct"
            ),
            apify_token=os.getenv("APIFY_TOKEN"),
            apify_actor_id=os.getenv("APIFY_ACTOR_ID"),
            contextual_api_key=os.getenv("CONTEXTUAL_API_KEY"),
            contextual_agent_id=os.getenv("CONTEXTUAL_AGENT_ID"),
            contextual_base_url=os.getenv(
                "CONTEXTUAL_BASE_URL", "https://api.contextual.ai"
            ),
            kubeconfig=os.getenv("KUBECONFIG"),
            kube_namespace=os.getenv("KUBE_NAMESPACE", "production"),
            discord_bot_token=os.getenv("DISCORD_BOT_TOKEN"),
            discord_guild_id=int(guild_id_raw) if guild_id_raw else None,
            discord_channel_ids=_parse_int_list(os.getenv("DISCORD_CHANNEL_IDS")),
            discord_message_limit=int(os.getenv("DISCORD_MESSAGE_LIMIT", "75")),
            civic_enabled=_parse_bool(os.getenv("CIVIC_ENABLED")),
        )

    def ensure_state_dir(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def kubewatch_state_path(self) -> Path:
        return self.state_path.with_name("kubewatch_state.json")

    @property
    def runbook_docs_path(self) -> Path:
        return Path("docs/context")

    @property
    def resolved_kubeconfig(self) -> Path | None:
        if self.kubeconfig:
            return Path(self.kubeconfig)
        local = Path(".local/kubeconfig")
        if local.exists():
            return local
        return None
