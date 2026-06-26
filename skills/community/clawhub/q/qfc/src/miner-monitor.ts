import { ethers } from 'ethers';
import { NetworkName, createProvider, rpcCall, getNetworkConfig } from './provider.js';
import type { EventSubscription } from './events.js';

export interface MinerEarning {
  /** Block height where the reward was issued */
  blockHeight: number;
  /** Task ID (hex) */
  taskId: string;
  /** Reward amount in wei */
  reward: string;
  /** Reward amount in QFC (human-readable) */
  rewardQfc: string;
  /** Task type (e.g. "TextEmbedding", "TextGeneration") */
  taskType: string;
  /** Model used */
  modelId: string;
  /** Execution time in ms */
  executionTimeMs: number;
  /** Block timestamp (unix seconds) */
  timestamp: number;
}

export interface MinerStatus {
  address: string;
  /** Total earned in wei (hex) */
  totalEarned: string;
  /** Total earned in QFC */
  totalEarnedQfc: string;
  /** Locked (vesting) in wei (hex) */
  locked: string;
  /** Available to withdraw in wei (hex) */
  available: string;
  /** Contribution score (0-100) */
  contributionScore: number;
  /** Number of active vesting tranches */
  activeTranches: number;
}

export interface MinerMonitorOptions {
  /** Polling interval in ms (default 15000 — one block time) */
  intervalMs?: number;
  /** Called on each new earning */
  onEarning?: (earning: MinerEarning) => void;
  /** Called on status change (balance change, score change) */
  onStatusChange?: (prev: MinerStatus, current: MinerStatus) => void;
  /** Called on errors (default: silent) */
  onError?: (error: Error) => void;
}

/**
 * QFCMinerMonitor — watch a miner's earnings in real-time via polling.
 *
 * Polls `qfc_getMinerEarnings` and `qfc_getMinerVesting` to detect new
 * rewards and balance changes, then fires callbacks.
 *
 * Usage:
 * ```ts
 * const monitor = new QFCMinerMonitor('testnet');
 * const sub = monitor.watch('0xMinerAddress', {
 *   onEarning: (e) => console.log(`Earned ${e.rewardQfc} QFC for ${e.taskType} task!`),
 *   onStatusChange: (prev, curr) => console.log(`Balance: ${curr.totalEarnedQfc} QFC`),
 * });
 * // later: sub.stop();
 * ```
 */
export class QFCMinerMonitor {
  private provider: ethers.JsonRpcProvider;
  private network: NetworkName;

  constructor(network: NetworkName = 'testnet') {
    this.network = network;
    this.provider = createProvider(network);
  }

  /**
   * Start watching a miner address for new earnings.
   * Returns a subscription that can be stopped.
   */
  watch(minerAddress: string, options: MinerMonitorOptions = {}): EventSubscription {
    const {
      intervalMs = 15_000,
      onEarning,
      onStatusChange,
      onError,
    } = options;

    let stopped = false;
    let lastStatus: MinerStatus | null = null;
    let knownEarningBlocks = new Set<string>();

    const poll = async () => {
      // Initialize: fetch current earnings to avoid replaying history
      try {
        const earnings = await this.getRecentEarnings(minerAddress);
        for (const e of earnings) {
          knownEarningBlocks.add(`${e.blockHeight}:${e.taskId}`);
        }
        lastStatus = await this.getStatus(minerAddress);
      } catch (err) {
        onError?.(err instanceof Error ? err : new Error(String(err)));
      }

      while (!stopped) {
        await new Promise((r) => setTimeout(r, intervalMs));
        if (stopped) break;

        try {
          // Check for new earnings
          if (onEarning) {
            const earnings = await this.getRecentEarnings(minerAddress);
            for (const e of earnings) {
              const key = `${e.blockHeight}:${e.taskId}`;
              if (!knownEarningBlocks.has(key)) {
                knownEarningBlocks.add(key);
                onEarning(e);
              }
            }
          }

          // Check for status changes
          const currentStatus = await this.getStatus(minerAddress);
          if (onStatusChange && lastStatus) {
            if (
              lastStatus.totalEarned !== currentStatus.totalEarned ||
              lastStatus.available !== currentStatus.available ||
              lastStatus.contributionScore !== currentStatus.contributionScore
            ) {
              onStatusChange(lastStatus, currentStatus);
            }
          }
          lastStatus = currentStatus;
        } catch (err) {
          onError?.(err instanceof Error ? err : new Error(String(err)));
        }
      }
    };

    poll();
    return { stop: () => { stopped = true; } };
  }

  /** Get miner's current status (balance, score, vesting) */
  async getStatus(minerAddress: string): Promise<MinerStatus> {
    const [vesting, contribution] = await Promise.all([
      rpcCall(this.provider, 'qfc_getMinerVesting', [minerAddress]).catch(() => null),
      rpcCall(this.provider, 'qfc_getContributionScore', [minerAddress]).catch(() => null),
    ]);

    const totalEarned = vesting?.totalEarned ?? '0x0';
    const locked = vesting?.locked ?? '0x0';
    const available = vesting?.available ?? '0x0';

    return {
      address: minerAddress.toLowerCase(),
      totalEarned,
      totalEarnedQfc: this.formatWei(totalEarned),
      locked,
      available,
      contributionScore: Number(contribution?.score ?? 0),
      activeTranches: Number(vesting?.activeTranches ?? 0),
    };
  }

  /** Get recent earnings for a miner */
  async getRecentEarnings(minerAddress: string): Promise<MinerEarning[]> {
    const raw = await rpcCall(
      this.provider,
      'qfc_getMinerEarnings',
      [minerAddress],
    ).catch(() => []);

    if (!Array.isArray(raw)) return [];

    return raw.map((e: any) => ({
      blockHeight: Number(e.blockHeight),
      taskId: e.taskId ?? '',
      reward: e.reward ?? '0x0',
      rewardQfc: this.formatWei(e.reward ?? '0x0'),
      taskType: e.taskType ?? 'unknown',
      modelId: e.modelId ?? '',
      executionTimeMs: Number(e.executionTimeMs ?? 0),
      timestamp: Number(e.timestamp ?? 0),
    }));
  }

  /**
   * Format a notification message for an earning event.
   * Useful for sending to Telegram, Discord, etc.
   */
  formatEarningMessage(earning: MinerEarning): string {
    const config = getNetworkConfig(this.network);
    const explorerUrl = config.explorerUrl;
    const blockUrl = `${explorerUrl}/blocks/${earning.blockHeight}`;
    return [
      `✅ Inference task completed!`,
      `Earned: ${earning.rewardQfc} QFC`,
      `Task: ${earning.taskType}${earning.modelId ? ` (${earning.modelId})` : ''}`,
      `Block: ${earning.blockHeight}`,
      `Time: ${earning.executionTimeMs}ms`,
      blockUrl,
    ].join('\n');
  }

  /**
   * Format a status summary message.
   */
  formatStatusMessage(status: MinerStatus): string {
    const config = getNetworkConfig(this.network);
    const explorerUrl = config.explorerUrl;
    const minerUrl = `${explorerUrl}/miner/${status.address}`;
    return [
      `⛏️ Miner Status`,
      `Total Earned: ${status.totalEarnedQfc} QFC`,
      `Available: ${this.formatWei(status.available)} QFC`,
      `Locked: ${this.formatWei(status.locked)} QFC`,
      `Score: ${status.contributionScore}/100`,
      minerUrl,
    ].join('\n');
  }

  private formatWei(hex: string): string {
    try {
      return ethers.formatEther(BigInt(hex));
    } catch {
      return '0.0';
    }
  }
}
