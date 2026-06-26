#!/usr/bin/env python3
"""
sleep_cycle.py — AI Agent NREM + REM Memory Consolidation (v2)

Two-track NREM based on Eichenlaub et al. 2020:
  Fast track  (compressed replay 0.1x): high-confidence → MEMORY.md
  Slow track  (dilated replay 1.5-2x) : weakly-learned  → bank/

Usage:
  python scripts/sleep_cycle.py --phase both --workspace ~/.agent_workspace
  python scripts/sleep_cycle.py --phase nrem --workspace ./ws
  python scripts/sleep_cycle.py --phase rem  --workspace ./ws --prune-memory
"""

import argparse
import json
import os
import sys
import http.client
from datetime import date, datetime
from pathlib import Path


# ── Prompts ────────────────────────────────────────────────────────────────────

NREM_SYSTEM = """You simulate NREM deep-sleep memory consolidation for an AI agent.

Two-track processing based on neural replay research (Eichenlaub et al. 2020):

FAST TRACK (compressed replay — high-confidence, clear facts → MEMORY.md):
- Distill into single-sentence durable memories
- Prune ~20% as redundant (synaptic homeostasis)
- Use type prefixes: W=world fact, B=experience, O(c=N)=opinion+confidence, S=summary
- Only add to MEMORY.md what truly warrants long-term retention

SLOW TRACK (dilated replay — weakly-learned, uncertain → bank/):
- Expand on items with low confidence or partial understanding
- These are what NREM prioritizes (replay strength ∝ weakness of encoding)
- Write as structured Markdown for bank/entities/ or bank/concepts/

Respond ONLY with valid JSON, no markdown fences:
{
  "memory_md_updates": [
    {
      "action": "add|update|remove",
      "type": "W|B|O|S",
      "confidence": 0.85,
      "text": "single clear sentence",
      "replaces": "old text verbatim if action=update, else null"
    }
  ],
  "bank_updates": [
    {
      "slug": "kebab-case-slug",
      "kind": "entity|concept",
      "section": "## Section heading",
      "content": "markdown block content"
    }
  ],
  "pruned_count": 2,
  "weakly_learned": ["items that need more attention next session"],
  "open_questions": ["gaps or unknowns raised by today's session"]
}"""

REM_SYSTEM = """You simulate REM dream-sleep creative synthesis for an AI agent.
The dreaming brain makes non-obvious connections across domains.

Tasks:
1. Find surprising cross-domain links between today's memories and MEMORY.md
2. Update O(c=N) confidence values where today's evidence shifted beliefs
3. Propose new bank/ pages if a topic recurred 3+ times
4. Generate concrete, specific next-session actions

Be creative but grounded in the provided memories. No invention.

Respond ONLY with valid JSON, no markdown fences:
{
  "aha_moments": ["surprising insight string"],
  "creative_connections": [
    {"link": "Concept A ↔ Concept B", "why": "why this matters"}
  ],
  "confidence_updates": [
    {"item": "verbatim text excerpt from MEMORY.md", "old_c": 0.7, "new_c": 0.9, "reason": "string"}
  ],
  "new_bank_suggestions": [
    {"slug": "kebab-case", "kind": "entity|concept", "seed_content": "## Overview\\n..."}
  ],
  "next_session_actions": ["specific action item"]
}"""


# ── API ────────────────────────────────────────────────────────────────────────

def call_claude(system_prompt: str, user_message: str, model: str = "claude-sonnet-4-20250514") -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set")
    payload = json.dumps({
        "model": model,
        "max_tokens": 2000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }).encode()
    conn = http.client.HTTPSConnection("api.anthropic.com")
    conn.request("POST", "/v1/messages", payload, {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    })
    resp = conn.getresponse()
    body = json.loads(resp.read().decode())
    conn.close()
    if "error" in body:
        raise RuntimeError(f"API error: {body['error']['message']}")
    return body["content"][0]["text"]


def parse_json(raw: str) -> dict:
    cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"  [warn] JSON parse failed: {e}", file=sys.stderr)
        return {}


# ── Workspace helpers ──────────────────────────────────────────────────────────

class Workspace:
    def __init__(self, root: str):
        self.root = Path(root).expanduser()
        self.memory_dir = self.root / "memory"
        self.bank_dir = self.root / "bank"
        self.memory_md = self.root / "MEMORY.md"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        (self.bank_dir / "entities").mkdir(parents=True, exist_ok=True)
        (self.bank_dir / "concepts").mkdir(parents=True, exist_ok=True)

    def today_log(self) -> Path:
        return self.memory_dir / f"{date.today()}.md"

    def yesterday_log(self) -> Path:
        from datetime import timedelta
        return self.memory_dir / f"{date.today() - timedelta(days=1)}.md"

    def read_daily_log(self) -> str:
        parts = []
        for p in [self.today_log(), self.yesterday_log()]:
            if p.exists():
                parts.append(f"### {p.name}\n{p.read_text(encoding='utf-8')}")
        return "\n\n".join(parts) if parts else "(no daily log entries yet)"

    def read_memory_md(self, max_chars: int = 6000) -> str:
        if not self.memory_md.exists():
            return "(MEMORY.md is empty — first session)"
        text = self.memory_md.read_text(encoding="utf-8")
        return text[:max_chars] + ("\n...[truncated]" if len(text) > max_chars else "")

    def list_bank_slugs(self) -> list[str]:
        slugs = []
        for subdir in ["entities", "concepts"]:
            for f in (self.bank_dir / subdir).glob("*.md"):
                slugs.append(f"{subdir}/{f.stem}")
        return slugs

    def apply_nrem(self, result: dict):
        """Write NREM results to MEMORY.md and bank/."""
        updates = result.get("memory_md_updates", [])
        if updates:
            self._update_memory_md(updates)

        for bu in result.get("bank_updates", []):
            slug = bu.get("slug", "unknown")
            kind = bu.get("kind", "concepts")
            section = bu.get("section", "## Notes")
            content = bu.get("content", "")
            subdir = "entities" if kind == "entity" else "concepts"
            bank_file = self.bank_dir / subdir / f"{slug}.md"
            if bank_file.exists():
                existing = bank_file.read_text(encoding="utf-8")
                if section not in existing:
                    bank_file.write_text(
                        existing.rstrip() + f"\n\n{section}\n{content}\n",
                        encoding="utf-8"
                    )
            else:
                bank_file.write_text(
                    f"# {slug.replace('-', ' ').title()}\n\n{section}\n{content}\n",
                    encoding="utf-8"
                )

    def apply_rem(self, result: dict, nrem_result: dict):
        """Append REM insights to MEMORY.md and suggest bank pages."""
        ahas = result.get("aha_moments", [])
        connections = result.get("creative_connections", [])
        actions = result.get("next_session_actions", [])
        conf_updates = result.get("confidence_updates", [])
        new_bank = result.get("new_bank_suggestions", [])

        # Update confidence values in MEMORY.md
        if conf_updates and self.memory_md.exists():
            text = self.memory_md.read_text(encoding="utf-8")
            for cu in conf_updates:
                old_item = cu.get("item", "")
                new_c = cu.get("new_c", 0)
                import re
                # Update O(c=old) → O(c=new) inline
                pattern = re.escape(old_item)
                replacement = re.sub(r"O\(c=[\d.]+\)", f"O(c={new_c:.2f})", old_item)
                text = text.replace(old_item, replacement)
            self.memory_md.write_text(text, encoding="utf-8")

        # Append REM insights section to MEMORY.md
        rem_block = f"\n\n## REM Synthesis — {date.today()}\n"
        if ahas:
            rem_block += "\n### Insights\n" + "\n".join(f"- {a}" for a in ahas)
        if connections:
            rem_block += "\n### Creative connections\n" + "\n".join(
                f"- {c['link']}: {c['why']}" for c in connections
            )
        if actions:
            rem_block += "\n### Next session\n" + "\n".join(f"- [ ] {a}" for a in actions)

        with open(self.memory_md, "a", encoding="utf-8") as f:
            f.write(rem_block + "\n")

        # Seed new bank pages
        for nb in new_bank:
            slug = nb.get("slug", "new-topic")
            kind = nb.get("kind", "concepts")
            seed = nb.get("seed_content", "")
            subdir = "entities" if kind == "entity" else "concepts"
            bank_file = self.bank_dir / subdir / f"{slug}.md"
            if not bank_file.exists():
                bank_file.write_text(
                    f"# {slug.replace('-', ' ').title()}\n\n{seed}\n",
                    encoding="utf-8"
                )

    def _update_memory_md(self, updates: list[dict]):
        lines = []
        if self.memory_md.exists():
            lines = self.memory_md.read_text(encoding="utf-8").splitlines()

        today_header = f"## Session {date.today()}"
        # Find or create today's section
        try:
            idx = next(i for i, l in enumerate(lines) if today_header in l)
        except StopIteration:
            lines.append("")
            lines.append(today_header)
            idx = len(lines) - 1

        for u in updates:
            action = u.get("action", "add")
            t = u.get("type", "W")
            c = u.get("confidence", 1.0)
            text = u.get("text", "")
            replaces = u.get("replaces")

            prefix = f"{t}(c={c:.2f})" if t == "O" else t
            new_line = f"- {prefix}: {text}"

            if action == "remove" and replaces:
                lines = [l for l in lines if replaces not in l]
            elif action == "update" and replaces:
                lines = [new_line if replaces in l else l for l in lines]
            else:  # add
                lines.append(new_line)

        self.memory_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def prune_memory(self):
        """Remove duplicate or superseded lines from MEMORY.md."""
        if not self.memory_md.exists():
            return 0
        lines = self.memory_md.read_text(encoding="utf-8").splitlines()
        seen = set()
        deduped = []
        removed = 0
        for line in lines:
            key = line.strip().lower()
            if key and key.startswith("- ") and key in seen:
                removed += 1
                continue
            seen.add(key)
            deduped.append(line)
        self.memory_md.write_text("\n".join(deduped) + "\n", encoding="utf-8")
        return removed


# ── Report ─────────────────────────────────────────────────────────────────────

def print_report(ws: Workspace, nrem: dict | None, rem: dict | None, session_num: int):
    bar = "═" * 52
    print(f"\n{bar}")
    print(f"  SLEEP CYCLE COMPLETE  |  session #{session_num}  |  {date.today()}")
    print(bar)

    if nrem:
        added = [u for u in nrem.get("memory_md_updates", []) if u.get("action") != "remove"]
        pruned = nrem.get("pruned_count", 0)
        weak = nrem.get("weakly_learned", [])
        bank = nrem.get("bank_updates", [])
        print(f"\nNREM — {len(added)} memory update(s), {pruned} pruned, {len(bank)} bank write(s)")
        for u in added:
            t = u.get("type", "W")
            c = u.get("confidence", 1.0)
            icon = "●" if c >= 0.8 else "○" if c >= 0.5 else "·"
            print(f"  {icon} [{t} c={c:.2f}] {u.get('text', '')}")
        if weak:
            print(f"  ↻ Slow-track ({len(weak)} weakly-learned):")
            for w in weak[:3]:
                print(f"    ? {w}")
        if nrem.get("open_questions"):
            print(f"  Open questions:")
            for q in nrem["open_questions"][:3]:
                print(f"    ? {q}")

    if rem:
        ahas = rem.get("aha_moments", [])
        conns = rem.get("creative_connections", [])
        actions = rem.get("next_session_actions", [])
        conf = rem.get("confidence_updates", [])
        print(f"\nREM — {len(ahas)} insight(s), {len(conns)} connection(s), {len(conf)} confidence update(s)")
        for a in ahas:
            print(f"  ★ {a}")
        for c in conns:
            print(f"  ↔ {c.get('link')} — {c.get('why')}")
        if actions:
            print(f"\n  Next session:")
            for a in actions:
                print(f"  → {a}")

    print(f"\n  Workspace: {ws.root}")
    print(f"  MEMORY.md: {ws.memory_md}")
    print(bar + "\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", "-w", default="~/.agent_workspace")
    p.add_argument("--phase", choices=["nrem", "rem", "both"], default="both")
    p.add_argument("--model", default="claude-sonnet-4-20250514")
    p.add_argument("--prune-memory", action="store_true", help="Deduplicate MEMORY.md before cycle")
    args = p.parse_args()

    ws = Workspace(args.workspace)

    # Load state
    daily_log = ws.read_daily_log()
    memory_md = ws.read_memory_md()
    bank_slugs = ws.list_bank_slugs()

    # Count sessions for report
    session_count_file = ws.root / ".session_count"
    session_num = int(session_count_file.read_text()) + 1 if session_count_file.exists() else 1
    session_count_file.write_text(str(session_num))

    if args.prune_memory:
        removed = ws.prune_memory()
        print(f"  [prune] Removed {removed} duplicate lines from MEMORY.md", file=sys.stderr)
        memory_md = ws.read_memory_md()

    nrem_result = None
    rem_result = None

    if daily_log.strip() == "(no daily log entries yet)" and args.phase in ("nrem", "both"):
        print("  [warn] No daily log found — nothing to consolidate. Run micro_rest.py first.", file=sys.stderr)
        return

    try:
        if args.phase in ("nrem", "both"):
            print("  [nrem] Two-track consolidation...", file=sys.stderr)
            user_msg = (
                f"Today's daily log:\n{daily_log}\n\n"
                f"Current MEMORY.md:\n{memory_md}\n\n"
                f"Existing bank slugs: {bank_slugs}"
            )
            raw = call_claude(NREM_SYSTEM, user_msg, args.model)
            nrem_result = parse_json(raw)
            if nrem_result:
                ws.apply_nrem(nrem_result)
                print(f"  [nrem] Done — {len(nrem_result.get('memory_md_updates', []))} updates", file=sys.stderr)

        if args.phase in ("rem", "both"):
            print("  [rem] Creative synthesis...", file=sys.stderr)
            nrem_ctx = json.dumps(nrem_result, ensure_ascii=False) if nrem_result else "(nrem skipped)"
            user_msg = (
                f"NREM result:\n{nrem_ctx}\n\n"
                f"Current MEMORY.md:\n{memory_md}\n\n"
                f"Today's log:\n{daily_log}"
            )
            raw = call_claude(REM_SYSTEM, user_msg, args.model)
            rem_result = parse_json(raw)
            if rem_result:
                ws.apply_rem(rem_result, nrem_result or {})
                print(f"  [rem] Done — {len(rem_result.get('aha_moments', []))} insights", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise

    print_report(ws, nrem_result, rem_result, session_num)


if __name__ == "__main__":
    main()
