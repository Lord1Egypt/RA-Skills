#!/usr/bin/env python3
"""Qualia CLI - VLA fine-tuning platform.

Pure Python, no external dependencies. Requires Python 3.6+.
Set QUALIA_API_KEY environment variable before use.

Global flag: --json (machine-readable output, exactly one JSON
object/array on stdout; errors become {"error": {...}} on stdout).
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.qualiastudios.dev"

JSON_MODE = False

# Exit code contract (stable, documented in SKILL.md):
EXIT_OK = 0
EXIT_GENERIC = 1        # unknown/unclassified failure
EXIT_USAGE = 2          # bad arguments / unknown command
EXIT_AUTH = 3           # missing key, HTTP 401/403
EXIT_CREDITS = 4        # insufficient credits (HTTP 402)
EXIT_VALIDATION = 5     # HTTP 400/422 (bad camera mapping, hyperparams, dataset)
EXIT_NOT_FOUND = 6      # HTTP 404
EXIT_CONNECTION = 7     # network/connection failure


def http_status_to_exit_code(status):
    """Map an HTTP status code to the CLI exit code contract."""
    if status in (401, 403):
        return EXIT_AUTH
    if status == 402:
        return EXIT_CREDITS
    if status in (400, 422):
        return EXIT_VALIDATION
    if status == 404:
        return EXIT_NOT_FOUND
    return EXIT_GENERIC


class CliError(Exception):
    """Carries an exit code, a message, and optional structured details."""

    def __init__(self, exit_code, message, details=None):
        super().__init__(message)
        self.exit_code = exit_code
        self.message = message
        self.details = details


def emit(obj):
    """Print a single JSON object/array (JSON mode output)."""
    print(json.dumps(obj, indent=2))


def fail(err):
    """Report a CliError and exit with its code."""
    if JSON_MODE:
        emit({"error": {
            "code": err.exit_code,
            "message": err.message,
            "details": err.details,
        }})
    else:
        print(f"Error: {err.message}", file=sys.stderr)
        if err.details is not None:
            print(json.dumps(err.details, indent=2), file=sys.stderr)
    sys.exit(err.exit_code)


def usage_error(text):
    raise CliError(EXIT_USAGE, text)


def get_api_key():
    key = os.environ.get("QUALIA_API_KEY", "")
    if not key:
        raise CliError(EXIT_AUTH, "QUALIA_API_KEY not set")
    return key


def api_request(method, path, body=None):
    """Make an authenticated API request. Returns parsed JSON.

    Raises CliError on HTTP or connection failure.
    """
    url = f"{API_BASE}{path}"
    headers = {"X-API-Key": get_api_key()}
    data = None

    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            details = json.loads(e.read().decode("utf-8"))
        except Exception:
            details = {"reason": str(e.reason)}
        raise CliError(http_status_to_exit_code(e.code),
                       f"API error ({e.code})", details)
    except urllib.error.URLError as e:
        raise CliError(EXIT_CONNECTION, f"Connection error: {e.reason}")


# -- Commands ----------------------------------------------------------


def cmd_credits(_args):
    result = api_request("GET", "/v1/credits")
    if JSON_MODE:
        emit(result)
        return
    print(f"Credits: {result.get('balance', 'unknown')}")


def cmd_models(_args):
    result = api_request("GET", "/v1/models")
    if JSON_MODE:
        emit(result.get("data", []))
        return
    for m in result.get("data", []):
        slots = ", ".join(m.get("camera_slots", []))
        print(f"[{m['id']}] {m['name']}")
        print(f"  {m.get('description', '')}")
        print(f"  camera slots: {slots}")
        if m.get("base_model_id"):
            print(f"  base model: {m['base_model_id']}")
        if m.get("supports_custom_model") is False:
            print("  ⚠ custom model_id not supported")
        print()


def cmd_instances(_args):
    result = api_request("GET", "/v1/instances")
    if JSON_MODE:
        emit(result.get("data", []))
        return
    for i in result.get("data", []):
        specs = i.get("specs", {})
        regions = ", ".join(r["name"] for r in i.get("regions", []))
        print(f"[{i['id']}] {i['gpu_description']} - {i['credits_per_hour']} credits/hr")
        print(f"  {specs.get('gpu_count', '?')}x {specs.get('gpu_type', '?')} | "
              f"{specs.get('memory_gib', '?')}GB RAM | "
              f"{specs.get('storage_gib', '?')}GB storage | "
              f"{specs.get('vcpus', '?')} vCPUs")
        print(f"  regions: {regions}")
        print()


def cmd_projects(_args):
    result = api_request("GET", "/v1/projects")
    if JSON_MODE:
        emit(result.get("data", []))
        return
    for p in result.get("data", []):
        desc = f" - {p['description']}" if p.get("description") else ""
        created = p.get("created_at", "")[:10]
        jobs = p.get("jobs", [])
        print(f"[{p['project_id']}] {p['name']}{desc}")
        print(f"  created: {created} | jobs: {len(jobs)}")
        for j in jobs:
            status = j.get("status", "unknown")
            name = j.get("name") or j.get("model") or ""
            dataset = f" on {j['dataset']}" if j.get("dataset") else ""
            print(f"  · {j['job_id']} [{status}] {name}{dataset}")
        print()


def cmd_project_create(args):
    if not args:
        usage_error("Usage: qualia.py project-create <name> [description]")
    body = {"name": args[0]}
    if len(args) > 1 and args[1]:
        body["description"] = args[1]
    result = api_request("POST", "/v1/projects", body)
    if JSON_MODE:
        emit(result)
        return
    if result.get("created"):
        print(f"Created project: {result['project_id']}")
    else:
        print("Failed to create project")


def cmd_project_delete(args):
    if not args:
        usage_error("Usage: qualia.py project-delete <project_id>")
    result = api_request("DELETE", f"/v1/projects/{args[0]}")
    if JSON_MODE:
        emit(result)
        return
    if result.get("deleted"):
        print(f"Deleted project: {result['project_id']}")
    else:
        print("Failed to delete project")


def cmd_dataset_keys(args):
    if not args:
        usage_error("Usage: qualia.py dataset-keys <huggingface_dataset_id>\n"
                    "  e.g. qualia.py dataset-keys lerobot/aloha_sim_insertion_human")
    dataset_id = args[0]
    result = api_request("GET", f"/v1/datasets/{dataset_id}/image-keys")
    if JSON_MODE:
        emit(result)
        return
    print(f"Image keys for {dataset_id}:")
    for key in result.get("image_keys", []):
        print(f"  {key}")


def cmd_hyperparams(args):
    if not args:
        usage_error("Usage: qualia.py hyperparams <act|smolvla|pi0|pi05|gr00t_n1_5> [model_id]\n"
                    "  model_id required for: smolvla, pi0, pi05")
    vla_type = args[0]
    model_id = args[1] if len(args) > 1 else None
    path = f"/v1/finetune/hyperparams/defaults?vla_type={urllib.parse.quote(vla_type)}"
    if model_id:
        path += f"&model_id={urllib.parse.quote(model_id)}"
    result = api_request("GET", path)
    if JSON_MODE:
        emit(result.get("data", result))
        return
    label = f"{vla_type} ({model_id})" if model_id else vla_type
    print(f"Defaults for {label}:")
    print(json.dumps(result.get("data", result), indent=2))


def cmd_hyperparams_validate(args):
    if len(args) < 2:
        usage_error("Usage: qualia.py hyperparams-validate <vla_type> '<hyperparams_json>'")
    vla_type = args[0]
    try:
        hyper_json = json.loads(args[1])
    except json.JSONDecodeError as e:
        usage_error(f"Invalid JSON: {e}")
    path = f"/v1/finetune/hyperparams/validate?vla_type={urllib.parse.quote(vla_type)}"
    result = api_request("POST", path, hyper_json)
    if JSON_MODE:
        emit(result)
        return
    if result.get("valid"):
        print("✓ Valid")
    elif "valid" in result and not result["valid"]:
        print("✗ Invalid")
        for issue in result.get("issues", []):
            print(f"  · {issue.get('field', '?')}: {issue.get('message', '')}")
    else:
        print(json.dumps(result, indent=2))


def _parse_flags(argv):
    """Parse --key value and --key=value flags from argv. Returns dict."""
    flags = {}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--"):
            if "=" in arg:
                key, val = arg.split("=", 1)
                flags[key[2:]] = val
            elif i + 1 < len(argv):
                flags[arg[2:]] = argv[i + 1]
                i += 1
            else:
                usage_error(f"Flag {arg} requires a value")
        else:
            usage_error(f"Unknown argument: {arg}")
        i += 1
    return flags


FINETUNE_USAGE = """Usage: qualia.py finetune <project_id> <vla_type> <dataset_id> <hours> '<camera_mappings_json>' [flags]

  Required:
    project_id       UUID from 'qualia.py projects'
    vla_type         act | smolvla | pi0 | pi05 | gr00t_n1_5
    dataset_id       HuggingFace dataset ID (e.g. lerobot/pusht)
    hours            Training duration (max 168)
    camera_mappings  JSON: slot name -> dataset image key
                     e.g. '{"cam_1": "observation.images.top"}'

  Optional flags:
    --model <id>         Base model (required for smolvla/pi0/pi05)
    --name <str>         Job display name
    --instance <id>      GPU instance (from 'qualia.py instances')
    --region <name>      Cloud region
    --batch-size <n>     Training batch size (1-512, default 32)
    --hyper-spec '<json>' Advanced hyperparameters (from 'qualia.py hyperparams')
    --rabc <model_path>  Enable RA-BC with SARM reward model (HF path)
    --rabc-image-key <k> Image key for reward annotations
    --rabc-head-mode <m> RA-BC head mode (e.g. sparse)

  Tip: run 'qualia.py dataset-keys <dataset_id>' to discover image key names"""


def cmd_finetune(args):
    if len(args) < 5:
        usage_error(FINETUNE_USAGE)

    project_id, vla_type, dataset_id = args[0], args[1], args[2]

    try:
        hours = int(args[3]) if "." not in args[3] else float(args[3])
    except ValueError:
        usage_error(f"Invalid hours value: {args[3]}")

    try:
        camera_mappings = json.loads(args[4])
    except json.JSONDecodeError as e:
        usage_error(f"Invalid camera_mappings JSON: {e}")

    flags = _parse_flags(args[5:])

    body = {
        "project_id": project_id,
        "vla_type": vla_type,
        "dataset_id": dataset_id,
        "hours": hours,
        "camera_mappings": camera_mappings,
    }

    if "model" in flags:
        body["model_id"] = flags["model"]
    if "name" in flags:
        body["name"] = flags["name"]
    if "instance" in flags:
        body["instance_type"] = flags["instance"]
    if "region" in flags:
        body["region"] = flags["region"]
    if "batch-size" in flags:
        try:
            body["batch_size"] = int(flags["batch-size"])
        except ValueError:
            usage_error(f"Invalid batch-size: {flags['batch-size']}")
    if "hyper-spec" in flags:
        try:
            body["vla_hyper_spec"] = json.loads(flags["hyper-spec"])
        except json.JSONDecodeError as e:
            usage_error(f"Invalid hyper-spec JSON: {e}")
    if "rabc" in flags:
        body["use_rabc"] = True
        body["sarm_reward_model_path"] = flags["rabc"]
        if "rabc-image-key" in flags:
            body["sarm_image_observation_key"] = flags["rabc-image-key"]
        if "rabc-head-mode" in flags:
            body["rabc_head_mode"] = flags["rabc-head-mode"]

    result = api_request("POST", "/v1/finetune", body)
    if JSON_MODE:
        emit(result)
        return
    print(f"Job created: {result.get('job_id', 'unknown')}")
    print(f"Status: {result.get('status', 'unknown')}")
    if result.get("message"):
        print(f"Message: {result['message']}")


def cmd_status(args):
    if not args:
        usage_error("Usage: qualia.py status <job_id>")
    result = api_request("GET", f"/v1/finetune/{args[0]}")
    if JSON_MODE:
        emit(result)
        return
    print(f"Job {result.get('job_id', '?')}")
    print(f"Status: {result.get('status', '?')} | Phase: {result.get('current_phase', '?')}")
    print()
    for phase in result.get("phases", []):
        status_str = phase.get("status", "?").upper()
        name = phase.get("name", "?")
        started = ""
        if phase.get("started_at"):
            started = f" (started {phase['started_at'][:10]})"
        print(f"[{status_str}] {name}{started}")
        if phase.get("error"):
            print(f"  Error: {phase['error']}")
        for event in phase.get("events", []):
            ev_status = event.get("status", "?")
            ev_msg = event.get("message", "")
            ev_err = f" | {event['error']}" if event.get("error") else ""
            ev_retry = f" (retry {event['retry_attempt']})" if event.get("retry_attempt", 0) > 0 else ""
            print(f"  → [{ev_status}] {ev_msg}{ev_err}{ev_retry}")


def cmd_cancel(args):
    if not args:
        usage_error("Usage: qualia.py cancel <job_id>")
    result = api_request("POST", f"/v1/finetune/{args[0]}/cancel")
    if JSON_MODE:
        emit(result)
        return
    status = "cancelled" if result.get("cancelled") else "cancellation failed"
    msg = f" - {result['message']}" if result.get("message") else ""
    print(f"Job {result.get('job_id', '?')}: {status}{msg}")


def cmd_doctor(_args):
    """Self-test: env var, auth/connectivity, models endpoint."""
    checks = []

    # Check 1: QUALIA_API_KEY set
    key_set = bool(os.environ.get("QUALIA_API_KEY", ""))
    checks.append({
        "name": "QUALIA_API_KEY set",
        "pass": key_set,
        "detail": "environment variable present" if key_set
                  else "set QUALIA_API_KEY before use",
    })

    # Check 2: GET /v1/credits (auth + connectivity)
    balance = None
    if key_set:
        try:
            result = api_request("GET", "/v1/credits")
            balance = result.get("balance")
            checks.append({
                "name": "API auth (GET /v1/credits)",
                "pass": True,
                "detail": f"balance: {balance}",
            })
        except CliError as e:
            checks.append({
                "name": "API auth (GET /v1/credits)",
                "pass": False,
                "detail": e.message,
            })
    else:
        checks.append({
            "name": "API auth (GET /v1/credits)",
            "pass": False,
            "detail": "skipped: no API key",
        })

    # Check 3: GET /v1/models
    model_count = None
    if key_set:
        try:
            result = api_request("GET", "/v1/models")
            models = result.get("data", [])
            model_count = len(models)
            checks.append({
                "name": "Models endpoint (GET /v1/models)",
                "pass": model_count > 0,
                "detail": f"{model_count} models available",
            })
        except CliError as e:
            checks.append({
                "name": "Models endpoint (GET /v1/models)",
                "pass": False,
                "detail": e.message,
            })
    else:
        checks.append({
            "name": "Models endpoint (GET /v1/models)",
            "pass": False,
            "detail": "skipped: no API key",
        })

    all_pass = all(c["pass"] for c in checks)

    if JSON_MODE:
        emit({
            "ok": all_pass,
            "checks": checks,
            "credits": balance,
            "model_count": model_count,
        })
    else:
        for c in checks:
            mark = "PASS" if c["pass"] else "FAIL"
            print(f"[{mark}] {c['name']}: {c['detail']}")
        passed = sum(1 for c in checks if c["pass"])
        print()
        print(f"{passed}/{len(checks)} checks passed"
              + ("" if all_pass else " - doctor found problems"))

    if not all_pass:
        sys.exit(EXIT_GENERIC)


HELP_TEXT = """Qualia CLI - VLA fine-tuning platform

Usage: qualia.py [--json] <command> [args]

Global flags:
  --json                                     Machine-readable output (single JSON object/array on stdout)

Commands:
  doctor                                     Self-test: env, auth, connectivity
  credits                                    Check credit balance
  models                                     List VLA types, camera slots, base models
  instances                                  List GPU instances with specs and pricing

  projects                                   List projects with jobs
  project-create <name> [description]        Create a project
  project-delete <project_id>                Delete a project (no active jobs)

  dataset-keys <dataset_id>                  List image keys in a HuggingFace dataset
  hyperparams <vla_type> [model_id]          Get default hyperparameters
  hyperparams-validate <vla_type> '<json>'   Validate custom hyperparameters

  finetune <project_id> <vla_type> <dataset_id> <hours> '<cameras>' [--flags]
    --model <id>         Base model ID (required for smolvla/pi0/pi05)
    --name <str>         Job display name
    --instance <id>      GPU instance type
    --region <name>      Cloud region
    --batch-size <n>     Batch size (1-512)
    --hyper-spec '<json>' Custom hyperparameters
    --rabc <model_path>  Enable RA-BC with SARM reward model (HF path)
    --rabc-image-key <k> Image key for reward annotations
    --rabc-head-mode <m> RA-BC head mode (e.g. sparse)

  status <job_id>                            Check job status and phase history
  cancel <job_id>                            Cancel a running job

VLA types: act, smolvla, pi0, pi05, gr00t_n1_5, sarm
  model_id REQUIRED for: smolvla, pi0, pi05
  model_id NOT supported for: act, gr00t_n1_5, sarm
  RA-BC supported for: smolvla, pi0, pi05

Exit codes:
  0 ok | 1 generic | 2 usage | 3 auth | 4 insufficient credits
  5 validation | 6 not found | 7 connection"""


def cmd_help(_args):
    if JSON_MODE:
        emit({"commands": sorted(COMMANDS.keys()), "usage": HELP_TEXT})
        return
    print(HELP_TEXT)


COMMANDS = {
    "doctor": cmd_doctor,
    "credits": cmd_credits,
    "models": cmd_models,
    "instances": cmd_instances,
    "projects": cmd_projects,
    "project-create": cmd_project_create,
    "project-delete": cmd_project_delete,
    "dataset-keys": cmd_dataset_keys,
    "hyperparams": cmd_hyperparams,
    "hyperparams-validate": cmd_hyperparams_validate,
    "finetune": cmd_finetune,
    "status": cmd_status,
    "cancel": cmd_cancel,
    "help": cmd_help,
}


def main():
    global JSON_MODE
    args = sys.argv[1:]

    # Strip the global --json flag wherever it appears.
    if "--json" in args:
        JSON_MODE = True
        args = [a for a in args if a != "--json"]

    cmd = args[0] if args else "help"
    rest = args[1:] if len(args) > 1 else []

    handler = COMMANDS.get(cmd)
    if handler is None:
        fail(CliError(EXIT_USAGE, f"Unknown command: {cmd}",
                      {"hint": "Run 'qualia.py help' for available commands."}))

    try:
        handler(rest)
    except CliError as err:
        fail(err)


if __name__ == "__main__":
    main()
