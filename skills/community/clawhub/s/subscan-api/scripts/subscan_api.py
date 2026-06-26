#!/usr/bin/env python3
"""
Subscan API Skill - Unified utility script

Usage:
  python3 subscan_api.py check-key          # Check if API Key is saved locally
  python3 subscan_api.py save-key <KEY>     # Save API Key to ~/.config/subscan-api-skill/key
  python3 subscan_api.py list-endpoints     # Parse swagger and output endpoint list
  python3 subscan_api.py call --url <URL> --body <JSON> [--key-file]  # Call API
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# API Key stored at user level — works regardless of where the skill is installed
KEY_FILE = Path.home() / ".config" / "subscan-api-skill" / "key"

SWAGGER_JSON = SCRIPT_DIR.parent / "swagger" / "swagger.json"
SWAGGER_YAML = SCRIPT_DIR.parent / "swagger" / "swagger.yaml"


# ─────────────────────────────────────────────────────────────────────────────
# API Key management
# ─────────────────────────────────────────────────────────────────────────────

def check_key() -> str | None:
    """Read API Key from user-level config file, return value or None."""
    if not KEY_FILE.exists():
        return None
    value = KEY_FILE.read_text(encoding="utf-8").strip()
    return value if value else None


def save_key(api_key: str) -> None:
    """Write API Key to user-level config file (~/.config/subscan-api-skill/key)."""
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("API Key cannot be empty")
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(api_key + "\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Swagger parsing
# ─────────────────────────────────────────────────────────────────────────────

def _load_swagger() -> dict:
    """Load swagger.json first, fall back to swagger.yaml."""
    if SWAGGER_JSON.exists():
        with open(SWAGGER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    if SWAGGER_YAML.exists():
        try:
            import yaml  # type: ignore
            with open(SWAGGER_YAML, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except ImportError:
            raise RuntimeError("PyYAML is required: pip install pyyaml")
    raise FileNotFoundError(f"Swagger doc not found: {SWAGGER_JSON} or {SWAGGER_YAML}")


def _resolve_ref(ref: str, definitions: dict) -> dict:
    """Resolve $ref, e.g. '#/definitions/Foo' -> definitions['Foo']."""
    if not ref.startswith("#/definitions/"):
        return {}
    key = ref[len("#/definitions/"):]
    return definitions.get(key, {})


def _extract_params(schema: dict, definitions: dict) -> tuple[list[str], list[str]]:
    """
    Extract required / optional parameter names from schema.
    Supports direct properties and $ref references.
    """
    if not schema:
        return [], []

    if "$ref" in schema:
        schema = _resolve_ref(schema["$ref"], definitions)

    properties: dict = schema.get("properties", {})
    required_fields: list = schema.get("required", [])

    required = [k for k in properties if k in required_fields]
    optional = [k for k in properties if k not in required_fields]
    return required, optional


def _get_param_descriptions(schema: dict, definitions: dict) -> dict[str, str]:
    """Return description and example for each parameter: {param_name: 'type - description (example)'}"""
    if not schema:
        return {}
    if "$ref" in schema:
        schema = _resolve_ref(schema["$ref"], definitions)

    result = {}
    for name, info in schema.get("properties", {}).items():
        parts = []
        if "type" in info:
            parts.append(info["type"])
        if "description" in info:
            parts.append(info["description"])
        if "example" in info:
            parts.append(f"example: {info['example']}")
        result[name] = " | ".join(parts) if parts else ""
    return result


def list_endpoints() -> list[dict]:
    """Parse swagger doc and return endpoint summary list."""
    doc = _load_swagger()
    definitions = doc.get("definitions", {})
    endpoints = []

    for path, path_item in doc.get("paths", {}).items():
        for method, operation in path_item.items():
            if method.lower() not in ("get", "post", "put", "delete", "patch"):
                continue

            body_schema = {}
            for param in operation.get("parameters", []):
                if param.get("in") == "body" and "schema" in param:
                    body_schema = param["schema"]
                    break

            required_params, optional_params = _extract_params(body_schema, definitions)
            param_descriptions = _get_param_descriptions(body_schema, definitions)

            endpoints.append({
                "path": path,
                "method": method.upper(),
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "tags": operation.get("tags", []),
                "synonyms": operation.get("x-synonyms", []),
                "required_params": required_params,
                "optional_params": optional_params,
                "param_descriptions": param_descriptions,
            })

    return endpoints


# ─────────────────────────────────────────────────────────────────────────────
# API call
# ─────────────────────────────────────────────────────────────────────────────

def call_api(url: str, body: dict, api_key: str) -> dict:
    """Call Subscan API and return parsed JSON response."""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "X-Refer": "subscan-api-skill",
    }
    body_bytes = json.dumps(body).encode("utf-8")

    # Prefer requests, fall back to urllib
    try:
        import requests  # type: ignore
        resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except ImportError:
        pass

    # urllib fallback
    import urllib.request
    import urllib.error

    req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            return json.loads(error_body)
        except Exception:
            raise RuntimeError(f"HTTP {e.code}: {error_body[:500]}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def cmd_check_key(_args):
    key = check_key()
    if key:
        # Only output first 8 chars for confirmation, do not expose full key
        print(f"KEY:{key[:8]}{'*' * (len(key) - 8)}")
    else:
        print("NO_KEY")


def cmd_save_key(args):
    if not args.key:
        print("ERROR: Please provide an API Key", file=sys.stderr)
        sys.exit(1)
    save_key(args.key)
    print(f"OK: API Key saved to {KEY_FILE}")


def cmd_list_endpoints(_args):
    try:
        endpoints = list_endpoints()
        print(json.dumps(endpoints, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_call(args):
    # Read API Key
    if args.key_file:
        api_key = check_key()
        if not api_key:
            print("ERROR: API Key not found, please run save-key first", file=sys.stderr)
            sys.exit(1)
    elif args.key:
        api_key = args.key
    else:
        print("ERROR: Please provide API Key via --key or --key-file", file=sys.stderr)
        sys.exit(1)

    # Parse request body
    try:
        body = json.loads(args.body) if args.body else {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in request body: {e}", file=sys.stderr)
        sys.exit(1)

    # Call API
    try:
        result = call_api(args.url, body, api_key)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Subscan API Skill utility")
    subparsers = parser.add_subparsers(dest="command")

    # check-key
    subparsers.add_parser("check-key", help="Check local API Key")

    # save-key
    p_save = subparsers.add_parser("save-key", help="Save API Key")
    p_save.add_argument("key", help="API Key value")

    # list-endpoints
    subparsers.add_parser("list-endpoints", help="List all endpoints")

    # call
    p_call = subparsers.add_parser("call", help="Call Subscan API")
    p_call.add_argument("--url", required=True, help="Full API URL")
    p_call.add_argument("--body", default="{}", help="Request body in JSON format")
    p_call.add_argument("--key-file", action="store_true", help="Read API Key from ~/.config/subscan-api-skill/key")
    p_call.add_argument("--key", default=None, help="Provide API Key directly (not recommended)")

    args = parser.parse_args()

    dispatch = {
        "check-key": cmd_check_key,
        "save-key": cmd_save_key,
        "list-endpoints": cmd_list_endpoints,
        "call": cmd_call,
    }

    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
