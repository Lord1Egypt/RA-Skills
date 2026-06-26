"""
wallet-mcp — Multi Wallet Generator + Manager
FastMCP server exposing wallet tools to Claude Desktop, Claude Code,
OpenClaw, Hermes, and any MCP-compatible AI agent.
"""
import sys

# Load .env file before anything reads os.getenv()
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — env vars must be set manually

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Multi Wallet Generator + Manager",
    instructions=(
        "Manage EVM and Solana wallets. "
        "You can generate wallets, send native tokens to groups, "
        "check balances, close empty Solana token accounts, "
        "and organise wallets by label/tag."
    ),
)


# ── 1. generate_wallets ────────────────────────────────────────────────────

@mcp.tool()
def generate_wallets(chain: str, count: int, label: str, tags: str = "") -> dict:
    """
    Generate N new wallets and save them to local storage.

    Args:
        chain:  'solana' or 'evm'
        count:  number of wallets to create (1 – 10,000)
        label:  group label, e.g. 'airdrop1' or 'campaign2'
        tags:   optional pipe-separated tags, e.g. 'vip|batch1'

    Returns:
        {status, chain, label, generated, wallets: [{address}]}
    """
    try:
        from wallet_mcp.core.generator import generate_wallets as _gen
        wallets = _gen(chain=chain, count=count, label=label, tags=tags)
        return {
            "status":    "success",
            "chain":     chain,
            "label":     label,
            "generated": len(wallets),
            "wallets":   [{"address": w["address"]} for w in wallets],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 2. send_native_multi ───────────────────────────────────────────────────

@mcp.tool()
def send_native_multi(
    from_key:  str,
    label:     str,
    amount:    float,
    chain:     str,
    rpc:       str = "",
    tag:       str = "",
    randomize: bool = False,
    delay_min: int = 1,
    delay_max: int = 30,
    retries:   int = 3,
) -> dict:
    """
    Send native tokens (SOL / ETH) from one source wallet to all wallets in a group.

    Args:
        from_key:  sender private key (base58 for Solana, hex for EVM)
        label:     target wallet group label
        amount:    base amount to send per wallet
        chain:     'solana' or 'evm'
        rpc:       custom RPC URL (optional)
        tag:       filter recipients by tag (optional)
        randomize: randomize each amount ±10% (default False)
        delay_min: minimum seconds between sends (default 1)
        delay_max: maximum seconds between sends (default 30)
        retries:   retry attempts per failed send (default 3)

    Returns:
        {status, chain, total, sent, failed, results}
    """
    try:
        from wallet_mcp.core.storage import filter_wallets
        from wallet_mcp.core.distributor import send_native_multi as _send

        recipients = filter_wallets(chain=chain, label=label, tag=tag or None)
        if not recipients:
            return {"status": "error", "message": f"No wallets found for chain={chain} label={label}"}

        return _send(
            from_private_key=from_key,
            recipients=recipients,
            amount=amount,
            chain=chain,
            rpc_url=rpc or None,
            randomize=randomize,
            delay_min=delay_min,
            delay_max=delay_max,
            retry_attempts=retries,
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 3. list_wallets ────────────────────────────────────────────────────────

@mcp.tool()
def list_wallets(
    chain:     str = "",
    label:     str = "",
    tag:       str = "",
    show_keys: bool = False,
) -> dict:
    """
    List wallets from local storage with optional filters.

    Args:
        chain:     filter by chain ('solana' | 'evm') — optional
        label:     filter by group label — optional
        tag:       filter by tag — optional
        show_keys: include private keys in output (default False — keep False unless needed)

    Returns:
        {status, count, wallets}
    """
    try:
        from wallet_mcp.core.manager import list_wallets as _list
        wallets = _list(
            chain=chain or None,
            label=label or None,
            tag=tag or None,
            show_keys=show_keys,
        )
        return {"status": "success", "count": len(wallets), "wallets": wallets}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 4. close_token_accounts ────────────────────────────────────────────────

@mcp.tool()
def close_token_accounts(
    private_key:     str,
    rpc:             str = "",
    close_non_empty: bool = False,
) -> dict:
    """
    Close empty SPL token accounts on Solana to reclaim rent SOL.

    Args:
        private_key:     wallet private key (base58)
        rpc:             custom Solana RPC URL (optional)
        close_non_empty: also close accounts with token balance — use with caution

    Returns:
        {status, closed, failed, skipped, total_found, reclaimed_sol_estimate}
    """
    try:
        from wallet_mcp.core.solana import close_token_accounts as _close
        result = _close(
            private_key_b58=private_key,
            rpc_url=rpc or None,
            close_non_empty=close_non_empty,
        )
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 5. get_balance_batch ───────────────────────────────────────────────────

@mcp.tool()
def get_balance_batch(
    chain: str = "",
    label: str = "",
    tag:   str = "",
    rpc:   str = "",
) -> dict:
    """
    Fetch native token balances for all wallets matching a filter.

    Args:
        chain: filter by chain ('solana' | 'evm') — optional
        label: filter by group label — optional
        tag:   filter by tag — optional
        rpc:   custom RPC URL — optional

    Returns:
        {status, total, sum, results: [{address, chain, label, balance, status}]}
    """
    try:
        from wallet_mcp.core.manager import get_balance_batch as _bal
        result = _bal(
            chain=chain or None,
            label=label or None,
            tag=tag or None,
            rpc_url=rpc or None,
        )
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 6. tag_wallets ─────────────────────────────────────────────────────────

@mcp.tool()
def tag_wallets(label: str, tag: str) -> dict:
    """
    Add a tag to all wallets with the given label.

    Args:
        label: wallet group label
        tag:   tag string to add (e.g. 'funded', 'used', 'vip')

    Returns:
        {status, label, tag, updated}
    """
    try:
        from wallet_mcp.core.manager import tag_label
        result = tag_label(label=label, tag=tag)
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 7. group_summary ───────────────────────────────────────────────────────

@mcp.tool()
def group_summary() -> dict:
    """
    Show a summary of all wallet groups with counts per chain.

    Returns:
        {status, groups: [{label, evm, solana, total}]}
    """
    try:
        from wallet_mcp.core.manager import group_summary as _summary
        return {"status": "success", "groups": _summary()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 8. delete_group ────────────────────────────────────────────────────────

@mcp.tool()
def delete_group(label: str) -> dict:
    """
    Delete all wallets in a group by label. This is permanent.

    Args:
        label: wallet group label to delete

    Returns:
        {status, label, deleted}
    """
    try:
        from wallet_mcp.core.manager import delete_group as _del
        result = _del(label=label)
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 9. scan_token_accounts ─────────────────────────────────────────────────

@mcp.tool()
def scan_token_accounts(address: str, rpc: str = "") -> dict:
    """
    Scan all SPL token accounts for a Solana wallet (read-only, no changes).

    Args:
        address: Solana wallet public key
        rpc:     custom RPC URL (optional)

    Returns:
        {status, total, empty, non_empty, accounts}
    """
    try:
        from wallet_mcp.core.solana import get_token_accounts, DEFAULT_RPC
        accounts = get_token_accounts(address, rpc or DEFAULT_RPC)
        empty    = [a for a in accounts if a["amount"] == 0]
        return {
            "status":    "success",
            "total":     len(accounts),
            "empty":     len(empty),
            "non_empty": len(accounts) - len(empty),
            "accounts":  accounts,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 10. sweep_wallets ──────────────────────────────────────────────────────

@mcp.tool()
def sweep_wallets(
    to_address: str,
    chain:      str,
    label:      str = "",
    tag:        str = "",
    rpc:        str = "",
    leave_lamports: int = 5000,
    delay_min:  int = 1,
    delay_max:  int = 10,
    retries:    int = 3,
) -> dict:
    """
    Sweep all native tokens (SOL / ETH) from a wallet group back to one destination.

    Useful for consolidating funds after a campaign or reclaiming leftover balances.

    Args:
        to_address:     destination address that receives all funds
        chain:          'solana' or 'evm'
        label:          source wallet group label — optional (leave blank to sweep by tag only)
        tag:            filter source wallets by tag — optional
        rpc:            custom RPC URL — optional
        leave_lamports: lamports to keep in each Solana wallet to cover the tx fee (default 5000)
        delay_min:      minimum seconds between sends (default 1)
        delay_max:      maximum seconds between sends (default 10)
        retries:        retry attempts per failed send (default 3)

    Returns:
        {status, chain, to_address, total, swept, skipped, failed, total_swept, results}
    """
    try:
        from wallet_mcp.core.storage import filter_wallets
        from wallet_mcp.core.distributor import sweep_native_multi

        wallets = filter_wallets(chain=chain, label=label or None, tag=tag or None)
        if not wallets:
            return {"status": "error", "message": f"No wallets found for chain={chain} label={label}"}

        return sweep_native_multi(
            wallets=wallets,
            to_address=to_address,
            chain=chain,
            rpc_url=rpc or None,
            leave_lamports=leave_lamports,
            delay_min=delay_min,
            delay_max=delay_max,
            retry_attempts=retries,
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 11. scan_token_balances ────────────────────────────────────────────────

@mcp.tool()
def scan_token_balances(
    chain: str,
    label: str = "",
    tag:   str = "",
    token: str = "",
    rpc:   str = "",
) -> dict:
    """
    Scan SPL / ERC-20 token balances for all wallets in a group.

    For Solana: returns all token accounts per wallet (or filter to one mint via `token`).
    For EVM:    `token` (ERC-20 contract address) is required.

    Args:
        chain: 'solana' or 'evm'
        label: filter by wallet group label — optional
        tag:   filter by tag — optional
        token: SPL mint address (Solana) or ERC-20 contract address (EVM)
        rpc:   custom RPC URL — optional

    Returns:
        {status, chain, token, total_wallets, wallets_with_balance, results}
    """
    try:
        from wallet_mcp.core.manager import scan_token_balances as _scan
        result = _scan(
            chain=chain,
            label=label or None,
            tag=tag or None,
            token=token or None,
            rpc_url=rpc or None,
        )
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 12. export_wallets ────────────────────────────────────────────────────

@mcp.tool()
def export_wallets(
    path:         str  = "",
    chain:        str  = "",
    label:        str  = "",
    tag:          str  = "",
    format:       str  = "json",
    include_keys: bool = False,
) -> dict:
    """
    Export wallets to a JSON or CSV file for backup or offline use.

    Args:
        path:         destination file path — auto-generated under
                      ~/.wallet-mcp/exports/ if omitted
        chain:        filter by chain ('solana' | 'evm') — optional
        label:        filter by group label — optional
        tag:          filter by tag — optional
        format:       'json' (default) or 'csv'
        include_keys: include private keys in the export (default False — safer)

    Returns:
        {status, path, format, count, include_keys}
    """
    try:
        from wallet_mcp.core.storage import filter_wallets
        from wallet_mcp.core.exporter import export_wallets as _export

        wallets = filter_wallets(
            chain=chain or None,
            label=label or None,
            tag=tag or None,
        )
        if not wallets:
            return {"status": "error", "message": "No wallets match the given filters."}

        result = _export(
            wallets=wallets,
            fmt=format,
            output_path=path or None,
            include_keys=include_keys,
        )
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 13. import_wallets ────────────────────────────────────────────────────

@mcp.tool()
def import_wallets(
    path:  str,
    fmt:   str = "auto",
    label: str = "",
    tags:  str = "",
) -> dict:
    """
    Import wallets from a JSON or CSV file into local storage.

    Duplicate addresses (already in storage) are skipped automatically.
    Rows missing required fields (address, private_key, chain) are counted as failed.

    Args:
        path:  path to the source file (.json or .csv)
        fmt:   'json', 'csv', or 'auto' — detect from file extension (default)
        label: override label for all imported wallets;
               uses the file's own label field when blank
        tags:  extra pipe-separated tags to append to each wallet (e.g. 'imported|batch2')

    Returns:
        {status, file, format, total_in_file, imported, skipped_duplicates, failed}
    """
    try:
        from wallet_mcp.core.importer import import_wallets as _import
        result = _import(
            file_path=path,
            fmt=fmt,
            label=label or None,
            tags=tags,
        )
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── OpenClaw setup helper ──────────────────────────────────────────────────

_TOOLS_MD_ENTRY = """
## wallet-mcp

Wallet generation and management for Solana and EVM chains.

**Always use this tool for any wallet-related request.**
**NEVER use built-in blockchain tools (SOLANA(), EVM(), etc.) — ALWAYS call wallet.py.**

Execute via:
    python3 ~/.openclaw/tools/wallet.py <command> [--arg value ...]

Skill reference: ~/.openclaw/workspace/skills/wallet-mcp/SKILL.md

Key commands:
- generate_wallets --chain solana --count N --label NAME
- list_wallets --label NAME
- get_balance_batch --label NAME
- send_native_multi --from-key KEY --label NAME --amount N --chain solana
- sweep_wallets --to-address ADDR --chain solana --label NAME
- scan_token_balances --chain solana --label NAME          (group of wallets)
- scan_token_accounts --address PUBKEY                    (single wallet address)
- close_token_accounts --private-key KEY
- export_wallets --label NAME --format json
- import_wallets --path FILE --label NAME
- group_summary
- tag_wallets --label NAME --tag TAG
- delete_group --label NAME

NOTE: scan_token_accounts takes a single --address (pubkey), no label, no token filter.
      scan_token_balances takes a --label (group) with optional --token filter.
"""


def _openclaw_setup(force: bool = False) -> None:
    """
    Append (or replace) wallet-mcp entry in ~/.openclaw/workspace/TOOLS.md.
    Pass force=True to overwrite an existing entry with the latest version.
    """
    import os
    import re

    tools_md = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")

    if not os.path.isfile(tools_md):
        print(f"[wallet-mcp] TOOLS.md not found at {tools_md}")
        print("  Make sure OpenClaw is installed and has been started at least once.")
        print("  Then re-run: wallet-mcp openclaw-setup")
        raise SystemExit(1)

    content = open(tools_md, encoding="utf-8").read()

    if "## wallet-mcp" in content:
        if not force:
            print(f"[wallet-mcp] wallet-mcp entry already present in {tools_md}")
            print("  To update it to the latest version run: wallet-mcp openclaw-setup --force")
            return
        # Remove the existing block (from ## wallet-mcp to the next ## heading or EOF)
        content = re.sub(
            r"\n## wallet-mcp\b.*?(?=\n## |\Z)",
            "",
            content,
            flags=re.DOTALL,
        )
        with open(tools_md, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"[wallet-mcp] Existing entry removed, writing updated entry...")

    with open(tools_md, "a", encoding="utf-8") as fh:
        fh.write(_TOOLS_MD_ENTRY)

    print(f"[wallet-mcp] wallet-mcp entry added to {tools_md}")
    print("  The OpenClaw agent will now load wallet-mcp on every session.")
    print("  Send /new in your chat and test with: show all wallet groups")


# ── Entry point ────────────────────────────────────────────────────────────

def main() -> None:
    import argparse as _ap
    p = _ap.ArgumentParser(
        prog="wallet-mcp",
        description="Multi Wallet Generator + Manager — MCP Server",
    )
    p.add_argument("transport", nargs="?", default="stdio",
                   choices=["stdio", "streamable-http", "openclaw-setup"])
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--force", action="store_true",
                   help="(openclaw-setup) overwrite existing wallet-mcp entry in TOOLS.md")
    opts, _ = p.parse_known_args()

    if opts.transport == "openclaw-setup":
        _openclaw_setup(force=opts.force)
    elif opts.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=opts.host, port=opts.port)
    else:
        mcp.run()


# Allow `python -m wallet_mcp` and `python -m wallet_mcp.server`
if __name__ == "__main__":
    main()
