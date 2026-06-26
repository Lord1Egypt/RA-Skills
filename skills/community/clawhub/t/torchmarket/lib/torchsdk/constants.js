"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getRaydiumFeeReceiver = exports.getRaydiumAmmConfig = exports.getRaydiumCpmmProgram = exports.BLACKLISTED_MINTS = exports.LEGACY_MINTS = exports.TOKEN_MULTIPLIER = exports.LAMPORTS_PER_SOL = exports.TOKEN_DECIMALS = exports.TOTAL_SUPPLY = exports.SHORT_CONFIG_SEED = exports.SHORT_SEED = exports.TREASURY_LOCK_SEED = exports.VAULT_WALLET_LINK_SEED = exports.TORCH_VAULT_SEED = exports.COLLATERAL_VAULT_SEED = exports.LOAN_SEED = exports.STAR_RECORD_SEED = exports.USER_STATS_SEED = exports.PROTOCOL_TREASURY_SEED = exports.USER_POSITION_SEED = exports.TREASURY_SEED = exports.BONDING_CURVE_SEED = exports.GLOBAL_CONFIG_SEED = exports.TOKEN_2022_PROGRAM_ID = exports.MEMO_PROGRAM_ID = exports.WSOL_MINT = exports.PROGRAM_ID = void 0;
const web3_js_1 = require("@solana/web3.js");
// program ID - Mainnet/Devnet (deployed program)
exports.PROGRAM_ID = new web3_js_1.PublicKey('8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT');
// WSOL Mint (same on all networks)
exports.WSOL_MINT = new web3_js_1.PublicKey('So11111111111111111111111111111111111111112');
// SPL Memo Program
exports.MEMO_PROGRAM_ID = new web3_js_1.PublicKey('MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr');
// token-2022 Program (for Token Extensions)
exports.TOKEN_2022_PROGRAM_ID = new web3_js_1.PublicKey('TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb');
// PDA seeds (must match the Rust program)
exports.GLOBAL_CONFIG_SEED = 'global_config';
exports.BONDING_CURVE_SEED = 'bonding_curve';
exports.TREASURY_SEED = 'treasury';
exports.USER_POSITION_SEED = 'user_position';
exports.PROTOCOL_TREASURY_SEED = 'protocol_treasury_v11';
exports.USER_STATS_SEED = 'user_stats';
exports.STAR_RECORD_SEED = 'star_record';
exports.LOAN_SEED = 'loan';
exports.COLLATERAL_VAULT_SEED = 'collateral_vault';
exports.TORCH_VAULT_SEED = 'torch_vault';
exports.VAULT_WALLET_LINK_SEED = 'vault_wallet';
exports.TREASURY_LOCK_SEED = 'treasury_lock';
exports.SHORT_SEED = 'short';
exports.SHORT_CONFIG_SEED = 'short_config';
// token constants (must match the Rust program)
exports.TOTAL_SUPPLY = BigInt('1000000000000000'); // 1B with 6 decimals
exports.TOKEN_DECIMALS = 6;
// formatting helpers
exports.LAMPORTS_PER_SOL = 1000000000;
exports.TOKEN_MULTIPLIER = Math.pow(10, exports.TOKEN_DECIMALS);
// legacy tokens (old test tokens, failed launches, etc.) — shown greyed out in UI
exports.LEGACY_MINTS = [
    '6JkGdXSKzUHTNwR5w7jce4WxjczUGpqheBJsP1if5htm', // legacy SPL test token (pre-prod-beta)
    'Nu5xbqZvZd4JerG2aNyxQfUiHBnM59w7CHzyVx5Vztm', // legacy SPL devnet test token
    '8wzap6FUtL4ko6LnnELt8ZoM6ksy6jPJ9veFkwGB56tm', // legacy SPL devnet test token
    'HgFGagsCFmBKRFM3U4zCpy3r8XU7RFS58UChup9xCytm', // legacy SPL devnet test token
    'CLJk4YLy8pBu7mRFm1hfaeFJJ6WQQR7RHmkptPSLCXtm', // pre-V13 devnet test token
    '61ryb1WAq2vqEcdeStvTMRvYdcgzvZYFjBtKzSzXv7tm', // pre-V13 devnet test token
    '9F8SXt7VP8b6Vb6RzE8dTdBEwKuKeCizhxEY6QQX1qtm', // pre-V13 mainnet test token
    'GQKidAtE2RmEpMq7ciPShniHZ9fh8NSAaXp59M89X3tm', // pre-V13 mainnet test token
    '7b7WHQdXQN4bR8eC47jaH9De6JYC4cze1BWJJcxU1Mtm', // pre-V13 mainnet test token
    'FjERW8DSNB81GYWhrXwdfS3s74xTF8T5gjcKYSa1v7tm', // duplicate test token (keep Second Torch only)
    'GawKda5Vzm34HaDCkQrCLjnGUaQFVuYcTFpkDstNBRtm', // failed mainnet token (relaunched)
    '2DSdhnjTZVCnVEdYrJDxdrdmeedooGCd4A2dDqjH9ctm', // relaunched token
    'WBMWGzvV2fSQEc8DbKQsbX4ueeUdg7buMJNpvVWk9tm',
    'E5MNMgWzs1DveEftiq4By6Sv95MdsEVyU5iXZ8y3F9tm',
    'GuLvJnT7dNVKT4hMxBEBSR84fXFkpu8su8seTWXJVqtm',
    '5n4Pwzw2u23Jo4fL6DTmHnmqVa4gHiH2TFeaAGypwVtm',
    '4871X12frXyXHup44Ji5L5BTBK7MNKdq3HYshPuJkhtm',
    'Ao49PDxkUF4YRuaxxoh31dj3QdZD6W8reAooHZEnRqtm',
    'ATp6vuxnL4ysnA8WWnRJ6XLCQsgnDWB3GyR5UD8YFbtm',
    'C2etphp3yh5aTx9gBiQ3tJ6vA2AUioXP9ApzjQTzWdtm',
    'G1UuoUbqUSWTrYMF1DcedazvPuReSc75t6yoUgbyHWtm',
    '9QZ66iAjJ9FkP79M7f5KCVTJ732E52qybrGp6F5B97tm',
    'w5kr3WJ5cqty33h7k4E36bysWsoiiZRfjm7zUBzPCtm',
    '3w2tZkQHZPksbj1bbq7mkJP16UPLbYWoDekMWootYKtm',
    '6qZeyoNhXJuQQiKRPVutuTojneBEVZ9UnDfJi1CJovtm',
    'J9vfPGJAWYTBVo3fBzAe5dk4DfmzybTKXumGbEi3a1tm',
    'Txi1N4zY6Gu8HmqPXdRVXoQ6R9TxUTYfQqsLTMawHtm',
    '5mVJc3PPWmJvJX3FsomxisDUG8Dr6coWVbnBZvYqCktm',
    '6VJbgHycoYb1y5VvaXZH9isB5sheuVT9ubU5rrkGvJtm',
    'ACgsqLCQfDbMe721pQQRTR9uXJHea3ZPdFdjKYBVkotm',
    '83yV9zfEuH116zNxZFbEzzpVZBae6MxabANRmdXhAwtm',
    'BiRMKYyqgwLfrKJEsdjAM7C7WJK3LoqDPNKQTy7CA9tm',
    'AmoCUAhSWdUbihSoGnddf1VurXZUgRZifJUoB54xGntm',
];
// blacklisted tokens — completely hidden, never returned by the SDK
exports.BLACKLISTED_MINTS = [
    '22fRDzkMUp8LW7RhPGa17FxifJJr6hR4PqyREAR6jitm',
    'DFM5jCjtnEaHnBzfMExiT4rUGnAj7t7kvxci8BgA64tm',
    // irys data loss — bundle items never settled to Arweave L1 (Irys gateway shutdown Mar 2026)
    '6Cc6izuk7816mV97fi9qDcbnLiBEnkFRho5Nnpcqbrtm',
    '4y2vpd8J8o4bEneohAn6LjwH72BiCgym3c6hYYLamatm',
    '2zKJuYvB9XJrW16xJgE2SNyECYWFpfEh3JYQU2npcZtm',
    'DzS7tdbSXET5pFtyqTXCM7JED7JegHvTeuVeJxm56Epy',
    '5YJdBkWu8wRG2zmaCTRZRBsCq5mcAhaac9ywsbNZtkpy',
    '8RBSyx31YkBvxGLx6Dd1um5RUgkaVHuuA8dfiKRh6Cpy',
];
// network detection: evaluated at call time so env can be set dynamically.
// checks globalThis.__TORCH_NETWORK__ first (for browser runtime switching), then falls back to process.env.TORCH_NETWORK (for Node.js / build-time).
const isDevnet = () => globalThis.__TORCH_NETWORK__ === 'devnet' ||
    (typeof process !== 'undefined' && process.env?.TORCH_NETWORK === 'devnet');
// raydium CPMM Program (different on mainnet vs devnet)
const getRaydiumCpmmProgram = () => new web3_js_1.PublicKey(isDevnet()
    ? 'CPMDWBwJDtYax9qW7AyRuVC19Cc4L4Vcy4n2BHAbHkCW'
    : 'CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C');
exports.getRaydiumCpmmProgram = getRaydiumCpmmProgram;
// raydium AMM Config (different on mainnet vs devnet)
const getRaydiumAmmConfig = () => new web3_js_1.PublicKey(isDevnet()
    ? '9zSzfkYy6awexsHvmggeH36pfVUdDGyCcwmjT3AQPBj6'
    : 'D4FPEruKEHrG5TenZ2mpDGEfu1iUvTiqBxvpU8HLBvC2');
exports.getRaydiumAmmConfig = getRaydiumAmmConfig;
// raydium Fee Receiver (different on mainnet vs devnet)
const getRaydiumFeeReceiver = () => new web3_js_1.PublicKey(isDevnet()
    ? 'G11FKBRaAkHAKuLCgLM6K6NUc9rTjPAznRCjZifrTQe2'
    : 'DNXgeM9EiiaAbaWvwjHj9fQQLAX5ZsfHyvmYUNRAdNC8');
exports.getRaydiumFeeReceiver = getRaydiumFeeReceiver;
//# sourceMappingURL=constants.js.map