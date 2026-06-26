"use strict";
/**
 * Token data fetching
 *
 * Read-only functions for querying token state from Solana.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchTokenRaw = exports.getTreasuryState = exports.getProtocolTreasuryState = exports.getUserStats = exports.getVaultWalletLink = exports.getVaultForWallet = exports.getVault = exports.getAllLoanPositions = exports.getShortPosition = exports.getLoanPosition = exports.getLendingInfo = exports.getMessages = exports.getHolders = exports.getToken = exports.getTokenMetadata = exports.getTokens = void 0;
const web3_js_1 = require("@solana/web3.js");
const anchor_1 = require("@coral-xyz/anchor");
const spl_token_1 = require("@solana/spl-token");
const program_1 = require("./program");
const constants_1 = require("./constants");
const torch_market_json_1 = __importDefault(require("./torch_market.json"));
const getTokenStatus = (bc) => {
    if (bc.reclaimed)
        return 'reclaimed';
    if (bc.migrated)
        return 'migrated';
    if (bc.bonding_complete)
        return 'complete';
    return 'bonding';
};
const fetchAllRawTokens = async (connection) => {
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const accounts = await connection.getProgramAccounts(constants_1.PROGRAM_ID, {
        filters: [{ memcmp: { offset: 0, bytes: '4y6pru6YvC7' } }],
    });
    const tokens = [];
    for (const acc of accounts) {
        try {
            const decoded = coder.accounts.decode('BondingCurve', acc.account.data);
            const mintStr = decoded.mint.toString();
            if (constants_1.BLACKLISTED_MINTS.includes(mintStr))
                continue;
            tokens.push({
                mint: mintStr,
                bondingCurve: decoded,
            });
        }
        catch {
            // Not a bonding curve account
        }
    }
    return tokens;
};
const toTokenSummary = (raw) => {
    const bc = raw.bondingCurve;
    const virtualSol = BigInt(bc.virtual_sol_reserves.toString());
    const virtualTokens = BigInt(bc.virtual_token_reserves.toString());
    const realSol = BigInt(bc.real_sol_reserves.toString());
    const realTokens = BigInt(bc.real_token_reserves.toString());
    const price = (0, program_1.calculatePrice)(virtualSol, virtualTokens);
    const priceInSol = (price * constants_1.TOKEN_MULTIPLIER) / constants_1.LAMPORTS_PER_SOL;
    // Market cap = fully diluted (total supply × price), matching pump.fun convention
    const marketCapSol = (priceInSol * Number(constants_1.TOTAL_SUPPLY)) / constants_1.TOKEN_MULTIPLIER;
    return {
        mint: raw.mint,
        name: (0, program_1.decodeString)(bc.name),
        symbol: (0, program_1.decodeString)(bc.symbol),
        status: getTokenStatus(bc),
        price_sol: priceInSol,
        market_cap_sol: marketCapSol,
        progress_percent: (0, program_1.calculateBondingProgress)(realSol),
        holders: null,
        created_at: 0,
        last_activity_at: Number(bc.last_activity_slot.toString()),
    };
};
const filterAndSort = (tokens, params) => {
    let filtered = [...tokens];
    if (params.status && params.status !== 'all') {
        filtered = filtered.filter((t) => getTokenStatus(t.bondingCurve) === params.status);
    }
    switch (params.sort) {
        case 'marketcap':
        case 'volume':
            filtered.sort((a, b) => {
                const aR = BigInt(a.bondingCurve.real_sol_reserves.toString());
                const bR = BigInt(b.bondingCurve.real_sol_reserves.toString());
                return bR > aR ? 1 : bR < aR ? -1 : 0;
            });
            break;
        case 'newest':
        default:
            filtered.sort((a, b) => {
                const aA = BigInt(a.bondingCurve.last_activity_slot.toString());
                const bA = BigInt(b.bondingCurve.last_activity_slot.toString());
                return bA > aA ? 1 : bA < aA ? -1 : 0;
            });
            break;
    }
    if (params.limit || params.offset) {
        const offset = params.offset || 0;
        const limit = params.limit || filtered.length;
        return filtered.slice(offset, offset + limit);
    }
    return filtered;
};
const buildTokenDetail = (mint, bc, treasury, metadata, holdersCount, solPriceUsd, saidVerification, warnings, poolPrice) => {
    const virtualSol = BigInt(bc.virtual_sol_reserves.toString());
    const virtualTokens = BigInt(bc.virtual_token_reserves.toString());
    const realSol = BigInt(bc.real_sol_reserves.toString());
    const realTokens = BigInt(bc.real_token_reserves.toString());
    const burned = BigInt(bc.permanently_burned_tokens?.toString() || '0');
    let priceInSol;
    let marketCapSol;
    if (bc.migrated && poolPrice && poolPrice.tokenReserves > 0) {
        // Use live Raydium pool price for migrated tokens
        // solReserves is in lamports, tokenReserves is in base units (10^6)
        priceInSol =
            (poolPrice.solReserves * constants_1.TOKEN_MULTIPLIER) / (poolPrice.tokenReserves * constants_1.LAMPORTS_PER_SOL);
    }
    else {
        // Use bonding curve virtual reserves for pre-migration tokens
        const price = (0, program_1.calculatePrice)(virtualSol, virtualTokens);
        priceInSol = (price * constants_1.TOKEN_MULTIPLIER) / constants_1.LAMPORTS_PER_SOL;
    }
    // Market cap = fully diluted (total supply × price), matching pump.fun convention
    marketCapSol = (priceInSol * Number(constants_1.TOTAL_SUPPLY)) / constants_1.TOKEN_MULTIPLIER;
    const circulating = constants_1.TOTAL_SUPPLY - realTokens;
    const treasurySol = treasury ? Number(treasury.sol_balance.toString()) / constants_1.LAMPORTS_PER_SOL : 0;
    const treasuryTokens = treasury ? Number(treasury.tokens_held.toString()) / constants_1.TOKEN_MULTIPLIER : 0;
    // V33: buyback removed — these fields are deprecated (always 0 for new tokens)
    const boughtBack = treasury ? Number(treasury.total_bought_back.toString()) / constants_1.TOKEN_MULTIPLIER : 0;
    const buybackCount = treasury ? Number(treasury.buyback_count.toString()) : 0;
    const stars = treasury ? Number(treasury.total_stars.toString()) : 0;
    return {
        mint,
        name: (0, program_1.decodeString)(bc.name),
        symbol: (0, program_1.decodeString)(bc.symbol),
        description: metadata?.description,
        image: metadata?.image,
        status: getTokenStatus(bc),
        price_sol: priceInSol,
        price_usd: solPriceUsd ? priceInSol * solPriceUsd : undefined,
        market_cap_sol: marketCapSol,
        market_cap_usd: solPriceUsd ? marketCapSol * solPriceUsd : undefined,
        progress_percent: (0, program_1.calculateBondingProgress)(realSol),
        sol_raised: Number(realSol) / constants_1.LAMPORTS_PER_SOL,
        sol_target: 200,
        total_supply: Number(constants_1.TOTAL_SUPPLY) / constants_1.TOKEN_MULTIPLIER,
        circulating_supply: Number(circulating) / constants_1.TOKEN_MULTIPLIER,
        tokens_in_curve: Number(realTokens) / constants_1.TOKEN_MULTIPLIER,
        tokens_burned: Number(burned) / constants_1.TOKEN_MULTIPLIER,
        treasury_sol_balance: treasurySol,
        treasury_token_balance: treasuryTokens,
        total_bought_back: boughtBack,
        buyback_count: buybackCount,
        creator: bc.creator.toString(),
        holders: holdersCount ?? null,
        stars,
        created_at: 0,
        last_activity_at: Number(bc.last_activity_slot.toString()),
        twitter: metadata?.twitter,
        telegram: metadata?.telegram,
        website: metadata?.website,
        creator_verified: saidVerification?.verified,
        creator_trust_tier: saidVerification?.trustTier,
        creator_said_name: saidVerification?.name,
        creator_badge_url: saidVerification?.verified
            ? `https://api.saidprotocol.com/api/badge/${bc.creator.toString()}.svg`
            : undefined,
        ...(warnings && warnings.length > 0 ? { warnings } : {}),
    };
};
// Internal: fetch single token on-chain data
const fetchTokenRaw = async (connection, mint) => {
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [bcAccount, treasuryAccount] = await Promise.all([
        connection.getAccountInfo(bondingCurvePda),
        connection.getAccountInfo(treasuryPda),
    ]);
    if (!bcAccount)
        return null;
    const bondingCurve = coder.accounts.decode('BondingCurve', bcAccount.data);
    let treasury = null;
    if (treasuryAccount) {
        treasury = coder.accounts.decode('Treasury', treasuryAccount.data);
    }
    return { bondingCurve, treasury };
};
exports.fetchTokenRaw = fetchTokenRaw;
// ============================================================================
// Public API
// ============================================================================
/**
 * List tokens with optional filtering and sorting.
 */
const getTokens = async (connection, params = {}) => {
    const allTokens = await fetchAllRawTokens(connection);
    const filtered = filterAndSort(allTokens, params);
    const summaries = filtered.map(toTokenSummary);
    return {
        tokens: summaries,
        total: allTokens.length,
        limit: params.limit || summaries.length,
        offset: params.offset || 0,
    };
};
exports.getTokens = getTokens;
/**
 * Get on-chain Token-2022 metadata for a token.
 *
 * Reads name, symbol, and uri directly from the mint's TokenMetadata extension.
 * Returns null if the mint has no metadata (legacy pre-V29 tokens).
 */
const getTokenMetadata = async (connection, mintStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const metadata = await (0, spl_token_1.getTokenMetadata)(connection, mint, 'confirmed', constants_1.TOKEN_2022_PROGRAM_ID);
    if (!metadata)
        return null;
    return {
        name: metadata.name,
        symbol: metadata.symbol,
        uri: metadata.uri,
        mint: mintStr,
    };
};
exports.getTokenMetadata = getTokenMetadata;
/**
 * Get detailed info for a single token.
 */
const getToken = async (connection, mintStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const tokenData = await fetchTokenRaw(connection, mint);
    if (!tokenData) {
        throw new Error(`Token not found: ${mintStr}`);
    }
    const { bondingCurve, treasury } = tokenData;
    const warnings = [];
    // Fetch metadata from URI
    let metadata;
    const uri = (0, program_1.decodeString)(bondingCurve.uri);
    if (uri) {
        try {
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 10000);
            const res = await fetch(uri, { signal: controller.signal }).finally(() => clearTimeout(timer));
            const data = (await res.json());
            metadata = {
                description: data.description,
                image: data.image,
                twitter: data.twitter,
                telegram: data.telegram,
                website: data.website,
            };
        }
        catch (e) {
            warnings.push(`Metadata fetch failed: ${e instanceof Error ? e.message : String(e)}`);
        }
    }
    // Fetch holders count
    let holdersCount = null;
    try {
        const holders = await connection.getTokenLargestAccounts(mint, 'confirmed');
        holdersCount = holders.value.filter((a) => a.uiAmount && a.uiAmount > 0).length;
    }
    catch (e) {
        warnings.push(`Holders fetch failed: ${e instanceof Error ? e.message : String(e)}`);
    }
    // Fetch SOL price
    let solPriceUsd;
    try {
        const res = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd');
        const data = (await res.json());
        solPriceUsd = data?.solana?.usd;
    }
    catch (e) {
        warnings.push(`SOL price fetch failed: ${e instanceof Error ? e.message : String(e)}`);
    }
    // Fetch live pool price for migrated tokens
    let poolPrice;
    if (bondingCurve.migrated) {
        try {
            const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
            const [vault0Info, vault1Info] = await Promise.all([
                connection.getTokenAccountBalance(raydium.token0Vault),
                connection.getTokenAccountBalance(raydium.token1Vault),
            ]);
            const vault0Amount = Number(vault0Info.value.amount);
            const vault1Amount = Number(vault1Info.value.amount);
            if (raydium.isWsolToken0) {
                poolPrice = { solReserves: vault0Amount, tokenReserves: vault1Amount };
            }
            else {
                poolPrice = { solReserves: vault1Amount, tokenReserves: vault0Amount };
            }
        }
        catch (e) {
            warnings.push(`Pool price fetch failed: ${e instanceof Error ? e.message : String(e)}`);
        }
    }
    return buildTokenDetail(mintStr, bondingCurve, treasury, metadata, holdersCount, solPriceUsd, undefined, warnings, poolPrice);
};
exports.getToken = getToken;
/**
 * Get top holders for a token.
 */
const getHolders = async (connection, mintStr, limit = 20) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const safeLimit = Math.min(limit, 100);
    // Build excluded addresses (pools/vaults)
    const excluded = new Set();
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const bondingCurveVault = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, bondingCurvePda, true, constants_1.TOKEN_2022_PROGRAM_ID);
    excluded.add(bondingCurveVault.toString());
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const treasuryVault = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, treasuryPda, true, constants_1.TOKEN_2022_PROGRAM_ID);
    excluded.add(treasuryVault.toString());
    try {
        const raydiumAccounts = (0, program_1.getRaydiumMigrationAccounts)(mint);
        excluded.add(raydiumAccounts.token0Vault.toString());
        excluded.add(raydiumAccounts.token1Vault.toString());
    }
    catch {
        // Ignore
    }
    const response = await connection.getTokenLargestAccounts(mint, 'confirmed');
    const totalSupply = BigInt(1000000000) * BigInt(10 ** constants_1.TOKEN_DECIMALS);
    const filteredAccounts = response.value
        .filter((account) => account.uiAmount && account.uiAmount > 0)
        .filter((account) => !excluded.has(account.address.toString()))
        .slice(0, safeLimit);
    const accountInfos = await connection.getMultipleParsedAccounts(filteredAccounts.map((a) => a.address));
    const holders = filteredAccounts.map((account, i) => {
        const parsed = accountInfos.value[i]?.data;
        const owner = parsed && 'parsed' in parsed ? parsed.parsed?.info?.owner : null;
        return {
            address: owner || account.address.toString(),
            balance: Number(account.amount) / 10 ** constants_1.TOKEN_DECIMALS,
            percentage: (Number(account.amount) / Number(totalSupply)) * 100,
        };
    });
    return {
        holders,
        total_holders: response.value.filter((a) => a.uiAmount && a.uiAmount > 0 && !excluded.has(a.address.toString())).length,
    };
};
exports.getHolders = getHolders;
/**
 * Get messages (memos) for a token.
 */
const getMessages = async (connection, mintStr, limit = 50, opts) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const safeLimit = Math.min(limit, 100);
    const sigLimit = Math.min(safeLimit, 50);
    const source = opts?.source ?? 'all';
    // Helper: extract memo from a parsed transaction
    const extractMemo = async (tx, signature, blockTime) => {
        const allInstructions = [
            ...tx.transaction.message.instructions,
            ...(tx.meta?.innerInstructions || []).flatMap((inner) => inner.instructions),
        ];
        for (const ix of allInstructions) {
            const programId = 'programId' in ix ? ix.programId.toString() : '';
            const programName = 'program' in ix ? ix.program : '';
            const isMemo = programId === constants_1.MEMO_PROGRAM_ID.toString() ||
                programId === 'MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr' ||
                programName === 'spl-memo';
            if (isMemo) {
                let memoText = '';
                if ('parsed' in ix) {
                    memoText = typeof ix.parsed === 'string' ? ix.parsed : JSON.stringify(ix.parsed);
                }
                else if ('data' in ix && typeof ix.data === 'string') {
                    try {
                        const bs58 = await Promise.resolve().then(() => __importStar(require('bs58')));
                        const decoded = bs58.default.decode(ix.data);
                        memoText = new TextDecoder().decode(decoded);
                    }
                    catch {
                        memoText = ix.data;
                    }
                }
                if (memoText && memoText.trim()) {
                    const sender = tx.transaction.message.accountKeys[0]?.pubkey?.toString() || 'Unknown';
                    return {
                        signature,
                        memo: memoText.trim(),
                        sender,
                        timestamp: blockTime,
                    };
                }
            }
        }
        return null;
    };
    // Helper: fetch messages from a given account's signatures
    const fetchMessagesFromAccount = async (account) => {
        const signatures = await connection.getSignaturesForAddress(account, { limit: sigLimit }, 'confirmed');
        if (signatures.length === 0)
            return [];
        const result = [];
        const BATCH_SIZE = 100;
        for (let i = 0; i < signatures.length && result.length < safeLimit; i += BATCH_SIZE) {
            const batch = signatures.slice(i, i + BATCH_SIZE);
            const sigStrings = batch.map((s) => s.signature);
            let txs;
            try {
                txs = await connection.getParsedTransactions(sigStrings, {
                    maxSupportedTransactionVersion: 0,
                });
            }
            catch {
                continue;
            }
            for (let j = 0; j < txs.length && result.length < safeLimit; j++) {
                const tx = txs[j];
                if (!tx?.meta || tx.meta.err)
                    continue;
                const msg = await extractMemo(tx, batch[j].signature, batch[j].blockTime || 0);
                if (msg)
                    result.push(msg);
            }
        }
        return result;
    };
    // Fetch from requested source(s)
    let bondingMessages = [];
    let poolMessages = [];
    if (source === 'bonding' || source === 'all') {
        const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
        bondingMessages = await fetchMessagesFromAccount(bondingCurvePda).catch(() => []);
    }
    if (source === 'pool' || source === 'all') {
        try {
            const { poolState } = (0, program_1.getRaydiumMigrationAccounts)(mint);
            poolMessages = await fetchMessagesFromAccount(poolState);
        }
        catch {
            // no pool
        }
    }
    // Merge, dedupe by signature, sort newest first, trim to limit
    const seen = new Set();
    const messages = [];
    for (const m of [...bondingMessages, ...poolMessages]) {
        if (!seen.has(m.signature)) {
            seen.add(m.signature);
            messages.push(m);
        }
    }
    messages.sort((a, b) => b.timestamp - a.timestamp);
    const trimmed = messages.slice(0, safeLimit);
    // Enrich with SAID verification when opted in
    if (opts?.enrich) {
        const { verifySaid } = await Promise.resolve().then(() => __importStar(require('./said')));
        const uniqueSenders = [...new Set(trimmed.map((m) => m.sender))];
        const verifications = await Promise.all(uniqueSenders.map(async (sender) => {
            try {
                const v = await verifySaid(sender);
                return [sender, v];
            }
            catch {
                return [sender, null];
            }
        }));
        const verifyMap = new Map(verifications);
        for (const msg of trimmed) {
            const v = verifyMap.get(msg.sender);
            if (v) {
                msg.sender_verified = v.verified;
                msg.sender_trust_tier = v.trustTier;
                msg.sender_said_name = v.name;
                if (v.verified) {
                    msg.sender_badge_url = `https://api.saidprotocol.com/api/badge/${msg.sender}.svg`;
                }
            }
        }
    }
    return { messages: trimmed, total: trimmed.length };
};
exports.getMessages = getMessages;
// ============================================================================
// Lending (V2.4)
// ============================================================================
// Lending constants (matching the Rust program — see programs/torch_market/src/constants.rs)
const INTEREST_RATE_BPS = 200; // 2% per epoch
const LIQUIDATION_THRESHOLD_BPS = 6500; // 65%
const LIQUIDATION_BONUS_BPS = 1000; // 10%
const LENDING_UTILIZATION_CAP_BPS = 8000; // 80% (V4.0, was 70%)
const BORROW_SHARE_MULTIPLIER = 23; // Per-user cap: max borrow = 23x collateral share of supply (V10.2.5, was 5x)
const EPOCH_DURATION_SLOTS = 1512000; // 7 days at 400ms/slot — matches on-chain EPOCH_DURATION_SLOTS
// Project simple-linear interest forward to the given slot, matching the on-chain
// accrue_interest() formula exactly:
//   interest = principal * rate_bps * slots_elapsed / (10000 * EPOCH_DURATION_SLOTS)
// See programs/torch_market/src/handlers/lending.rs:accrue_interest.
// Returns total accrued interest (stored + projected pending), not just the delta.
const projectAccruedInterest = (principal, storedAccrued, lastUpdateSlot, currentSlot, rateBps = INTEREST_RATE_BPS) => {
    if (principal <= 0)
        return storedAccrued;
    const slotsElapsed = Math.max(0, currentSlot - lastUpdateSlot);
    if (slotsElapsed === 0)
        return storedAccrued;
    // Use BigInt to match on-chain u128 math and avoid precision loss at high slot counts.
    const delta = Number((BigInt(principal) * BigInt(rateBps) * BigInt(slotsElapsed)) /
        (BigInt(10000) * BigInt(EPOCH_DURATION_SLOTS)));
    return storedAccrued + delta;
};
// Depth-based risk bands (V7): pool SOL depth → max LTV
const MIN_POOL_SOL_LENDING = 5000000000; // 5 SOL
const DEPTH_TIER_1 = 50000000000; // 50 SOL
const DEPTH_TIER_2 = 200000000000; // 200 SOL
const DEPTH_TIER_3 = 500000000000; // 500 SOL
const DEPTH_LTV_0 = 2500; // <50 SOL  → 25%
const DEPTH_LTV_1 = 3500; // 50-200   → 35%
const DEPTH_LTV_2 = 4500; // 200-500  → 45%
const DEPTH_LTV_3 = 5000; // 500+     → 50%
const getDepthMaxLtvBps = (poolSol) => {
    if (poolSol < MIN_POOL_SOL_LENDING)
        return 0;
    if (poolSol < DEPTH_TIER_1)
        return DEPTH_LTV_0;
    if (poolSol < DEPTH_TIER_2)
        return DEPTH_LTV_1;
    if (poolSol < DEPTH_TIER_3)
        return DEPTH_LTV_2;
    return DEPTH_LTV_3;
};
/**
 * Get lending info for a migrated token.
 *
 * Returns interest rates, LTV limits, and active loan statistics.
 * Lending is available on all migrated tokens with treasury SOL.
 */
const getLendingInfo = async (connection, mintStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const tokenData = await fetchTokenRaw(connection, mint);
    if (!tokenData)
        throw new Error(`Token not found: ${mintStr}`);
    const { bondingCurve, treasury } = tokenData;
    if (!bondingCurve.migrated)
        throw new Error('Token not yet migrated, lending not available');
    const treasurySol = treasury ? Number(treasury.sol_balance.toString()) : 0;
    // Fetch pool SOL depth for depth-band max LTV
    let poolSol = 0;
    try {
        const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
        const [vault0Info, vault1Info] = await Promise.all([
            connection.getTokenAccountBalance(raydium.token0Vault),
            connection.getTokenAccountBalance(raydium.token1Vault),
        ]);
        poolSol = raydium.isWsolToken0
            ? Number(vault0Info.value.amount)
            : Number(vault1Info.value.amount);
    }
    catch {
        // Fall back to minimum tier if pool fetch fails
    }
    const effectiveMaxLtv = getDepthMaxLtvBps(poolSol);
    // Scan for active loan positions via collateral vault balance
    const [collateralVaultPda] = (0, program_1.getCollateralVaultPda)(mint);
    const vaultInfo = await connection.getAccountInfo(collateralVaultPda);
    // Count active loans by scanning LoanPosition accounts
    let activeLoans = 0;
    let totalSolLent = 0;
    const warnings = [];
    try {
        // Derive discriminator from IDL rather than hardcoding
        const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
        const loanDiscriminator = coder.accounts.accountDiscriminator('LoanPosition');
        const bs58 = await Promise.resolve().then(() => __importStar(require('bs58')));
        const accounts = await connection.getProgramAccounts(constants_1.PROGRAM_ID, {
            filters: [
                { memcmp: { offset: 0, bytes: bs58.default.encode(loanDiscriminator) } },
                { memcmp: { offset: 8 + 32, bytes: mint.toBase58() } }, // mint at offset 40
            ],
            dataSlice: { offset: 8 + 32 + 32, length: 16 }, // collateral_amount + borrowed_amount
        });
        for (const acc of accounts) {
            try {
                // Read borrowed_amount (u64 at offset 8 within the slice)
                const borrowed = acc.account.data.readBigUInt64LE(8);
                if (borrowed > BigInt(0)) {
                    activeLoans = (activeLoans ?? 0) + 1;
                    totalSolLent = (totalSolLent ?? 0) + Number(borrowed);
                }
            }
            catch {
                // Skip malformed accounts
            }
        }
    }
    catch (e) {
        activeLoans = null;
        totalSolLent = null;
        warnings.push(`Loan enumeration failed: ${e instanceof Error ? e.message : String(e)}`);
    }
    return {
        interest_rate_bps: INTEREST_RATE_BPS,
        max_ltv_bps: effectiveMaxLtv,
        liquidation_threshold_bps: LIQUIDATION_THRESHOLD_BPS,
        liquidation_bonus_bps: LIQUIDATION_BONUS_BPS,
        utilization_cap_bps: LENDING_UTILIZATION_CAP_BPS,
        borrow_share_multiplier: BORROW_SHARE_MULTIPLIER,
        total_sol_lent: totalSolLent,
        active_loans: activeLoans,
        treasury_sol_available: Math.max(0, Math.floor((treasurySol * LENDING_UTILIZATION_CAP_BPS) / 10000) - (totalSolLent ?? 0)),
        ...(warnings.length > 0 ? { warnings } : {}),
    };
};
exports.getLendingInfo = getLendingInfo;
/**
 * Get loan position for a wallet on a specific token.
 *
 * Returns collateral locked, SOL owed, health status, etc.
 * Returns health="none" if no active loan exists.
 */
const getLoanPosition = async (connection, mintStr, walletStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const wallet = new web3_js_1.PublicKey(walletStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [loanPositionPda] = (0, program_1.getLoanPositionPda)(mint, wallet);
    const [accountInfo, currentSlot] = await Promise.all([
        connection.getAccountInfo(loanPositionPda),
        connection.getSlot('confirmed'),
    ]);
    if (!accountInfo) {
        return {
            collateral_amount: 0,
            borrowed_amount: 0,
            accrued_interest: 0,
            accrued_interest_stored: 0,
            last_update_slot: 0,
            total_owed: 0,
            collateral_value_sol: 0,
            current_ltv_bps: 0,
            health: 'none',
        };
    }
    const loan = coder.accounts.decode('LoanPosition', accountInfo.data);
    const collateral = Number(loan.collateral_amount.toString());
    const borrowed = Number(loan.borrowed_amount.toString());
    const storedInterest = Number(loan.accrued_interest.toString());
    const lastUpdateSlot = Number(loan.last_update_slot.toString());
    const interest = projectAccruedInterest(borrowed, storedInterest, lastUpdateSlot, currentSlot);
    const totalOwed = borrowed + interest;
    // Get collateral value from Raydium pool price
    let collateralValueSol = 0;
    let poolSol = 0;
    const warnings = [];
    try {
        const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
        const [vault0Info, vault1Info] = await Promise.all([
            connection.getTokenAccountBalance(raydium.token0Vault),
            connection.getTokenAccountBalance(raydium.token1Vault),
        ]);
        const vault0Amount = Number(vault0Info.value.amount);
        const vault1Amount = Number(vault1Info.value.amount);
        // Determine which vault is SOL and which is token
        if (raydium.isWsolToken0) {
            poolSol = vault0Amount;
            const tokenReserves = vault1Amount;
            if (tokenReserves > 0) {
                collateralValueSol = (collateral * poolSol) / tokenReserves;
            }
        }
        else {
            poolSol = vault1Amount;
            const tokenReserves = vault0Amount;
            if (tokenReserves > 0) {
                collateralValueSol = (collateral * poolSol) / tokenReserves;
            }
        }
    }
    catch (e) {
        collateralValueSol = null;
        warnings.push(`Collateral valuation failed: ${e instanceof Error ? e.message : String(e)}`);
    }
    let currentLtvBps;
    if (collateralValueSol === null) {
        currentLtvBps = null;
    }
    else if (collateralValueSol > 0) {
        currentLtvBps = Math.floor((totalOwed / collateralValueSol) * 10000);
    }
    else {
        currentLtvBps = totalOwed > 0 ? 10000 : 0;
    }
    const maxLtvBps = getDepthMaxLtvBps(poolSol);
    let health;
    if (borrowed === 0 && interest === 0) {
        health = 'none';
    }
    else if (currentLtvBps === null) {
        health = 'healthy';
    }
    else if (currentLtvBps >= LIQUIDATION_THRESHOLD_BPS) {
        health = 'liquidatable';
    }
    else if (currentLtvBps >= maxLtvBps) {
        health = 'at_risk';
    }
    else {
        health = 'healthy';
    }
    return {
        collateral_amount: collateral,
        borrowed_amount: borrowed,
        accrued_interest: interest,
        accrued_interest_stored: storedInterest,
        last_update_slot: lastUpdateSlot,
        total_owed: totalOwed,
        collateral_value_sol: collateralValueSol,
        current_ltv_bps: currentLtvBps,
        health,
        ...(warnings.length > 0 ? { warnings } : {}),
    };
};
exports.getLoanPosition = getLoanPosition;
/**
 * Get a user's short position for a given token.
 *
 * Reads the ShortPosition PDA on-chain and computes health status
 * using the Raydium pool price to value the token debt against SOL collateral.
 */
const getShortPosition = async (connection, mintStr, walletStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const wallet = new web3_js_1.PublicKey(walletStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [shortPositionPda] = (0, program_1.getShortPositionPda)(mint, wallet);
    const [accountInfo, currentSlot] = await Promise.all([
        connection.getAccountInfo(shortPositionPda),
        connection.getSlot('confirmed'),
    ]);
    if (!accountInfo) {
        return {
            sol_collateral: 0,
            tokens_borrowed: 0,
            accrued_interest: 0,
            accrued_interest_stored: 0,
            last_update_slot: 0,
            total_owed_tokens: 0,
            debt_value_sol: 0,
            current_ltv_bps: 0,
            health: 'none',
        };
    }
    const short = coder.accounts.decode('ShortPosition', accountInfo.data);
    const solCollateral = Number(short.sol_collateral.toString());
    const tokensBorrowed = Number(short.tokens_borrowed.toString());
    const storedInterest = Number(short.accrued_interest.toString());
    const lastUpdateSlot = Number(short.last_update_slot.toString());
    const interest = projectAccruedInterest(tokensBorrowed, storedInterest, lastUpdateSlot, currentSlot);
    const totalOwedTokens = tokensBorrowed + interest;
    // Get token debt value from Raydium pool price
    let debtValueSol = 0;
    let poolSol = 0;
    const warnings = [];
    try {
        const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
        const [vault0Info, vault1Info] = await Promise.all([
            connection.getTokenAccountBalance(raydium.token0Vault),
            connection.getTokenAccountBalance(raydium.token1Vault),
        ]);
        const vault0Amount = Number(vault0Info.value.amount);
        const vault1Amount = Number(vault1Info.value.amount);
        if (raydium.isWsolToken0) {
            poolSol = vault0Amount;
            const tokenReserves = vault1Amount;
            if (tokenReserves > 0) {
                debtValueSol = (totalOwedTokens * poolSol) / tokenReserves;
            }
        }
        else {
            poolSol = vault1Amount;
            const tokenReserves = vault0Amount;
            if (tokenReserves > 0) {
                debtValueSol = (totalOwedTokens * poolSol) / tokenReserves;
            }
        }
    }
    catch (e) {
        debtValueSol = null;
        warnings.push(`Debt valuation failed: ${e instanceof Error ? e.message : String(e)}`);
    }
    // For shorts, LTV = debt_value_sol / sol_collateral
    let currentLtvBps;
    if (debtValueSol === null) {
        currentLtvBps = null;
    }
    else if (solCollateral > 0) {
        currentLtvBps = Math.floor((debtValueSol / solCollateral) * 10000);
    }
    else {
        currentLtvBps = totalOwedTokens > 0 ? 10000 : 0;
    }
    const maxLtvBps = getDepthMaxLtvBps(poolSol);
    let health;
    if (tokensBorrowed === 0 && interest === 0) {
        health = 'none';
    }
    else if (currentLtvBps === null) {
        health = 'healthy';
    }
    else if (currentLtvBps >= LIQUIDATION_THRESHOLD_BPS) {
        health = 'liquidatable';
    }
    else if (currentLtvBps >= maxLtvBps) {
        health = 'at_risk';
    }
    else {
        health = 'healthy';
    }
    return {
        sol_collateral: solCollateral,
        tokens_borrowed: tokensBorrowed,
        accrued_interest: interest,
        accrued_interest_stored: storedInterest,
        last_update_slot: lastUpdateSlot,
        total_owed_tokens: totalOwedTokens,
        debt_value_sol: debtValueSol,
        current_ltv_bps: currentLtvBps,
        health,
        ...(warnings.length > 0 ? { warnings } : {}),
    };
};
exports.getShortPosition = getShortPosition;
/**
 * Get all active loan positions for a given token mint.
 *
 * Scans on-chain LoanPosition accounts, computes health for each,
 * and returns them sorted: liquidatable first, then at_risk, then healthy.
 */
const getAllLoanPositions = async (connection, mintStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    // 1. Fetch all LoanPosition accounts for this mint
    const loanDiscriminator = coder.accounts.accountDiscriminator('LoanPosition');
    const bs58 = await Promise.resolve().then(() => __importStar(require('bs58')));
    const accounts = await connection.getProgramAccounts(constants_1.PROGRAM_ID, {
        filters: [
            { memcmp: { offset: 0, bytes: bs58.default.encode(loanDiscriminator) } },
            { memcmp: { offset: 8 + 32, bytes: mint.toBase58() } }, // mint at offset 40
        ],
    });
    // 2. Decode and filter to active loans (borrowed_amount > 0)
    const activeLoans = [];
    for (const acc of accounts) {
        try {
            const loan = coder.accounts.decode('LoanPosition', acc.account.data);
            const borrowed = Number(loan.borrowed_amount.toString());
            if (borrowed > 0) {
                activeLoans.push({
                    borrower: loan.user.toString(),
                    loan,
                });
            }
        }
        catch {
            // Skip malformed accounts
        }
    }
    // 3. Fetch Raydium pool price + current slot ONCE (interest projection needs currentSlot)
    let poolPriceSol = null;
    let solReserves = 0;
    let tokenReserves = 0;
    let currentSlot = 0;
    try {
        const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
        const [vault0Info, vault1Info, slot] = await Promise.all([
            connection.getTokenAccountBalance(raydium.token0Vault),
            connection.getTokenAccountBalance(raydium.token1Vault),
            connection.getSlot('confirmed'),
        ]);
        currentSlot = slot;
        const vault0Amount = Number(vault0Info.value.amount);
        const vault1Amount = Number(vault1Info.value.amount);
        if (raydium.isWsolToken0) {
            solReserves = vault0Amount;
            tokenReserves = vault1Amount;
        }
        else {
            solReserves = vault1Amount;
            tokenReserves = vault0Amount;
        }
        if (tokenReserves > 0) {
            poolPriceSol = solReserves / tokenReserves;
        }
    }
    catch {
        // Pool price unavailable — fall back to a plain slot fetch so we can still project interest
        try {
            currentSlot = await connection.getSlot('confirmed');
        }
        catch {
            /* ignore */
        }
    }
    // 4. Compute health for each position (interest projected to currentSlot)
    const positions = activeLoans.map(({ borrower, loan }) => {
        const collateral = Number(loan.collateral_amount.toString());
        const borrowed = Number(loan.borrowed_amount.toString());
        const storedInterest = Number(loan.accrued_interest.toString());
        const lastUpdateSlot = Number(loan.last_update_slot.toString());
        const interest = projectAccruedInterest(borrowed, storedInterest, lastUpdateSlot, currentSlot);
        const totalOwed = borrowed + interest;
        let collateralValueSol = null;
        if (poolPriceSol !== null && tokenReserves > 0) {
            collateralValueSol = (collateral * solReserves) / tokenReserves;
        }
        let currentLtvBps;
        if (collateralValueSol === null) {
            currentLtvBps = null;
        }
        else if (collateralValueSol > 0) {
            currentLtvBps = Math.floor((totalOwed / collateralValueSol) * 10000);
        }
        else {
            currentLtvBps = totalOwed > 0 ? 10000 : 0;
        }
        const maxLtvBps = getDepthMaxLtvBps(solReserves);
        let health;
        if (borrowed === 0 && interest === 0) {
            health = 'none';
        }
        else if (currentLtvBps === null) {
            health = 'healthy';
        }
        else if (currentLtvBps >= LIQUIDATION_THRESHOLD_BPS) {
            health = 'liquidatable';
        }
        else if (currentLtvBps >= maxLtvBps) {
            health = 'at_risk';
        }
        else {
            health = 'healthy';
        }
        return {
            borrower,
            collateral_amount: collateral,
            borrowed_amount: borrowed,
            accrued_interest: interest,
            accrued_interest_stored: storedInterest,
            last_update_slot: lastUpdateSlot,
            total_owed: totalOwed,
            collateral_value_sol: collateralValueSol,
            current_ltv_bps: currentLtvBps,
            health,
        };
    });
    // 5. Sort: liquidatable first, then at_risk, then healthy
    const healthOrder = { liquidatable: 0, at_risk: 1, healthy: 2, none: 3 };
    positions.sort((a, b) => (healthOrder[a.health] ?? 3) - (healthOrder[b.health] ?? 3));
    return { positions, pool_price_sol: poolPriceSol };
};
exports.getAllLoanPositions = getAllLoanPositions;
// ============================================================================
// Vault Queries (V2.0)
// ============================================================================
/**
 * Get vault state by the vault creator's public key.
 *
 * Returns vault balance, authority, linked wallet count, etc.
 * Returns null if no vault exists for this creator.
 */
const getVault = async (connection, creatorStr) => {
    const creator = new web3_js_1.PublicKey(creatorStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(creator);
    const accountInfo = await connection.getAccountInfo(vaultPda);
    if (!accountInfo)
        return null;
    const vault = coder.accounts.decode('TorchVault', accountInfo.data);
    return {
        address: vaultPda.toString(),
        creator: vault.creator.toString(),
        authority: vault.authority.toString(),
        sol_balance: Number(vault.sol_balance.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_deposited: Number(vault.total_deposited.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_withdrawn: Number(vault.total_withdrawn.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_spent: Number(vault.total_spent.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_received: Number(vault.total_received.toString()) / constants_1.LAMPORTS_PER_SOL,
        linked_wallets: vault.linked_wallets,
        created_at: Number(vault.created_at.toString()),
    };
};
exports.getVault = getVault;
/**
 * Get vault state by looking up a linked wallet's VaultWalletLink.
 *
 * Useful when you have an agent wallet and need to find its vault.
 * Returns null if the wallet is not linked to any vault.
 */
const getVaultForWallet = async (connection, walletStr) => {
    const wallet = new web3_js_1.PublicKey(walletStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [walletLinkPda] = (0, program_1.getVaultWalletLinkPda)(wallet);
    const linkInfo = await connection.getAccountInfo(walletLinkPda);
    if (!linkInfo)
        return null;
    const link = coder.accounts.decode('VaultWalletLink', linkInfo.data);
    // Now fetch the vault using the vault PDA stored in the link
    const vaultInfo = await connection.getAccountInfo(link.vault);
    if (!vaultInfo)
        return null;
    const vault = coder.accounts.decode('TorchVault', vaultInfo.data);
    return {
        address: link.vault.toString(),
        creator: vault.creator.toString(),
        authority: vault.authority.toString(),
        sol_balance: Number(vault.sol_balance.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_deposited: Number(vault.total_deposited.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_withdrawn: Number(vault.total_withdrawn.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_spent: Number(vault.total_spent.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_received: Number(vault.total_received.toString()) / constants_1.LAMPORTS_PER_SOL,
        linked_wallets: vault.linked_wallets,
        created_at: Number(vault.created_at.toString()),
    };
};
exports.getVaultForWallet = getVaultForWallet;
/**
 * Get wallet link state for a specific wallet.
 *
 * Returns the link info (which vault it's linked to, when) or null if not linked.
 */
const getVaultWalletLink = async (connection, walletStr) => {
    const wallet = new web3_js_1.PublicKey(walletStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [walletLinkPda] = (0, program_1.getVaultWalletLinkPda)(wallet);
    const accountInfo = await connection.getAccountInfo(walletLinkPda);
    if (!accountInfo)
        return null;
    const link = coder.accounts.decode('VaultWalletLink', accountInfo.data);
    return {
        address: walletLinkPda.toString(),
        vault: link.vault.toString(),
        wallet: link.wallet.toString(),
        linked_at: Number(link.linked_at.toString()),
    };
};
exports.getVaultWalletLink = getVaultWalletLink;
// Per-user trading stats (volume, rewards claimed). Returns null if the user has
// no stats account yet (no trading activity).
const getUserStats = async (connection, walletStr) => {
    const wallet = new web3_js_1.PublicKey(walletStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [userStatsPda] = (0, program_1.getUserStatsPda)(wallet);
    const accountInfo = await connection.getAccountInfo(userStatsPda);
    if (!accountInfo)
        return null;
    const stats = coder.accounts.decode('UserStats', accountInfo.data);
    return {
        address: userStatsPda.toString(),
        user: stats.user.toString(),
        total_volume_sol: Number(stats.total_volume.toString()) / constants_1.LAMPORTS_PER_SOL,
        volume_current_epoch_sol: Number(stats.volume_current_epoch.toString()) / constants_1.LAMPORTS_PER_SOL,
        volume_previous_epoch_sol: Number(stats.volume_previous_epoch.toString()) / constants_1.LAMPORTS_PER_SOL,
        last_epoch_claimed: Number(stats.last_epoch_claimed.toString()),
        total_rewards_claimed_sol: Number(stats.total_rewards_claimed.toString()) / constants_1.LAMPORTS_PER_SOL,
        last_volume_epoch: Number(stats.last_volume_epoch.toString()),
    };
};
exports.getUserStats = getUserStats;
// Protocol treasury state (current epoch, balances, distribution accounting).
// Returns null if the protocol hasn't been initialized yet.
const getProtocolTreasuryState = async (connection) => {
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [protocolTreasuryPda] = (0, program_1.getProtocolTreasuryPda)();
    const accountInfo = await connection.getAccountInfo(protocolTreasuryPda);
    if (!accountInfo)
        return null;
    const t = coder.accounts.decode('ProtocolTreasury', accountInfo.data);
    return {
        address: protocolTreasuryPda.toString(),
        authority: t.authority.toString(),
        current_balance_sol: Number(t.current_balance.toString()) / constants_1.LAMPORTS_PER_SOL,
        reserve_floor_sol: Number(t.reserve_floor.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_fees_received_sol: Number(t.total_fees_received.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_distributed_sol: Number(t.total_distributed.toString()) / constants_1.LAMPORTS_PER_SOL,
        current_epoch: Number(t.current_epoch.toString()),
        last_epoch_ts: Number(t.last_epoch_ts.toString()),
        total_volume_current_epoch_sol: Number(t.total_volume_current_epoch.toString()) / constants_1.LAMPORTS_PER_SOL,
        total_volume_previous_epoch_sol: Number(t.total_volume_previous_epoch.toString()) / constants_1.LAMPORTS_PER_SOL,
        distributable_amount_sol: Number(t.distributable_amount.toString()) / constants_1.LAMPORTS_PER_SOL,
    };
};
exports.getProtocolTreasuryState = getProtocolTreasuryState;
// Per-token Treasury state: SOL balance, tokens held, harvested fees, stars,
// and baseline pool reserves captured at migration. Returns null if the token
// or its treasury hasn't been created yet.
const getTreasuryState = async (connection, mintStr) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const coder = new anchor_1.BorshCoder(torch_market_json_1.default);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const accountInfo = await connection.getAccountInfo(treasuryPda);
    if (!accountInfo)
        return null;
    const t = coder.accounts.decode('Treasury', accountInfo.data);
    return {
        address: treasuryPda.toString(),
        bonding_curve: t.bonding_curve.toString(),
        mint: t.mint.toString(),
        sol_balance_sol: Number(t.sol_balance.toString()) / constants_1.LAMPORTS_PER_SOL,
        tokens_held: Number(t.tokens_held.toString()),
        harvested_fees_sol: Number(t.harvested_fees.toString()) / constants_1.LAMPORTS_PER_SOL,
        baseline_sol_reserves: Number(t.baseline_sol_reserves.toString()),
        baseline_token_reserves: Number(t.baseline_token_reserves.toString()),
        baseline_initialized: t.baseline_initialized,
        total_stars: Number(t.total_stars.toString()),
        star_sol_balance_sol: Number(t.star_sol_balance.toString()) / constants_1.LAMPORTS_PER_SOL,
        creator_paid_out: t.creator_paid_out,
        total_bought_back: Number(t.total_bought_back.toString()),
        total_burned_from_buyback: Number(t.total_burned_from_buyback.toString()),
        last_buyback_slot: Number(t.last_buyback_slot.toString()),
        buyback_count: Number(t.buyback_count.toString()),
    };
};
exports.getTreasuryState = getTreasuryState;
//# sourceMappingURL=tokens.js.map