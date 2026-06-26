import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

export interface BlockInfo {
  number: number;
  hash: string;
  parentHash: string;
  timestamp: number;
  miner: string;
  gasUsed: number;
  gasLimit: number;
  transactionCount: number;
  stateRoot: string;
}

export interface TransactionInfo {
  hash: string;
  from: string;
  to: string | null;
  value: string;
  gasPrice: string;
  blockNumber: number | null;
  status: 'pending' | 'confirmed';
}

export interface ReceiptInfo {
  txHash: string;
  blockNumber: number;
  from: string;
  to: string | null;
  gasUsed: number;
  status: 'success' | 'failed';
  contractAddress: string | null;
  logs: LogInfo[];
}

export interface LogInfo {
  address: string;
  topics: string[];
  data: string;
}

/**
 * QFCChain — query blocks, transactions, and receipts on QFC.
 */
export class QFCChain {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /** Get the latest block number */
  async getBlockNumber(): Promise<number> {
    return this.provider.getBlockNumber();
  }

  /** Get block info by number or 'latest' */
  async getBlock(blockNumber: number | 'latest'): Promise<BlockInfo> {
    const tag = blockNumber === 'latest' ? 'latest' : blockNumber;
    const block = await this.provider.getBlock(tag);
    if (!block) {
      throw new Error(`Block not found: ${blockNumber}`);
    }
    return {
      number: block.number,
      hash: block.hash!,
      parentHash: block.parentHash,
      timestamp: block.timestamp,
      miner: block.miner,
      gasUsed: Number(block.gasUsed),
      gasLimit: Number(block.gasLimit),
      transactionCount: block.transactions.length,
      stateRoot: block.stateRoot ?? '',
    };
  }

  /** Get transaction by hash */
  async getTransaction(txHash: string): Promise<TransactionInfo | null> {
    const tx = await this.provider.getTransaction(txHash);
    if (!tx) return null;
    return {
      hash: tx.hash,
      from: tx.from,
      to: tx.to,
      value: ethers.formatEther(tx.value),
      gasPrice: ethers.formatUnits(tx.gasPrice ?? 0n, 'gwei'),
      blockNumber: tx.blockNumber,
      status: tx.blockNumber != null ? 'confirmed' : 'pending',
    };
  }

  /** Get transaction receipt */
  async getReceipt(txHash: string): Promise<ReceiptInfo | null> {
    const receipt = await this.provider.getTransactionReceipt(txHash);
    if (!receipt) return null;
    return {
      txHash: receipt.hash,
      blockNumber: receipt.blockNumber,
      from: receipt.from,
      to: receipt.to,
      gasUsed: Number(receipt.gasUsed),
      status: receipt.status === 1 ? 'success' : 'failed',
      contractAddress: receipt.contractAddress,
      logs: receipt.logs.map((log) => ({
        address: log.address,
        topics: log.topics as string[],
        data: log.data,
      })),
    };
  }
}
