"use strict";
/**
 * Pyre vanity mint address grinder
 *
 * Grinds for Solana keypairs whose base58 address ends with "pyre".
 * This is how we distinguish pyre faction tokens from regular torch tokens —
 * no registry program needed, just check the mint suffix.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildCreateFactionTransaction = exports.isPyreMint = exports.grindPyreMint = exports.getTreasuryLockPda = exports.getTokenTreasuryPda = exports.getBondingCurvePda = void 0;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const anchor_1 = require("@coral-xyz/anchor");
const torchsdk_1 = require("torchsdk");
// Token-2022 program ID
const TOKEN_2022_PROGRAM_ID = new web3_js_1.PublicKey('TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb');
// PDA seeds (must match the Rust program)
const GLOBAL_CONFIG_SEED = 'global_config';
const BONDING_CURVE_SEED = 'bonding_curve';
const TREASURY_SEED = 'treasury';
const TREASURY_LOCK_SEED = 'treasury_lock';
// IDL loaded from torchsdk dist
const torch_market_json_1 = __importDefault(require("torchsdk/dist/torch_market.json"));
// ── PDA helpers (copied from torchsdk internals) ──
const getGlobalConfigPda = () => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(GLOBAL_CONFIG_SEED)], torchsdk_1.PROGRAM_ID);
const getBondingCurvePda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(BONDING_CURVE_SEED), mint.toBuffer()], torchsdk_1.PROGRAM_ID);
exports.getBondingCurvePda = getBondingCurvePda;
const getTokenTreasuryPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(TREASURY_SEED), mint.toBuffer()], torchsdk_1.PROGRAM_ID);
exports.getTokenTreasuryPda = getTokenTreasuryPda;
const getTreasuryTokenAccount = (mint, treasury) => (0, spl_token_1.getAssociatedTokenAddressSync)(mint, treasury, true, TOKEN_2022_PROGRAM_ID);
const getTreasuryLockPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(TREASURY_LOCK_SEED), mint.toBuffer()], torchsdk_1.PROGRAM_ID);
exports.getTreasuryLockPda = getTreasuryLockPda;
const getTreasuryLockTokenAccount = (mint, treasuryLock) => (0, spl_token_1.getAssociatedTokenAddressSync)(mint, treasuryLock, true, TOKEN_2022_PROGRAM_ID);
const makeDummyProvider = (connection, payer) => new anchor_1.AnchorProvider(connection, {
    publicKey: payer,
    signTransaction: async (t) => t,
    signAllTransactions: async (t) => t,
}, {});
const finalizeTransaction = async (connection, tx, feePayer) => {
    const { blockhash } = await connection.getLatestBlockhash();
    const message = new web3_js_1.TransactionMessage({
        payerKey: feePayer,
        recentBlockhash: blockhash,
        instructions: tx.instructions,
    }).compileToV0Message();
    return new web3_js_1.VersionedTransaction(message);
};
// ── Vanity grinder ──
const PYRE_SUFFIX = 'pr';
/** Grind for a keypair whose base58 address ends with "pr" (pyre) */
const grindPyreMint = (maxAttempts = 500_000) => {
    for (let i = 0; i < maxAttempts; i++) {
        const kp = web3_js_1.Keypair.generate();
        if (kp.publicKey.toBase58().endsWith(PYRE_SUFFIX)) {
            return kp;
        }
    }
    // Fallback — return last generated keypair (should be extremely rare)
    return web3_js_1.Keypair.generate();
};
exports.grindPyreMint = grindPyreMint;
/** Check if a mint address is a pyre faction (ends with "pr") */
const isPyreMint = (mint) => mint.endsWith(PYRE_SUFFIX);
exports.isPyreMint = isPyreMint;
// ── Build create transaction with pyre vanity address ──
const buildCreateFactionTransaction = async (connection, params) => {
    const { creator: creatorStr, name, symbol, metadata_uri, sol_target = 0, community_token = true, } = params;
    const creator = new web3_js_1.PublicKey(creatorStr);
    if (name.length > 32)
        throw new Error('Name must be 32 characters or less');
    if (symbol.length > 10)
        throw new Error('Symbol must be 10 characters or less');
    // Grind for "pyre" suffix instead of "tm"
    const mint = (0, exports.grindPyreMint)();
    // Derive PDAs
    const [globalConfig] = getGlobalConfigPda();
    const [bondingCurve] = (0, exports.getBondingCurvePda)(mint.publicKey);
    const [treasury] = (0, exports.getTokenTreasuryPda)(mint.publicKey);
    const bondingCurveTokenAccount = (0, spl_token_1.getAssociatedTokenAddressSync)(mint.publicKey, bondingCurve, true, TOKEN_2022_PROGRAM_ID);
    const treasuryTokenAccount = getTreasuryTokenAccount(mint.publicKey, treasury);
    const [treasuryLock] = (0, exports.getTreasuryLockPda)(mint.publicKey);
    const treasuryLockTokenAccount = getTreasuryLockTokenAccount(mint.publicKey, treasuryLock);
    const tx = new web3_js_1.Transaction();
    const provider = makeDummyProvider(connection, creator);
    const program = new anchor_1.Program(torch_market_json_1.default, provider);
    const createIx = await program.methods.createToken({
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
        token2022Program: TOKEN_2022_PROGRAM_ID,
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
        message: `Create faction "${name}" ($${symbol}) [pyre:${mint.publicKey.toBase58()}]`,
    };
};
exports.buildCreateFactionTransaction = buildCreateFactionTransaction;
