"""JournalEntry resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks journal entries.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_entries(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all journal entries."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM JournalEntry", max_results=limit)
    entries = result.get("QueryResponse", {}).get("JournalEntry", [])
    format_output(
        entries,
        fmt,
        columns=["Id", "DocNumber", "TxnDate", "TotalAmt", "PrivateNote"],
    )


@app.command()
def get(
    entry_id: Annotated[str, typer.Argument(help="JournalEntry ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a journal entry by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"journalentry/{entry_id}")
    format_output(result.get("JournalEntry"), fmt)


@app.command()
def create(
    lines: Annotated[
        Optional[str],
        typer.Option("--lines", help='Simplified lines JSON: [{"account_id":"X","amount":100,"type":"Debit","description":"..."},...]'),
    ] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Entry date (YYYY-MM-DD)")] = None,
    doc_number: Annotated[Optional[str], typer.Option("--doc-number", help="Reference number")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full journal entry JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a journal entry (adjusting entry, accrual, depreciation, etc.).

    Simplified: --lines '[{"account_id":"80","amount":500,"type":"Debit"},{"account_id":"35","amount":500,"type":"Credit"}]'
    Full control: --json '{"Line":[...]}'

    Debits must equal credits or the request will fail.
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif lines:
        parsed = json.loads(lines)
        # Validate debits == credits
        total_debit = sum(l["amount"] for l in parsed if l.get("type", "").lower() == "debit")
        total_credit = sum(l["amount"] for l in parsed if l.get("type", "").lower() == "credit")
        if abs(total_debit - total_credit) > 0.01:
            typer.echo(
                json.dumps({
                    "error": True,
                    "message": f"Debits ({total_debit}) must equal credits ({total_credit})",
                }),
                err=True,
            )
            raise SystemExit(5)

        qb_lines = []
        for l in parsed:
            posting_type = "Debit" if l.get("type", "").lower() == "debit" else "Credit"
            detail: dict = {
                "PostingType": posting_type,
                "AccountRef": {"value": str(l["account_id"])},
            }
            if l.get("entity_id"):
                detail["Entity"] = {
                    "EntityRef": {"value": str(l["entity_id"])},
                    "Type": l.get("entity_type", "Customer"),
                }
            if l.get("class_id"):
                detail["ClassRef"] = {"value": str(l["class_id"])}
            if l.get("department_id"):
                detail["DepartmentRef"] = {"value": str(l["department_id"])}

            qb_lines.append({
                "Amount": l["amount"],
                "DetailType": "JournalEntryLineDetail",
                "JournalEntryLineDetail": detail,
                "Description": l.get("description", ""),
            })

        body = {"Line": qb_lines}
    else:
        typer.echo(
            json.dumps({"error": True, "message": "Provide --lines or --json"}),
            err=True,
        )
        raise SystemExit(5)

    if txn_date:
        body["TxnDate"] = txn_date
    if doc_number:
        body["DocNumber"] = doc_number
    if memo:
        body["PrivateNote"] = memo

    result = client.post("journalentry", body)
    format_output(result.get("JournalEntry"), fmt)


@app.command()
def delete(
    entry_id: Annotated[str, typer.Argument(help="JournalEntry ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a journal entry."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"journalentry/{entry_id}").get("JournalEntry", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("journalentry", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against JournalEntry."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM JournalEntry WHERE {sql}"

    result = client.query(sql)
    entries = result.get("QueryResponse", {}).get("JournalEntry", [])
    format_output(
        entries,
        fmt,
        columns=["Id", "DocNumber", "TxnDate", "TotalAmt", "PrivateNote"],
    )
