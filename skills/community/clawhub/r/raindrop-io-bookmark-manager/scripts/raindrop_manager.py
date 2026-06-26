from __future__ import annotations

import argparse
import csv
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any

try:
    import certifi  # type: ignore
except Exception:
    certifi = None

API_BASE = "https://api.raindrop.io/rest/v1"
OAUTH_AUTHORIZE_URL = "https://raindrop.io/oauth/authorize"
OAUTH_TOKEN_URL = "https://raindrop.io/oauth/access_token"
OPENCLAW_HOME = Path.home() / ".openclaw"
DEFAULT_ENV_FILE = OPENCLAW_HOME / "raindrop.env"
LEGACY_JSON_FILE = OPENCLAW_HOME / "raindrop-credentials.json"


class RaindropError(Exception):
    pass


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def save_env_values(path: Path, values: dict[str, str | None]) -> None:
    existing = load_dotenv(path)
    for key, value in values.items():
        existing[key] = "" if value is None else str(value)
    lines = [f"{key}={existing[key]}" for key in sorted(existing.keys())]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_credentials(*, require_access_token: bool = True) -> dict[str, Any]:
    env_path = Path(os.environ.get("RAINDROP_ENV_FILE", DEFAULT_ENV_FILE))
    file_env = load_dotenv(env_path)

    merged: dict[str, Any] = {
        "client_id": os.environ.get("RAINDROP_CLIENT_ID") or file_env.get("RAINDROP_CLIENT_ID"),
        "client_secret": os.environ.get("RAINDROP_CLIENT_SECRET") or file_env.get("RAINDROP_CLIENT_SECRET"),
        "access_token": os.environ.get("RAINDROP_ACCESS_TOKEN") or file_env.get("RAINDROP_ACCESS_TOKEN"),
        "refresh_token": os.environ.get("RAINDROP_REFRESH_TOKEN") or file_env.get("RAINDROP_REFRESH_TOKEN"),
        "redirect_uri": os.environ.get("RAINDROP_REDIRECT_URI") or file_env.get("RAINDROP_REDIRECT_URI"),
        "env_file": str(env_path),
    }

    if LEGACY_JSON_FILE.exists():
        data = json.loads(LEGACY_JSON_FILE.read_text(encoding="utf-8"))
        merged["client_id"] = merged["client_id"] or data.get("client_id")
        merged["client_secret"] = merged["client_secret"] or data.get("client_secret")
        merged["access_token"] = merged["access_token"] or data.get("access_token")
        merged["refresh_token"] = merged["refresh_token"] or data.get("refresh_token")
        merged["redirect_uri"] = merged["redirect_uri"] or data.get("redirect_uri")

    if not merged["redirect_uri"]:
        merged["redirect_uri"] = "http://127.0.0.1:8765/callback"

    if require_access_token and not merged["access_token"]:
        raise RaindropError(f"No access token found. Set RAINDROP_ACCESS_TOKEN in {env_path}")
    return merged


def ssl_context() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=certifi.where()) if certifi else ssl.create_default_context()


def normalize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: normalize_payload(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [normalize_payload(v) for v in value]
    return value


def request_json(
    method: str,
    endpoint: str,
    token: str,
    payload: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    if query:
        clean_query = {k: v for k, v in query.items() if v is not None and v != ""}
        if clean_query:
            url += "?" + urllib.parse.urlencode(clean_query, doseq=True)

    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "OpenClaw-Raindrop-Bookmark-Manager/0.2",
    }
    if payload is not None:
        data = json.dumps(normalize_payload(payload), ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, context=ssl_context()) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RaindropError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RaindropError(f"Network/SSL error: {e}") from e

    if not body.strip():
        return {"result": True}

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise RaindropError(f"Non-JSON response: {body}") from e


def oauth_token_request(payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(normalize_payload(payload), ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "OpenClaw-Raindrop-Bookmark-Manager/0.2",
    }
    req = urllib.request.Request(OAUTH_TOKEN_URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ssl_context()) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RaindropError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RaindropError(f"Network/SSL error: {e}") from e

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise RaindropError(f"Non-JSON response: {body}") from e


def build_authorize_url(client_id: str, redirect_uri: str) -> str:
    return OAUTH_AUTHORIZE_URL + "?" + urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
    )


def emit(data: Any, as_csv: bool = False) -> None:
    if not as_csv:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = (
            data.get("items")
            or data.get("collections")
            or data.get("user")
            or data.get("item")
            or data.get("result")
            or []
        )
    else:
        rows = []

    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list) or not rows:
        print("")
        return

    flattened = [flatten_dict(row) if isinstance(row, dict) else {"value": row} for row in rows]
    keys = sorted({k for row in flattened for k in row.keys()})
    writer = csv.DictWriter(sys.stdout, fieldnames=keys)
    writer.writeheader()
    for row in flattened:
        writer.writerow({k: row.get(k) for k in keys})


def flatten_dict(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            out.update(flatten_dict(value, full_key))
        elif isinstance(value, list):
            out[full_key] = json.dumps(value, ensure_ascii=False)
        else:
            out[full_key] = value
    return out


def write_output(path: str | None, data: Any) -> None:
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_tags(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    tags = [part.strip() for part in raw.split(",") if part.strip()]
    return tags or None


def parse_bool(raw: str | None) -> bool | None:
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False
    raise RaindropError(f"Invalid boolean value: {raw}")


def build_collection_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": args.title,
        "view": args.view,
        "sort": args.sort,
        "public": parse_bool(args.public),
        "cover": args.cover,
    }
    if args.parent_id is not None:
        payload["parent"] = {"$id": args.parent_id}
    return payload


def build_raindrop_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "link": getattr(args, "link", None),
        "title": getattr(args, "title", None),
        "excerpt": getattr(args, "excerpt", None),
        "note": getattr(args, "note", None),
        "cover": getattr(args, "cover", None),
        "pleaseParse": parse_bool(getattr(args, "please_parse", None)),
        "important": parse_bool(getattr(args, "important", None)),
        "tags": parse_tags(getattr(args, "tags", None)),
    }
    collection_id = getattr(args, "collection_id", None)
    if collection_id is not None:
        payload["collection"] = {"$id": collection_id}
    return payload


def filter_items(
    rows: list[dict[str, Any]],
    *,
    tag: str | None = None,
    domain: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if tag:
            tags = [str(t).lower() for t in (row.get("tags") or [])]
            if tag.lower() not in tags:
                continue
        if domain:
            blob = " ".join([str(row.get("domain") or ""), str(row.get("link") or "")])
            if domain.lower() not in blob.lower():
                continue
        if text:
            blob = " ".join(
                [
                    str(row.get("title") or ""),
                    str(row.get("excerpt") or ""),
                    str(row.get("note") or ""),
                    str(row.get("link") or ""),
                ]
            )
            if text.lower() not in blob.lower():
                continue
        out.append(row)
    return out


def cmd_whoami(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("GET", "user", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_auth_start(args: argparse.Namespace) -> int:
    creds = load_credentials(require_access_token=False)
    client_id = args.client_id or creds.get("client_id")
    redirect_uri = args.redirect_uri or creds.get("redirect_uri")
    if not client_id:
        raise RaindropError("No client id found. Set RAINDROP_CLIENT_ID or pass --client-id")
    if not redirect_uri:
        raise RaindropError("No redirect URI found. Set RAINDROP_REDIRECT_URI or pass --redirect-uri")

    url = build_authorize_url(str(client_id), str(redirect_uri))
    if not args.no_browser:
        webbrowser.open(url)
    emit({"authorize_url": url, "opened_browser": not args.no_browser})
    return 0


def cmd_auth_finish(args: argparse.Namespace) -> int:
    creds = load_credentials(require_access_token=False)
    client_id = args.client_id or creds.get("client_id")
    client_secret = args.client_secret or creds.get("client_secret")
    redirect_uri = args.redirect_uri or creds.get("redirect_uri")
    if not client_id:
        raise RaindropError("No client id found. Set RAINDROP_CLIENT_ID or pass --client-id")
    if not client_secret:
        raise RaindropError("No client secret found. Set RAINDROP_CLIENT_SECRET or pass --client-secret")
    if not redirect_uri:
        raise RaindropError("No redirect URI found. Set RAINDROP_REDIRECT_URI or pass --redirect-uri")

    data = oauth_token_request(
        {
            "grant_type": "authorization_code",
            "code": args.code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
    )

    if not args.no_save:
        save_env_values(
            Path(creds["env_file"]),
            {
                "RAINDROP_CLIENT_ID": str(client_id),
                "RAINDROP_CLIENT_SECRET": str(client_secret),
                "RAINDROP_ACCESS_TOKEN": data.get("access_token"),
                "RAINDROP_REFRESH_TOKEN": data.get("refresh_token"),
                "RAINDROP_REDIRECT_URI": str(redirect_uri),
            },
        )
    emit(data, args.csv)
    return 0


def cmd_refresh_token(args: argparse.Namespace) -> int:
    creds = load_credentials(require_access_token=False)
    client_id = args.client_id or creds.get("client_id")
    client_secret = args.client_secret or creds.get("client_secret")
    refresh_token = args.refresh_token or creds.get("refresh_token")
    if not client_id:
        raise RaindropError("No client id found. Set RAINDROP_CLIENT_ID or pass --client-id")
    if not client_secret:
        raise RaindropError("No client secret found. Set RAINDROP_CLIENT_SECRET or pass --client-secret")
    if not refresh_token:
        raise RaindropError("No refresh token found. Set RAINDROP_REFRESH_TOKEN or pass --refresh-token")

    data = oauth_token_request(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )

    if not args.no_save:
        save_env_values(
            Path(creds["env_file"]),
            {
                "RAINDROP_CLIENT_ID": str(client_id),
                "RAINDROP_CLIENT_SECRET": str(client_secret),
                "RAINDROP_ACCESS_TOKEN": data.get("access_token"),
                "RAINDROP_REFRESH_TOKEN": data.get("refresh_token") or str(refresh_token),
                "RAINDROP_REDIRECT_URI": str(creds.get("redirect_uri") or "http://127.0.0.1:8765/callback"),
            },
        )
    emit(data, args.csv)
    return 0


def cmd_collections(args: argparse.Namespace) -> int:
    creds = load_credentials()
    endpoint = "collections/childrens" if args.children else "collections"
    data = request_json("GET", endpoint, creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_collection_get(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("GET", f"collection/{args.collection_id}", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_collection_create(args: argparse.Namespace) -> int:
    creds = load_credentials()
    payload = build_collection_payload(args)
    data = request_json("POST", "collection", creds["access_token"], payload=payload)
    emit(data, args.csv)
    return 0


def cmd_collection_update(args: argparse.Namespace) -> int:
    creds = load_credentials()
    payload = build_collection_payload(args)
    if args.expanded is not None:
        payload["expanded"] = parse_bool(args.expanded)
    data = request_json("PUT", f"collection/{args.collection_id}", creds["access_token"], payload=payload)
    emit(data, args.csv)
    return 0


def cmd_collection_delete(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("DELETE", f"collection/{args.collection_id}", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_bookmarks(args: argparse.Namespace) -> int:
    creds = load_credentials()
    query = {
        "page": args.page,
        "perpage": args.perpage,
        "search": args.search,
        "sort": args.sort,
    }
    data = request_json("GET", f"raindrops/{args.collection_id}", creds["access_token"], query=query)
    rows = data.get("items") or []
    rows = filter_items(rows, tag=args.tag, domain=args.domain, text=args.contains)
    out = {
        "result": data.get("result"),
        "items": rows,
        "count": data.get("count"),
        "collectionId": args.collection_id,
    }
    write_output(args.output, out)
    emit(out, args.csv)
    return 0


def cmd_bookmark_get(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("GET", f"raindrop/{args.raindrop_id}", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_add_bookmark(args: argparse.Namespace) -> int:
    creds = load_credentials()
    payload = build_raindrop_payload(args)
    data = request_json("POST", "raindrop", creds["access_token"], payload=payload)
    emit(data, args.csv)
    return 0


def cmd_update_bookmark(args: argparse.Namespace) -> int:
    creds = load_credentials()
    payload = build_raindrop_payload(args)
    data = request_json("PUT", f"raindrop/{args.raindrop_id}", creds["access_token"], payload=payload)
    emit(data, args.csv)
    return 0


def cmd_delete_bookmark(args: argparse.Namespace) -> int:
    creds = load_credentials()
    data = request_json("DELETE", f"raindrop/{args.raindrop_id}", creds["access_token"])
    emit(data, args.csv)
    return 0


def cmd_export_bookmarks(args: argparse.Namespace) -> int:
    creds = load_credentials()
    query = {
        "page": args.page,
        "perpage": args.perpage,
        "search": args.search,
        "sort": args.sort,
    }
    data = request_json("GET", f"raindrops/{args.collection_id}", creds["access_token"], query=query)
    rows = data.get("items") or []
    rows = filter_items(rows, tag=args.tag, domain=args.domain, text=args.contains)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif args.format == "txt":
        links = [str(row.get("link") or "") for row in rows if row.get("link")]
        out_path.write_text(("\n".join(links) + "\n") if links else "", encoding="utf-8")
    else:
        flat = [flatten_dict(row) for row in rows]
        keys = sorted({k for row in flat for k in row.keys()})
        with out_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=keys)
            writer.writeheader()
            for row in flat:
                writer.writerow({k: row.get(k) for k in keys})
    emit({"result": True, "output": str(out_path), "count": len(rows)})
    return 0


def cmd_import_bookmarks(args: argparse.Namespace) -> int:
    creds = load_credentials()
    source = Path(args.input)
    if not source.exists():
        raise RaindropError(f"Input file not found: {source}")

    items: list[dict[str, Any]] = []
    if source.suffix.lower() == ".json":
        data = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise RaindropError("JSON import file must contain a list of bookmark objects")
        for row in data:
            if not isinstance(row, dict) or not row.get("link"):
                continue
            payload = {
                "link": row.get("link"),
                "title": row.get("title"),
                "excerpt": row.get("excerpt"),
                "note": row.get("note"),
                "tags": row.get("tags"),
                "collection": {"$id": args.collection_id},
            }
            items.append(normalize_payload(payload))
    else:
        for line in source.read_text(encoding="utf-8").splitlines():
            link = line.strip()
            if not link:
                continue
            items.append({"link": link, "collection": {"$id": args.collection_id}})

    results = []
    for payload in items:
        try:
            data = request_json("POST", "raindrop", creds["access_token"], payload=payload)
            item = data.get("item") or {}
            results.append({"link": payload.get("link"), "id": item.get("_id"), "title": item.get("title")})
        except Exception as e:
            results.append({"link": payload.get("link"), "error": str(e)})

    out = {"result": True, "items": results}
    write_output(args.output, out)
    emit(out, args.csv)
    return 0


def cmd_env_template(args: argparse.Namespace) -> int:
    template_data = {
        "variables": [
            {"name": "RAINDROP_CLIENT_ID", "description": "Raindrop app client id"},
            {"name": "RAINDROP_CLIENT_SECRET", "description": "Raindrop app client secret"},
            {"name": "RAINDROP_ACCESS_TOKEN", "description": "Raindrop test token or OAuth access token"},
            {"name": "RAINDROP_REFRESH_TOKEN", "description": "Optional OAuth refresh token"},
            {"name": "RAINDROP_REDIRECT_URI", "description": "Local callback URL", "example": "http://127.0.0.1:8765/callback"},
        ]
    }
    rendered = json.dumps(template_data, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        print(str(out))
    else:
        print(rendered, end="")
    return 0


def add_common_output_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--csv", action="store_true", help="Emit flattened CSV-like output to stdout")


def add_collection_fields(parser: argparse.ArgumentParser, *, require_title: bool = False) -> None:
    parser.add_argument("--title", required=require_title)
    parser.add_argument("--view", choices=["list", "simple", "grid", "masonry"])
    parser.add_argument("--sort", type=int)
    parser.add_argument("--public", help="true/false")
    parser.add_argument("--parent-id", type=int)
    parser.add_argument("--cover")


def add_raindrop_fields(parser: argparse.ArgumentParser, *, require_link: bool = False, require_collection: bool = False) -> None:
    parser.add_argument("--link", required=require_link)
    parser.add_argument("--title")
    parser.add_argument("--excerpt")
    parser.add_argument("--note")
    parser.add_argument("--tags", help="Comma-separated tag list")
    parser.add_argument("--cover")
    parser.add_argument("--please-parse", help="true/false")
    parser.add_argument("--important", help="true/false")
    parser.add_argument("--collection-id", type=int, required=require_collection)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Raindrop.io bookmark and collection manager")
    sub = parser.add_subparsers(dest="command", required=True)

    whoami = sub.add_parser("whoami", help="Verify auth and inspect the authenticated user")
    add_common_output_flags(whoami)
    whoami.set_defaults(func=cmd_whoami)

    auth_start = sub.add_parser("auth-start", help="Generate the OAuth authorize URL and optionally open it in a browser")
    auth_start.add_argument("--client-id")
    auth_start.add_argument("--redirect-uri")
    auth_start.add_argument("--no-browser", action="store_true")
    add_common_output_flags(auth_start)
    auth_start.set_defaults(func=cmd_auth_start)

    auth_finish = sub.add_parser("auth-finish", help="Exchange an OAuth code for access and refresh tokens")
    auth_finish.add_argument("--code", required=True)
    auth_finish.add_argument("--client-id")
    auth_finish.add_argument("--client-secret")
    auth_finish.add_argument("--redirect-uri")
    auth_finish.add_argument("--no-save", action="store_true")
    add_common_output_flags(auth_finish)
    auth_finish.set_defaults(func=cmd_auth_finish)

    refresh_token = sub.add_parser("refresh-token", help="Refresh the OAuth access token and save it back to the env file")
    refresh_token.add_argument("--client-id")
    refresh_token.add_argument("--client-secret")
    refresh_token.add_argument("--refresh-token")
    refresh_token.add_argument("--no-save", action="store_true")
    add_common_output_flags(refresh_token)
    refresh_token.set_defaults(func=cmd_refresh_token)

    collections = sub.add_parser("collections", help="List root collections or nested collections")
    collections.add_argument("--children", action="store_true", help="List nested collections instead of root collections")
    add_common_output_flags(collections)
    collections.set_defaults(func=cmd_collections)

    collection_get = sub.add_parser("collection-get", help="Fetch one collection by id")
    collection_get.add_argument("collection_id", type=int)
    add_common_output_flags(collection_get)
    collection_get.set_defaults(func=cmd_collection_get)

    collection_create = sub.add_parser("create-collection", help="Create a new collection")
    add_collection_fields(collection_create, require_title=True)
    add_common_output_flags(collection_create)
    collection_create.set_defaults(func=cmd_collection_create)

    collection_update = sub.add_parser("update-collection", help="Update an existing collection")
    collection_update.add_argument("collection_id", type=int)
    add_collection_fields(collection_update)
    collection_update.add_argument("--expanded", help="true/false")
    add_common_output_flags(collection_update)
    collection_update.set_defaults(func=cmd_collection_update)

    collection_delete = sub.add_parser("delete-collection", help="Delete a collection")
    collection_delete.add_argument("collection_id", type=int)
    add_common_output_flags(collection_delete)
    collection_delete.set_defaults(func=cmd_collection_delete)

    bookmarks = sub.add_parser("bookmarks", help="List bookmarks in a collection")
    bookmarks.add_argument("collection_id", type=int, help="Collection id; use -1 for Unsorted or -99 for Trash")
    bookmarks.add_argument("--page", type=int, default=0)
    bookmarks.add_argument("--perpage", type=int, default=25)
    bookmarks.add_argument("--search")
    bookmarks.add_argument("--sort")
    bookmarks.add_argument("--tag")
    bookmarks.add_argument("--domain")
    bookmarks.add_argument("--contains")
    bookmarks.add_argument("--output")
    add_common_output_flags(bookmarks)
    bookmarks.set_defaults(func=cmd_bookmarks)

    bookmark_get = sub.add_parser("bookmark-get", help="Fetch one bookmark by id")
    bookmark_get.add_argument("raindrop_id", type=int)
    add_common_output_flags(bookmark_get)
    bookmark_get.set_defaults(func=cmd_bookmark_get)

    add_bookmark = sub.add_parser("add-bookmark", help="Save a bookmark into a collection")
    add_raindrop_fields(add_bookmark, require_link=True, require_collection=True)
    add_common_output_flags(add_bookmark)
    add_bookmark.set_defaults(func=cmd_add_bookmark)

    update_bookmark = sub.add_parser("update-bookmark", help="Update one bookmark")
    update_bookmark.add_argument("raindrop_id", type=int)
    add_raindrop_fields(update_bookmark)
    add_common_output_flags(update_bookmark)
    update_bookmark.set_defaults(func=cmd_update_bookmark)

    delete_bookmark = sub.add_parser("delete-bookmark", help="Delete one bookmark")
    delete_bookmark.add_argument("raindrop_id", type=int)
    add_common_output_flags(delete_bookmark)
    delete_bookmark.set_defaults(func=cmd_delete_bookmark)

    export_bookmarks = sub.add_parser("export-bookmarks", help="Export filtered bookmarks from a collection")
    export_bookmarks.add_argument("collection_id", type=int)
    export_bookmarks.add_argument("--page", type=int, default=0)
    export_bookmarks.add_argument("--perpage", type=int, default=100)
    export_bookmarks.add_argument("--search")
    export_bookmarks.add_argument("--sort")
    export_bookmarks.add_argument("--tag")
    export_bookmarks.add_argument("--domain")
    export_bookmarks.add_argument("--contains")
    export_bookmarks.add_argument("--format", choices=["json", "txt", "csv"], default="json")
    export_bookmarks.add_argument("--output", required=True)
    add_common_output_flags(export_bookmarks)
    export_bookmarks.set_defaults(func=cmd_export_bookmarks)

    import_bookmarks = sub.add_parser("import-bookmarks", help="Import bookmarks from txt or json into a collection")
    import_bookmarks.add_argument("--input", required=True)
    import_bookmarks.add_argument("--collection-id", type=int, required=True)
    import_bookmarks.add_argument("--output")
    add_common_output_flags(import_bookmarks)
    import_bookmarks.set_defaults(func=cmd_import_bookmarks)

    env_template = sub.add_parser("env-template", help="Print or write a local env template")
    env_template.add_argument("--output")
    env_template.set_defaults(func=cmd_env_template)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except RaindropError as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
