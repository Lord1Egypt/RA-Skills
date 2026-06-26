# QFC OpenClaw Skill — Roadmap

## v2.1 (Released)

AI inference integration, contract interaction, and OpenClaw best-practice alignment.

---

## Phase 1: OpenClaw Alignment (High Priority) -- DONE

- [x] Add `{baseDir}` reference in SKILL.md for setup/module paths
- [x] Add setup instruction: `Run {baseDir}/scripts/setup.sh before first use`
- [x] Add `openclaw skills add` install method to README

## Phase 2: AI Inference Skill (High Priority) -- DONE

> QFC's biggest differentiator vs ETH/EVM wallet skills

- [x] `QFCInference` class (`src/inference.ts`)
  - [x] `getModels()` — list approved AI models from registry
  - [x] `getStats()` — network-wide inference statistics
  - [x] `submitTask(model, input, maxFee)` — submit a public inference task
  - [x] `getTaskStatus(taskId)` — query task status
  - [x] `waitForResult(taskId, timeout)` — poll until completion
  - [x] `decodeResult(resultData)` — decode base64 result payload
  - [x] `estimateFee(model, inputSize)` — estimate inference cost
- [x] Add inference section to SKILL.md capabilities
- [x] Add `references/ai-compute.md` — AI compute network guide for agents
  - GPU tiers, supported models, task lifecycle
  - Fee estimation, result format
  - Usage examples

## Phase 3: Contract Interaction (Medium Priority) -- DONE

- [x] `QFCContract` class (`src/contract.ts`)
  - [x] `call(address, abi, method, args)` — read contract state
  - [x] `send(address, abi, method, args, value?)` — write transaction
  - [x] `deploy(abi, bytecode, args)` — deploy contract
  - [x] `isContract(address)` — check if address has contract code
  - [x] `getCode(address)` — retrieve raw bytecode
- [x] Add contract section to SKILL.md capabilities
- [x] SecurityPolicy: contract calls already trigger confirmation (existing `isContractCall` flag)

## Phase 4: Reference Docs (Low Priority) -- DONE

- [x] `references/defi-operations.md` — swap, liquidity, staking guide
- [x] `references/governance.md` — model governance, proposals, voting
- [x] `references/error-handling.md` — comprehensive error catalog

## Phase 5: ERC-20 Token Support (Low Priority) -- DONE

- [x] `QFCToken` class (`src/token.ts`)
  - [x] `getTokenInfo(tokenAddress)` — name, symbol, decimals, totalSupply
  - [x] `getBalance(tokenAddress, owner)` — token balance with decimal formatting
  - [x] `transfer(tokenAddress, to, amount)` — send tokens (auto-handles decimals)
  - [x] `approve(tokenAddress, spender, amount)` — approve spender (supports "max")
  - [x] `getAllowance(tokenAddress, owner, spender)` — check allowance
- [x] Add token section to SKILL.md

---

## v2.2 (Planned)

> Token creation & explorer integration — let users deploy ERC-20 tokens on QFC via natural language.

### Phase 6: One-Click Token Deployment (High Priority) -- DONE

- [x] `QFCToken.deploy(name, symbol, initialSupply, signer)` — deploy a new ERC-20 token
  - Embed pre-compiled bytecode (Paris EVM target, no PUSH0) to avoid requiring solc
  - Auto-set gasLimit (800k) to work within QFC block gas limits
  - Raw RPC receipt polling to avoid ethers.js log-parsing issues on QFC
  - Return contract address, tx hash, explorer URL, token info
  - Export `ERC20_SOURCE_CODE` for explorer contract verification
- [x] Add `deploy-token` usage example to SKILL.md and README
  - Natural language trigger: "Create a token called X with symbol Y and supply Z on QFC"
- [x] Add `references/token-deployment.md`
  - Step-by-step guide: create wallet → fund via faucet → deploy token → verify
  - Constructor parameters explained (name, symbol, initialSupply, decimals)
  - Gas cost estimates and testnet vs mainnet considerations
  - Known QFC EVM quirks (Paris EVM target required, eth_call limitations)

### Phase 7: Token Management (Medium Priority) -- DONE

- [x] `QFCToken.mint(tokenAddress, to, amount, signer)` — mint new tokens (if mintable)
- [x] `QFCToken.burn(tokenAddress, amount, signer)` — burn tokens
- [x] Mintable/Burnable token template (`deploy()` with `mintable: true` flag)
  - MintableToken contract: owner, mint(onlyOwner), burn(anyone), transferOwnership
  - Pre-compiled bytecode (Paris EVM, optimizer 200 runs)
  - Exported `MINTABLE_SOURCE_CODE` for explorer verification
- [x] `QFCToken.getDeployedTokens(owner)` — list tokens deployed by an address
  - Uses CREATE address derivation + eth_getCode to find contracts at each nonce

### Phase 8: Explorer Contract Verification (Low Priority) -- DONE

- [x] Explorer: add contract source code verification API (`POST /api/contracts/verify`)
- [x] Explorer: DB migration for `source_code`, `abi`, `compiler_version`, `is_verified` fields
- [x] `QFCContract.verify(address, sourceCode, compilerVersion, evmVersion)` — submit source for verification
- [x] After token deployment, auto-submit source code to explorer for verification
- [x] Verified contracts show source code and ABI on explorer contract page

---

## v2.3 (Current)

> Portfolio & transfer history — let users see all their token holdings and track transfers.

### Phase 9: Token Portfolio (High Priority) -- DONE

- [x] `QFCToken.getPortfolio(owner)` — native QFC balance + all ERC-20 token balances
  - Fetches known token list from explorer `/api/tokens`
  - Queries `balanceOf` for each token in parallel
  - Filters to non-zero balances only
  - Returns native balance + token list with formatted amounts

### Phase 10: Transfer History (High Priority) -- DONE

- [x] `QFCToken.getTransferHistory(tokenAddress, address?, page?, limit?)` — token transfer history
  - Fetches from explorer `/api/tokens/:address` endpoint
  - Optional address filter (sender or receiver)
  - Paginated results with token symbol

---

## v2.4 (Current)

> Batch operations, NFT support, and Discord integration.

### Phase 11: Batch Operations (High Priority) -- DONE

- [x] `QFCToken.batchTransfer(tokenAddress, recipients[], signer)` — airdrop tokens to multiple addresses sequentially
- [x] `QFCWallet.batchSend(recipients[], signer)` — batch native QFC transfers

### Phase 12: NFT Support (Medium Priority) -- DONE

- [x] `QFCNFT` class (`src/nft.ts`)
  - [x] `deploy(name, symbol, signer)` — deploy ERC-721 collection (bytecode TBD, source ready)
  - [x] `mint(contractAddress, to, uri, signer)` — mint NFT with URI
  - [x] `getTokenURI(contractAddress, tokenId)` — get metadata URI
  - [x] `ownerOf(contractAddress, tokenId)` — check NFT owner
  - [x] `balanceOf(contractAddress, owner)` — check NFT balance
  - [x] `transfer(contractAddress, from, to, tokenId, signer)` — transfer NFT
- [x] ERC-721 Solidity source code (`ERC721_SOURCE_CODE`)
- [x] Pre-compiled ERC-721 bytecode (Paris EVM, solc 0.8.34, optimizer 200)
- [x] Auto-verify on explorer after deployment (ready, pending bytecode)

### Phase 13: Discord Bot Integration (Low Priority) -- DONE

- [x] `QFCDiscordBot` class — framework-agnostic command processor
  - [x] `!help` — list available commands
  - [x] `!faucet <address>` — request test QFC
  - [x] `!balance <address>` — check balance
  - [x] `!portfolio <address>` — show token holdings
  - [x] `!tx <hash>` — lookup transaction
  - [x] `!block [number]` — get block info
  - [x] `!price` — gas price
  - [x] `!info` — network info
- [x] Example discord.js integration script (`scripts/discord-bot-example.mjs`)

---

## v2.5 (Planned)

> Advanced features and ecosystem tools.

### Phase 14: NFT Bytecode Compilation -- DONE

- [x] Compile ERC-721 source with solc (Paris EVM, optimizer 200)
- [x] Embed bytecode in `nft.ts`
- [ ] Test deployment on QFC testnet

### Phase 15: Airdrop Smart Contract -- DONE

- [x] Pre-compiled Airdrop contract (Solidity 0.8.34, paris, optimizer 200)
  - `airdrop(token, recipients[], amounts[])` — variable amounts per recipient
  - `airdropFixed(token, recipients[], amount)` — same amount to all (gas savings)
  - Uses `transferFrom` — caller approves contract, then batch-sends in one tx
- [x] `QFCToken.deployAirdrop(signer)` — deploy reusable Airdrop contract
- [x] `QFCToken.airdrop(airdropContract, tokenAddress, recipients[], signer)` — single-tx airdrop
  - Auto-approves airdrop contract if needed
  - Auto-selects `airdropFixed` when all amounts are equal

### Phase 16: Token Swap / DEX -- DONE

- [x] SimpleSwap AMM contract (Solidity 0.8.34, paris, optimizer 200)
  - Constant-product x*y=k with 0.3% swap fee
  - LP tokens (sqrt-based minting, proportional redemption)
  - Slippage protection (minOut parameter)
- [x] `QFCSwap` class (`src/swap.ts`)
  - [x] `deployPool(tokenA, tokenB, signer)` — deploy pair pool
  - [x] `getPoolInfo(poolAddress)` — reserves, prices, LP supply
  - [x] `addLiquidity(poolAddress, amountA, amountB, signer)` — deposit + auto-approve
  - [x] `removeLiquidity(poolAddress, lpAmount, signer)` — burn LP, withdraw tokens
  - [x] `swap(poolAddress, tokenIn, amountIn, signer, slippagePct?)` — execute swap
  - [x] `getQuote(poolAddress, tokenIn, amountIn)` — preview output + price impact
  - [x] `getLPBalance(poolAddress, owner)` — check LP balance
- [x] Auto-verify source code on explorer after deployment
- [x] Exported `SWAP_SOURCE_CODE` for manual verification

---

## v3.0 (Current)

> DeFi infrastructure — wrapped QFC, token launchpad, NFT marketplace, and multi-call.

### Phase 17: Wrapped QFC (WQFC) (High Priority) -- DONE

- [x] WQFC contract (Solidity 0.8.34, paris, optimizer 200)
  - `deposit()` payable — wrap QFC → WQFC
  - `withdraw(amount)` — unwrap WQFC → QFC
  - Standard ERC-20 interface (transfer, approve, etc.)
- [x] `QFCSwap.deployWQFC(signer)` — deploy WQFC contract
- [x] `QFCSwap.wrapQFC(wqfcAddress, amount, signer)` — wrap native QFC into WQFC
- [x] `QFCSwap.unwrapQFC(wqfcAddress, amount, signer)` — unwrap WQFC back to native QFC
- [x] `QFCSwap.swapQFCForToken(poolAddress, wqfcAddress, amountQFC, signer)` — auto-wrap + swap
- [x] `QFCSwap.swapTokenForQFC(poolAddress, wqfcAddress, tokenIn, amountIn, signer)` — swap + auto-unwrap
- [x] Exported `WQFC_SOURCE_CODE` for verification

### Phase 18: Token Launchpad (High Priority) -- DONE

- [x] `QFCToken.launch(name, symbol, supply, liquidityTokenAmount, liquidityQFCAmount, wqfcAddress, signer)`
  - Deploy ERC-20 token (standard or mintable)
  - Wrap QFC → WQFC
  - Deploy WQFC pool
  - Approve + add initial liquidity (token + WQFC)
  - Return token address, pool address, LP details

### Phase 19: NFT Marketplace (Medium Priority) -- DONE

- [x] NFTMarketplace contract (Solidity 0.8.34, paris, optimizer 200)
  - `list(nftContract, tokenId, price)` — list NFT for sale (native QFC)
  - `buy(listingId)` payable — purchase listed NFT (auto-refund excess)
  - `cancel(listingId)` — cancel listing (seller only)
  - `getListing(listingId)` — view listing details
  - `getActiveListingCount()` — count active listings
- [x] `QFCMarketplace` class (`src/marketplace.ts`)
  - [x] `deploy(signer)` — deploy marketplace contract
  - [x] `listNFT(marketplace, nftContract, tokenId, priceQFC, signer)` — auto-approves NFT
  - [x] `buyNFT(marketplace, listingId, signer)` — purchase with QFC
  - [x] `cancelListing(marketplace, listingId, signer)`
  - [x] `getListing(marketplace, listingId)` — single listing
  - [x] `getListings(marketplace)` — all active listings
  - [x] `getListingsByCollection(marketplace, nftContract)` — filter by collection
- [x] Exported `MARKETPLACE_SOURCE_CODE` for verification

### Phase 20: Multi-Call (Low Priority) -- DONE

- [x] Multicall3 contract (Solidity 0.8.34, paris, optimizer 200)
  - `aggregate3(calls[])` — batch staticcall, return results
- [x] `QFCMulticall` class (`src/multicall.ts`)
  - [x] `deploy(signer)` — deploy Multicall3 contract
  - [x] `call(multicallAddress, calls[])` — batch contract reads
  - [x] `getTokenBalances(multicallAddress, tokens[], owner)` — batch balanceOf
  - [x] `getPoolReserves(multicallAddress, pools[])` — batch reserve queries
- [x] Exported `MULTICALL_SOURCE_CODE` for verification

### Phase 21: Event Subscriptions (Low Priority) -- DONE

- [x] `QFCEvents` class (`src/events.ts`)
  - [x] `watchTransfers(tokenAddress, callback)` — ERC-20 Transfer events
  - [x] `watchSwaps(poolAddress, callback)` — Swap events on AMM pool
  - [x] `watchNFTSales(marketplace, callback)` — marketplace Sold events
  - [x] `watchBlocks(callback)` — new block notifications
- [x] Uses polling (QFC doesn't support WebSocket subscriptions yet)
- [x] All watchers return `{ stop() }` for cleanup

---

## Release Criteria

- `npm run build` passes with no errors
- SKILL.md updated with all new capabilities
- All pre-compiled bytecodes use solc 0.8.34, evmVersion: paris, optimizer 200 runs

## Dependencies

- QFC testnet RPC operational (eth_call must support storage reads)
- QFC explorer API `/api/tokens` endpoint operational
- Pre-compiled bytecodes (Solidity 0.8.x, evmVersion: paris)
- Explorer contract verification API
