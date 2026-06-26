import { ethers } from 'ethers';
import { NetworkName, createProvider, rpcCall } from './provider.js';

export interface NodeInfo {
  version: string;
  chainId: number;
  peerCount: number;
  isValidator: boolean;
  syncing: boolean;
}

/**
 * QFCNetwork — node and network status queries.
 */
export class QFCNetwork {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /** Get node info via qfc_nodeInfo */
  async getNodeInfo(): Promise<NodeInfo> {
    const info = await rpcCall(this.provider, 'qfc_nodeInfo', []);
    return {
      version: info.version,
      chainId: Number(info.chainId),
      peerCount: Number(info.peerCount),
      isValidator: Boolean(info.isValidator),
      syncing: Boolean(info.syncing),
    };
  }

  /** Get network state (e.g. "normal", "congested") */
  async getNetworkState(): Promise<string> {
    return rpcCall(this.provider, 'qfc_getNetworkState', []);
  }

  /** Get chain ID */
  async getChainId(): Promise<number> {
    const hex = await rpcCall(this.provider, 'eth_chainId', []);
    return Number(hex);
  }

  /** Get latest block number */
  async getBlockNumber(): Promise<number> {
    const hex = await rpcCall(this.provider, 'eth_blockNumber', []);
    return Number(hex);
  }

  /** Get current gas price in Gwei */
  async getGasPrice(): Promise<string> {
    const hex = await rpcCall(this.provider, 'eth_gasPrice', []);
    return ethers.formatUnits(BigInt(hex), 'gwei');
  }
}
