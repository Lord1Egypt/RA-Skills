#!/usr/bin/env python3
"""
Zonein MCP API Client — OpenClaw Skill Script

SECURITY MANIFEST:
  Environment variables accessed: ZONEIN_API_KEY (only)
  External endpoints called: https://mcp.zonein.xyz/api/v1/* (only)
  Local files read: ~/.openclaw/openclaw.json (API key fallback only, if ZONEIN_API_KEY env var is not set)
  Local files written: none
  Output sanitization: All API responses are truncated (max 500 chars/field) before output
  Financial gate: --confirm flag required for all financial commands (programmatic, not bypassable via prompt)

Usage:
  python3 scripts/zonein.py <command> [options]

Commands:
  signals          — PM smart money trading signals
  leaderboard      — PM leaderboard (top traders by PnL)
  consensus        — PM consensus positions
  trader <wallet>  — PM trader profile + performance
  pm-top           — PM top traders by smart score
  smart-bettors    — PM smart money bettors (high ROI)
  trader-positions <wallet> — PM trader current positions
  trader-trades <wallet> — PM trader trade history
  perp-signals     — Perp trading signals (HyperLiquid)
  perp-traders     — Perp smart money traders
  perp-top         — Perp top performers by PnL
  perp-categories  — Perp trader categories
  perp-category-stats — Perp category statistics
  perp-coins       — Perp coin distribution
  perp-trader <addr> — Perp trader details
  agents           — List your trading agents
  agent-get <id>   — Get agent details
  agent-create     — Create a new trading agent
  agent-update <id>— Update agent config
  agent-deploy <id>— Deploy agent (validate + enable)
  agent-enable <id>— Enable agent
  agent-disable <id>— Disable agent
  agent-pause <id> — Pause agent
  agent-delete <id>— Delete agent
  agent-stats <id> — Agent performance stats
  agent-trades <id>— Agent trade history
  agent-vault <id> — Agent vault/wallet info
  agent-balance <id>— Live vault balance (Hyperliquid)
  agent-positions <id>— Open positions (live)
  agent-deposit <id>— Get deposit address (USDC on Arbitrum)
  agent-open <id>  — Open a position (manual order)
  agent-close <id> — Close a position
  agent-update-sl-tp <id> — Update stop-loss / take-profit for open position
  agent-orders <id>— Manual order history
  agent-withdraw <id>— Withdraw funds to your wallet
  agent-backtest <id>— Run backtest on agent (streaming)
  agent-backtests <id>— List past backtests for agent
  agent-templates  — Available agent types & config templates
  agent-assets     — Available trading assets
  agent-categories — Smart money categories with stats
  agent-overview <id> — Agent overview (PnL, ROI, win rate) via AgentsArena
  agent-performance <id> — Advanced performance metrics via AgentsArena
  agent-check      — Check pending trade plans across all agents (HITL)
  agent-plans <id> — List trade plans for a specific agent
  agent-plan-detail <id> <plan_id> — Full trade plan with evidence
  agent-plan-action <id> <plan_id> <action> — Approve/reject/edit/paper a plan
  agent-plan-history <id> — Past trade plans (audit trail)
  agent-signal <sym> — Raw composite data for agents (SM + TA + Market)
  dashboard        — AI Dashboard overview (top signals all types)
  dashboard-latest — Latest AI signal snapshots by asset type
  dashboard-asset  — Full detail for single asset (SM + TA + Market)
  derivatives <sym>— Derivatives indicators (OI, funding, L/S, liq)
  fear-greed       — Crypto Fear & Greed Index
  derivatives-pairs <sym> — Per-exchange pair data
  ta <sym>         — Multi-timeframe TA indicators
  ta-single <sym> <ind> — Single TA indicator value
  liquidation-map <coin> — Liquidation price distribution
  telegram-setup-init — Easy Telegram setup (bot_token only)
  telegram-setup   — Full Telegram setup (bot_token + chat_id)
  telegram-config  — View current Telegram notification config
  telegram-disable — Disable Telegram notifications
  status           — Check API key status
"""

import sys
import os
import json
import argparse

try:
    import urllib.request
    import urllib.error
    import urllib.parse
except ImportError:
    pass

API_BASE = "https://mcp.zonein.xyz/api/v1"
CONTENT_JSON = "application/json"
CONFIRM_HELP = "Required: confirms user approved this financial action"

# Max length for any single string field in API responses (defense against oversized payloads)
_MAX_FIELD_LEN = 500


def _sanitize_value(v):
    """Sanitize a single value from API response. Truncates long strings."""
    if isinstance(v, str) and len(v) > _MAX_FIELD_LEN:
        return v[:_MAX_FIELD_LEN] + "…[truncated]"
    return v


def _sanitize(obj):
    """Recursively sanitize API response data. Truncates oversized string fields."""
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(item) for item in obj]
    return _sanitize_value(obj)


def _output(data):
    """Sanitize and print API response as JSON."""
    print(json.dumps(_sanitize(data), indent=2))


def get_api_key():
    """Get ZONEIN_API_KEY from environment."""
    key = os.environ.get("ZONEIN_API_KEY", "")
    if not key:
        # Fallback: read from ~/.openclaw/openclaw.json (documented in SKILL.md)
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    cfg = json.load(f)
                key = (cfg.get("skills", {}).get("entries", {})
                       .get("zonein", {}).get("apiKey", ""))
            except Exception:
                pass
    if not key:
        print(json.dumps({"error": "ZONEIN_API_KEY not set. Get your key at https://app.zonein.xyz/pm"}))
        sys.exit(1)
    return key


def _parse_json_arg(value: str, param_name: str):
    """Parse a JSON string from CLI argument. Exits with clean error on invalid JSON."""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError) as e:
        print(json.dumps({"error": f"Invalid JSON for {param_name}", "detail": str(e)}))
        sys.exit(1)


def _require_confirm(args, action_desc: str):
    """Programmatic confirmation gate for financial commands.
    Refuses to execute unless --confirm is explicitly passed.
    This prevents prompt injection from bypassing user confirmation."""
    if not getattr(args, 'confirm', False):
        print(json.dumps({
            "error": "Confirmation required",
            "detail": f"This is a financial action: {action_desc}. "
                       f"Add --confirm to execute after user has explicitly approved.",
        }))
        sys.exit(1)


def _do_request(path, params=None, method="GET", body=None):
    """Make authenticated request to Zonein API."""
    key = get_api_key()
    url = f"{API_BASE}{path}"
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        if query:
            url = f"{url}?{query}"

    data_bytes = None
    headers = {"X-API-Key": key, "Accept": CONTENT_JSON}
    if body is not None:
        data_bytes = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = CONTENT_JSON

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(raw)
        except Exception:
            err = {"detail": raw}
        print(json.dumps({"error": f"HTTP {e.code}", "detail": err.get("detail", raw)}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def api_request(path, params=None):
    """GET request."""
    return _do_request(path, params=params, method="GET")


def api_post(path, body=None):
    """POST request."""
    return _do_request(path, method="POST", body=body or {})


def api_patch(path, body=None):
    """PATCH request."""
    return _do_request(path, method="PATCH", body=body or {})


def api_delete(path):
    """DELETE request."""
    return _do_request(path, method="DELETE")


def cmd_signals(args):
    """PM smart money trading signals."""
    params = {"limit": args.limit}
    if args.categories:
        params["categories"] = args.categories
    if args.period:
        params["period"] = args.period
    if args.min_wallets:
        params["min_wallets"] = args.min_wallets
    data = api_request("/pm/signals", params)
    _output(data)


def cmd_leaderboard(args):
    """PM leaderboard."""
    params = {
        "period": args.period,
        "category": args.category,
        "limit": args.limit,
    }
    data = api_request("/pm/leaderboard", params)
    _output(data)


def cmd_consensus(args):
    """PM consensus positions."""
    params = {"min_bettors": args.min_bettors}
    data = api_request("/pm/consensus", params)
    _output(data)


def cmd_trader(args):
    """PM trader profile."""
    data = api_request(f"/pm/trader/{args.wallet}")
    _output(data)


def cmd_pm_top(args):
    """PM top traders by smart score."""
    params = {"limit": args.limit}
    if args.min_score:
        params["min_score"] = args.min_score
    data = api_request("/pm/traders/top", params)
    _output(data)


def cmd_smart_bettors(args):
    """PM smart money bettors (high ROI, high trade count)."""
    params = {"limit": args.limit}
    data = api_request("/pm/traders/smart-bettors", params)
    _output(data)


def cmd_trader_positions(args):
    """PM trader current positions."""
    data = api_request(f"/pm/trader/{args.wallet}/positions")
    _output(data)


def cmd_trader_trades(args):
    """PM trader trade history."""
    params = {"limit": args.limit}
    data = api_request(f"/pm/trader/{args.wallet}/trades", params)
    _output(data)


def cmd_perp_signals(args):
    """Perp trading signals."""
    params = {"limit": args.limit}
    if args.min_wallets:
        params["min_wallets"] = args.min_wallets
    if args.min_score:
        params["min_score"] = args.min_score
    data = api_request("/perp/signals", params)
    _output(data)


def cmd_perp_traders(args):
    """Perp smart traders."""
    params = {"limit": args.limit}
    if args.min_score:
        params["min_score"] = args.min_score
    if args.categories:
        params["categories"] = args.categories
    data = api_request("/perp/traders", params)
    _output(data)


def cmd_perp_top(args):
    """Perp top performers."""
    params = {"limit": args.limit, "time_period": args.period}
    data = api_request("/perp/traders/top", params)
    _output(data)


def cmd_perp_categories(args):
    """Perp categories."""
    data = api_request("/perp/categories")
    _output(data)


def cmd_perp_category_stats(args):
    """Perp category stats."""
    data = api_request("/perp/categories/stats")
    _output(data)


def cmd_perp_coins(args):
    """Perp coin distribution."""
    data = api_request("/perp/coins")
    _output(data)


def cmd_perp_trader(args):
    """Perp trader details."""
    data = api_request(f"/perp/trader/{args.address}")
    _output(data)


def cmd_agents(args):
    """List trading agents."""
    data = api_request("/agents/")
    _output(data)


def cmd_agent_get(args):
    """Get agent details."""
    data = api_request(f"/agents/{args.agent_id}")
    _output(data)


def cmd_agent_create(args):
    """Create a new trading agent."""
    body = {"name": args.name, "agent_type": args.type}
    if args.assets:
        body["allowed_assets"] = args.assets.split(",")
    if args.categories:
        body["smart_money_categories"] = args.categories.split(",")
    if args.leverage:
        body["max_leverage"] = args.leverage
    if args.description:
        body["description"] = args.description
    if args.execution_mode:
        body["execution_mode"] = args.execution_mode
    if args.risk_per_trade:
        body.setdefault("risk_profile", {})["risk_per_trade_percent"] = args.risk_per_trade
    if args.max_daily_loss:
        body.setdefault("risk_profile", {})["max_daily_loss"] = args.max_daily_loss
    if args.risk_reward:
        body.setdefault("risk_profile", {})["risk_reward_ratio"] = args.risk_reward
    if args.max_trades_per_day:
        body.setdefault("trading_preferences", {})["max_trades_per_day"] = args.max_trades_per_day
    if args.min_confidence:
        body.setdefault("trading_preferences", {})["min_confidence_threshold"] = args.min_confidence
    if args.min_consensus:
        body.setdefault("trading_preferences", {})["min_smart_money_consensus"] = args.min_consensus
    if args.strength_thresholds:
        body["strength_thresholds"] = _parse_json_arg(args.strength_thresholds, "--strength-thresholds")
    if args.timeframe_weights:
        body["timeframe_weights"] = _parse_json_arg(args.timeframe_weights, "--timeframe-weights")
    if args.signal_weights:
        body["signal_weights"] = _parse_json_arg(args.signal_weights, "--signal-weights")
    if args.trigger_conditions:
        body["trigger_conditions"] = _parse_json_arg(args.trigger_conditions, "--trigger-conditions")
    if args.trading_risk:
        body["trading_risk"] = _parse_json_arg(args.trading_risk, "--trading-risk")
    if args.prompt_config:
        body["prompt_config"] = _parse_json_arg(args.prompt_config, "--prompt-config")
    if args.withdrawal_addresses:
        body["withdrawal_addresses"] = [a.strip() for a in args.withdrawal_addresses.split(",")]
    data = api_post("/agents/", body)
    # Extract and promote critical fields to top level for LLM safety.
    agent_id = (data.get("agent") or {}).get("agent_id", "UNKNOWN")
    vault = data.get("vault") or {}
    deposit_address = vault.get("address", "NONE")
    data["CRITICAL_AGENT_ID"] = agent_id
    data["CRITICAL_DEPOSIT_ADDRESS"] = deposit_address

    # Script-side verification: call deposit-info API to double-confirm address
    # AND fetch enhanced deposit info (payment link, QR, Arbiscan).
    verification = "SKIPPED"
    deposit_info = {}
    if deposit_address and deposit_address != "NONE" and agent_id != "UNKNOWN":
        try:
            verify_data = _do_request(f"/agents/{agent_id}/deposit-info", method="GET")
            verified_address = (verify_data or {}).get("deposit_address", "")
            if verified_address == deposit_address:
                verification = f"VERIFIED_OK — deposit-info confirmed {deposit_address}"
                deposit_info = {
                    "payment_link": verify_data.get("payment_link", ""),
                    "qr_code_url": verify_data.get("qr_code_url", ""),
                    "verify_address_url": verify_data.get("verify_address_url", ""),
                    "chain": verify_data.get("chain", "Arbitrum One"),
                    "token": verify_data.get("token", "USDC"),
                    "safety_warnings": verify_data.get("safety_warnings", []),
                }
            else:
                verification = (
                    f"MISMATCH — create returned {deposit_address} "
                    f"but deposit-info returned {verified_address} — DO NOT USE"
                )
        except Exception:
            verification = f"VERIFY_FAILED — could not reach deposit-info, use with caution: {deposit_address}"

    data["ADDRESS_VERIFICATION"] = verification
    if deposit_info:
        data["DEPOSIT_INFO"] = deposit_info
    data["CRITICAL_NOTICE"] = (
        f"AGENT_ID={agent_id} | DEPOSIT_ADDRESS={deposit_address} | "
        f"VERIFICATION={verification} | "
        "You MUST copy these values EXACTLY from this output. "
        "DO NOT generate or guess agent IDs or wallet addresses from memory. "
        "Use DEPOSIT_INFO.payment_link or qr_code_url for safest deposit."
    )
    _output(data)


def cmd_agent_update(args):
    """Update agent config."""
    body = {}
    if args.name:
        body["name"] = args.name
    if args.description:
        body["description"] = args.description
    if args.assets:
        body["allowed_assets"] = args.assets.split(",")
    if args.categories:
        body["smart_money_categories"] = args.categories.split(",")
    if args.leverage:
        body["max_leverage"] = args.leverage
    if args.execution_mode:
        body["execution_mode"] = args.execution_mode
    if args.prompt_config:
        body["prompt_config"] = _parse_json_arg(args.prompt_config, "--prompt-config")
    if args.trading_strategy:
        body.setdefault("prompt_config", {})["trading_strategy"] = args.trading_strategy
    if args.custom_rules:
        body.setdefault("prompt_config", {})["custom_rules"] = args.custom_rules
    if args.risk_management:
        body.setdefault("prompt_config", {})["risk_management"] = args.risk_management
    if args.trigger_conditions:
        body["trigger_conditions"] = _parse_json_arg(args.trigger_conditions, "--trigger-conditions")
    if args.trading_risk:
        body["trading_risk"] = _parse_json_arg(args.trading_risk, "--trading-risk")
    if args.signal_weights:
        body["signal_weights"] = _parse_json_arg(args.signal_weights, "--signal-weights")
    if args.strength_thresholds:
        body["strength_thresholds"] = _parse_json_arg(args.strength_thresholds, "--strength-thresholds")
    if args.timeframe_weights:
        body["timeframe_weights"] = _parse_json_arg(args.timeframe_weights, "--timeframe-weights")
    if args.withdrawal_addresses:
        body["withdrawal_addresses"] = [a.strip() for a in args.withdrawal_addresses.split(",")]
    if not body:
        print(json.dumps({"error": "No updates provided"}))
        sys.exit(1)
    data = api_patch(f"/agents/{args.agent_id}", body)
    _output(data)


def cmd_agent_deploy(args):
    """Deploy agent — validate + enable."""
    _require_confirm(args, "Deploy and enable agent for live trading")
    data = api_post(f"/agents/{args.agent_id}/deploy", {})
    _output(data)


def cmd_agent_enable(args):
    """Enable agent."""
    _require_confirm(args, "Enable agent for live trading")
    data = api_post(f"/agents/{args.agent_id}/enable", {})
    _output(data)


def cmd_agent_disable(args):
    """Disable agent."""
    data = api_post(f"/agents/{args.agent_id}/disable", {})
    _output(data)


def cmd_agent_pause(args):
    """Pause agent."""
    data = api_post(f"/agents/{args.agent_id}/pause")
    _output(data)


def cmd_agent_delete(args):
    """Delete agent."""
    data = api_delete(f"/agents/{args.agent_id}")
    _output(data)


def cmd_agent_stats(args):
    """Agent performance stats."""
    data = api_request(f"/agents/{args.agent_id}/stats")
    _output(data)


def cmd_agent_trades(args):
    """Agent trade history."""
    params = {"limit": args.limit}
    if getattr(args, 'offset', 0):
        params["offset"] = args.offset
    if getattr(args, 'filter', 'all') != 'all':
        params["filter"] = args.filter
    data = api_request(f"/agents/{args.agent_id}/trades", params)
    _output(data)


def cmd_agent_vault(args):
    """Agent vault/wallet info."""
    data = api_request(f"/agents/{args.agent_id}/vault")
    _output(data)


def cmd_agent_templates(args):
    """Available agent types & config templates."""
    data = api_request("/agents/config/templates")
    _output(data)


def cmd_agent_assets(args):
    """Available trading assets."""
    data = api_request("/agents/config/assets")
    _output(data)


def cmd_agent_categories(args):
    """Smart money categories with stats."""
    data = api_request("/agents/config/categories")
    _output(data)


def cmd_agent_balance(args):
    """Agent vault balance (live from Hyperliquid)."""
    data = api_request(f"/agents/{args.agent_id}/balance")
    _output(data)


def cmd_agent_positions(args):
    """Agent open positions (live from Hyperliquid)."""
    data = api_request(f"/agents/{args.agent_id}/positions")
    _output(data)


def cmd_agent_deposit(args):
    """Get deposit address for funding agent."""
    data = api_request(f"/agents/{args.agent_id}/deposit-info")
    _output(data)


def cmd_agent_fund(args):
    """Bridge USDC from Arbitrum to Hyperliquid."""
    _require_confirm(args, "Bridge USDC from Arbitrum to Hyperliquid")
    data = api_post(f"/agents/{args.agent_id}/fund", {})
    _output(data)


def cmd_agent_open(args):
    """Open a position (manual order via chat)."""
    _require_confirm(args, f"Open {args.direction} {args.coin} position (${args.size})")
    body = {
        "action": "open",
        "coin": args.coin,
        "direction": args.direction,
        "size_usd": args.size,
    }
    if args.leverage:
        body["leverage"] = args.leverage
    if args.stop_loss is not None:
        body["stop_loss"] = args.stop_loss
    if args.take_profit is not None:
        body["take_profit"] = args.take_profit
    if args.order_type and args.order_type != "market":
        body["order_type"] = args.order_type
    if args.limit_price is not None:
        body["limit_price"] = args.limit_price
    data = api_post(f"/agents/{args.agent_id}/orders", body)
    _output(data)


def cmd_agent_close(args):
    """Close a position (manual order via chat)."""
    _require_confirm(args, f"Close {args.coin} position")
    body = {
        "action": "close",
        "coin": args.coin,
    }
    data = api_post(f"/agents/{args.agent_id}/orders", body)
    _output(data)


def cmd_agent_update_sl_tp(args):
    """Update stop-loss and/or take-profit for an existing position."""
    parts = []
    if args.stop_loss is not None:
        parts.append(f"SL=${args.stop_loss}")
    if args.take_profit is not None:
        parts.append(f"TP=${args.take_profit}")
    desc = f"Update {args.coin} {', '.join(parts)}"
    _require_confirm(args, desc)
    body = {"coin": args.coin}
    if args.stop_loss is not None:
        body["stop_loss"] = args.stop_loss
    if args.take_profit is not None:
        body["take_profit"] = args.take_profit
    data = api_post(f"/agents/{args.agent_id}/update-sl-tp", body)
    _output(data)


def cmd_agent_orders(args):
    """Manual order history."""
    params = {"limit": args.limit}
    data = api_request(f"/agents/{args.agent_id}/orders", params)
    _output(data)


def cmd_agent_withdraw(args):
    """Withdraw funds from agent vault."""
    _require_confirm(args, f"Withdraw funds to {args.to}")
    body = {"destination_address": args.to}
    data = api_post(f"/agents/{args.agent_id}/withdraw", body)
    _output(data)


def _process_backtest_msg(msg):
    """Handle a single NDJSON message from backtest stream.
    Returns the report dict on 'complete', None otherwise. Exits on 'error'."""
    t = msg.get("type")
    if t == "status":
        sys.stderr.write(f"  {msg.get('message')}\n")
    elif t == "init":
        sys.stderr.write(f"  Backtest {msg.get('backtest_id')}: {msg.get('total_steps')} steps\n")
    elif t == "trade":
        tr = msg["trade"]
        pnl_s = f" pnl=${tr['pnl']:.2f}" if tr.get("pnl") is not None else ""
        sys.stderr.write(f"  [trade] {tr['action']} @ ${tr['price']:.2f}{pnl_s}\n")
    elif t == "complete":
        return msg["report"]
    elif t == "error":
        print(json.dumps({"error": msg.get("message")}))
        sys.exit(1)
    return None


def _build_backtest_result(backtest_id, dashboard_url, report):
    """Assemble the final backtest JSON output."""
    result = {
        "backtest_id": backtest_id,
        "dashboard_url": f"https://mcp.zonein.xyz{dashboard_url}" if dashboard_url else None,
    }
    if report:
        s = report.get("stats", {})
        result.update({
            "symbol": report.get("symbol"),
            "days": report.get("days"),
            "initial_balance": report.get("initial_balance"),
            "final_balance": report.get("final_balance"),
            "pnl": report.get("pnl"),
            "total_trades": report.get("total_trades"),
            "win_rate": s.get("win_rate"),
            "profit_factor": s.get("profit_factor"),
            "sharpe_ratio": s.get("sharpe_ratio"),
            "max_drawdown": report.get("max_drawdown"),
            "max_consecutive_wins": s.get("max_consecutive_wins"),
            "max_consecutive_losses": s.get("max_consecutive_losses"),
        })
    return result


def cmd_agent_backtest(args):
    """Run a backtest on an agent. Streams NDJSON progress, prints dashboard link."""
    _require_confirm(args, f"Run backtest on {args.agent_id} ({args.symbol}, {args.days}d)")
    key = get_api_key()
    url = f"{API_BASE}/backtest/run"
    body = json.dumps({
        "agent_id": args.agent_id,
        "symbol": args.symbol.upper(),
        "days": args.days,
        "initial_balance": args.initial_balance,
    }).encode("utf-8")
    headers = {
        "X-API-Key": key,
        "Content-Type": CONTENT_JSON,
        "Accept": "application/x-ndjson",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            backtest_id = resp.headers.get("X-Backtest-Id", "")
            dashboard_url = resp.headers.get("X-Dashboard-Url", "")
            last_report = None
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                report = _process_backtest_msg(json.loads(line))
                if report is not None:
                    last_report = report
            _output(_build_backtest_result(backtest_id, dashboard_url, last_report))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(raw)
        except Exception:
            err = {"detail": raw}
        print(json.dumps({"error": f"HTTP {e.code}", "detail": err.get("detail", raw)}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def cmd_agent_backtests(args):
    """List past backtests for an agent."""
    data = api_request(f"/backtest/list/{args.agent_id}", {"limit": args.limit})
    _output(data)


def cmd_agent_overview(args):
    """Agent overview (name, PnL, ROI, win rate, config, status) via AgentsArena."""
    data = api_request(f"/agents/{args.agent_id}/overview")
    _output(data)


def cmd_agent_performance(args):
    """Detailed agent performance + advanced metrics via AgentsArena."""
    data = api_request(f"/agents/{args.agent_id}/performance")
    _output(data)


def cmd_agent_check(args):
    """Check pending trade plans across all agents (HITL)."""
    data = api_request("/agents/plans/pending")
    _output(data)


def cmd_agent_plans(args):
    """List trade plans for a specific agent."""
    params = {"limit": args.limit}
    if args.status:
        params["status"] = args.status
    data = api_request(f"/agents/{args.agent_id}/plans", params)
    _output(data)


def cmd_agent_plan_detail(args):
    """Get full detail for a specific trade plan."""
    data = api_request(f"/agents/{args.agent_id}/plans/{args.plan_id}")
    _output(data)


def cmd_agent_plan_action(args):
    """Act on a pending trade plan (approve/reject/edit/paper)."""
    if args.action in ("approve", "edit"):
        _require_confirm(args, f"{args.action.title()} trade plan {args.plan_id}")
    body = {"action": args.action}
    if args.notes:
        body["notes"] = args.notes
    if args.edits:
        body["edits"] = _parse_json_arg(args.edits, "--edits")
    data = api_post(f"/agents/{args.agent_id}/plans/{args.plan_id}/action", body)
    _output(data)


def cmd_agent_plan_history(args):
    """Past trade plans (approved, rejected, executed, expired)."""
    params = {"status": "all", "limit": args.limit}
    data = api_request(f"/agents/{args.agent_id}/plans", params)
    _output(data)


def cmd_telegram_setup_init(args):
    """Easy Telegram setup: provide bot_token only, then send /start to bot."""
    data = api_post("/telegram/setup-init", {"bot_token": args.bot_token})
    _output(data)


def cmd_telegram_setup(args):
    """Full Telegram setup with bot_token + chat_id."""
    data = api_post("/telegram/setup", {"bot_token": args.bot_token, "chat_id": args.chat_id})
    _output(data)


def cmd_telegram_config(args):
    """View current Telegram notification config."""
    data = api_request("/telegram/config")
    _output(data)


def cmd_telegram_disable(args):
    """Disable Telegram notifications and remove webhook."""
    data = api_delete("/telegram/config")
    _output(data)


def cmd_hip3_dexs(args):
    """List all HIP-3 DEXs."""
    data = api_request("/dashboard/hip3/dexs")
    _output(data)


def cmd_hip3_assets(args):
    """List assets for a HIP-3 DEX."""
    data = api_request(f"/dashboard/hip3/assets/{args.dex}")
    _output(data)


def cmd_agent_signal(args):
    """Raw composite data for trading agents (SM + TA + Market in one call)."""
    params = {}
    if args.categories:
        params["categories"] = args.categories
    sym = args.symbol
    if ":" in sym:
        data = api_request(f"/dashboard/agent-signal/hip3/{sym}", params)
    else:
        data = api_request(f"/dashboard/agent-signal/perp/{sym.upper()}", params)
    _output(data)


def cmd_dashboard(args):
    """AI Dashboard overview — top signals across all asset types."""
    data = api_request("/dashboard/overview")
    _output(data)


def cmd_dashboard_latest(args):
    """Latest AI signal snapshots by asset type."""
    params = {}
    if args.limit:
        params["limit"] = args.limit
    data = api_request(f"/dashboard/latest/{args.type}", params)
    _output(data)


def cmd_dashboard_asset(args):
    """Full detail for a single asset (SM + TA + Market data)."""
    data = api_request(f"/dashboard/asset/{args.type}/{args.symbol.upper()}")
    _output(data)


def cmd_derivatives(args):
    """All derivatives indicators for a coin (OI, funding, L/S ratio, liquidations)."""
    data = api_request(f"/derivatives/indicators/{args.symbol.upper()}")
    _output(data)


def cmd_fear_greed(args):
    """Crypto Fear & Greed Index."""
    data = api_request("/derivatives/fear-greed")
    _output(data)


def cmd_derivatives_pairs(args):
    """Per-exchange pair data (OI, volume, funding, liquidation, price)."""
    data = api_request(f"/derivatives/pairs/{args.symbol.upper()}")
    _output(data)


def cmd_ta(args):
    """Multi-timeframe TA indicators for a symbol."""
    params = {}
    if args.timeframes:
        params["timeframes"] = args.timeframes
    if args.indicators:
        params["indicators"] = args.indicators
    if args.exchange:
        params["exchange"] = args.exchange
    data = api_request(f"/ta/indicators/{args.symbol.upper()}", params)
    _output(data)


def cmd_ta_single(args):
    """Single TA indicator value."""
    params = {"interval": args.interval}
    if args.exchange:
        params["exchange"] = args.exchange
    if args.period:
        params["period"] = args.period
    data = api_request(f"/ta/indicator/{args.symbol.upper()}/{args.indicator}", params)
    _output(data)


def cmd_liquidation_map(args):
    """Liquidation price distribution for a coin."""
    params = {}
    if args.buckets:
        params["buckets"] = args.buckets
    data = api_request(f"/perp/liquidation-map/{args.coin.upper()}", params)
    _output(data)


def cmd_status(args):
    """Check API key status."""
    data = api_request("/auth/api-key/status")
    _output(data)


def main():
    parser = argparse.ArgumentParser(
        description="Zonein Smart Money Intelligence API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- PM Signals ---
    p = sub.add_parser("signals", help="PM smart money trading signals")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--categories", type=str, default=None, help="Comma-separated: POLITICS,CRYPTO,SPORTS")
    p.add_argument("--period", type=str, default="WEEK", help="DAY, WEEK, MONTH, ALL")
    p.add_argument("--min-wallets", type=int, default=None)
    p.set_defaults(func=cmd_signals)

    # --- PM Leaderboard ---
    p = sub.add_parser("leaderboard", help="PM leaderboard")
    p.add_argument("--period", type=str, default="WEEK", help="DAY, WEEK, MONTH, ALL")
    p.add_argument("--category", type=str, default="OVERALL", help="OVERALL, POLITICS, SPORTS, CRYPTO, etc.")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_leaderboard)

    # --- PM Consensus ---
    p = sub.add_parser("consensus", help="PM consensus positions")
    p.add_argument("--min-bettors", type=int, default=3)
    p.set_defaults(func=cmd_consensus)

    # --- PM Trader ---
    p = sub.add_parser("trader", help="PM trader profile by wallet")
    p.add_argument("wallet", type=str)
    p.set_defaults(func=cmd_trader)

    # --- PM Top Traders ---
    p = sub.add_parser("pm-top", help="PM top traders by smart score")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--min-score", type=float, default=None)
    p.set_defaults(func=cmd_pm_top)

    # --- PM Smart Bettors ---
    p = sub.add_parser("smart-bettors", help="PM smart money bettors (high ROI)")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_smart_bettors)

    # --- PM Trader Positions ---
    p = sub.add_parser("trader-positions", help="PM trader current positions")
    p.add_argument("wallet", type=str)
    p.set_defaults(func=cmd_trader_positions)

    # --- PM Trader Trades ---
    p = sub.add_parser("trader-trades", help="PM trader trade history")
    p.add_argument("wallet", type=str)
    p.add_argument("--limit", type=int, default=100)
    p.set_defaults(func=cmd_trader_trades)

    # --- Perp Signals ---
    p = sub.add_parser("perp-signals", help="Perp trading signals")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--min-wallets", type=int, default=None)
    p.add_argument("--min-score", type=float, default=None)
    p.set_defaults(func=cmd_perp_signals)

    # --- Perp Traders ---
    p = sub.add_parser("perp-traders", help="Perp smart traders")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--min-score", type=float, default=None)
    p.add_argument("--categories", type=str, default=None, help="Comma-separated category filter")
    p.set_defaults(func=cmd_perp_traders)

    # --- Perp Top ---
    p = sub.add_parser("perp-top", help="Perp top performers by PnL")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--period", type=str, default="month", help="day, week, month")
    p.set_defaults(func=cmd_perp_top)

    # --- Perp Categories ---
    p = sub.add_parser("perp-categories", help="Perp trader categories")
    p.set_defaults(func=cmd_perp_categories)

    # --- Perp Category Stats ---
    p = sub.add_parser("perp-category-stats", help="Perp category statistics")
    p.set_defaults(func=cmd_perp_category_stats)

    # --- Perp Coins ---
    p = sub.add_parser("perp-coins", help="Perp coin distribution")
    p.set_defaults(func=cmd_perp_coins)

    # --- Perp Trader ---
    p = sub.add_parser("perp-trader", help="Perp trader details by address")
    p.add_argument("address", type=str)
    p.set_defaults(func=cmd_perp_trader)

    # --- Agents ---
    p = sub.add_parser("agents", help="List trading agents")
    p.set_defaults(func=cmd_agents)

    # --- Agent Get ---
    p = sub.add_parser("agent-get", help="Get agent details")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_get)

    # --- Agent Create ---
    p = sub.add_parser("agent-create", help="Create a new trading agent")
    p.add_argument("--name", type=str, required=True, help="Agent name")
    p.add_argument("--type", type=str, default="composite", help="Agent type: composite, momentum_hunter, stable_grower, precision_master, whale_follower, scalping_pro, swing_trader, hip3_whale_follower, hip3_diversified, hip3_conviction")
    p.add_argument("--assets", type=str, default=None, help="Comma-separated: BTC,ETH,SOL,HYPE")
    p.add_argument("--categories", type=str, default=None, help="Comma-separated SM categories")
    p.add_argument("--leverage", type=int, default=None, help="Max leverage (1-20)")
    p.add_argument("--description", type=str, default=None)
    p.add_argument("--risk-per-trade", type=float, default=None, help="Risk per trade %%")
    p.add_argument("--max-daily-loss", type=float, default=None, help="Max daily loss %%")
    p.add_argument("--risk-reward", type=str, default=None, help="Risk:reward ratio e.g. 1:2")
    p.add_argument("--max-trades-per-day", type=int, default=None)
    p.add_argument("--min-confidence", type=float, default=None, help="Min confidence 0-1")
    p.add_argument("--min-consensus", type=float, default=None, help="Min SM consensus 0-1")
    p.add_argument("--strength-thresholds", type=str, default=None, help="JSON: {\"BTC\": {\"min_strength_buy\": 70, \"min_strength_sell\": 65}, ...}")
    p.add_argument("--timeframe-weights", type=str, default=None, help="JSON: {\"24h\": 0.5, \"4h\": 0.35, \"1h\": 0.15}")
    p.add_argument("--execution-mode", type=str, default=None, help="auto (fully automated) or hitl (human-in-the-loop)")
    p.add_argument("--signal-weights", type=str, default=None, help="JSON: {\"sm\":40,\"ta\":35,\"market\":25} (must sum to 100)")
    p.add_argument("--trigger-conditions", type=str, default=None, help="JSON: entry/exit trigger conditions")
    p.add_argument("--trading-risk", type=str, default=None, help="JSON: {max_positions, max_position_size_pct, default_stop_loss_pct, default_take_profit_pct, max_leverage}")
    p.add_argument("--prompt-config", type=str, default=None, help="JSON: {trading_strategy, custom_rules, risk_management}")
    p.add_argument("--withdrawal-addresses", type=str, default=None, help="Comma-separated 0x... addresses for withdrawal whitelist")
    p.set_defaults(func=cmd_agent_create)

    # --- Agent Update ---
    p = sub.add_parser("agent-update", help="Update agent configuration")
    p.add_argument("agent_id", type=str)
    p.add_argument("--name", type=str, default=None)
    p.add_argument("--description", type=str, default=None)
    p.add_argument("--assets", type=str, default=None, help="Comma-separated: BTC,ETH,SOL,HYPE")
    p.add_argument("--categories", type=str, default=None, help="Comma-separated SM categories")
    p.add_argument("--leverage", type=int, default=None)
    p.add_argument("--execution-mode", type=str, default=None, help="auto or hitl")
    p.add_argument("--prompt-config", type=str, default=None, help="JSON: {trading_strategy, custom_rules, risk_management}")
    p.add_argument("--trading-strategy", type=str, default=None, help="Overall trading approach for LLM")
    p.add_argument("--custom-rules", type=str, default=None, help="Specific entry/exit rules for LLM")
    p.add_argument("--risk-management", type=str, default=None, help="Risk management rules for LLM")
    p.add_argument("--trigger-conditions", type=str, default=None, help="JSON: entry/exit trigger conditions")
    p.add_argument("--trading-risk", type=str, default=None, help="JSON: {max_positions, max_position_size_pct, default_stop_loss_pct, default_take_profit_pct, max_leverage}")
    p.add_argument("--signal-weights", type=str, default=None, help="JSON: {\"sm\":40,\"ta\":35,\"market\":25} (must sum to 100)")
    p.add_argument("--strength-thresholds", type=str, default=None, help="JSON: {\"BTC\": {\"min_strength_buy\": 70, ...}}")
    p.add_argument("--timeframe-weights", type=str, default=None, help="JSON: {\"24h\": 0.5, \"4h\": 0.35, \"1h\": 0.15}")
    p.add_argument("--withdrawal-addresses", type=str, default=None, help="Comma-separated 0x... addresses for withdrawal whitelist")
    p.set_defaults(func=cmd_agent_update)

    # --- Agent Deploy ---
    p = sub.add_parser("agent-deploy", help="Deploy agent (validate + enable)")
    p.add_argument("agent_id", type=str)
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_deploy)

    # --- Agent Enable ---
    p = sub.add_parser("agent-enable", help="Enable agent")
    p.add_argument("agent_id", type=str)
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_enable)

    # --- Agent Disable ---
    p = sub.add_parser("agent-disable", help="Disable agent")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_disable)

    # --- Agent Pause ---
    p = sub.add_parser("agent-pause", help="Pause agent")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_pause)

    # --- Agent Delete ---
    p = sub.add_parser("agent-delete", help="Delete agent")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_delete)

    # --- Agent Stats ---
    p = sub.add_parser("agent-stats", help="Agent performance stats")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_stats)

    # --- Agent Overview ---
    p = sub.add_parser("agent-overview", help="Agent overview (PnL, ROI, win rate, config) via AgentsArena")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_overview)

    # --- Agent Performance ---
    p = sub.add_parser("agent-performance", help="Detailed performance + advanced metrics via AgentsArena")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_performance)

    # --- Agent Trades ---
    p = sub.add_parser("agent-trades", help="Agent trade history")
    p.add_argument("agent_id", type=str)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--offset", type=int, default=0, help="Pagination offset")
    p.add_argument("--filter", type=str, default="all", help="Filter: all, wins, losses")
    p.set_defaults(func=cmd_agent_trades)

    # --- Agent Vault ---
    p = sub.add_parser("agent-vault", help="Agent vault/wallet info")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_vault)

    # --- Agent Templates ---
    p = sub.add_parser("agent-templates", help="Available agent types & config templates")
    p.set_defaults(func=cmd_agent_templates)

    # --- Agent Assets ---
    p = sub.add_parser("agent-assets", help="Available trading assets")
    p.set_defaults(func=cmd_agent_assets)

    # --- Agent Categories ---
    p = sub.add_parser("agent-categories", help="Smart money categories with live stats")
    p.set_defaults(func=cmd_agent_categories)

    # --- Agent Balance ---
    p = sub.add_parser("agent-balance", help="Agent vault balance (live from Hyperliquid)")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_balance)

    # --- Agent Positions ---
    p = sub.add_parser("agent-positions", help="Agent open positions (live)")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_positions)

    # --- Agent Deposit ---
    p = sub.add_parser("agent-deposit", help="Get deposit address for funding agent")
    p.add_argument("agent_id", type=str)
    p.set_defaults(func=cmd_agent_deposit)

    # --- Agent Fund (bridge Arb → HL) ---
    p = sub.add_parser("agent-fund", help="Bridge USDC from Arbitrum to Hyperliquid")
    p.add_argument("agent_id", type=str)
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_fund)

    # --- Agent Open (manual order) ---
    p = sub.add_parser("agent-open", help="Open a position (manual order)")
    p.add_argument("agent_id", type=str)
    p.add_argument("--coin", type=str, required=True, help="BTC, ETH, SOL, HYPE, or HIP-3 dex:COIN (e.g. xyz:TSLA)")
    p.add_argument("--direction", type=str, default="LONG", help="LONG or SHORT")
    p.add_argument("--size", type=float, required=True, help="Position size in USD")
    p.add_argument("--leverage", type=int, default=None, help="Leverage (1-20)")
    p.add_argument("--stop-loss", type=float, default=None, help="Stop loss price")
    p.add_argument("--take-profit", type=float, default=None, help="Take profit price")
    p.add_argument("--order-type", type=str, default="market", help="market or limit")
    p.add_argument("--limit-price", type=float, default=None, help="Limit price (for limit orders)")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_open)

    # --- Agent Close (manual order) ---
    p = sub.add_parser("agent-close", help="Close a position")
    p.add_argument("agent_id", type=str)
    p.add_argument("--coin", type=str, required=True, help="BTC, ETH, SOL, HYPE, or HIP-3 dex:COIN (e.g. xyz:TSLA)")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_close)

    # --- Agent Update SL/TP ---
    p = sub.add_parser("agent-update-sl-tp", help="Update stop-loss / take-profit for open position")
    p.add_argument("agent_id", type=str)
    p.add_argument("--coin", type=str, required=True, help="BTC, ETH, SOL, HYPE, or HIP-3 dex:COIN (e.g. xyz:TSLA)")
    p.add_argument("--stop-loss", type=float, default=None, help="New stop-loss price")
    p.add_argument("--take-profit", type=float, default=None, help="New take-profit price")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_update_sl_tp)

    # --- Agent Orders ---
    p = sub.add_parser("agent-orders", help="Manual order history")
    p.add_argument("agent_id", type=str)
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_agent_orders)

    # --- Agent Withdraw ---
    p = sub.add_parser("agent-withdraw", help="Withdraw funds from agent vault")
    p.add_argument("agent_id", type=str)
    p.add_argument("--to", type=str, required=True, help="Destination 0x... wallet address")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_withdraw)

    # --- Agent Backtest ---
    p = sub.add_parser("agent-backtest", help="Run backtest on agent (streaming)")
    p.add_argument("agent_id", type=str)
    p.add_argument("--symbol", type=str, default="BTC", help="Coin: BTC, ETH, SOL, HYPE")
    p.add_argument("--days", type=int, default=30, help="Period in days (7-90)")
    p.add_argument("--initial-balance", type=float, default=10000, help="Starting balance USD")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_backtest)

    # --- Agent Backtests (list) ---
    p = sub.add_parser("agent-backtests", help="List past backtests for agent")
    p.add_argument("agent_id", type=str)
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_agent_backtests)

    # --- Agent Check (HITL — all pending plans) ---
    p = sub.add_parser("agent-check", help="Check pending trade plans across all agents (HITL)")
    p.set_defaults(func=cmd_agent_check)

    # --- Agent Plans ---
    p = sub.add_parser("agent-plans", help="List trade plans for a specific agent")
    p.add_argument("agent_id", type=str)
    p.add_argument("--status", type=str, default=None, help="Filter: pending, approved, rejected, expired, all")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_agent_plans)

    # --- Agent Plan Detail ---
    p = sub.add_parser("agent-plan-detail", help="Get full trade plan with evidence")
    p.add_argument("agent_id", type=str)
    p.add_argument("plan_id", type=str)
    p.set_defaults(func=cmd_agent_plan_detail)

    # --- Agent Plan Action (approve/reject/edit/paper) ---
    p = sub.add_parser("agent-plan-action", help="Act on a pending trade plan")
    p.add_argument("agent_id", type=str)
    p.add_argument("plan_id", type=str)
    p.add_argument("action", type=str, help="approve, reject, edit, paper")
    p.add_argument("--notes", type=str, default=None, help="User reasoning for the action")
    p.add_argument("--edits", type=str, default=None, help="JSON: {entry, stop_loss, take_profit, size_usd, leverage}")
    p.add_argument("--confirm", action="store_true", help=CONFIRM_HELP)
    p.set_defaults(func=cmd_agent_plan_action)

    # --- Agent Plan History ---
    p = sub.add_parser("agent-plan-history", help="Past trade plans (approved, rejected, executed, expired)")
    p.add_argument("agent_id", type=str)
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_agent_plan_history)

    # --- Telegram Setup Init ---
    p = sub.add_parser("telegram-setup-init", help="Easy Telegram setup (bot_token only, then send /start)")
    p.add_argument("--bot-token", type=str, required=True, help="Telegram bot token from @BotFather")
    p.set_defaults(func=cmd_telegram_setup_init)

    # --- Telegram Setup ---
    p = sub.add_parser("telegram-setup", help="Full Telegram setup with bot_token + chat_id")
    p.add_argument("--bot-token", type=str, required=True, help="Telegram bot token from @BotFather")
    p.add_argument("--chat-id", type=str, required=True, help="Your Telegram chat ID")
    p.set_defaults(func=cmd_telegram_setup)

    # --- Telegram Config ---
    p = sub.add_parser("telegram-config", help="View current Telegram notification config")
    p.set_defaults(func=cmd_telegram_config)

    # --- Telegram Disable ---
    p = sub.add_parser("telegram-disable", help="Disable Telegram notifications + remove webhook")
    p.set_defaults(func=cmd_telegram_disable)

    # --- HIP-3 DEXs ---
    p = sub.add_parser("hip3-dexs", help="List all HIP-3 DEXs")
    p.set_defaults(func=cmd_hip3_dexs)

    # --- HIP-3 Assets ---
    p = sub.add_parser("hip3-assets", help="List assets for a HIP-3 DEX")
    p.add_argument("dex", type=str, help="DEX name: xyz, flx, vntl, hyna, km, cash")
    p.set_defaults(func=cmd_hip3_assets)

    # --- Agent Signal (raw composite data) ---
    p = sub.add_parser("agent-signal", help="Raw composite data for trading agents (SM + TA + Market)")
    p.add_argument("symbol", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.add_argument("--categories", type=str, default=None, help="Comma-separated SM wallet categories to filter")
    p.set_defaults(func=cmd_agent_signal)

    # --- Dashboard Overview ---
    p = sub.add_parser("dashboard", help="AI Dashboard overview — top signals across all asset types")
    p.set_defaults(func=cmd_dashboard)

    # --- Dashboard Latest ---
    p = sub.add_parser("dashboard-latest", help="Latest AI signal snapshots by asset type")
    p.add_argument("type", type=str, help="Asset type: perp, spot, pm, hip3")
    p.add_argument("--limit", type=int, default=None, help="Max snapshots to return")
    p.set_defaults(func=cmd_dashboard_latest)

    # --- Dashboard Asset Detail ---
    p = sub.add_parser("dashboard-asset", help="Full detail for a single asset (SM + TA + Market)")
    p.add_argument("type", type=str, help="Asset type: perp, spot, pm, hip3")
    p.add_argument("symbol", type=str, help="Asset symbol (e.g. BTC, ETH, SOL)")
    p.set_defaults(func=cmd_dashboard_asset)

    # --- Derivatives Indicators ---
    p = sub.add_parser("derivatives", help="All derivatives indicators for a coin (OI, funding, L/S ratio, liq)")
    p.add_argument("symbol", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.set_defaults(func=cmd_derivatives)

    # --- Fear & Greed ---
    p = sub.add_parser("fear-greed", help="Crypto Fear & Greed Index")
    p.set_defaults(func=cmd_fear_greed)

    # --- Derivatives Pairs ---
    p = sub.add_parser("derivatives-pairs", help="Per-exchange pair data (OI, volume, funding, liq, price)")
    p.add_argument("symbol", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.set_defaults(func=cmd_derivatives_pairs)

    # --- TA Multi-timeframe ---
    p = sub.add_parser("ta", help="Multi-timeframe TA indicators (RSI, MACD, BB, etc.)")
    p.add_argument("symbol", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.add_argument("--timeframes", type=str, default=None, help="Comma-separated: 15m,4h,1d")
    p.add_argument("--indicators", type=str, default=None, help="Comma-separated: rsi,macd,bbands")
    p.add_argument("--exchange", type=str, default=None, help="Exchange name (default: binancefutures)")
    p.set_defaults(func=cmd_ta)

    # --- TA Single Indicator ---
    p = sub.add_parser("ta-single", help="Single TA indicator value")
    p.add_argument("symbol", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.add_argument("indicator", type=str, help="Indicator name: rsi, macd, bbands, sma, ema, etc.")
    p.add_argument("--interval", type=str, default="4h", help="Timeframe: 15m, 1h, 4h, 1d")
    p.add_argument("--exchange", type=str, default=None, help="Exchange name")
    p.add_argument("--period", type=int, default=None, help="Period parameter (e.g. 14 for RSI)")
    p.set_defaults(func=cmd_ta_single)

    # --- Liquidation Map ---
    p = sub.add_parser("liquidation-map", help="Liquidation price distribution for a coin")
    p.add_argument("coin", type=str, help="Coin symbol: BTC, ETH, SOL, etc.")
    p.add_argument("--buckets", type=int, default=None, help="Number of price buckets (10-100, default 40)")
    p.set_defaults(func=cmd_liquidation_map)

    # --- Status ---
    p = sub.add_parser("status", help="Check API key status")
    p.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
