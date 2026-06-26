#!/usr/bin/env python3
"""Shopify Admin GraphQL CLI tool.

A single-file CLI that calls the Shopify Admin GraphQL API directly via
urllib.request.  Zero external dependencies — only Python 3.10+ stdlib.

Environment variables required:
    SHOPIFY_STORE_URL      – e.g. https://my-store.myshopify.com
    SHOPIFY_ACCESS_TOKEN   – Admin API access token (shpat_…)
    SHOPIFY_API_VERSION    – optional, defaults to 2025-01
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import textwrap
import urllib.error
import urllib.request
import uuid

import shopify_admin_graphql as gql

# ── Configuration ───────────────────────────────────────────────────────────

STORE_URL = os.environ.get("SHOPIFY_STORE_URL", "").rstrip("/")
TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")
API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2025-01")


def emit(payload: dict, *, to_stderr: bool = False, exit_code: int = 0) -> None:
    stream = sys.stderr if to_stderr else sys.stdout
    print(json.dumps(payload, indent=2, ensure_ascii=False), file=stream)
    if exit_code:
        raise SystemExit(exit_code)


def die(message: str, *, exit_code: int = 1, details: dict | None = None) -> None:
    emit(
        {"ok": False, "error": {"message": message, "details": details or {}}},
        to_stderr=True,
        exit_code=exit_code,
    )


def _endpoint() -> str:
    if not STORE_URL or not TOKEN:
        die(
            "SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN must be set.",
            details={"SHOPIFY_STORE_URL": bool(STORE_URL), "SHOPIFY_ACCESS_TOKEN": bool(TOKEN)},
        )
    return f"{STORE_URL}/admin/api/{API_VERSION}/graphql.json"


# ── GraphQL helpers ─────────────────────────────────────────────────────────


def graphql(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL request and return the parsed JSON response."""
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        _endpoint(),
        data=body,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
    )
    last_exc: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode(errors="replace")
            die(
                "HTTP error from Shopify Admin API.",
                details={"status": exc.code, "body": err_body},
            )
        except urllib.error.URLError as exc:
            last_exc = exc
    die("Network error.", details={"error": str(last_exc)})


def ensure_ok(result: dict, mutation_key: str | None = None) -> dict:
    if "errors" in result:
        die("GraphQL errors.", details={"errors": result["errors"]})
    if mutation_key:
        payload = result.get("data", {}).get(mutation_key, {})
        user_errors = payload.get("userErrors", [])
        if user_errors:
            die("User errors.", details={"userErrors": user_errors})
    return result


def to_gid(resource_type: str, id_or_gid: str) -> str:
    """Normalise a numeric ID or full GID into gid://shopify/… form."""
    if str(id_or_gid).startswith("gid://"):
        return id_or_gid
    return f"gid://shopify/{resource_type}/{id_or_gid}"


def _multipart_form_data(
    fields: list[tuple[str, str]],
    file_field: tuple[str, str, bytes, str],
) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    boundary_bytes = boundary.encode()

    body = bytearray()
    for name, value in fields:
        body.extend(b"--" + boundary_bytes + b"\r\n")
        body.extend(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        )
        body.extend(value.encode())
        body.extend(b"\r\n")

    name, filename, content, content_type = file_field
    body.extend(b"--" + boundary_bytes + b"\r\n")
    body.extend(
        f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
    )
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
    body.extend(content)
    body.extend(b"\r\n")
    body.extend(b"--" + boundary_bytes + b"--\r\n")

    return bytes(body), f"multipart/form-data; boundary={boundary}"


def _upload_to_staged_target(
    target: dict,
    file_name: str,
    file_bytes: bytes,
    mime_type: str,
) -> None:
    fields = [(p["name"], p["value"]) for p in target.get("parameters", [])]
    body, content_type = _multipart_form_data(
        fields=fields,
        file_field=("file", file_name, file_bytes, mime_type),
    )
    req = urllib.request.Request(
        target["url"],
        data=body,
        headers={"Content-Type": content_type, "Content-Length": str(len(body))},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        if not (200 <= resp.status < 300):
            raise RuntimeError(f"Upload failed with HTTP {resp.status}")


def _staged_upload(file_path: str, resource: str) -> str:
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    result = ensure_ok(
        graphql(
            gql.STAGED_UPLOADS_CREATE,
            {
                "input": [
                    {
                        "resource": resource,
                        "filename": file_name,
                        "mimeType": mime_type,
                        "fileSize": str(file_size),
                        "httpMethod": "POST",
                    }
                ]
            },
        ),
    )
    payload = result.get("data", {}).get("stagedUploadsCreate", {})
    user_errors = payload.get("userErrors", [])
    if user_errors:
        die("User errors.", details={"userErrors": user_errors})
    targets = payload.get("stagedTargets", [])
    if not targets:
        die("stagedUploadsCreate returned no targets.")

    target = targets[0]
    _upload_to_staged_target(target, file_name, file_bytes, mime_type)

    resource_url = target.get("resourceUrl")
    if not resource_url:
        die("staged upload target missing resourceUrl.")
    return resource_url


def _staged_upload_image(file_path: str) -> str:
    try:
        return _staged_upload(file_path, "IMAGE")
    except Exception as exc:
        die("Upload error.", details={"error": str(exc)})


def _build_media_inputs(
    image_urls: list[str],
    image_files: list[str],
    alt: str | None,
) -> list[dict]:
    media: list[dict] = []
    for url in image_urls:
        item = {"mediaContentType": "IMAGE", "originalSource": url}
        if alt:
            item["alt"] = alt
        media.append(item)
    for path in image_files:
        resource_url = _staged_upload_image(path)
        item = {"mediaContentType": "IMAGE", "originalSource": resource_url}
        if alt:
            item["alt"] = alt
        media.append(item)
    return media


# ── Product commands ────────────────────────────────────────────────────────


def product_list(args: argparse.Namespace) -> None:
    query_filter = args.filter or None
    result = ensure_ok(
        graphql(
        gql.PRODUCT_LIST,
        {"first": args.limit, "query": query_filter},
        ),
    )
    nodes = result["data"]["products"]["nodes"]
    emit({"ok": True, "data": nodes})


def product_get(args: argparse.Namespace) -> None:
    gid = to_gid("Product", args.id)
    result = ensure_ok(
        graphql(
        gql.PRODUCT_GET,
        {"id": gid},
        ),
    )
    emit({"ok": True, "data": result["data"]["product"]})


def product_create(args: argparse.Namespace) -> None:
    product_input: dict = {
        "title": args.title,
        "status": args.status,
    }
    if args.description:
        product_input["descriptionHtml"] = args.description
    if args.vendor:
        product_input["vendor"] = args.vendor
    if args.tags:
        product_input["tags"] = args.tags

    media = _build_media_inputs(args.image_url, args.image_file, args.image_alt)

    result = ensure_ok(
        graphql(
        gql.PRODUCT_CREATE,
        {"input": product_input, "media": media or None},
        ),
        "productCreate",
    )
    emit({"ok": True, "data": result["data"]["productCreate"]["product"]})


def product_update(args: argparse.Namespace) -> None:
    gid = to_gid("Product", args.id)
    product_input: dict = {"id": gid}
    if args.title is not None:
        product_input["title"] = args.title
    if args.description is not None:
        product_input["descriptionHtml"] = args.description
    if args.vendor is not None:
        product_input["vendor"] = args.vendor
    if args.tags is not None:
        product_input["tags"] = args.tags
    if args.status is not None:
        product_input["status"] = args.status

    media = _build_media_inputs(args.image_url, args.image_file, args.image_alt)

    result = ensure_ok(
        graphql(
        gql.PRODUCT_UPDATE,
        {"input": product_input, "media": media or None},
        ),
        "productUpdate",
    )
    emit({"ok": True, "data": result["data"]["productUpdate"]["product"]})


def product_delete(args: argparse.Namespace) -> None:
    gid = to_gid("Product", args.id)
    result = ensure_ok(
        graphql(
        gql.PRODUCT_DELETE,
        {"input": {"id": gid}},
        ),
        "productDelete",
    )
    emit({"ok": True, "data": {"deletedProductId": result["data"]["productDelete"]["deletedProductId"]}})


# ── Metafield commands ──────────────────────────────────────────────────────


def metafield_list(args: argparse.Namespace) -> None:
    owner_type = args.owner_type.upper()
    result = ensure_ok(
        graphql(
        gql.METAFIELD_DEFINITION_LIST,
        {"ownerType": owner_type, "first": args.limit},
        ),
    )
    nodes = result["data"]["metafieldDefinitions"]["nodes"]
    emit({"ok": True, "data": nodes})


def metafield_define(args: argparse.Namespace) -> None:
    definition: dict = {
        "ownerType": args.owner_type.upper(),
        "key": args.key,
        "name": args.name or args.key,
        "type": args.type,
    }
    if args.namespace:
        definition["namespace"] = args.namespace
    if args.pin:
        definition["pin"] = True

    result = ensure_ok(
        graphql(
        gql.METAFIELD_DEFINITION_CREATE,
        {"definition": definition},
        ),
        "metafieldDefinitionCreate",
    )
    emit({"ok": True, "data": result["data"]["metafieldDefinitionCreate"]["createdDefinition"]})


def metafield_set(args: argparse.Namespace) -> None:
    entry: dict = {
        "ownerId": to_gid(args.owner_type, args.owner_id),
        "key": args.key,
        "value": args.value,
    }
    if args.namespace:
        entry["namespace"] = args.namespace
    if args.type:
        entry["type"] = args.type

    result = ensure_ok(
        graphql(
        gql.METAFIELDS_SET,
        {"metafields": [entry]},
        ),
        "metafieldsSet",
    )
    emit({"ok": True, "data": result["data"]["metafieldsSet"]["metafields"]})


# ── Metaobject commands ─────────────────────────────────────────────────────


def metaobject_define(args: argparse.Namespace) -> None:
    field_defs = []
    for spec in args.fields:
        # Format: key:type[:name[:required]]
        parts = spec.split(":")
        fd: dict = {"key": parts[0], "type": parts[1]}
        if len(parts) > 2 and parts[2]:
            fd["name"] = parts[2]
        if len(parts) > 3 and parts[3].lower() in ("required", "true", "1"):
            fd["required"] = True
        field_defs.append(fd)

    definition: dict = {
        "type": args.type,
        "name": args.name or args.type,
        "fieldDefinitions": field_defs,
    }
    if args.display_key:
        definition["displayNameKey"] = args.display_key

    result = ensure_ok(
        graphql(
        gql.METAOBJECT_DEFINITION_CREATE,
        {"definition": definition},
        ),
        "metaobjectDefinitionCreate",
    )
    emit({"ok": True, "data": result["data"]["metaobjectDefinitionCreate"]["metaobjectDefinition"]})


def metaobject_create(args: argparse.Namespace) -> None:
    fields = []
    for spec in args.fields:
        key, value = spec.split("=", 1)
        fields.append({"key": key, "value": value})

    result = ensure_ok(
        graphql(
        gql.METAOBJECT_UPSERT,
        {
            "handle": {"type": args.type, "handle": args.handle},
            "metaobject": {"fields": fields},
        },
        ),
        "metaobjectUpsert",
    )
    emit({"ok": True, "data": result["data"]["metaobjectUpsert"]["metaobject"]})


def metaobject_list(args: argparse.Namespace) -> None:
    result = ensure_ok(
        graphql(
        gql.METAOBJECT_LIST,
        {"type": args.type, "first": args.limit},
        ),
    )
    nodes = result["data"]["metaobjects"]["nodes"]
    emit({"ok": True, "data": nodes})


def metaobject_update(args: argparse.Namespace) -> None:
    gid = to_gid("Metaobject", args.id)
    fields = []
    for spec in args.fields:
        key, value = spec.split("=", 1)
        fields.append({"key": key, "value": value})

    result = ensure_ok(
        graphql(
        gql.METAOBJECT_UPDATE,
        {"id": gid, "metaobject": {"fields": fields}},
        ),
        "metaobjectUpdate",
    )
    emit({"ok": True, "data": result["data"]["metaobjectUpdate"]["metaobject"]})


def metaobject_delete(args: argparse.Namespace) -> None:
    gid = to_gid("Metaobject", args.id)
    result = ensure_ok(
        graphql(
        gql.METAOBJECT_DELETE,
        {"id": gid},
        ),
        "metaobjectDelete",
    )
    emit({"ok": True, "data": {"deletedId": result["data"]["metaobjectDelete"]["deletedId"]}})


# ── Blog commands ───────────────────────────────────────────────────────────


def blog_list(args: argparse.Namespace) -> None:
    result = ensure_ok(
        graphql(
        gql.BLOG_LIST,
        {"first": args.limit},
        ),
    )
    nodes = result["data"]["blogs"]["nodes"]
    emit({"ok": True, "data": nodes})


def blog_create(args: argparse.Namespace) -> None:
    result = ensure_ok(
        graphql(
        gql.BLOG_CREATE,
        {"blog": {"title": args.title}},
        ),
        "blogCreate",
    )
    emit({"ok": True, "data": result["data"]["blogCreate"]["blog"]})


# ── Article commands ────────────────────────────────────────────────────────


def article_list(args: argparse.Namespace) -> None:
    query_str = None
    if args.blog:
        blog_id = str(args.blog)
        if blog_id.startswith("gid://"):
            blog_id = blog_id.rsplit("/", 1)[-1]
        query_str = f"blog_id:{blog_id}"

    result = ensure_ok(
        graphql(
        gql.ARTICLE_LIST,
        {"first": args.limit, "query": query_str},
        ),
    )
    nodes = result["data"]["articles"]["nodes"]
    emit({"ok": True, "data": nodes})


def article_create(args: argparse.Namespace) -> None:
    article_input: dict = {
        "blogId": to_gid("Blog", args.blog),
        "title": args.title,
        "body": args.body,
        "author": {"name": args.author},
        "isPublished": args.publish,
    }
    if args.tags:
        article_input["tags"] = args.tags

    result = ensure_ok(
        graphql(
        gql.ARTICLE_CREATE,
        {"article": article_input},
        ),
        "articleCreate",
    )
    emit({"ok": True, "data": result["data"]["articleCreate"]["article"]})


def article_update(args: argparse.Namespace) -> None:
    gid = to_gid("Article", args.id)
    article_input: dict = {}
    if args.title is not None:
        article_input["title"] = args.title
    if args.body is not None:
        article_input["body"] = args.body
    if args.tags is not None:
        article_input["tags"] = args.tags
    if args.publish and args.unpublish:
        die("Choose only one of --publish or --unpublish.", exit_code=2)
    if args.publish:
        article_input["isPublished"] = True
    if args.unpublish:
        article_input["isPublished"] = False

    result = ensure_ok(
        graphql(
        gql.ARTICLE_UPDATE,
        {"id": gid, "article": article_input},
        ),
        "articleUpdate",
    )
    emit({"ok": True, "data": result["data"]["articleUpdate"]["article"]})


def article_delete(args: argparse.Namespace) -> None:
    gid = to_gid("Article", args.id)
    result = ensure_ok(
        graphql(
        gql.ARTICLE_DELETE,
        {"id": gid},
        ),
        "articleDelete",
    )
    emit({"ok": True, "data": {"deletedArticleId": result["data"]["articleDelete"]["deletedArticleId"]}})


def file_upload(args: argparse.Namespace) -> None:
    content_type = args.content_type
    if not content_type:
        guessed = mimetypes.guess_type(args.path)[0] or ""
        ext = os.path.splitext(args.path)[1].lower()
        if guessed.startswith("image/"):
            content_type = "IMAGE"
        elif guessed.startswith("video/"):
            content_type = "VIDEO"
        elif ext in {".glb", ".gltf", ".usdz"}:
            content_type = "MODEL_3D"
        else:
            content_type = "FILE"

    if content_type == "EXTERNAL_VIDEO":
        die(
            "EXTERNAL_VIDEO must be created from a URL, not a local file.",
            exit_code=2,
        )

    try:
        resource_url = _staged_upload(args.path, content_type)
    except Exception as exc:
        die("Upload error.", details={"error": str(exc)})
    file_input: dict = {
        "originalSource": resource_url,
        "duplicateResolutionMode": args.duplicate,
        "contentType": content_type,
    }
    if args.alt:
        file_input["alt"] = args.alt
    if args.filename:
        file_input["filename"] = args.filename

    result = ensure_ok(
        graphql(
        gql.FILE_CREATE,
        {"files": [file_input]},
        ),
        "fileCreate",
    )
    emit({"ok": True, "data": result["data"]["fileCreate"]["files"]})


# ── CLI definition ──────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    class JsonArgumentParser(argparse.ArgumentParser):
        def error(self, message: str) -> None:
            die("Argument parsing error.", exit_code=2, details={"message": message, "usage": self.format_usage().strip()})

        def print_help(self, file=None) -> None:
            emit({"ok": True, "help": self.format_help()})

    parser = JsonArgumentParser(
        prog="shopify_admin",
        description="Shopify Admin GraphQL CLI — manage products, metafields, metaobjects, blogs & articles.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s product list --filter "status:active"
              %(prog)s product create "Hiking Boots" --vendor GeoStep --tags outdoor hiking
              %(prog)s metafield define product care_guide multi_line_text_field --name "Care Guide"
              %(prog)s metafield set Product 123 care_guide "Hand wash only"
              %(prog)s metaobject define designer name:single_line_text_field bio:multi_line_text_field
              %(prog)s metaobject create designer li-ming name="Li Ming" bio="Senior designer"
              %(prog)s blog create "Outdoor Adventures"
              %(prog)s article create --blog 123 "Summer Hiking" "<p>Best trails…</p>" --publish
        """),
    )
    sub = parser.add_subparsers(dest="command", help="top-level command")

    # ── product ─────────────────────────────────────────
    p_product = sub.add_parser("product", help="manage products")
    p_product_sub = p_product.add_subparsers(dest="action")

    p_pl = p_product_sub.add_parser("list", help="list products")
    p_pl.add_argument("--filter", "-f", default="", help="Shopify search query, e.g. 'status:active'")
    p_pl.add_argument("--limit", "-n", type=int, default=20, help="max results (default: 20)")
    p_pl.set_defaults(func=product_list)

    p_pg = p_product_sub.add_parser("get", help="get product details")
    p_pg.add_argument("id", help="product ID or GID")
    p_pg.set_defaults(func=product_get)

    p_pc = p_product_sub.add_parser("create", help="create a product")
    p_pc.add_argument("title", help="product title")
    p_pc.add_argument("--description", "-d", default=None, help="HTML description")
    p_pc.add_argument("--vendor", "-v", default=None, help="vendor name")
    p_pc.add_argument("--tags", nargs="*", default=None, help="space-separated tags")
    p_pc.add_argument("--image-url", action="append", default=[], help="attach image by URL (repeatable)")
    p_pc.add_argument("--image-file", action="append", default=[], help="upload local image file (repeatable)")
    p_pc.add_argument("--image-alt", default=None, help="alt text for all uploaded/attached images")
    p_pc.add_argument(
        "--status",
        choices=["ACTIVE", "DRAFT", "ARCHIVED"],
        default="DRAFT",
        help="product status (default: DRAFT)",
    )
    p_pc.set_defaults(func=product_create)

    p_pu = p_product_sub.add_parser("update", help="update a product")
    p_pu.add_argument("id", help="product ID or GID")
    p_pu.add_argument("--title", default=None)
    p_pu.add_argument("--description", default=None, help="HTML description")
    p_pu.add_argument("--vendor", default=None)
    p_pu.add_argument("--tags", nargs="*", default=None)
    p_pu.add_argument("--image-url", action="append", default=[], help="attach image by URL (repeatable)")
    p_pu.add_argument("--image-file", action="append", default=[], help="upload local image file (repeatable)")
    p_pu.add_argument("--image-alt", default=None, help="alt text for all uploaded/attached images")
    p_pu.add_argument("--status", choices=["ACTIVE", "DRAFT", "ARCHIVED"], default=None)
    p_pu.set_defaults(func=product_update)

    p_pd = p_product_sub.add_parser("delete", help="delete a product")
    p_pd.add_argument("id", help="product ID or GID")
    p_pd.set_defaults(func=product_delete)

    # ── metafield ───────────────────────────────────────
    p_mf = sub.add_parser("metafield", help="manage metafield definitions & values")
    p_mf_sub = p_mf.add_subparsers(dest="action")

    p_mfl = p_mf_sub.add_parser("list", help="list metafield definitions for an owner type")
    p_mfl.add_argument("owner_type", help="e.g. product, customer, order")
    p_mfl.add_argument("--limit", "-n", type=int, default=50)
    p_mfl.set_defaults(func=metafield_list)

    p_mfd = p_mf_sub.add_parser("define", help="create a metafield definition")
    p_mfd.add_argument("owner_type", help="e.g. product, customer, order")
    p_mfd.add_argument("key", help="metafield key (2-64 chars)")
    p_mfd.add_argument(
        "type",
        help="metafield type: single_line_text_field, number_integer, boolean, color, json, …",
    )
    p_mfd.add_argument("--name", default=None, help="human-readable name (defaults to key)")
    p_mfd.add_argument("--namespace", default=None, help="namespace (defaults to $app)")
    p_mfd.add_argument("--pin", action="store_true", help="pin the definition in admin")
    p_mfd.set_defaults(func=metafield_define)

    p_mfs = p_mf_sub.add_parser("set", help="set a metafield value on a resource")
    p_mfs.add_argument("owner_type", help="resource type, e.g. Product, Customer")
    p_mfs.add_argument("owner_id", help="resource numeric ID or GID")
    p_mfs.add_argument("key", help="metafield key")
    p_mfs.add_argument("value", help="metafield value (always a string)")
    p_mfs.add_argument("--type", default=None, help="metafield type (required if no definition)")
    p_mfs.add_argument("--namespace", default=None, help="namespace (defaults to $app)")
    p_mfs.set_defaults(func=metafield_set)

    # ── metaobject ──────────────────────────────────────
    p_mo = sub.add_parser("metaobject", help="manage metaobject definitions & entries")
    p_mo_sub = p_mo.add_subparsers(dest="action")

    p_mod = p_mo_sub.add_parser("define", help="create a metaobject definition")
    p_mod.add_argument("type", help="metaobject type identifier")
    p_mod.add_argument(
        "fields",
        nargs="+",
        help="field specs: key:type[:name[:required]]",
    )
    p_mod.add_argument("--name", default=None, help="human-readable name (defaults to type)")
    p_mod.add_argument("--display-key", default=None, help="field key used as display name")
    p_mod.set_defaults(func=metaobject_define)

    p_moc = p_mo_sub.add_parser("create", help="create/upsert a metaobject entry")
    p_moc.add_argument("type", help="metaobject type")
    p_moc.add_argument("handle", help="unique handle for the entry")
    p_moc.add_argument("fields", nargs="+", help="field values: key=value")
    p_moc.set_defaults(func=metaobject_create)

    p_mol = p_mo_sub.add_parser("list", help="list metaobject entries")
    p_mol.add_argument("type", help="metaobject type")
    p_mol.add_argument("--limit", "-n", type=int, default=20)
    p_mol.set_defaults(func=metaobject_list)

    p_mou = p_mo_sub.add_parser("update", help="update a metaobject entry")
    p_mou.add_argument("id", help="metaobject ID or GID")
    p_mou.add_argument("fields", nargs="+", help="field values: key=value")
    p_mou.set_defaults(func=metaobject_update)

    p_moDel = p_mo_sub.add_parser("delete", help="delete a metaobject entry")
    p_moDel.add_argument("id", help="metaobject ID or GID")
    p_moDel.set_defaults(func=metaobject_delete)

    # ── blog ────────────────────────────────────────────
    p_blog = sub.add_parser("blog", help="manage blogs")
    p_blog_sub = p_blog.add_subparsers(dest="action")

    p_bl = p_blog_sub.add_parser("list", help="list blogs")
    p_bl.add_argument("--limit", "-n", type=int, default=20)
    p_bl.set_defaults(func=blog_list)

    p_bc = p_blog_sub.add_parser("create", help="create a blog")
    p_bc.add_argument("title", help="blog title")
    p_bc.set_defaults(func=blog_create)

    # ── article ─────────────────────────────────────────
    p_art = sub.add_parser("article", help="manage blog articles")
    p_art_sub = p_art.add_subparsers(dest="action")

    p_al = p_art_sub.add_parser("list", help="list articles")
    p_al.add_argument("--blog", default=None, help="filter by blog ID")
    p_al.add_argument("--limit", "-n", type=int, default=20)
    p_al.set_defaults(func=article_list)

    p_ac = p_art_sub.add_parser("create", help="create an article")
    p_ac.add_argument("--blog", required=True, help="blog ID or GID")
    p_ac.add_argument("title", help="article title")
    p_ac.add_argument("body", help="article body (HTML)")
    p_ac.add_argument("--author", default="Admin", help="author name (default: Admin)")
    p_ac.add_argument("--tags", nargs="*", default=None, help="space-separated tags")
    p_ac.add_argument("--publish", action="store_true", help="publish immediately")
    p_ac.set_defaults(func=article_create)

    p_au = p_art_sub.add_parser("update", help="update an article")
    p_au.add_argument("id", help="article ID or GID")
    p_au.add_argument("--title", default=None)
    p_au.add_argument("--body", default=None, help="article body (HTML)")
    p_au.add_argument("--tags", nargs="*", default=None)
    p_au.add_argument("--publish", action="store_true", help="publish immediately")
    p_au.add_argument("--unpublish", action="store_true", help="set visibility to hidden")
    p_au.set_defaults(func=article_update)

    p_adel = p_art_sub.add_parser("delete", help="delete an article")
    p_adel.add_argument("id", help="article ID or GID")
    p_adel.set_defaults(func=article_delete)

    p_file = sub.add_parser("file", help="manage files")
    p_file_sub = p_file.add_subparsers(dest="action")

    p_fu = p_file_sub.add_parser("upload", help="upload a file to Shopify Files")
    p_fu.add_argument("path", help="local file path")
    p_fu.add_argument("--alt", default=None, help="alt text")
    p_fu.add_argument("--filename", default=None, help="override filename (must match extension)")
    p_fu.add_argument(
        "--content-type",
        default=None,
        choices=["IMAGE", "VIDEO", "MODEL_3D", "FILE"],
        help="file type (default: auto-detect)",
    )
    p_fu.add_argument(
        "--duplicate",
        default="APPEND_UUID",
        choices=["APPEND_UUID", "RAISE_ERROR", "REPLACE"],
        help="duplicate filename handling (default: APPEND_UUID)",
    )
    p_fu.set_defaults(func=file_upload)

    return parser


def main() -> None:
    try:
        parser = build_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
    except SystemExit:
        raise
    except Exception as exc:
        die(
            "Unhandled exception.",
            details={"type": exc.__class__.__name__, "error": str(exc)},
        )


if __name__ == "__main__":
    main()
