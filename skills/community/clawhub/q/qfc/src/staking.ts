import { ethers } from 'ethers';
import { NetworkName, createProvider, rpcCall } from './provider.js';

export interface ValidatorInfo {
  address: string;
  stake: string;
  contributionScore: number;
  isActive: boolean;
  computeMode: string;
}

export interface ScoreBreakdown {
  address: string;
  totalScore: number;
  stake: string;
  dimensions: {
    stake: number;
    compute: number;
    uptime: number;
    accuracy: number;
    network: number;
    storage: number;
    reputation: number;
  };
  metrics: {
    uptimePercent: string;
    accuracyPercent: string;
    blocksProduced: number;
    providesCompute: boolean;
  };
}

/**
 * QFCStaking — validator and staking information.
 */
export class QFCStaking {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /** Get all validators */
  async getValidators(): Promise<ValidatorInfo[]> {
    const raw: any[] = await rpcCall(this.provider, 'qfc_getValidators', []);
    return raw.map((v) => ({
      address: v.address,
      stake: ethers.formatEther(BigInt(v.stake)),
      contributionScore: Number(v.contributionScore),
      isActive: Boolean(v.isActive),
      computeMode: v.computeMode ?? 'none',
    }));
  }

  /** Get stake amount for an address (returns QFC) */
  async getStake(address: string): Promise<string> {
    const hex = await rpcCall(this.provider, 'qfc_getStake', [address]);
    return ethers.formatEther(BigInt(hex));
  }

  /** Get contribution score (0-10000) */
  async getContributionScore(address: string): Promise<number> {
    const raw = await rpcCall(this.provider, 'qfc_getContributionScore', [address]);
    return Number(raw);
  }

  /** Get detailed score breakdown */
  async getScoreBreakdown(address: string): Promise<ScoreBreakdown> {
    const raw = await rpcCall(this.provider, 'qfc_getValidatorScoreBreakdown', [address]);
    if (!raw || !raw.address) {
      throw new Error(`No score breakdown found for ${address}`);
    }
    const metrics = raw.metrics ?? {};
    return {
      address: raw.address,
      totalScore: Number(raw.totalScore),
      stake: ethers.formatEther(BigInt(raw.stake ?? '0x0')),
      dimensions: {
        stake: Number(raw.stakeScore ?? 0),
        compute: Number(raw.computeScore ?? 0),
        uptime: Number(raw.uptimeScore ?? 0),
        accuracy: Number(raw.accuracyScore ?? 0),
        network: Number(raw.networkScore ?? 0),
        storage: Number(raw.storageScore ?? 0),
        reputation: Number(raw.reputationScore ?? 0),
      },
      metrics: {
        uptimePercent: metrics.uptimePercent ?? '0',
        accuracyPercent: metrics.accuracyPercent ?? '0',
        blocksProduced: Number(metrics.blocksProduced ?? 0),
        providesCompute: Boolean(metrics.providesCompute),
      },
    };
  }
}
