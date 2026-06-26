/**
 * Privy Signer for OpenClaw Agents
 * Enables signing transactions and messages using Privy server wallets
 */

import { ethers } from 'ethers';

export interface PrivySignerOptions {
  walletId: string;
  appId: string;
  appSecret: string;
  chainId: number;
  rpcUrl: string;
}

/**
 * Privy-based signer that implements ethers.Signer interface
 * Uses Privy API to sign transactions and messages
 */
export class PrivySigner extends ethers.AbstractSigner {
  private walletId: string;
  private appId: string;
  private appSecret: string;
  private chainId: number;
  private rpcUrl: string;
  private _address?: string;

  constructor(options: PrivySignerOptions) {
    super();
    this.walletId = options.walletId;
    this.appId = options.appId;
    this.appSecret = options.appSecret;
    this.chainId = options.chainId;
    this.rpcUrl = options.rpcUrl;
  }

  async getAddress(): Promise<string> {
    if (!this._address) {
      const wallet = await this.getWallet() as { address: string };
      this._address = wallet.address;
    }
    return this._address!;
  }

  async signTransaction(tx: ethers.TransactionRequest): Promise<string> {
    // Use Privy API to sign transaction
    const response = await fetch(`https://auth.privy.io/api/v1/wallets/${this.walletId}/sign_transaction`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${Buffer.from(`${this.appId}:${this.appSecret}`).toString('base64')}`
      },
      body: JSON.stringify({
        chain_id: this.chainId,
        transaction: {
          to: tx.to,
          value: tx.value?.toString(),
          data: tx.data,
          gas: tx.gasLimit?.toString(),
          gasPrice: tx.gasPrice?.toString(),
          nonce: tx.nonce?.toString()
        }
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText })) as { message?: string };
      throw new Error(`Privy signing failed: ${error.message || response.statusText}`);
    }

    const result = await response.json() as { signed_transaction: string };
    return result.signed_transaction;
  }

  async signMessage(message: string | Uint8Array): Promise<string> {
    const messageHash = typeof message === 'string' 
      ? ethers.keccak256(ethers.toUtf8Bytes(message))
      : ethers.keccak256(message);

    // Use Privy API to sign message (EIP-191)
    const response = await fetch(`https://auth.privy.io/api/v1/wallets/${this.walletId}/sign_message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${Buffer.from(`${this.appId}:${this.appSecret}`).toString('base64')}`
      },
      body: JSON.stringify({
        message: typeof message === 'string' ? message : ethers.hexlify(message),
        message_hash: messageHash
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText })) as { message?: string };
      throw new Error(`Privy message signing failed: ${error.message || response.statusText}`);
    }

    const result = await response.json() as { signature: string };
    return result.signature;
  }

  async signTypedData(domain: any, types: any, value: any): Promise<string> {
    // EIP-712 signing via Privy
    const response = await fetch(`https://auth.privy.io/api/v1/wallets/${this.walletId}/sign_typed_data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${Buffer.from(`${this.appId}:${this.appSecret}`).toString('base64')}`
      },
      body: JSON.stringify({
        domain,
        types,
        message: value
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText })) as { message?: string };
      throw new Error(`Privy typed data signing failed: ${error.message || response.statusText}`);
    }

    const result = await response.json() as { signature: string };
    return result.signature;
  }

  connect(provider: ethers.Provider | null): ethers.Signer {
    // Return new instance with provider
    return new PrivySigner({
      walletId: this.walletId,
      appId: this.appId,
      appSecret: this.appSecret,
      chainId: this.chainId,
      rpcUrl: this.rpcUrl
    });
  }

  private async getWallet() {
    const response = await fetch(`https://auth.privy.io/api/v1/wallets/${this.walletId}`, {
      headers: {
        'Authorization': `Basic ${Buffer.from(`${this.appId}:${this.appSecret}`).toString('base64')}`
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to get Privy wallet: ${response.statusText}`);
    }

    return response.json();
  }
}
