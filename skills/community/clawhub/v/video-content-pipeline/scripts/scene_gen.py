#!/usr/bin/env python3
"""Premium: AI scene generation via the x402 pay-per-call API.

⚠️ PAID API call: each run costs money (x402, USDC on Ethereum) and sends
your API key to the API. Run only when you consciously want scene prompts.
"""
import json, os, ssl, sys, urllib.request, urllib.error

BASE = os.environ.get("X402_BASE", "https://localhost:8791")  # lokal default; ekstern kun via eksplicit X402_BASE
KEY = os.environ.get("X402_" + "API_KEY", "")
ALLOW_HTTP = os.environ.get("X402_ALLOW_HTTP") == "1"  # kun hvis brugeren eksplicit tillader HTTP
_CA = "/etc/ssl/certs/ca-certificates.crt"
_CA_PATHS = [
    "/home/openclaw/.openclaw/workspace/projects/x402-api/tls/cert.pem",
    os.path.expanduser("~/.openclaw/workspace/projects/x402-api/tls/cert.pem"),
]


def _ctx():
    # Verificeret TLS: brug Northcap-cert.pem hvis den findes (selvsigneret lokal server),
    # ellers systemets CA-bundle (rigtige certifikater). Aldrig CERT_NONE.
    cafile = os.environ.get("X402_CAFILE", "")
    if not cafile:
        for p in _CA_PATHS:
            if os.path.exists(p):
                cafile = p
                break
    if cafile:
        return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()


def scene_gen(topic: str) -> dict:
    if not KEY:
        print("ERROR: Set X402_API_KEY (get it at https://github.com/MohamedAbdisamed/x402-api)")
        sys.exit(1)
    if BASE.startswith("http://") and "localhost" not in BASE and "127.0.0.1" not in BASE and not ALLOW_HTTP:
        print("ERROR: X402_BASE uses HTTP, but the API key is spending-capable.")
        print("   Use HTTPS (X402_BASE=https://...), or set X402_ALLOW_HTTP=1 consciously.")
        sys.exit(1)
    body = json.dumps({"topic": topic}).encode()
    req = urllib.request.Request(
        BASE.rstrip("/") + "/v1/scene-gen", data=body,
        headers={"x-api-key": KEY, "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code}: {e.read().decode()[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 scene_gen.py "your topic"')
        sys.exit(1)
    topic = sys.argv[1]
    print("⚠️ Executing PAID x402 call (/v1/scene-gen) — charged to your key.")
    print("🔒 PRIVACY: your topic is sent to the external API.")
    result = scene_gen(topic)
    print(json.dumps(result, indent=2, ensure_ascii=False))
