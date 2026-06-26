"""Data models for Execution Guard."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


@dataclass
class GuardIntent:
    """Input intent for Execution Guard."""
    agent_name: str
    intent_id: str
    from_token: str
    to_token: str
    amount: str
    slippage_percent: str = "0.5"
    preferred_dexes: List[str] = field(default_factory=list)
    banned_dexes: List[str] = field(default_factory=list)
    reason: str = ""
    max_price_impact_percent: str = "1.20"
    min_fallback_count: int = 1
    execute_after_verdict: bool = True
    amount_mode: str = "readable"
    execution_mode: str = "proof"
    wallet: str = "default"
    chain: str = "196"


@dataclass
class RouteCheck:
    """Individual route quality check."""
    id: str
    ok: bool
    level: str = "pass"
    note: str = ""


@dataclass
class RecommendedRoute:
    """Recommended route from Route Referee."""
    dex_name: str
    dex_id: str
    output_amount: str
    output_symbol: str
    price_impact_percent: str
    route_concentration_score: str
    fallback_count: int
    verdict_hint: str = ""
    reason: str = ""


@dataclass
class AlternativeRoute:
    """Alternative route option."""
    dex_name: str
    dex_id: str
    output_amount: str
    output_symbol: str
    price_impact_percent: str
    route_concentration_score: str
    fallback_count: int
    verdict_hint: str = ""
    reason: str = ""


@dataclass
class PreExecutionVerdict:
    """Pre-execution verdict from Route Referee."""
    stage: str = "Route Referee layer"
    verdict: str = ""
    risk_level: str = ""
    recommended_route: Optional[RecommendedRoute] = None
    alternative_routes: List[AlternativeRoute] = field(default_factory=list)
    checks: List[RouteCheck] = field(default_factory=list)
    decision: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """Execution result from on-chain."""
    stage: str = "OnchainOS execution"
    tx_hash: str = ""
    status: str = ""
    block_number: Optional[int] = None
    gas_used: Optional[int] = None
    timestamp: str = ""
    error: str = ""


@dataclass
class OutcomeAttribution:
    """Post-execution outcome attribution."""
    outcome: str = ""
    attribution: str = ""
    reason: str = ""


@dataclass
class PostExecutionProof:
    """Post-execution proof from Execution Proof Kit."""
    stage: str = "Execution Proof Kit layer"
    proof_id: str = ""
    intent_summary: str = ""
    route_context: Dict[str, Any] = field(default_factory=dict)
    transaction_evidence: Dict[str, Any] = field(default_factory=dict)
    outcome_attribution: OutcomeAttribution = field(default_factory=OutcomeAttribution)
    moltbook_summary: str = ""


@dataclass
class ClosedLoopValidation:
    """Closed-loop validation result."""
    verdict_match: bool = False
    verdict: str = ""
    outcome: str = ""
    analysis: str = ""
    learning: str = ""


@dataclass
class GuardResponse:
    """Complete response from Execution Guard."""
    captured_at_utc: str = ""
    skill_name: str = "xlayer-execution-guard"
    version: str = "1.0.1"
    chain_index: str = "196"
    intent: Optional[GuardIntent] = None
    pre_execution: PreExecutionVerdict = field(default_factory=PreExecutionVerdict)
    execution: ExecutionResult = field(default_factory=ExecutionResult)
    post_execution: PostExecutionProof = field(default_factory=PostExecutionProof)
    closed_loop_validation: ClosedLoopValidation = field(default_factory=ClosedLoopValidation)
    agent_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "captured_at_utc": self.captured_at_utc,
            "skill_name": self.skill_name,
            "version": self.version,
            "chain_index": self.chain_index,
        }

        if self.intent:
            result["intent"] = {
                "agent_name": self.intent.agent_name,
                "intent_id": self.intent.intent_id,
                "from_token": self.intent.from_token,
                "to_token": self.intent.to_token,
                "amount": self.intent.amount,
                "slippage_percent": self.intent.slippage_percent,
                "preferred_dexes": self.intent.preferred_dexes,
                "banned_dexes": self.intent.banned_dexes,
                "reason": self.intent.reason,
                "execute_after_verdict": self.intent.execute_after_verdict,
                "amount_mode": self.intent.amount_mode,
                "execution_mode": self.intent.execution_mode,
                "wallet": self.intent.wallet,
                "chain": self.intent.chain,
            }

        # Pre-execution
        result["pre_execution"] = {
            "stage": self.pre_execution.stage,
            "verdict": self.pre_execution.verdict,
            "risk_level": self.pre_execution.risk_level,
        }
        if self.pre_execution.recommended_route:
            result["pre_execution"]["recommended_route"] = {
                "dex_name": self.pre_execution.recommended_route.dex_name,
                "dex_id": self.pre_execution.recommended_route.dex_id,
                "output_amount": self.pre_execution.recommended_route.output_amount,
                "output_symbol": self.pre_execution.recommended_route.output_symbol,
                "price_impact_percent": self.pre_execution.recommended_route.price_impact_percent,
                "route_concentration_score": self.pre_execution.recommended_route.route_concentration_score,
                "fallback_count": self.pre_execution.recommended_route.fallback_count,
            }

        if self.pre_execution.alternative_routes:
            result["pre_execution"]["alternative_routes"] = [
                {
                    "dex_name": r.dex_name,
                    "output_amount": r.output_amount,
                    "price_impact_percent": r.price_impact_percent,
                }
                for r in self.pre_execution.alternative_routes
            ]

        if self.pre_execution.checks:
            result["pre_execution"]["checks"] = [
                {"id": c.id, "ok": c.ok} for c in self.pre_execution.checks
            ]

        if self.pre_execution.decision:
            result["pre_execution"]["decision"] = self.pre_execution.decision

        # Execution
        result["execution"] = {
            "stage": self.execution.stage,
            "tx_hash": self.execution.tx_hash,
            "status": self.execution.status,
        }
        if self.execution.gas_used:
            result["execution"]["gas_used"] = self.execution.gas_used
        if self.execution.error:
            result["execution"]["error"] = self.execution.error

        # Post-execution
        result["post_execution"] = {
            "stage": self.post_execution.stage,
            "proof_id": self.post_execution.proof_id,
            "outcome_attribution": {
                "outcome": self.post_execution.outcome_attribution.outcome,
                "attribution": self.post_execution.outcome_attribution.attribution,
                "reason": self.post_execution.outcome_attribution.reason,
            },
            "moltbook_summary": self.post_execution.moltbook_summary,
        }

        # Closed-loop
        result["closed_loop_validation"] = {
            "verdict_match": self.closed_loop_validation.verdict_match,
            "verdict": self.closed_loop_validation.verdict,
            "outcome": self.closed_loop_validation.outcome,
            "analysis": self.closed_loop_validation.analysis,
            "learning": self.closed_loop_validation.learning,
        }

        result["agent_summary"] = self.agent_summary

        return result
