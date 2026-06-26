import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig, rpcCall } from './provider.js';

export interface FaucetResult {
  txHash: string;
  amount: string;
  to: string;
  explorerUrl: string;
}

/**
 * QFCFaucet — request test tokens on QFC testnet.
 */
export class QFCFaucet {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    if (network !== 'testnet') {
      throw new Error('Faucet is only available on testnet (chain_id=9000)');
    }
    this.provider = createProvider(network);
    this.networkConfig = getNetworkConfig(network);
  }

  /**
   * Request test QFC tokens.
   * @param address - recipient address
   * @param amount - amount in QFC (not wei), defaults to "10"
   */
  async requestQFC(address: string, amount: string = '10'): Promise<FaucetResult> {
    if (!ethers.isAddress(address)) {
      throw new Error('Invalid address format. Expected 0x + 40 hex characters.');
    }
    const parsed = parseFloat(amount);
    if (isNaN(parsed) || parsed <= 0) {
      throw new Error('Amount must be a positive number.');
    }

    let result: any;
    try {
      const amountInWei = ethers.parseEther(amount).toString();
      result = await rpcCall(this.provider, 'qfc_requestFaucet', [address, amountInWei]);
    } catch (err: any) {
      throw new Error(`Faucet request failed: ${err.message ?? err}`);
    }

    const txHash = typeof result === 'string' ? result : result.txHash;
    return {
      txHash,
      amount,
      to: address,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${txHash}`,
    };
  }
}
