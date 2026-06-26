export type ChainType = "evm" | "solana" | "stellar";
export type TokenSymbol = "USDC" | "USDT";
export type Direction = "payin" | "payout";

export interface ChainInfo {
  name: string;
  type: ChainType;
}

export interface TokenInfo {
  address: string;
  decimals: number;
}

export const CHAINS: Record<number, ChainInfo> = {
  1: { name: "Ethereum", type: "evm" },
  42161: { name: "Arbitrum", type: "evm" },
  8453: { name: "Base", type: "evm" },
  56: { name: "BSC", type: "evm" },
  137: { name: "Polygon", type: "evm" },
  900: { name: "Solana", type: "solana" },
  1500: { name: "Stellar", type: "stellar" },
};

export const CHAIN_NAME_TO_ID: Record<string, number> = Object.fromEntries(
  Object.entries(CHAINS).map(([id, info]) => [info.name.toLowerCase(), Number(id)])
);

export const PAYIN_TOKENS: Record<TokenSymbol, Record<number, TokenInfo>> = {
  USDC: {
    1: { address: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", decimals: 6 },
    42161: { address: "0xaf88d065e77c8cc2239327c5edb3a432268e5831", decimals: 6 },
    8453: { address: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", decimals: 6 },
    56: { address: "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d", decimals: 18 },
    137: { address: "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359", decimals: 6 },
    900: { address: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", decimals: 6 },
    1500: { address: "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN", decimals: 7 },
  },
  USDT: {
    1: { address: "0xdac17f958d2ee523a2206206994597c13d831ec7", decimals: 6 },
    42161: { address: "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", decimals: 6 },
    56: { address: "0x55d398326f99059ff775485246999027b3197955", decimals: 18 },
    137: { address: "0xc2132d05d31c914a87c6611c10748aeb04b58e8f", decimals: 6 },
    900: { address: "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", decimals: 6 },
  },
};

export const PAYOUT_TOKENS: Record<TokenSymbol, Record<number, TokenInfo>> = {
  USDC: {
    1: { address: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", decimals: 6 },
    42161: { address: "0xaf88d065e77c8cc2239327c5edb3a432268e5831", decimals: 6 },
    8453: { address: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", decimals: 6 },
    56: { address: "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d", decimals: 18 },
    137: { address: "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359", decimals: 6 },
    900: { address: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", decimals: 6 },
    1500: { address: "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN", decimals: 7 },
  },
  USDT: {
    1: { address: "0xdac17f958d2ee523a2206206994597c13d831ec7", decimals: 6 },
    42161: { address: "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", decimals: 6 },
    8453: { address: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", decimals: 6 },
    56: { address: "0x55d398326f99059ff775485246999027b3197955", decimals: 18 },
    137: { address: "0xc2132d05d31c914a87c6611c10748aeb04b58e8f", decimals: 6 },
  },
};

export function getTokenAddress(
  chainId: number,
  token: TokenSymbol,
  direction: Direction = "payin"
): TokenInfo | null {
  const tokens = direction === "payout" ? PAYOUT_TOKENS : PAYIN_TOKENS;
  return tokens[token]?.[chainId] ?? null;
}

export function getChainName(chainId: number): string {
  return CHAINS[chainId]?.name ?? `Unknown (${chainId})`;
}

export function isPayoutSupported(chainId: number, token: TokenSymbol): boolean {
  return PAYOUT_TOKENS[token]?.[chainId] !== undefined;
}
