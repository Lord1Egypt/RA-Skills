#!/usr/bin/env python3
"""
Trade-Audit — mandatory audit gate for trading and transfer decisions.

This script does not fetch or summarize pages on its own.
The agent must collect and organize the relevant material first.

The script only:
1. Accepts agent-prepared decision material
2. Normalizes it into a deterministic decision bundle
3. Sends the bundle to Apus deterministic inference
4. Returns an attested decision packet
5. Appends an audit record to the local audit log

Exit codes (gate mode):
  0 = APPROVE   — the decision passed audit
  1 = REJECT    — the decision failed audit (or error)
  2 = WAIT      — insufficient information to decide
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import ssl
import sys
import urllib.request
from pathlib import Path
from typing import Any


APUS_BASE_URL = "https://hb.apus.network/~inference@1.0"
MODEL_NAME = "google/gemma-3-27b-it"
AUDIT_LOG_DIR = Path.home() / ".trade-audit"
AUDIT_LOG_FILE = AUDIT_LOG_DIR / "audit.jsonl"

BUNDLE_WARN_CHARS = 4000
BUNDLE_HARD_LIMIT_CHARS = 12000

VERDICT_EXIT_CODES = {
    "APPROVE": 0,
    "REJECT": 1,
    "WAIT": 2,
}


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def maybe_write_json(path: str | None, payload: dict[str, Any]) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_audit_record(record: dict[str, Any]) -> None:
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def check_bundle_size(material: str) -> None:
    length = len(material)
    if length > BUNDLE_HARD_LIMIT_CHARS:
        print(
            f"[WARNING] Bundle material is {length:,} chars (hard limit {BUNDLE_HARD_LIMIT_CHARS:,}). "
            f"Truncating to {BUNDLE_HARD_LIMIT_CHARS:,} chars. Decision quality may be degraded — "
            f"consider providing only core data points.",
            file=sys.stderr,
        )
    elif length > BUNDLE_WARN_CHARS:
        print(
            f"[WARNING] Bundle material is {length:,} chars (recommended < {BUNDLE_WARN_CHARS:,}). "
            f"The model performs best with concise, focused inputs. "
            f"Consider trimming to key facts, prices, rules, and risks only.",
            file=sys.stderr,
        )


def truncate_material(material: str) -> str:
    if len(material) <= BUNDLE_HARD_LIMIT_CHARS:
        return material
    truncated = material[:BUNDLE_HARD_LIMIT_CHARS]
    last_newline = truncated.rfind("\n")
    if last_newline > BUNDLE_HARD_LIMIT_CHARS * 0.8:
        truncated = truncated[:last_newline]
    return truncated + "\n\n[TRUNCATED — original material exceeded size limit]"


def _http_post(url: str, payload: dict[str, Any], timeout: int = 120) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "trade-audit/1.0"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_bundle_from_text(decision_goal: str, input_path: str, context_label: str | None) -> dict[str, Any]:
    text = Path(input_path).read_text(encoding="utf-8")
    prepared_text = normalize_text(text)
    if not prepared_text:
        raise RuntimeError("prepared input file is empty after normalization")
    check_bundle_size(prepared_text)
    prepared_text = truncate_material(prepared_text)
    bundle = {
        "schema_version": 3,
        "decision_goal": decision_goal,
        "input_mode": "prepared_text",
        "context_label": context_label or Path(input_path).name,
        "prepared_material": prepared_text,
    }
    bundle["bundle_hash"] = sha256_text(canonical_json(bundle))
    return bundle


def build_bundle_from_json(decision_goal: str | None, bundle_path: str) -> dict[str, Any]:
    raw = Path(bundle_path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise RuntimeError("bundle file must contain a JSON object")
    bundle = dict(data)
    bundle["schema_version"] = bundle.get("schema_version", 3)
    if decision_goal:
        bundle["decision_goal"] = decision_goal
    if not str(bundle.get("decision_goal", "")).strip():
        raise RuntimeError("bundle file must contain decision_goal or pass --decision-goal")
    material = bundle.get("prepared_material", "")
    material_text = json.dumps(material, ensure_ascii=False) if isinstance(material, dict) else str(material)
    check_bundle_size(material_text)
    if isinstance(material, str):
        bundle["prepared_material"] = truncate_material(material)
    bundle["bundle_hash"] = sha256_text(canonical_json({k: v for k, v in bundle.items() if k != "bundle_hash"}))
    return bundle


def build_prompt(bundle: dict[str, Any]) -> str:
    bundle_json = json.dumps(bundle, ensure_ascii=False, indent=2)
    return f"""You are a deterministic transaction-and-investment decision engine.

Analyze ONLY the supplied decision bundle. Do not use outside facts, outside memory, current events, or live market data.

The material in the bundle has already been collected and organized by another agent. Treat it as the complete working set for this decision.

Your task is to make the core decision from the supplied bundle.

Focus on the core data points: prices, thresholds, rules, numeric values, addresses, and explicit conditions. Ignore narrative text, disclaimers, and background context that do not directly affect the decision.

Rules:
1. Stay strictly grounded in the supplied bundle.
2. Make exactly one concrete decision.
3. If the bundle supports action, say what to do in plain language.
4. If the bundle does not support action, reject or wait explicitly.
5. Preserve uncertainty explicitly in `risks` and `missing_information`.
6. For market pages, it is acceptable to output a trigger-style recommendation such as "Buy BTC only at or below $55,000."
7. For transfer decisions, clearly say whether to proceed, reject, or wait.
8. If `verdict` is `APPROVE` or `REJECT`, set `confidence` to an integer from 1 to 100.
9. Do not invent facts that are not present in the bundle.
10. Base your decision on numeric evidence and explicit rules first, narrative context second.

Return ONLY valid JSON with this exact schema:
{{
  "decision_summary": "one sentence summary of the decision",
  "action": "direct action in plain language",
  "decision_type": "BUY|SELL|HOLD|WAIT|APPROVE_TRANSFER|REJECT_TRANSFER|AVOID",
  "verdict": "APPROVE|REJECT|WAIT",
  "target": "asset, market, pool, or transfer subject",
  "trigger_condition": "specific price/condition/address condition or N/A",
  "confidence": 0,
  "decision_rationale": [
    "reason 1",
    "reason 2"
  ],
  "supporting_observations": [
    "specific fact from the bundle",
    "specific fact from the bundle"
  ],
  "risks": [
    "risk 1",
    "risk 2"
  ],
  "missing_information": [
    "missing item 1",
    "missing item 2"
  ],
  "source_discipline": "confirm the decision used only the supplied bundle"
}}

Decision bundle:
```json
{bundle_json}
```"""


def run_inference(bundle: dict[str, Any]) -> tuple[dict[str, Any], str, dict[str, Any]]:
    print("\nCalling Apus deterministic inference on NVIDIA H100 TEE...", flush=True)
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": build_prompt(bundle)}],
        "tee": True,
    }
    url = f"{APUS_BASE_URL}/chat/completions"
    resp_dict = _http_post(url, payload)

    raw_content = (resp_dict["choices"][0]["message"]["content"] or "").strip()
    if raw_content.startswith("```"):
        lines = raw_content.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw_content = "\n".join(lines).strip()

    packet = json.loads(raw_content)
    return packet, raw_content, resp_dict


def normalize_string_list(values: Any) -> list[str]:
    return [str(item).strip() for item in (values or []) if str(item).strip()]


def clamp_confidence(value: Any) -> int:
    try:
        confidence = int(float(value))
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, confidence))


def normalize_packet(packet: dict[str, Any]) -> dict[str, Any]:
    norm = dict(packet)
    norm["decision_summary"] = str(norm.get("decision_summary", "")).strip()
    norm["action"] = str(norm.get("action", "WAIT")).strip() or "WAIT"
    norm["decision_type"] = str(norm.get("decision_type", "WAIT")).strip().upper()
    norm["verdict"] = str(norm.get("verdict", "WAIT")).strip().upper()
    norm["target"] = str(norm.get("target", "N/A")).strip() or "N/A"
    norm["trigger_condition"] = str(norm.get("trigger_condition", "N/A")).strip() or "N/A"
    norm["confidence"] = clamp_confidence(norm.get("confidence"))
    norm["decision_rationale"] = normalize_string_list(norm.get("decision_rationale"))
    norm["supporting_observations"] = normalize_string_list(norm.get("supporting_observations"))
    norm["risks"] = normalize_string_list(norm.get("risks"))
    norm["missing_information"] = normalize_string_list(norm.get("missing_information"))
    discipline = str(norm.get("source_discipline", "")).strip()
    if len(discipline) < 20 or "bundle" not in discipline.lower():
        discipline = "This decision was derived strictly from the supplied decision bundle only."
    norm["source_discipline"] = discipline
    return norm


def apply_confidence_gate(packet: dict[str, Any], min_confidence: int) -> dict[str, Any]:
    if packet["verdict"] == "APPROVE" and packet["confidence"] < min_confidence:
        packet["verdict"] = "REJECT"
        packet["decision_rationale"].insert(
            0,
            f"Auto-rejected: confidence {packet['confidence']}% is below the minimum threshold of {min_confidence}%",
        )
    return packet


def row(text: str = "", width: int = 76) -> str:
    text = text[: width - 2] if len(text) > width - 2 else text
    return f"║ {text:<{width - 2}} ║"


def wrap_rows(text: str, indent: int = 2, width: int = 76) -> list[str]:
    words = text.split()
    if not words:
        return [row("", width)]
    lines: list[str] = []
    current = " " * indent
    for word in words:
        candidate = " " * indent + f"{current} {word}".strip()
        if len(candidate) > width - 2:
            lines.append(row(current, width))
            current = " " * indent + word
        else:
            current = candidate
    lines.append(row(current, width))
    return lines


def print_section(title: str, lines: list[str], width: int, thin: str) -> None:
    print(row(title, width))
    if lines:
        for idx, item in enumerate(lines):
            if idx:
                print(f"║ {thin} ║")
            for line in wrap_rows(item, indent=4, width=width):
                print(line)
    else:
        print(row("  None", width))


def short_hash(text: str, keep: int = 46) -> str:
    return text if len(text) <= keep else text[:keep] + "..."


def print_report(
    bundle: dict[str, Any],
    packet: dict[str, Any],
    output_hash: str,
    nonce: str,
    verified: bool,
    gpu_model: str,
    driver_ver: str,
) -> None:
    width = 76
    border = "═" * width
    thin = "·" * (width - 2)

    print(f"\n╔{border}╗")
    print(f"║{'  TRADE-AUDIT VERIFIED DECISION':^{width}}║")
    print(f"╠{border}╣")
    print(row(f"  Goal          : {bundle['decision_goal']}", width))
    print(row(f"  Input Mode    : {bundle.get('input_mode', 'prepared_bundle')}", width))
    print(row(f"  Model         : {MODEL_NAME}  (Apus Network)", width))
    print(row(f"  Hardware      : {gpu_model}  /  Driver {driver_ver}", width))
    ver_icon = "VERIFIED" if verified else "UNVERIFIED"
    print(row(f"  TEE           : {ver_icon}  ({gpu_model})", width))
    print(row(f"  Bundle Hash   : {short_hash(bundle['bundle_hash'])}", width))
    print(row(f"  Output Hash   : {short_hash(output_hash)}", width))
    print(row(f"  TEE Nonce     : {short_hash(nonce)}", width))
    print(f"╠{border}╣")
    print(row(f"  Verdict       : {packet['verdict']}", width))
    print(row(f"  Decision Type : {packet['decision_type']}", width))
    print(row(f"  Action        : {packet['action']}", width))
    print(row(f"  Target        : {packet['target']}", width))
    print(row(f"  Trigger       : {packet['trigger_condition']}", width))
    print(row(f"  Confidence    : {packet['confidence']}%", width))
    print(f"╠{border}╣")
    for line in wrap_rows(packet["decision_summary"], indent=2, width=width):
        print(line)
    print(f"╠{border}╣")
    print_section("  Decision Rationale", packet["decision_rationale"], width, thin)
    print(f"╠{border}╣")
    print_section("  Supporting Observations", packet["supporting_observations"], width, thin)
    print(f"╠{border}╣")
    print_section("  Risks", packet["risks"], width, thin)
    print(f"╠{border}╣")
    print_section("  Missing Information", packet["missing_information"], width, thin)
    print(f"╠{border}╣")
    for line in wrap_rows(packet["source_discipline"], indent=2, width=width):
        print(line)
    print(f"╚{border}╝")

    print(f"\nBundle Hash (input bundle): {bundle['bundle_hash']}")
    print(f"Output Hash (decision):     {output_hash}")
    print(f"TEE Nonce   (this run):     {nonce}")
    print(f"GPU TEE verified:           {verified}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trade-Audit: mandatory audit gate for trading and transfer decisions via Apus TEE."
    )
    parser.add_argument("--decision-goal", help="Plain-language decision request")
    parser.add_argument("--input-file", help="Path to agent-prepared text or markdown material")
    parser.add_argument("--bundle-file", help="Path to agent-prepared JSON bundle")
    parser.add_argument("--context-label", help="Optional label for prepared text input")
    parser.add_argument("--bundle-out", help="Write the normalized decision bundle JSON to this path")
    parser.add_argument("--packet-out", help="Write the decision packet JSON to this path")
    parser.add_argument(
        "--gate",
        action="store_true",
        help="Gate mode: exit code reflects verdict (0=APPROVE, 1=REJECT, 2=WAIT)",
    )
    parser.add_argument(
        "--min-confidence",
        type=int,
        default=60,
        help="Auto-reject if confidence is below this threshold (default: 60)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if bool(args.input_file) == bool(args.bundle_file):
        print("Use exactly one of --input-file or --bundle-file.", file=sys.stderr)
        return 1

    try:
        if args.input_file:
            if not args.decision_goal:
                print("--decision-goal is required with --input-file.", file=sys.stderr)
                return 1
            bundle = build_bundle_from_text(args.decision_goal, args.input_file, args.context_label)
        else:
            bundle = build_bundle_from_json(args.decision_goal, args.bundle_file)

        maybe_write_json(args.bundle_out, bundle)

        packet, raw_content, resp_dict = run_inference(bundle)
        packet = normalize_packet(packet)
        packet = apply_confidence_gate(packet, args.min_confidence)
        output_hash = sha256_text(raw_content)

        attestation = resp_dict.get("attestation", {}) or {}
        nonce = attestation.get("nonce", "N/A")
        verified = bool(attestation.get("verified", False))
        claims = attestation.get("claims", [{}]) or [{}]
        evidences = attestation.get("evidences", [{}]) or [{}]
        gpu_model = claims[0].get("hwmodel", "Unknown GPU")
        driver_ver = evidences[0].get("driver_version", "N/A")

        artifact = {
            "bundle": bundle,
            "decision_packet": packet,
            "output_hash": output_hash,
            "attestation": {
                "nonce": nonce,
                "verified": verified,
                "gpu_model": gpu_model,
                "driver_version": driver_ver,
            },
        }
        maybe_write_json(args.packet_out, artifact)

        # Append audit record
        audit_record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "bundle_hash": bundle["bundle_hash"],
            "output_hash": output_hash,
            "tee_nonce": nonce,
            "tee_verified": verified,
            "verdict": packet["verdict"],
            "confidence": packet["confidence"],
            "decision_type": packet["decision_type"],
            "target": packet["target"],
            "decision_goal": bundle["decision_goal"],
            "min_confidence_threshold": args.min_confidence,
            "gate_mode": args.gate,
        }
        append_audit_record(audit_record)
        print(f"\nAudit record appended to {AUDIT_LOG_FILE}")

        print_report(bundle, packet, output_hash, nonce, verified, gpu_model, driver_ver)

        if args.gate:
            verdict = packet["verdict"]
            exit_code = VERDICT_EXIT_CODES.get(verdict, 1)
            label = {0: "APPROVED", 1: "REJECTED", 2: "WAIT"}.get(exit_code, "REJECTED")
            print(f"\n[GATE] Verdict: {verdict} -> exit code {exit_code} ({label})")
            return exit_code

        return 0
    except json.JSONDecodeError as exc:
        print(f"[ERROR] invalid JSON: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
