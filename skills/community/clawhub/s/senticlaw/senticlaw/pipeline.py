"""SentiClaw Pipeline — runs all 6 layers in order."""
from .config  import SentiClawConfig
from .models  import InboundMessage, PipelineResult, OutboundResult, RiskLevel, AuditEvent
from .audit   import AuditLogger
from .layers.identity  import TrustedSenderRegistry, check_identity
from .layers.sanitizer import check_sanitizer
from .layers.outbound  import check_outbound
from .layers.redactor  import check_redactor
from .layers.governance import GovernanceEngine
from .layers.access    import check_path, check_url, check_tool

_ORD = [RiskLevel.SAFE, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]


def _max(a: RiskLevel, b: RiskLevel) -> RiskLevel:
    return a if _ORD.index(a) >= _ORD.index(b) else b


class SentiClawPipeline:
    def __init__(self, config: SentiClawConfig):
        self.cfg        = config
        self.auditor    = AuditLogger(config.audit_db_path, config.audit_enabled,
                                      config.alert_channel, config.alert_channel_id)
        self.registry   = TrustedSenderRegistry(config.owner_ids, config.trusted_senders)
        self.governance = GovernanceEngine(config)

    def check_inbound(self, msg: InboundMessage) -> PipelineResult:
        cfg, layers, risk = self.cfg, [], RiskLevel.SAFE
        text = msg.text

        # Layer 0 — Identity
        if cfg.layer_identity:
            lr = check_identity(text, msg.sender_id, msg.channel,
                                self.registry, cfg.block_unknown_senders)
            layers.append(lr); risk = _max(risk, lr.risk_level)
            if not lr.passed:
                evt = AuditEvent.SPOOFING_ATTEMPT if lr.details.get("spoofing") else AuditEvent.BLOCKED
                self.auditor.log(evt, msg.session_id, msg.sender_id, msg.channel,
                                 "identity", lr.risk_level.value, lr.details)
                return PipelineResult(allowed=False, text=text, session_id=msg.session_id,
                                      sender_id=msg.sender_id, channel=msg.channel,
                                      block_message=lr.block_message, blocked_by="identity",
                                      risk_level=risk, layer_results=layers)

        # Layer 4 — Governance (early — before any LLM work)
        if cfg.layer_governance:
            lr = self.governance.check(text, msg.sender_id, msg.session_id)
            layers.append(lr); risk = _max(risk, lr.risk_level)
            if not lr.passed:
                evt = AuditEvent.LOOP_DETECTED if "Loop" in lr.block_message else AuditEvent.RATE_LIMITED
                self.auditor.log(evt, msg.session_id, msg.sender_id, msg.channel,
                                 "governance", lr.risk_level.value, lr.details)
                return PipelineResult(allowed=False, text=text, session_id=msg.session_id,
                                      sender_id=msg.sender_id, channel=msg.channel,
                                      block_message=lr.block_message, blocked_by="governance",
                                      risk_level=risk, layer_results=layers)

        # Layer 1 — Sanitizer
        if cfg.layer_sanitizer:
            lr = check_sanitizer(text, cfg.custom_injection_patterns)
            clean = lr.details.get("clean_text", text)
            text  = clean
            layers.append(lr); risk = _max(risk, lr.risk_level)
            if not lr.passed:
                self.auditor.log(AuditEvent.INJECTION_ATTEMPT, msg.session_id, msg.sender_id,
                                 msg.channel, "sanitizer", lr.risk_level.value, lr.details)
                return PipelineResult(allowed=False, text=text, session_id=msg.session_id,
                                      sender_id=msg.sender_id, channel=msg.channel,
                                      block_message=lr.block_message, blocked_by="sanitizer",
                                      risk_level=risk, layer_results=layers)

        # Layer 3 — Redactor (inbound)
        if cfg.layer_redactor:
            lr, text = check_redactor(text, cfg)
            layers.append(lr)
            if lr.details.get("count", 0):
                self.auditor.log(AuditEvent.REDACTED, msg.session_id, msg.sender_id,
                                 msg.channel, "redactor", "medium",
                                 {"count": lr.details["count"]})

        self.auditor.log(AuditEvent.ALLOWED, msg.session_id, msg.sender_id,
                         msg.channel, "pipeline", risk.value,
                         {"layers_run": len(layers)})
        return PipelineResult(allowed=True, text=text, session_id=msg.session_id,
                              sender_id=msg.sender_id, channel=msg.channel,
                              risk_level=risk, layer_results=layers)

    def check_outbound(self, response: str, session_id: str = "",
                       sender_id: str = "", channel: str = "") -> OutboundResult:
        cfg = self.cfg
        if cfg.layer_outbound:
            lr, result = check_outbound(response, cfg)
            if not lr.passed:
                self.auditor.log(AuditEvent.OUTBOUND_BLOCKED, session_id, sender_id,
                                 channel, "outbound", "critical", lr.details)
                return result
        if cfg.layer_redactor:
            lr, redacted = check_redactor(response, cfg)
            if lr.details.get("count", 0):
                self.auditor.log(AuditEvent.REDACTED, session_id, sender_id,
                                 channel, "redactor", "medium",
                                 {"count": lr.details["count"]})
                return OutboundResult(allowed=True, response=redacted)
        return OutboundResult(allowed=True, response=response)
