"""
agent_finalize_1on1.py — Merge agent-produced LLM output into the final SkillOutput artifact.

Usage:
    python scripts/agent_finalize_1on1.py --login jsmith
    python scripts/agent_finalize_1on1.py --login jsmith --input-dir .pullstar --output-dir .pullstar

Reads:
    .pullstar/score_{login}.json        (required — provides scored profile and metadata)
    .pullstar/ingest_{login}.json       (optional — provides engineer_name and org)
    .pullstar/llm_output_{login}.json   (required — agent-produced brief)

Writes:
    .pullstar/output_{login}.json       (final SkillOutput artifact, same schema as generate_brief.py)

Expected llm_output format (two accepted forms):

  JSON (preferred):
    {
      "version":        "1.0",
      "engineer_login": str,
      "brief":          str   (non-empty markdown brief)
    }

  Plain text (accepted):
    The entire file content is used as the brief directly.
    Useful when copying raw output from a chat interface.

Fails clearly (non-zero exit, no output written) if:
    - score file is missing
    - llm_output file is missing
    - brief is empty (either the JSON field or the plain-text file)
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def fail(msg: str) -> NoReturn:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge agent-produced LLM output into the final PullStar SkillOutput."
    )
    parser.add_argument("--login",      required=True,       help="Engineer GitHub login")
    parser.add_argument("--input-dir",  default=".pullstar", help="Directory containing score, ingest, and llm_output files")
    parser.add_argument("--output-dir", default=".pullstar", help="Directory to write output_{login}.json")
    args = parser.parse_args()

    input_dir  = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    # -- Load score (required) ------------------------------------------------
    score_path = input_dir / f"score_{args.login}.json"
    if not score_path.exists():
        fail(f"Score file not found: {score_path}\n  Run: python scripts/score.py --login {args.login}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    print(f"> Score loaded — {score['engineer_login']} "
          f"{score['total_score']}/100 ({score['confidence']} confidence)")

    # -- Load ingest (optional) -----------------------------------------------
    ingest_path = input_dir / f"ingest_{args.login}.json"
    ingest: dict | None = None
    if ingest_path.exists():
        ingest = json.loads(ingest_path.read_text(encoding="utf-8"))
        assert ingest is not None
        print(f"> Ingest loaded — engineer_name={ingest.get('engineer_name')!r}, "
              f"org={ingest.get('org')!r}")
    else:
        print("> No ingest file — engineer_name and org will be null/empty in output")

    # -- Load llm_output (required) -------------------------------------------
    llm_output_path = input_dir / f"llm_output_{args.login}.json"
    if not llm_output_path.exists():
        fail(
            f"LLM output file not found: {llm_output_path}\n"
            f"  An agent must write this file before finalize can run.\n"
            f"  Expected schema: {{\"version\": \"1.0\", \"engineer_login\": \"{args.login}\", \"brief\": \"...\"}}\n"
            f"  Plain text (raw model output) is also accepted — the full file content will be used as the brief."
        )

    raw_content = llm_output_path.read_text(encoding="utf-8")

    # Try JSON first; fall back to treating the whole file as plain-text brief.
    # Plain text is common when copying output directly from a chat interface.
    brief: str
    try:
        llm_output = json.loads(raw_content)
        print(f"> LLM output loaded as JSON from {llm_output_path}")

        # Cross-check engineer_login if present
        output_login = llm_output.get("engineer_login", "")
        if output_login and output_login != args.login:
            fail(
                f"engineer_login mismatch: --login={args.login!r} but "
                f"llm_output.engineer_login={output_login!r}"
            )

        brief = llm_output.get("brief", "")
        if not isinstance(brief, str) or not brief.strip():
            fail(
                f"Invalid llm_output: 'brief' field is missing or empty.\n"
                f"  File: {llm_output_path}\n"
                f"  The agent must populate 'brief' with a non-empty markdown string."
            )

    except json.JSONDecodeError:
        # File is plain text — treat the entire content as the brief.
        print(f"  (file is plain text, not JSON — using full content as brief)",
              file=sys.stderr)
        brief = raw_content
        if not brief.strip():
            fail(
                f"llm_output file is empty.\n"
                f"  File: {llm_output_path}\n"
                f"  Write the brief text (or valid JSON) before running finalize."
            )

    print(f"> Brief validated — {len(brief)} chars")

    # -- Write final output ---------------------------------------------------
    # brief comes exclusively from llm_output — always overwrites any prior file
    output = {
        "version":        "1.0",
        "mode":           "agent",
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "engineer_login": score["engineer_login"],
        "engineer_name":  (ingest or {}).get("engineer_name"),
        "org":            (ingest or {}).get("org", ""),
        "lookback_days":  score["lookback_days"],
        "scored_profile": score,
        "brief":          brief,
    }

    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"output_{args.login}.json"
    tmp_path    = output_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    tmp_path.replace(output_path)

    print(f"> Output written to {output_path}")
    print("""
[OK] PullStar brief generated successfully.

If this was useful, you can join the early access list for PullStar Pro:
https://savory-step-9d7.notion.site/32fc2b5d4feb8054b937f54c753ff73b?pvs=105

PullStar Pro will explore:
- longitudinal trends across time
- team-level patterns
- coaching and pairing signals
- workflow integrations

Thanks for trying PullStar.""")


if __name__ == "__main__":
    main()
