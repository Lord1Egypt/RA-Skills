#!/usr/bin/env python3
"""
Web3 Investor MCP Client

Wrapper that calls the MCP server at https://mcp-skills.ai.antalpha.com/mcp
All logic runs on the remote server.

MCP Protocol Flow:
1. POST initialize → get mcp-session-id from response headers
2. POST notifications/initialized → confirm session
3. POST tools/call → actual tool invocation

Usage:
    python3 scripts/mcp_client.py discover --chain ethereum --min-apy 5
    python3 scripts/mcp_client.py analyze --product-id <uuid> --depth detailed
    python3 scripts/mcp_client.py compare --ids <uuid1> <uuid2>
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Any, Optional


MCP_SERVER_URL = "https://mcp-skills.ai.antalpha.com/mcp"


class MCPClient:
    """MCP client with proper session management."""

    def __init__(self, server_url: str = MCP_SERVER_URL):
        self.server_url = server_url
        self.session_id: Optional[str] = None

    def _parse_sse_response(self, response_text: str) -> dict:
        """Parse SSE (Server-Sent Events) response format."""
        for line in response_text.split("\n"):
            if line.startswith("data: ") or line.startswith("data:"):
                data_str = line[5:].strip()
                if data_str and data_str != "[DONE]":
                    return json.loads(data_str)
        return {}

    def initialize(self) -> bool:
        """
        Initialize MCP session.
        Must be called before any tool calls.
        Returns True if successful.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "web3-investor-client",
                    "version": "1.0.0",
                },
            },
            "id": 1,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                # Get session ID from response headers
                self.session_id = response.headers.get("mcp-session-id")

                response_text = response.read().decode("utf-8")
                result = self._parse_sse_response(response_text)

                if "error" in result:
                    print(f"Initialize error: {result['error']}", file=sys.stderr)
                    return False

                # Send initialized notification
                self._send_initialized()
                return True

        except Exception as e:
            print(f"Initialize failed: {e}", file=sys.stderr)
            return False

    def _send_initialized(self) -> None:
        """Send notifications/initialized to complete handshake."""
        if not self.session_id:
            return

        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id,
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=30):
                pass  # Notification doesn't return content
        except Exception:
            pass  # Ignore notification errors

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Call an MCP tool and return the result.
        Auto-initializes session if needed.
        """
        # Auto-initialize if no session
        if not self.session_id:
            if not self.initialize():
                return {"error": "Failed to initialize MCP session"}

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
            "id": 2,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id,
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=120) as response:
                response_text = response.read().decode("utf-8")
                result = self._parse_sse_response(response_text)

                if "error" in result:
                    return {"error": result["error"]}

                return result.get("result", {})

        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"error": f"Connection error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse response: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}


# Global client instance
_client: Optional[MCPClient] = None


def get_client() -> MCPClient:
    """Get or create MCP client instance."""
    global _client
    if _client is None:
        _client = MCPClient()
    return _client


def discover(
    chain: str,
    min_apy: float = 0,
    max_apy: Optional[float] = None,
    stablecoin_only: bool = False,
    limit: int = 5,
    session_id: Optional[str] = None,
    natural_language: Optional[str] = None,
) -> dict[str, Any]:
    """Discover DeFi investment opportunities (investor_discover)."""
    args: dict[str, Any] = {"limit": limit}

    if session_id:
        args["session_id"] = session_id
    if natural_language:
        args["natural_language"] = natural_language

    prefs: dict[str, Any] = {
        "chain": chain,
        "min_apy": min_apy,
    }
    if max_apy is not None:
        prefs["max_apy"] = max_apy
    if stablecoin_only:
        prefs["asset_type"] = "stablecoin"

    args["structured_preferences"] = prefs

    return get_client().call_tool("investor_discover", args)


def analyze(
    product_id: str,
    depth: str = "detailed",
    include_history: bool = True,
) -> dict[str, Any]:
    """Deep analysis of a specific opportunity (investor_analyze)."""
    return get_client().call_tool(
        "investor_analyze",
        {
            "product_id": product_id,
            "analysis_depth": depth,
            "include_history": include_history,
        },
    )


def compare(product_ids: list[str]) -> dict[str, Any]:
    """Compare multiple opportunities (investor_compare)."""
    return get_client().call_tool(
        "investor_compare",
        {
            "product_ids": product_ids,
        },
    )





def format_response(result: dict[str, Any]) -> str:
    """Format raw MCP response for human-readable display."""
    if "error" in result:
        return f"❌ 错误: {result['error']}"

    lines: list[str] = []

    # ── NEEDS_CLARIFICATION (discover gate) ──
    if result.get("structuredContent", {}).get("gate_status") == "NEEDS_CLARIFICATION":
        return _format_clarification(result["structuredContent"])

    # ── analyzer_meta (analyze result) ──
    if "structuredContent" in result and "product" in result["structuredContent"]:
        lines.append(_format_analyze(result["structuredContent"]))
        _append_analysis_meta(result["structuredContent"], lines)
        _append_suggested_actions(result["structuredContent"], lines)
        return "\n".join(lines)

    # ── discover result ──
    if (
        "structuredContent" in result
        and "recommendations" in result["structuredContent"]
    ):
        lines.append(_format_discover(result["structuredContent"]))
        _append_suggested_actions(result["structuredContent"], lines)
        return "\n".join(lines)

    # ── compare result ──
    if "structuredContent" in result and "comparisons" in result["structuredContent"]:
        lines.append(_format_compare(result["structuredContent"]))
        return "\n".join(lines)

    return json.dumps(result, indent=2)


def _format_clarification(sc: dict[str, Any]) -> str:
    """Format NEEDS_CLARIFICATION response."""
    cla = sc.get("clarification", {})
    lines: list[str] = []
    lines.append("❓ 需要澄清意图\n")
    lines.append(f"问题: {cla.get('question', '')}")

    structured_opts = cla.get("structured_options") or []
    if structured_opts:
        lines.append("\n请选择:")
        for opt in structured_opts:
            lines.append(f"  [{opt['id']}] {opt['label']} — {opt['description']}")
    else:
        opts = cla.get("options", [])
        if opts:
            lines.append("\n选项:")
            for o in opts:
                lines.append(f"  • {o}")

    guidance = cla.get("guidance_for_agent", "")
    if guidance:
        lines.append(f"\n提示: {guidance}")

    ctx = cla.get("context", {})
    if ctx:
        we_know = ctx.get("what_we_know", [])
        we_need = ctx.get("what_we_need", [])
        if we_know:
            lines.append(f"\n已收集: {', '.join(we_know)}")
        if we_need:
            lines.append(f"还需:  {', '.join(we_need)}")

    # Show suggested next actions from top-level
    actions = sc.get("suggested_next_actions", [])
    if actions:
        lines.append("\n下一步:")
        for a in sorted(actions, key=lambda x: x.get("priority", 99)):
            lines.append(f"  → {a.get('action', '')}")

    return "\n".join(lines)


def _format_discover(sc: dict[str, Any]) -> str:
    """Format discover result."""
    recs = sc.get("recommendations", [])
    stats = sc.get("search_stats", {})
    lines: list[str] = []
    lines.append(f"📊 发现 {len(recs)} 个投资机会")
    lines.append(
        f"   候选池: {stats.get('total_candidates', 0)} | 通过筛选: {stats.get('total_after_risk_filter', 0)}"
    )

    for i, rec in enumerate(recs, 1):
        name = rec.get("name", rec.get("protocol_name", "Unknown"))
        apy = rec.get("yield", {}).get("apy", 0)
        tvl = rec.get("scale", {}).get("tvl_usd", 0)
        risk = rec.get("risk", {}).get("risk_score", 0)
        tvl_m = f"${tvl / 1e6:.0f}M" if tvl >= 1e6 else f"${tvl / 1e3:.0f}K"
        lines.append(f"\n  {i}. {name}")
        lines.append(f"     APY: {apy:.1f}%  TVL: {tvl_m}  安全评分: {risk}")

        explanation = rec.get("explanation")
        if explanation and explanation.get("summary"):
            lines.append(f"     摘要: {explanation['summary']}")

    return "\n".join(lines)


def _format_analyze(sc: dict[str, Any]) -> str:
    """Format analyze result."""
    product = sc.get("product", {})
    name = product.get("name", product.get("protocol_name", "Unknown"))
    apy = product.get("yield", {}).get("apy", 0)
    lines: list[str] = []
    lines.append(f"🔍 分析: {name}")
    lines.append(f"   APY: {apy:.1f}%")

    llm = sc.get("llm_insights")
    if llm and llm.get("sustainability_assessment"):
        lines.append(f"   可持续性: {llm.get('sustainability_assessment', '')[:120]}")
    if llm and llm.get("risk_narrative"):
        lines.append(f"   风险: {llm['risk_narrative'][:120]}")

    return "\n".join(lines)


def _append_analysis_meta(sc: dict[str, Any], lines: list[str]) -> None:
    """Append analysis_meta transparency info."""
    meta = sc.get("analysis_meta")
    if not meta:
        return

    indicators: list[str] = []
    if meta.get("llm_used"):
        if meta.get("cache_hit"):
            indicators.append("📦 缓存命中")
        else:
            indicators.append("🧠 LLM 深度分析")
    else:
        indicators.append("⚠️ 规则引擎降级")

    if meta.get("fallback_applied"):
        indicators.append("⚠️ 已使用降级方案")

    confidence = meta.get("confidence_note", "")
    error = meta.get("llm_error")
    if error:
        lines.append(f"\n   分析状态: {' | '.join(indicators)}")
        lines.append(f"   注意: {confidence}")
    elif confidence:
        lines.append(f"\n   分析状态: {' | '.join(indicators)}")
        lines.append(f"   注意: {confidence}")


def _append_suggested_actions(sc: dict[str, Any], lines: list[str]) -> None:
    """Append suggested next actions."""
    actions = sc.get("suggested_next_actions", [])
    if not actions:
        return
    lines.append("\n💡 建议下一步:")
    for a in sorted(actions, key=lambda x: x.get("priority", 99)):
        hint = a.get("command_hint", "")
        lines.append(f"  → {a.get('action', '')}{' — ' + hint if hint else ''}")


def _format_compare(sc: dict[str, Any]) -> str:
    """Format compare result."""
    products = sc.get("products", [])
    comps = sc.get("comparisons", [])
    lines: list[str] = []
    names = [p.get("name", p.get("id", "?")) for p in products]
    lines.append(f"⚖️ 对比: {' vs '.join(names)}")

    for c in comps:
        dim = c.get("dimension", "")
        best = c.get("best_performer", "")
        lines.append(f"\n  {dim}:")
        for pid, val in c.get("values", {}).items():
            marker = " ★" if pid == best else ""
            lines.append(f"    {pid}: {val}{marker}")

    rec = sc.get("recommendation", "")
    if rec:
        lines.append(f"\n  推荐: {rec}")

    llm_comp = sc.get("llm_comparison")
    if llm_comp and llm_comp.get("narrative"):
        lines.append(f"\n  LLM 解读: {llm_comp['narrative'][:200]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Web3 Investor MCP Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    discover_parser = subparsers.add_parser("discover", help="Discover opportunities")
    discover_parser.add_argument(
        "--chain",
        default="ethereum",
        help="Blockchain: ethereum, base, arbitrum, optimism",
    )
    discover_parser.add_argument(
        "--min-apy", type=float, default=0, help="Minimum APY percentage"
    )
    discover_parser.add_argument("--max-apy", type=float, help="Maximum APY percentage")
    discover_parser.add_argument(
        "--stablecoin-only", action="store_true", help="Only stablecoin pools"
    )
    discover_parser.add_argument(
        "--limit", type=int, default=5, help="Max results (1-10)"
    )
    discover_parser.add_argument("--session-id", help="Session ID for stored intent")
    discover_parser.add_argument("--natural-language", help="Natural language query")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze opportunity")
    analyze_parser.add_argument(
        "--product-id", required=True, help="Product ID to analyze"
    )
    analyze_parser.add_argument(
        "--depth", choices=["basic", "detailed", "full"], default="detailed"
    )
    analyze_parser.add_argument(
        "--no-history", action="store_true", help="Exclude historical data"
    )

    compare_parser = subparsers.add_parser("compare", help="Compare opportunities")
    compare_parser.add_argument("--ids", nargs="+", required=True, help="Product IDs")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    result = None

    if args.command == "discover":
        result = discover(
            chain=args.chain,
            min_apy=args.min_apy,
            max_apy=args.max_apy,
            stablecoin_only=args.stablecoin_only,
            limit=args.limit,
            session_id=args.session_id,
            natural_language=args.natural_language,
        )
    elif args.command == "analyze":
        result = analyze(
            product_id=args.product_id,
            depth=args.depth,
            include_history=not args.no_history,
        )
    elif args.command == "compare":
        result = compare(product_ids=args.ids)


    if result:
        formatted = format_response(result)
        print(formatted)
    else:
        print(json.dumps({"error": "Unknown command"}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
