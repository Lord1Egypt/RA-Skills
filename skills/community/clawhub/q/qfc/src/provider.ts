import { ethers } from 'ethers';
import networks from '../config/qfc-networks.json' with { type: 'json' };

export type NetworkName = 'testnet' | 'mainnet';

export interface NetworkConfig {
  name: string;
  chainId: number;
  rpcUrl: string;
  explorerUrl: string;
  faucetUrl?: string;
  symbol: string;
  decimals: number;
}

/** Get the config for a named network */
export function getNetworkConfig(network: NetworkName): NetworkConfig {
  return networks[network];
}

/** Create a JsonRpcProvider for the given network */
export function createProvider(network: NetworkName): ethers.JsonRpcProvider {
  const config = getNetworkConfig(network);
  return new ethers.JsonRpcProvider(config.rpcUrl, config.chainId);
}

/** Send a custom JSON-RPC method */
export async function rpcCall(
  provider: ethers.JsonRpcProvider,
  method: string,
  params: any[],
): Promise<any> {
  return provider.send(method, params);
}
