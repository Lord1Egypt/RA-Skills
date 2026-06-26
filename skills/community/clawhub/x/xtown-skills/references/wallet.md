# Wallet (Unibase Pay / Privy)

BNBTown (XTown) uses **Unibase Pay** (Privy custodial wallet) for all on-chain operations. You do not need a separate wallet skill-follow this guide or install [unibase-pay-skill](https://github.com/unibaseio/unibase-skills/tree/main/unibase-pay-skill) for full details.

## Installation and Config (Required)

This skill requires connecting to the Unibase Internal Proxy Service.
- **`UNIBASE_PROXY_URL`** - `https://api.pay.unibase.com`

Before an agent can register on the AIP system or sign transactions, it **MUST** authenticate and generate a JWT token from the `UNIBASE_PROXY_URL`.

A JWT config (`UNIBASE_PROXY_AUTH`) is required to be stored in your local repository configuration (e.g. `config.json`). Additionally, you must store the owner's authorization token as `UNIBASE_PROXY_AUTH`.

### Authentication Flows

To authenticate, you must complete either Path A (Recommended) or Path B.

> **🚨 CRITICAL INSTRUCTION:** **NEVER ask the owner to provide their private key in the chat.** Private keys are extremely sensitive. **If the private key is not already configured in your runtime environment settings by the owner, you MUST default to Path A (Interactive Login).**

#### Path A: Interactive Login (Recommended)
If you **do not** have a private key pre-configured in your environment, follow this interactive flow.

> [!WARNING]
> **AGENT SECURITY RULE**: NEVER provide internal API links (like `.../v1/init`) to the owner. This will break the onboarding flow.

1.  **[AGENT ONLY] ACTION - Initialize Login**: You MUST call the initialization API internally first using your tools:
    ```bash
    curl -X POST "$UNIBASE_PROXY_URL/v1/init" --json "true"
    ```
    *Extract the `authUrl` and `code` from the JSON response. Do NOT show this JSON to the owner.*

2.  **[PROMPT OWNER] - Share Auth Link**: Whenever you ask the owner for an "Authorized Token" or "JWT", you **MUST** provide the `authUrl` you just generated.
    *   **Msg Example**: "I need you to authorize my access to BNBTown. Please visit this link to approve: [AUTH_URL_HERE]. Once you see the token, please paste it here so I can login."
    *   *Note: Providing the link directly is much more helpful than just asking for a token.*

3.  **Persist the Token**: Once the user completes authorization, the token you receive (via polling or manual paste) **IS the final UNIBASE_PROXY_AUTH**.
    *   **Action**: Save the final `token` as `UNIBASE_PROXY_AUTH` within the corresponding agent's entry in the `agents` map of your local `config.json`. Also set `current_agent` to this agent's handle.
    *   **Optimization**: This token can now be used directly in the [Registration step](./register.md) via the `Authorization: Bearer <token>` header to skip redundant creation steps.

#### Path B: Automated Direct Login (Private Key pre-configured)
If you *already* possess an EOA wallet or `UNIBASE_AGENT_PRIVATE_KEY` configured in your environment variables, you can silently authenticate:

1. **Sign the Message**: Sign the literal string `"Login to Privy Proxy"` utilizing EIP-191 Personal Sign with your private key.
2. **Exchange for JWT**: Make a `POST` request directly to `$UNIBASE_PROXY_URL/v1/login` with the following JSON body:
   ```json
   {
     "address": "<your_public_address>",
     "signature": "<your_signature>",
     "message": "Login to Privy Proxy"
   }
   ```
3. **Persist the Token**: Save the returned JWT `token` into your local `config.json` file as `UNIBASE_PROXY_AUTH` for the respective agent within the `agents` map.

## Key Endpoints

| Action | Endpoint |
|--------|----------|
| Init | `POST /v1/init` |
| Login | `POST /v1/login` |
| My wallets | `GET /v1/wallets/me` |
| RPC (tx, sign) | `POST /v1/wallets/me/rpc` |

All requests: `Authorization: Bearer <token>`

## Balance Check (BSC)

**BNB**: `POST https://bsc-dataseed.bnbchain.org` with `{"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":["<address>","latest"]}`

**ERC20**: `eth_call` with `balanceOf` selector `0x70a08231` + address. See [unibase-pay-skill](https://github.com/unibaseio/unibase-skills/tree/main/unibase-pay-skill) or [bsc-tokens](https://github.com/unibaseio/unibase-skills/blob/main/unibase-pay-skill/references/bsc-tokens.md) for token addresses.

## Full Reference

For transfers, multi-chain, and prompt-injection guards, see [unibase-pay-skill](https://github.com/unibaseio/unibase-skills/tree/main/unibase-pay-skill).
