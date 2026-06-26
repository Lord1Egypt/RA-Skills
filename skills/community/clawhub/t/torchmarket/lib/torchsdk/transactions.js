"use strict";
/**
 * Transaction builders
 *
 * Build unsigned transactions for buy, sell, create, star, vault, and lending.
 * Agents sign these locally and submit to the network.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildEnableShortSellingTransaction = exports.buildLiquidateShortTransaction = exports.buildCloseShortTransaction = exports.buildOpenShortTransaction = exports.buildSwapFeesToSolTransaction = exports.buildHarvestFeesTransaction = exports.buildAdvanceProtocolEpochTransaction = exports.buildMigrateTransaction = exports.buildWithdrawTokensTransaction = exports.buildReclaimFailedTokenTransaction = exports.buildClaimProtocolRewardsTransaction = exports.buildLiquidateTransaction = exports.buildRepayTransaction = exports.buildBorrowTransaction = exports.buildTransferAuthorityTransaction = exports.buildUnlinkWalletTransaction = exports.buildLinkWalletTransaction = exports.buildWithdrawVaultTransaction = exports.buildDepositVaultTransaction = exports.buildCreateVaultTransaction = exports.buildStarTransaction = exports.sendCreateToken = exports.buildCreateTokenTransaction = exports.buildSellTransaction = exports.sendDirectBuy = exports.sendBuy = exports.buildDirectBuyTransaction = exports.buildBuyTransaction = void 0;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const anchor_1 = require("@coral-xyz/anchor");
const program_1 = require("./program");
const constants_1 = require("./constants");
const tokens_1 = require("./tokens");
const quotes_1 = require("./quotes");
const torch_market_json_1 = __importDefault(require("./torch_market.json"));
// ============================================================================
// Helpers
// ============================================================================
const MAX_MESSAGE_LENGTH = 500;
const makeDummyProvider = (connection, payer) => {
    const dummyWallet = {
        publicKey: payer,
        signTransaction: async (t) => t,
        signAllTransactions: async (t) => t,
    };
    return new anchor_1.AnchorProvider(connection, dummyWallet, {});
};
/** Derive vault + wallet link PDAs. Returns nulls if vaultCreatorStr is undefined. */
const deriveVaultAccounts = (vaultCreatorStr, signer) => {
    if (!vaultCreatorStr)
        return { torchVault: null, walletLink: null };
    const vaultCreator = new web3_js_1.PublicKey(vaultCreatorStr);
    const [torchVault] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const [walletLink] = (0, program_1.getVaultWalletLinkPda)(signer);
    return { torchVault, walletLink };
};
/** Create vault token ATA instruction (idempotent). */
const createVaultTokenAtaIx = (payer, mint, vaultPda) => (0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(payer, (0, spl_token_1.getAssociatedTokenAddressSync)(mint, vaultPda, true, spl_token_1.TOKEN_2022_PROGRAM_ID), vaultPda, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID);
/** Get the vault's token ATA address. */
const getVaultTokenAta = (mint, vaultPda) => (0, spl_token_1.getAssociatedTokenAddressSync)(mint, vaultPda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
/** Add an SPL Memo instruction to a transaction. */
const addMemoIx = (tx, signer, message, maxLength = MAX_MESSAGE_LENGTH) => {
    if (!message || message.trim().length === 0)
        return;
    const trimmed = message.trim().slice(0, maxLength);
    if (trimmed.length < message.trim().length && maxLength === MAX_MESSAGE_LENGTH) {
        throw new Error(`Message must be ${MAX_MESSAGE_LENGTH} characters or less`);
    }
    tx.add(new web3_js_1.TransactionInstruction({
        programId: constants_1.MEMO_PROGRAM_ID,
        keys: [{ pubkey: signer, isSigner: true, isWritable: false }],
        data: Buffer.from(trimmed, 'utf-8'),
    }));
};
// ── Transaction finalization ────────────────────────────────────────
/**
 * Compile instructions into a VersionedTransaction (v0 message).
 */
const finalizeTransaction = async (connection, tx, feePayer) => {
    const { blockhash } = await connection.getLatestBlockhash();
    const message = new web3_js_1.TransactionMessage({
        payerKey: feePayer,
        recentBlockhash: blockhash,
        instructions: tx.instructions,
    }).compileToV0Message();
    return new web3_js_1.VersionedTransaction(message);
};
// ============================================================================
// Buy
// ============================================================================
// Internal buy builder shared by both vault and direct variants
const buildBuyTransactionInternal = async (connection, mintStr, buyerStr, amount_sol, slippage_bps, message, vaultCreatorStr, quote) => {
    const mint = new web3_js_1.PublicKey(mintStr);
    const buyer = new web3_js_1.PublicKey(buyerStr);
    const tokenData = await (0, tokens_1.fetchTokenRaw)(connection, mint);
    if (!tokenData)
        throw new Error(`Token not found: ${mintStr}`);
    const { bondingCurve, treasury } = tokenData;
    // Migrated token — route through vault swap on Raydium DEX
    if (quote?.source === 'dex' || bondingCurve.bonding_complete) {
        if (!vaultCreatorStr) {
            throw new Error('Migrated tokens require vault-based trading. Use buildBuyTransaction with a vault parameter.');
        }
        const resolvedQuote = quote ?? (await (0, quotes_1.getBuyQuote)(connection, mintStr, amount_sol));
        const slippage = slippage_bps ?? 100;
        const minOut = (BigInt(resolvedQuote.min_output_tokens) * BigInt(10000 - slippage)) / BigInt(10000);
        const result = await buildVaultSwapTransaction(connection, {
            mint: mintStr,
            signer: buyerStr,
            vault_creator: vaultCreatorStr,
            amount_in: amount_sol,
            minimum_amount_out: Number(minOut),
            is_buy: true,
            message,
        });
        return {
            ...result,
            message: `Buy ~${resolvedQuote.tokens_to_user / 1e6} tokens for ${amount_sol / 1e9} SOL (via DEX)`,
        };
    }
    // Calculate expected output
    const virtualSol = BigInt(bondingCurve.virtual_sol_reserves.toString());
    const virtualTokens = BigInt(bondingCurve.virtual_token_reserves.toString());
    const realSol = BigInt(bondingCurve.real_sol_reserves.toString());
    const bondingTarget = BigInt(bondingCurve.bonding_target.toString());
    const solAmount = BigInt(amount_sol);
    const result = (0, program_1.calculateTokensOut)(solAmount, virtualSol, virtualTokens, realSol, 100, 100, bondingTarget);
    // [V28] Detect if this buy will complete bonding
    const resolvedTarget = bondingTarget === BigInt(0) ? BigInt('200000000000') : bondingTarget;
    const newRealSol = realSol + result.solToCurve;
    const willCompleteBonding = newRealSol >= resolvedTarget;
    // Apply slippage
    if (slippage_bps < 10 || slippage_bps > 1000) {
        throw new Error(`slippage_bps must be between 10 (0.1%) and 1000 (10%), got ${slippage_bps}`);
    }
    const slippage = slippage_bps;
    const minTokens = (result.tokensToUser * BigInt(10000 - slippage)) / BigInt(10000);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [userPositionPda] = (0, program_1.getUserPositionPda)(bondingCurvePda, buyer);
    const [userStatsPda] = (0, program_1.getUserStatsPda)(buyer);
    const [globalConfigPda] = (0, program_1.getGlobalConfigPda)();
    const [protocolTreasuryPda] = (0, program_1.getProtocolTreasuryPda)();
    const bondingCurveTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, bondingCurvePda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const treasuryTokenAccount = (0, program_1.getTreasuryTokenAccount)(mint, treasuryPda);
    const buyerTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, buyer, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const tx = new web3_js_1.Transaction();
    // Create buyer ATA if needed
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(buyer, buyerTokenAccount, buyer, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    const provider = makeDummyProvider(connection, buyer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    // Fetch global config for dev wallet
    const globalConfigAccount = (await program.account.globalConfig.fetch(globalConfigPda));
    // Vault accounts (optional — pass null when not using vault)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, buyer);
    let vaultTokenAccount = null;
    if (torchVaultAccount) {
        vaultTokenAccount = getVaultTokenAta(mint, torchVaultAccount);
        tx.add(createVaultTokenAtaIx(buyer, mint, torchVaultAccount));
    }
    const buyIx = await program.methods
        .buy({
        solAmount: new anchor_1.BN(amount_sol.toString()),
        minTokensOut: new anchor_1.BN(minTokens.toString()),
    })
        .accounts({
        buyer,
        globalConfig: globalConfigPda,
        devWallet: globalConfigAccount.devWallet || globalConfigAccount.dev_wallet,
        protocolTreasury: protocolTreasuryPda,
        creator: bondingCurve.creator,
        mint,
        bondingCurve: bondingCurvePda,
        tokenVault: bondingCurveTokenAccount,
        tokenTreasury: treasuryPda,
        treasuryTokenAccount,
        buyerTokenAccount,
        userPosition: userPositionPda,
        userStats: userStatsPda,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(buyIx);
    addMemoIx(tx, buyer, message);
    const versionedTx = await finalizeTransaction(connection, tx, buyer);
    // [V28] Build separate migration transaction when this buy completes bonding.
    // Split into two txs because buy + migration exceeds the 1232-byte legacy limit.
    // Program handles treasury reimbursement internally, so this is just a standard migration call.
    let migrationTransaction;
    if (willCompleteBonding) {
        const migResult = await (0, exports.buildMigrateTransaction)(connection, {
            mint: mintStr,
            payer: buyerStr,
        });
        migrationTransaction = migResult.transaction;
    }
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    const migrateLabel = willCompleteBonding ? ' + migrate to DEX' : '';
    return {
        transaction: versionedTx,
        migrationTransaction,
        message: `Buy ${Number(result.tokensToUser) / 1e6} tokens for ${Number(solAmount) / 1e9} SOL${vaultLabel}${migrateLabel}`,
    };
};
/**
 * Build an unsigned vault-funded buy transaction.
 *
 * The vault pays for the buy. This is the recommended path for AI agents.
 *
 * @param connection - Solana RPC connection
 * @param params - Buy parameters with required vault creator pubkey
 * @returns Unsigned transaction and descriptive message
 */
const buildBuyTransaction = async (connection, params) => {
    const { mint, buyer, amount_sol, slippage_bps = 100, message, vault, quote } = params;
    return buildBuyTransactionInternal(connection, mint, buyer, amount_sol, slippage_bps, message, vault, quote);
};
exports.buildBuyTransaction = buildBuyTransaction;
/**
 * Build an unsigned direct buy transaction (no vault).
 *
 * The buyer pays from their own wallet. Use this for human-operated wallets only.
 * For AI agents, use buildBuyTransaction with a vault instead.
 *
 * @param connection - Solana RPC connection
 * @param params - Buy parameters (no vault)
 * @returns Unsigned transaction and descriptive message
 */
const buildDirectBuyTransaction = async (connection, params) => {
    const { mint, buyer, amount_sol, slippage_bps = 100, message, quote } = params;
    return buildBuyTransactionInternal(connection, mint, buyer, amount_sol, slippage_bps, message, undefined, quote);
};
exports.buildDirectBuyTransaction = buildDirectBuyTransaction;
// ── Sign-and-send helpers (Phantom / wallet-integrated flows) ────────
/**
 * Build, simulate, and submit a vault-funded buy via signAndSendTransaction.
 *
 * This is the recommended path for Phantom and other browser wallets.
 * The wallet receives the final, immutable transaction for atomic sign+send,
 * which avoids false-positive "malicious dapp" warnings.
 *
 * @returns Transaction signature on success
 */
const sendBuy = async (connection, wallet, params) => {
    const fullParams = { ...params, buyer: wallet.publicKey.toBase58() };
    const { transaction, migrationTransaction } = await (0, exports.buildBuyTransaction)(connection, fullParams);
    const sim = await connection.simulateTransaction(transaction, { sigVerify: false });
    if (sim.value.err) {
        throw new Error(`Buy simulation failed: ${JSON.stringify(sim.value.err)}`);
    }
    const { signature } = await wallet.signAndSendTransaction(transaction);
    if (migrationTransaction) {
        const migSim = await connection.simulateTransaction(migrationTransaction, { sigVerify: false });
        if (!migSim.value.err) {
            await wallet.signAndSendTransaction(migrationTransaction);
        }
    }
    return signature;
};
exports.sendBuy = sendBuy;
/**
 * Build, simulate, and submit a direct buy (no vault) via signAndSendTransaction.
 *
 * Same Phantom-friendly flow as sendBuy but buyer pays from their own wallet.
 *
 * @returns Transaction signature on success
 */
const sendDirectBuy = async (connection, wallet, params) => {
    const fullParams = { ...params, buyer: wallet.publicKey.toBase58() };
    const { transaction, migrationTransaction } = await (0, exports.buildDirectBuyTransaction)(connection, fullParams);
    const sim = await connection.simulateTransaction(transaction, { sigVerify: false });
    if (sim.value.err) {
        throw new Error(`Buy simulation failed: ${JSON.stringify(sim.value.err)}`);
    }
    const { signature } = await wallet.signAndSendTransaction(transaction);
    if (migrationTransaction) {
        const migSim = await connection.simulateTransaction(migrationTransaction, { sigVerify: false });
        if (!migSim.value.err) {
            await wallet.signAndSendTransaction(migrationTransaction);
        }
    }
    return signature;
};
exports.sendDirectBuy = sendDirectBuy;
// ============================================================================
// Sell
// ============================================================================
/**
 * Build an unsigned sell transaction.
 *
 * @param connection - Solana RPC connection
 * @param params - Sell parameters (mint, seller, amount_tokens in raw units, optional slippage_bps)
 * @returns Unsigned transaction and descriptive message
 */
const buildSellTransaction = async (connection, params) => {
    const { mint: mintStr, seller: sellerStr, amount_tokens, slippage_bps = 100, message, vault: vaultCreatorStr, quote, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const seller = new web3_js_1.PublicKey(sellerStr);
    const tokenData = await (0, tokens_1.fetchTokenRaw)(connection, mint);
    if (!tokenData)
        throw new Error(`Token not found: ${mintStr}`);
    const { bondingCurve } = tokenData;
    // Migrated token — route through vault swap on Raydium DEX
    if (quote?.source === 'dex' || bondingCurve.bonding_complete) {
        if (!vaultCreatorStr) {
            throw new Error('Migrated tokens require vault-based trading. Use buildSellTransaction with a vault parameter.');
        }
        const resolvedQuote = quote ?? (await (0, quotes_1.getSellQuote)(connection, mintStr, amount_tokens));
        const slippage = slippage_bps ?? 100;
        const minOut = (BigInt(resolvedQuote.min_output_sol) * BigInt(10000 - slippage)) / BigInt(10000);
        const result = await buildVaultSwapTransaction(connection, {
            mint: mintStr,
            signer: sellerStr,
            vault_creator: vaultCreatorStr,
            amount_in: amount_tokens,
            minimum_amount_out: Number(minOut),
            is_buy: false,
            message,
        });
        return {
            ...result,
            message: `Sell ${amount_tokens / 1e6} tokens for ~${resolvedQuote.output_sol / 1e9} SOL (via DEX)`,
        };
    }
    // Calculate expected output
    const virtualSol = BigInt(bondingCurve.virtual_sol_reserves.toString());
    const virtualTokens = BigInt(bondingCurve.virtual_token_reserves.toString());
    const tokenAmount = BigInt(amount_tokens);
    const result = (0, program_1.calculateSolOut)(tokenAmount, virtualSol, virtualTokens);
    // Apply slippage
    if (slippage_bps < 10 || slippage_bps > 1000) {
        throw new Error(`slippage_bps must be between 10 (0.1%) and 1000 (10%), got ${slippage_bps}`);
    }
    const slippage = slippage_bps;
    const minSol = (result.solToUser * BigInt(10000 - slippage)) / BigInt(10000);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [userPositionPda] = (0, program_1.getUserPositionPda)(bondingCurvePda, seller);
    const [userStatsPda] = (0, program_1.getUserStatsPda)(seller);
    // [V35] Optional accounts — check existence before passing (Anchor needs
    // program ID for None, not a non-existent PDA address)
    const [userPositionInfo, userStatsInfo] = await connection.getMultipleAccountsInfo([
        userPositionPda,
        userStatsPda,
    ]);
    const userPositionAccount = userPositionInfo ? userPositionPda : null;
    const userStatsAccount = userStatsInfo ? userStatsPda : null;
    const bondingCurveTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, bondingCurvePda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const sellerTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, seller, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Vault accounts (optional — pass null when not using vault)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, seller);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(seller, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, seller);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const sellIx = await program.methods
        .sell({
        tokenAmount: new anchor_1.BN(amount_tokens.toString()),
        minSolOut: new anchor_1.BN(minSol.toString()),
    })
        .accounts({
        seller,
        mint,
        bondingCurve: bondingCurvePda,
        tokenVault: bondingCurveTokenAccount,
        sellerTokenAccount,
        userPosition: userPositionAccount,
        tokenTreasury: treasuryPda,
        userStats: userStatsAccount,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(sellIx);
    addMemoIx(tx, seller, message);
    const versionedTx = await finalizeTransaction(connection, tx, seller);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Sell ${Number(tokenAmount) / 1e6} tokens for ${Number(result.solToUser) / 1e9} SOL${vaultLabel}`,
    };
};
exports.buildSellTransaction = buildSellTransaction;
// ============================================================================
// Create Token
// ============================================================================
/**
 * Build an unsigned create token transaction.
 *
 * Returns the transaction (partially signed by the mint keypair) and the mint keypair
 * so the agent can extract the mint address.
 *
 * @param connection - Solana RPC connection
 * @param params - Create parameters (creator, name, symbol, metadata_uri)
 * @returns Partially-signed transaction, mint PublicKey, and mint Keypair
 */
const buildCreateTokenTransaction = async (connection, params) => {
    const { creator: creatorStr, name, symbol, metadata_uri, sol_target = 0, community_token = true, } = params;
    const creator = new web3_js_1.PublicKey(creatorStr);
    if (name.length > 32)
        throw new Error('Name must be 32 characters or less');
    if (symbol.length > 10)
        throw new Error('Symbol must be 10 characters or less');
    // Grind for vanity "tm" suffix
    let mint;
    const maxAttempts = 500000;
    let attempts = 0;
    while (true) {
        mint = web3_js_1.Keypair.generate();
        attempts++;
        if (mint.publicKey.toBase58().endsWith('tm'))
            break;
        if (attempts >= maxAttempts)
            break;
    }
    // Derive PDAs
    const [globalConfig] = (0, program_1.getGlobalConfigPda)();
    const [bondingCurve] = (0, program_1.getBondingCurvePda)(mint.publicKey);
    const [treasury] = (0, program_1.getTokenTreasuryPda)(mint.publicKey);
    const bondingCurveTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint.publicKey, bondingCurve, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const treasuryTokenAccount = (0, program_1.getTreasuryTokenAccount)(mint.publicKey, treasury);
    // [V27] Treasury lock PDA and its token ATA
    const [treasuryLock] = (0, program_1.getTreasuryLockPda)(mint.publicKey);
    const treasuryLockTokenAccount = (0, program_1.getTreasuryLockTokenAccount)(mint.publicKey, treasuryLock);
    const tx = new web3_js_1.Transaction();
    const provider = makeDummyProvider(connection, creator);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const createIx = await program.methods
        .createToken({
        name,
        symbol,
        uri: metadata_uri,
        solTarget: new anchor_1.BN(sol_target),
        communityToken: community_token,
    })
        .accounts({
        creator,
        globalConfig,
        mint: mint.publicKey,
        bondingCurve,
        tokenVault: bondingCurveTokenAccount,
        treasury,
        treasuryTokenAccount,
        treasuryLock,
        treasuryLockTokenAccount,
        token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
        rent: web3_js_1.SYSVAR_RENT_PUBKEY,
    })
        .instruction();
    tx.add(createIx);
    const versionedTx = await finalizeTransaction(connection, tx, creator);
    // Partially sign with mint keypair
    versionedTx.sign([mint]);
    return {
        transaction: versionedTx,
        mint: mint.publicKey,
        mintKeypair: mint,
        message: `Create token "${name}" ($${symbol})`,
    };
};
exports.buildCreateTokenTransaction = buildCreateTokenTransaction;
/**
 * Build, simulate, and submit a create token via signAndSendTransaction.
 *
 * Phantom-friendly: simulates with sigVerify: false (mint keypair is already
 * partially signed), then hands the tx to the wallet for the creator signature.
 * Avoids the "malicious dapp" warning caused by Phantom trying to simulate a
 * partially-signed transaction.
 *
 * @returns { signature, mint } on success
 */
const sendCreateToken = async (connection, wallet, params) => {
    const fullParams = { ...params, creator: wallet.publicKey.toBase58() };
    const { transaction, mint } = await (0, exports.buildCreateTokenTransaction)(connection, fullParams);
    const sim = await connection.simulateTransaction(transaction, { sigVerify: false });
    if (sim.value.err) {
        throw new Error(`Create token simulation failed: ${JSON.stringify(sim.value.err)}`);
    }
    const { signature } = await wallet.signAndSendTransaction(transaction);
    return { signature, mint };
};
exports.sendCreateToken = sendCreateToken;
// ============================================================================
// Star
// ============================================================================
/**
 * Build an unsigned star transaction (costs 0.05 SOL).
 *
 * @param connection - Solana RPC connection
 * @param params - Star parameters (mint, user)
 * @returns Unsigned transaction and descriptive message
 */
const buildStarTransaction = async (connection, params) => {
    const { mint: mintStr, user: userStr, vault: vaultCreatorStr } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const user = new web3_js_1.PublicKey(userStr);
    const tokenData = await (0, tokens_1.fetchTokenRaw)(connection, mint);
    if (!tokenData)
        throw new Error(`Token not found: ${mintStr}`);
    const { bondingCurve } = tokenData;
    if (user.equals(bondingCurve.creator)) {
        throw new Error('Cannot star your own token');
    }
    // Check if already starred
    const [starRecordPda] = (0, program_1.getStarRecordPda)(user, mint);
    const starRecord = await connection.getAccountInfo(starRecordPda);
    if (starRecord)
        throw new Error('Already starred this token');
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    // Vault accounts (optional — vault pays star cost)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, user);
    const tx = new web3_js_1.Transaction();
    const provider = makeDummyProvider(connection, user);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const starIx = await program.methods
        .starToken()
        .accounts({
        user,
        mint,
        bondingCurve: bondingCurvePda,
        tokenTreasury: treasuryPda,
        creator: bondingCurve.creator,
        starRecord: starRecordPda,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(starIx);
    const versionedTx = await finalizeTransaction(connection, tx, user);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Star token (costs 0.05 SOL)${vaultLabel}`,
    };
};
exports.buildStarTransaction = buildStarTransaction;
// ============================================================================
// Message
// ============================================================================
// ============================================================================
// Vault (V2.0)
// ============================================================================
/**
 * Build an unsigned create vault transaction.
 *
 * Creates a TorchVault PDA and auto-links the creator's wallet.
 *
 * @param connection - Solana RPC connection
 * @param params - Creator public key
 * @returns Unsigned transaction
 */
const buildCreateVaultTransaction = async (connection, params) => {
    const creator = new web3_js_1.PublicKey(params.creator);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(creator);
    const [walletLinkPda] = (0, program_1.getVaultWalletLinkPda)(creator);
    const provider = makeDummyProvider(connection, creator);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .createVault()
        .accounts({
        creator,
        vault: vaultPda,
        walletLink: walletLinkPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, creator);
    return {
        transaction: versionedTx,
        message: `Create vault for ${params.creator.slice(0, 8)}...`,
    };
};
exports.buildCreateVaultTransaction = buildCreateVaultTransaction;
/**
 * Build an unsigned deposit vault transaction.
 *
 * Anyone can deposit SOL into any vault.
 *
 * @param connection - Solana RPC connection
 * @param params - Depositor, vault creator, amount in lamports
 * @returns Unsigned transaction
 */
const buildDepositVaultTransaction = async (connection, params) => {
    const depositor = new web3_js_1.PublicKey(params.depositor);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const provider = makeDummyProvider(connection, depositor);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .depositVault(new anchor_1.BN(params.amount_sol.toString()))
        .accounts({
        depositor,
        vault: vaultPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, depositor);
    return {
        transaction: versionedTx,
        message: `Deposit ${params.amount_sol / 1e9} SOL into vault`,
    };
};
exports.buildDepositVaultTransaction = buildDepositVaultTransaction;
/**
 * Build an unsigned withdraw vault transaction.
 *
 * Only the vault authority can withdraw.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, amount in lamports
 * @returns Unsigned transaction
 */
const buildWithdrawVaultTransaction = async (connection, params) => {
    const authority = new web3_js_1.PublicKey(params.authority);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .withdrawVault(new anchor_1.BN(params.amount_sol.toString()))
        .accounts({
        authority,
        vault: vaultPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Withdraw ${params.amount_sol / 1e9} SOL from vault`,
    };
};
exports.buildWithdrawVaultTransaction = buildWithdrawVaultTransaction;
/**
 * Build an unsigned link wallet transaction.
 *
 * Only the vault authority can link wallets.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, wallet to link
 * @returns Unsigned transaction
 */
const buildLinkWalletTransaction = async (connection, params) => {
    const authority = new web3_js_1.PublicKey(params.authority);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const walletToLink = new web3_js_1.PublicKey(params.wallet_to_link);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const [walletLinkPda] = (0, program_1.getVaultWalletLinkPda)(walletToLink);
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .linkWallet()
        .accounts({
        authority,
        vault: vaultPda,
        walletToLink,
        walletLink: walletLinkPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Link wallet ${params.wallet_to_link.slice(0, 8)}... to vault`,
    };
};
exports.buildLinkWalletTransaction = buildLinkWalletTransaction;
/**
 * Build an unsigned unlink wallet transaction.
 *
 * Only the vault authority can unlink wallets. Rent returns to authority.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, wallet to unlink
 * @returns Unsigned transaction
 */
const buildUnlinkWalletTransaction = async (connection, params) => {
    const authority = new web3_js_1.PublicKey(params.authority);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const walletToUnlink = new web3_js_1.PublicKey(params.wallet_to_unlink);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const [walletLinkPda] = (0, program_1.getVaultWalletLinkPda)(walletToUnlink);
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .unlinkWallet()
        .accounts({
        authority,
        vault: vaultPda,
        walletToUnlink,
        walletLink: walletLinkPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Unlink wallet ${params.wallet_to_unlink.slice(0, 8)}... from vault`,
    };
};
exports.buildUnlinkWalletTransaction = buildUnlinkWalletTransaction;
/**
 * Build an unsigned transfer authority transaction.
 *
 * Transfers vault admin control to a new wallet.
 *
 * @param connection - Solana RPC connection
 * @param params - Current authority, vault creator, new authority
 * @returns Unsigned transaction
 */
const buildTransferAuthorityTransaction = async (connection, params) => {
    const authority = new web3_js_1.PublicKey(params.authority);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const newAuthority = new web3_js_1.PublicKey(params.new_authority);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .transferAuthority()
        .accounts({
        authority,
        vault: vaultPda,
        newAuthority,
    })
        .instruction();
    const tx = new web3_js_1.Transaction().add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Transfer vault authority to ${params.new_authority.slice(0, 8)}...`,
    };
};
exports.buildTransferAuthorityTransaction = buildTransferAuthorityTransaction;
// ============================================================================
// Borrow (V2.4)
// ============================================================================
/**
 * Build an unsigned borrow transaction.
 *
 * Lock tokens as collateral in the collateral vault and receive SOL from treasury.
 * Token must be migrated (has Raydium pool for price calculation).
 *
 * @param connection - Solana RPC connection
 * @param params - Borrow parameters (mint, borrower, collateral_amount, sol_to_borrow)
 * @returns Unsigned transaction and descriptive message
 */
const buildBorrowTransaction = async (connection, params) => {
    const { mint: mintStr, borrower: borrowerStr, collateral_amount, sol_to_borrow, vault: vaultCreatorStr, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const borrower = new web3_js_1.PublicKey(borrowerStr);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [collateralVaultPda] = (0, program_1.getCollateralVaultPda)(mint);
    const [loanPositionPda] = (0, program_1.getLoanPositionPda)(mint, borrower);
    const borrowerTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, borrower, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Get Raydium pool accounts for price calculation
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    // Vault accounts (optional — collateral from vault ATA, SOL to vault)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, borrower);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // borrower_token_account is mut + non-optional in the borrow instruction,
    // so the on-chain handler requires it to exist even in vault mode (collateral
    // flows vault → borrower ATA → collateral_vault).
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(borrower, borrowerTokenAccount, borrower, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(borrower, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, borrower);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const borrowIx = await program.methods
        .borrow({
        collateralAmount: new anchor_1.BN(collateral_amount.toString()),
        solToBorrow: new anchor_1.BN(sol_to_borrow.toString()),
    })
        .accounts({
        borrower,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        collateralVault: collateralVaultPda,
        borrowerTokenAccount,
        loanPosition: loanPositionPda,
        poolState: raydium.poolState,
        tokenVault0: raydium.token0Vault,
        tokenVault1: raydium.token1Vault,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(borrowIx);
    const versionedTx = await finalizeTransaction(connection, tx, borrower);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Borrow ${Number(sol_to_borrow) / 1e9} SOL with ${Number(collateral_amount) / 1e6} tokens as collateral${vaultLabel}`,
    };
};
exports.buildBorrowTransaction = buildBorrowTransaction;
// ============================================================================
// Repay (V2.4)
// ============================================================================
/**
 * Build an unsigned repay transaction.
 *
 * Repay SOL debt. Interest is paid first, then principal.
 * Full repay returns all collateral and closes the position.
 *
 * @param connection - Solana RPC connection
 * @param params - Repay parameters (mint, borrower, sol_amount)
 * @returns Unsigned transaction and descriptive message
 */
const buildRepayTransaction = async (connection, params) => {
    const { mint: mintStr, borrower: borrowerStr, sol_amount, vault: vaultCreatorStr } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const borrower = new web3_js_1.PublicKey(borrowerStr);
    // Derive PDAs
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [collateralVaultPda] = (0, program_1.getCollateralVaultPda)(mint);
    const [loanPositionPda] = (0, program_1.getLoanPositionPda)(mint, borrower);
    const borrowerTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, borrower, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Vault accounts (optional — SOL from vault, collateral returns to vault ATA)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, borrower);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // borrower_token_account is mut + non-optional; must exist even in vault mode.
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(borrower, borrowerTokenAccount, borrower, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(borrower, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, borrower);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const repayIx = await program.methods
        .repay(new anchor_1.BN(sol_amount.toString()))
        .accounts({
        borrower,
        mint,
        treasury: treasuryPda,
        collateralVault: collateralVaultPda,
        borrowerTokenAccount,
        loanPosition: loanPositionPda,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(repayIx);
    const versionedTx = await finalizeTransaction(connection, tx, borrower);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Repay ${Number(sol_amount) / 1e9} SOL${vaultLabel}`,
    };
};
exports.buildRepayTransaction = buildRepayTransaction;
// ============================================================================
// Liquidate (V2.4)
// ============================================================================
/**
 * Build an unsigned liquidate transaction.
 *
 * Permissionless — anyone can call when a borrower's LTV exceeds the
 * liquidation threshold. Liquidator pays SOL and receives collateral + bonus.
 *
 * @param connection - Solana RPC connection
 * @param params - Liquidate parameters (mint, liquidator, borrower)
 * @returns Unsigned transaction and descriptive message
 */
const buildLiquidateTransaction = async (connection, params) => {
    const { mint: mintStr, liquidator: liquidatorStr, borrower: borrowerStr, vault: vaultCreatorStr, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const liquidator = new web3_js_1.PublicKey(liquidatorStr);
    const borrower = new web3_js_1.PublicKey(borrowerStr);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [collateralVaultPda] = (0, program_1.getCollateralVaultPda)(mint);
    const [loanPositionPda] = (0, program_1.getLoanPositionPda)(mint, borrower);
    const liquidatorTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, liquidator, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Get Raydium pool accounts for price calculation
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    // Vault accounts (optional — SOL from vault, collateral to vault ATA)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, liquidator);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // Create liquidator ATA if needed
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(liquidator, liquidatorTokenAccount, liquidator, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(liquidator, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, liquidator);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const liquidateIx = await program.methods
        .liquidate()
        .accounts({
        liquidator,
        borrower,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        collateralVault: collateralVaultPda,
        liquidatorTokenAccount,
        loanPosition: loanPositionPda,
        poolState: raydium.poolState,
        tokenVault0: raydium.token0Vault,
        tokenVault1: raydium.token1Vault,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(liquidateIx);
    const versionedTx = await finalizeTransaction(connection, tx, liquidator);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Liquidate loan position for ${borrowerStr.slice(0, 8)}...${vaultLabel}`,
    };
};
exports.buildLiquidateTransaction = buildLiquidateTransaction;
// ============================================================================
// Claim Protocol Rewards
// ============================================================================
/**
 * Build an unsigned claim protocol rewards transaction.
 *
 * Claims the user's proportional share of protocol treasury rewards
 * based on trading volume in the previous epoch. Requires >= 2 SOL volume. Min claim: 0.1 SOL.
 *
 * @param connection - Solana RPC connection
 * @param params - Claim parameters (user, optional vault)
 * @returns Unsigned transaction and descriptive message
 */
const buildClaimProtocolRewardsTransaction = async (connection, params) => {
    const { user: userStr, vault: vaultCreatorStr } = params;
    const user = new web3_js_1.PublicKey(userStr);
    // Derive PDAs
    const [userStatsPda] = (0, program_1.getUserStatsPda)(user);
    const [protocolTreasuryPda] = (0, program_1.getProtocolTreasuryPda)();
    // Vault accounts (optional — rewards go to vault instead of user)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, user);
    const tx = new web3_js_1.Transaction();
    const provider = makeDummyProvider(connection, user);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const claimIx = await program.methods
        .claimProtocolRewards()
        .accounts({
        user,
        userStats: userStatsPda,
        protocolTreasury: protocolTreasuryPda,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(claimIx);
    const versionedTx = await finalizeTransaction(connection, tx, user);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Claim protocol rewards${vaultLabel}`,
    };
};
exports.buildClaimProtocolRewardsTransaction = buildClaimProtocolRewardsTransaction;
// ============================================================================
// Reclaim Failed Token (V4)
// ============================================================================
/**
 * Build an unsigned reclaim-failed-token transaction.
 *
 * Permissionless — anyone can reclaim a failed token that has been
 * inactive for 7+ days and hasn't completed bonding.
 * SOL from both bonding curve and token treasury goes to protocol treasury.
 */
const buildReclaimFailedTokenTransaction = async (connection, params) => {
    const { payer: payerStr, mint: mintStr } = params;
    const payer = new web3_js_1.PublicKey(payerStr);
    const mint = new web3_js_1.PublicKey(mintStr);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [tokenTreasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [protocolTreasuryPda] = (0, program_1.getProtocolTreasuryPda)();
    const tx = new web3_js_1.Transaction();
    const provider = makeDummyProvider(connection, payer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .reclaimFailedToken()
        .accounts({
        payer,
        mint,
        bondingCurve: bondingCurvePda,
        tokenTreasury: tokenTreasuryPda,
        protocolTreasury: protocolTreasuryPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, payer);
    return {
        transaction: versionedTx,
        message: `Reclaim failed token ${mintStr.slice(0, 8)}...`,
    };
};
exports.buildReclaimFailedTokenTransaction = buildReclaimFailedTokenTransaction;
// ============================================================================
// Withdraw Tokens (V18)
// ============================================================================
/**
 * Build an unsigned withdraw tokens transaction.
 *
 * Withdraw tokens from a vault ATA to any destination token account.
 * Authority only. Composability escape hatch for external DeFi.
 *
 * @param connection - Solana RPC connection
 * @param params - Authority, vault creator, mint, destination, amount in raw units
 * @returns Unsigned transaction
 */
const buildWithdrawTokensTransaction = async (connection, params) => {
    const authority = new web3_js_1.PublicKey(params.authority);
    const vaultCreator = new web3_js_1.PublicKey(params.vault_creator);
    const mint = new web3_js_1.PublicKey(params.mint);
    const destination = new web3_js_1.PublicKey(params.destination);
    const [vaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const vaultTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, vaultPda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const destinationTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, destination, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    const tx = new web3_js_1.Transaction();
    // Create destination ATA if needed
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(authority, destinationTokenAccount, destination, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .withdrawTokens(new anchor_1.BN(params.amount.toString()))
        .accounts({
        authority,
        vault: vaultPda,
        mint,
        vaultTokenAccount,
        destinationTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
    })
        .instruction();
    tx.add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Withdraw ${params.amount} tokens from vault to ${params.destination.slice(0, 8)}...`,
    };
};
exports.buildWithdrawTokensTransaction = buildWithdrawTokensTransaction;
// ============================================================================
// Vault Swap (V19)
// ============================================================================
// ============================================================================
// Migration (V26)
// ============================================================================
// build an unsigned migration transaction.
// permissionless — anyone can call once bonding completes.
// combines fund_migration_wsol + migrate_to_dex and creates a Raydium CPMM pool with LP tokens burned.
// payer fronts ~1 SOL for Raydium pool creation + account rent; treasury reimburses in the same tx (net cost: 0).
// when a buy completes bonding, buildBuyTransaction returns a separate migrationTransaction — the caller is
// expected to send both. Call buildMigrateTransaction directly only if that second tx was never sent.
const buildMigrateTransaction = async (connection, params) => {
    const { mint: mintStr, payer: payerStr } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const payer = new web3_js_1.PublicKey(payerStr);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [globalConfigPda] = (0, program_1.getGlobalConfigPda)();
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const treasuryTokenAccount = (0, program_1.getTreasuryTokenAccount)(mint, treasuryPda);
    const [treasuryLock] = (0, program_1.getTreasuryLockPda)(mint);
    const treasuryLockTokenAccount = (0, program_1.getTreasuryLockTokenAccount)(mint, treasuryLock);
    // Token vault = bonding curve's Token-2022 ATA
    const tokenVault = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, bondingCurvePda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Bonding curve's WSOL ATA (SPL Token, not Token-2022)
    const bcWsol = (0, spl_token_1.getAssociatedTokenAddressSync)(constants_1.WSOL_MINT, bondingCurvePda, true, spl_token_1.TOKEN_PROGRAM_ID);
    // Payer's WSOL ATA
    const payerWsol = (0, spl_token_1.getAssociatedTokenAddressSync)(constants_1.WSOL_MINT, payer, false, spl_token_1.TOKEN_PROGRAM_ID);
    // Payer's token ATA (Token-2022)
    const payerToken = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, payer, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Raydium accounts
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    const payerLpToken = (0, spl_token_1.getAssociatedTokenAddressSync)(raydium.lpMint, payer, false, spl_token_1.TOKEN_PROGRAM_ID);
    const tx = new web3_js_1.Transaction();
    // Compute budget — migration is heavy
    tx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: 400000 }));
    // Create ATAs: bc_wsol, payer_wsol, payer_token
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(payer, bcWsol, bondingCurvePda, constants_1.WSOL_MINT, spl_token_1.TOKEN_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID), (0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(payer, payerWsol, payer, constants_1.WSOL_MINT, spl_token_1.TOKEN_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID), (0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(payer, payerToken, payer, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    // Build program instructions
    const provider = makeDummyProvider(connection, payer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    // Step 1: Fund bonding curve's WSOL ATA (direct lamport manipulation, no CPI)
    const fundIx = await program.methods
        .fundMigrationWsol()
        .accounts({
        payer,
        mint,
        bondingCurve: bondingCurvePda,
        bcWsol,
    })
        .instruction();
    // Step 2: Migrate to DEX (all CPI-based)
    const migrateIx = await program.methods
        .migrateToDex()
        .accounts({
        payer,
        globalConfig: globalConfigPda,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        tokenVault,
        treasuryTokenAccount,
        treasuryLockTokenAccount,
        treasuryLock,
        bcWsol,
        payerWsol,
        payerToken,
        raydiumProgram: (0, constants_1.getRaydiumCpmmProgram)(),
        ammConfig: (0, constants_1.getRaydiumAmmConfig)(),
        raydiumAuthority: raydium.raydiumAuthority,
        poolState: raydium.poolState,
        wsolMint: constants_1.WSOL_MINT,
        token0Vault: raydium.token0Vault,
        token1Vault: raydium.token1Vault,
        lpMint: raydium.lpMint,
        payerLpToken,
        observationState: raydium.observationState,
        createPoolFee: (0, constants_1.getRaydiumFeeReceiver)(),
        tokenProgram: spl_token_1.TOKEN_PROGRAM_ID,
        token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
        rent: web3_js_1.SYSVAR_RENT_PUBKEY,
    })
        .instruction();
    tx.add(fundIx, migrateIx);
    const versionedTx = await finalizeTransaction(connection, tx, payer);
    return {
        transaction: versionedTx,
        message: `Migrate token ${mintStr.slice(0, 8)}... to Raydium DEX`,
    };
};
exports.buildMigrateTransaction = buildMigrateTransaction;
// ============================================================================
// Vault Swap (V19)
// ============================================================================
/**
 * Build an unsigned vault-routed DEX swap transaction.
 *
 * Executes a Raydium CPMM swap through the vault PDA for migrated Torch tokens.
 * Full custody preserved — all value flows through the vault.
 *
 * @param connection - Solana RPC connection
 * @param params - Swap parameters (mint, signer, vault_creator, amount_in, minimum_amount_out, is_buy)
 * @returns Unsigned transaction and descriptive message
 */
const buildVaultSwapTransaction = async (connection, params) => {
    const { mint: mintStr, signer: signerStr, vault_creator: vaultCreatorStr, amount_in, minimum_amount_out, is_buy, message, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const signer = new web3_js_1.PublicKey(signerStr);
    const vaultCreator = new web3_js_1.PublicKey(vaultCreatorStr);
    // Derive vault PDAs
    const [torchVaultPda] = (0, program_1.getTorchVaultPda)(vaultCreator);
    const [vaultWalletLinkPda] = (0, program_1.getVaultWalletLinkPda)(signer);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    // Vault's token ATA (Token-2022)
    const vaultTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, torchVaultPda, true, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Vault's WSOL ATA (SPL Token — persistent, reused across swaps)
    const vaultWsolAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(constants_1.WSOL_MINT, torchVaultPda, true, spl_token_1.TOKEN_PROGRAM_ID);
    // Raydium pool accounts
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    const tx = new web3_js_1.Transaction();
    // Create vault token ATA if needed (for first buy of a migrated token)
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(signer, vaultTokenAccount, torchVaultPda, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    // Create vault WSOL ATA if needed (persistent — reused across swaps)
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(signer, vaultWsolAccount, torchVaultPda, constants_1.WSOL_MINT, spl_token_1.TOKEN_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    const provider = makeDummyProvider(connection, signer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    // On buy: fund WSOL with lamports from vault in a separate instruction
    // (isolates direct lamport manipulation from CPIs to avoid runtime balance errors)
    if (is_buy) {
        const fundIx = await program.methods
            .fundVaultWsol(new anchor_1.BN(amount_in.toString()))
            .accounts({
            signer,
            torchVault: torchVaultPda,
            vaultWalletLink: vaultWalletLinkPda,
            vaultWsolAccount,
        })
            .instruction();
        tx.add(fundIx);
    }
    const swapIx = await program.methods
        .vaultSwap(new anchor_1.BN(amount_in.toString()), new anchor_1.BN(minimum_amount_out.toString()), is_buy)
        .accounts({
        signer,
        torchVault: torchVaultPda,
        vaultWalletLink: vaultWalletLinkPda,
        mint,
        bondingCurve: bondingCurvePda,
        vaultTokenAccount,
        vaultWsolAccount,
        raydiumProgram: (0, constants_1.getRaydiumCpmmProgram)(),
        raydiumAuthority: raydium.raydiumAuthority,
        ammConfig: (0, constants_1.getRaydiumAmmConfig)(),
        poolState: raydium.poolState,
        poolTokenVault0: raydium.token0Vault,
        poolTokenVault1: raydium.token1Vault,
        observationState: raydium.observationState,
        wsolMint: constants_1.WSOL_MINT,
        tokenProgram: spl_token_1.TOKEN_PROGRAM_ID,
        token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(swapIx);
    // Vault swap txs are larger, so truncate message to 280 chars
    addMemoIx(tx, signer, message, 280);
    const versionedTx = await finalizeTransaction(connection, tx, signer);
    const direction = is_buy ? 'Buy' : 'Sell';
    const amountLabel = is_buy ? `${amount_in / 1e9} SOL` : `${amount_in / 1e6} tokens`;
    return {
        transaction: versionedTx,
        message: `${direction} ${amountLabel} via vault DEX swap`,
    };
};
// ============================================================================
// Treasury Cranks
// ============================================================================
// permissionless crank — rolls the protocol epoch forward so the previous epoch's
// trading-volume-weighted rewards become claimable via buildClaimProtocolRewardsTransaction.
// safe to call repeatedly; the program no-ops if the current epoch hasn't elapsed.
const buildAdvanceProtocolEpochTransaction = async (connection, params) => {
    const { payer: payerStr } = params;
    const payer = new web3_js_1.PublicKey(payerStr);
    const [protocolTreasuryPda] = (0, program_1.getProtocolTreasuryPda)();
    const provider = makeDummyProvider(connection, payer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const ix = await program.methods
        .advanceProtocolEpoch()
        .accounts({ payer, protocolTreasury: protocolTreasuryPda })
        .instruction();
    const tx = new web3_js_1.Transaction();
    tx.add(ix);
    const versionedTx = await finalizeTransaction(connection, tx, payer);
    return { transaction: versionedTx, message: 'Advance protocol epoch' };
};
exports.buildAdvanceProtocolEpochTransaction = buildAdvanceProtocolEpochTransaction;
/**
 * Build an unsigned harvest-fees transaction.
 *
 * Permissionless crank — harvests accumulated Token-2022 transfer fees
 * from token accounts into the mint, then withdraws from the mint into
 * the treasury's token account.
 *
 * If `params.sources` is provided, uses those accounts directly.
 * Otherwise auto-discovers token accounts with withheld fees.
 */
const buildHarvestFeesTransaction = async (connection, params) => {
    const { mint: mintStr, payer: payerStr, sources: sourcesStr } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const payer = new web3_js_1.PublicKey(payerStr);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const treasuryTokenAccount = (0, program_1.getTreasuryTokenAccount)(mint, treasuryPda);
    // Discover source accounts with withheld transfer fees
    let sourceAccounts;
    if (sourcesStr && sourcesStr.length > 0) {
        sourceAccounts = sourcesStr.map((s) => new web3_js_1.PublicKey(s));
    }
    else {
        // Auto-discover: fetch largest token accounts and filter to those with withheld > 0
        try {
            const largestAccounts = await connection.getTokenLargestAccounts(mint, 'confirmed');
            const addresses = largestAccounts.value.map((a) => a.address);
            if (addresses.length > 0) {
                const accountInfos = await connection.getMultipleAccountsInfo(addresses);
                sourceAccounts = [];
                for (let i = 0; i < addresses.length; i++) {
                    const info = accountInfos[i];
                    if (!info)
                        continue;
                    try {
                        const account = (0, spl_token_1.unpackAccount)(addresses[i], info, spl_token_1.TOKEN_2022_PROGRAM_ID);
                        const feeAmount = (0, spl_token_1.getTransferFeeAmount)(account);
                        if (feeAmount && feeAmount.withheldAmount > BigInt(0)) {
                            sourceAccounts.push(addresses[i]);
                        }
                    }
                    catch {
                        // Not a Token-2022 account or can't decode — skip
                    }
                }
            }
            else {
                sourceAccounts = [];
            }
        }
        catch {
            // RPC doesn't support getTokenLargestAccounts — proceed without source accounts
            sourceAccounts = [];
        }
    }
    const provider = makeDummyProvider(connection, payer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const tx = new web3_js_1.Transaction();
    // Scale compute budget: base 200k + 20k per source account (Token-2022 harvest CPI is expensive)
    const computeUnits = 200000 + 20000 * sourceAccounts.length;
    tx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: computeUnits }));
    const harvestIx = await program.methods
        .harvestFees()
        .accounts({
        payer,
        mint,
        bondingCurve: bondingCurvePda,
        tokenTreasury: treasuryPda,
        treasuryTokenAccount,
        token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
        associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
    })
        .remainingAccounts(sourceAccounts.map((pubkey) => ({
        pubkey,
        isSigner: false,
        isWritable: true,
    })))
        .instruction();
    tx.add(harvestIx);
    const versionedTx = await finalizeTransaction(connection, tx, payer);
    return {
        transaction: versionedTx,
        message: `Harvest transfer fees for ${mintStr.slice(0, 8)}... (${sourceAccounts.length} source accounts)`,
    };
};
exports.buildHarvestFeesTransaction = buildHarvestFeesTransaction;
/** Max transaction size in bytes (Solana packet data limit) */
const PACKET_DATA_SIZE = 1232;
/**
 * [V20] Harvest transfer fees AND swap them to SOL.
 *
 * Tries to bundle: create_idempotent(treasury_wsol) + harvest_fees + swap_fees_to_sol.
 * If the combined transaction exceeds the 1232-byte limit (many source accounts),
 * automatically splits into a harvest-only tx + swap-only tx via additionalTransactions.
 * Set harvest=false to skip harvest (if already harvested separately).
 */
const buildSwapFeesToSolTransaction = async (connection, params) => {
    const { mint: mintStr, payer: payerStr, minimum_amount_out = 1, harvest = true, sources: sourcesStr, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const payer = new web3_js_1.PublicKey(payerStr);
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const treasuryTokenAccount = (0, program_1.getTreasuryTokenAccount)(mint, treasuryPda);
    // Treasury's WSOL ATA (SPL Token, not Token-2022)
    const treasuryWsol = (0, spl_token_1.getAssociatedTokenAddressSync)(constants_1.WSOL_MINT, treasuryPda, true, spl_token_1.TOKEN_PROGRAM_ID);
    // Raydium accounts — swap direction is token → WSOL (sell)
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    const tokenVault = raydium.isWsolToken0 ? raydium.token1Vault : raydium.token0Vault;
    const wsolVault = raydium.isWsolToken0 ? raydium.token0Vault : raydium.token1Vault;
    const provider = makeDummyProvider(connection, payer);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    // [V34] Fetch bonding curve to get creator address for fee split
    const tokenData = await (0, tokens_1.fetchTokenRaw)(connection, mint);
    if (!tokenData)
        throw new Error(`Token not found: ${mintStr}`);
    const creator = tokenData.bondingCurve.creator;
    // Helper: build the harvest instruction with given sources
    const buildHarvestIx = async (sources) => {
        return program.methods
            .harvestFees()
            .accounts({
            payer,
            mint,
            bondingCurve: bondingCurvePda,
            tokenTreasury: treasuryPda,
            treasuryTokenAccount,
            token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
            associatedTokenProgram: spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID,
        })
            .remainingAccounts(sources.map((pubkey) => ({
            pubkey,
            isSigner: false,
            isWritable: true,
        })))
            .instruction();
    };
    // Helper: build the swap instruction
    const buildSwapIx = async () => {
        return program.methods
            .swapFeesToSol(new anchor_1.BN(minimum_amount_out.toString()))
            .accounts({
            payer,
            mint,
            bondingCurve: bondingCurvePda,
            creator,
            treasury: treasuryPda,
            treasuryTokenAccount,
            treasuryWsol,
            raydiumProgram: (0, constants_1.getRaydiumCpmmProgram)(),
            raydiumAuthority: raydium.raydiumAuthority,
            ammConfig: (0, constants_1.getRaydiumAmmConfig)(),
            poolState: raydium.poolState,
            tokenVault,
            wsolVault,
            wsolMint: constants_1.WSOL_MINT,
            observationState: raydium.observationState,
            tokenProgram: spl_token_1.TOKEN_PROGRAM_ID,
            token2022Program: spl_token_1.TOKEN_2022_PROGRAM_ID,
            systemProgram: web3_js_1.SystemProgram.programId,
        })
            .instruction();
    };
    // Helper: create WSOL ATA instruction
    const createWsolAtaIx = (0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(payer, treasuryWsol, treasuryPda, constants_1.WSOL_MINT, spl_token_1.TOKEN_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID);
    // Discover source accounts
    let sourceAccounts = [];
    if (harvest) {
        if (sourcesStr && sourcesStr.length > 0) {
            sourceAccounts = sourcesStr.map((s) => new web3_js_1.PublicKey(s));
        }
        else {
            try {
                const largestAccounts = await connection.getTokenLargestAccounts(mint, 'confirmed');
                const addresses = largestAccounts.value.map((a) => a.address);
                if (addresses.length > 0) {
                    const accountInfos = await connection.getMultipleAccountsInfo(addresses);
                    for (let i = 0; i < addresses.length; i++) {
                        const info = accountInfos[i];
                        if (!info)
                            continue;
                        try {
                            const account = (0, spl_token_1.unpackAccount)(addresses[i], info, spl_token_1.TOKEN_2022_PROGRAM_ID);
                            const feeAmount = (0, spl_token_1.getTransferFeeAmount)(account);
                            if (feeAmount && feeAmount.withheldAmount > BigInt(0)) {
                                sourceAccounts.push(addresses[i]);
                            }
                        }
                        catch {
                            // Not a Token-2022 account or can't decode — skip
                        }
                    }
                }
            }
            catch {
                sourceAccounts = [];
            }
        }
    }
    // Try combined transaction first
    const tx = new web3_js_1.Transaction();
    tx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: 400000 }));
    tx.add(createWsolAtaIx);
    if (harvest && sourceAccounts.length > 0) {
        tx.add(await buildHarvestIx(sourceAccounts));
    }
    tx.add(await buildSwapIx());
    const versionedTx = await finalizeTransaction(connection, tx, payer);
    // Check if it fits in a single transaction
    let fitsInSingleTx = false;
    try {
        const serialized = versionedTx.serialize();
        fitsInSingleTx = serialized.length <= PACKET_DATA_SIZE;
    }
    catch {
        // serialize() throws when tx exceeds size limit
    }
    if (fitsInSingleTx) {
        return {
            transaction: versionedTx,
            message: `Swap harvested fees to SOL for ${mintStr.slice(0, 8)}...${harvest ? ' (harvest + swap)' : ''}`,
        };
    }
    // Too large — split into harvest tx + swap-only tx
    // Transaction 1: harvest with all source accounts
    const harvestTx = new web3_js_1.Transaction();
    const computeUnits = 200000 + 20000 * sourceAccounts.length;
    harvestTx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: computeUnits }));
    harvestTx.add(await buildHarvestIx(sourceAccounts));
    const versionedHarvestTx = await finalizeTransaction(connection, harvestTx, payer);
    // Transaction 2: swap only (no harvest — tokens already in treasury ATA)
    const swapTx = new web3_js_1.Transaction();
    swapTx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: 400000 }));
    swapTx.add(createWsolAtaIx);
    swapTx.add(await buildSwapIx());
    const versionedSwapTx = await finalizeTransaction(connection, swapTx, payer);
    return {
        transaction: versionedHarvestTx,
        additionalTransactions: [versionedSwapTx],
        message: `Harvest + swap fees to SOL for ${mintStr.slice(0, 8)}... (split: ${sourceAccounts.length} sources)`,
    };
};
exports.buildSwapFeesToSolTransaction = buildSwapFeesToSolTransaction;
// ============================================================================
// Open Short (V5)
// ============================================================================
/**
 * Build an unsigned open_short transaction.
 *
 * Post SOL collateral and borrow tokens from treasury.
 * Mirror of borrow: same LTV, same liquidation, opposite direction.
 *
 * @param connection - Solana RPC connection
 * @param params - Open short parameters (mint, shorter, sol_collateral, tokens_to_borrow)
 * @returns Unsigned transaction and descriptive message
 */
const buildOpenShortTransaction = async (connection, params) => {
    const { mint: mintStr, shorter: shorterStr, sol_collateral, tokens_to_borrow, vault: vaultCreatorStr, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const shorter = new web3_js_1.PublicKey(shorterStr);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [treasuryLockPda] = (0, program_1.getTreasuryLockPda)(mint);
    const treasuryLockTokenAccount = (0, program_1.getTreasuryLockTokenAccount)(mint, treasuryLockPda);
    const [shortConfigPda] = (0, program_1.getShortConfigPda)(mint);
    const [shortPositionPda] = (0, program_1.getShortPositionPda)(mint, shorter);
    const shorterTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, shorter, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Get Raydium pool accounts for price calculation
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    // Vault accounts (optional — SOL from vault, tokens to vault ATA)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, shorter);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // Create shorter's token ATA if needed (to receive borrowed tokens)
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(shorter, shorterTokenAccount, shorter, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(shorter, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, shorter);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const openShortIx = await program.methods
        .openShort({
        solCollateral: new anchor_1.BN(sol_collateral.toString()),
        tokensToBorrow: new anchor_1.BN(tokens_to_borrow.toString()),
    })
        .accounts({
        shorter,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        treasuryLock: treasuryLockPda,
        treasuryLockTokenAccount,
        shortConfig: shortConfigPda,
        shortPosition: shortPositionPda,
        shorterTokenAccount,
        poolState: raydium.poolState,
        tokenVault0: raydium.token0Vault,
        tokenVault1: raydium.token1Vault,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(openShortIx);
    const versionedTx = await finalizeTransaction(connection, tx, shorter);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Open short: ${Number(tokens_to_borrow) / 1e6} tokens with ${Number(sol_collateral) / 1e9} SOL collateral${vaultLabel}`,
    };
};
exports.buildOpenShortTransaction = buildOpenShortTransaction;
// ============================================================================
// Close Short (V5)
// ============================================================================
/**
 * Build an unsigned close_short transaction.
 *
 * Return tokens to close or partially repay a short position.
 * Interest paid first (in tokens), then principal.
 * Full close returns all SOL collateral.
 *
 * @param connection - Solana RPC connection
 * @param params - Close short parameters (mint, shorter, token_amount)
 * @returns Unsigned transaction and descriptive message
 */
const buildCloseShortTransaction = async (connection, params) => {
    const { mint: mintStr, shorter: shorterStr, token_amount, vault: vaultCreatorStr } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const shorter = new web3_js_1.PublicKey(shorterStr);
    // Derive PDAs (no Raydium needed — same as repay)
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [treasuryLockPda] = (0, program_1.getTreasuryLockPda)(mint);
    const treasuryLockTokenAccount = (0, program_1.getTreasuryLockTokenAccount)(mint, treasuryLockPda);
    const [shortConfigPda] = (0, program_1.getShortConfigPda)(mint);
    const [shortPositionPda] = (0, program_1.getShortPositionPda)(mint, shorter);
    const shorterTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, shorter, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Vault accounts (optional — tokens from vault ATA, SOL to vault)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, shorter);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // shorter_token_account is mut + non-optional; must exist even in vault mode.
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(shorter, shorterTokenAccount, shorter, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(shorter, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, shorter);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const closeShortIx = await program.methods
        .closeShort(new anchor_1.BN(token_amount.toString()))
        .accounts({
        shorter,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        treasuryLock: treasuryLockPda,
        treasuryLockTokenAccount,
        shortConfig: shortConfigPda,
        shortPosition: shortPositionPda,
        shorterTokenAccount,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(closeShortIx);
    const versionedTx = await finalizeTransaction(connection, tx, shorter);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Close short: return ${Number(token_amount) / 1e6} tokens${vaultLabel}`,
    };
};
exports.buildCloseShortTransaction = buildCloseShortTransaction;
// ============================================================================
// Liquidate Short (V5)
// ============================================================================
/**
 * Build an unsigned liquidate_short transaction.
 *
 * Permissionless — anyone can call when a short position's LTV exceeds the
 * liquidation threshold (65%). Liquidator sends tokens and receives SOL + bonus.
 *
 * @param connection - Solana RPC connection
 * @param params - Liquidate short parameters (mint, liquidator, borrower)
 * @returns Unsigned transaction and descriptive message
 */
const buildLiquidateShortTransaction = async (connection, params) => {
    const { mint: mintStr, liquidator: liquidatorStr, borrower: borrowerStr, vault: vaultCreatorStr, } = params;
    const mint = new web3_js_1.PublicKey(mintStr);
    const liquidator = new web3_js_1.PublicKey(liquidatorStr);
    const borrower = new web3_js_1.PublicKey(borrowerStr);
    // Derive PDAs
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [treasuryLockPda] = (0, program_1.getTreasuryLockPda)(mint);
    const treasuryLockTokenAccount = (0, program_1.getTreasuryLockTokenAccount)(mint, treasuryLockPda);
    const [shortConfigPda] = (0, program_1.getShortConfigPda)(mint);
    const [shortPositionPda] = (0, program_1.getShortPositionPda)(mint, borrower);
    const liquidatorTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint, liquidator, false, spl_token_1.TOKEN_2022_PROGRAM_ID);
    // Get Raydium pool accounts for price calculation
    const raydium = (0, program_1.getRaydiumMigrationAccounts)(mint);
    // Vault accounts (optional — tokens from vault ATA, SOL to vault)
    const { torchVault: torchVaultAccount, walletLink: vaultWalletLinkAccount } = deriveVaultAccounts(vaultCreatorStr, liquidator);
    const vaultTokenAccount = torchVaultAccount ? getVaultTokenAta(mint, torchVaultAccount) : null;
    const tx = new web3_js_1.Transaction();
    // Create liquidator's token ATA if needed (source of covering tokens)
    tx.add((0, spl_token_1.createAssociatedTokenAccountIdempotentInstruction)(liquidator, liquidatorTokenAccount, liquidator, mint, spl_token_1.TOKEN_2022_PROGRAM_ID, spl_token_1.ASSOCIATED_TOKEN_PROGRAM_ID));
    if (torchVaultAccount) {
        tx.add(createVaultTokenAtaIx(liquidator, mint, torchVaultAccount));
    }
    const provider = makeDummyProvider(connection, liquidator);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const liquidateShortIx = await program.methods
        .liquidateShort()
        .accounts({
        liquidator,
        borrower,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        treasuryLock: treasuryLockPda,
        treasuryLockTokenAccount,
        shortConfig: shortConfigPda,
        shortPosition: shortPositionPda,
        liquidatorTokenAccount,
        poolState: raydium.poolState,
        tokenVault0: raydium.token0Vault,
        tokenVault1: raydium.token1Vault,
        torchVault: torchVaultAccount,
        vaultWalletLink: vaultWalletLinkAccount,
        vaultTokenAccount,
        tokenProgram: spl_token_1.TOKEN_2022_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    tx.add(liquidateShortIx);
    const versionedTx = await finalizeTransaction(connection, tx, liquidator);
    const vaultLabel = vaultCreatorStr ? ' (via vault)' : '';
    return {
        transaction: versionedTx,
        message: `Liquidate short position for ${borrowerStr.slice(0, 8)}...${vaultLabel}`,
    };
};
exports.buildLiquidateShortTransaction = buildLiquidateShortTransaction;
// ============================================================================
// Enable Short Selling (V5) — Admin / Pre-V5 Tokens
// ============================================================================
/**
 * Build an unsigned enable_short_selling transaction.
 *
 * Admin-only. For pre-V5 tokens that weren't created with the short selling
 * sentinel. New tokens (V5+) have shorts auto-enabled at creation.
 *
 * @param connection - Solana RPC connection
 * @param params - Enable short selling parameters (authority, mint)
 * @returns Unsigned transaction and descriptive message
 */
const buildEnableShortSellingTransaction = async (connection, params) => {
    const { authority: authorityStr, mint: mintStr } = params;
    const authority = new web3_js_1.PublicKey(authorityStr);
    const mint = new web3_js_1.PublicKey(mintStr);
    // Derive PDAs
    const [globalConfigPda] = (0, program_1.getGlobalConfigPda)();
    const [bondingCurvePda] = (0, program_1.getBondingCurvePda)(mint);
    const [treasuryPda] = (0, program_1.getTokenTreasuryPda)(mint);
    const [shortConfigPda] = (0, program_1.getShortConfigPda)(mint);
    const provider = makeDummyProvider(connection, authority);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const enableIx = await program.methods
        .enableShortSelling()
        .accounts({
        authority,
        globalConfig: globalConfigPda,
        mint,
        bondingCurve: bondingCurvePda,
        treasury: treasuryPda,
        shortConfig: shortConfigPda,
        systemProgram: web3_js_1.SystemProgram.programId,
    })
        .instruction();
    const tx = new web3_js_1.Transaction();
    tx.add(enableIx);
    const versionedTx = await finalizeTransaction(connection, tx, authority);
    return {
        transaction: versionedTx,
        message: `Enable short selling for ${mintStr.slice(0, 8)}...`,
    };
};
exports.buildEnableShortSellingTransaction = buildEnableShortSellingTransaction;
//# sourceMappingURL=transactions.js.map