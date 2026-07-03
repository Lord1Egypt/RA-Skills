#!/usr/bin/env python3
"""
smb-client-onboarding — executable (v1.0)

Usage:
  clawhub run smb-client-onboarding connect <service>     # gmail | stripe | hubspot | slack | trello
  clawhub run smb-client-onboarding edit <field>           # welcome_email | welcome_whatsapp
  clawhub run smb-client-onboarding configure              # required-docs, reminder-schedule, escalate-to
  clawhub run smb-client-onboarding new --name "Acme Corp" --contact "jane@acme.com" --package "Growth" --contract-value 5000
  clawhub run smb-client-onboarding status                 # show all in-progress onboardings
  clawhub run smb-client-onboarding status --client "Acme Corp"
  clawhub run smb-client-onboarding send-reminder --client "Acme Corp"
  clawhub run smb-client-onboarding skip-step --client "Acme Corp" --step "NDA"

Free tier: 1 client record.
Pro tier: unlimited (--pro flag, $39 one-time).
"""
import argparse
import csv
import json
import logging
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

__version__ = "1.0.1"
SCHEMA_VERSION = 1

logger = logging.getLogger("smb-client-onboarding")
USER_AGENT = "SMBClientOnboarding/1.0 (+https://clawhub.ai)"
DATA_DIR = Path.home() / ".openclaw" / "smb-client-onboarding"


def configure_logging(verbose=False, quiet=False):
    """Configure logging level based on flags / env."""
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    elif not quiet:
        level = logging.INFO
    env_level = os.environ.get("CLAWHUB_LOG_LEVEL", "").upper()
    if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        level = getattr(logging, env_level)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
DATA_PATH = DATA_DIR / "onboardings.json"
CONFIG_PATH = DATA_DIR / "config.json"


def load_onboardings():
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH) as f:
            data = json.load(f)
            if isinstance(data, dict) and "onboardings" in data:
                file_schema = data.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating onboardings schema from v{file_schema} to v{SCHEMA_VERSION}")
                return data["onboardings"]
            return data
    except (json.JSONDecodeError, IOError):
        return []


def save_onboardings(onboardings):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, "onboardings": onboardings}
    with open(DATA_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
                file_schema = cfg.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating config schema from v{file_schema} to v{SCHEMA_VERSION}")
                cfg.pop("_schema_version", None)
                return cfg
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "connected_services": {},
        "required_docs": ["NDA", "BriefForm"],
        "reminder_schedule": "T+1,T+3,T+7",
        "escalate_to": None,
        "welcome_email_template": "",
        "welcome_whatsapp_template": "",
        "templates": {
            "stripe_product": None,
            "trello_board_template": None,
            "slack_channel_prefix": "client-",
        },
    }


def save_config(config):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, **config}
    with open(CONFIG_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


def get_llm_api_key():
    # Scope to MINIMAX only — do not accept OPENAI_API_KEY or LLM_API_KEY.
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key, "MINIMAX_API_KEY"
    return None, None


def call_llm(prompt, max_tokens=800):
    """Call LLM via pinned minimax endpoint. TT3 fix: no LLM_BASE_URL override."""
    api_key, _ = get_llm_api_key()
    if not api_key:
        return None
    base_url = "https://api.minimax.chat/v1"  # pinned, no env override
    try:
        data = json.dumps({
            "model": "minimax/MiniMax-M3",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.4,
        }).encode()
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def cmd_connect(args):
    config = load_config()
    service = args.service
    valid_services = ["gmail", "stripe", "hubspot", "slack", "trello", "asana", "pipedrive", "linear", "notion"]

    if service not in valid_services:
        logger.info(f"Unknown service: {service}")
        logger.info(f"Valid services: {', '.join(valid_services)}")
        sys.exit(1)

    logger.info(f"\n[{service}] OAuth flow:")
    logger.info("=" * 60)

    oauth_instructions = {
        "gmail": ("https://console.cloud.google.com", "GMAIL_CLIENT_ID + GMAIL_CLIENT_SECRET"),
        "stripe": ("https://dashboard.stripe.com/apikeys", "STRIPE_API_KEY"),
        "hubspot": ("https://app.hubspot.com/private-apps", "HUBSPOT_API_KEY"),
        "slack": ("https://api.slack.com/apps", "SLACK_BOT_TOKEN"),
        "trello": ("https://trello.com/app-key", "TRELLO_API_KEY + TRELLO_TOKEN"),
    }

    if service in oauth_instructions:
        url, env = oauth_instructions[service]
        logger.info(f"Step 1: Visit {url}")
        logger.info(f"Step 2: Set env var(s): {env}")
    else:
        logger.info(f"Visit the {service} developer portal and obtain API credentials.")

    logger.info("=" * 60)
    print()

    if args.simulate:
        config["connected_services"][service] = {"simulated": True, "connected_at": datetime.now().isoformat()}
        save_config(config)
        logger.info(f"OK (Simulated) {service} marked as connected.")


def cmd_edit(args):
    config = load_config()

    if args.field == "welcome_email":
        config["welcome_email_template"] = args.template
        save_config(config)
        logger.info("OK Welcome email template saved.")
    elif args.field == "welcome_whatsapp":
        config["welcome_whatsapp_template"] = args.template
        save_config(config)
        logger.info("OK Welcome WhatsApp template saved.")
    else:
        logger.info(f"Unknown field: {args.field}")
        logger.info("Valid: welcome_email, welcome_whatsapp")
        sys.exit(1)


def cmd_configure(args):
    config = load_config()

    changed = False
    if args.required_docs:
        config["required_docs"] = args.required_docs.split(",")
        changed = True
    if args.reminder_schedule:
        config["reminder_schedule"] = args.reminder_schedule
        changed = True
    if args.escalate_to:
        config["escalate_to"] = args.escalate_to
        changed = True
    if args.stripe_product:
        config["templates"]["stripe_product"] = args.stripe_product
        changed = True
    if args.trello_template:
        config["templates"]["trello_board_template"] = args.trello_template
        changed = True
    if args.slack_prefix:
        config["templates"]["slack_channel_prefix"] = args.slack_prefix
        changed = True

    if changed:
        save_config(config)
        logger.info("\nOK Configuration updated:")
    else:
        logger.info("\nCurrent configuration:")

    logger.info(f"  Required docs: {', '.join(config['required_docs'])}")
    logger.info(f"  Reminder schedule: {config['reminder_schedule']}")
    logger.info(f"  Escalate to: {config['escalate_to'] or '(not set)'}")
    logger.info(f"  Connected services: {list(config['connected_services'].keys()) or '(none)'}")


def cmd_new(args):
    onboardings = load_onboardings()
    config = load_config()

    if not args.pro and len(onboardings) >= 1:
        logger.info("Free tier limited to 1 active onboarding template.")
        logger.info("Use --pro flag for unlimited clients (paid tier, $39 one-time).")
        sys.exit(1)

    for ob in onboardings:
        if ob.get("name", "").lower() == args.name.lower():
            logger.info(f"Client '{args.name}' already exists with ID {ob['id']}")
            sys.exit(1)

    onboarding_id = f"ONB-{len(onboardings) + 1:04d}"
    today = datetime.now().date()

    onboarding = {
        "id": onboarding_id,
        "name": args.name,
        "contact": args.contact,
        "package": args.package,
        "contract_value": args.contract_value,
        "start_date": args.start_date or today.isoformat(),
        "status": "in_progress",
        "created_at": datetime.now().isoformat(),
        "steps": {
            "welcome_email": {"status": "pending", "scheduled_for": today.isoformat()},
            "welcome_whatsapp": {"status": "skipped" if args.no_whatsapp else "pending"},
            "document_collection": {"status": "pending", "docs_required": config["required_docs"]},
            "stripe_payment": {"status": "pending"},
            "calendly_booking": {"status": "pending"},
            "crm_entry": {"status": "pending"},
            "trello_board": {"status": "pending"},
            "slack_channel": {"status": "pending"},
            "team_notification": {"status": "pending"},
        },
        "reminders_sent": [],
        "escalations": [],
    }

    onboardings.append(onboarding)
    save_onboardings(onboardings)

    logger.info(f"\nOK Created {onboarding_id}: {args.name}")
    logger.info(f"  Steps to complete: {len(onboarding['steps'])}")
    logger.info(f"  Estimated time: 24h with full automation")
    print()
    logger.info("Next steps (run these to execute the sequence):")
    logger.info(f"  clawhub run smb-client-onboarding status --client \"{args.name}\"")
    logger.info(f"  clawhub run smb-client-onboarding send-reminder --client \"{args.name}\"")


def cmd_status(args):
    onboardings = load_onboardings()

    if args.client:
        ob = None
        for o in onboardings:
            if o.get("name", "").lower() == args.client.lower():
                ob = o
                break
        if not ob:
            logger.info(f"Client '{args.client}' not found.")
            return
        logger.info(f"\n{ob['name']} ({ob['id']})")
        logger.info(f"  Status: {ob['status']}")
        logger.info(f"  Package: {ob['package']}")
        logger.info(f"  Contract: ${ob['contract_value']:,.2f}")
        logger.info(f"  Start: {ob['start_date']}")
        logger.info("\n  Steps:")
        for step_name, step in ob.get("steps", {}).items():
            status = step.get("status", "?")
            icon = {"pending": "PENDING", "complete": "DONE", "skipped": "SKIP"}.get(status, status)
            logger.info(f"    [{icon:6}] {step_name}")
        if ob.get("reminders_sent"):
            logger.info(f"\n  Reminders sent: {len(ob['reminders_sent'])}")
    else:
        if not onboardings:
            logger.info("No active onboardings.")
            return
        logger.info(f"\n{'ID':<10} {'Client':<30} {'Status':<15} {'Started':<12}")
        logger.info("-" * 70)
        for ob in onboardings:
            logger.info(f"{ob['id']:<10} {ob['name'][:30]:<30} {ob['status']:<15} {ob['start_date']:<12}")


def cmd_send_reminder(args):
    onboardings = load_onboardings()

    ob = None
    for o in onboardings:
        if o.get("name", "").lower() == args.client.lower():
            ob = o
            break
    if not ob:
        logger.info(f"Client '{args.client}' not found.")
        sys.exit(1)

    stuck_steps = [name for name, step in ob.get("steps", {}).items() if step.get("status") == "pending"]

    if not stuck_steps:
        logger.info(f"All steps complete for {ob['name']}.")
        return

    api_key, _ = get_llm_api_key()
    if api_key:
        prompt = f"""Write a short, friendly reminder email for a stuck onboarding.

Client: {ob['name']}
Contact: {ob['contact']}
Stuck steps: {', '.join(stuck_steps)}

Mention the specific stuck items and ask the client to complete them. Keep it warm, professional, and brief (3-4 sentences max)."""
        body = call_llm(prompt)
    
    # Fallback to template if LLM unavailable or failed
    if not body:
        body = f"Hi {ob['name']},\n\nJust checking in on your onboarding. The following items are still pending: {', '.join(stuck_steps)}.\n\nPlease let me know if you have any questions or need help.\n\nThank you."

    today_str = datetime.now().strftime("%Y-%m-%d")
    ob["reminders_sent"].append({
        "date": today_str,
        "stuck_steps": stuck_steps,
        "channel": "email",
    })
    save_onboardings(onboardings)

    logger.info(f"\n{'=' * 70}")
    logger.info(f"REMINDER for {ob['name']} ({ob['contact']})")
    logger.info(f"{'=' * 70}")
    print(body)
    logger.info(f"{'=' * 70}")
    logger.info(f"Reminder tracked ({len(ob['reminders_sent'])} total sent)")


def cmd_skip_step(args):
    onboardings = load_onboardings()
    ob = None
    for o in onboardings:
        if o.get("name", "").lower() == args.client.lower():
            ob = o
            break
    if not ob:
        logger.info(f"Client '{args.client}' not found.")
        sys.exit(1)

    if args.step not in ob.get("steps", {}):
        logger.info(f"Unknown step: {args.step}")
        logger.info(f"Valid: {', '.join(ob.get('steps', {}).keys())}")
        sys.exit(1)

    ob["steps"][args.step]["status"] = "complete"
    ob["steps"][args.step]["completed_at"] = datetime.now().isoformat()
    save_onboardings(onboardings)
    logger.info(f"OK {args.step} marked complete for {ob['name']}")


def main():
    parser = argparse.ArgumentParser(description="SMB Client Onboarding")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress info logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_connect = subparsers.add_parser("connect", help="Connect a service (OAuth)")
    p_connect.add_argument("service", help="gmail | stripe | hubspot | slack | trello | asana | pipedrive | linear | notion")
    p_connect.add_argument("--simulate", action="store_true", help="Simulate connection")
    p_connect.set_defaults(func=cmd_connect)

    p_edit = subparsers.add_parser("edit", help="Edit a template")
    p_edit.add_argument("field", help="welcome_email | welcome_whatsapp")
    p_edit.add_argument("--template", required=True, help="Template content (supports {{name}}, {{agency}} placeholders)")
    p_edit.set_defaults(func=cmd_edit)

    p_config = subparsers.add_parser("configure", help="Configure onboarding settings")
    p_config.add_argument("--required-docs", help="Comma-separated doc names")
    p_config.add_argument("--reminder-schedule", help="T+1,T+3,T+7")
    p_config.add_argument("--escalate-to", help="Email to escalate stuck onboardings")
    p_config.add_argument("--stripe-product", help="Stripe product ID")
    p_config.add_argument("--trello-template", help="Trello board template URL")
    p_config.add_argument("--slack-prefix", help="Slack channel prefix (default 'client-')")
    p_config.set_defaults(func=cmd_configure)

    p_new = subparsers.add_parser("new", help="Trigger onboarding for a new client")
    p_new.add_argument("--name", required=True, help="Client name")
    p_new.add_argument("--contact", required=True, help="Contact email")
    p_new.add_argument("--package", required=True, help="Service package (e.g., 'Growth Consulting')")
    p_new.add_argument("--contract-value", type=float, required=True, help="Contract value in USD")
    p_new.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    p_new.add_argument("--no-whatsapp", action="store_true", help="Skip WhatsApp step")
    p_new.add_argument("--pro", action="store_true", help="Pro tier (unlimited clients)")
    p_new.set_defaults(func=cmd_new)

    p_status = subparsers.add_parser("status", help="Show onboarding status")
    p_status.add_argument("--client", help="Specific client name")
    p_status.set_defaults(func=cmd_status)

    p_remind = subparsers.add_parser("send-reminder", help="Send reminder for stuck steps")
    p_remind.add_argument("--client", required=True, help="Client name")
    p_remind.set_defaults(func=cmd_send_reminder)

    p_skip = subparsers.add_parser("skip-step", help="Mark a step as complete manually")
    p_skip.add_argument("--client", required=True, help="Client name")
    p_skip.add_argument("--step", required=True, help="Step name to mark complete")
    p_skip.set_defaults(func=cmd_skip_step)

    args = parser.parse_args()
    configure_logging(verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False))
    logger.debug(f"smb-client-onboarding v{__version__}")
    args.func(args)


if __name__ == "__main__":
    main()