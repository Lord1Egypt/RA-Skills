import type { Address } from 'viem';
import { base, mainnet } from 'viem/chains';

export type Operation = 'deposit' | 'redeem' | 'rebalance';
export type ChainSlug = 'ethereum' | 'base';
export type SignerBackend = 'privy' | 'private-key';

export interface RunControls {
  dryRun?: boolean;
  strictMode?: boolean;
  requireConfirm?: boolean;
  confirm?: string;
  maxGasGwei?: string;
  maxAmount?: string;
}

export interface RequiredRunControls {
  dryRun: boolean;
  strictMode: boolean;
  requireConfirm: boolean;
  confirm: string;
  maxGasGwei?: string;
  maxAmount?: string;
}

export interface DepositInput {
  asset: string;
  amount: string;
  vaultId: string;
}

export interface RedeemInput {
  vaultId: string;
  percentage?: number;
  shares?: string;
}

export interface RebalanceInput {
  vaultId: string;
  asset: string;
  percentage?: number;
  shares?: string;
}

export interface PrepareSignExecuteRequest {
  operation: Operation;
  chain?: ChainSlug | string;
  agentAddress?: Address;
  deposit?: DepositInput;
  redeem?: RedeemInput;
  rebalance?: RebalanceInput;
  controls?: RunControls;
}

export interface ResolvedChain {
  slug: ChainSlug;
  chainId: number;
  chain: typeof mainnet | typeof base;
}

export interface HealthSnapshot {
  status?: string;
  sessions?: number;
  tools?: number;
  freshnessStatus?: string;
  latestSnapshotAt?: string | null;
}

export interface RpcOverrideConfig {
  chainRpcUrl?: string;
}

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export function normalizeControls(controls?: RunControls): RequiredRunControls {
  return {
    dryRun: controls?.dryRun ?? false,
    strictMode: controls?.strictMode ?? true,
    requireConfirm: controls?.requireConfirm ?? true,
    confirm: (controls?.confirm ?? '').toLowerCase(),
    maxGasGwei: controls?.maxGasGwei,
    maxAmount: controls?.maxAmount,
  };
}

export function resolveChain(input?: string): ResolvedChain {
  const slug = (input ?? 'base').toLowerCase();
  if (slug === 'base') {
    return { slug: 'base', chainId: 8453, chain: base };
  }
  if (slug === 'ethereum') {
    return { slug: 'ethereum', chainId: 1, chain: mainnet };
  }
  throw new Error(`Unsupported chain "${input}". Allowed: base, ethereum.`);
}

export class PreflightError extends Error {
  constructor(
    public readonly what: string,
    public readonly why: string,
    public readonly fix: string,
  ) {
    super(what);
    this.name = 'PreflightError';
  }
}
