import { ethers } from 'ethers';
import { NetworkName, createProvider, rpcCall } from './provider.js';

export interface EpochInfo {
  number: number;
  startTime: number;
  durationMs: number;
}

/**
 * QFCEpoch — epoch and finality information.
 */
export class QFCEpoch {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /** Get current epoch info */
  async getCurrentEpoch(): Promise<EpochInfo> {
    const raw = await rpcCall(this.provider, 'qfc_getEpoch', []);
    return {
      number: Number(raw.number),
      startTime: Number(raw.startTime),
      durationMs: Number(raw.durationMs),
    };
  }

  /** Get the latest finalized block number */
  async getFinalizedBlock(): Promise<number> {
    const raw = await rpcCall(this.provider, 'qfc_getFinalizedBlock', []);
    return Number(raw);
  }
}
