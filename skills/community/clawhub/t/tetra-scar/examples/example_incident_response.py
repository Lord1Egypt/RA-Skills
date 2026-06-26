#!/usr/bin/env python3
"""Incident response with scar-safety.

Run: python3 example_incident_response.py

Simulates a secret leak incident, records it as a scar,
then shows the reflex arc blocking the same mistake next time.
"""
import sys, os, tempfile, shutil

# Add parent dirs so we can import scar_safety
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "tetra-scar-safety",
))
from scar_safety import safety_check, record_incident, load_safety_scars, reflex_block

# ---------------------------------------------------------------------------
# Simulated agent actions
# ---------------------------------------------------------------------------
ACTIONS = {
    "commit_with_secret": (
        "git add config.py && git commit -m 'update config'\n"
        "# config.py contains: API_KEY = 'sk-proj-abc123def456ghi789'"
    ),
    "log_token": (
        "print(f'Debug: user token is {access_token}')\n"
        "logger.info(f'Auth header: Bearer {jwt_secret}')"
    ),
    "safe_deploy": (
        "Run test suite, build Docker image, deploy to staging"
    ),
    "post_with_key": (
        "Send bearer token via curl: "
        "curl -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.secret' "
        "https://api.example.com/data"
    ),
}


def header(text: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def check_and_report(label: str, action: str, scar_file: str) -> dict:
    """Run safety_check and print result."""
    print(f"\n  Action: {label}")
    print(f"  Detail: {action[:70]}...")

    result = safety_check(action, scar_file=scar_file)

    if result["safe"]:
        print(f"  Result: SAFE -- {result['reason']}")
    else:
        print(f"  Result: BLOCKED [{result['severity']}]")
        print(f"          {result['reason']}")
        for d in result.get("details", [])[1:]:
            print(f"          also: [{d['severity']}] {d['reason']}")
    return result


def main():
    tmp = tempfile.mkdtemp(prefix="scar_safety_demo_")
    scar_file = os.path.join(tmp, "safety_scars.jsonl")

    try:
        header("scar-safety: Incident Response Demo")
        print("  An agent leaks a secret. The scar prevents it from ever")
        print("  happening again -- without any LLM calls.")

        # ------------------------------------------------------------------
        # ACT 1: Built-in detection catches a secret in code
        # ------------------------------------------------------------------
        header("ACT 1: Built-in threat detection")
        print("  (No scars yet. Pure regex detection.)")

        r1 = check_and_report(
            "Commit config with API key",
            ACTIONS["commit_with_secret"],
            scar_file,
        )
        assert not r1["safe"], "Should have been blocked"

        r2 = check_and_report(
            "Deploy to staging",
            ACTIONS["safe_deploy"],
            scar_file,
        )
        assert r2["safe"], "Should be safe"

        # ------------------------------------------------------------------
        # ACT 2: Incident happens -- secret was logged, not in code
        # ------------------------------------------------------------------
        header("ACT 2: Incident -- secret leaked via debug logging")
        print("  The built-in detector missed this because the token was")
        print("  in a variable, not a hardcoded string. Production logs")
        print("  were scraped by an attacker.")

        print("\n  Recording incident as scar...")
        scar = record_incident(
            what_happened=(
                "JWT secret leaked via debug logging. "
                "print(f'token is {access_token}') exposed bearer tokens "
                "in production logs. Attacker scraped CloudWatch."
            ),
            never_allow=(
                "Never log or print access_token, jwt_secret, bearer token, "
                "or any credential variable to stdout, stderr, or logger. "
                "Use [REDACTED] placeholder instead."
            ),
            severity="CRITICAL",
            scar_file=scar_file,
        )
        print(f"  SCAR RECORDED: {scar['id']}")
        print(f"  What happened: {scar['what_happened'][:70]}...")
        print(f"  Never allow:   {scar['never_allow'][:70]}...")

        # ------------------------------------------------------------------
        # ACT 3: Reflex arc blocks similar actions
        # ------------------------------------------------------------------
        header("ACT 3: Reflex arc in action (with scar)")
        print("  Now the agent tries similar actions. The reflex arc")
        print("  pattern-matches against the scar -- no LLM needed.")

        r3 = check_and_report(
            "Log user token for debugging",
            ACTIONS["log_token"],
            scar_file,
        )
        assert not r3["safe"], "Should be blocked by scar reflex"

        r4 = check_and_report(
            "POST request with secret key",
            ACTIONS["post_with_key"],
            scar_file,
        )
        # This is caught by built-in exfil detection too
        assert not r4["safe"], "Should be blocked"

        r5 = check_and_report(
            "Safe deployment",
            ACTIONS["safe_deploy"],
            scar_file,
        )
        assert r5["safe"], "Should still be safe"

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        header("RESULT")
        scars = load_safety_scars(scar_file)
        print(f"\n  Safety scars in memory: {len(scars)}")
        for s in scars:
            print(f"    [{s['severity']}] {s['what_happened'][:50]}...")

        print(f"""
  Timeline:
    1. Built-in detection caught hardcoded API key    (regex)
    2. Debug logging leaked a token                   (missed by regex)
    3. Incident recorded as scar                      (one line of code)
    4. Reflex arc now blocks token logging             (keyword match)
    5. Safe actions still pass                         (no false positives)

  The scar is permanent. Even if the agent is restarted,
  the JSONL file persists. The reflex arc fires in microseconds.
  No LLM. No API calls. No latency. Just pattern matching.""")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
