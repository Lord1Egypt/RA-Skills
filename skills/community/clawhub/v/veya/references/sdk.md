# Custom logic with `@veyanet/sdk`

The MCP server covers the standard flows. When the user needs custom pipelines, their own
validators, local signing, or VEYA inside a backend, point them to the TypeScript SDK.
The MCP itself is built on it, so the capabilities match.

```bash
npm install @veyanet/sdk     # Node.js 20+
```

```ts
import { VeyaClient } from "@veyanet/sdk";

const client = new VeyaClient();                 // Mainnet by default
// const client = new VeyaClient({ network: "testnet" }); 

const ping = await client.pingChain();
const digest = await client.hashBlake3("hello");
const { publicKey, privateKey } = await client.pqKeygen();
const quorum = await client.runConsensus("task-8819", { amount: 250 });
```

| MCP tool | SDK |
|---|---|
| `veya_ping_chain` | `client.pingChain()` |
| `veya_hash_blake3` | `client.hashBlake3(data)` |
| `veya_prove` | `client.proveInput(source, { anchor, environmentId })` |
| `veya_verify_transaction` | `client.verifyTransaction(txHash)` |
| `veya_pq_keygen` / `veya_pq_sign` / `veya_pq_verify` | `client.pqKeygen()`, `pq` helpers |
| `veya_run_consensus` | `client.runConsensus(taskId, payload)` |
| `veya_sealed_execute` | `client.protectedExecute({ … })` |
| `veya_register_pq_onchain` | `client.registerPqOnchain(envType)` |
| write tools | `client.requireEvm()` → `EvmAnchor` (`storeCommitment`, `attestExecution`, `registerEnvironment`, `anchorPqAttestation`) |

Docs: https://github.com/veyanet/veya-sdk
