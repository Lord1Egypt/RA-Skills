---
name: quantplay
version: 1.0.1
description: >
  Read a user's Indian broker accounts through Quantplay: positions, holdings, orders,
  margins, P&L history, option chains, expiries and live market data, across 10+ brokers
  (Zerodha, Upstox, Angel One, Kotak, Finvasia and more) from one connection.
when_to_use: >
  Use when the user asks about their portfolio, holdings, positions, open orders, margins,
  today's or historical P&L, an option chain, expiries, live prices, or wants analysis
  across their broker accounts on Indian markets (NSE, BSE, NFO).
---

# Quantplay

Quantplay connects you to the user's broker accounts. This skill says how to use it well.

## Connect

The tools come from the Quantplay MCP server, `https://mcp.quantplay.tech/mcp/readonly`. It uses OAuth: on first use the
user signs in to Quantplay in their browser and approves you. There is no key to paste.

This listing is **read-only**. If the user asks you to place, modify, cancel or square off
an order, say that this connector can't, and that trading needs the full Quantplay
connector (`https://mcp.quantplay.tech/mcp`) added as a custom connector, with trading allowed when they approve it.

## Always

- **Start with `get_accounts`.** Accounts are named by nickname, and every other call
  needs one. Never assume which brokers or accounts the user has.
- **Read before you answer.** Quote numbers from tool results, never from memory, and say
  which account and when.
- **A price of 0, or one you can't date, is not a live price.** Some brokers return 0.00 or
  the previous close instead of an error. Say so rather than computing on it.
- **Money is INR.** Format lakhs and crores the Indian way when the user does.
- **Disconnected accounts.** If an account's session has expired, the user must log in to
  the broker again in Quantplay; you can't fix it from here.

## Useful patterns

| The user asks | Do |
|---|---|
| "How am I doing today?" | `get_accounts`, then `get_live_pnl` / `get_positions` per account |
| "Review my portfolio" | `get_holdings`, then group by sector and flag concentration |
| "What's my option exposure?" | `get_positions`, identify each strategy, and net long or short premium |
| "Show NIFTY's chain" | `get_expiry_date_list`, then `get_option_chain` for the nearest expiry |
| "Am I close to a margin call?" | `get_margins`, compared with open positions |

## Risk limits

Each broker account can have a stoploss, target and kill switch set in Quantplay. They are
account-level and Quantplay auto-exits positions when one is breached. `get_accounts`
returns each account's `stoploss`, `target` and `rms_settings`; this listing can't change them.
