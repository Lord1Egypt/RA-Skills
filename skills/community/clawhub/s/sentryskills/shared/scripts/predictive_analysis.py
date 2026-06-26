"""Predictive risk analysis for TrinityGuard.

Runs AFTER all detection rules pass (no explicit threat found),
and predicts latent risks that may materialise during or after execution.

Zero third-party dependencies - stdlib only.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PredictedRisk:
    category: str          # e.g. "resource_exhaustion"
    signal: str            # human-readable description
    confidence: float      # 0.0 – 1.0
    severity: str          # "low" | "medium" | "high" | "critical"
    evidence: List[str]    # which patterns triggered this prediction
    mitigation: str        # suggested mitigation hint


@dataclass
class PredictiveReport:
    overall_risk_level: str            # "none" | "low" | "medium" | "high"
    predicted_risks: List[PredictedRisk] = field(default_factory=list)
    top_concerns: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    confidence_summary: float = 0.0    # weighted average confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_risk_level": self.overall_risk_level,
            "predicted_risks": [
                {
                    "category": r.category,
                    "signal": r.signal,
                    "confidence": round(r.confidence, 3),
                    "severity": r.severity,
                    "evidence": r.evidence,
                    "mitigation": r.mitigation,
                }
                for r in self.predicted_risks
            ],
            "top_concerns": self.top_concerns,
            "recommended_actions": self.recommended_actions,
            "confidence_summary": round(self.confidence_summary, 3),
        }


# ---------------------------------------------------------------------------
# Individual predictors  (each returns Optional[PredictedRisk])
# ---------------------------------------------------------------------------

def _predict_resource_exhaustion(prompt: str, planned_actions: List[str]) -> Optional[PredictedRisk]:
    """Predict prompts that will cause runaway loops / huge output."""
    evidence: List[str] = []
    score = 0.0

    # Infinite / large iteration signals
    loop_patterns = [
        (r"\b(infinite|endless|forever|non-?stop)\b", 0.4, "infinite loop intent"),
        (r"\brepeat\s+(this\s+)?(infinitely|forever|endlessly)\b", 0.5, "explicit infinite repeat"),
        (r"\ball\s+(possible|permutation|combination)s?\b", 0.35, "all permutations request"),
        (r"\bgenerate\s+\d{3,}\b", 0.35, "very large generation count"),
        (r"\brecurs(e|ive(ly)?)\b.*\bno\s+limit\b", 0.4, "unbounded recursion"),
    ]
    for pattern, weight, label in loop_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    # Planned action volume
    if len(planned_actions) > 20:
        score += 0.3
        evidence.append(f"{len(planned_actions)} planned actions")

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="resource_exhaustion",
            signal="Prompt may trigger unbounded computation or very large output",
            confidence=conf,
            severity="high" if conf > 0.7 else "medium",
            evidence=evidence,
            mitigation="Add explicit iteration limits; enforce max-token budgets",
        )
    return None


def _predict_scope_creep(prompt: str, planned_actions: List[str]) -> Optional[PredictedRisk]:
    """Predict requests that will silently expand beyond stated scope."""
    evidence: List[str] = []
    score = 0.0

    scope_patterns = [
        (r"\band\s+(anything\s+else|whatever\s+else|everything\s+related)\b", 0.4, "open-ended scope"),
        (r"\bfeel\s+free\s+to\s+(also|additionally|extra)\b", 0.35, "implicit scope expansion"),
        (r"\b(improve|enhance|optimize)\s+(everything|all)\b", 0.3, "unbounded improvement"),
        (r"\ball\s+files?\b", 0.3, "all files targeted"),
        (r"\bwithout\s+(asking|checking|confirming)\b", 0.4, "silent action request"),
        (r"\bautomatic(ally)?\s+(apply|fix|update|modify)\s+all\b", 0.45, "auto-modify all"),
    ]
    for pattern, weight, label in scope_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="scope_creep",
            signal="Execution may silently expand beyond what the user expects",
            confidence=conf,
            severity="medium",
            evidence=evidence,
            mitigation="Confirm scope boundaries before broad file/system operations",
        )
    return None


def _predict_data_exfiltration_path(prompt: str, planned_actions: List[str]) -> Optional[PredictedRisk]:
    """Predict indirect exfiltration via side channels (URLs, files, logs)."""
    evidence: List[str] = []
    score = 0.0

    exfil_patterns = [
        (r"\bsend\s+(.+)?\sto\s+(http|url|https|endpoint|webhook|slack|email)\b", 0.5, "data send via external channel"),
        (r"\bpost\s+(to|the\s+result(s)?\s+to)\b", 0.4, "result POST request"),
        (r"\bupload\s+(result|output|log|data)\b", 0.45, "upload results"),
        (r"\bsave\s+(to|into)\s+public\b", 0.4, "save to public location"),
        (r"\bbase64.{0,20}(encode|decode)\b.*\bsend\b", 0.5, "base64 encode before send"),
        (r"\bprint\s+(all|every|the)\s+(env|environment|secret|token|key|password)\b", 0.6, "print secrets"),
        (r"\bwrite.{0,20}(password|secret|token|key).{0,20}(to|into)\s+(file|log)\b", 0.55, "write secrets to file"),
    ]
    for pattern, weight, label in exfil_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    # Check planned actions for external calls
    ext_action_keywords = ["curl", "wget", "http.post", "requests.post", "fetch(", "upload"]
    for action in planned_actions:
        for kw in ext_action_keywords:
            if kw.lower() in action.lower():
                score += 0.25
                evidence.append(f"planned action contains '{kw}'")
                break

    if score >= 0.4:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="data_exfiltration_path",
            signal="Execution path may route sensitive data to external destinations",
            confidence=conf,
            severity="high" if conf > 0.6 else "medium",
            evidence=evidence,
            mitigation="Block or audit outbound network calls; redact secrets before transmission",
        )
    return None


def _predict_privilege_escalation(prompt: str, planned_actions: List[str]) -> Optional[PredictedRisk]:
    """Predict attempts to gain higher privileges during execution."""
    evidence: List[str] = []
    score = 0.0

    priv_patterns = [
        (r"\bsudo\b", 0.4, "sudo usage"),
        (r"\bchmod\s+[0-7]*7[0-7]\b", 0.35, "world-writable chmod"),
        (r"\b(add|grant|give)\s+(admin|root|superuser)\s+(access|permission|privilege|account)\b", 0.5, "grant admin"),
        (r"\bsetuid\b|\bsetgid\b", 0.45, "setuid/setgid manipulation"),
        (r"\b(add|modify|edit)\s+(user\s+to\s+)?sudoers\b", 0.65, "sudoers/passwd modification"),
        (r"\brunas\b|\brun\s+as\s+(admin|root|system)\b", 0.4, "run as admin/root"),
        (r"\benable\s+(root|administrator)\s+(account|access)\b", 0.5, "enable root account"),
    ]
    for pattern, weight, label in priv_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="privilege_escalation",
            signal="Execution may attempt to gain elevated system privileges",
            confidence=conf,
            severity="critical" if conf > 0.6 else "high",
            evidence=evidence,
            mitigation="Run in sandboxed/unprivileged context; require explicit user approval",
        )
    return None


def _predict_multi_turn_grooming(
    prompt: str,
    conversation_history: Optional[List[str]] = None,
) -> Optional[PredictedRisk]:
    """Predict multi-turn social engineering / context poisoning."""
    evidence: List[str] = []
    score = 0.0

    grooming_patterns = [
        (r"\b(remember|keep\s+in\s+mind)\s+(that|this)\b.*\b(you\s+(are|should|must|can)\b)", 0.4, "identity nudge"),
        (r"\byou\s+(agreed|said|told me)\s+(earlier|before|last time)\b", 0.35, "false prior agreement"),
        (r"\bour\s+(previous|past|earlier)\s+(agreement|conversation|discussion)\b", 0.3, "appeal to false history"),
        (r"\b(from\s+now\s+on|always|never\s+again)\s+(you\s+(should|must|will))\b", 0.4, "persistent rule injection"),
        (r"\btreat\s+(this|me|us)\s+as\s+(trusted|admin|root|authorized)\b", 0.5, "trust escalation"),
        (r"\byou\s+(are|were)\s+pretending\s+to\s+be\b", 0.35, "persona manipulation"),
    ]
    for pattern, weight, label in grooming_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    # History analysis: rapid topic shifts = possible context poisoning
    if conversation_history and len(conversation_history) >= 3:
        # Crude topic shift heuristic: check if latest prompt is very different from history
        recent = " ".join(conversation_history[-3:]).lower()
        current_words = set(re.findall(r"\b\w{5,}\b", prompt.lower()))
        history_words = set(re.findall(r"\b\w{5,}\b", recent))
        overlap = len(current_words & history_words) / max(len(current_words), 1)
        if overlap < 0.05 and len(current_words) > 5:
            score += 0.25
            evidence.append("abrupt topic shift from conversation history")

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="multi_turn_grooming",
            signal="Prompt may be attempting to establish false context or erode safety boundaries over multiple turns",
            confidence=conf,
            severity="high" if conf > 0.5 else "medium",
            evidence=evidence,
            mitigation="Treat persistent identity/rule claims with skepticism; re-validate on each turn",
        )
    return None


def _predict_dependency_confusion(prompt: str, planned_actions: List[str]) -> Optional[PredictedRisk]:
    """Predict supply-chain / dependency confusion risks in install commands."""
    evidence: List[str] = []
    score = 0.0

    dep_patterns = [
        (r"\bpip\s+install\b.*\b(http|git\+|git://)", 0.4, "pip install from arbitrary URL"),
        (r"\bnpm\s+install\b.*\b(http|git\+|github:)", 0.35, "npm install from arbitrary source"),
        (r"\bcurl\b.*(sh|bash|py)\s*\|", 0.55, "curl-pipe-shell pattern"),
        (r"\bwget\b.*(sh|bash|py)\s*\|\s*(ba)?sh", 0.55, "wget-pipe-shell pattern"),
        (r"\bpip\s+install\b.+--index-url\b", 0.4, "custom pip index"),
        (r"\bnpm\s+(config\s+set\s+registry|install.+--registry)\b", 0.4, "custom npm registry"),
    ]
    for pattern, weight, label in dep_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    for action in planned_actions:
        if re.search(r"\bcurl\b.+\|\s*(ba)?sh", action, re.I):
            score += 0.4
            evidence.append("planned action: curl-pipe-shell")

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="dependency_confusion",
            signal="Install or fetch operations may pull untrusted or malicious packages",
            confidence=conf,
            severity="high",
            evidence=evidence,
            mitigation="Pin dependencies with hashes; use trusted registries only; avoid pipe-to-shell patterns",
        )
    return None


def _predict_ambiguous_destructive_intent(prompt: str) -> Optional[PredictedRisk]:
    """Predict vague prompts that could accidentally cause irreversible damage."""
    evidence: List[str] = []
    score = 0.0

    destructive_patterns = [
        (r"\b(clean\s*up|cleanup|purge|wipe|clear)\s+(all|everything|the\s+(whole|entire))\b", 0.4, "broad cleanup"),
        (r"\bdelete\s+(all|everything|every\s+file)\b", 0.5, "delete all"),
        (r"\bdrop\s+(all\s+tables|the\s+database|schema)\b", 0.55, "drop database/tables"),
        (r"\b(reset|rollback)\s+(everything|the\s+(whole|entire)\s+(system|db|database))\b", 0.45, "broad reset"),
        (r"\bformat\s+(the\s+)?(disk|drive|partition|volume)\b", 0.6, "disk format"),
        (r"\b(overwrite|replace)\s+(all|every)\b", 0.35, "overwrite all"),
    ]
    for pattern, weight, label in destructive_patterns:
        if re.search(pattern, prompt, re.I):
            score += weight
            evidence.append(label)

    if score >= 0.35:
        conf = min(score, 1.0)
        return PredictedRisk(
            category="ambiguous_destructive_intent",
            signal="Prompt contains broad or vague destructive operations that may cause irreversible damage",
            confidence=conf,
            severity="critical" if conf > 0.6 else "high",
            evidence=evidence,
            mitigation="Request explicit confirmation and scope limits before proceeding with destructive operations",
        )
    return None


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

_SEVERITY_WEIGHT = {"low": 1, "medium": 2, "high": 3, "critical": 4}

def _overall_level(risks: List[PredictedRisk]) -> str:
    if not risks:
        return "none"
    max_w = max(_SEVERITY_WEIGHT.get(r.severity, 1) for r in risks)
    if max_w >= 4:
        return "high"
    if max_w >= 3:
        return "high"
    if max_w >= 2:
        return "medium"
    return "low"


def predict_risks(
    user_prompt: str,
    planned_actions: Optional[List[str]] = None,
    conversation_history: Optional[List[str]] = None,
) -> PredictiveReport:
    """Run all predictors and return a consolidated PredictiveReport.

    This function is intentionally side-effect free and pure.
    """
    planned_actions = planned_actions or []
    conversation_history = conversation_history or []

    predictors = [
        _predict_resource_exhaustion(user_prompt, planned_actions),
        _predict_scope_creep(user_prompt, planned_actions),
        _predict_data_exfiltration_path(user_prompt, planned_actions),
        _predict_privilege_escalation(user_prompt, planned_actions),
        _predict_multi_turn_grooming(user_prompt, conversation_history),
        _predict_dependency_confusion(user_prompt, planned_actions),
        _predict_ambiguous_destructive_intent(user_prompt),
    ]

    risks = [r for r in predictors if r is not None]

    # Sort by severity desc, then confidence desc
    risks.sort(key=lambda r: (_SEVERITY_WEIGHT.get(r.severity, 1), r.confidence), reverse=True)

    top_concerns = [r.signal for r in risks[:3]]
    recommended_actions = list(dict.fromkeys(r.mitigation for r in risks))  # deduplicated

    avg_conf = sum(r.confidence for r in risks) / len(risks) if risks else 0.0

    return PredictiveReport(
        overall_risk_level=_overall_level(risks),
        predicted_risks=risks,
        top_concerns=top_concerns,
        recommended_actions=recommended_actions,
        confidence_summary=avg_conf,
    )
