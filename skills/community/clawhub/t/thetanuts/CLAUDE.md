# Thetanuts OpenClaw Skill

## Project Structure
- `SKILL.md` - Agent instruction set (loaded by OpenClaw, 1800 lines)
- `scripts/*.js` - Wallet management scripts (run with `node`)
- `scripts/*.ts` - Trading scripts (run with `npx tsx`)
- `scripts/onboard.sh` - Installs deps at project root AND `~/.openclaw/wdk-mcp/`
- `manifest.json` - ClawHub publishing metadata

## SDK Quirks (@thetanuts-finance/thetanuts-client, ^0.2.4)
- `client.erc20.approve()` returns a TransactionReceipt, NOT TransactionResponse. Do not call `.wait()` on it.
- `client.optionBook.fillOrder()` same — returns receipt, already waited internally.
- r12 settlement is automatic via `notifyTradeSettled`. There is NO zero-arg `BaseOption.payout()` write call — SDK ≥ 0.2.4 throws `INVALID_PARAMS` on the legacy method. Read `client.option.getOptionInfo(addr).settled` for status; use `client.option.calculatePayout(addr, settlementPrice)` (view) for amounts.
- `client.option.reclaimCollateral(optionAddress, ownedOption)` and `client.loan.reclaimCollateral(...)` are now payable — the SDK reads `getReclaimFee(ownedOption)` and forwards as `msg.value`. Don't call the raw contract or you'll forget the fee.
- `client.loan.splitOption(optionAddress, amount)` is payable — SDK reads `getSplitFee()` and forwards as `msg.value`.
- `client.collar` exists but the `CollarLoanCoordinator` is a zero address on Base — write methods throw `NETWORK_UNSUPPORTED` until collar-v12 deploys. Pricing/estimation (`estimateCollar`, `getCapStrikeOptions`) works today.
- `client.optionFactory` lost referral/admin surface in 0.2.4: `getOfferSignature`, `getPendingFees`, `getReferralOwner`, `withdrawFees`, `renounceOwnership`, `transferOwnership` no longer exist.
- `client.vault.trigger()` removed in 0.2.4.
- `RFQBuilderParams.requesterPublicKey?: string` was added — `requestLoan()` auto-resolves it via `client.rfqKeys.getOrCreateKeyPair()`. Only set explicitly for viem/wagmi integrations using `encodeRequestLoan`.
- `validateAddress(addr, field)` now RETURNS the EIP-55 checksummed form (previously returned void). Legacy ignore-return callsites still work.
- `client.erc20.getBalance(token, address)` returns `Promise<bigint>`.
- `client.erc20.getAllowance(token, owner, spender)` returns `Promise<bigint>`.
- Strikes use 8 decimals internally. USDC uses 6, WETH uses 18.
- `OrderWithSignature` has NO root-level `collateralToken` field. Use `order.rawApiData?.collateral` or `order.order?.collateralToken` (both are address strings).
- `Order.strikePrice` is deprecated. Use `order.order.strikes?.[0]` going forward.
- `RFQBuilderParams.requester` is typed `\`0x${string}\``. Cast string addresses with `as \`0x${string}\``.
- `RFQBuilderParams.strikes` is `number | number[]`. The deprecated `strike` field still works but emits a warning — prefer passing `strikes: single` or `strikes: [...]`.
- `optionFactory.encodeRequestForQuotation()` returns `{ to, data }` only — no `value` field. RFQ transactions are value-zero.

## Dependencies
- `@scure/bip39` must be a direct dependency — wallet scripts import it directly, not via WDK.
- Two install targets: project root (for scripts) and `~/.openclaw/wdk-mcp/` (for MCP runtime).

## Repo
- GitHub: `Thetanuts-Finance/thetanuts-openclaw` (canonical; `goheesheng/thetanuts-openclaw` is the legacy fork)
- ClawHub: `clawhub.ai/goheesheng/thetanuts`
- Published with: `clawhub skill publish /absolute/path --slug thetanuts --version X.Y.Z`

## Common Commands
- `node scripts/wallet-create.js` - Create wallet (must have no existing WDK_SEED in .env)
- `npx tsx scripts/fill-order.ts --order-index 0 --collateral 10 --execute --wait` - Fill order (reads `WDK_SEED` env from `.env`)
- `npx tsx scripts/check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry <ts> --direction sell` - Check liquidity
- `bash scripts/onboard.sh` - Full setup (installs both dep targets)
- `bash scripts/update.sh` - Check for manifest-based updates

## Gotchas
- Wallet scripts output JSON to stdout — this is intentional, the agent parses it.
- `onboard.sh` changes directory during execution — use absolute paths when extending.
- SKILL.md is 79KB — large but within OpenClaw limits.
- All trading on Base Mainnet (chain ID 8453). ETH needed for gas, USDC for PUTs, WETH for CALLs.
