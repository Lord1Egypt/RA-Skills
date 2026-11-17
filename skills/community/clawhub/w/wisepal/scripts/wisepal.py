"""WisePal onboarding CLI and shared private credential storage (standard library only)."""
import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import UUID, uuid4

DEFAULT_BASE_URL = "https://my.wisepal.com"
MAX_INPUT_BYTES = 32768


def submission_token(directory, submission_id, *, create, bootstrap=None):
    """Publish a private token atomically before any HTTP request; never overwrite."""
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if stat.S_IMODE(directory.stat().st_mode) & 0o077:
        raise ValueError("Credential directory must be private")
    path = directory / (str(submission_id) + ".token")
    if create and not path.exists():
        if bootstrap is None:
            raise ValueError("Server credential bootstrap is required")
        token = bootstrap()
        if not isinstance(token, str) or not re.fullmatch(r"wpg_[A-Za-z0-9_-]{43}", token):
            raise ValueError("Credential bootstrap failed")
        descriptor, temporary = tempfile.mkstemp(dir=directory)
        try:
            with os.fdopen(descriptor, "w") as file:
                file.write(token)
                file.flush()
                os.fsync(file.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                pass  # Another process published this submission's token first.
            if hasattr(os, "O_DIRECTORY"):
                folder = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(folder)
                finally:
                    os.close(folder)
        finally:
            os.unlink(temporary)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor) as file:
        if stat.S_IMODE(os.fstat(file.fileno()).st_mode) & 0o077:
            raise ValueError("Credential file must be private")
        token = file.read(129)
    if not re.fullmatch(r"wpg_[A-Za-z0-9_-]{43}", token):
        raise ValueError("Invalid stored credential; restore it rather than replacing it")
    return token



def client_paths(base_url, state_dir=None):
    parsed = urlsplit(base_url)
    if not parsed.hostname or (parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"})):
        raise ValueError("Use HTTPS for the REST API, or loopback HTTP for local testing")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Supply a plain REST API base URL")
    root = base_url.rstrip("/")
    directory = Path(state_dir or Path.home() / ".wisepal" / "agent-onboarding")
    directory /= hashlib.sha256(root.encode()).hexdigest()
    directory /= "v2"
    return root + "/api/agent-onboarding/v2/submissions", directory


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        return None  # Never forward contact data or a capability to another URL.


def attribution_headers(distribution_id, assistant="unknown", campaign="unknown"):
    values = {"X-WisePal-Distribution": distribution_id,
              "X-WisePal-Assistant": assistant, "X-WisePal-Campaign": campaign}
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value) for value in values.values()):
        raise ValueError("Attribution identifiers must be lowercase slugs of at most 64 characters")
    return values


def request_json(method, url, token, payload=None, *, headers=None):
    data = json.dumps(payload, allow_nan=False).encode() if payload is not None else None
    request = Request(url, data=data, method=method, headers={
        **({"Authorization": "Bearer " + token} if token else {}),
        "Content-Type": "application/json",
        "Accept": "application/json",
        **(headers or {}),
    })
    try:
        response = build_opener(NoRedirect()).open(request, timeout=120)
    except HTTPError as error:
        response = error
    with response:
        if response.status in {200, 201, 400, 401, 403, 404, 409, 413, 415, 422, 429, 503}:
            result = json.load(response)
            if isinstance(result, dict):
                return result
    return {"error": "api_unavailable", "retry": "Reuse the same idempotency key and payload."}


def call_api(operation, submission_id, payload=None, *, base_url=DEFAULT_BASE_URL, state_dir=None, headers=None):
    submission_id = UUID(str(submission_id))
    base, directory = client_paths(base_url, state_dir)
    try:
        legacy = directory.parent / (str(submission_id) + ".token")
        if legacy.exists():
            return {"error": "legacy_submission", "recovery": "Resume this submission with the original version 1 client, or connect with Google using the same email. Never create a duplicate signup."}
        token = submission_token(directory, submission_id, create=operation == "begin",
            bootstrap=lambda: request_json("POST", base_url.rstrip("/") + "/api/agent-onboarding/v2/credentials", "").get("access_token"))
    except FileNotFoundError:
        return {"error": "credentials_missing", "recovery": "Restore the connector's private state for the original submission. Do not create a duplicate negotiation."}
    except (OSError, URLError, ValueError):
        return {"error": "credentials_unavailable", "recovery": "Restore or repair the connector's private credential storage, then retry the original submission."}
    url = base if operation == "begin" else base + "/" + str(submission_id)
    if operation in {"details", "approve"}:
        url += "/" + {"details": "details", "approve": "consent"}[operation]
    try:
        return request_json("GET" if operation == "status" else "POST", url, token, payload,
                            headers=headers if operation == "begin" else None)
    except (OSError, URLError, ValueError):
        return {"error": "api_unavailable", "retry": "Reuse the same idempotency key and payload."}


def main():
    parser = argparse.ArgumentParser(description="WisePal free bill negotiation; JSON input through stdin.")
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("headers", help="Runtime credential hook ONLY: emits secret Authorization JSON; never invoke as a model tool.")
    commands.add_parser("new-id", help="Generate a UUID to retain for this submission and all retries.")
    commands.add_parser("begin", help="Register name, mobile, email and selected services; no calls.")
    for name in ["details", "approve", "status"]:
        command = commands.add_parser(name)
        command.add_argument("submission_id", type=UUID)
    command = commands.add_parser("schema", help="Read the published request schema; no network or credentials.")
    command.add_argument("step", choices=["begin", "details", "approve"])
    args = parser.parse_args()
    try:
        if args.operation == "headers":
            base_url = os.environ.get("WISEPAL_API_BASE_URL", DEFAULT_BASE_URL)
            _, directory = client_paths(base_url, os.environ.get("WISEPAL_AGENT_STATE_DIR"))
            token = submission_token(directory / "connection", "runtime", create=True,
                bootstrap=lambda: request_json("POST", base_url.rstrip("/") + "/api/agent-onboarding/v2/credentials", "").get("access_token"))
            package = json.loads((Path(__file__).resolve().parent.parent / "distribution.json").read_text())
            result = {"Authorization": "Bearer " + token, **attribution_headers(package["distribution_id"],
                os.environ.get("WISEPAL_ASSISTANT", package["assistant"]), package["campaign"])}
        elif args.operation == "new-id":
            result = {"idempotency_key": str(uuid4())}
        elif args.operation == "schema":
            path = Path(__file__).resolve().parent.parent / "references" / "request-schemas.json"
            result = json.loads(path.read_text())[args.step]
        else:
            payload = None
            if args.operation != "status":
                raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
                if len(raw) > MAX_INPUT_BYTES:
                    raise ValueError("Request JSON exceeds 32 KiB")
                payload = json.loads(raw)
                if not isinstance(payload, dict):
                    raise ValueError("Supply a JSON object through stdin")
            submission_id = payload.get("idempotency_key") if args.operation == "begin" else args.submission_id
            headers = None
            if args.operation == "begin":
                package = json.loads((Path(__file__).resolve().parent.parent / "distribution.json").read_text())
                headers = attribution_headers(
                    package["distribution_id"], os.environ.get("WISEPAL_ASSISTANT", package["assistant"]),
                    package["campaign"],
                )
            result = call_api(args.operation, submission_id, payload,
                base_url=os.environ.get("WISEPAL_API_BASE_URL", DEFAULT_BASE_URL),
                state_dir=os.environ.get("WISEPAL_AGENT_STATE_DIR"), headers=headers)
    except (OSError, ValueError):
        result = {"error": "invalid_input", "recovery": "Use the matching request schema and a valid submission UUID. Keep the original UUID when correcting input."}
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
