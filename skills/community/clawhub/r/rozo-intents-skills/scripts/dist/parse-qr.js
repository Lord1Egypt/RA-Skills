/**
 * Parse payment QR code content.
 *
 * Supports:
 * - EIP-681: ethereum:<address>[@chainId][/transfer?address=<to>&uint256=<amount>]
 * - Solana Pay: solana:<address>?amount=<amount>[&spl-token=<mint>][&label=...][&message=...][&memo=...]
 * - Stellar URI: web+stellar:pay?destination=<address>&amount=<amount>[&asset_code=USDC&asset_issuer=...]
 * - Plain addresses: 0x..., base58, G..., C...
 */
// EIP-681 chain ID to Rozo chain ID mapping
const EIP681_CHAIN_MAP = {
    1: 1, // Ethereum
    42161: 42161, // Arbitrum
    8453: 8453, // Base
    56: 56, // BSC
    137: 137, // Polygon
};
// Known ERC-20 token contract → symbol mapping (lowercase)
const EVM_TOKEN_CONTRACTS = {
    // USDC
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": { symbol: "USDC", chainId: 1 },
    "0xaf88d065e77c8cc2239327c5edb3a432268e5831": { symbol: "USDC", chainId: 42161 },
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": { symbol: "USDC", chainId: 8453 },
    "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d": { symbol: "USDC", chainId: 56 },
    "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359": { symbol: "USDC", chainId: 137 },
    // USDT
    "0xdac17f958d2ee523a2206206994597c13d831ec7": { symbol: "USDT", chainId: 1 },
    "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": { symbol: "USDT", chainId: 42161 },
    "0x55d398326f99059ff775485246999027b3197955": { symbol: "USDT", chainId: 56 },
    "0xc2132d05d31c914a87c6611c10748aeb04b58e8f": { symbol: "USDT", chainId: 137 },
};
// Solana SPL token mint → symbol mapping
const SOLANA_TOKEN_MINTS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
};
function parseEIP681(uri) {
    // ethereum:<contract_or_address>[@chainId][/transfer?address=<to>&uint256=<amount>]
    // or ethereum:<address>[@chainId][?value=<wei_amount>]
    const match = uri.match(/^ethereum:(0x[0-9a-fA-F]{40})(?:@(\d+))?(?:\/(\w+))?(?:\?(.+))?$/);
    if (!match)
        return null;
    const [, addressOrContract, chainIdStr, method, queryStr] = match;
    const params = new URLSearchParams(queryStr ?? "");
    const chainId = chainIdStr ? EIP681_CHAIN_MAP[Number(chainIdStr)] ?? Number(chainIdStr) : undefined;
    // ERC-20 transfer: contract is the token, address param is the recipient
    if (method === "transfer") {
        const recipient = params.get("address");
        const rawAmount = params.get("uint256");
        if (!recipient)
            return null;
        const contractLower = addressOrContract.toLowerCase();
        const tokenInfo = EVM_TOKEN_CONTRACTS[contractLower];
        return {
            type: "eip681",
            address: recipient,
            chainId: chainId ?? tokenInfo?.chainId,
            token: tokenInfo?.symbol,
            tokenAddress: addressOrContract,
            amount: rawAmount ?? undefined,
            raw: uri,
        };
    }
    // Simple ETH/native transfer with value (we note it but it's not a stablecoin transfer)
    return {
        type: "eip681",
        address: addressOrContract,
        chainId,
        amount: params.get("value") ?? undefined,
        raw: uri,
    };
}
function parseSolanaPay(uri) {
    // solana:<address>?amount=<amount>[&spl-token=<mint>][&label=...][&message=...][&memo=...]
    const match = uri.match(/^solana:([1-9A-HJ-NP-Za-km-z]{32,44})(?:\?(.+))?$/);
    if (!match)
        return null;
    const [, address, queryStr] = match;
    const params = new URLSearchParams(queryStr ?? "");
    const splToken = params.get("spl-token");
    return {
        type: "solana-pay",
        address,
        chainId: 900,
        token: splToken ? SOLANA_TOKEN_MINTS[splToken] : undefined,
        tokenAddress: splToken ?? undefined,
        amount: params.get("amount") ?? undefined,
        memo: params.get("memo") ?? undefined,
        label: params.get("label") ?? undefined,
        message: params.get("message") ?? undefined,
        raw: uri,
    };
}
function parseStellarURI(uri) {
    // web+stellar:pay?destination=<address>&amount=<amount>[&asset_code=USDC&asset_issuer=...]
    const match = uri.match(/^web\+stellar:pay\?(.+)$/);
    if (!match)
        return null;
    const params = new URLSearchParams(match[1]);
    const destination = params.get("destination");
    if (!destination)
        return null;
    const assetCode = params.get("asset_code");
    return {
        type: "stellar-uri",
        address: destination,
        chainId: 1500,
        token: assetCode ?? undefined,
        amount: params.get("amount") ?? undefined,
        memo: params.get("memo") ?? undefined,
        raw: uri,
    };
}
function parsePlainAddress(text) {
    const trimmed = text.trim();
    // EVM
    if (/^0x[0-9a-fA-F]{40}$/.test(trimmed)) {
        return { type: "plain-address", address: trimmed, raw: trimmed };
    }
    // Stellar G-wallet
    if (/^G[A-Z2-7]{55}$/.test(trimmed)) {
        return { type: "plain-address", address: trimmed, chainId: 1500, raw: trimmed };
    }
    // Stellar C-wallet
    if (/^C[A-Z2-7]{55}$/.test(trimmed)) {
        return { type: "plain-address", address: trimmed, chainId: 1500, raw: trimmed };
    }
    // Solana
    if (/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(trimmed)) {
        return { type: "plain-address", address: trimmed, chainId: 900, raw: trimmed };
    }
    return null;
}
export function parseQR(content) {
    const trimmed = content.trim();
    if (trimmed.startsWith("ethereum:"))
        return parseEIP681(trimmed);
    if (trimmed.startsWith("solana:"))
        return parseSolanaPay(trimmed);
    if (trimmed.startsWith("web+stellar:"))
        return parseStellarURI(trimmed);
    return parsePlainAddress(trimmed);
}
// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
    const input = process.argv.slice(2).join(" ").trim();
    if (!input) {
        console.error("Usage: node parse-qr.js <qr_content>");
        process.exit(1);
    }
    const result = parseQR(input);
    if (result) {
        console.log(JSON.stringify(result, null, 2));
    }
    else {
        console.error(JSON.stringify({ error: "Could not parse QR content", raw: input }));
        process.exit(1);
    }
}
