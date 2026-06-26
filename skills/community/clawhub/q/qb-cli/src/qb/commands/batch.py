"""Batch operations command."""

import json
from pathlib import Path
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Batch operations (up to 30 per request).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command()
def run(
    file: Annotated[str, typer.Option("--file", help="JSON file with batch operations array")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Execute a batch of operations from a JSON file.

    File format: array of operations, each with:
    - "operation": "create", "update", "delete", or "query"
    - "entity": entity name (e.g., "Customer", "Invoice")
    - "body": entity data (for create/update/delete)
    - "sql": query string (for query operations)

    Max 30 operations per batch. Auto-chunks if more.
    """
    fmt = output or _output()
    client = _client()

    with open(file) as f:
        operations = json.load(f)

    if not isinstance(operations, list):
        typer.echo(json.dumps({"error": True, "message": "File must contain a JSON array"}), err=True)
        raise SystemExit(5)

    # Build BatchItemRequest items
    all_results = []
    chunk_size = 30

    for chunk_start in range(0, len(operations), chunk_size):
        chunk = operations[chunk_start:chunk_start + chunk_size]
        batch_items = []

        for i, op in enumerate(chunk):
            bid = str(chunk_start + i + 1)
            item: dict = {"bId": bid}

            op_type = op.get("operation", "").lower()
            entity = op.get("entity", "")

            if op_type == "query":
                item["Query"] = op.get("sql", op.get("query", ""))
            elif op_type in ("create", "update"):
                item["operation"] = op_type
                item[entity] = op.get("body", {})
            elif op_type == "delete":
                item["operation"] = "delete"
                body = op.get("body", {})
                if not body:
                    body = {"Id": op.get("id"), "SyncToken": op.get("sync_token", "0")}
                item[entity] = body
            else:
                all_results.append({"bId": bid, "error": f"Unknown operation: {op_type}"})
                continue

            batch_items.append(item)

        if batch_items:
            payload = {"BatchItemRequest": batch_items}
            resp = client.post("batch", payload)
            batch_resp = resp.get("BatchItemResponse", [])
            all_results.extend(batch_resp)

    result = {
        "total_operations": len(operations),
        "chunks": (len(operations) + chunk_size - 1) // chunk_size,
        "results": all_results,
    }

    format_output(result, fmt)
