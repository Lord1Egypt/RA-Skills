import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';
import { QFCKeystore, type WalletMeta } from './keystore.js';
import type { BatchTransferItem, BatchTransferResult } from './token.js';

interface WalletCreationResult {
  address: string;
  mnemonic: string;
  privateKey: string;
}

interface BalanceResult {
  qfc: string;
  wei: string;
}

interface SendResult {
  txHash: string;
  explorerUrl: string;
}

/**
 * QFC Wallet — manages wallet operations on the QFC blockchain.
 */
export class QFCWallet {
  private provider: ethers.JsonRpcProvider;
  private wallet: ethers.Wallet | null = null;
  private network: NetworkName;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.network = network;
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  /** Create a new random wallet */
  createWallet(): WalletCreationResult {
    const hdWallet = ethers.Wallet.createRandom();
    this.wallet = new ethers.Wallet(hdWallet.privateKey, this.provider);
    return {
      address: hdWallet.address,
      mnemonic: hdWallet.mnemonic!.phrase,
      privateKey: hdWallet.privateKey,
    };
  }

  /** Import an existing wallet from private key */
  importWallet(privateKey: string): string {
    this.wallet = new ethers.Wallet(privateKey, this.provider);
    return this.wallet.address;
  }

  /** Get balance for an address (defaults to current wallet) */
  async getBalance(address?: string): Promise<BalanceResult> {
    const target = address ?? this.requireWallet().address;
    const balance = await this.provider.getBalance(target);
    return {
      qfc: ethers.formatEther(balance),
      wei: balance.toString(),
    };
  }

  /** Send QFC to an address */
  async sendQFC(
    to: string,
    amount: string,
    opts?: { gasLimit?: number },
  ): Promise<SendResult> {
    if (!ethers.isAddress(to)) {
      throw new Error('Invalid address format. Expected 0x + 40 hex characters.');
    }
    const wallet = this.requireWallet();
    const tx = await wallet.sendTransaction({
      to,
      value: ethers.parseEther(amount),
      gasLimit: opts?.gasLimit,
    });
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`Transaction reverted (tx: ${tx.hash})`);
    }
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /** Sign a message with the current wallet */
  async signMessage(message: string): Promise<string> {
    const wallet = this.requireWallet();
    return wallet.signMessage(message);
  }

  /** Get the current wallet address */
  get address(): string | null {
    return this.wallet?.address ?? null;
  }

  /** Save current wallet to encrypted keystore on disk */
  async save(password: string, name?: string): Promise<void> {
    const wallet = this.requireWallet();
    const ks = new QFCKeystore();
    await ks.saveWallet(wallet, password, { name, network: this.network });
  }

  /** Load a wallet from encrypted keystore */
  static async load(
    address: string,
    password: string,
    network: NetworkName = 'testnet',
  ): Promise<QFCWallet> {
    const ks = new QFCKeystore();
    const raw = await ks.loadWallet(address, password);
    const instance = new QFCWallet(network);
    instance.importWallet(raw.privateKey);
    return instance;
  }

  /** List all saved wallets (no password needed) */
  static listSaved(): WalletMeta[] {
    const ks = new QFCKeystore();
    return ks.listWallets();
  }

  /** Poll for transaction receipt via raw RPC (avoids ethers.js log-parsing issues on QFC) */
  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; blockNumber: string }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return raw;
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  /**
   * Batch send native QFC to multiple addresses sequentially.
   * @param recipients - array of {to, amount} objects (amount in QFC, e.g. "10")
   * @param signer - wallet to sign the transactions
   */
  async batchSend(
    recipients: BatchTransferItem[],
    signer: ethers.Wallet,
  ): Promise<BatchTransferResult> {
    const connected = signer.connect(this.provider);
    const result: BatchTransferResult = { successful: [], failed: [] };

    for (const recipient of recipients) {
      try {
        if (!ethers.isAddress(recipient.to)) {
          result.failed.push({ to: recipient.to, amount: recipient.amount, error: 'Invalid address format' });
          continue;
        }
        const tx = await connected.sendTransaction({
          to: recipient.to,
          value: ethers.parseEther(recipient.amount),
        });
        const receipt = await this.waitForReceipt(tx.hash);
        if (receipt.status !== '0x1') {
          result.failed.push({ to: recipient.to, amount: recipient.amount, error: 'Transaction reverted' });
        } else {
          result.successful.push({ to: recipient.to, amount: recipient.amount, txHash: tx.hash });
        }
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        result.failed.push({ to: recipient.to, amount: recipient.amount, error: message });
      }
    }

    return result;
  }

  private requireWallet(): ethers.Wallet {
    if (!this.wallet) {
      throw new Error('No wallet loaded. Call createWallet() or importWallet() first.');
    }
    return this.wallet;
  }
}
