#!/usr/bin/env python3
"""
SMB Sales Boost API client - part of the smb-sales-boost agent skill (v1.9.6).

One dependency-free command (Python 3.8+ standard library only) for every
SMB Sales Boost REST API call. It handles authentication, parameter encoding,
safe file saving, bounded retries and safety confirmations.

Authentication
  Set the SMB_SALES_BOOST_API_KEY environment variable to your API key. Keys
  start with smbk_ and are created in the dashboard (Dashboard > API). Passing
  the key as the first argument still works for backward compatibility, but it
  is discouraged: command lines can be seen by other local processes and are
  often written to logs.

Usage
  python3 smb_api.py METHOD ENDPOINT [options]

  METHOD    GET, POST, PATCH, PUT or DELETE
  ENDPOINT  a path below https://smbsalesboost.com/api/v1, for example /leads

Options
  --params JSON        query parameters as a JSON object (any method). Lists may
                       be given as real JSON arrays; they are encoded the way
                       each parameter expects.
  --params-file PATH   read the query parameters from a JSON file ("-" = stdin)
  --body JSON          request body as a JSON object (POST, PATCH, PUT)
  --body-file PATH     read the request body from a JSON file ("-" = stdin)
  --confirm            required for calls that charge money or authorize future
                       charges, send email, spend credits on enrichment, search
                       or export leads without a maxCredits cap, send lead data
                       to an outside destination (creating, connecting,
                       re-pointing, re-enabling, testing or pushing to an
                       integration, retrying a delivery, changing or testing a
                       CRM field mapping), cancel the subscription or delete
                       data. Add it only after the user has explicitly
                       approved that exact action.
  --dry-run            print the request that would be sent, then exit
  --output-dir DIR     folder for downloaded and exported files (default:
                       $SMB_SALES_BOOST_OUTPUT_DIR, else /mnt/user-data/outputs
                       when it exists, else ./smb-sales-boost-files)
  --out NAME           also save the full JSON response as NAME.json in the
                       output folder (useful for large lead searches)
  --compact            print lead results as a short summary of key fields
  --idempotency-key K  reuse the key printed by a call that timed out. For
                       POST /purchase-credits Stripe does not charge the same key
                       twice for about 24 hours; for the long-running calls below
                       the server returns the same job instead of running it again
  --async              long-running calls: ask the server to answer 202 with a
                       jobId at once, and print it instead of following it
  --no-wait            long-running calls: do not follow a 202 answer; print the
                       jobId (follow it later with GET /jobs/<jobId>)
  --job-timeout SEC    how long to follow a 202 answer before printing the jobId
                       instead (default 3600)
  --timeout SEC        network timeout in seconds (default 180)
  --no-retry           do not retry after 429 or 503 responses (calls that
                       change or send through an integration are never
                       retried automatically)
  --no-fetch           for download-link endpoints, print the link instead of
                       downloading the file

Examples
  export SMB_SALES_BOOST_API_KEY=smbk_...
  python3 smb_api.py GET /me
  python3 smb_api.py GET /leads/preview --params '{"positiveKeywords":["*dental*","*dentist*"],"stateInclude":["TX"],"limit":25}'
  python3 smb_api.py GET /leads --params '{"positiveKeywords":["*dental*"],"stateInclude":["TX"],"limit":25,"maxCredits":25}' --compact
  python3 smb_api.py POST /leads/export --body '{"filters":{"positiveKeywords":["*med*spa*"],"stateInclude":["FL"]},"maxCredits":100}'
  python3 smb_api.py GET /export-history/412/download
  python3 smb_api.py POST /purchase-credits --body '{"creditCount":500}' --confirm
  python3 smb_api.py GET /integrations
  python3 smb_api.py POST /integrations/webhook --body-file hook.json --confirm

Credit caps
  GET /leads (query) and POST /leads/export (body) should always carry
  maxCredits, a whole number of 0 or more (0 returns only leads you already
  have, free). Without it the call needs --confirm, because it can spend up to
  the page limit (GET /leads) or the whole balance (export). A maxCredits of
  null, a negative number, a decimal, a boolean or text is refused before
  anything is sent, because the API would treat it as "no cap". On GET /leads
  a limit, when given, must be a whole number from 1 to 1000, given once (the
  API reads 0 or a bad value as 100, and the page limit is the most one call
  can spend).

Integrations
  Integrations send lead data (business contact details) to outside systems
  (CRMs, Zapier, n8n, Make, Pipedream, Clay, any webhook URL) and keep doing so
  automatically. Reading them (GET) needs no confirmation; every call that
  creates, connects, re-points, re-enables, tests or pushes, or changes the
  header apiKey sent to the destination, needs --confirm. The signingSecret
  returned when a webhook integration is created is shown only once: hand it
  to the user and do not log or save it.

Long-running calls
  POST /leads/export, POST /email-schedules/{id}/trigger,
  POST /ai/suggest-categories and POST /lead-export-history/refresh,
  /refresh-and-export and /re-export run as background jobs on the server.
  They answer as usual when the work finishes within about 75 seconds;
  otherwise the server answers 202 with a jobId, and this script follows it
  (GET /jobs/<jobId>, up to 50 seconds per poll, progress on stderr) and then
  handles the final answer exactly like the original call, so files are saved
  the same way. Each of these calls sends an Idempotency-Key (printed on
  stderr): if a call times out, re-run it with --idempotency-key <key> and the
  server returns the same job instead of exporting or sending again (the key
  is kept with the job for up to about 25 hours after it finishes, about 48
  hours for a schedule trigger; a server restart forgets it). Only a 409, 429
  or 503 answer, or an export's 402, frees the key: after any other error, or
  with changed arguments, run without --idempotency-key so a new key is sent.
  GET /jobs/<jobId> can also be called directly.

Retries
  A 429 or 503 with a Retry-After of 60 seconds or less is retried (up to 3
  attempts), except for calls that change or send through an integration
  (anything but GET under /integrations): those return the error with advice,
  so the agent checks GET /integrations or the delivery log before repeating.

Exit codes
  0 success (also a long-running call that is still running when it is not
  followed: --async, --no-wait or --job-timeout), 1 API error (or an
  unexpected client error), 2 usage error or confirmation required (nothing
  sent), 3 network error or timeout, 4 local file error (checked before
  anything is sent)
"""

import argparse
import base64
import binascii
import http.client
import json
import os
import re
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

__version__ = "1.9.6"

API_ORIGIN = "https://smbsalesboost.com"
API_PREFIX = "/api/v1"
USER_AGENT = "smb-sales-boost-skill/%s (+https://github.com/Tomsonx232/smb-sales-boost-skill)" % __version__

KEY_ENV_VAR_NAME = "SMB_SALES_BOOST_API_KEY"
ENV_OUTPUT_DIR = "SMB_SALES_BOOST_OUTPUT_DIR"
SANDBOX_OUTPUT_DIR = "/mnt/user-data/outputs"
FALLBACK_OUTPUT_DIR = "smb-sales-boost-files"

METHODS = ("GET", "POST", "PATCH", "PUT", "DELETE")
DEFAULT_TIMEOUT = 180
MAX_ATTEMPTS = 3
MAX_RETRY_WAIT_SECONDS = 60
CHUNK_SIZE = 65536

SAFE_EXTENSIONS = (".csv", ".json", ".xlsx")
EXTENSION_BY_FILE_TYPE = {"csv": ".csv", "json": ".json", "xlsx": ".xlsx"}
EXTENSION_BY_CONTENT_TYPE = {
    "text/csv": ".csv",
    "application/json": ".json",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
}

# These two endpoints are public: an API key is never sent to them.
PUBLIC_ENDPOINTS = ("/purchase", "/claim-key")
# Presigned download links are only ever fetched from Amazon S3 hosts, over HTTPS.
PRESIGNED_HOST_RE = re.compile(r"(?:[a-z0-9.-]+\.)?s3(?:[.-][a-z0-9-]+)*\.amazonaws\.com")

# Query parameters that take a comma-separated list rather than a JSON array.
COMMA_LIST_PARAMS = frozenset([
    "stateInclude", "stateExclude", "websiteSchemaFilter",
    "buyingSignalTypeFilter", "updateReasonFilter",
])
# Export filter keys whose plain-string form is split on commas.
EXPORT_SPLIT_KEYS = COMMA_LIST_PARAMS | frozenset([
    "cityInclude", "cityExclude", "zipInclude", "zipExclude", "streetInclude", "streetExclude",
])
# Export filter keys that also accept a string, so they are left alone.
EXPORT_STRING_OK_KEYS = frozenset(["positiveKeywords", "negativeKeywords", "orColumns"])
# Every other export filter with one of these suffixes must be a real JSON array.
EXPORT_LIST_SUFFIXES = ("Include", "Exclude", "IncludeTerms", "ExcludeTerms", "Values")
EXPORT_INT_KEYS = ("maxLeads", "maxResults", "maxCredits")
EXPORT_BOOL_KEYS = ("excludePurchased", "inline")

COMPACT_FIELDS = (
    "id", "Company Name", "City", "State", "Phone Primary", "Email Primary",
    "Registered URL", "AI Categories", "Last Buying Signal", "Buying Signal Type",
    "contactExported",
)

HEADERS_TO_REPORT = (
    "X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset",
    "Retry-After", "X-Credits-Capped", "X-Lead-Query-Path",
    "X-SMBSB-Job-Id", "X-SMBSB-Job-Status",
)

EXPORT_RE = re.compile(r"/leads/export")
HISTORY_LINK_RE = re.compile(r"/export-history/(\d+)/download-url")
ENRICHMENT_LINK_RE = re.compile(r"/enrichments/(\d+)/download")
TRIGGER_RE = re.compile(r"/email-schedules/\d+/trigger")
SCHEDULE_RECIPIENT_KEYS = ("recipients", "fullCopyRecipients", "combinedRecipients", "combinedFileEnabled")
SCHEDULE_SEARCH_KEYS = ("filterPresetId", "maxLeadsPerEmail")
SCHEDULE_RE = re.compile(r"/email-schedules/\d+")
# Integrations (paths are already lower case when these are matched).
INTEGRATION_ID_RE = re.compile(r"/integrations/[^/]+")
INTEGRATION_CONNECT_RE = re.compile(r"/integrations/[^/]+/connect")
INTEGRATION_SEND_RE = re.compile(r"/integrations/[^/]+/(test|push-lead)")
INTEGRATION_RETRY_RE = re.compile(r"/integrations/[^/]+/deliveries/[^/]+/retry")
INTEGRATION_MAPPING_RE = re.compile(r"/integrations/[^/]+/field-mapping")
INTEGRATION_MAPPING_TEST_RE = re.compile(r"/integrations/[^/]+/field-mapping/test")
INTEGRATION_DESTINATION_KEYS = ("subscriptions", "defaultTargetUrl", "pipedriveDeals")
INTEGRATION_RATE_LIMITS = "60 integration requests per minute per account, 30 per minute for connect"
LEADS_DEFAULT_LIMIT = 100
LEADS_MAX_LIMIT = 1000
# Long-running calls (background jobs on the server, 2026-10-14). The trigger and the export
# are matched by TRIGGER_RE / EXPORT_RE; GET /jobs/<jobId> follows a 202 answer.
JOB_ROUTE_PATHS = (
    "/ai/suggest-categories", "/lead-export-history/refresh",
    "/lead-export-history/refresh-and-export", "/lead-export-history/re-export",
)
JOB_STATUS_RE = re.compile(r"/jobs/([a-f0-9]{32})")
JOB_ID_RE = re.compile(r"[a-f0-9]{32}")
SERVER_JOB_WAIT_SECONDS = 75
JOB_POLL_WAIT_SECONDS = 50
JOB_POLL_MIN_TIMEOUT = 70
DEFAULT_JOB_TIMEOUT = 3600
JOB_POLL_MAX_NETWORK_FAILURES = 3


class UsageError(Exception):
    """Bad command line or input; nothing was sent."""


class LocalFileError(Exception):
    """A file could not be written locally."""


class NetworkError(Exception):
    """The request did not complete (timeout, dropped connection, DNS, TLS)."""


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Never follow redirects, so an API key is never forwarded to another host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirectHandler())


# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------

def emit(obj):
    """Print a JSON document to stdout."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def note(message):
    """Print an advisory line to stderr (never mixed into the JSON on stdout)."""
    print("note: " + message, file=sys.stderr)


def _configure_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --------------------------------------------------------------------------
# Input parsing and normalization
# --------------------------------------------------------------------------

def load_json_arg(text, path, label):
    """Read a JSON object from --X or --X-file. Returns None when neither is given."""
    if text is not None and path is not None:
        raise UsageError("use either --%s or --%s-file, not both" % (label, label))
    if path is not None:
        try:
            if path == "-":
                raw = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read().encode("utf-8")
            else:
                with open(path, "rb") as handle:
                    raw = handle.read()
        except OSError as exc:
            raise UsageError("could not read --%s-file: %s" % (label, exc))
        try:
            # Windows PowerShell writes UTF-16 with a byte-order mark, or UTF-8 with a BOM.
            if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
                text = raw.decode("utf-16")
            else:
                text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise UsageError("--%s-file must be saved as UTF-8 text" % label)
    if text is None:
        return None
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise UsageError("--%s is not valid JSON: %s" % (label, exc))
    if not isinstance(value, dict):
        raise UsageError("--%s must be a JSON object, for example {\"limit\": 25}" % label)
    return value


def normalize_endpoint(raw):
    """Return (path, query_pairs). The path is relative to /api/v1 and strictly validated."""
    text = (raw or "").strip()
    if text.startswith(API_ORIGIN):
        text = text[len(API_ORIGIN):]
    path, _, query = text.partition("?")
    # Every API path is lower case and the server matches paths without regard to case,
    # so normalize here to keep the --confirm, public-endpoint and idempotency checks exact.
    path = path.lower()
    if not path.startswith("/"):
        path = "/" + path
    if path == API_PREFIX or path.startswith(API_PREFIX + "/"):
        path = path[len(API_PREFIX):] or "/"
    if len(path) > 1:
        path = path.rstrip("/")
    if "//" in path or not re.fullmatch(r"/[A-Za-z0-9/_-]*", path):
        raise UsageError(
            "invalid endpoint %r: use a path such as /leads or /export-history/12/download "
            "and pass query parameters with --params" % raw)
    return path, urllib.parse.parse_qsl(query, keep_blank_values=True)


def _split_list_string(text):
    stripped = text.strip()
    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
        except ValueError:
            parsed = None
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    return [part.strip() for part in text.split(",") if part.strip()]


def _is_list_param(key):
    """Parameters the API reads as a JSON array (everything except the comma-separated ones)."""
    return key not in COMMA_LIST_PARAMS and (key in EXPORT_STRING_OK_KEYS or key.endswith(EXPORT_LIST_SUFFIXES))


def _as_list(value):
    """A list parameter given as one value: parse a JSON-array string, else split on commas and trim."""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
            except ValueError:
                parsed = None
            if isinstance(parsed, list):
                return parsed
        return [part.strip() for part in value.split(",") if part.strip()]
    return [value]


def _list_items(items):
    """Numbers inside a list are sent as text (ZIP codes and similar are stored as text)."""
    return [item if isinstance(item, (str, dict)) else str(item) for item in items]


def encode_query(params, notes):
    """Encode query parameters the way the SMB Sales Boost API expects them."""
    pairs = []
    for key, value in params.items():
        if value is None:
            continue
        if _is_list_param(key) and isinstance(value, (str, int, float)) and not isinstance(value, bool):
            if not isinstance(value, str) or "," in value:
                notes.append("%s: sent as a JSON array (the API ignores a bare value such as a single "
                             "ZIP code, and does not trim comma-separated items)" % key)
            value = _as_list(value)
        if isinstance(value, bool):
            pairs.append((key, "true" if value else "false"))
        elif isinstance(value, (int, float)):
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            pairs.append((key, str(value)))
        elif isinstance(value, (list, tuple)):
            if key in COMMA_LIST_PARAMS:
                pairs.append((key, ",".join(str(item).strip() for item in value)))
            else:
                pairs.append((key, json.dumps(_list_items(value), ensure_ascii=False, separators=(",", ":"))))
        elif isinstance(value, dict):
            pairs.append((key, json.dumps(value, ensure_ascii=False, separators=(",", ":"))))
        else:
            text = str(value)
            if key in COMMA_LIST_PARAMS and text.strip().startswith("["):
                items = _split_list_string(text)
                notes.append("%s: converted a JSON-array string to the comma-separated form this "
                             "parameter needs" % key)
                text = ",".join(items)
            pairs.append((key, text))
    return pairs


def _normalize_filter_value(key, value, notes):
    is_list_key = key in EXPORT_SPLIT_KEYS or key.endswith(EXPORT_LIST_SUFFIXES)
    if is_list_key and isinstance(value, (int, float)) and not isinstance(value, bool):
        notes.append("filters.%s: wrapped the number in an array (export filters ignore non-array values)" % key)
        return [str(value)]
    if is_list_key and isinstance(value, list):
        return _list_items(value)
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
        except ValueError:
            parsed = None
        if isinstance(parsed, list):
            if key not in EXPORT_STRING_OK_KEYS:
                notes.append("filters.%s: converted a JSON-array string to a real array "
                             "(export filters ignore the string form)" % key)
            return parsed
    if key in EXPORT_STRING_OK_KEYS:
        return value
    if key in EXPORT_SPLIT_KEYS:
        notes.append("filters.%s: split the comma-separated string into an array" % key)
        return _split_list_string(value)
    if key.endswith(EXPORT_LIST_SUFFIXES):
        notes.append("filters.%s: wrapped the string in an array (export filters ignore "
                     "plain strings)" % key)
        return [value]
    return value


EXPORT_TOP_LEVEL_KEYS = ("maxCredits", "maxResults", "maxLeads", "excludePurchased", "inline", "formatId")
EXPORT_IGNORED_FILTER_KEYS = ("search", "page", "limit")


def checked_max_credits(value, where):
    """Return maxCredits as a whole number of 0 or more, or raise UsageError.

    The API treats null (and, on GET /leads, any non-number or negative value) as "no cap",
    so anything that is not a plain whole number is refused instead of being sent or dropped.
    """
    if value is None:
        raise UsageError(
            "%s is null, which the API treats as no credit cap. Send a whole number of 0 or more "
            "(0 returns only leads you already have, free), or leave it out and get the user's approval "
            "for an uncapped spend (--confirm)." % where)
    if isinstance(value, bool):
        raise UsageError("%s must be a whole number of 0 or more, not a true/false value" % where)
    if isinstance(value, int):
        number = value
    elif isinstance(value, float) and value.is_integer():
        number = int(value)
    elif isinstance(value, str) and re.fullmatch(r"\s*-?\d+\s*", value):
        number = int(value)
    else:
        raise UsageError("%s must be a whole number of 0 or more (a JSON number such as 25), got %s; any "
                         "other value can leave the call without the cap you intended" % (where, json.dumps(value)[:60]))
    if number < 0:
        raise UsageError("%s must be 0 or more, got %d; a negative value can leave the call without a "
                         "credit cap" % (where, number))
    return number


def check_leads_max_credits(params, endpoint_query):
    """Validate maxCredits for GET /leads, from --params or the endpoint's own query string."""
    sources = []
    if "maxCredits" in params:
        sources.append("params")
    sources.extend("endpoint" for key, _ in endpoint_query if key == "maxCredits")
    if len(sources) > 1:
        raise UsageError("maxCredits is given more than once; the API then ignores it and the search has "
                         "no credit cap. Send it once, in --params.")
    if "maxCredits" in params:
        params["maxCredits"] = checked_max_credits(params["maxCredits"], "maxCredits")
    for index, (key, value) in enumerate(endpoint_query):
        if key == "maxCredits":
            endpoint_query[index] = (key, str(checked_max_credits(value, "maxCredits")))


def checked_leads_limit(value, where):
    """Return a GET /leads limit as a whole number from 1 to 1000, or raise UsageError.

    The API reads 0 or a non-numeric value as the default page of 100 (a negative value as 1, "5abc" as 5),
    and the page limit is the most credits one call can spend, so only a plain whole number in range
    is accepted instead of guessing what the server will do with it.
    """
    if value is None:
        raise UsageError("%s is null; leave it out for the default page of %d, or send a whole number from 1 to "
                         "%d" % (where, LEADS_DEFAULT_LIMIT, LEADS_MAX_LIMIT))
    if isinstance(value, bool):
        raise UsageError("%s must be a whole number from 1 to %d, not a true/false value" % (where, LEADS_MAX_LIMIT))
    if isinstance(value, int):
        number = value
    elif isinstance(value, float) and value.is_integer():
        number = int(value)
    elif isinstance(value, str) and re.fullmatch(r"\s*[+-]?\d+\s*", value):
        number = int(value)
    else:
        raise UsageError("%s must be a whole number from 1 to %d (a JSON number such as 25), got %s; the API "
                         "would read another value as a different page size" % (where, LEADS_MAX_LIMIT,
                                                                                 json.dumps(value)[:60]))
    if number == 0:
        raise UsageError("%s 0 is treated as %d by the API, so this page could spend up to %d credits. Send a "
                         "whole number from 1 to %d, or use GET /leads/preview (free) for counts"
                         % (where, LEADS_DEFAULT_LIMIT, LEADS_DEFAULT_LIMIT, LEADS_MAX_LIMIT))
    if number < 0:
        raise UsageError("%s must be a whole number from 1 to %d, got %d" % (where, LEADS_MAX_LIMIT, number))
    if number > LEADS_MAX_LIMIT:
        raise UsageError("%s must be at most %d (the API cuts larger values to %d), got %d"
                         % (where, LEADS_MAX_LIMIT, LEADS_MAX_LIMIT, number))
    return number


def check_leads_limit(params, endpoint_query):
    """Validate limit for GET /leads, from --params or the endpoint's own query string."""
    count = (1 if "limit" in params else 0) + sum(1 for key, _ in endpoint_query if key == "limit")
    if count > 1:
        raise UsageError("limit is given more than once; the API then reads the first value and the page can "
                         "be larger than intended. Send it once, in --params.")
    if "limit" in params:
        params["limit"] = checked_leads_limit(params["limit"], "limit")
    for index, (key, value) in enumerate(endpoint_query):
        if key == "limit":
            endpoint_query[index] = (key, str(checked_leads_limit(value, "limit")))


def _page_limit(value):
    """The most leads (and so credits) one GET /leads page can return, as the server clamps it.

    check_leads_limit has already refused anything outside 1-1000; below 1 falls back to the
    server default as a second line of defense.
    """
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        return LEADS_DEFAULT_LIMIT
    if number < 1:
        return LEADS_DEFAULT_LIMIT
    return min(number, LEADS_MAX_LIMIT)


def normalize_export_body(body, notes):
    """Fix the input mistakes that would otherwise be silently ignored by POST /leads/export."""
    if "maxCredits" in body and body["maxCredits"] is None:
        checked_max_credits(None, "maxCredits")
    filters = body.get("filters")
    if isinstance(filters, dict):
        for key in EXPORT_TOP_LEVEL_KEYS:
            if key in filters:
                value = filters.pop(key)
                if body.get(key) is None:
                    body[key] = value
                    notes.append("moved filters.%s to the top level of the body (the export ignores it "
                                 "inside filters)" % key)
        ignored = [key for key in EXPORT_IGNORED_FILTER_KEYS if filters.get(key) not in (None, "")]
        if ignored:
            raise UsageError(
                "POST /leads/export ignores filters.%s, so this export would match and charge for more "
                "leads than intended. Remove it: use maxResults to limit the number of leads and keyword or "
                "include-term filters to narrow the match." % ", filters.".join(ignored))
    ids = body.get("selectedIds")
    if isinstance(ids, (str, int)) and not isinstance(ids, bool):
        parts = _as_list(ids) if isinstance(ids, str) else [ids]
        if parts and all(re.fullmatch(r"\d+", str(part).strip()) for part in parts):
            body["selectedIds"] = [int(str(part).strip()) for part in parts]
            notes.append("selectedIds: converted to an array of lead ids (the export ignores any other "
                         "form and would export by filters instead)")
        else:
            raise UsageError("selectedIds must be an array of lead ids, for example [4521, 4522]")
    for key in EXPORT_INT_KEYS:
        value = body.get(key)
        if isinstance(value, str) and re.fullmatch(r"\s*\d+\s*", value):
            body[key] = int(value)
            notes.append("%s: converted the string %r to a number" % (key, value))
    if "maxCredits" in body:
        body["maxCredits"] = checked_max_credits(body["maxCredits"], "maxCredits")
    for key in EXPORT_BOOL_KEYS:
        value = body.get(key)
        if isinstance(value, str) and value.strip().lower() in ("true", "false", "1", "0"):
            body[key] = value.strip().lower() in ("true", "1")
            notes.append("%s: converted the string %r to a boolean" % (key, value))
    if isinstance(filters, dict):
        for key in list(filters):
            filters[key] = _normalize_filter_value(key, filters[key], notes)
    return body


def is_job_route(method, path):
    """Calls the server runs as a background job (202 + jobId when they take longer than about 75 s)."""
    return method == "POST" and bool(EXPORT_RE.fullmatch(path) or TRIGGER_RE.fullmatch(path)
                                      or path in JOB_ROUTE_PATHS)


def job_key_kept(path):
    """How long, at most, the server keeps an Idempotency-Key of this long-running call with its job."""
    return "about 48 hours" if TRIGGER_RE.fullmatch(path) else "about 25 hours"


def job_prefer_header(args, method, path):
    """The Prefer header for a long-running call or a GET /jobs/<jobId>, or None."""
    if is_job_route(method, path):
        if args.respond_async:
            return "respond-async"
        # The server waits up to 75 s by default; ask for less when --timeout would cut that wait.
        wait = int(args.timeout) - 10
        if wait < SERVER_JOB_WAIT_SECONDS:
            return "wait=%d" % max(0, wait)
        return None
    if method == "GET" and JOB_STATUS_RE.fullmatch(path) and not (args.respond_async or args.no_wait):
        return "wait=%d" % max(0, min(JOB_POLL_WAIT_SECONDS, int(args.timeout) - 10))
    return None


# --------------------------------------------------------------------------
# Safety rules
# --------------------------------------------------------------------------

OUTSIDE_DESTINATION = ("lead data (business contact details) leaves SMB Sales Boost for an outside "
                       "destination")


def integration_patch_changes(body):
    """The parts of a PATCH /integrations/{id} body that change where or whether lead data is sent."""
    changes = [key for key in INTEGRATION_DESTINATION_KEYS if key in body]
    status = body.get("status")
    if isinstance(status, str) and status.strip().lower() == "connected":
        changes.append("status \"connected\"")
    if "apiKey" in body:
        changes.append("apiKey, the secret sent to the destination as X-SMB-API-Key")
    return changes


def confirmation_reason(method, path, body, query=None):
    """Why this call needs --confirm, or None when it does not.

    path is already lower case (normalize_endpoint), so mixed-case paths cannot slip past these checks.
    query is a dict of the query parameters that will be sent.
    """
    body = body if isinstance(body, dict) else {}
    query = query if isinstance(query, dict) else {}
    if method == "GET" and path == "/leads" and "maxCredits" not in query:
        most = _page_limit(query.get("limit", LEADS_DEFAULT_LIMIT))
        return ("it has no maxCredits, so it can spend up to %d credits (1 per new lead on the page; the page "
                "limit is %d). Pass maxCredits to cap it (0 returns only "
                "leads you already have, free)" % (most, most))
    if method == "DELETE":
        if INTEGRATION_MAPPING_RE.fullmatch(path):
            return ("it resets the CRM field mapping to the defaults, which changes which lead fields are "
                    "written to the connected CRM on every future delivery")
        if INTEGRATION_ID_RE.fullmatch(path):
            return ("it permanently deletes the integration with its event subscriptions and delivery log; "
                    "lead data stops going to that destination, and a webhook's signing secret cannot be "
                    "recovered (a new integration gets a new one); to stop sending without losing them, pause "
                    "it instead (PATCH /integrations/{id} with {\"status\": \"disabled\"} needs no --confirm)")
        if path.startswith("/filter-presets/"):
            return ("it permanently deletes the preset AND every email schedule that uses it (list them first: "
                    "GET /email-schedules, the ones whose filterPresetId is this preset's id, and name them "
                    "to the user)")
        if path.startswith("/email-schedules/"):
            return ("it permanently deletes the schedule and its list of recipients who unsubscribed; to stop it "
                    "without losing that list, pause it instead (PATCH /email-schedules/{id} with {\"isActive\": false})")
        return "it permanently deletes data"
    if method == "POST":
        if path == "/purchase":
            return "it starts a paid subscription checkout (the card is charged at checkout, or automatically when a free trial ends)"
        if path == "/purchase-credits":
            return ("it charges the card on file immediately, and the new credits restart every email schedule "
                    "that was paused for insufficient credits (they email their recipients again at their next run)")
        if path == "/subscription/change-plan":
            return ("it changes the plan and can charge the card on file immediately; an upgrade, an early "
                    "trial activation or a trial switch to a larger plan also restarts email schedules paused "
                    "for insufficient credits")
        if path == "/subscription/cancel":
            return "it cancels the subscription"
        if path == "/ai/generate-keywords":
            return "it deletes ALL existing keyword lists before generating new ones"
        if TRIGGER_RE.fullmatch(path):
            return "it emails leads to the schedule's recipients right now and spends credits"
        if path == "/email-schedules" and body.get("isActive", True) is not False:
            return ("it creates an ACTIVE schedule that emails real recipients within about 15 minutes "
                    "and spends credits (create it with \"isActive\": false to review it first)")
        if path == "/enrichments":
            if "maxCredits" not in body:
                return ("it spends credits (1 per new database match, 0.1 per live fetch), cannot be undone, "
                        "and has no maxCredits, so it can spend up to your whole credit balance")
            return "it spends credits (1 per new database match, 0.1 per live fetch) and cannot be undone"
        if EXPORT_RE.fullmatch(path) and "maxCredits" not in body:
            return ("it has no maxCredits, so it can spend up to your whole credit balance plus any overage "
                    "budget (1 credit per new lead). Add a top-level maxCredits to cap it (0 exports only "
                    "leads you already have, free)")
        if path == "/integrations/webhook":
            return ("it creates an integration that sends lead data (business contact details) to an outside "
                    "URL automatically on every subscribed event until it is disabled or deleted; the account "
                    "owner is emailed about it, and the response shows the signing secret only once")
        if INTEGRATION_CONNECT_RE.fullmatch(path):
            return ("it starts connecting a CRM: once the user opens the returned link and approves, lead "
                    "data (business contact details) is sent to that CRM automatically on every subscribed "
                    "event, and the account owner is emailed about it (signing in to a CRM account that is "
                    "already connected re-authorizes that integration instead: its events, field mapping and "
                    "delivery history are kept, a paused one stays paused, and a needs_attention one starts "
                    "sending again; the owner is then emailed only in that last case)")
        if INTEGRATION_RETRY_RE.fullmatch(path):
            return "it sends that delivery again right now, so %s" % OUTSIDE_DESTINATION
        if INTEGRATION_MAPPING_TEST_RE.fullmatch(path):
            return ("it creates and then deletes test records in the connected CRM, an outside system "
                    "(a dry run of the field mapping)")
        send = INTEGRATION_SEND_RE.fullmatch(path)
        if send and send.group(1) == "test":
            return ("it sends a test event to the integration's real destination right now, an outside "
                    "system (for a CRM it creates a real test record that is not removed)")
        if send:
            return ("it sends one lead right now, so %s; a leadId you have not received before costs "
                    "1 credit and also goes to your other integrations subscribed to lead.created, and a "
                    "leadId you already received goes to your other integrations subscribed to lead.updated "
                    "when it changed since you last received it (a newer Last Buying Signal)"
                    % OUTSIDE_DESTINATION)
    if method == "PATCH":
        if INTEGRATION_MAPPING_RE.fullmatch(path):
            return ("it changes which lead fields are written to the connected CRM, an outside system, on "
                    "every future delivery")
        if INTEGRATION_ID_RE.fullmatch(path):
            changes = integration_patch_changes(body)
            if changes:
                return ("it changes where, what or whether the integration sends (%s): %s automatically on "
                        "every subscribed event, and the account owner is emailed when the destination "
                        "changes, events are added or the integration is re-enabled"
                        % ("; ".join(changes), OUTSIDE_DESTINATION))
        if path == "/overage-budget" and body.get("enabled") is True:
            return ("it authorizes automatic daily charges to the card on file, and it restarts email schedules "
                    "paused for insufficient credits (their leads can then be billed as overage)")
        if path == "/auto-top-up" and body.get("enabled") is True:
            return "it authorizes automatic future charges to the card on file"
        if SCHEDULE_RE.fullmatch(path) and body.get("isActive") is True:
            return "it activates a schedule that emails real recipients and spends credits"
        if (SCHEDULE_RE.fullmatch(path) and body.get("isActive") is not False
                and any(key in body for key in SCHEDULE_RECIPIENT_KEYS)):
            return ("it changes who the schedule emails; if the schedule is active, the new recipients get "
                    "leads at its next send (add \"isActive\": false to the same call to review it first)")
        if (SCHEDULE_RE.fullmatch(path) and body.get("isActive") is not False
                and any(key in body for key in SCHEDULE_SEARCH_KEYS)):
            return ("it changes which leads the schedule sends and charges for at its next send if it is active "
                    "(add \"isActive\": false to the same call to review it first)")
    return None


def pre_send_notes(method, path, query_keys, body):
    notes = []
    if method == "GET" and path == "/leads":
        if "maxCredits" not in query_keys:
            notes.append("no maxCredits: this search can spend 1 credit per new lead on the page "
                         "(up to limit, default 100). Preview first with GET /leads/preview.")
        if "excludePurchased" in query_keys:
            notes.append("excludePurchased is ignored by GET /leads (it works on /leads/preview and /leads/export)")
    if method == "POST" and path == "/leads/export" and isinstance(body, dict) and "maxCredits" not in body:
        notes.append("no maxCredits: this export can spend up to your whole credit balance "
                     "(plus any overage budget). Set maxCredits to cap it.")
    if method == "POST" and path == "/enrichments" and isinstance(body, dict) and "maxCredits" not in body:
        notes.append("no maxCredits: this enrichment run can spend up to your whole credit balance")
    return notes


ADVICE_AFTER_FAILURE = {
    ("GET", "/leads"): (
        "The server may still have finished and charged credits. Do not repeat it blindly: check "
        "GET /me for the balance. Repeating the same search with maxCredits set to 0 returns any "
        "leads that were already charged, free."),
    ("POST", "/leads/export"): (
        "Do not repeat this export: an export picks new leads first, so a repeat can charge again for "
        "different leads. Check GET /export-history (newest entry) and GET /me. If it was charged, download "
        "the file with GET /export-history/{id}/download, or re-run the same filters with maxCredits 0 and "
        "no excludePurchased (returns only leads you already have, free), or use "
        "POST /lead-export-history/re-export."),
    ("POST", "/enrichments"): (
        "A run may have been created and started spending credits. Check GET /enrichments with limit 5 "
        "before submitting again."),
    ("POST", "/subscription/change-plan"): (
        "The plan change may have gone through and charged the card. Check GET /me before trying again."),
    ("POST", "/purchase-credits"): (
        "The purchase may have gone through. Retry within 24 hours only with the same --idempotency-key "
        "(the same key is not charged twice in that window); later, check permanentCredits in GET /me "
        "before buying again."),
    ("POST", "/purchase"): (
        "A checkout session may have been created. Do not start a second checkout; ask the user whether "
        "the checkout link was opened."),
    ("POST", "/lead-export-history/refresh-and-export"): (
        "The snapshots may already have been refreshed, and lead.updated sent to your integrations for "
        "leads with newer data (a repeat does not send it again for the same data). Retrying is free."),
    ("POST", "/integrations/webhook"): (
        "The integration may have been created. Check GET /integrations before trying again. Repeating "
        "the same provider and targetUrl returns 409 integration_exists; a different provider or a changed "
        "URL (even a trailing slash) creates a second integration that sends the same lead data again, with "
        "its own signing secret. The signing secret cannot be shown again, so if the integration exists but "
        "the user did not get its signingSecret, delete it (DELETE /integrations/{id}) and create it again."),
}


def is_integration_change(method, path):
    """Calls under /integrations that change something or send data (everything except GET)."""
    return method != "GET" and (path == "/integrations" or path.startswith("/integrations/"))


def job_retry_advice(method, path, idempotency_key):
    """For a long-running call that timed out: the same key returns the same job instead of a repeat."""
    if not idempotency_key or not is_job_route(method, path):
        return None
    return ("Safest next step: re-run the exact same command with --idempotency-key %s. The server then returns "
            "the same job (still running, or its result) instead of running it again; it keeps the key for up to "
            "%s after the job finishes, and a server restart forgets it." % (idempotency_key, job_key_kept(path)))


def failure_advice(method, path, idempotency_key=None):
    """What to do after a call failed without a usable answer (a timeout, or a non-JSON gateway error).

    With the Idempotency-Key of a long-running call, re-running with that key comes first.
    """
    specific = _failure_advice(method, path)
    retry = job_retry_advice(method, path, idempotency_key)
    if retry and specific:
        return retry + " Without that key: " + specific
    return retry or specific


def _failure_advice(method, path):
    if method == "POST" and TRIGGER_RE.fullmatch(path):
        return ("The schedule may already have emailed its recipients and charged credits. Check "
                "GET /email-schedules (lastSent and totalSentCount) before triggering it again.")
    send = INTEGRATION_SEND_RE.fullmatch(path) if method == "POST" else None
    if send and send.group(1) == "push-lead":
        return ("The lead may already have been sent to the destination (and 1 credit charged for a new "
                "lead). Check GET /integrations/{id}/deliveries (a push that was sent is recorded there, CRM "
                "pushes included; one refused before sending is not, and one still in progress can take a "
                "minute to appear), for a CRM the record in the "
                "CRM itself, and GET /me before pushing it again. A repeat can create a duplicate record in a "
                "CRM.")
    if (send and send.group(1) == "test") or (method == "POST" and INTEGRATION_RETRY_RE.fullmatch(path)):
        return ("The event may already have been delivered (for a CRM, a test record may exist). Check "
                "GET /integrations/{id}/deliveries before sending it again.")
    if method == "POST" and INTEGRATION_CONNECT_RE.fullmatch(path):
        return ("Nothing is connected until the user opens the link and approves, so asking for a new link "
                "is safe. Check GET /integrations first if the user may already have approved one.")
    if method == "PATCH" and (INTEGRATION_ID_RE.fullmatch(path) or INTEGRATION_MAPPING_RE.fullmatch(path)):
        return ("The change may already have been saved. Check GET /integrations/{id} (or its "
                "field-mapping) before sending it again.")
    if method == "DELETE" and (INTEGRATION_ID_RE.fullmatch(path) or INTEGRATION_MAPPING_RE.fullmatch(path)):
        return ("The delete may already have happened. Check GET /integrations before sending it again.")
    return ADVICE_AFTER_FAILURE.get((method, path))


def integration_no_retry_advice(method, path, status, data):
    """Advice for a 429 or 503 on an integration call, which the script never retries by itself."""
    code = data.get("error") if isinstance(data, dict) else None
    if status == 503 and code == "provider_unavailable":
        return ("This provider is not available on this deployment yet. Do not retry; tell the user and check "
                "GET /integrations/providers.")
    check = "GET /integrations"
    if INTEGRATION_SEND_RE.fullmatch(path) or INTEGRATION_RETRY_RE.fullmatch(path):
        check = "GET /integrations/{id}/deliveries"
    if status == 429:
        return ("Rate limited (%s, shared by the dashboard, the API and MCP). This call was not retried "
                "automatically because it changes or sends through an integration. Wait for Retry-After, then "
                "check %s to confirm an earlier attempt did not already go through before sending it once more."
                % (INTEGRATION_RATE_LIMITS, check))
    specific = failure_advice(method, path)
    general = ("This call was not retried automatically because it changes or sends through an integration. "
               "Check %s first; repeat it after Retry-After only if the change or delivery is not there."
               % check)
    return general if not specific else specific + " " + general


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def _retry_after_seconds(headers):
    value = headers.get("Retry-After") if headers is not None else None
    if value is None:
        return None
    try:
        return max(0, int(float(value)))
    except ValueError:
        return None


def perform(build, timeout, allow_retry):
    """Send a request built by build(); retry only 429 and 503 with a short Retry-After.

    The caller passes allow_retry=False for calls that change or send through an integration: on
    those a 503 may come after part of the work was done, so the error is returned with advice instead.
    """
    attempt = 0
    while True:
        attempt += 1
        request = build()
        try:
            response = _OPENER.open(request, timeout=timeout)
            status = response.status
        except urllib.error.HTTPError as err:
            response = err
            status = err.code
        except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
            reason = getattr(exc, "reason", None) or exc
            raise NetworkError(str(reason))
        if status in (429, 503) and allow_retry and attempt < MAX_ATTEMPTS:
            wait = _retry_after_seconds(response.headers)
            if wait is not None and wait <= MAX_RETRY_WAIT_SECONDS:
                try:
                    response.read()
                    response.close()
                except Exception:
                    pass
                note("HTTP %d, retrying in %d s (attempt %d of %d)" % (status, wait, attempt + 1, MAX_ATTEMPTS))
                time.sleep(max(1, wait))
                continue
        return status, response


def api_request_builder(method, path, query_pairs, api_key, body, extra_headers):
    url = API_ORIGIN + API_PREFIX + path
    if query_pairs:
        url += "?" + urllib.parse.urlencode(query_pairs)
    data = None
    if method in ("POST", "PATCH", "PUT"):
        data = json.dumps(body if body is not None else {}, ensure_ascii=False).encode("utf-8")
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json, */*;q=0.5"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    if data is not None:
        headers["Content-Type"] = "application/json"
    headers.update(extra_headers)

    def build():
        return urllib.request.Request(url, data=data, headers=headers, method=method)

    return url, build


def read_body(response):
    """Read a whole response body; an interrupted read becomes a NetworkError."""
    try:
        return response.read()
    except (http.client.HTTPException, OSError) as exc:
        raise NetworkError(str(exc) or exc.__class__.__name__)


def report_headers(headers):
    for name in HEADERS_TO_REPORT:
        value = headers.get(name) if headers is not None else None
        if value is not None:
            print("%s: %s" % (name, value), file=sys.stderr)
    if headers is None:
        return
    if (headers.get("X-Credits-Capped") or "").lower() == "true":
        note("results were cut to the credits you have available (X-Credits-Capped)")
    if (headers.get("X-Lead-Query-Path") or "").lower() == "trigram":
        note("this query ran on the slow path (up to about 110 s). Keyword, company name, URL, state "
             "and city filters with the default sort keep searches fast.")


# --------------------------------------------------------------------------
# Files
# --------------------------------------------------------------------------

class OutputDir(object):
    def __init__(self, requested):
        self.requested = requested
        self._path = None

    def path(self):
        if self._path is None:
            if self.requested:
                directory = self.requested
            elif os.environ.get(ENV_OUTPUT_DIR):
                directory = os.environ[ENV_OUTPUT_DIR]
            elif os.path.isdir(SANDBOX_OUTPUT_DIR) and os.access(SANDBOX_OUTPUT_DIR, os.W_OK):
                directory = SANDBOX_OUTPUT_DIR
            else:
                directory = os.path.join(os.getcwd(), FALLBACK_OUTPUT_DIR)
            directory = os.path.abspath(os.path.expanduser(directory))
            try:
                os.makedirs(directory, mode=0o700, exist_ok=True)
            except OSError as exc:
                raise LocalFileError("could not create the output folder %s: %s" % (directory, exc))
            self._path = directory
        return self._path


def safe_filename(raw, default_ext):
    """Strip any directory part, keep a conservative character set, force an allowed extension."""
    name = os.path.basename(str(raw or "").replace("\\", "/"))
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name).lstrip(".")
    if not name:
        name = "smb-sales-boost-file"
    root, ext = os.path.splitext(name)
    if ext.lower() not in SAFE_EXTENSIONS:
        root, ext = name, default_ext
    root = root[:120] or "smb-sales-boost-file"
    return root + ext.lower()


def open_new_file(output_dir, name):
    """Create a new file (mode 0600) without overwriting or following an existing path."""
    directory = output_dir.path()
    root, ext = os.path.splitext(name)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
    for index in range(1000):
        candidate = name if index == 0 else "%s-%d%s" % (root, index, ext)
        path = os.path.join(directory, candidate)
        try:
            descriptor = os.open(path, flags, 0o600)
        except FileExistsError:
            continue
        except OSError as exc:
            raise LocalFileError("could not create %s: %s" % (path, exc))
        return path, os.fdopen(descriptor, "wb")
    raise LocalFileError("no free file name for %s in %s" % (name, directory))


def write_bytes(output_dir, name, content):
    path, handle = open_new_file(output_dir, name)
    try:
        with handle:
            handle.write(content)
    except OSError as exc:
        raise LocalFileError("could not write %s: %s" % (path, exc))
    return {"fileName": os.path.basename(path), "path": path, "bytes": len(content)}


def _discard(path):
    try:
        os.remove(path)
    except OSError:
        pass


def stream_to_file(output_dir, response, name):
    path, handle = open_new_file(output_dir, name)
    size = 0
    with handle:
        while True:
            try:
                chunk = response.read(CHUNK_SIZE)
            except (http.client.HTTPException, OSError) as exc:
                handle.close()
                _discard(path)
                raise NetworkError("the download was interrupted (%s); no partial file was kept" % exc)
            if not chunk:
                break
            try:
                handle.write(chunk)
            except OSError as exc:
                handle.close()
                _discard(path)
                raise LocalFileError("could not write %s: %s" % (path, exc))
            size += len(chunk)
    return {"fileName": os.path.basename(path), "path": path, "bytes": size}


def filename_from_disposition(value):
    if not value:
        return None
    match = re.search(r"filename\*\s*=\s*([^']*)'[^']*'([^;]+)", value, re.I)
    if match:
        try:
            return urllib.parse.unquote(match.group(2).strip().strip('"'), encoding=match.group(1) or "utf-8")
        except LookupError:
            pass
    match = re.search(r'filename\s*=\s*"([^"]*)"', value, re.I) or re.search(r"filename\s*=\s*([^;]+)", value, re.I)
    return match.group(1).strip() if match else None


def content_type_of(headers):
    return ((headers.get("Content-Type") if headers is not None else "") or "").split(";")[0].strip().lower()


def decode_inline_file(entry):
    """POST /leads/export returns CSV and JSON as plain text and XLSX as base64."""
    file_type = str(entry.get("fileType") or "").lower()
    data = entry.get("data")
    if file_type == "xlsx":
        try:
            return base64.b64decode(data or "", validate=True)
        except (binascii.Error, TypeError, ValueError) as exc:
            raise LocalFileError("the XLSX file data could not be decoded: %s" % exc)
    if isinstance(data, str):
        return data.encode("utf-8")
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


# --------------------------------------------------------------------------
# Response handling
# --------------------------------------------------------------------------

class Context(object):
    def __init__(self, args, method, path, api_key, output_dir, idempotency_key=None):
        self.args = args
        self.method = method
        self.path = path
        self.api_key = api_key
        self.output_dir = output_dir
        self.idempotency_key = idempotency_key


def download_api_path(ctx, link, name):
    """Stream a file from an API path such as /api/v1/export-history/12/download (sends the key)."""
    path, query = normalize_endpoint(link)
    _, build = api_request_builder("GET", path, query, ctx.api_key, None, {})
    status, response = perform(build, ctx.args.timeout, not ctx.args.no_retry)
    if 200 <= status < 300:
        saved = stream_to_file(ctx.output_dir, response, name)
        saved["source"] = "export history"
        return saved
    raw = read_body(response)
    try:
        detail = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        detail = {"error": "http_%d" % status}
    detail["httpStatus"] = status
    return {"fileName": name, "error": detail}


def download_presigned(ctx, url, name_hint):
    """Fetch a presigned storage link WITHOUT the API key. HTTPS and the storage host only."""
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.scheme != "https" or not PRESIGNED_HOST_RE.fullmatch(host):
        raise UsageError("refusing to download from an unexpected link host (%s)" % (host or "none"))

    def build():
        return urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")

    status, response = perform(build, ctx.args.timeout, not ctx.args.no_retry)
    if not 200 <= status < 300:
        read_body(response)
        return {"error": {"httpStatus": status, "message": "the download link was refused; request a new one"}}
    server_name = filename_from_disposition(response.headers.get("Content-Disposition"))
    ext = EXTENSION_BY_CONTENT_TYPE.get(content_type_of(response.headers), ".csv")
    return stream_to_file(ctx.output_dir, response, safe_filename(server_name or name_hint, ext))


def handle_export(ctx, data, headers):
    payload = data.get("data") if isinstance(data, dict) else None
    files = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(files, list):
        emit(data)
        return 0
    saved = []
    for entry in files:
        if not isinstance(entry, dict):
            continue
        file_type = str(entry.get("fileType") or "").lower()
        name = safe_filename(entry.get("fileName"), EXTENSION_BY_FILE_TYPE.get(file_type, ".csv"))
        try:
            if entry.get("data") is not None:
                result = write_bytes(ctx.output_dir, name, decode_inline_file(entry))
            elif entry.get("downloadUrl"):
                result = download_api_path(ctx, entry["downloadUrl"], name)
            else:
                result = {"fileName": name, "error": "the response had neither file data nor a download link"}
        except (LocalFileError, NetworkError) as exc:
            # The export is already paid for: report it and point at the free re-download.
            result = {"fileName": name, "error": str(exc),
                      "advice": "The export was charged. Download this file again with GET "
                                "/export-history/{exportId}/download (kept 90 days); do not repeat the export."}
        result["fileType"] = file_type or None
        if entry.get("exportId") is not None:
            result["exportId"] = entry.get("exportId")
        saved.append(result)
    summary = {"httpStatus": 200}
    for key in ("leadCount", "exportId", "databaseType", "creditsUsed", "creditsRemaining",
                "maxLeads", "overflowCount", "maxResults", "maxCredits"):
        if payload.get(key) is not None:
            summary[key] = payload.get(key)
    if (headers.get("X-Credits-Capped") or "").lower() == "true":
        summary["creditsCapped"] = True
    summary["savedFiles"] = saved
    emit(summary)
    return 1 if any("error" in item for item in saved) else 0


def handle_download_link(ctx, data, kind, run_id):
    payload = data.get("data") if isinstance(data, dict) else None
    link = payload.get("downloadUrl") if isinstance(payload, dict) else None
    if not link:
        emit(data)
        return 0
    if kind == "export":
        file_type = str(payload.get("fileType") or "").lower()
        name = safe_filename(payload.get("fileName"), EXTENSION_BY_FILE_TYPE.get(file_type, ".csv"))
    else:
        name = "enrichment_%s.csv" % run_id
    if link.startswith("/"):
        result = download_api_path(ctx, link, name)
    else:
        result = download_presigned(ctx, link, name)
    summary = {"httpStatus": 200}
    summary.update({key: value for key, value in payload.items() if key != "downloadUrl"})
    summary["downloadUrl"] = "(a short-lived link was used to download the file; it is not shown)"
    summary["savedFile"] = result
    emit(summary)
    return 1 if "error" in result else 0


def compact_view(data):
    payload = data.get("data") if isinstance(data, dict) else None
    leads = payload.get("leads") if isinstance(payload, dict) else None
    if not isinstance(leads, list):
        return data
    view = {key: value for key, value in payload.items() if key != "leads"}
    view["leads"] = [
        {field: lead.get(field) for field in COMPACT_FIELDS if field in lead}
        for lead in leads if isinstance(lead, dict)
    ]
    view["note"] = "Compact view of key fields only. Use --out to save every field."
    return {"data": view}


def save_json_copy(ctx, data):
    root = os.path.splitext(os.path.basename(str(ctx.args.out)))[0]
    name = safe_filename(root + ".json", ".json")
    try:
        result = write_bytes(ctx.output_dir, name, json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))
    except LocalFileError as exc:
        note("the --out copy was not saved: %s" % exc)
        return
    note("full response saved to %s" % result["path"])


def is_job_accepted(data):
    """A 202 body that names a background job (jobId + statusUrl)."""
    return (isinstance(data, dict) and isinstance(data.get("jobId"), str)
            and bool(JOB_ID_RE.fullmatch(data["jobId"])) and isinstance(data.get("statusUrl"), str))


def is_export_answer(data):
    payload = data.get("data") if isinstance(data, dict) else None
    return isinstance(payload, dict) and isinstance(payload.get("files"), list)


def job_progress_text(view):
    text = str(view.get("phase") or "running")
    progress = view.get("progress")
    if isinstance(progress, dict) and progress.get("done") is not None:
        label = progress.get("label")
        total = progress.get("total")
        text += " (%s%s%s)" % (str(label) + " " if label else "", progress.get("done"),
                               "/%s" % total if total is not None else "")
    elapsed = view.get("elapsedMs")
    if isinstance(elapsed, (int, float)) and not isinstance(elapsed, bool):
        text += ", %d s so far" % int(elapsed / 1000)
    return text


def follow_advice(ctx, job_id):
    text = ("The work keeps running on the server. Get its result later with: python3 smb_api.py GET /jobs/%s "
            "(it waits for the result and saves any file the same way). Do not repeat the original request" % job_id)
    if ctx.idempotency_key and is_job_route(ctx.method, ctx.path):
        text += " without --idempotency-key %s (with that key it returns this same job)" % ctx.idempotency_key
    return text + "."


def job_summary(ctx, view, advice):
    out = {"httpStatus": 202, "status": "running"}
    for key in ("jobId", "kind", "phase", "progress", "elapsedMs", "statusUrl"):
        if view.get(key) is not None:
            out[key] = view.get(key)
    if ctx.idempotency_key and is_job_route(ctx.method, ctx.path):
        out["idempotencyKey"] = ctx.idempotency_key
    out["advice"] = advice
    return out


def _retry_after_hint(view):
    value = view.get("retryAfterSeconds")
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return min(value, 30)
    return 5


def follow_job(ctx, accepted):
    """Follow a 202 answer with GET /jobs/<jobId> until it is final, then handle that answer like the original.

    The job id is checked against JOB_ID_RE and the poll path is built from it: statusUrl and Location are
    never followed as given. The final answer goes to handle_response with the ORIGINAL ctx, so an export
    is saved by handle_export and a file answer by the attachment branch, exactly as without a 202.
    """
    job_id = accepted["jobId"]
    if ctx.args.respond_async or ctx.args.no_wait:
        emit(job_summary(ctx, accepted, follow_advice(ctx, job_id)))
        return 0
    deadline = time.monotonic() + ctx.args.job_timeout
    poll_timeout = max(ctx.args.timeout, JOB_POLL_MIN_TIMEOUT)
    view = accepted
    last_text = None
    failures = 0
    while True:
        text = job_progress_text(view)
        if text != last_text:
            note("job %s is still running: %s" % (job_id, text))
            last_text = text
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            emit(job_summary(ctx, view, "Stopped following it after --job-timeout. " + follow_advice(ctx, job_id)))
            return 0
        wait = int(max(0, min(JOB_POLL_WAIT_SECONDS, remaining)))
        _, build = api_request_builder("GET", "/jobs/" + job_id, [], ctx.api_key, None, {"Prefer": "wait=%d" % wait})
        started = time.monotonic()
        try:
            status, response = perform(build, poll_timeout, not ctx.args.no_retry)
            job_status = response.headers.get("X-SMBSB-Job-Status") if response.headers is not None else None
            # A 429 or 503 without X-SMBSB-Job-Status refused the poll itself (rate limit, a temporary
            # server problem); the job is not affected, so it counts like a dropped connection.
            refused = status in (429, 503) and not job_status
            raw = read_body(response) if status in (202, 404) or refused else None
            if refused:
                raise NetworkError("the poll was refused with HTTP %d" % status)
        except NetworkError as exc:
            failures += 1
            if failures >= JOB_POLL_MAX_NETWORK_FAILURES:
                result = job_summary(ctx, view, follow_advice(ctx, job_id))
                result["error"] = "network_error"
                result["message"] = "Following the job failed: %s." % exc
                emit(result)
                return 3
            note("polling job %s failed (%s); trying again" % (job_id, exc))
            time.sleep(max(1, min(5, remaining)))
            continue
        failures = 0
        if status in (202, 404):
            try:
                data = json.loads(raw.decode("utf-8")) if raw else None
            except (ValueError, UnicodeDecodeError):
                data = None
            if status == 202 and is_job_accepted(data):
                view = data
                if time.monotonic() - started < 1:
                    time.sleep(max(0, min(_retry_after_hint(view), deadline - time.monotonic())))
                continue
            result = {"httpStatus": status, "jobId": job_id}
            if isinstance(data, dict):
                result.update(data)
            if status == 404:
                # The job is gone: a server restart interrupts running jobs and forgets kept results.
                result["advice"] = ("The job is no longer known to the server (it finished more than about a day "
                                    "ago, or a server restart interrupted it). " + (_failure_advice(ctx.method, ctx.path)
                                                 or "Check what it already saved before running it again."))
            else:
                result["error"] = result.get("error") or "unexpected_response"
            emit(result)
            return 1
        return handle_response(ctx, status, response)


def handle_response(ctx, status, response):
    headers = response.headers
    report_headers(headers)
    ok = 200 <= status < 300
    disposition = (headers.get("Content-Disposition") if headers is not None else "") or ""
    ctype = content_type_of(headers)

    if ok and "attachment" in disposition.lower():
        ext = EXTENSION_BY_CONTENT_TYPE.get(ctype, ".csv")
        saved = stream_to_file(ctx.output_dir, response, safe_filename(filename_from_disposition(disposition), ext))
        saved["contentType"] = ctype or None
        emit({"httpStatus": status, "savedFile": saved})
        return 0

    raw = read_body(response)
    try:
        data = json.loads(raw.decode("utf-8")) if raw else None
        is_json = True
    except (ValueError, UnicodeDecodeError):
        data, is_json = None, False

    if is_json and status == 202 and is_job_accepted(data):
        return follow_job(ctx, data)

    if not is_json:
        if ok and ctype in EXTENSION_BY_CONTENT_TYPE:
            saved = write_bytes(ctx.output_dir, safe_filename(None, EXTENSION_BY_CONTENT_TYPE[ctype]), raw)
            emit({"httpStatus": status, "savedFile": saved})
            return 0
        text = re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "replace"))
        result = {
            "httpStatus": status,
            "error": "unexpected_response",
            "message": "The server returned a non-JSON response.",
            "contentType": ctype or None,
            "bodyPreview": re.sub(r"\s+", " ", text).strip()[:300],
        }
        if status in (502, 504, 520, 522, 524):
            result["message"] = ("The request timed out at the network edge (HTTP %d). The server may "
                                 "still be working on it." % status)
        advice = failure_advice(ctx.method, ctx.path, ctx.idempotency_key)
        if is_integration_change(ctx.method, ctx.path) and status in (429, 503):
            result["advice"] = integration_no_retry_advice(ctx.method, ctx.path, status, None)
        elif advice and status >= 500:
            result["advice"] = advice
        emit(result)
        return 1

    if not ok:
        result = {"httpStatus": status}
        if isinstance(data, dict):
            result.update(data)
        elif data is not None:
            result["body"] = data
        if 300 <= status < 400:
            result["error"] = "redirect_not_followed"
            result["message"] = ("The server answered with a redirect. This client never follows "
                                 "redirects, so the API key is not sent anywhere else.")
        advice = failure_advice(ctx.method, ctx.path)
        if is_integration_change(ctx.method, ctx.path) and status in (429, 503):
            result["advice"] = integration_no_retry_advice(ctx.method, ctx.path, status, data)
        elif advice and status >= 500:
            result["advice"] = advice
        emit(result)
        return 1

    if ctx.method == "POST" and EXPORT_RE.fullmatch(ctx.path):
        return handle_export(ctx, data, headers)
    if ctx.method == "GET" and JOB_STATUS_RE.fullmatch(ctx.path) and is_export_answer(data):
        # GET /jobs/<jobId> called directly for an export: save its files like the export itself.
        return handle_export(ctx, data, headers)
    link_match = HISTORY_LINK_RE.fullmatch(ctx.path)
    enrich_match = ENRICHMENT_LINK_RE.fullmatch(ctx.path)
    if ctx.method == "GET" and (link_match or enrich_match) and not ctx.args.no_fetch:
        if link_match:
            return handle_download_link(ctx, data, "export", link_match.group(1))
        return handle_download_link(ctx, data, "enrichment", enrich_match.group(1))
    if ctx.method == "GET" and (link_match or enrich_match):
        note("the downloadUrl works without an API key for a few minutes; do not share or log it")

    payload = data.get("data") if isinstance(data, dict) else None
    if isinstance(payload, dict) and payload.get("requiresKeywords"):
        note("no positive filter was sent, so no leads were returned and no credits were used. Add "
             "positiveKeywords (or nameIncludeTerms, urlIncludeTerms, crawledUrlIncludeTerms or "
             "descriptionIncludeTerms).")
    emit(compact_view(data) if ctx.args.compact else data)
    holds_secret = ctx.method == "POST" and ctx.path == "/integrations/webhook"
    if holds_secret:
        note("the signingSecret above is shown only this once: give it to the user to verify the "
             "X-SMB-Signature header, and do not log it, save it or repeat it elsewhere")
    if ctx.args.out and holds_secret:
        note("--out was ignored: this response holds the one-time signing secret, so it is not saved to a file")
    elif ctx.args.out:
        save_json_copy(ctx, data)
    return 0


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def _timeout_seconds(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number of seconds")
    if not 1 <= value <= 3600:
        raise argparse.ArgumentTypeError("must be between 1 and 3600 seconds")
    return value


def _job_timeout_seconds(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number of seconds")
    if not 1 <= value <= 86400:
        raise argparse.ArgumentTypeError("must be between 1 and 86400 seconds")
    return value


CONFIRM_HELP = """\
--confirm is required (nothing is sent without it) for:
  money:        POST /purchase, POST /purchase-credits, POST /subscription/change-plan,
                PATCH /auto-top-up or /overage-budget with "enabled": true
  credits:      GET /leads and POST /leads/export without maxCredits, POST /enrichments
  email:        POST /email-schedules/{id}/trigger, creating or activating a schedule, changing
                the recipients, preset or maxLeadsPerEmail of a schedule that is not paused
  lead data to an outside destination (integrations):
                POST /integrations/webhook, POST /integrations/{provider}/connect,
                PATCH /integrations/{id} with subscriptions, defaultTargetUrl, pipedriveDeals,
                apiKey or "status": "connected", POST /integrations/{id}/test, /push-lead,
                /deliveries/{deliveryId}/retry and /field-mapping/test,
                PATCH /integrations/{id}/field-mapping
  other:        POST /subscription/cancel, POST /ai/generate-keywords, every DELETE

maxCredits must be a whole number of 0 or more; null, negative, decimal, true/false or text
values are refused before anything is sent. On GET /leads, limit must be a whole number from
1 to 1000, given once.

429 and 503 responses are retried automatically (Retry-After up to 60 s), except on calls that
change or send through an integration (anything but GET under /integrations): those return the
error with advice to check GET /integrations or the delivery log first.

Long-running calls (POST /leads/export, /email-schedules/{id}/trigger, /ai/suggest-categories,
/lead-export-history/refresh, /refresh-and-export and /re-export) send an Idempotency-Key and
follow a 202 answer (GET /jobs/<jobId>) until the result is ready; --async and --no-wait print
the jobId instead. Re-run a call that timed out with the --idempotency-key it printed: the server
returns the same job instead of exporting or sending again.
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="smb_api.py",
        description="SMB Sales Boost API client (skill version %s). See the module docstring for details." % __version__,
        epilog=CONFIRM_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("positionals", nargs="+", metavar="ARG",
                        help="METHOD ENDPOINT (an API key may come first, but prefer the %s env var)" % KEY_ENV_VAR_NAME)
    parser.add_argument("--params", default=None)
    parser.add_argument("--params-file", default=None)
    parser.add_argument("--body", default=None)
    parser.add_argument("--body-file", default=None)
    parser.add_argument("--confirm", action="store_true",
                        help="approve a call that needs it (see the list below); only after the user said yes")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--idempotency-key", default=None)
    parser.add_argument("--async", dest="respond_async", action="store_true",
                        help="long-running calls: answer 202 with a jobId at once and print it")
    parser.add_argument("--no-wait", action="store_true",
                        help="long-running calls: print the jobId of a 202 answer instead of following it")
    parser.add_argument("--job-timeout", type=_job_timeout_seconds, default=DEFAULT_JOB_TIMEOUT,
                        help="seconds to follow a 202 answer before printing the jobId instead (default 3600)")
    parser.add_argument("--timeout", type=_timeout_seconds, default=DEFAULT_TIMEOUT)
    parser.add_argument("--no-retry", action="store_true")
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    return parser.parse_intermixed_args(argv)


def resolve_positionals(positionals):
    if len(positionals) == 3:
        key_arg, method, endpoint = positionals
    elif len(positionals) == 2:
        key_arg = None
        method, endpoint = positionals
    else:
        raise UsageError("expected METHOD ENDPOINT, for example: GET /me")
    method = method.upper()
    if method not in METHODS:
        raise UsageError("unsupported method: the first argument must be one of %s" % ", ".join(METHODS))
    return key_arg, method, endpoint


def run(args):
    key_arg, method, endpoint = resolve_positionals(args.positionals)
    path, endpoint_query = normalize_endpoint(endpoint)
    params = load_json_arg(args.params, args.params_file, "params") or {}
    body = load_json_arg(args.body, args.body_file, "body")
    if body is not None and method in ("GET", "DELETE"):
        raise UsageError("%s requests take --params, not --body" % method)

    notes = []
    if method == "POST" and EXPORT_RE.fullmatch(path) and isinstance(body, dict):
        body = normalize_export_body(body, notes)
    if method == "GET" and path == "/leads":
        check_leads_max_credits(params, endpoint_query)
        check_leads_limit(params, endpoint_query)
    if (method in ("POST", "PATCH") and (path == "/integrations/webhook" or INTEGRATION_ID_RE.fullmatch(path))
            and isinstance(body, dict) and body.get("apiKey") not in (None, "") and args.body is not None):
        notes.append("the body holds apiKey (a shared secret) on the command line, where other local "
                     "processes and shell history can see it; pass such a body with --body-file instead")
    query_pairs = endpoint_query + encode_query(params, notes)
    notes.extend(pre_send_notes(method, path, set(key for key, _ in query_pairs), body))

    is_public = path in PUBLIC_ENDPOINTS
    if key_arg is not None and key_arg.strip().lower() != "none":
        api_key = clean_api_key(key_arg)
        note("the API key was passed on the command line; prefer the %s environment variable" % KEY_ENV_VAR_NAME)
    elif key_arg is not None:
        api_key = None
    else:
        api_key = clean_api_key(os.environ.get(KEY_ENV_VAR_NAME))
    if is_public:
        api_key = None
    if api_key and not api_key.startswith("smbk_"):
        note("API keys normally start with smbk_; check that the right value is set")

    extra_headers = {}
    idempotency_key = None
    job_route = is_job_route(method, path)
    if method == "POST" and (path == "/purchase-credits" or job_route):
        # purchase-credits: Stripe's key; long-running calls: the server returns the same job for the same key.
        body_key = (body or {}).get("idempotencyKey") if path == "/purchase-credits" else None
        if args.idempotency_key and body_key not in (None, args.idempotency_key):
            raise UsageError("the body idempotencyKey and --idempotency-key differ; use only one of them")
        idempotency_key = args.idempotency_key or body_key or ("smbsk-" + secrets.token_hex(12))
        if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", str(idempotency_key)):
            raise UsageError("--idempotency-key must be 8-64 characters of letters, digits, _ or -")
        extra_headers["Idempotency-Key"] = idempotency_key
        if path == "/purchase-credits" and isinstance(body, dict):
            body["idempotencyKey"] = idempotency_key  # the server prefers the body value; keep them identical
    elif args.idempotency_key:
        notes.append("--idempotency-key is used only by POST /purchase-credits and the long-running calls "
                     "(see --help); it was not sent")
    prefer = job_prefer_header(args, method, path)
    if prefer:
        extra_headers["Prefer"] = prefer
    if (args.respond_async or args.no_wait) and not (job_route or JOB_STATUS_RE.fullmatch(path)):
        notes.append("--async and --no-wait only change the long-running calls and GET /jobs/<jobId>")

    reason = confirmation_reason(method, path, body, dict(query_pairs))
    url, build = api_request_builder(method, path, query_pairs, api_key, body, extra_headers)

    for message in notes:
        note(message)

    if args.dry_run:
        emit({
            "dryRun": True,
            "method": method,
            "url": url,
            "sendsApiKey": bool(api_key),
            "body": body,
            "confirmationRequired": reason,
            "idempotencyKey": idempotency_key,
            "prefer": extra_headers.get("Prefer"),
        })
        return 0

    if reason and not args.confirm:
        emit({
            "error": "confirmation_required",
            "message": ("Not sent: %s %s needs explicit approval because %s. Describe the action and its "
                        "cost to the user, and re-run with --confirm only after they approve it."
                        % (method, path, reason)),
        })
        return 2

    if not api_key and not is_public:
        raise UsageError("no API key: set the %s environment variable (keys start with smbk_)" % KEY_ENV_VAR_NAME)

    if idempotency_key and path == "/purchase-credits":
        note("Idempotency-Key: %s (if this call times out, retry within 24 hours with --idempotency-key %s "
             "so it is not charged twice)" % (idempotency_key, idempotency_key))
    elif idempotency_key:
        note("Idempotency-Key: %s (if this call times out, re-run it with --idempotency-key %s: the server "
             "returns the same job instead of running it again; kept for up to %s after the job finishes, and a "
             "server restart forgets it)" % (idempotency_key, idempotency_key, job_key_kept(path)))

    ctx = Context(args, method, path, api_key, OutputDir(args.output_dir), idempotency_key)
    if writes_files(args, method, path):
        ctx.output_dir.path()  # create the folder now, so a folder problem stops us before anything is charged
    try:
        allow_retry = not args.no_retry and not is_integration_change(method, path)
        status, response = perform(build, args.timeout, allow_retry)
    except NetworkError as exc:
        return report_network_failure(method, path, idempotency_key, "The request did not complete: %s." % exc)
    try:
        return handle_response(ctx, status, response)
    except NetworkError as exc:
        return report_network_failure(method, path, idempotency_key, "The response was interrupted: %s." % exc)


def clean_api_key(raw):
    """Strip copy-paste whitespace; refuse anything that is not a plain key (never echo it)."""
    key = (raw or "").strip()
    if key and not re.fullmatch(r"[A-Za-z0-9_-]+", key):
        raise UsageError("the API key contains spaces, line breaks or other unexpected characters; "
                         "copy it again from Dashboard > API (nothing was sent)")
    return key or None


def writes_files(args, method, path):
    if args.out:
        return True
    if method == "POST" and (EXPORT_RE.fullmatch(path) or path in (
            "/lead-export-history/re-export", "/lead-export-history/refresh-and-export")):
        return True
    if method == "GET" and (path.endswith("/download") or JOB_STATUS_RE.fullmatch(path)):
        return True
    return method == "GET" and bool(HISTORY_LINK_RE.fullmatch(path) or ENRICHMENT_LINK_RE.fullmatch(path)) \
        and not args.no_fetch


DEFAULT_FAILURE_ADVICE = (
    "The request may still have reached the server. A GET is safe to repeat. Before repeating anything "
    "else, check the current state with the matching GET (for example GET /email-schedules, "
    "GET /filter-presets, GET /keyword-lists, GET /export-formats or GET /integrations), because repeating "
    "a create can make a duplicate.")


def report_network_failure(method, path, idempotency_key, message):
    result = {"error": "network_error", "message": message,
              "advice": failure_advice(method, path, idempotency_key) or DEFAULT_FAILURE_ADVICE}
    if idempotency_key:
        result["idempotencyKey"] = idempotency_key
    emit(result)
    return 3


def main(argv=None):
    _configure_stdio()
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    try:
        return run(args)
    except UsageError as exc:
        emit({"error": "usage_error", "message": str(exc)})
        return 2
    except LocalFileError as exc:
        emit({"error": "local_file_error", "message": str(exc)})
        return 4
    except NetworkError as exc:
        emit({"error": "network_error", "message": str(exc)})
        return 3
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # never print a traceback: it could include request headers
        emit({"error": "internal_error", "message": "unexpected %s inside smb_api.py; nothing more is "
                                                    "shown to avoid printing secrets" % exc.__class__.__name__})
        return 1


if __name__ == "__main__":
    sys.exit(main())
