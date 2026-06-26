# Tool Reference

## Exported Tools

- `tyrpay_ready`: checks buyer signer and provider reachability.
- `tyrpay_post_task`: creates a task and optionally waits for seller commitment and funds it. **`expectations` is required** unless `createOnly: true`.
- `tyrpay_fund_task`: funds a task that already has a seller commitment. **`expectations` is required.**
- `tyrpay_check_task`: returns the normalized task plus derived and buyer-facing status.
- `tyrpay_list_tasks`: batch status lookup for 1 to 20 task IDs with bounded concurrency.
- `tyrpay_refund_task`: starts a refund on timeout paths.

## Operational Guarantees

- Runtime input validation runs before SDK or ethers calls.
- Validation failures surface as `BuyerSkillToolError` with stable fields:
  `code`, `message`, `field`, `received`, `suggestion`, `retryable`, `causeName`.
- Seller wait timeout after task creation returns a structured result with:
  `taskId`, `taskNonce`, `createTxHash`, `timedOut`, `userStatus`, `userMessage`.
- Manual funding uses a single commitment validation pass.
- Funding calls without `expectations` are rejected at the validation layer.

## Mandatory Expectations

The settlement contract does **not** validate that the seller's commitment matches the buyer's intent.
To prevent funding under unintended terms, the skill layer **requires** `expectations` on every funding path:
- `tyrpay_fund_task` rejects calls that omit `expectations`.
- `tyrpay_post_task` rejects calls that omit `expectations` when `createOnly` is not `true`.

The SDK checks host, path, models, minimum usage, verifier, and deadline **before** locking payment.

## Buyer-Facing Statuses

- `WAITING_FOR_SELLER`
- `READY_TO_FUND`
- `IN_PROGRESS`
- `AWAITING_VERIFICATION`
- `VERIFIED_PASS`
- `VERIFIED_FAIL`
- `COMPLETED`
- `REFUNDED`
- `EXPIRED`
- `REFUND_IN_PROGRESS`

## Environment Configuration

Copy these variables into a `.env` file and fill in the values. buyer-skill does not read environment variables directly — all config is passed through the `BuyerSdk` constructor. These variables are needed to construct the sdk dependencies (signer, provider, storage adapter, etc.) at application startup.

### Settlement Chain & Wallet (required)

| Variable | Description | Example |
|---|---|---|
| `ZERO_G_EVM_RPC` | EVM RPC endpoint for the 0G settlement chain. Used to create the ethers JsonRpcProvider. | `https://evmrpc.0g.ai` |
| `BUYER_PRIVATE_KEY` | Buyer wallet private key (hex, with or without 0x prefix). Used to create the ethers Signer. | |
| `CHAIN_ID` | Settlement chain ID. Must match the network behind `ZERO_G_EVM_RPC`. 16661 = 0G mainnet, 16602 = 0G Galileo testnet. | `16661` |
| `SETTLEMENT_CONTRACT` | Deployed TyrPaySettlement contract address on the settlement chain. Passed as `settlementAddress` to the BuyerSdk constructor. | `0x6D548b2eD427ABeb1564e0A65C5FC8d5A8394ad9` |

### 0G Storage Adapter (production required)

Required when using `ZeroGStorageAdapter` for reading seller commitments. Omit when using `MemoryStorageAdapter` (testing only).

| Variable | Description | Example |
|---|---|---|
| `ZERO_G_INDEXER_RPC` | 0G storage indexer endpoint for reading stored objects. | `https://indexer-storage-turbo.0g.ai` |
| `ZERO_G_STORAGE_PRIVATE_KEY` | Private key used to access 0G storage. Can differ from `BUYER_PRIVATE_KEY`. | |

### Debug / Testing (optional)

| Variable | Description | Example |
|---|---|---|
| `VERIFIER_SERVICE_URL` | Local verifier service URL. | |
