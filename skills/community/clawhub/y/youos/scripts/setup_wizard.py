#!/usr/bin/env python3
"""YouOS Setup Wizard — interactive first-time configuration."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

# Add root to path for imports
sys.path.insert(0, str(ROOT_DIR))

# Resolve the config path through settings so setup writes (and re-reads)
# the active instance's config when YOUOS_DATA_DIR is set, rather than
# always editing the repo's youos_config.yaml — which left every instance
# silently sharing one config file and the wizard's writes invisible to
# `youos status`/`youos ui` running for that instance.
from app.core.settings import get_instance_root  # noqa: E402

CONFIG_PATH = get_instance_root() / "youos_config.yaml"


def _print_banner():
    print()
    print("+" + "=" * 41 + "+")
    print("|           Welcome to YouOS              |")
    print("|  Your personal AI email copilot         |")
    print("+" + "=" * 41 + "+")
    print()
    print("YouOS learns how YOU write email - from your own sent history.")
    print("It runs entirely on your Mac. Your data never leaves your machine.")
    print()
    print("This setup takes about 5 minutes to first draft (full ingestion continues in background).")
    print("Let's get started.")
    print()


def _check_dependencies() -> bool:
    """Check and display status for each dependency. Returns True if all critical deps present."""
    print("Checking dependencies...")
    print()
    all_ok = True

    # Python version
    py_ver = sys.version_info
    if py_ver >= (3, 11):
        print(f"  Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}  OK")
    else:
        print(f"  Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}  FAIL (need 3.11+)")
        all_ok = False

    # Google ingestion backend dependency (backend-aware: gog / gws / native)
    from app.core.doctor import _google_backend_status

    backend, backend_ok, backend_detail = _google_backend_status()
    label = f"Google backend ({backend})"
    if backend_ok:
        print(f"  {label:<22} OK")
    else:
        print(f"  {label:<22} MISSING")
        print(f"    {backend_detail}")
        if backend == "gog":
            print("    Install: pip install gog-cli  OR  see OpenClaw docs for gog setup")
        elif backend == "native":
            print("    Install: pip install 'youos[google]'")
        all_ok = False

    # mlx (optional but recommended)
    import importlib.util as _ilu

    if _ilu.find_spec("mlx") is not None:
        print("  mlx (Apple Silicon ML) OK")
    else:
        print("  mlx (Apple Silicon ML) MISSING (optional - needed for local model)")
        print("    Install: pip install mlx mlx-lm")

    # git
    if shutil.which("git"):
        print("  git                    OK")
    else:
        print("  git                    MISSING")
        all_ok = False

    # RAM check
    try:
        # Use sysctl on macOS
        result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            ram_bytes = int(result.stdout.strip())
            ram_gb = ram_bytes / (1024**3)
            if ram_gb >= 16:
                print(f"  RAM: {ram_gb:.0f} GB         OK")
            elif ram_gb >= 8:
                print(f"  RAM: {ram_gb:.0f} GB         WARN (16GB recommended)")
            else:
                print(f"  RAM: {ram_gb:.0f} GB         WARN (<8GB, may be slow)")
    except Exception:
        print("  RAM: unknown")

    # Disk check
    try:
        stat = os.statvfs(str(ROOT_DIR))
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        if free_gb >= 10:
            print(f"  Disk: {free_gb:.0f} GB free    OK")
        else:
            print(f"  Disk: {free_gb:.0f} GB free    WARN (<10GB, recommend more)")
    except Exception:
        print("  Disk: unknown")

    print()
    return all_ok


def _detect_gog_accounts() -> list[str]:
    """E23: Auto-detect connected gog accounts via `gog auth list --json`."""
    if not shutil.which("gog"):
        return []
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # gog auth list --json returns list of {email, ...} or {accounts: [...]}
            if isinstance(data, list):
                return [a.get("email") or a.get("account") for a in data if a.get("email") or a.get("account")]
            if isinstance(data, dict):
                accounts = data.get("accounts") or data.get("emails") or []
                if isinstance(accounts, list):
                    return [a if isinstance(a, str) else a.get("email", "") for a in accounts if a]
    except Exception:
        pass
    return []


def _get_user_identity() -> dict:
    """Prompt for user name, emails, and names."""
    print("--- User Identity ---")
    print()

    name = input("What's your name? (used to personalise the UI)\n> ").strip()
    if not name:
        name = "User"

    print()
    print("What email accounts should YouOS learn from?")

    # E23: auto-detect gog accounts
    detected_accounts = _detect_gog_accounts()
    emails = []
    if detected_accounts:
        print("Detected connected gog accounts:")
        for i, acct in enumerate(detected_accounts, 1):
            print(f"  {i}. {acct}")
        print()
        confirm = input("Use all detected accounts? [Y/n] ").strip().lower()
        if confirm != "n":
            emails = list(detected_accounts)
            print(f"Using: {', '.join(emails)}")
        else:
            print("Which accounts? Enter numbers separated by commas, or type emails manually:")
            sel = input("> ").strip()
            selected = []
            for part in sel.split(","):
                part = part.strip()
                if part.isdigit() and 1 <= int(part) <= len(detected_accounts):
                    selected.append(detected_accounts[int(part) - 1])
                elif "@" in part:
                    selected.append(part)
            emails = selected
    else:
        print("Enter your Gmail addresses one per line. Empty line when done.")
    while not emails:
        email = input("> ").strip()
        if not email:
            break
        if "@" in email:
            emails.append(email)
        else:
            print(f"  '{email}' doesn't look like an email, skipping")

    print()
    print("What names do you go by in email? (for signature detection)")
    names = [name]  # include primary name by default
    while True:
        n = input("> ").strip()
        if not n:
            break
        if n not in names:
            names.append(n)

    print()
    print("What domains are internal to your organisation? (e.g. company.com, subsidiary.com) [optional, press Enter to skip]")
    domains_input = input("> ").strip()
    internal_domains = [d.strip().lower() for d in domains_input.split(",") if d.strip()] if domains_input else []

    return {"name": name, "emails": emails, "names": names, "internal_domains": internal_domains}


def _detect_internal_domains(db_path: "Path", user_emails: list[str]) -> list[str]:
    """E24: Scan reply_author domains from corpus, suggest most common non-user domains."""
    import re as _re
    from collections import Counter

    user_domains = {e.split("@")[-1].lower() for e in user_emails if "@" in e}
    # Common free/consumer email domains to exclude
    skip_domains = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
        "me.com", "mac.com", "live.com", "msn.com", "aol.com",
    }

    try:
        import sqlite3 as _sqlite3
        conn = _sqlite3.connect(db_path)
        rows = conn.execute("SELECT reply_author FROM reply_pairs WHERE reply_author IS NOT NULL").fetchall()
        conn.close()
    except Exception:
        return []

    domain_counts: Counter = Counter()
    for (author,) in rows:
        m = _re.search(r"@([\w.-]+\.\w+)", author or "")
        if m:
            domain = m.group(1).lower()
            if domain not in user_domains and domain not in skip_domains:
                domain_counts[domain] += 1

    return [domain for domain, _count in domain_counts.most_common(5) if _count >= 3]


def _verify_accounts(emails: list[str]) -> list[str]:
    """Verify each email account has gog access. Returns list of verified accounts."""
    print()
    print("--- Account Verification ---")
    verified = []
    for email in emails:
        try:
            result = subprocess.run(
                ["gog", "gmail", "search", "in:sent", "--account", email, "--limit", "1", "--json"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                print(f"  {email}  OK")
                verified.append(email)
            else:
                print(f"  {email}  FAIL")
                print(f"    Run: gog auth --account {email}")
        except FileNotFoundError:
            print(f"  {email}  FAIL (gog not found)")
        except subprocess.TimeoutExpired:
            print(f"  {email}  TIMEOUT")

    if not verified:
        print()
        print("No accounts verified. You can still proceed and configure accounts later.")

    return verified


def _run_ingestion(config: dict) -> dict:
    """Run ingestion for configured accounts. Returns stats.

    Supports quick-start foreground ingest + background full ingest.
    """
    emails = config.get("user", {}).get("emails", [])
    if not emails:
        print("No email accounts configured. Skipping ingestion.")
        return {"threads": 0, "reply_pairs": 0}

    ingestion_cfg = config.get("ingestion", {})
    mode = ingestion_cfg.get("mode", "balanced")
    months = int(ingestion_cfg.get("initial_months", 12))
    max_threads = int(ingestion_cfg.get("max_threads", 0))
    quick_start = bool(ingestion_cfg.get("quick_start_enabled", False))
    quick_months = int(ingestion_cfg.get("quick_start_months", min(3, months)))
    quick_max_threads = int(ingestion_cfg.get("quick_start_max_threads", 200))

    def _query_for_months(m: int) -> str:
        return f"in:sent newer_than:{m}m"

    def _run_foreground(email: str, *, query: str, thread_cap: int, timeout_s: int = 1800) -> tuple[int, int]:
        print(f"\nIngesting {email} ({query}, max_threads={thread_cap})...")
        local_threads = 0
        local_pairs = 0
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT_DIR / "scripts" / "ingest_gmail_threads.py"),
                "--live",
                "--account",
                email,
                "--query",
                query,
                "--max-threads",
                str(thread_cap),
            ],
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        print(result.stdout)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "threads" in line.lower() and "reply" in line.lower():
                    import re

                    thread_match = re.search(r"(\d+)\s*threads?", line)
                    pair_match = re.search(r"(\d+)\s*reply.?pairs?", line)
                    if thread_match:
                        local_threads += int(thread_match.group(1))
                    if pair_match:
                        local_pairs += int(pair_match.group(1))
        else:
            print(f"  WARN: Ingestion for {email} had issues")
            if result.stderr:
                print(f"  {result.stderr[:300]}")
        return local_threads, local_pairs

    print()
    print("--- Corpus Ingestion ---")
    print(f"  Accounts: {', '.join(emails)}")
    print(f"  Ingestion mode: {mode}")
    print(f"  Full range: last {months} months | max_threads={max_threads}")
    if quick_start:
        print(f"  Quick start: last {quick_months} months | max_threads={quick_max_threads}")
    print()

    proceed = input("Start ingestion? [Y/n] ").strip().lower()
    if proceed == "n":
        print("Skipping ingestion. Run 'youos ingest' later.")
        return {"threads": 0, "reply_pairs": 0}

    total_threads = 0
    total_pairs = 0

    try:
        if quick_start:
            print("\nQuick start enabled: running a smaller ingest so you can use YouOS faster...")
            for email in emails:
                t, p = _run_foreground(email, query=_query_for_months(quick_months), thread_cap=quick_max_threads, timeout_s=1200)
                total_threads += t
                total_pairs += p

            print(f"\nQuick-start corpus: {total_threads} threads | {total_pairs} reply pairs")
            print("You can start drafting now while full ingestion continues in the background.")

            full_query = _query_for_months(months)
            # Per-instance: background-ingest logs land in the active
            # instance's var/, so multi-instance setups don't co-mingle logs.
            from app.core.settings import get_var_dir

            log_dir = get_var_dir()
            log_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

            for email in emails:
                safe_email = email.replace("@", "_at_").replace(".", "_")
                log_path = log_dir / f"ingest-background-{safe_email}-{stamp}.log"
                with open(log_path, "w", encoding="utf-8") as logf:
                    proc = subprocess.Popen(
                        [
                            sys.executable,
                            str(ROOT_DIR / "scripts" / "ingest_gmail_threads.py"),
                            "--live",
                            "--account",
                            email,
                            "--query",
                            full_query,
                            "--max-threads",
                            str(max_threads),
                        ],
                        stdout=logf,
                        stderr=subprocess.STDOUT,
                    )
                print(f"  Background ingest started for {email} (pid={proc.pid})")
                print(f"    Log: {log_path}")
        else:
            for email in emails:
                t, p = _run_foreground(email, query=_query_for_months(months), thread_cap=max_threads, timeout_s=1800)
                total_threads += t
                total_pairs += p
    except subprocess.TimeoutExpired:
        print("  TIMEOUT: Ingestion timed out")
    except Exception as exc:
        print(f"  ERROR: {exc}")

    print(f"\nCorpus built: {total_threads} threads | {total_pairs} reply pairs")
    return {"threads": total_threads, "reply_pairs": total_pairs}


def _run_persona_analysis(config: dict) -> dict | None:
    """Run persona analysis with interactive preference setting."""
    print()
    print("--- Persona Analysis ---")
    print("Analysing your writing style...")

    try:
        from app.core.settings import get_settings
        from app.db.bootstrap import resolve_sqlite_path
        from scripts.analyze_persona import analyze

        settings = get_settings()
        db_path = resolve_sqlite_path(settings.database_url)

        if not db_path.exists():
            print("  No database found. Skipping persona analysis.")
            return None

        findings = analyze(db_path)
        if findings.get("error"):
            print(f"  {findings['error']}")
            return None

        print()
        total = findings.get("total_pairs", 0)
        rl = findings.get("reply_length", {})
        greetings = findings.get("greeting_patterns", {})
        closers = findings.get("closing_patterns", {})

        top_greeting = ""
        greeting_pct = 0
        if greetings:
            top_greeting = max(greetings, key=greetings.get)
            greeting_pct = round(greetings[top_greeting] / total * 100) if total else 0

        top_closing = ""
        if closers:
            top_closing = max(closers, key=closers.get)

        # Determine work email ratio from sender classification
        work_pct = 0
        try:
            conn = sqlite3.connect(db_path)
            total_pairs = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
            personal_count = conn.execute(
                "SELECT COUNT(*) FROM reply_pairs WHERE inbound_author LIKE '%gmail.com%' "
                "OR inbound_author LIKE '%yahoo.com%' OR inbound_author LIKE '%hotmail.com%'"
            ).fetchone()[0]
            conn.close()
            if total_pairs > 0:
                work_pct = round((1 - personal_count / total_pairs) * 100)
        except Exception:
            pass

        print(f"Here's what we found from your {total} replies:")
        print()
        print(f"  Average reply length:    {rl.get('avg_words', 'N/A')} words")
        if top_greeting:
            print(f'  Most common greeting:    "{top_greeting}" ({greeting_pct}%)')
        if top_closing:
            print(f'  Most common closing:     "{top_closing}"')
        print(f"  Work email ratio:        {work_pct}%")
        print()

        # Interactive greeting preference
        print("Let's set your preferences:")
        print()
        print("Preferred greeting style:")
        print("  1. Hi [name],          (casual-professional)")
        print("  2. Dear [name],        (formal)")
        print("  3. Hey [name],         (casual)")
        print("  4. No greeting         (direct)")
        if top_greeting:
            print(f'  5. Keep what we found  ["{top_greeting}"]')
        choice = input("> ").strip()
        greeting_map = {
            "1": "Hi {name},",
            "2": "Dear {name},",
            "3": "Hey {name},",
            "4": "",
        }
        if choice == "5" and top_greeting:
            chosen_greeting = top_greeting
        elif choice in greeting_map:
            chosen_greeting = greeting_map[choice]
        else:
            chosen_greeting = greeting_map.get("1", "Hi {name},")

        print()
        user_name = config.get("user", {}).get("name", "User")
        default_formal = f"Best,\\n{user_name}"
        print("Preferred formal closing (e.g. partnership emails):")
        formal_input = input(f"> [{default_formal}] ").strip()
        chosen_formal = formal_input if formal_input else f"Best,\n{user_name}"

        print()
        default_informal = f"Cheers,\\n{user_name}"
        print("Preferred informal closing (e.g. supplier emails):")
        informal_input = input(f"> [{default_informal}] ").strip()
        chosen_informal = informal_input if informal_input else f"Cheers,\n{user_name}"

        print()
        print("Any phrases you never want to use? (comma-separated, or press Enter to skip)")
        print('e.g. "Hope this email finds you well, I wanted to reach out, Please don\'t hesitate"')
        banned_input = input("> ").strip()
        banned_phrases = [p.strip() for p in banned_input.split(",") if p.strip()] if banned_input else []

        # Save to configs/persona.yaml
        import yaml as _yaml

        persona_path = ROOT_DIR / "configs" / "persona.yaml"
        persona_config = _yaml.safe_load(persona_path.read_text(encoding="utf-8")) if persona_path.exists() else {}
        persona_config["name"] = user_name
        persona_config.setdefault("style", {})["avg_reply_words"] = rl.get("avg_words", 40)
        persona_config.setdefault("greeting_patterns", {})["default"] = chosen_greeting
        persona_config.setdefault("closing_patterns", {})["formal"] = chosen_formal.replace("\\n", "\n")
        persona_config["closing_patterns"]["informal"] = chosen_informal.replace("\\n", "\n")
        if banned_phrases:
            constraints = persona_config.get("style", {}).get("constraints", [])
            for phrase in banned_phrases:
                constraints.append(f'never use: "{phrase}"')
            persona_config["style"]["constraints"] = constraints

        persona_path.write_text(
            _yaml.dump(persona_config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
            encoding="utf-8",
        )
        print(f"\nPersona saved to {persona_path}")

        # Also update youos_config.yaml persona section
        config.setdefault("persona", {})
        config["persona"]["avg_reply_words"] = rl.get("avg_words", 40)
        config["persona"]["greeting_style"] = chosen_greeting
        config["persona"]["closing_formal"] = chosen_formal.replace("\\n", "\n")
        config["persona"]["closing_informal"] = chosen_informal.replace("\\n", "\n")
        config["persona"]["custom_constraints"] = banned_phrases

        import yaml as _yaml2

        CONFIG_PATH.write_text(
            _yaml2.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
            encoding="utf-8",
        )

        # Save analysis JSON
        output_path = ROOT_DIR / "configs" / "persona_analysis.json"
        output_path.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")

        return findings
    except Exception as exc:
        print(f"  Persona analysis failed: {exc}")
        return None


def _generate_benchmarks() -> bool:
    """Generate benchmark cases from corpus using generate_benchmarks module."""
    print()
    print("--- Benchmark Generation ---")
    print("Generating personalised benchmark cases from your corpus...")

    try:
        from app.core.settings import get_settings
        from app.db.bootstrap import resolve_sqlite_path
        from scripts.generate_benchmarks import (
            generate_cases,
            seed_to_db,
            update_refresh_count,
            write_fixtures,
        )

        settings = get_settings()
        db_path = resolve_sqlite_path(settings.database_url)

        if not db_path.exists():
            print("  No database found. Skipping benchmarks.")
            return False

        cases = generate_cases(db_path, count=15)
        if not cases:
            print("  Not enough reply pairs for benchmarks.")
            return False

        write_fixtures(cases)
        inserted = seed_to_db(cases, db_path)

        # Update refresh count
        conn = sqlite3.connect(db_path)
        try:
            pair_count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
        finally:
            conn.close()
        update_refresh_count(pair_count)

        print(f"  Generated {inserted} benchmark cases from your corpus")
        return True
    except Exception as exc:
        print(f"  Benchmark generation failed: {exc}")
        return False


def _offer_finetune(config: dict) -> None:
    """Offer initial fine-tuning if enough data."""
    print()
    try:
        from app.core.settings import get_settings
        from app.db.bootstrap import resolve_sqlite_path

        settings = get_settings()
        db_path = resolve_sqlite_path(settings.database_url)

        if not db_path.exists():
            return

        conn = sqlite3.connect(db_path)
        try:
            count = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
        finally:
            conn.close()

        if count < 50:
            print(f"Only {count} reply pairs — not enough for fine-tuning yet.")
            print("Review some emails in the web UI first, then run 'youos finetune'.")
            return

        print(f"You have {count} reply pairs — enough to do an initial fine-tune.")
        print("This trains a local Qwen model on your writing style (~3 minutes).")
        print()
        proceed = input("Run initial fine-tune? [Y/n] ").strip().lower()
        if proceed == "n":
            return

        result = subprocess.run(
            [sys.executable, str(ROOT_DIR / "scripts" / "finetune_lora.py")],
            timeout=3600,
        )
        if result.returncode == 0:
            print("  Fine-tuning complete!")
        else:
            print("  Fine-tuning had issues. Run 'youos finetune' later.")
    except Exception as exc:
        print(f"  Fine-tuning skipped: {exc}")


def _setup_pin(config: dict) -> dict:
    """Optionally set a PIN for web UI access."""
    print()
    print("--- Access PIN ---")
    print("Set an access PIN? (recommended if sharing Tailscale with others)")
    print("Leave blank to skip (your Tailscale network is the auth layer).")
    pin = input("PIN (4-digit numeric, leave blank for random default): ").strip()

    if not pin:
        import secrets
        pin = ''.join(secrets.choice('0123456789') for i in range(4))
        print(f"  No PIN entered, generated: {pin}")

    from app.core.auth import get_pin_hash
    config.setdefault("server", {})["pin"] = get_pin_hash(pin)
    print("  PIN set. You'll need this to access the web UI.")

    import yaml as _yaml

    CONFIG_PATH.write_text(
        _yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    return config


def _start_server(config: dict) -> None:
    """Start the YouOS server."""
    port = config.get("server", {}).get("port", 8765)
    host = config.get("server", {}).get("host", "127.0.0.1")

    print()
    print("--- Server ---")
    print(f"Starting YouOS server on {host}:{port}...")
    print()
    print(f"  Web UI:      http://localhost:{port}/feedback")
    print(f"  Stats:       http://localhost:{port}/stats")
    print(f"  Bookmarklet: http://localhost:{port}/bookmarklet")
    print()
    print("  Next step: open the Review Queue and review 10 emails.")
    print("  After 10 reviews, YouOS will fine-tune to your exact style.")
    print()
    print("  Run 'youos status' to check the system anytime.")
    print("  Run 'youos ui' to open the web UI.")


def _offer_nightly_pipeline(config: dict) -> None:
    """Offer to set up nightly pipeline."""
    print()
    print("Set up nightly self-improvement? (runs at 1 AM, takes ~90 min)")
    print("This ingests new emails, captures feedback, and auto-tunes the system.")
    print()
    proceed = input("Enable nightly pipeline? [Y/n] ").strip().lower()
    if proceed == "n":
        return

    schedule = config.get("autoresearch", {}).get("schedule", "0 1 * * *")
    print(f"  Nightly pipeline scheduled at: {schedule}")
    print("  To change: edit autoresearch.schedule in youos_config.yaml")

    # Try to set up cron
    try:
        if shutil.which("openclaw"):
            subprocess.run(
                [
                    "openclaw",
                    "cron",
                    "add",
                    "--name",
                    "youos:nightly",
                    "--schedule",
                    schedule,
                    "--command",
                    f"{sys.executable} {ROOT_DIR / 'scripts' / 'nightly_pipeline.py'}",
                ],
                timeout=10,
            )
            print("  Registered with OpenClaw scheduler.")
        else:
            print("  OpenClaw not found. Add to your system crontab manually:")
            print(f"  {schedule} cd {ROOT_DIR} && {sys.executable} scripts/nightly_pipeline.py")
    except Exception:
        print(f"  Add to crontab: {schedule} cd {ROOT_DIR} && {sys.executable} scripts/nightly_pipeline.py")


def _run_coldstart_check() -> int:
    """Non-interactive setup reliability check for cold-start environments."""
    print("Running setup cold-start check...")

    from app.core.doctor import run_doctor_checks

    passed, failures = run_doctor_checks()
    if not passed:
        print("System check failed:")
        for msg in failures:
            print(f"  ✗ {msg}")
        return 1

    deps_ok = _check_dependencies()
    if not deps_ok:
        print("Dependency check failed.")
        return 1

    # Ensure config path is writable.
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not CONFIG_PATH.exists():
            CONFIG_PATH.touch()
    except OSError as exc:
        print(f"Config path not writable: {exc}")
        return 1

    detected_accounts = _detect_gog_accounts()
    if detected_accounts:
        print(f"Detected gog accounts: {', '.join(detected_accounts)}")
    else:
        print("No gog accounts auto-detected (this can be okay if not authenticated yet).")

    print("Cold-start check passed.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--check-only", action="store_true", help="Run non-interactive cold-start reliability checks and exit")
    args, _unknown = parser.parse_known_args()

    if args.check_only:
        raise SystemExit(_run_coldstart_check())

    _print_banner()

    # Pre-flight: run doctor checks
    from app.core.doctor import run_doctor_checks

    passed, failures = run_doctor_checks()
    if not passed:
        print("System check failed:")
        for msg in failures:
            print(f"  \u2717 {msg}")
        print("\nFix the above issues first.")
        sys.exit(1)

    input("Press Enter to continue...")
    print()

    # Step 1: Dependency check
    deps_ok = _check_dependencies()
    if not deps_ok:
        print("Some critical dependencies are missing. Please install them and re-run setup.")
        proceed = input("Continue anyway? [y/N] ").strip().lower()
        if proceed != "y":
            sys.exit(1)

    # Step 2: User identity
    identity = _get_user_identity()

    # Step 3: Verify accounts
    _verify_accounts(identity["emails"])

    # Step 4: Build config
    import yaml

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
    config.setdefault("user", {})
    config["user"]["name"] = identity["name"]
    config["user"]["display_name"] = f"{identity['name']}OS" if identity["name"] != "User" else "YouOS"
    config["user"]["emails"] = identity["emails"]
    config["user"]["names"] = identity["names"]
    if identity.get("internal_domains"):
        config["user"]["internal_domains"] = identity["internal_domains"]
    config.setdefault("ingestion", {})
    config["ingestion"]["accounts"] = identity["emails"]
    # Quickstart-first onboarding defaults
    config["ingestion"].setdefault("mode", "quick_start")
    config["ingestion"].setdefault("initial_months", 12)
    config["ingestion"].setdefault("max_threads", 0)
    config["ingestion"].setdefault("quick_start_enabled", True)
    config["ingestion"].setdefault("quick_start_months", 3)
    config["ingestion"].setdefault("quick_start_max_threads", 200)
    config.setdefault("review", {})["batch_size"] = 10
    config["review"].setdefault("draft_model", "claude")  # 'claude', 'local', or 'auto'

    # Save config
    CONFIG_PATH.write_text(
        yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(f"\nConfiguration saved to {CONFIG_PATH}")

    # Step 5: Bootstrap database
    print()
    print("Initializing database...")
    try:
        subprocess.run(
            [sys.executable, str(ROOT_DIR / "scripts" / "bootstrap_db.py")],
            timeout=30,
        )
    except Exception as exc:
        print(f"  Database init failed: {exc}")

    # Step 6: Ingestion
    _run_ingestion(config)

    # E24: auto-detect internal domains from corpus
    if not identity.get("internal_domains"):
        try:
            from app.core.settings import get_settings as _gs
            from app.db.bootstrap import resolve_sqlite_path as _rsp
            _db_path = _rsp(_gs().database_url)
            if _db_path.exists():
                suggested_domains = _detect_internal_domains(_db_path, identity["emails"])
                if suggested_domains:
                    print()
                    print("Based on your corpus, these domains appear frequently in sent replies:")
                    for d in suggested_domains:
                        print(f"  - {d}")
                    print()
                    confirm = input("Mark these as internal domains? [Y/n] ").strip().lower()
                    if confirm != "n":
                        config.setdefault("user", {})["internal_domains"] = suggested_domains
                        import yaml as _yaml_e24
                        CONFIG_PATH.write_text(
                            _yaml_e24.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
                            encoding="utf-8",
                        )
                        print(f"  Saved internal domains: {', '.join(suggested_domains)}")
        except Exception:
            pass

    # Step 7: Persona analysis
    _run_persona_analysis(config)

    # Step 8: Benchmarks
    _generate_benchmarks()

    # Step 9: Fine-tune offer
    _offer_finetune(config)

    # Step 10: PIN auth
    config = _setup_pin(config)

    # Step 11: Server info
    _start_server(config)

    # Step 12: Nightly pipeline
    _offer_nightly_pipeline(config)

    print()
    print("Setup complete!")
    print()


if __name__ == "__main__":
    main()
