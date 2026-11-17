# The Agent Times UCP Gateway Skill

Open agents can recommend products, but safe commerce needs structured identity, confirmation, and handoff. The Agent Times UCP Gateway gives agents a hosted UCP identity registry and provider-neutral Shopping MCP tools for product search, buyer-confirmed carts, and merchant-hosted checkout links — without scraping, provider secrets, or payment handling.

`SKILL.md` is the authoritative runtime guide for agents. This README is human onboarding and package documentation.

ClawHub metadata targets the **MCP Tools** category. Source: <https://github.com/theagenttimes/ucp-gateway-skill>. Homepage: <https://ucpg.ai/>.

## What agents can do

- Publish or reuse a hosted UCP profile with `register_ucp_profile` and use the returned `agent_id`.
- Fetch a hosted profile with `get_ucp_profile`.
- Search and inspect products with `shopping_product_search` and `shopping_product_get`.
- Create, refresh, update, or cancel buyer-confirmed carts.
- Create, refresh, update, or cancel merchant checkout handoff sessions.
- Read `next_step` guidance after every MCP response.

Core tool names:

```text
register_ucp_profile
get_ucp_profile
shopping_product_search
shopping_product_get
shopping_cart_create
shopping_cart_get
shopping_cart_update
shopping_cart_cancel
shopping_checkout_create
shopping_checkout_get
shopping_checkout_update
shopping_checkout_cancel
```

`tools/list` is the authoritative source for schemas, annotations, and descriptions.

## Install

```bash
clawhub install theagenttimes/ucp-gateway-skill
```

The skill is usable from `SKILL.md` alone. Helper scripts are optional deterministic utilities for local key setup, registration, and MCP discovery/calls.

## MCP endpoint

```text
https://ucpg.ai/mcp
```

Use JSON-RPC 2.0 `POST /mcp` for `initialize`, `tools/list`, `tools/call`, `resources/list/read`, and `prompts/list/get`. GET `/mcp` returns a markdown guide/SSE bootstrap; `/messages` and `/mcp/messages` may exist as POST fallbacks.

Legacy `https://ucpgateway.theagenttimes.com/mcp` still works. New integrations should use `https://ucpg.ai/mcp`; existing installs can keep their saved endpoint or override it with `UCP_GATEWAY_MCP_URL`.

Agents should not load every resource at startup. Branch by state: register if no `agent_id`, search if shopping intent is clear, and read focused resources/prompts only when needed.

## Profile publishing and `agent_id`

Every Shopping tool requires an active `agent_id`. Default registration is SKILL.md-friendly: send `agent_name` + `public_key_jwk`; the backend builds the canonical UCP profile and default Shopping capabilities.

- Keep `./.ucpgateway/private_key.jwk` local (`0600` when possible); never pass private key material to MCP.
- Send `./.ucpgateway/public_key.jwk` as `public_key_jwk` with optional namespace/description/public metadata/skill version.
- Save returned `agent_id`, `namespace`, `profile_url`, `registry_url`, `gateway_mcp_url`, `profile_json`, `created`, `existing_profile`, `message`, and local `saved_at` to `./.ucpgateway/agent.json`.
- Same namespace + public key registration is idempotent: `existing_profile: true`, `created: false`, same `agent_id`, hosted profile not modified.

Do not build full `profile_json` for normal registration. Advanced legacy `profile_json` must use exact keys only:

```text
dev.ucp.shopping.catalog.search
dev.ucp.shopping.catalog.lookup
dev.ucp.shopping.catalog
dev.ucp.shopping.cart
dev.ucp.shopping.checkout
```

`shopping` and `dev.ucp.shopping` are invalid shorthand.

## Safe Shopping flow

1. Load/register `agent_id`.
2. Search with `shopping_product_search`.
3. Fetch detail with `shopping_product_get` when variant, merchant, or availability detail is needed.
4. Show provider-returned options only; do not invent prices, availability, URLs, variants, merchant domains, or warnings.
5. Ask buyer/operator to choose variant(s) and quantity.
6. Create/update/cancel cart only after explicit confirmation.
7. Show cart items, totals, messages, warnings, and any `continue_url`.
8. Collect checkout contact/shipping data only from the buyer.
9. Ask final confirmation, then call `shopping_checkout_create` with `operator_confirmed: true`.
10. Hand off merchant `continue_url`; the buyer enters payment on the merchant site.

## Safety boundaries

- No scraping, hidden purchasing, or payment completion claims.
- No card, CVV, bank, wallet, payment token, payment method, password, or one-time payment code fields.
- No invented buyer PII.
- `operator_confirmed: true` is checkout-handoff authorization, not payment authorization.
- `REQUIRES_ESCALATION_*` or `requires_escalation` means the buyer must continue on the merchant-hosted page.

Suggested checkout handoff copy:

> Open this merchant checkout link and enter your payment method there. I cannot see or process payment details. Review merchant totals, shipping, taxes, and terms before paying.

## Optional helper scripts

The helper scripts require Python 3.8+. Use `uv run python` for live gateway calls when possible; direct `python3` also works when the local Python install has current CA certificates.

```bash
git clone https://github.com/theagenttimes/ucp-gateway-skill.git
cd ucp-gateway-skill
```

To validate a checkout before editing or publishing, optionally run:

```bash
uv run python scripts/check_skill.py
uv run python scripts/init_ucpgateway.py --dry-run
uv run python scripts/call_mcp.py --help
```

Normal helper usage does not require npm. Run the Python scripts directly:

```bash
uv run python scripts/init_ucpgateway.py
uv run python scripts/register_profile.py --agent-name "OpenClaw UCP Shopping Agent"
uv run python scripts/call_mcp.py shopping_product_search '{"query":"trail running shoes","limit":5}'
```

Local helper state is written under `./.ucpgateway/`:

```text
private_key.jwk       local only; never upload
public_key.jwk        public key material sent as public_key_jwk
profile.draft.json    optional legacy full-profile draft, not needed for normal registration
agent.json            saved agent_id/profile_url/profile_json after registration
```

### `init_ucpgateway.py`

- Both key files present: reuse the local keypair and verify public coordinates match the private key.
- Both missing: generate `private_key.jwk` and `public_key.jwk`.
- Private-only: derive `public_key.jwk` from the existing private key; never overwrite the private key.
- Public-only: fail unless `--public-only` is passed for agents that manage the private key elsewhere.
- `--force-rotate`: intentionally overwrite both key files with a fresh pair.
- `--dry-run`: non-mutating preview; `--legacy-draft` creates `profile.draft.json` only for advanced legacy profile work.

### `register_profile.py`

Sends `public_key_jwk` to `register_ucp_profile` and writes `agent.json` with `saved_at` plus `created`, `existing_profile`, and `message`. When the gateway reuses an existing profile and local `agent.json` already has the same `agent_id`, local custom fields are preserved while flags and `saved_at` refresh.

### `call_mcp.py`

Discovery modes do not require `agent.json`:

```bash
uv run python scripts/call_mcp.py --initialize
uv run python scripts/call_mcp.py --tools
uv run python scripts/call_mcp.py --tool shopping_product_search
uv run python scripts/call_mcp.py --shopping-tools
uv run python scripts/call_mcp.py --resources
uv run python scripts/call_mcp.py --resource ucp://gateway/skill-runtime-guide
uv run python scripts/call_mcp.py --prompts
uv run python scripts/call_mcp.py --prompt ucp-skill-runtime-guide --prompt-arg shopping_goal='trail running shoes'
```

Tool-call mode injects `agent_id` from `./.ucpgateway/agent.json` for Shopping tools when omitted:

```bash
uv run python scripts/call_mcp.py shopping_product_search '{"query":"trail running shoes","limit":5}'
```

Tool names, descriptions, and input field descriptions come from the live MCP `tools/list` response, not from a hardcoded local schema. Use `--tool <tool_name>` for the exact descriptor before calling search, cart, or checkout tools.

Environment overrides:

```bash
export UCP_GATEWAY_MCP_URL=https://ucpg.ai/mcp
export UCP_NAMESPACE=openclaw
export UCP_AGENT_NAME="OpenClaw UCP Shopping Agent"
```

## Version

Current package version: `0.2.4`.
