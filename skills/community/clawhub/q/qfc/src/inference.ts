import { NetworkName, createProvider, rpcCall } from './provider.js';
import { ethers } from 'ethers';

export interface InferenceTaskStatus {
  taskId: string;
  status: 'Pending' | 'Assigned' | 'Completed' | 'Failed' | 'Expired' | 'NotFound';
  submitter: string;
  taskType: string;
  modelId: string;
  createdAt: number;
  deadline: number;
  maxFee: string;
  /** How the result is stored: 'inline' (embedded in `result`) or 'ipfs' (fetch via `resultCid`) */
  resultType?: 'inline' | 'ipfs';
  /** Base64-encoded result (present when resultType is 'inline') */
  result?: string;
  /** IPFS CID of the result (present when resultType is 'ipfs') */
  resultCid?: string;
  /** Base64-encoded preview of the first ~1KB (present when resultType is 'ipfs') */
  resultPreview?: string;
  resultSize?: number;
  minerAddress?: string;
  executionTimeMs?: number;
}

export interface SubmitTaskRequest {
  /** Task type, e.g. "text_generation", "speech_to_text" */
  taskType: string;
  /** Model identifier, e.g. "qwen2.5-0.5b" */
  modelId: string;
  /** Input data (base64-encoded for binary, plain text for text tasks) */
  inputData: string;
  /** Maximum fee in wei (hex string, e.g. "0x2386f26fc10000") */
  maxFee: string;
  /** Submitter address (hex) */
  submitter: string;
  /** Ed25519 signature over (taskType || modelId || inputData || maxFee) */
  signature: string;
  /** Language code for speech_to_text tasks (e.g. "en", "zh") */
  language?: string;
}

export interface InferenceModel {
  name: string;
  version: string;
  minMemoryMb: number;
  minTier: string;
  approved: boolean;
}

export interface DecodedResult {
  model: string;
  submitter: string;
  miner: string;
  output: any;
  executionTimeMs: number;
  timestamps: {
    submitted: number;
    completed: number;
  };
}

export interface FeeEstimate {
  baseFee: string;
  model: string;
  gpuTier: string;
  estimatedTimeMs: number;
}

/**
 * QFCInference — submit and query AI inference tasks on QFC.
 */
export class QFCInference {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /** List approved models */
  async getModels(): Promise<InferenceModel[]> {
    return rpcCall(this.provider, 'qfc_getSupportedModels', []);
  }

  /** Get inference statistics (tasks completed, avg time, FLOPS, pass rate) */
  async getStats(): Promise<{
    tasksCompleted: number;
    avgTimeMs: number;
    flopsTotal: string;
    passRate: number;
  }> {
    const r = await rpcCall(this.provider, 'qfc_getInferenceStats', []);
    return {
      tasksCompleted: Number(r.tasksCompleted),
      avgTimeMs: Number(r.avgTimeMs),
      flopsTotal: String(r.flopsTotal),
      passRate: Number(r.passRate),
    };
  }

  /** Query the status of a submitted inference task */
  async getTaskStatus(taskId: string): Promise<InferenceTaskStatus> {
    try {
      return await rpcCall(this.provider, 'qfc_getPublicTaskStatus', [taskId]);
    } catch (err: any) {
      if (typeof err?.message === 'string' && err.message.includes('Task not found')) {
        return {
          taskId,
          status: 'NotFound',
          submitter: '',
          taskType: '',
          modelId: '',
          createdAt: 0,
          deadline: 0,
          maxFee: '0',
        } as InferenceTaskStatus;
      }
      throw err;
    }
  }

  /**
   * Poll until the task reaches a terminal state.
   * @param taskId - Task ID (hex)
   * @param timeoutMs - Max wait (default 120s)
   * @param intervalMs - Poll interval (default 2s)
   */
  async waitForResult(
    taskId: string,
    timeoutMs: number = 120_000,
    intervalMs: number = 2_000,
  ): Promise<InferenceTaskStatus> {
    const deadline = Date.now() + timeoutMs;
    let sawInProgress = false;
    while (Date.now() < deadline) {
      const status = await this.getTaskStatus(taskId);
      if (status.status === 'Pending' || status.status === 'Assigned') {
        sawInProgress = true;
      }
      if (status.status === 'Completed' || status.status === 'Failed' || status.status === 'Expired') {
        return status;
      }
      // qfc-core #69: completed/expired/failed tasks are deleted from TaskPool,
      // so getTaskStatus returns NotFound. If we previously saw the task in progress,
      // treat this as Expired rather than an error.
      if (status.status === 'NotFound' && sawInProgress) {
        return {
          ...status,
          status: 'Expired',
          result: undefined,
          resultType: undefined,
          _note: 'Task disappeared from TaskPool after being in progress (qfc-core #69). Likely Expired.',
        } as InferenceTaskStatus & { _note: string };
      }
      if (status.status === 'NotFound') {
        return status;
      }
      await new Promise((r) => setTimeout(r, intervalMs));
    }
    return this.getTaskStatus(taskId);
  }

  /**
   * Submit a public inference task.
   * @param modelId - model ID from the registry (e.g. "qfc-embed-small")
   * @param taskType - task type (e.g. "TextEmbedding", "TextGeneration")
   * @param input - input data (text string — will be base64-encoded automatically)
   * @param maxFee - maximum fee in QFC (e.g. "0.5")
   * @param signer - wallet to sign and pay for the task
   */
  async submitTask(
    modelId: string,
    taskType: string,
    input: string,
    maxFee: string,
    signer: ethers.Wallet,
  ): Promise<string> {
    const inputData = Buffer.from(input).toString('base64');
    const payload = {
      modelId,
      taskType,
      inputData,
      maxFee: ethers.parseEther(maxFee).toString(),
      submitter: signer.address,
    };
    const message = JSON.stringify(payload);
    const signature = await signer.signMessage(message);
    const result = await rpcCall(this.provider, 'qfc_submitPublicTask', [
      { ...payload, signature },
    ]);
    return typeof result === 'string' ? result : result.taskId;
  }

  /** Estimate the fee for an inference task */
  async estimateFee(modelId: string, taskType: string = 'TextEmbedding', inputSize: number = 0): Promise<FeeEstimate> {
    const raw = await rpcCall(this.provider, 'qfc_estimateInferenceFee', [
      { modelId, taskType, inputSize },
    ]);
    return {
      baseFee: ethers.formatEther(BigInt(raw.baseFee)),
      model: raw.modelId,
      gpuTier: raw.gpuTier,
      estimatedTimeMs: Number(raw.estimatedTimeMs),
    };
  }

  /**
   * Fetch the full IPFS result for a given CID via the node's gateway proxy.
   * Calls `qfc_getInferenceResult` and returns the base64-encoded content.
   *
   * @param cid - IPFS content identifier (e.g. "QmXYZ...")
   * @returns Base64-encoded result payload
   */
  async fetchIpfsResult(cid: string): Promise<string> {
    return rpcCall(this.provider, 'qfc_getInferenceResult', [cid]);
  }

  /**
   * Unified method to retrieve the result of a completed inference task,
   * regardless of whether it was stored inline or on IPFS.
   *
   * - If `resultType` is `'inline'`, returns the `result` field directly.
   * - If `resultType` is `'ipfs'`, fetches the full content via `fetchIpfsResult`.
   * - For legacy responses without `resultType`, falls back to `result`.
   *
   * @param taskId - Task ID (hex)
   * @returns Base64-encoded result string
   * @throws If the task has no result or is not completed
   */
  async getResult(taskId: string): Promise<string> {
    const status = await this.getTaskStatus(taskId);
    if (status.status !== 'Completed') {
      throw new Error(`Task ${taskId} is not completed (status: ${status.status})`);
    }

    if (status.resultType === 'ipfs') {
      if (!status.resultCid) {
        throw new Error(`Task ${taskId} has resultType 'ipfs' but no resultCid`);
      }
      return this.fetchIpfsResult(status.resultCid);
    }

    // inline or legacy (no resultType field)
    if (!status.result) {
      throw new Error(`Task ${taskId} is completed but has no result`);
    }
    return status.result;
  }

  /**
   * Decode a base64 result payload from a completed task.
   * Works with both inline and IPFS-fetched results — both are base64-encoded
   * JSON envelopes with the same structure.
   */
  decodeResult(base64Result: string): DecodedResult {
    const json = Buffer.from(base64Result, 'base64').toString('utf-8');
    const envelope = JSON.parse(json);
    const outputRaw = Buffer.from(envelope.output_base64, 'base64').toString('utf-8');
    let output: any;
    try {
      output = JSON.parse(outputRaw);
    } catch {
      output = outputRaw;
    }
    return {
      model: envelope.model,
      submitter: envelope.submitter,
      miner: envelope.miner,
      output,
      executionTimeMs: envelope.execution_time_ms,
      timestamps: {
        submitted: envelope.submitted_at,
        completed: envelope.completed_at,
      },
    };
  }

  /**
   * Decode a base64 result payload to raw bytes.
   */
  decodeResultBytes(base64Result: string): Uint8Array {
    return Buffer.from(base64Result, 'base64');
  }
}
