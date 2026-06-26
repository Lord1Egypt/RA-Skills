"""Attachment (file upload) commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks file attachments.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_attachments(
    entity_type: Annotated[str, typer.Option("--entity-type", help="Entity type (Invoice, Bill, Customer, etc.)")],
    entity_id: Annotated[str, typer.Option("--entity-id", help="Entity ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List attachments for an entity."""
    fmt = output or _output()
    client = _client()

    from qb.api.query import escape_query_value

    safe_type = escape_query_value(entity_type)
    safe_id = escape_query_value(entity_id)
    result = client.query(
        f"SELECT * FROM Attachable WHERE AttachableRef.EntityRef.Type = '{safe_type}' "
        f"AND AttachableRef.EntityRef.value = '{safe_id}'",
        max_results=100,
    )
    attachments = result.get("QueryResponse", {}).get("Attachable", [])
    format_output(
        attachments,
        fmt,
        columns=["Id", "FileName", "ContentType", "Size", "Note"],
    )


@app.command()
def get(
    attachment_id: Annotated[str, typer.Argument(help="Attachment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get attachment metadata (includes temporary download URL)."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"attachable/{attachment_id}")
    format_output(result.get("Attachable"), fmt)


@app.command()
def upload(
    entity_type: Annotated[str, typer.Option("--entity-type", help="Entity type to attach to")],
    entity_id: Annotated[str, typer.Option("--entity-id", help="Entity ID to attach to")],
    file_path: Annotated[str, typer.Option("--file", help="Path to file to upload")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Upload a file attachment to an entity.

    Note: Uses the multipart upload endpoint. Supported file types include
    images (PNG, JPG, GIF), documents (PDF, DOC, DOCX, XLS, XLSX), and text files.
    """
    fmt = output or _output()
    client = _client()

    import mimetypes
    from pathlib import Path

    path = Path(file_path)
    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    file_name = path.name

    # Create metadata
    metadata = {
        "AttachableRef": [{
            "EntityRef": {
                "type": entity_type,
                "value": entity_id,
            },
        }],
        "FileName": file_name,
        "ContentType": content_type,
    }

    # For the upload endpoint, we need to use multipart/form-data
    # The QB API expects: metadata part (JSON) + file part (binary)
    import httpx

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Build multipart manually
    files = {
        "file_metadata_0": (None, json.dumps(metadata), "application/json"),
        "file_content_0": (file_name, file_data, content_type),
    }

    # Use the client's auth headers but make a direct request
    headers = {
        "Authorization": f"Bearer {client.token_manager.get_access_token(client.client_id, client.client_secret)}",
        "Accept": "application/json",
    }

    url = f"{client.base_url}/v3/company/{client.realm_id}/upload?minorversion=75"

    with httpx.Client() as http:
        resp = http.post(url, files=files, headers=headers)
        resp.raise_for_status()
        result = resp.json()

    format_output(result.get("AttachableResponse", [{}])[0].get("Attachable", result), fmt)


@app.command()
def delete(
    attachment_id: Annotated[str, typer.Argument(help="Attachment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete an attachment."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"attachable/{attachment_id}").get("Attachable", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("attachable", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def note(
    entity_type: Annotated[str, typer.Option("--entity-type", help="Entity type")],
    entity_id: Annotated[str, typer.Option("--entity-id", help="Entity ID")],
    text: Annotated[str, typer.Option("--text", help="Note text")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Add a note-only attachment to an entity."""
    fmt = output or _output()
    client = _client()

    body = {
        "Note": text,
        "AttachableRef": [{
            "EntityRef": {
                "type": entity_type,
                "value": entity_id,
            },
        }],
    }

    result = client.post("attachable", body)
    format_output(result.get("Attachable"), fmt)
