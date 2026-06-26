"""Pure token filtering and formatting. No I/O."""

from typing import Any, Dict, List


def filter_tokens(tokens: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Return tokens whose name or symbol contains query (case-insensitive)."""
    if not query or not query.strip():
        return list(tokens)
    q = query.strip().lower()
    return [
        t
        for t in tokens
        if q in str(t.get("name", "")).lower() or q in str(t.get("symbol", "")).lower()
    ]


def get_solana_addresses(tokens: List[Dict[str, Any]]) -> List[str]:
    """Extract Solana addresses from tokens."""
    return [t["address"] for t in tokens if t.get("address")]


def format_names(tokens: List[Dict[str, Any]]) -> List[str]:
    """Return one line per token: 'Name [SYMBOL]' or just 'Name' if no symbol."""
    lines: List[str] = []
    for t in tokens:
        name = str(t.get("name", "")).strip()
        symbol = str(t.get("symbol", "")).strip()
        if symbol:
            lines.append(f"{name} [{symbol}]")
        else:
            lines.append(name)
    return lines


def find_token_by_solana_address(
    tokens: List[Dict[str, Any]], address: str
) -> Dict[str, Any]:
    """Return the first token whose address matches. Returns {} if no match."""
    if not address:
        return {}
    for t in tokens:
        if address in str(t.get("address", "")):
            return t
    return {}
