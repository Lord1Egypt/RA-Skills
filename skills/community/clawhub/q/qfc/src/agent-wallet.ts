import { ethers } from 'ethers';
import { NetworkName, createProvider, rpcCall } from './provider.js';
import {
  QFCAgent,
  AgentInfo,
  AgentTxResult,
  RegisterAgentResult,
  AgentPermission,
  SessionKeyInfo,
  PreflightResult,
} from './agent.js';
import { QFCInference, InferenceTaskStatus, DecodedResult, FeeEstimate } from './inference.js';

/** Options for registering a new agent */
export interface RegisterAgentOptions {
  agentId: string;
  agentAddress: string;
  permissions: AgentPermission[];
  dailyLimitQFC: string;
  maxPerTxQFC: string;
  depositQFC: string;
}

/** Session key configuration for the client */
export interface SessionKeyConfig {
  /** Private key of the session key (hex) */
  privateKey: string;
  /** Agent ID this session key belongs to */
  agentId: string;
}

/** Options for issuing a session key */
export interface IssueSessionKeyOptions {
  agentId: string;
  /** Address of the session key (derived from its private key) */
  sessionKeyAddress: string;
  /** Duration in seconds */
  durationSeconds: number;
}

/** Result from session-key-aware inference submission */
export interface AgentInferenceResult {
  taskId: string;
  status: InferenceTaskStatus;
  decoded?: DecodedResult;
}

/**
 * AgentWalletClient — high-level client for AI agent wallet operations.
 *
 * Wraps QFCAgent (on-chain registry) and QFCInference (task submission)
 * to enable session-key-aware operations. An agent can submit inference
 * tasks using a session key instead of the owner's long-lived private key.
 *
 * @example
 * ```ts
 * // Owner registers agent and issues session key
 * const client = new AgentWalletClient('testnet');
 * const ownerWallet = new ethers.Wallet(OWNER_KEY);
 * await client.register(ownerWallet, {
 *   agentId: 'trader-1',
 *   agentAddress: sessionWallet.address,
 *   permissions: ['InferenceSubmit', 'Transfer'],
 *   dailyLimitQFC: '100',
 *   maxPerTxQFC: '10',
 *   depositQFC: '50',
 * });
 * await client.issueSessionKey(ownerWallet, {
 *   agentId: 'trader-1',
 *   sessionKeyAddress: sessionWallet.address,
 *   durationSeconds: 86400,
 * });
 *
 * // Agent operates autonomously with session key (no owner key needed)
 * const agentClient = new AgentWalletClient('testnet', {
 *   privateKey: SESSION_PRIVATE_KEY,
 *   agentId: 'trader-1',
 * });
 * const result = await agentClient.submitInference(
 *   'qfc-embed-small', 'TextEmbedding', 'analyze market sentiment', '0.1',
 * );
 * ```
 */
export class AgentWalletClient {
  private agent: QFCAgent;
  private inference: QFCInference;
  private network: NetworkName;
  private sessionKey?: SessionKeyConfig;
  private sessionWallet?: ethers.Wallet;

  constructor(network: NetworkName = 'testnet', sessionKey?: SessionKeyConfig) {
    this.network = network;
    this.agent = new QFCAgent(network);
    this.inference = new QFCInference(network);

    if (sessionKey) {
      this.sessionKey = sessionKey;
      this.sessionWallet = new ethers.Wallet(sessionKey.privateKey);
    }
  }

  // ===================================================
  // Agent Lifecycle (owner operations)
  // ===================================================

  /** Register a new agent on-chain. Requires owner signer. */
  async register(
    ownerSigner: ethers.Signer,
    opts: RegisterAgentOptions,
  ): Promise<RegisterAgentResult> {
    return this.agent.registerAgent(
      ownerSigner,
      opts.agentId,
      opts.agentAddress,
      opts.permissions,
      opts.dailyLimitQFC,
      opts.maxPerTxQFC,
      opts.depositQFC,
    );
  }

  /** Fund an agent with additional QFC. Requires owner signer. */
  async fund(
    ownerSigner: ethers.Signer,
    agentId: string,
    amountQFC: string,
  ): Promise<AgentTxResult> {
    return this.agent.fundAgent(ownerSigner, agentId, amountQFC);
  }

  /** Revoke an agent, deactivating it. Requires owner signer. */
  async revoke(
    ownerSigner: ethers.Signer,
    agentId: string,
  ): Promise<AgentTxResult> {
    return this.agent.revokeAgent(ownerSigner, agentId);
  }

  /** Get agent info by ID. */
  async status(agentId: string): Promise<AgentInfo> {
    return this.agent.getAgent(agentId);
  }

  /** List all agent IDs owned by an address. */
  async list(ownerAddress: string): Promise<string[]> {
    return this.agent.listAgents(ownerAddress);
  }

  // ===================================================
  // Session Key Management (owner operations)
  // ===================================================

  /** Issue a session key for an agent. Requires owner signer. */
  async issueSessionKey(
    ownerSigner: ethers.Signer,
    opts: IssueSessionKeyOptions,
  ): Promise<AgentTxResult> {
    return this.agent.issueSessionKey(
      ownerSigner,
      opts.agentId,
      opts.sessionKeyAddress,
      opts.durationSeconds,
    );
  }

  /** Rotate a session key: revoke old, issue new. Requires owner signer. */
  async rotateSessionKey(
    ownerSigner: ethers.Signer,
    agentId: string,
    oldKeyAddress: string,
    newKeyAddress: string,
    durationSeconds: number,
  ): Promise<AgentTxResult> {
    return this.agent.rotateSessionKey(
      ownerSigner,
      agentId,
      oldKeyAddress,
      newKeyAddress,
      durationSeconds,
    );
  }

  /** Revoke a session key. Requires owner signer. */
  async revokeSessionKey(
    ownerSigner: ethers.Signer,
    agentId: string,
    keyAddress: string,
  ): Promise<AgentTxResult> {
    return this.agent.revokeSessionKey(ownerSigner, agentId, keyAddress);
  }

  /** Get session key info. */
  async getSessionKey(agentId: string, keyAddress: string): Promise<SessionKeyInfo> {
    return this.agent.getSessionKey(agentId, keyAddress);
  }

  /** Check if a session key is still valid. */
  async isSessionKeyValid(keyAddress: string): Promise<boolean> {
    return this.agent.isSessionKeyValid(keyAddress);
  }

  // ===================================================
  // Session-Key-Aware Inference (agent operations)
  // ===================================================

  /**
   * Submit an inference task using the session key (no owner key needed).
   *
   * The task is signed by the session key wallet. The on-chain registry
   * validates that the session key is authorized for the agent and has
   * the InferenceSubmit permission.
   *
   * @param modelId - Model ID (e.g. "qfc-embed-small")
   * @param taskType - Task type (e.g. "TextEmbedding", "TextGeneration")
   * @param input - Input text
   * @param maxFeeQFC - Maximum fee in QFC
   * @param opts - Optional: waitForResult (default true), timeoutMs
   */
  async submitInference(
    modelId: string,
    taskType: string,
    input: string,
    maxFeeQFC: string,
    opts?: { waitForResult?: boolean; timeoutMs?: number },
  ): Promise<AgentInferenceResult> {
    if (!this.sessionKey || !this.sessionWallet) {
      throw new Error(
        'No session key configured. Create AgentWalletClient with a SessionKeyConfig to use session-key inference.',
      );
    }

    // Preflight: verify agent is active and session key is valid
    const preflight = await this.agent.preflight({
      agentId: this.sessionKey.agentId,
      requiredPermission: 'InferenceSubmit',
      amountQFC: maxFeeQFC,
      sessionKeyAddress: this.sessionWallet.address,
    });

    if (!preflight.allowed) {
      throw new Error(
        `Preflight denied: ${preflight.reasons.join('; ')}`,
      );
    }

    // Submit task signed by the session key wallet
    const provider = createProvider(this.network);
    const connectedWallet = this.sessionWallet.connect(provider);
    const taskId = await this.inference.submitTask(
      modelId,
      taskType,
      input,
      maxFeeQFC,
      connectedWallet,
    );

    // Optionally wait for result
    const shouldWait = opts?.waitForResult !== false;
    if (shouldWait) {
      const status = await this.inference.waitForResult(
        taskId,
        opts?.timeoutMs ?? 120_000,
      );
      let decoded: DecodedResult | undefined;
      if (status.status === 'Completed' && status.result) {
        try {
          decoded = this.inference.decodeResult(status.result);
        } catch {
          // result may be in IPFS — caller can fetch separately
        }
      }
      return { taskId, status, decoded };
    }

    const status = await this.inference.getTaskStatus(taskId);
    return { taskId, status };
  }

  /** Estimate fee for an inference task. */
  async estimateFee(
    modelId: string,
    taskType?: string,
    inputSize?: number,
  ): Promise<FeeEstimate> {
    return this.inference.estimateFee(modelId, taskType, inputSize);
  }

  /** Get the session key wallet address (if configured). */
  get sessionKeyAddress(): string | undefined {
    return this.sessionWallet?.address;
  }

  /** Get the agent ID associated with the session key (if configured). */
  get agentId(): string | undefined {
    return this.sessionKey?.agentId;
  }

  // ===================================================
  // Safe Execution (preflight + execute)
  // ===================================================

  /** Run preflight checks without submitting. */
  async preflight(agentId: string, opts?: {
    requiredPermission?: AgentPermission;
    amountQFC?: string;
    sessionKeyAddress?: string;
  }): Promise<PreflightResult> {
    return this.agent.preflight({
      agentId,
      ...opts,
      sessionKeyAddress: opts?.sessionKeyAddress ?? this.sessionWallet?.address,
    });
  }

  /**
   * Safely fund an agent: run preflight checks, then fund if allowed.
   * In dry-run mode, returns only the preflight result.
   */
  async safeFund(
    ownerSigner: ethers.Signer,
    agentId: string,
    amountQFC: string,
    opts?: { dryRun?: boolean },
  ): Promise<{ preflight: PreflightResult; tx?: AgentTxResult }> {
    return this.agent.safeFundAgent(ownerSigner, agentId, amountQFC, {
      dryRun: opts?.dryRun,
      sessionKeyAddress: this.sessionWallet?.address,
    });
  }
}
