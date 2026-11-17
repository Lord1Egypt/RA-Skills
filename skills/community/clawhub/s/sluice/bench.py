"""Reproducible benchmark on REAL outbound copy from this machine.

Two measurements:

  * RECALL  - on a fixtures set of realistic, freshly-minted secrets embedded in
              prose, what fraction does sluice catch? (secrets are synthetic, not
              live credentials.)
  * FALSE-POSITIVE RATE - scan every article we have actually published
              (workloft-site ships/notes/news) plus queued drafts. These are
              clean by construction; any HIGH/MEDIUM finding is a false alarm.

Run:  python3 bench.py
"""
import glob
import os
import secrets as _secrets
import string

from sluice.core import scan

HOME = "/home/workloft"
SITE = os.path.join(HOME, "workloft-site")

CLEAN_GLOBS = [
    os.path.join(SITE, "ships", "*.html"),
    os.path.join(SITE, "labs", "notes", "*.html"),
    os.path.join(SITE, "labs", "news", "*.html"),
    os.path.join(HOME, "drafts", "*.md"),
]


def _rand(n, alphabet=string.ascii_letters + string.digits):
    return "".join(_secrets.choice(alphabet) for _ in range(n))


def recall_fixtures():
    """Realistic shapes, synthetic values, wrapped in plausible prose."""
    hexs = string.hexdigits.lower()[:16]
    return [
        ("anthropic_key", f"export ANTHROPIC_API_KEY=sk-ant-api03-{_rand(80)}"),
        ("openrouter_key", f"OPENROUTER_KEY=sk-or-v1-{''.join(_secrets.choice(hexs) for _ in range(64))}"),
        ("openai_key", f"the key sk-{_rand(48)} goes in .env"),
        ("gitlab_pat", f"GITLAB_TOKEN=glpat-{_rand(20)} for the mirror push"),
        ("github_pat", f"use ghp_{_rand(36)} to open the PR"),
        ("aws_access_key", f"aws creds: AKIA{_rand(16, string.ascii_uppercase + string.digits)}"),
        ("slack_token", f"webhook bot token REDACTED-SECRET{_rand(24)}"),
        ("stripe_secret", f"STRIPE_KEY=sk_live_{_rand(28)} (prod!)"),
        ("telegram_bot_token", f"bot token 8766746046:{_rand(35)} for the bridge"),
        ("jwt", f"Authorization: Bearer eyJ{_rand(20)}.eyJ{_rand(30)}.{_rand(40)}"),
        ("private_key_block", "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXk\n"),
        ("generic_secret_assignment", f"db_password = {_rand(24)}"),
        ("private_path", "creds live at /home/workloft/secrets/x-account.txt"),
        ("private_ip", "ssh -i key workloft@10.0.0.1"),
    ]


def run_recall():
    fixtures = recall_fixtures()
    hits = 0
    misses = []
    for expected, text in fixtures:
        found = {f.detector for f in scan(text)}
        if expected in found:
            hits += 1
        else:
            misses.append((expected, found))
    return hits, len(fixtures), misses


def run_false_positives():
    files = []
    for g in CLEAN_GLOBS:
        files.extend(glob.glob(g))
    total_chars = 0
    sev_counts = {"high": 0, "medium": 0, "low": 0}
    flagged_files = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        total_chars += len(text)
        findings = scan(text, min_severity="medium")  # ignore low (private IPs)
        if findings:
            flagged_files.append((path, findings))
        for f in findings:
            sev_counts[f.severity] += 1
    return len(files), total_chars, sev_counts, flagged_files


def main():
    print("=== sluice benchmark ===\n")

    hits, total, misses = run_recall()
    print(f"RECALL on planted secrets: {hits}/{total} ({100*hits/total:.1f}%)")
    for exp, found in misses:
        print(f"  MISS: {exp} (got {found or 'nothing'})")

    n_files, chars, sev, flagged = run_false_positives()
    print(f"\nFALSE-POSITIVE scan over published/queued copy:")
    print(f"  files scanned : {n_files}")
    print(f"  chars scanned : {chars:,}")
    print(f"  HIGH findings : {sev['high']}")
    print(f"  MEDIUM findings: {sev['medium']}")
    if flagged:
        print("  flagged (inspect — may be legit content in security articles):")
        for path, fs in flagged:
            labels = ", ".join(f"{f.detector}@L{f.line}" for f in fs)
            print(f"    {os.path.relpath(path, HOME)}: {labels}")
    else:
        print("  no medium/high false positives across the corpus.")


if __name__ == "__main__":
    main()
