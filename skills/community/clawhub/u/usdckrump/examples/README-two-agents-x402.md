# Two-agent x402 simulation

Two scripts simulate **Agent A (Payer)** and **Agent B (Receiver)** with USDC Krump (USDC.k) and x402 (EIP-3009).

## 1. Direct x402 transfer (no EVVM)

**Script:** `two-agents-x402-direct.ts`  
**Flow:** Agent A signs EIP-3009 and sends USDC.k directly to Agent B via `BridgeUSDC.transferWithAuthorization`. No adapter, no EVVM.

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-direct.ts
# Optional: PAYMENT_AMOUNT=500000  (0.5 USDC.k, 6 decimals)
```

## 2. Full x402 + EVVM (adapter + EVVM Core)

**Script:** `two-agents-x402-simulation.ts`  
**Flow:** Agent A pays via `payViaEVVM` (x402 + EVVM adapter); Agent B verifies with `checkPaymentStatus`. Requires EVVM Core and Bridge EVVM adapter to be deployed and configured.

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_PRIVATE_KEY=0x... npx tsx examples/two-agents-x402-simulation.ts
```

If you see `EVVMPaymentAdapter: EVVM payment failed`, EVVM Core is not set up for this path; use the direct script instead.

## 3. x402 + EVVM Native adapter (no EIP-3009 on token)

**Script:** `two-agents-x402-native.ts`  
**Flow:** Same as (2) but uses **EVVM Native x402 adapter** by default: x402 auth is verified on-chain by the adapter; EVVM Core moves **internal ledger balances** (no token pull in Core). Token does not need EIP-3009.

**Important – EVVM deposit before pay:** In EVVM v3 testnet, `Core.pay()` only moves internal balances; it does not pull tokens from the wallet. The **payer must deposit USDC.k into EVVM first** (approve Treasury, then `Treasury.deposit(USDC.k, amount)`). After that, x402 native adapter’s call to `Core.pay()` will debit the payer’s internal USDC.k balance. Use the script in `lz-bridge/scripts/evvm-deposit-usdck.js` (run with payer’s key):

```bash
# In lz-bridge: deposit USDC.k into EVVM so payer has internal balance for pay()
PRIVATE_KEY=0x<payer_private_key> DEPOSIT_AMOUNT=1000000 npm run evvm:deposit-usdck -- --network storyAeneid
```

Then run the two-agent native script:

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-native.ts
# Optional: PAYMENT_AMOUNT=1000  (0.001 USDC.k), BRIDGE_EVVM_NATIVE_ADAPTER, BRIDGE_USDC_ADDRESS
```

## x402 signer fix

The skill’s `x402-signer.ts` was updated to use **EIP-712 `signTypedData`** instead of `signMessage`, so signatures match BridgeUSDC’s `transferWithAuthorization` verification.
