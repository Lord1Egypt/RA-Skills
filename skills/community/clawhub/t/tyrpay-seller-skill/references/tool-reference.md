# Tool Reference

## Exported Tools

- `tyrpay_ready`: checks seller signer reachability and storage adapter configuration.
- `tyrpay_discover_model_endpoint`: given a model, discovers matching reachable TeeTLS/TeeML endpoints and returns host/path/model/providerOptions for the seller workflow.
- `tyrpay_accept_task`: builds execution commitment, uploads it, and submits on-chain.
- `tyrpay_execute_task`: performs a zkTLS-proven API call and returns a delivery receipt.
- `tyrpay_submit_proof`: assembles receipts into a proof bundle and submits on-chain.
- `tyrpay_check_settlement`: returns raw protocol status and seller-facing payout status.

## Operational Guarantees

- Runtime input validation runs before SDK or on-chain calls.
- Validation failures surface as `SellerSkillToolError` with stable fields:
  `code`, `message`, `field`, `received`, `suggestion`, `retryable`, `causeName`.
- `tyrpay_accept_task` reads the on-chain task record to validate task existence before submission.
- `ExecutionCommitment.verifier` is the registry-authorized verifier signer
  address that signs `VerificationReport`; it is not a verifier contract address.
- `tyrpay_execute_task` validates that `request.host`, `request.path`, and `request.method` match the commitment target.
- With provider `"0g-teetls"`, the commitment target/model must be the actual
  0G TeeTLS endpoint/model resolved by the adapter. A commitment to a generic
  upstream endpoint or different model is invalid for TeeTLS execution.
- Use `tyrpay_discover_model_endpoint` before accepting a task when the seller
  only has a target model. Its `recommended.host`, `recommended.path`,
  `recommended.method`, and `recommended.model` are commitment inputs; its
  `recommended.providerOptions` should be forwarded to `tyrpay_execute_task`.
- `tyrpay_submit_proof` verifies storage hash integrity after upload.

## Integration Requirements

- The settlement contract ABI must match the current `TyrPaySettlement.Task`
  struct order: `taskId`, `taskNonce`, `buyer`, `seller`, `token`, `amount`,
  `deadlineMs`, `requiredMinUsage`, `requiredModelsHash`, `commitmentHash`,
  `commitmentURI`, `fundedAtMs`, `proofBundleHash`, `proofBundleURI`,
  `proofSubmittedAtMs`, `reportHash`, `settledAtMs`, `refundedAtMs`, `status`.
- `MemoryStorageAdapter` and `memory://` URIs are valid only for local tests in
  one process. Production or cross-agent flows need persistent retrievable
  storage.
- `commitmentHash` is the canonical hash of the complete
  `ExecutionCommitment`. It cannot be recomputed from task fields alone.
- Reclaim proof generation requires runtime installation of optional Reclaim
  peer dependencies, credentials, and zk resource files.

## Seller-Facing Statuses

- `READY_TO_ACCEPT`: buyer created the task, waiting for seller commitment.
- `WAITING_FOR_BUYER_FUNDING`: commitment submitted, waiting for buyer to lock payment.
- `READY_TO_EXECUTE`: payment locked, seller can execute the task.
- `PROOF_CAPTURED`: execution proof captured, ready to submit.
- `AWAITING_VERIFICATION`: proof submitted, waiting for verifier.
- `PAID`: task settled, payment released to seller.
- `NOT_PAID_REFUNDED`: task refunded to buyer, no seller payout.

## Environment Configuration

Copy these variables into a `.env` file and fill in the values. seller-skill receives all config through constructor parameters; these variables are needed to build those parameters (signer, adapters, contract address, etc.) at application startup.

### Settlement Chain & Wallet (required)

| Variable | Description | Example |
|---|---|---|
| `ZERO_G_EVM_RPC` | EVM RPC endpoint for the 0G settlement chain. Used by ethers provider, 0G storage adapter, and on-chain interactions. | `https://evmrpc.0g.ai` |
| `SELLER_PRIVATE_KEY` | Seller wallet private key (hex, with or without 0x prefix). Used to create the ethers Signer that signs all on-chain transactions. | |
| `CHAIN_ID` | Settlement chain ID. Must match the network behind `ZERO_G_EVM_RPC`. 16661 = 0G mainnet, 16602 = 0G Galileo testnet. | `16661` |
| `SETTLEMENT_CONTRACT` | Deployed TyrPaySettlement contract address on the settlement chain. | `0x6D548b2eD427ABeb1564e0A65C5FC8d5A8394ad9` |

### 0G Storage Adapter (production required)

Required when using `ZeroGStorageAdapter`. Omit when using `MemoryStorageAdapter` (testing only).

| Variable | Description | Example |
|---|---|---|
| `ZERO_G_INDEXER_RPC` | 0G storage indexer endpoint for reading stored objects. | `https://indexer-storage-turbo.0g.ai` |
| `ZERO_G_STORAGE_PRIVATE_KEY` | Private key used to upload proof bundles and receipts to 0G storage. Can differ from `SELLER_PRIVATE_KEY`. | |

### Reclaim zkTLS Adapter (production required)

Required when using `ReclaimZkTlsAdapter`. Omit when using `MockZkTlsAdapter` (testing only).

| Variable | Description | Example |
|---|---|---|
| `RECLAIM_APP_ID` | Reclaim protocol application ID. | |
| `RECLAIM_APP_SECRET` | Reclaim protocol application secret. | |

### Upstream Model API (runtime required)

The model API key / URL are typically passed at call time via `providerOptions`, but many integrations load them from the environment.

| Variable | Description | Example |
|---|---|---|
| `MODEL_API_KEY` | API key for the upstream LLM provider (e.g. OpenAI, DeepSeek). | |
| `MODEL_BASE_URL` | Base URL of the upstream LLM provider. | `https://api.openai.com` |
| `MODEL_NAME` | Model name to use for completions. | `gpt-4o-mini` |

### Verifier (optional)

| Variable | Description | Example |
|---|---|---|
| `VERIFIER_SIGNER_ADDRESS` | Verifier signer address registered on-chain. Passed as `verifierSignerAddress` to `SellerSkillConfig`. | `0x2833BfA9a65D77dC61a0A7d2D74d84E73ca60Ab0` |
| `VERIFIER_CONTRACT` | Deployed verifier contract address (used in some setups). | `0x20Fd439a0BB7F250d7a097Bffe465e8f7D1a97dc` |
| `VERIFIER_SERVICE_URL` | Local verifier service URL. | |

### Debug / Testing (optional)

| Variable | Description | Example |
|---|---|---|
| `tyrpay_E2E_TIMING` | Set to `"1"` to enable end-to-end timing logs in `SellerAgent.provenFetch()`. | |
