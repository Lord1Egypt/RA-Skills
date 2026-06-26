# QFC OpenClaw Skill

AI agent skill for QFC blockchain interaction. Published on [ClawHub](https://clawhub.ai/lai3d/qfc).

## Tech Stack

- **Language**: TypeScript (ES modules, `"type": "module"`)
- **Runtime**: Node.js >= 18
- **Blockchain lib**: ethers.js v6
- **Build**: `tsc` → `dist/`
- **Package manager**: npm

## Project Structure

```
src/
  index.ts          — barrel exports
  provider.ts       — shared RPC provider, network config
  wallet.ts         — QFCWallet: create, import, balance, send, sign
  keystore.ts       — QFCKeystore: encrypted wallet persistence (scrypt)
  security.ts       — SecurityPolicy: pre-transaction safety checks
  faucet.ts         — QFCFaucet: testnet token requests
  chain.ts          — QFCChain: block, tx, receipt queries
  network.ts        — QFCNetwork: node info, network status
  staking.ts        — QFCStaking: validators, stake, scores
  epoch.ts          — QFCEpoch: epoch & finality
  inference.ts      — QFCInference: AI inference tasks
  agent-wallet.ts   — AgentWalletClient: session-key-aware agent operations
  contract.ts       — QFCContract: read/write/deploy/verify contracts
  token.ts          — QFCToken: ERC-20 deploy/transfer/mint/burn/airdrop
  swap.ts           — QFCSwap: AMM token swap + WQFC wrapper
  marketplace.ts    — QFCMarketplace: NFT marketplace (list/buy/sell)
  multicall.ts      — QFCMulticall: batch contract reads
  events.ts         — QFCEvents: event subscriptions via polling
config/
  qfc-networks.json — RPC endpoints, chain IDs, explorer URLs
references/         — markdown guides for agents (wallet ops, token deployment, etc.)
scripts/
  setup.sh          — npm install + tsc build
SKILL.md            — OpenClaw skill manifest (capabilities, security rules, examples)
ROADMAP.md          — feature roadmap with phase tracking
```

## QFC Chain Quirks (IMPORTANT)

1. **No PUSH0**: QFC EVM does not support the PUSH0 opcode (Shanghai). All Solidity must be compiled with `evmVersion: "paris"`. Contracts compiled with default Shanghai target will deploy but all calls return `0x`.

2. **eth_call returns 0x**: View function calls on contracts compiled with Shanghai bytecode silently fail (return `0x` instead of reverting). This is the symptom of the PUSH0 issue above.

3. **RPC log fields**: QFC RPC returns `null` for `transactionIndex`, `blockNumber`, etc. in log entries. This causes ethers.js `BAD_DATA` errors when using `tx.wait()`. Workaround: use raw RPC `eth_getTransactionReceipt` polling (see `waitForReceipt()` in `token.ts`).

4. **Gas estimation overshoot**: ethers.js may estimate gas above QFC's 30M block gas limit. Set explicit `gasLimit` (e.g., 800,000 for ERC-20 deploy).

5. **Network config**: Testnet chain ID 9000, Mainnet chain ID 9001. Default to testnet unless user explicitly requests mainnet.

## Token Deployment

Pre-compiled bytecodes are embedded in `token.ts` (no solc dependency needed):
- `ERC20_DEPLOY_BYTECODE` — standard fixed-supply ERC-20 (Solidity 0.8.34, paris, optimizer 200)
- `MINTABLE_DEPLOY_BYTECODE` — mintable/burnable with owner (same compiler settings)
- Source code exported as `ERC20_SOURCE_CODE` and `MINTABLE_SOURCE_CODE` for explorer verification

After deployment, `QFCToken.deploy()` auto-submits source code to the explorer's `POST /api/contracts/verify` endpoint (best-effort).

## Contract Verification

`QFCContract.verify()` calls the QFC explorer API:
- Endpoint: `{explorerUrl}/api/contracts/verify`
- Method: POST with `{ address, sourceCode, compilerVersion, evmVersion, optimizationRuns, constructorArgs }`
- Explorer compiles source with solc, strips CBOR metadata, compares against deployed bytecode
- See `qfc-explorer` repo for the server-side implementation

## Build & Release

```bash
npm run build          # tsc → dist/
npm run dev            # tsc --watch
```

## Publishing to ClawHub

Install: `npm install -g clawhub`

```bash
# Login first (opens browser, one-time)
clawhub login

# Verify auth
clawhub whoami

# Publish — version should match package.json
clawhub publish . --slug qfc --version X.Y.Z --changelog "..."

# Users install/update with:
clawhub install qfc
clawhub update qfc
```

### acceptLicenseTerms workaround

ClawHub registry (as of 2026-03) requires `acceptLicenseTerms: true` in the
publish payload, but the CLI (v0.6–v0.7) doesn't send it. If you get:

```
Error: Publish payload: acceptLicenseTerms: invalid value
```

Patch `$(npm root -g)/clawhub/dist/cli/commands/publish.js` — find the
`form.set('payload', JSON.stringify({` block and add `acceptLicenseTerms: true`
to the object.

### Full release checklist

1. Bump version in `package.json`
2. `npm run build` — verify no errors
3. `git add . && git commit && git push`
4. `gh release create vX.Y.Z --title "vX.Y.Z — Title" --notes "..."`
5. `clawhub publish . --slug qfc --version X.Y.Z --changelog "..."`

## Conventions

- All classes take `network: NetworkName = 'testnet'` as constructor param
- Use `ethers.parseEther()` for human-readable amounts → wei conversion
- Explorer URLs: `/contract/{address}` for contracts, `/txs/{hash}` for transactions
- Security: never expose private keys in output, confirm large transfers, validate addresses
