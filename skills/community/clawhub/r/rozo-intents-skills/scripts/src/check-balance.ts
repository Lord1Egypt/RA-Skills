/**
 * Check wallet balances via the Rozo balance API.
 *
 * Single call returns all USDC/USDT balances across all supported chains
 * for the given address type (evm, solana, stellar).
 */

const BALANCE_API = "https://api-balance.rozo-deeplink.workers.dev/balance";

export interface TokenBalance {
  token: string;
  chain: string;
  balance: string;
  decimals: number;
}

export interface BalanceResponse {
  address: string;
  chain: string;
  balances: TokenBalance[];
  error?: string;
}

type ChainParam = "evm" | "solana" | "stellar";

function detectChainParam(address: string): ChainParam | null {
  if (address.startsWith("0x") && address.length === 42) return "evm";
  if (address.startsWith("G") && address.length === 56) return "stellar";
  if (address.startsWith("C") && address.length === 56) return "stellar";
  if (/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address)) return "solana";
  return null;
}

export async function checkBalance(
  address: string,
  chain?: ChainParam
): Promise<BalanceResponse> {
  const chainParam = chain ?? detectChainParam(address);
  if (!chainParam) {
    return { address, chain: "unknown", balances: [], error: "Cannot detect chain from address format" };
  }

  const url = `${BALANCE_API}/${address}?chain=${chainParam}`;

  let response: Response;
  try {
    response = await fetch(url);
  } catch (err) {
    return { address, chain: chainParam, balances: [], error: `Network error: ${(err as Error).message}` };
  }

  if (!response.ok) {
    return { address, chain: chainParam, balances: [], error: `Balance API error: ${response.status}` };
  }

  try {
    return await response.json() as BalanceResponse;
  } catch {
    return { address, chain: chainParam, balances: [], error: "Invalid JSON response from balance API" };
  }
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const addrIdx = args.indexOf("--address");
  const chainIdx = args.indexOf("--chain");

  if (addrIdx === -1) {
    console.error("Usage: --address <wallet_address> [--chain <evm|solana|stellar>]");
    process.exit(1);
  }

  const chain = chainIdx !== -1 ? (args[chainIdx + 1] as ChainParam) : undefined;
  const result = await checkBalance(args[addrIdx + 1], chain);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
}
