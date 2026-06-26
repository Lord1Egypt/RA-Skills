#!/usr/bin/env python3
"""
Confluence Cloud CLI - Interact with Confluence Cloud REST API v2.

Environment variables required:
  CONFLUENCE_BASE_URL - Confluence instance URL (e.g., https://yourcompany.atlassian.net)
  CONFLUENCE_USER_EMAIL - Atlassian account email
  CONFLUENCE_API_TOKEN - API token from https://id.atlassian.com/manage-profile/security/api-tokens
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote


def get_config():
    """Get Confluence configuration from environment."""
    base_url = os.environ.get("CONFLUENCE_BASE_URL", "").rstrip("/")
    email = os.environ.get("CONFLUENCE_USER_EMAIL", "")
    token = os.environ.get("CONFLUENCE_API_TOKEN", "")
    
    if not all([base_url, email, token]):
        missing = []
        if not base_url: missing.append("CONFLUENCE_BASE_URL")
        if not email: missing.append("CONFLUENCE_USER_EMAIL")
        if not token: missing.append("CONFLUENCE_API_TOKEN")
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    
    return base_url, email, token


def make_request(method, endpoint, data=None, params=None, api_version="v2"):
    """Make authenticated request to Confluence API."""
    base_url, email, token = get_config()
    
    if api_version == "v2":
        url = f"{base_url}/wiki/api/v2{endpoint}"
    else:
        url = f"{base_url}/wiki/rest/api{endpoint}"
    
    if params:
        url = f"{url}?{urlencode(params)}"
    
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
    }
    
    body = None
    if data:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    
    req = Request(url, data=body, headers=headers, method=method)
    
    try:
        with urlopen(req) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {}
    except HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except:
            print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def make_multipart_request(endpoint, file_path, comment=None):
    """Make multipart form request for file upload."""
    base_url, email, token = get_config()
    url = f"{base_url}/wiki/rest/api{endpoint}"
    
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    
    # Read file
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    filename = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(filename)
    if not content_type:
        content_type = "application/octet-stream"
    
    # Build multipart body
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    body_parts = []
    
    # File part
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    body_parts.append(f'Content-Type: {content_type}'.encode())
    body_parts.append(b'')
    body_parts.append(file_data)
    
    # Comment part (optional)
    if comment:
        body_parts.append(f'--{boundary}'.encode())
        body_parts.append(b'Content-Disposition: form-data; name="comment"')
        body_parts.append(b'Content-Type: text/plain; charset=utf-8')
        body_parts.append(b'')
        body_parts.append(comment.encode())
    
    # Minor edit
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(b'Content-Disposition: form-data; name="minorEdit"')
    body_parts.append(b'')
    body_parts.append(b'true')
    
    body_parts.append(f'--{boundary}--'.encode())
    
    body = b'\r\n'.join(body_parts)
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "X-Atlassian-Token": "nocheck",
    }
    
    req = Request(url, data=body, headers=headers, method="PUT")
    
    try:
        with urlopen(req) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {}
    except HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except:
            print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


# =============================================================================
# Space Commands
# =============================================================================

def cmd_spaces(args):
    """List all spaces."""
    params = {"limit": args.limit}
    if args.type:
        params["type"] = args.type
    if args.status:
        params["status"] = args.status
    if args.keys:
        params["keys"] = args.keys
    
    result = make_request("GET", "/spaces", params=params)
    
    spaces = []
    for space in result.get("results", []):
        spaces.append({
            "id": space.get("id"),
            "key": space.get("key"),
            "name": space.get("name"),
            "type": space.get("type"),
            "status": space.get("status"),
            "homepageId": space.get("homepageId"),
        })
    
    print(json.dumps(spaces, indent=2))


def cmd_space(args):
    """Get space details by ID."""
    params = {}
    if args.include_labels:
        params["include-labels"] = "true"
    
    result = make_request("GET", f"/spaces/{args.space_id}", params=params if params else None)
    print(json.dumps(result, indent=2))


def cmd_space_by_key(args):
    """Get space by key."""
    params = {"keys": args.space_key, "limit": 1}
    result = make_request("GET", "/spaces", params=params)
    
    spaces = result.get("results", [])
    if not spaces:
        print(f"Error: Space with key '{args.space_key}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(spaces[0], indent=2))


def cmd_create_space(args):
    """Create a new space."""
    data = {
        "name": args.name,
        "key": args.key,
    }
    
    if args.description:
        data["description"] = {
            "value": args.description,
            "representation": "plain"
        }
    
    if args.private:
        data["createPrivateSpace"] = True
    
    result = make_request("POST", "/spaces", data)
    print(json.dumps(result, indent=2))


# =============================================================================
# Page Commands
# =============================================================================

def cmd_pages(args):
    """List pages."""
    params = {"limit": args.limit}
    
    if args.space_id:
        endpoint = f"/spaces/{args.space_id}/pages"
    else:
        endpoint = "/pages"
        if args.title:
            params["title"] = args.title
    
    if args.status:
        params["status"] = args.status
    if args.body_format:
        params["body-format"] = args.body_format
    
    result = make_request("GET", endpoint, params=params)
    
    pages = []
    for page in result.get("results", []):
        pages.append({
            "id": page.get("id"),
            "title": page.get("title"),
            "status": page.get("status"),
            "spaceId": page.get("spaceId"),
            "parentId": page.get("parentId"),
            "createdAt": page.get("createdAt"),
            "version": page.get("version", {}).get("number"),
        })
    
    print(json.dumps(pages, indent=2))


def cmd_page(args):
    """Get page by ID."""
    params = {}
    if args.body_format:
        params["body-format"] = args.body_format
    if args.include_labels:
        params["include-labels"] = "true"
    if args.version:
        params["version"] = args.version
    
    result = make_request("GET", f"/pages/{args.page_id}", params=params if params else None)
    print(json.dumps(result, indent=2))


def cmd_create_page(args):
    """Create a new page."""
    data = {
        "spaceId": args.space_id,
        "title": args.title,
        "body": {
            "representation": "storage",
            "value": args.body or ""
        }
    }
    
    if args.parent_id:
        data["parentId"] = args.parent_id
    
    if args.status:
        data["status"] = args.status
    
    result = make_request("POST", "/pages", data)
    print(json.dumps(result, indent=2))


def cmd_update_page(args):
    """Update an existing page."""
    # First get current page to get version number
    current = make_request("GET", f"/pages/{args.page_id}")
    current_version = current.get("version", {}).get("number", 1)
    
    data = {
        "id": args.page_id,
        "status": args.status or "current",
        "title": args.title or current.get("title"),
        "body": {
            "representation": "storage",
            "value": args.body
        },
        "version": {
            "number": current_version + 1
        }
    }
    
    if args.message:
        data["version"]["message"] = args.message
    
    result = make_request("PUT", f"/pages/{args.page_id}", data)
    print(json.dumps(result, indent=2))


def cmd_delete_page(args):
    """Delete a page."""
    params = {}
    if args.purge:
        params["purge"] = "true"
    
    make_request("DELETE", f"/pages/{args.page_id}", params=params if params else None)
    print(json.dumps({"status": "deleted", "id": args.page_id, "purged": args.purge}))


# =============================================================================
# Page Tree / Children Commands
# =============================================================================

def cmd_children(args):
    """Get child pages."""
    params = {"limit": args.limit}
    
    result = make_request("GET", f"/pages/{args.page_id}/children", params=params)
    
    children = []
    for child in result.get("results", []):
        children.append({
            "id": child.get("id"),
            "title": child.get("title"),
            "status": child.get("status"),
            "spaceId": child.get("spaceId"),
        })
    
    print(json.dumps(children, indent=2))


def cmd_ancestors(args):
    """Get page ancestors (parent chain)."""
    # Use v1 API for ancestors
    result = make_request("GET", f"/content/{args.page_id}?expand=ancestors", api_version="v1")
    
    ancestors = []
    for ancestor in result.get("ancestors", []):
        ancestors.append({
            "id": ancestor.get("id"),
            "title": ancestor.get("title"),
            "type": ancestor.get("type"),
        })
    
    print(json.dumps(ancestors, indent=2))


# =============================================================================
# Search Commands
# =============================================================================

def cmd_search(args):
    """Search content using CQL."""
    params = {
        "cql": args.cql,
        "limit": args.limit,
    }
    
    if args.expand:
        params["expand"] = args.expand
    
    result = make_request("GET", "/search", params=params, api_version="v1")
    
    results = []
    for item in result.get("results", []):
        content = item.get("content", {})
        results.append({
            "id": content.get("id"),
            "type": content.get("type"),
            "title": item.get("title") or content.get("title"),
            "space": content.get("space", {}).get("key"),
            "excerpt": item.get("excerpt"),
            "url": item.get("url"),
            "lastModified": item.get("lastModified"),
        })
    
    print(json.dumps(results, indent=2))


# =============================================================================
# Attachment Commands
# =============================================================================

def cmd_attachments(args):
    """List attachments for a page."""
    params = {"limit": args.limit}
    if args.filename:
        params["filename"] = args.filename
    if args.media_type:
        params["mediaType"] = args.media_type
    
    result = make_request("GET", f"/pages/{args.page_id}/attachments", params=params)
    
    attachments = []
    for att in result.get("results", []):
        attachments.append({
            "id": att.get("id"),
            "title": att.get("title"),
            "mediaType": att.get("mediaType"),
            "fileSize": att.get("fileSize"),
            "downloadLink": att.get("downloadLink"),
            "createdAt": att.get("createdAt"),
        })
    
    print(json.dumps(attachments, indent=2))


def cmd_attachment(args):
    """Get attachment by ID."""
    result = make_request("GET", f"/attachments/{args.attachment_id}")
    print(json.dumps(result, indent=2))


def cmd_upload_attachment(args):
    """Upload an attachment to a page."""
    result = make_multipart_request(
        f"/content/{args.page_id}/child/attachment",
        args.file_path,
        args.comment
    )
    print(json.dumps(result, indent=2))


def cmd_download_attachment(args):
    """Download an attachment."""
    base_url, email, token = get_config()
    
    # Get attachment info
    att = make_request("GET", f"/attachments/{args.attachment_id}")
    download_link = att.get("downloadLink")
    
    if not download_link:
        print("Error: No download link found", file=sys.stderr)
        sys.exit(1)
    
    url = f"{base_url}/wiki{download_link}"
    
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    
    req = Request(url, headers=headers)
    
    try:
        with urlopen(req) as resp:
            output_path = args.output or att.get("title", "attachment")
            with open(output_path, "wb") as f:
                f.write(resp.read())
            print(json.dumps({"status": "downloaded", "path": output_path}))
    except HTTPError as e:
        print(f"HTTP {e.code}: Failed to download", file=sys.stderr)
        sys.exit(1)


def cmd_delete_attachment(args):
    """Delete an attachment."""
    params = {}
    if args.purge:
        params["purge"] = "true"
    
    make_request("DELETE", f"/attachments/{args.attachment_id}", params=params if params else None)
    print(json.dumps({"status": "deleted", "id": args.attachment_id}))


# =============================================================================
# Comment Commands
# =============================================================================

def cmd_comments(args):
    """List comments for a page."""
    params = {"limit": args.limit}
    if args.body_format:
        params["body-format"] = args.body_format
    
    result = make_request("GET", f"/pages/{args.page_id}/footer-comments", params=params)
    
    comments = []
    for comment in result.get("results", []):
        body = comment.get("body", {})
        body_value = ""
        if body.get("storage"):
            body_value = body.get("storage", {}).get("value", "")
        elif body.get("atlas_doc_format"):
            body_value = body.get("atlas_doc_format", {}).get("value", "")
        
        comments.append({
            "id": comment.get("id"),
            "status": comment.get("status"),
            "body": body_value,
            "version": comment.get("version", {}).get("number"),
        })
    
    print(json.dumps(comments, indent=2))


def cmd_comment(args):
    """Get comment by ID."""
    params = {}
    if args.body_format:
        params["body-format"] = args.body_format
    
    result = make_request("GET", f"/footer-comments/{args.comment_id}", params=params if params else None)
    print(json.dumps(result, indent=2))


def cmd_create_comment(args):
    """Create a comment on a page."""
    data = {
        "pageId": args.page_id,
        "body": {
            "representation": "storage",
            "value": args.body
        }
    }
    
    result = make_request("POST", "/footer-comments", data)
    print(json.dumps(result, indent=2))


def cmd_update_comment(args):
    """Update a comment."""
    # Get current version
    current = make_request("GET", f"/footer-comments/{args.comment_id}")
    current_version = current.get("version", {}).get("number", 1)
    
    data = {
        "body": {
            "representation": "storage",
            "value": args.body
        },
        "version": {
            "number": current_version + 1
        }
    }
    
    result = make_request("PUT", f"/footer-comments/{args.comment_id}", data)
    print(json.dumps(result, indent=2))


def cmd_delete_comment(args):
    """Delete a comment."""
    make_request("DELETE", f"/footer-comments/{args.comment_id}")
    print(json.dumps({"status": "deleted", "id": args.comment_id}))


# =============================================================================
# Label Commands
# =============================================================================

def cmd_labels(args):
    """Get labels for a page."""
    params = {"limit": args.limit}
    
    result = make_request("GET", f"/pages/{args.page_id}/labels", params=params)
    
    labels = []
    for label in result.get("results", []):
        labels.append({
            "id": label.get("id"),
            "name": label.get("name"),
            "prefix": label.get("prefix"),
        })
    
    print(json.dumps(labels, indent=2))


def cmd_add_labels(args):
    """Add labels to a page."""
    labels = [{"prefix": "global", "name": l.strip()} for l in args.labels.split(",")]
    
    # V1 API for label management
    result = make_request("POST", f"/content/{args.page_id}/label", labels, api_version="v1")
    print(json.dumps(result, indent=2))


def cmd_remove_label(args):
    """Remove a label from a page."""
    make_request("DELETE", f"/content/{args.page_id}/label/{args.label}", api_version="v1")
    print(json.dumps({"status": "removed", "label": args.label}))


# =============================================================================
# User Commands
# =============================================================================

def cmd_me(args):
    """Get current user info."""
    result = make_request("GET", "/user/current", api_version="v1")
    print(json.dumps(result, indent=2))


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Confluence Cloud CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # --- Spaces ---
    p = subparsers.add_parser("spaces", help="List spaces")
    p.add_argument("--type", choices=["global", "personal"])
    p.add_argument("--status", choices=["current", "archived"])
    p.add_argument("--keys", help="Comma-separated space keys")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_spaces)
    
    p = subparsers.add_parser("space", help="Get space by ID")
    p.add_argument("space_id", help="Space ID")
    p.add_argument("--include-labels", action="store_true")
    p.set_defaults(func=cmd_space)
    
    p = subparsers.add_parser("space-by-key", help="Get space by key")
    p.add_argument("space_key", help="Space key (e.g., PROJ)")
    p.set_defaults(func=cmd_space_by_key)
    
    p = subparsers.add_parser("create-space", help="Create space")
    p.add_argument("--name", required=True, help="Space name")
    p.add_argument("--key", required=True, help="Space key")
    p.add_argument("--description", help="Space description")
    p.add_argument("--private", action="store_true", help="Create private space")
    p.set_defaults(func=cmd_create_space)
    
    # --- Pages ---
    p = subparsers.add_parser("pages", help="List pages")
    p.add_argument("--space-id", help="Filter by space ID")
    p.add_argument("--title", help="Filter by title")
    p.add_argument("--status", choices=["current", "draft", "trashed"])
    p.add_argument("--body-format", choices=["storage", "atlas_doc_format", "view"])
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_pages)
    
    p = subparsers.add_parser("page", help="Get page by ID")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--body-format", choices=["storage", "atlas_doc_format", "view"])
    p.add_argument("--include-labels", action="store_true")
    p.add_argument("--version", type=int, help="Specific version")
    p.set_defaults(func=cmd_page)
    
    p = subparsers.add_parser("create-page", help="Create page")
    p.add_argument("--space-id", required=True, help="Space ID")
    p.add_argument("--title", required=True, help="Page title")
    p.add_argument("--body", help="Page body (storage format)")
    p.add_argument("--parent-id", help="Parent page ID")
    p.add_argument("--status", choices=["current", "draft"], default="current")
    p.set_defaults(func=cmd_create_page)
    
    p = subparsers.add_parser("update-page", help="Update page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--body", required=True, help="New body (storage format)")
    p.add_argument("--status", choices=["current", "draft"])
    p.add_argument("--message", help="Version message")
    p.set_defaults(func=cmd_update_page)
    
    p = subparsers.add_parser("delete-page", help="Delete page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--purge", action="store_true", help="Permanently delete")
    p.set_defaults(func=cmd_delete_page)
    
    # --- Page Tree ---
    p = subparsers.add_parser("children", help="Get child pages")
    p.add_argument("page_id", help="Parent page ID")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_children)
    
    p = subparsers.add_parser("ancestors", help="Get page ancestors")
    p.add_argument("page_id", help="Page ID")
    p.set_defaults(func=cmd_ancestors)
    
    # --- Search ---
    p = subparsers.add_parser("search", help="Search content (CQL)")
    p.add_argument("cql", help="CQL query string")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--expand", help="Fields to expand")
    p.set_defaults(func=cmd_search)
    
    # --- Attachments ---
    p = subparsers.add_parser("attachments", help="List page attachments")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--filename", help="Filter by filename")
    p.add_argument("--media-type", help="Filter by media type")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_attachments)
    
    p = subparsers.add_parser("attachment", help="Get attachment by ID")
    p.add_argument("attachment_id", help="Attachment ID")
    p.set_defaults(func=cmd_attachment)
    
    p = subparsers.add_parser("upload", help="Upload attachment")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("file_path", help="Path to file")
    p.add_argument("--comment", help="Attachment comment")
    p.set_defaults(func=cmd_upload_attachment)
    
    p = subparsers.add_parser("download", help="Download attachment")
    p.add_argument("attachment_id", help="Attachment ID")
    p.add_argument("--output", "-o", help="Output file path")
    p.set_defaults(func=cmd_download_attachment)
    
    p = subparsers.add_parser("delete-attachment", help="Delete attachment")
    p.add_argument("attachment_id", help="Attachment ID")
    p.add_argument("--purge", action="store_true", help="Permanently delete")
    p.set_defaults(func=cmd_delete_attachment)
    
    # --- Comments ---
    p = subparsers.add_parser("comments", help="List page comments")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--body-format", choices=["storage", "atlas_doc_format", "view"])
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_comments)
    
    p = subparsers.add_parser("comment", help="Get comment by ID")
    p.add_argument("comment_id", help="Comment ID")
    p.add_argument("--body-format", choices=["storage", "atlas_doc_format", "view"])
    p.set_defaults(func=cmd_comment)
    
    p = subparsers.add_parser("create-comment", help="Create comment")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("body", help="Comment body (storage format)")
    p.set_defaults(func=cmd_create_comment)
    
    p = subparsers.add_parser("update-comment", help="Update comment")
    p.add_argument("comment_id", help="Comment ID")
    p.add_argument("body", help="New body (storage format)")
    p.set_defaults(func=cmd_update_comment)
    
    p = subparsers.add_parser("delete-comment", help="Delete comment")
    p.add_argument("comment_id", help="Comment ID")
    p.set_defaults(func=cmd_delete_comment)
    
    # --- Labels ---
    p = subparsers.add_parser("labels", help="Get page labels")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_labels)
    
    p = subparsers.add_parser("add-labels", help="Add labels to page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("labels", help="Comma-separated label names")
    p.set_defaults(func=cmd_add_labels)
    
    p = subparsers.add_parser("remove-label", help="Remove label from page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("label", help="Label name")
    p.set_defaults(func=cmd_remove_label)
    
    # --- User ---
    p = subparsers.add_parser("me", help="Get current user")
    p.set_defaults(func=cmd_me)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
