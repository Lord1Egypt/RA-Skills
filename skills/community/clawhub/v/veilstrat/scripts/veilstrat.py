#!/usr/bin/env python3
"""Read-only VeilStrat API client. Python 3.9+, standard library only."""

import argparse
import datetime
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE_URL = "https://app.veilstrat.com/api/v1"
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
TIMEOUT_SECONDS = 30
USAGE_HEADERS = (
    "X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset",
    "X-RateLimit-Policy", "Retry-After",
)


class ClientError(Exception):
    def __init__(self, code, message, status=None, details=None, usage=None):
        super().__init__(message)
        self.code = code
        self.status = status
        self.details = details
        self.usage = usage or {}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent sending authenticated requests to a redirected destination."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sanitize(value, api_key):
    if isinstance(value, dict):
        return {key: sanitize(item, api_key) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item, api_key) for item in value]
    if isinstance(value, str):
        return value.replace(api_key, "[REDACTED]") if api_key else value
    return value


def request_api(method, path, body=None, query=None):
    api_key = os.environ.get("VEILSTRAT_API_KEY", "").strip()
    if not api_key:
        raise ClientError("missing_api_key", "Configure VEILSTRAT_API_KEY as an execution-environment secret. See https://app.veilstrat.com/docs/api.")
    if not re.fullmatch(r"vs_[A-Za-z0-9_-]+", api_key):
        raise ClientError("invalid_api_key", "VEILSTRAT_API_KEY must be a vs_ team API key without whitespace.")
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    headers = {
        "Authorization": "Bearer " + api_key,
        "Accept": "application/json",
        "User-Agent": "VeilStrat-Agent-Skill/1.0.0",
    }
    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    opener = urllib.request.build_opener(NoRedirect())
    try:
        response = opener.open(req, timeout=TIMEOUT_SECONDS)
    except urllib.error.HTTPError as exc:
        usage = {name: exc.headers[name] for name in USAGE_HEADERS if exc.headers.get(name) is not None}
        try:
            with exc:
                raw = exc.read(MAX_RESPONSE_BYTES + 1)
            details = json.loads(raw) if len(raw) <= MAX_RESPONSE_BYTES else None
        except (ValueError, OSError):
            details = None
        messages = {
            401: "VeilStrat rejected the API key. Configure a valid team key.",
            403: "VeilStrat denied API access. Check the Pro API Access add-on and key permissions.",
            404: "The company, slice, or endpoint was not found.",
            422: "VeilStrat rejected the query or filters. Check the filter catalog and API docs.",
            429: "VeilStrat quota reached. Respect Retry-After and resetUnix before another request.",
        }
        message = messages.get(exc.code, "VeilStrat returned an HTTP error; no automatic retry was attempted.")
        raise ClientError("http_error", message, exc.code, sanitize(details, api_key), usage) from None
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
        raise ClientError("network_error", "Could not reach VeilStrat. No automatic retry was attempted.") from None
    try:
        with response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            status = response.status
            usage = {name: response.headers[name] for name in USAGE_HEADERS if response.headers.get(name) is not None}
    except (OSError, TimeoutError, socket.timeout):
        raise ClientError("network_error", "VeilStrat response was interrupted. No automatic retry was attempted.") from None
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ClientError("response_too_large", "VeilStrat response exceeded the 4 MiB safety limit.", status, usage=usage)
    try:
        data = json.loads(raw)
    except ValueError:
        raise ClientError("invalid_response", "VeilStrat returned a non-JSON response.", status, usage=usage) from None
    return {
        "ok": True, "status": status, "data": sanitize(data, api_key),
        "usage": usage, "source": url,
        "retrievedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def bounded_int(minimum, maximum):
    def parse(value):
        try:
            number = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Use an integer.") from None
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError("Use a value from %s to %s." % (minimum, maximum))
        return number
    return parse


def countries_arg(value):
    codes = list(dict.fromkeys(part.strip().upper() for part in value.split(",")))
    if not codes or any(not re.fullmatch(r"[A-Z]{2}", code) for code in codes):
        raise argparse.ArgumentTypeError("Use comma-separated two-letter country codes, such as US,GB.")
    return codes


def nonempty(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("Use a non-empty value.")
    return value.strip()


def company_id(value):
    try:
        return str(uuid.UUID(value))
    except ValueError:
        raise argparse.ArgumentTypeError("Use a company UUID returned by VeilStrat.") from None


def slice_slug(value):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Use a lowercase slice slug from VeilStrat.")
    return value


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="command", required=True)
    for command in ("health", "stats", "filters"):
        commands.add_parser(command)
    search = commands.add_parser("search", help="Search companies with a required signal query.")
    search.add_argument("--query", required=True, type=nonempty)
    search.add_argument("--countries", type=countries_arg)
    search.add_argument("--limit", type=bounded_int(1, 50), default=10)
    search.add_argument("--page", type=bounded_int(1, 500), default=1)
    company = commands.add_parser("company", help="Retrieve a company signal dossier.")
    company.add_argument("id", type=company_id)
    slices = commands.add_parser("slices", help="Search a buying-window slice with at least one filter.")
    slices.add_argument("--slice", required=True, type=slice_slug)
    slices.add_argument("--countries", type=countries_arg)
    slices.add_argument("--score-min", type=bounded_int(0, 100))
    return p


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    if args.command == "search" and args.page * args.limit > 500:
        p.error("Search offset plus page size cannot exceed 500. Narrow the query.")
    if args.command == "slices" and args.countries is None and args.score_min is None:
        p.error("slices requires --countries and/or --score-min.")
    try:
        if args.command in ("health", "stats", "filters"):
            result = request_api("GET", "/" + args.command)
        elif args.command == "company":
            result = request_api("GET", "/companies/" + args.id)
        elif args.command == "search":
            body = {"signal_query": args.query, "page": args.page, "pageSize": args.limit}
            if args.countries:
                body["countries"] = args.countries
            result = request_api("POST", "/companies", body=body)
        else:
            query = {"slice": args.slice}
            if args.countries:
                query["countries"] = ",".join(args.countries)
            if args.score_min is not None:
                query["scoreMin"] = args.score_min
            result = request_api("GET", "/slices", query=query)
    except ClientError as exc:
        error = {"ok": False, "status": exc.status, "error": {"code": exc.code, "message": str(exc)}, "usage": exc.usage}
        if exc.details is not None:
            error["error"]["details"] = exc.details
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
