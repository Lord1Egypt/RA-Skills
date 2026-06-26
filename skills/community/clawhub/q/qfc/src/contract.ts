import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

export interface CallResult {
  result: any;
  decoded: any[];
}

export interface SendResult {
  txHash: string;
  explorerUrl: string;
  gasUsed: number;
  logs: { address: string; topics: string[]; data: string }[];
}

export interface DeployResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
}

export interface VerifyResult {
  address: string;
  verified: boolean;
  contractName: string;
  compiler: string;
  evmVersion: string;
}

/**
 * QFCContract — read, write, and deploy smart contracts on QFC.
 */
export class QFCContract {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  /** Poll for transaction receipt via raw RPC (avoids ethers.js log-parsing issues on QFC) */
  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; hash: string; blockNumber: string; gasUsed: string; logs: Array<{ address: string; topics: string[]; data: string }> }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return { ...raw, hash: txHash };
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  /**
   * Read contract state (no gas, no signer needed).
   * @param address - contract address
   * @param abi - ABI array or JSON string
   * @param method - method name
   * @param args - method arguments
   */
  async call(
    address: string,
    abi: ethers.InterfaceAbi,
    method: string,
    args: any[] = [],
  ): Promise<CallResult> {
    const contract = new ethers.Contract(address, abi, this.provider);
    const result = await contract[method](...args);
    const iface = new ethers.Interface(abi);
    const fragment = iface.getFunction(method);
    let decoded: any[];
    if (fragment && fragment.outputs && fragment.outputs.length > 1) {
      decoded = Array.isArray(result) ? [...result] : [result];
    } else {
      decoded = [result];
    }
    return { result, decoded };
  }

  /**
   * Write to a contract (requires signer, costs gas).
   * @param address - contract address
   * @param abi - ABI array or JSON string
   * @param method - method name
   * @param args - method arguments
   * @param signer - wallet to sign the transaction
   * @param value - optional QFC value to send (in ether units, e.g. "1.5")
   */
  async send(
    address: string,
    abi: ethers.InterfaceAbi,
    method: string,
    args: any[],
    signer: ethers.Wallet,
    value?: string,
  ): Promise<SendResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(address, abi, connected);
    const overrides: ethers.Overrides = {};
    if (value) {
      overrides.value = ethers.parseEther(value);
    }
    const tx = await contract[method](...args, overrides);
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`Transaction reverted (tx: ${tx.hash})`);
    }
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
      gasUsed: Number(receipt.gasUsed),
      logs: (receipt.logs ?? []).map((log: { address: string; topics: string[]; data: string }) => ({
        address: log.address,
        topics: log.topics as string[],
        data: log.data,
      })),
    };
  }

  /**
   * Deploy a new contract.
   * @param abi - contract ABI
   * @param bytecode - compiled bytecode (hex string)
   * @param args - constructor arguments
   * @param signer - wallet to deploy from
   */
  async deploy(
    abi: ethers.InterfaceAbi,
    bytecode: string,
    args: any[],
    signer: ethers.Wallet,
  ): Promise<DeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(abi, bytecode, connected);
    const contract = await factory.deploy(...args);
    const receipt = await contract.deploymentTransaction()!.wait();
    const address = await contract.getAddress();
    return {
      contractAddress: address,
      txHash: receipt!.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${receipt!.hash}`,
    };
  }

  /**
   * Check if an address has contract code deployed.
   * @param address - address to check
   * @returns true if contract code exists
   */
  async isContract(address: string): Promise<boolean> {
    const code = await this.provider.getCode(address);
    return code !== '0x';
  }

  /**
   * Get the raw bytecode at an address.
   * @param address - contract address
   * @returns hex-encoded bytecode or "0x" if no contract
   */
  async getCode(address: string): Promise<string> {
    return this.provider.getCode(address);
  }

  /**
   * Submit contract source code for verification on the QFC explorer.
   * The explorer compiles the source, strips metadata, and compares against deployed bytecode.
   *
   * @param address - contract address to verify
   * @param sourceCode - Solidity source code
   * @param compilerVersion - e.g. "v0.8.28"
   * @param evmVersion - e.g. "paris" (required for QFC, no PUSH0)
   * @param optimizationRuns - optimizer runs (e.g. 200), omit for no optimization
   * @param constructorArgs - ABI-encoded constructor arguments (hex), optional
   */
  async verify(
    address: string,
    sourceCode: string,
    compilerVersion: string = 'v0.8.28',
    evmVersion: string = 'paris',
    optimizationRuns?: number,
    constructorArgs?: string,
  ): Promise<VerifyResult> {
    const explorerUrl = this.networkConfig.explorerUrl;
    const response = await fetch(`${explorerUrl}/api/contracts/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address,
        sourceCode,
        compilerVersion,
        evmVersion,
        optimizationRuns,
        constructorArgs,
      }),
    });

    const data = await response.json();

    if (!data.ok) {
      throw new Error(data.error || 'Verification failed');
    }

    return {
      address: data.data.address,
      verified: data.data.verified,
      contractName: data.data.contractName,
      compiler: data.data.compiler,
      evmVersion: data.data.evmVersion,
    };
  }
}
