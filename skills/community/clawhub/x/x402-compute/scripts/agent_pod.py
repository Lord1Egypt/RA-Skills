#!/usr/bin/env python3
"""
x402Compute — Agent Pods: deploy an always-on hosted OpenClaw agent and talk to it
through its OpenAI-compatible adapter.

A pod IS a compute order — the pod id returned by `deploy` is the compute order id and is
used for every pod + lifecycle call. See references/agent-pods.md for the full surface.

Auth (two surfaces):
  - Owner calls (catalog is public; deploy / list / get / create-key are owner-authed) use the
    SAME compute auth as the rest of this skill: COMPUTE_API_KEY (X-API-Key) or wallet-signing
    keys, loaded by wallet_signing.create_compute_auth_headers.
  - Adapter calls (chat / models) use the pod-scoped integration key `sk-sglpod-int-…` as
    `Authorization: Bearer …`. Provide it with --key or the POD_INTEGRATION_KEY env var.

Credentials are read ONLY from explicit environment variables. No .env auto-loading here.

Usage:
  python agent_pod.py catalog
  python agent_pod.py list
  python agent_pod.py get <pod_id>
  python agent_pod.py deploy --ai-mode managed --tier pro --plan <plan_id> \
      --prepaid-hours 720 --telegram <bot_token> --use-credits
  python agent_pod.py deploy --ai-mode byok --plan <plan_id> --prepaid-hours 720 \
      --llm-base-url https://openrouter.ai/api/v1 --llm-api-key <key> --model openai/gpt-4o-mini --use-credits
  python agent_pod.py templates
  python agent_pod.py deploy --ai-mode managed --tier pro --plan <plan_id> --use-credits \
      --telegram <bot_token> --template community-manager \
      --template-config group_id=-1001234567890 --template-config owner_id=987654321 \
      --template-config project_summary="What this community is about"
  python agent_pod.py deploy --ai-mode managed --tier starter --use-credits \
      --agent-identity "You are Atlas, Acme's support agent." \
      --agent-instructions "Answer as Acme support. Be concise." \
      --heartbeat-prompt "Check open support escalations. Stay silent if clear."
  python agent_pod.py create-key <pod_id> --name my-integration
  python agent_pod.py chat <pod_id> "What's on my calendar today?" --key sk-sglpod-int-...
"""

import argparse
import json
import os
import sys
from typing import Dict, Optional

import requests

from wallet_signing import create_compute_auth_headers

BASE_URL = "https://compute.x402layer.cc"


def _owner_headers(method: str, path: str, body_json: str = "") -> Dict[str, str]:
    """Compute auth headers (X-API-Key from COMPUTE_API_KEY, or wallet signature)."""
    headers = create_compute_auth_headers(method, path, body_json)
    if body_json:
        headers["Content-Type"] = "application/json"
    return headers


def catalog() -> dict:
    """Public: deployable agents, managed tiers/models, channels, pricing."""
    resp = requests.get(f"{BASE_URL}/pods/catalog", timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:500]}
    return resp.json()


def templates() -> dict:
    """Public: curated templates (what a pod is FOR) + the setup keys each one requires.

    Served from the same catalog the dashboard uses, so this list is never stale. Each
    entry carries `setup`, the exact --template-config keys deploy will demand, and
    `coming_soon`, which means announced but not yet buildable.
    """
    cat = catalog()
    if "error" in cat:
        return cat
    return {
        "templates_enabled": cat.get("templates_enabled", False),
        "templates": cat.get("templates", []),
        "group_allowance": {t.get("id"): t.get("max_groups") for t in cat.get("tiers", [])},
    }


def list_pods() -> dict:
    path = "/pods"
    resp = requests.get(f"{BASE_URL}/pods", headers=_owner_headers("GET", path), timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:500]}
    return resp.json()


def get_pod(pod_id: str) -> dict:
    path = f"/pods/{pod_id}"
    resp = requests.get(f"{BASE_URL}{path}", headers=_owner_headers("GET", path), timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:500]}
    return resp.json()


def deploy(
    ai_mode: str,
    plan: str,
    prepaid_hours: int,
    agent_id: str = "openclaw",
    tier: Optional[str] = None,
    model: Optional[str] = None,
    telegram: Optional[str] = None,
    discord: Optional[str] = None,
    llm_base_url: Optional[str] = None,
    llm_api_key: Optional[str] = None,
    llm_api: Optional[str] = None,
    use_credits: bool = False,
    network: Optional[str] = None,
    template: Optional[str] = None,
    template_config: Optional[Dict[str, str]] = None,
    agent_instructions: Optional[str] = None,
    agent_identity: Optional[str] = None,
    heartbeat_prompt: Optional[str] = None,
    agent_heartbeat_minutes: Optional[int] = None,
) -> dict:
    """Deploy a pod via POST /pods (owner / compute auth).

    Managed (we run the LLM, metered from credits): pick --tier starter|pro|max.
    BYOK (your own OpenAI-compatible key): pass --llm-base-url/--llm-api-key/--model.
    Pay from credits with --use-credits, else omit it to settle via x402 (402 flow — use the
    dashboard or the x402 provision path to complete payment).

    Curated templates (--template) say what the pod is FOR: they supply the persona, the
    channel policy and the briefing schedule on top of the engine. `catalog` lists them
    under "templates", each with the exact setup keys it needs. A template is validated
    BEFORE anything is charged, so a missing key fails as a 400, not as a pod that boots
    and quietly does nothing.

    Platform customization is layered on top of the managed base files:
    --agent-instructions and --agent-identity render into the pod's managed AGENTS.md /
    IDENTITY.md, while --heartbeat-prompt changes the self-check prompt. Raw AGENTS.md
    replacement is intentionally not exposed by the API.
    """
    body: dict = {
        "agent_id": agent_id,
        "ai_mode": ai_mode,
        "plan": plan,
        "prepaid_hours": prepaid_hours,
    }
    if ai_mode == "managed":
        if not tier:
            return {"error": "managed mode requires --tier (starter|pro|max)"}
        body["tier"] = tier
        if model:
            body["model"] = model
    else:  # byok
        if not (llm_base_url and llm_api_key):
            return {"error": "byok mode requires --llm-base-url and --llm-api-key"}
        body["llm_base_url"] = llm_base_url
        body["llm_api_key"] = llm_api_key
        body["llm_api"] = llm_api or "openai-completions"
        if model:
            body["model"] = model
    channels: dict = {}
    if telegram:
        channels["telegram"] = telegram
    if discord:
        channels["discord"] = discord
    if channels:
        body["channels"] = channels
    if template:
        body["template"] = template
        body["template_config"] = template_config or {}
    if agent_instructions:
        body["agent_instructions"] = agent_instructions
    if agent_identity:
        body["agent_identity"] = agent_identity
    if heartbeat_prompt:
        body["heartbeat_prompt"] = heartbeat_prompt
    if agent_heartbeat_minutes is not None:
        body["agent_heartbeat_minutes"] = agent_heartbeat_minutes
    if use_credits:
        body["use_credits"] = True
    if network:
        body["network"] = network

    body_json = json.dumps(body, separators=(",", ":"))
    path = "/pods"
    resp = requests.post(
        f"{BASE_URL}/pods", data=body_json, headers=_owner_headers("POST", path, body_json), timeout=120,
    )
    if resp.status_code == 402:
        return {
            "error": "402 Payment Required — pod requires x402 payment.",
            "hint": "Deploy with --use-credits, or complete the x402 payment flow via the dashboard.",
            "challenge": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text[:500],
        }
    if resp.status_code == 202:
        # PAID, delivery not yet confirmed: the pod exists and is booting. Do NOT deploy again
        # (that buys a second pod). Poll it with `get <pod_id>` instead.
        data = resp.json()
        data["pending"] = True
        data.setdefault("hint", "Payment accepted; delivery is being confirmed. Do NOT deploy again. Poll with: agent_pod.py get <pod_id>")
        return data
    if resp.status_code not in (200, 201):
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:2000]}
    return resp.json()


def create_key(pod_id: str, name: str = "API key") -> dict:
    """Create an sk-sglpod-int-* integration key for the OpenAI adapter (owner / compute auth)."""
    body_json = json.dumps({"name": name}, separators=(",", ":"))
    path = f"/pods/{pod_id}/api-keys"
    resp = requests.post(
        f"{BASE_URL}{path}", data=body_json, headers=_owner_headers("POST", path, body_json), timeout=30,
    )
    if resp.status_code == 404:
        return {"error": "OpenAI adapter is not enabled for this pod (feature-flagged)."}
    if resp.status_code not in (200, 201):
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:500]}
    return resp.json()


def chat(pod_id: str, message: str, key: Optional[str] = None) -> dict:
    """Call the pod's OpenAI-compatible adapter (Bearer sk-sglpod-int-*), non-streaming."""
    key = key or os.getenv("POD_INTEGRATION_KEY")
    if not key:
        return {"error": "Provide the integration key via --key or POD_INTEGRATION_KEY (sk-sglpod-int-...)."}
    body_json = json.dumps(
        {"model": "agent-pod", "stream": False, "messages": [{"role": "user", "content": message}]},
        separators=(",", ":"),
    )
    resp = requests.post(
        f"{BASE_URL}/pods/{pod_id}/v1/chat/completions",
        data=body_json,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        timeout=120,
    )
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "response": resp.text[:500]}
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Pods: deploy + OpenAI adapter")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("catalog", help="List deployable agents, tiers, channels, pricing (public)")
    sub.add_parser("templates", help="List curated pod templates and the setup each one needs (public)")
    sub.add_parser("list", help="List your pods")

    p_get = sub.add_parser("get", help="Get one pod (details + heartbeat + masked creds)")
    p_get.add_argument("pod_id")

    p_dep = sub.add_parser("deploy", help="Deploy a pod (POST /pods)")
    p_dep.add_argument("--agent-id", default="openclaw", help="Agent to deploy (default: openclaw)")
    p_dep.add_argument("--ai-mode", required=True, choices=["managed", "byok"])
    p_dep.add_argument("--tier", choices=["starter", "pro", "max"], help="Managed tier")
    p_dep.add_argument("--plan", required=True, help="Machine plan id (from GET /compute/plans)")
    p_dep.add_argument("--prepaid-hours", type=int, default=720, help="Prepaid runtime hours (min 24; default 720)")
    p_dep.add_argument("--model", help="Managed model override (must be in tier list) or byok model id")
    p_dep.add_argument("--telegram", help="Telegram bot token")
    p_dep.add_argument("--discord", help="Discord bot token")
    p_dep.add_argument("--llm-base-url", help="BYOK: OpenAI-compatible base URL")
    p_dep.add_argument("--llm-api-key", help="BYOK: your LLM API key")
    p_dep.add_argument("--llm-api", choices=["openai-completions", "openai-responses", "anthropic-messages", "google-generative"],
                       help="BYOK: LLM API shape (default openai-completions)")
    p_dep.add_argument("--use-credits", action="store_true", help="Pay from platform credits (else x402)")
    p_dep.add_argument("--network", help="x402 network for non-Base payment (e.g. solana, robinhood, megaeth)")
    p_dep.add_argument("--template", help="Curated template id, e.g. community-manager (TGPod). See `catalog` -> templates")
    p_dep.add_argument("--template-config", action="append", metavar="KEY=VALUE", default=[],
                       help="Template setup value, repeatable. e.g. --template-config group_id=-1001234567890 "
                            "--template-config owner_id=987654321. Required keys are in catalog -> templates[].setup.")
    p_dep.add_argument("--agent-instructions",
                       help="Owner/platform instructions layered into managed AGENTS.md (max 8000 chars)")
    p_dep.add_argument("--agent-identity",
                       help="Owner/platform identity text layered into AGENTS.md and IDENTITY.md (max 8000 chars)")
    p_dep.add_argument("--heartbeat-prompt",
                       help="Self-check heartbeat prompt for the agent's quiet background check (max 4000 chars)")
    p_dep.add_argument("--agent-heartbeat-minutes", type=int,
                       help="Self-check cadence in minutes; 0 disables, otherwise 15-1440")

    p_key = sub.add_parser("create-key", help="Create an sk-sglpod-int-* adapter integration key")
    p_key.add_argument("pod_id")
    p_key.add_argument("--name", default="API key", help="Key label")

    p_chat = sub.add_parser("chat", help="Call the pod OpenAI adapter (non-streaming)")
    p_chat.add_argument("pod_id")
    p_chat.add_argument("message")
    p_chat.add_argument("--key", help="Integration key (sk-sglpod-int-...); else POD_INTEGRATION_KEY env")

    args = parser.parse_args()

    if args.command == "catalog":
        result = catalog()
    elif args.command == "templates":
        result = templates()
    elif args.command == "list":
        result = list_pods()
    elif args.command == "get":
        result = get_pod(args.pod_id)
    elif args.command == "deploy":
        tpl_cfg: Dict[str, str] = {}
        for pair in (args.template_config or []):
            if "=" not in pair:
                print(json.dumps({"error": f"--template-config expects KEY=VALUE, got: {pair}"}, indent=2))
                sys.exit(1)
            k, v = pair.split("=", 1)
            tpl_cfg[k.strip()] = v
        if tpl_cfg and not args.template:
            print(json.dumps({"error": "--template-config given without --template"}, indent=2))
            sys.exit(1)
        result = deploy(
            ai_mode=args.ai_mode, plan=args.plan, prepaid_hours=args.prepaid_hours,
            agent_id=args.agent_id, tier=args.tier, model=args.model,
            telegram=args.telegram, discord=args.discord,
            llm_base_url=args.llm_base_url, llm_api_key=args.llm_api_key, llm_api=args.llm_api,
            use_credits=args.use_credits, network=args.network,
            template=args.template, template_config=tpl_cfg,
            agent_instructions=args.agent_instructions, agent_identity=args.agent_identity,
            heartbeat_prompt=args.heartbeat_prompt, agent_heartbeat_minutes=args.agent_heartbeat_minutes,
        )
        if "pod" in result:
            pod = result["pod"]
            if result.get("pending"):
                print("⏳ Paid; the pod is booting but delivery is not confirmed yet. Do NOT deploy again.")
                print(f"   {result.get('pending_note') or result.get('hint') or ''}")
            else:
                print("✅ Pod deployed!")
            print(f"   ID:        {pod.get('id')}   (use this for all pod + lifecycle calls)")
            print(f"   Agent:     {pod.get('display_name')} ({pod.get('agent_id')})")
            print(f"   AI mode:   {pod.get('ai_mode')}  tier={pod.get('tier')}  model={pod.get('model')}")
            print(f"   Channels:  {', '.join(pod.get('channels') or []) or 'none'}")
            if pod.get("template"):
                print(f"   Template:  {pod.get('template')}")
            if pod.get("managed_ai_key"):
                print(f"   Managed AI key (shown once): {pod['managed_ai_key']}")
            print("   Next: python agent_pod.py create-key <id>  →  chat via the OpenAI adapter.")
            sys.exit(0)
    elif args.command == "create-key":
        result = create_key(args.pod_id, name=args.name)
        if result.get("key"):
            print("✅ Integration key created (shown ONCE — store it securely):")
            print(f"   Key:      {result['key']}")
            print(f"   Base URL: {result.get('base_url')}")
            print("   Call it:  Authorization: Bearer <key>, model 'agent-pod', stream:false")
            sys.exit(0)
    elif args.command == "chat":
        result = chat(args.pod_id, args.message, key=args.key)
        if "choices" in result:
            try:
                print(result["choices"][0]["message"]["content"])
            except (KeyError, IndexError, TypeError):
                print(json.dumps(result, indent=2))
            sys.exit(0)
    else:
        parser.error("unknown command")

    if isinstance(result, dict) and "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    print(json.dumps(result, indent=2))
