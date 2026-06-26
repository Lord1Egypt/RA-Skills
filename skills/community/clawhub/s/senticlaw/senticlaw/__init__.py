"""SentiClaw — 6-Layer Runtime AI Security for OpenClaw."""
from .config   import SentiClawConfig
from .pipeline import SentiClawPipeline
from .models   import (InboundMessage, PipelineResult, OutboundResult,
                       TrustLevel, RiskLevel, AuditEvent)
from .audit    import AuditLogger


class SentiClaw:
    """
    Drop-in 6-layer AI security for OpenClaw agents.

    Quick start:
        from senticlaw import SentiClaw

        sc = SentiClaw(config={
            "owner_ids":      {"discord": ["YOUR_USER_ID"]},
            "trusted_senders": {"discord": ["YOUR_USER_ID"]},
            "alert_channel_id": "YOUR_SECURITY_CHANNEL_ID",
        })

        result = sc.check_inbound(text, sender_id=id, channel="discord", session_id=sess)
        if not result.allowed:
            return result.block_message

        response = agent.respond(result.text)
        safe = sc.check_outbound(response, session_id=sess)
        return safe.response
    """

    def __init__(self, config: dict | SentiClawConfig | None = None):
        if config is None:
            cfg = SentiClawConfig()
        elif isinstance(config, dict):
            cfg = SentiClawConfig.from_dict(config)
        else:
            cfg = config
        self._cfg      = cfg
        self._pipeline = SentiClawPipeline(cfg)

    def check_inbound(self, text: str, sender_id: str = "", channel: str = "",
                      session_id: str = "", metadata: dict | None = None) -> PipelineResult:
        return self._pipeline.check_inbound(
            InboundMessage(text=text, sender_id=sender_id, channel=channel,
                           session_id=session_id, metadata=metadata or {}))

    def check_outbound(self, response: str, session_id: str = "",
                       sender_id: str = "", channel: str = "") -> OutboundResult:
        return self._pipeline.check_outbound(response, session_id, sender_id, channel)

    def check_path(self, path: str):
        from .layers.access import check_path
        return check_path(path, self._cfg.allowed_dirs)

    def check_url(self, url: str):
        from .layers.access import check_url
        return check_url(url, self._cfg.block_private_urls)

    def recent_threats(self, hours: int = 24) -> list[dict]:
        return self._pipeline.auditor.recent_threats(hours)

    def stats(self) -> dict:
        return self._pipeline.auditor.stats()

    @property
    def config(self) -> SentiClawConfig:
        return self._cfg


__version__ = "1.0.0"
__all__ = ["SentiClaw", "SentiClawConfig", "SentiClawPipeline",
           "InboundMessage", "PipelineResult", "OutboundResult",
           "TrustLevel", "RiskLevel", "AuditEvent", "AuditLogger"]
