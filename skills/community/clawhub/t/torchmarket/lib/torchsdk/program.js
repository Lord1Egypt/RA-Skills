"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getRaydiumMigrationAccounts = exports.getRaydiumObservationPda = exports.getRaydiumVaultPda = exports.getRaydiumLpMintPda = exports.getRaydiumPoolStatePda = exports.getRaydiumAuthorityPda = exports.orderTokensForRaydium = exports.calculateBondingProgress = exports.calculatePrice = exports.calculateSolOut = exports.calculateTokensOut = exports.getProgram = exports.getTreasuryLockTokenAccount = exports.getShortConfigPda = exports.getShortPositionPda = exports.getTreasuryLockPda = exports.getVaultWalletLinkPda = exports.getTorchVaultPda = exports.getCollateralVaultPda = exports.getLoanPositionPda = exports.getStarRecordPda = exports.getUserStatsPda = exports.getProtocolTreasuryPda = exports.getTokenTreasuryPda = exports.getUserPositionPda = exports.getTreasuryTokenAccount = exports.getBondingCurvePda = exports.getGlobalConfigPda = exports.decodeString = exports.PROGRAM_ID = void 0;
const anchor_1 = require("@coral-xyz/anchor");
const web3_js_1 = require("@solana/web3.js");
const constants_1 = require("./constants");
Object.defineProperty(exports, "PROGRAM_ID", { enumerable: true, get: function () { return constants_1.PROGRAM_ID; } });
const spl_token_1 = require("@solana/spl-token");
const torch_market_json_1 = __importDefault(require("./torch_market.json"));
// treasury SOL rate decays linearly from 17.5% at bonding start to 2.5% at completion
const TREASURY_SOL_MAX_BPS = 1750;
const TREASURY_SOL_MIN_BPS = 250;
// creator SOL share grows from 0.2% → 1% during bonding (carved from treasury rate)
const CREATOR_SOL_MIN_BPS = 20;
const CREATOR_SOL_MAX_BPS = 100;
const decodeString = (bytes) => Buffer.from(bytes).toString('utf8').replace(/\0/g, '');
exports.decodeString = decodeString;
const getGlobalConfigPda = () => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.GLOBAL_CONFIG_SEED)], constants_1.PROGRAM_ID);
exports.getGlobalConfigPda = getGlobalConfigPda;
const getBondingCurvePda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.BONDING_CURVE_SEED), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getBondingCurvePda = getBondingCurvePda;
const getTreasuryTokenAccount = (mint, treasury) => (0, spl_token_1.getAssociatedTokenAddressSync)(mint, treasury, true, constants_1.TOKEN_2022_PROGRAM_ID);
exports.getTreasuryTokenAccount = getTreasuryTokenAccount;
const getUserPositionPda = (bondingCurve, user) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.USER_POSITION_SEED), bondingCurve.toBuffer(), user.toBuffer()], constants_1.PROGRAM_ID);
exports.getUserPositionPda = getUserPositionPda;
const getTokenTreasuryPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.TREASURY_SEED), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getTokenTreasuryPda = getTokenTreasuryPda;
const getProtocolTreasuryPda = () => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.PROTOCOL_TREASURY_SEED)], constants_1.PROGRAM_ID);
exports.getProtocolTreasuryPda = getProtocolTreasuryPda;
const getUserStatsPda = (user) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.USER_STATS_SEED), user.toBuffer()], constants_1.PROGRAM_ID);
exports.getUserStatsPda = getUserStatsPda;
const getStarRecordPda = (user, mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.STAR_RECORD_SEED), user.toBuffer(), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getStarRecordPda = getStarRecordPda;
const getLoanPositionPda = (mint, borrower) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.LOAN_SEED), mint.toBuffer(), borrower.toBuffer()], constants_1.PROGRAM_ID);
exports.getLoanPositionPda = getLoanPositionPda;
const getCollateralVaultPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.COLLATERAL_VAULT_SEED), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getCollateralVaultPda = getCollateralVaultPda;
const getTorchVaultPda = (creator) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.TORCH_VAULT_SEED), creator.toBuffer()], constants_1.PROGRAM_ID);
exports.getTorchVaultPda = getTorchVaultPda;
const getVaultWalletLinkPda = (wallet) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.VAULT_WALLET_LINK_SEED), wallet.toBuffer()], constants_1.PROGRAM_ID);
exports.getVaultWalletLinkPda = getVaultWalletLinkPda;
const getTreasuryLockPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.TREASURY_LOCK_SEED), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getTreasuryLockPda = getTreasuryLockPda;
const getShortPositionPda = (mint, shorter) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.SHORT_SEED), mint.toBuffer(), shorter.toBuffer()], constants_1.PROGRAM_ID);
exports.getShortPositionPda = getShortPositionPda;
const getShortConfigPda = (mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(constants_1.SHORT_CONFIG_SEED), mint.toBuffer()], constants_1.PROGRAM_ID);
exports.getShortConfigPda = getShortConfigPda;
const getTreasuryLockTokenAccount = (mint, treasuryLock) => {
    return (0, spl_token_1.getAssociatedTokenAddressSync)(mint, treasuryLock, true, // allowOwnerOffCurve (PDA)
    constants_1.TOKEN_2022_PROGRAM_ID);
};
exports.getTreasuryLockTokenAccount = getTreasuryLockTokenAccount;
const getProgram = (provider) => new anchor_1.Program(torch_market_json_1.default, provider);
exports.getProgram = getProgram;
// tokens out for a given SOL amount
const calculateTokensOut = (solAmount, virtualSolReserves, virtualTokenReserves, realSolReserves = BigInt(0), // V2.3: needed for dynamic rate calculation
protocolFeeBps = 50, // [V4.0] 0.5% protocol fee (90% protocol treasury, 10% dev)
treasuryFeeBps = 0, // [V10] 0% token treasury fee (removed — treasury funded by dynamic SOL rate + transfer fees)
bondingTarget = BigInt('200000000000')) => {
    // calculate protocol fee (1%)
    const protocolFee = (solAmount * BigInt(protocolFeeBps)) / BigInt(10000);
    // calculate treasury fee (1%)
    const treasuryFee = (solAmount * BigInt(treasuryFeeBps)) / BigInt(10000);
    const solAfterFees = solAmount - protocolFee - treasuryFee;
    // flat 20% → 5% treasury rate across all tiers
    const resolvedTarget = bondingTarget === BigInt(0) ? BigInt('200000000000') : bondingTarget;
    // dynamic treasury rate - decays from 20% to 5% as bonding progresses
    const rateRange = BigInt(TREASURY_SOL_MAX_BPS - TREASURY_SOL_MIN_BPS);
    const decay = (realSolReserves * rateRange) / resolvedTarget;
    const treasuryRateBps = Math.max(TREASURY_SOL_MAX_BPS - Number(decay), TREASURY_SOL_MIN_BPS);
    // creator rate - grows from 0.2% to 1% (inverse of treasury decay)
    const creatorRange = BigInt(CREATOR_SOL_MAX_BPS - CREATOR_SOL_MIN_BPS);
    const creatorGrowth = (realSolReserves * creatorRange) / resolvedTarget;
    const creatorRateBps = Math.min(CREATOR_SOL_MIN_BPS + Number(creatorGrowth), CREATOR_SOL_MAX_BPS);
    // split remaining SOL: total rate → creator + treasury + curve
    const totalSplit = (solAfterFees * BigInt(treasuryRateBps)) / BigInt(10000);
    const solToCreator = (solAfterFees * BigInt(creatorRateBps)) / BigInt(10000);
    const solToTreasurySplit = totalSplit - solToCreator;
    const solToCurve = solAfterFees - totalSplit;
    // total to treasury = flat fee + dynamic split (minus creator)
    const solToTreasury = treasuryFee + solToTreasurySplit;
    // constant product: tokens out for the SOL that enters the curve
    const tokensOut = (virtualTokenReserves * solToCurve) / (virtualSolReserves + solToCurve);
    const tokensToUser = tokensOut;
    return {
        tokensOut,
        tokensToUser,
        protocolFee,
        treasuryFee,
        solToCurve,
        solToTreasury,
        solToCreator,
        treasuryRateBps,
        creatorRateBps,
    };
};
exports.calculateTokensOut = calculateTokensOut;
// calculate SOL out for a given token amount (no sell fee)
const calculateSolOut = (tokenAmount, virtualSolReserves, virtualTokenReserves) => {
    // calculate SOL using inverse formula
    const solOut = (virtualSolReserves * tokenAmount) / (virtualTokenReserves + tokenAmount);
    // no fees on sells - user gets full amount
    return { solOut, solToUser: solOut };
};
exports.calculateSolOut = calculateSolOut;
// calculate current token price in SOL
const calculatePrice = (virtualSolReserves, virtualTokenReserves) => {
    // price = virtualSol / virtualTokens
    return Number(virtualSolReserves) / Number(virtualTokenReserves);
};
exports.calculatePrice = calculatePrice;
const calculateBondingProgress = (realSolReserves) => {
    const target = BigInt('200000000000'); // 200 SOL in lamports
    if (realSolReserves >= target) {
        return 100;
    }
    return (Number(realSolReserves) / Number(target)) * 100;
};
exports.calculateBondingProgress = calculateBondingProgress;
// ============================================================================
// RAYDIUM CPMM PDA DERIVATION
// ============================================================================
// order tokens for Raydium (token_0 < token_1 by pubkey bytes)
const orderTokensForRaydium = (tokenA, tokenB) => {
    const aBytes = tokenA.toBuffer();
    const bBytes = tokenB.toBuffer();
    for (let i = 0; i < 32; i++) {
        if (aBytes[i] < bBytes[i]) {
            return { token0: tokenA, token1: tokenB, isToken0First: true };
        }
        else if (aBytes[i] > bBytes[i]) {
            return { token0: tokenB, token1: tokenA, isToken0First: false };
        }
    }
    // equal - shouldn't happen
    return { token0: tokenA, token1: tokenB, isToken0First: true };
};
exports.orderTokensForRaydium = orderTokensForRaydium;
const getRaydiumAuthorityPda = () => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from('vault_and_lp_mint_auth_seed')], (0, constants_1.getRaydiumCpmmProgram)());
exports.getRaydiumAuthorityPda = getRaydiumAuthorityPda;
const getRaydiumPoolStatePda = (ammConfig, token0Mint, token1Mint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from('pool'), ammConfig.toBuffer(), token0Mint.toBuffer(), token1Mint.toBuffer()], (0, constants_1.getRaydiumCpmmProgram)());
exports.getRaydiumPoolStatePda = getRaydiumPoolStatePda;
const getRaydiumLpMintPda = (poolState) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from('pool_lp_mint'), poolState.toBuffer()], (0, constants_1.getRaydiumCpmmProgram)());
exports.getRaydiumLpMintPda = getRaydiumLpMintPda;
const getRaydiumVaultPda = (poolState, tokenMint) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from('pool_vault'), poolState.toBuffer(), tokenMint.toBuffer()], (0, constants_1.getRaydiumCpmmProgram)());
exports.getRaydiumVaultPda = getRaydiumVaultPda;
const getRaydiumObservationPda = (poolState) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from('observation'), poolState.toBuffer()], (0, constants_1.getRaydiumCpmmProgram)());
exports.getRaydiumObservationPda = getRaydiumObservationPda;
const getRaydiumMigrationAccounts = (tokenMint) => {
    const { token0, token1, isToken0First } = (0, exports.orderTokensForRaydium)(constants_1.WSOL_MINT, tokenMint);
    const isWsolToken0 = isToken0First;
    const [raydiumAuthority] = (0, exports.getRaydiumAuthorityPda)();
    const [poolState] = (0, exports.getRaydiumPoolStatePda)((0, constants_1.getRaydiumAmmConfig)(), token0, token1);
    const [lpMint] = (0, exports.getRaydiumLpMintPda)(poolState);
    const [token0Vault] = (0, exports.getRaydiumVaultPda)(poolState, token0);
    const [token1Vault] = (0, exports.getRaydiumVaultPda)(poolState, token1);
    const [observationState] = (0, exports.getRaydiumObservationPda)(poolState);
    return {
        token0,
        token1,
        isWsolToken0,
        raydiumAuthority,
        poolState,
        lpMint,
        token0Vault,
        token1Vault,
        observationState,
    };
};
exports.getRaydiumMigrationAccounts = getRaydiumMigrationAccounts;
//# sourceMappingURL=program.js.map