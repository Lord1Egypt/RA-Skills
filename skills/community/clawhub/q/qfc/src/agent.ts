import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

/**
 * Permission enum values matching the AgentRegistry contract.
 * 0 = InferenceSubmit, 1 = Transfer, 2 = StakeDelegate, 3 = QueryOnly
 */
export type AgentPermission = 'InferenceSubmit' | 'Transfer' | 'StakeDelegate' | 'QueryOnly';

const PERMISSION_VALUES: Record<AgentPermission, number> = {
  InferenceSubmit: 0,
  Transfer: 1,
  StakeDelegate: 2,
  QueryOnly: 3,
};

/** Agent info returned by getAgent */
export interface AgentInfo {
  agentId: string;
  owner: string;
  agentAddress: string;
  permissions: number[];
  dailyLimit: string;
  maxPerTx: string;
  deposit: string;
  spentToday: string;
  lastSpendDay: bigint;
  registeredAt: bigint;
  active: boolean;
}

/** Session key info returned by getSessionKey */
export interface SessionKeyInfo {
  agentId: string;
  keyAddress: string;
  expiresAt: bigint;
  active: boolean;
}

/** Result from register/fund/revoke/session-key write operations */
export interface AgentTxResult {
  txHash: string;
  explorerUrl: string;
}

/** Result from registerAgent (includes agentId) */
export interface RegisterAgentResult extends AgentTxResult {
  agentId: string;
}

/** Reverse mapping from numeric permission to name */
const PERMISSION_NAMES: Record<number, AgentPermission> = {
  0: 'InferenceSubmit',
  1: 'Transfer',
  2: 'StakeDelegate',
  3: 'QueryOnly',
};

/** Preflight check result — returned before tx submission */
export interface PreflightResult {
  allowed: boolean;
  reasons: string[];
  warnings: string[];
  agent: AgentInfo | null;
  sessionKeyValid?: boolean;
}

/** Options for preflight policy check */
export interface PreflightOptions {
  agentId: string;
  /** Permission required for the operation */
  requiredPermission?: AgentPermission;
  /** Amount in QFC the operation will spend */
  amountQFC?: string;
  /** Session key address to validate (optional) */
  sessionKeyAddress?: string;
}

/** Registry addresses per network */
const REGISTRY_ADDRESS: Record<NetworkName, string> = {
  testnet: '0x7791dfa4d489f3d524708cbc0caa8689b76322b3',
  mainnet: '0x0000000000000000000000000000000000000000', // TBD
};

const AGENT_REGISTRY_ABI = [
  'function registerAgent(string agentId, address agentAddress, uint8[] permissions, uint256 dailyLimit, uint256 maxPerTx) payable returns (string)',
  'function fundAgent(string agentId) payable',
  'function revokeAgent(string agentId)',
  'function getAgent(string agentId) view returns (tuple(string agentId, address owner, address agentAddress, uint8[] permissions, uint256 dailyLimit, uint256 maxPerTx, uint256 deposit, uint256 spentToday, uint256 lastSpendDay, uint256 registeredAt, bool active))',
  'function getAgentsByOwner(address owner) view returns (string[])',
  'function issueSessionKey(string agentId, address sessionKeyAddress, uint256 durationSeconds)',
  'function rotateSessionKey(string agentId, address oldKeyAddress, address newKeyAddress, uint256 durationSeconds)',
  'function revokeSessionKey(string agentId, address keyAddress)',
  'function getSessionKey(string agentId, address keyAddress) view returns (tuple(string agentId, address keyAddress, uint256 expiresAt, bool active))',
  'function isSessionKeyValid(address keyAddress) view returns (bool)',
];

/**
 * QFCAgent — AI Agent Registry interaction.
 *
 * Manages on-chain agent accounts: registration, funding, revocation,
 * session key lifecycle (issue, rotate, revoke, validate), and querying agent info.
 *
 * @example
 * ```ts
 * const agent = new QFCAgent('testnet');
 * // Register
 * const result = await agent.registerAgent(signer, 'my-agent', agentAddr, ['Transfer'], '100', '10', '5');
 * // Issue session key
 * await agent.issueSessionKey(signer, 'my-agent', sessionAddr, 3600);
 * // Rotate session key
 * await agent.rotateSessionKey(signer, 'my-agent', oldAddr, newAddr, 3600);
 * // Revoke session key
 * await agent.revokeSessionKey(signer, 'my-agent', sessionAddr);
 * ```
 */
export class QFCAgent {
  private provider: ethers.JsonRpcProvider;
  private registryAddress: string;
  private network: NetworkName;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.network = network;
    this.provider = createProvider(network);
    this.networkConfig = getNetworkConfig(network);
    this.registryAddress = REGISTRY_ADDRESS[network];
  }

  private getContract(signerOrProvider?: ethers.Signer | ethers.Provider): ethers.Contract {
    return new ethers.Contract(
      this.registryAddress,
      AGENT_REGISTRY_ABI,
      signerOrProvider ?? this.provider,
    );
  }

  /** Poll for transaction receipt via raw RPC (avoids ethers.js log-parsing issues on QFC) */
  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; blockNumber: string; gasUsed: string }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return raw;
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  private explorerTxUrl(txHash: string): string {
    return `${this.networkConfig.explorerUrl}/txs/${txHash}`;
  }

  private requireAgentId(agentId: string): void {
    if (!agentId || agentId.trim().length === 0) {
      throw new Error('agentId must be a non-empty string.');
    }
  }

  private requireAddress(address: string, label: string): void {
    if (!ethers.isAddress(address)) {
      throw new Error(`Invalid ${label} format. Expected 0x + 40 hex characters.`);
    }
  }

  private requirePositiveAmount(value: string, label: string): void {
    const parsed = parseFloat(value);
    if (isNaN(parsed) || parsed <= 0) {
      throw new Error(`${label} must be a positive number.`);
    }
  }

  /**
   * Register a new AI agent on the registry.
   * @param ownerSigner - wallet of the agent owner
   * @param agentId - unique string identifier for the agent
   * @param agentAddress - the agent's on-chain address
   * @param permissions - array of permission types
   * @param dailyLimitQFC - daily spending limit in QFC
   * @param maxPerTxQFC - max spend per transaction in QFC
   * @param depositQFC - initial deposit in QFC (sent as msg.value)
   */
  async registerAgent(
    ownerSigner: ethers.Signer,
    agentId: string,
    agentAddress: string,
    permissions: AgentPermission[],
    dailyLimitQFC: string,
    maxPerTxQFC: string,
    depositQFC: string,
  ): Promise<RegisterAgentResult> {
    this.requireAgentId(agentId);
    this.requireAddress(agentAddress, 'agentAddress');
    this.requirePositiveAmount(dailyLimitQFC, 'dailyLimitQFC');
    this.requirePositiveAmount(maxPerTxQFC, 'maxPerTxQFC');
    this.requirePositiveAmount(depositQFC, 'depositQFC');
    if (permissions.length === 0) {
      throw new Error('At least one permission is required.');
    }

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);
    const permissionValues = permissions.map((p) => PERMISSION_VALUES[p]);

    const tx = await contract.registerAgent(
      agentId,
      agentAddress,
      permissionValues,
      ethers.parseEther(dailyLimitQFC),
      ethers.parseEther(maxPerTxQFC),
      { value: ethers.parseEther(depositQFC), gasLimit: 500_000 },
    );

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`registerAgent reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, agentId, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Fund an existing agent with additional QFC.
   */
  async fundAgent(
    ownerSigner: ethers.Signer,
    agentId: string,
    amountQFC: string,
  ): Promise<AgentTxResult> {
    this.requireAgentId(agentId);
    this.requirePositiveAmount(amountQFC, 'amountQFC');

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);

    const tx = await contract.fundAgent(agentId, {
      value: ethers.parseEther(amountQFC),
      gasLimit: 200_000,
    });

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`fundAgent reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Revoke an agent, deactivating it on the registry.
   */
  async revokeAgent(
    ownerSigner: ethers.Signer,
    agentId: string,
  ): Promise<AgentTxResult> {
    this.requireAgentId(agentId);

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);

    const tx = await contract.revokeAgent(agentId, { gasLimit: 200_000 });

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`revokeAgent reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Get agent info by ID.
   */
  async getAgent(agentId: string): Promise<AgentInfo> {
    this.requireAgentId(agentId);

    const contract = this.getContract(this.provider);
    const result = await contract.getAgent(agentId);

    return {
      agentId: result.agentId,
      owner: result.owner,
      agentAddress: result.agentAddress,
      permissions: Array.from(result.permissions).map(Number),
      dailyLimit: ethers.formatEther(result.dailyLimit),
      maxPerTx: ethers.formatEther(result.maxPerTx),
      deposit: ethers.formatEther(result.deposit),
      spentToday: ethers.formatEther(result.spentToday),
      lastSpendDay: BigInt(result.lastSpendDay),
      registeredAt: BigInt(result.registeredAt),
      active: result.active,
    };
  }

  /**
   * List all agent IDs owned by an address.
   */
  async listAgents(ownerAddress: string): Promise<string[]> {
    this.requireAddress(ownerAddress, 'ownerAddress');

    const contract = this.getContract(this.provider);
    return contract.getAgentsByOwner(ownerAddress);
  }

  /**
   * Issue a session key for an agent.
   * @param durationSeconds - how long the session key is valid (must be > 0)
   */
  async issueSessionKey(
    ownerSigner: ethers.Signer,
    agentId: string,
    sessionKeyAddress: string,
    durationSeconds: number,
  ): Promise<AgentTxResult> {
    this.requireAgentId(agentId);
    this.requireAddress(sessionKeyAddress, 'sessionKeyAddress');
    if (!Number.isInteger(durationSeconds) || durationSeconds <= 0) {
      throw new Error('durationSeconds must be a positive integer.');
    }

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);

    const tx = await contract.issueSessionKey(agentId, sessionKeyAddress, durationSeconds, {
      gasLimit: 200_000,
    });

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`issueSessionKey reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Rotate a session key: atomically revoke the old key and issue a new one.
   * @param oldKeyAddress - the session key address to revoke
   * @param newKeyAddress - the new session key address to authorize
   * @param durationSeconds - validity period for the new key (must be > 0)
   */
  async rotateSessionKey(
    ownerSigner: ethers.Signer,
    agentId: string,
    oldKeyAddress: string,
    newKeyAddress: string,
    durationSeconds: number,
  ): Promise<AgentTxResult> {
    this.requireAgentId(agentId);
    this.requireAddress(oldKeyAddress, 'oldKeyAddress');
    this.requireAddress(newKeyAddress, 'newKeyAddress');
    if (oldKeyAddress.toLowerCase() === newKeyAddress.toLowerCase()) {
      throw new Error('newKeyAddress must differ from oldKeyAddress.');
    }
    if (!Number.isInteger(durationSeconds) || durationSeconds <= 0) {
      throw new Error('durationSeconds must be a positive integer.');
    }

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);

    const tx = await contract.rotateSessionKey(
      agentId,
      oldKeyAddress,
      newKeyAddress,
      durationSeconds,
      { gasLimit: 300_000 },
    );

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`rotateSessionKey reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Revoke a session key, immediately deactivating it.
   */
  async revokeSessionKey(
    ownerSigner: ethers.Signer,
    agentId: string,
    keyAddress: string,
  ): Promise<AgentTxResult> {
    this.requireAgentId(agentId);
    this.requireAddress(keyAddress, 'keyAddress');

    const connected = ownerSigner.connect(this.provider);
    const contract = this.getContract(connected);

    const tx = await contract.revokeSessionKey(agentId, keyAddress, { gasLimit: 200_000 });

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`revokeSessionKey reverted (tx: ${tx.hash})`);
    }

    return { txHash: tx.hash, explorerUrl: this.explorerTxUrl(tx.hash) };
  }

  /**
   * Get session key details for an agent.
   */
  async getSessionKey(agentId: string, keyAddress: string): Promise<SessionKeyInfo> {
    this.requireAgentId(agentId);
    this.requireAddress(keyAddress, 'keyAddress');

    const contract = this.getContract(this.provider);
    const result = await contract.getSessionKey(agentId, keyAddress);

    return {
      agentId: result.agentId,
      keyAddress: result.keyAddress,
      expiresAt: BigInt(result.expiresAt),
      active: result.active,
    };
  }

  /**
   * Check if a session key address is still valid.
   */
  async isSessionKeyValid(keyAddress: string): Promise<boolean> {
    this.requireAddress(keyAddress, 'keyAddress');

    const contract = this.getContract(this.provider);
    return contract.isSessionKeyValid(keyAddress);
  }

  // ===================================================
  // Safe Execution Mode — preflight policy checks
  // ===================================================

  /**
   * Run preflight policy checks against on-chain state before submitting a tx.
   * Returns whether the operation is allowed with human-readable deny reasons.
   *
   * Checks performed:
   * - Agent exists and is active
   * - Required permission is granted
   * - Amount within per-tx limit (maxPerTx)
   * - Amount within remaining daily budget (dailyLimit − spentToday)
   * - Sufficient deposit balance
   * - Session key validity (if provided)
   */
  async preflight(opts: PreflightOptions): Promise<PreflightResult> {
    this.requireAgentId(opts.agentId);

    const reasons: string[] = [];
    const warnings: string[] = [];
    let agent: AgentInfo | null = null;
    let sessionKeyValid: boolean | undefined;

    // 1. Fetch agent from chain
    try {
      agent = await this.getAgent(opts.agentId);
    } catch {
      return { allowed: false, reasons: [`Agent "${opts.agentId}" not found on-chain.`], warnings, agent: null };
    }

    // 2. Active check
    if (!agent.active) {
      reasons.push(`Agent "${opts.agentId}" is revoked/inactive.`);
    }

    // 3. Permission check
    if (opts.requiredPermission) {
      const requiredValue = PERMISSION_VALUES[opts.requiredPermission];
      if (!agent.permissions.includes(requiredValue)) {
        const granted = agent.permissions
          .map((p) => PERMISSION_NAMES[p] ?? `unknown(${p})`)
          .join(', ');
        reasons.push(
          `Missing permission "${opts.requiredPermission}". Agent has: [${granted}].`,
        );
      }
    }

    // 4. Amount checks (if spending QFC)
    if (opts.amountQFC) {
      const amount = parseFloat(opts.amountQFC);
      const maxPerTx = parseFloat(agent.maxPerTx);
      const dailyLimit = parseFloat(agent.dailyLimit);
      const spentToday = parseFloat(agent.spentToday);
      const deposit = parseFloat(agent.deposit);

      if (amount > maxPerTx) {
        reasons.push(
          `Amount ${opts.amountQFC} QFC exceeds per-tx limit of ${agent.maxPerTx} QFC.`,
        );
      }

      const remainingDaily = dailyLimit - spentToday;
      if (amount > remainingDaily) {
        reasons.push(
          `Amount ${opts.amountQFC} QFC exceeds remaining daily budget of ${remainingDaily.toFixed(4)} QFC (limit: ${agent.dailyLimit}, spent: ${agent.spentToday}).`,
        );
      } else if (amount > remainingDaily * 0.8) {
        warnings.push(
          `This tx uses ${((amount / remainingDaily) * 100).toFixed(0)}% of remaining daily budget (${remainingDaily.toFixed(4)} QFC left).`,
        );
      }

      if (amount > deposit) {
        reasons.push(
          `Insufficient deposit: ${agent.deposit} QFC available, ${opts.amountQFC} QFC required.`,
        );
      } else if (amount > deposit * 0.9) {
        warnings.push(
          `Deposit nearly depleted: ${agent.deposit} QFC remaining after this tx.`,
        );
      }
    }

    // 5. Session key check (if provided)
    if (opts.sessionKeyAddress) {
      this.requireAddress(opts.sessionKeyAddress, 'sessionKeyAddress');
      try {
        sessionKeyValid = await this.isSessionKeyValid(opts.sessionKeyAddress);
        if (!sessionKeyValid) {
          reasons.push(
            `Session key ${opts.sessionKeyAddress} is expired or revoked.`,
          );
        }
      } catch {
        warnings.push(`Could not verify session key ${opts.sessionKeyAddress} (RPC error).`);
      }
    }

    return {
      allowed: reasons.length === 0,
      reasons,
      warnings,
      agent,
      sessionKeyValid,
    };
  }

  /**
   * Fund an agent with preflight policy checks (safe mode).
   * In dry-run mode, returns the preflight result without submitting the tx.
   */
  async safeFundAgent(
    ownerSigner: ethers.Signer,
    agentId: string,
    amountQFC: string,
    opts?: { dryRun?: boolean; sessionKeyAddress?: string },
  ): Promise<{ preflight: PreflightResult; tx?: AgentTxResult }> {
    const check = await this.preflight({
      agentId,
      amountQFC,
      requiredPermission: 'Transfer',
      sessionKeyAddress: opts?.sessionKeyAddress,
    });

    if (opts?.dryRun || !check.allowed) {
      return { preflight: check };
    }

    const tx = await this.fundAgent(ownerSigner, agentId, amountQFC);
    return { preflight: check, tx };
  }

  /**
   * Generic safe execution wrapper: run preflight, then execute a callback if allowed.
   * In dry-run mode, returns the preflight result without executing.
   *
   * @example
   * ```ts
   * const result = await agent.safeExecute(
   *   { agentId: 'my-agent', requiredPermission: 'Transfer', amountQFC: '5' },
   *   async () => agent.fundAgent(signer, 'my-agent', '5'),
   * );
   * if (!result.preflight.allowed) {
   *   console.log('Denied:', result.preflight.reasons);
   * }
   * ```
   */
  async safeExecute<T>(
    opts: PreflightOptions & { dryRun?: boolean },
    execute: () => Promise<T>,
  ): Promise<{ preflight: PreflightResult; result?: T }> {
    const check = await this.preflight(opts);

    if (opts.dryRun || !check.allowed) {
      return { preflight: check };
    }

    const result = await execute();
    return { preflight: check, result };
  }
}
