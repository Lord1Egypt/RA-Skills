import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

const MULTICALL_ABI = [
  'function aggregate3((address target, bool allowFailure, bytes callData)[] calls) view returns ((bool success, bytes returnData)[])',
];

/**
 * Pre-compiled Multicall3 bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * No constructor args.
 */
const MULTICALL_DEPLOY_BYTECODE = '0x6080604052348015600f57600080fd5b506104a68061001f6000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c806382ad56cb14610030575b600080fd5b61004361003e366004610248565b610059565b60405161005091906102bf565b60405180910390f35b60608167ffffffffffffffff81111561007457610074610374565b6040519080825280602002602001820160405280156100ba57816020015b6040805180820190915260008152606060208201528152602001906001900390816100925790505b50905060005b82811015610241576000808585848181106100dd576100dd61038a565b90506020028101906100ef91906103a0565b6100fd9060208101906103c0565b6001600160a01b03168686858181106101185761011861038a565b905060200281019061012a91906103a0565b6101389060408101906103f0565b60405161014692919061043e565b600060405180830381855afa9150503d8060008114610181576040519150601f19603f3d011682016040523d82523d6000602084013e610186565b606091505b509150915085858481811061019d5761019d61038a565b90506020028101906101af91906103a0565b6101c090604081019060200161044e565b61020357816102035760405162461bcd60e51b815260206004820152600b60248201526a18d85b1b0819985a5b195960aa1b604482015260640160405180910390fd5b604051806040016040528083151581526020018281525084848151811061022c5761022c61038a565b602090810291909101015250506001016100c0565b5092915050565b6000806020838503121561025b57600080fd5b823567ffffffffffffffff81111561027257600080fd5b8301601f8101851361028357600080fd5b803567ffffffffffffffff81111561029a57600080fd5b8560208260051b84010111156102af57600080fd5b6020919091019590945092505050565b6000602082016020835280845180835260408501915060408160051b86010192506020860160005b8281101561036857603f1987860301845281518051151586526020810151905060406020870152805180604088015260005b8181101561033657602081840181015160608a8401015201610319565b506000606082890101526060601f19601f830116880101965050506020820191506020840193506001810190506102e7565b50929695505050505050565b634e487b7160e01b600052604160045260246000fd5b634e487b7160e01b600052603260045260246000fd5b60008235605e198336030181126103b657600080fd5b9190910192915050565b6000602082840312156103d257600080fd5b81356001600160a01b03811681146103e957600080fd5b9392505050565b6000808335601e1984360301811261040757600080fd5b83018035915067ffffffffffffffff82111561042257600080fd5b60200191503681900382131561043757600080fd5b9250929050565b8183823760009101908152919050565b60006020828403121561046057600080fd5b813580151581146103e957600080fdfea26469706673582212201cbdc583641adb0a9c4eb1a4fdfd090fe7d1e4bd03289f0139650b1c692fdb8d64736f6c63430008220033';

/**
 * Solidity source code for Multicall3.
 */
export const MULTICALL_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Multicall3 {
    struct Call3 {
        address target;
        bool allowFailure;
        bytes callData;
    }

    struct Result {
        bool success;
        bytes returnData;
    }

    function aggregate3(Call3[] calldata calls) external view returns (Result[] memory results) {
        results = new Result[](calls.length);
        for (uint256 i = 0; i < calls.length; i++) {
            (bool success, bytes memory ret) = calls[i].target.staticcall(calls[i].callData);
            if (!calls[i].allowFailure) {
                require(success, "call failed");
            }
            results[i] = Result(success, ret);
        }
    }
}
`;

export interface MulticallCall {
  target: string;
  allowFailure?: boolean;
  callData: string;
}

export interface MulticallResult {
  success: boolean;
  returnData: string;
}

export interface MulticallDeployResult {
  multicallAddress: string;
  txHash: string;
  explorerUrl: string;
}

/**
 * QFCMulticall — Batch multiple view/read calls into a single RPC request.
 */
export class QFCMulticall {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; contractAddress: string }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return raw;
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  /**
   * Deploy a Multicall3 contract.
   */
  async deploy(signer: ethers.Wallet): Promise<MulticallDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(MULTICALL_ABI, MULTICALL_DEPLOY_BYTECODE, connected);
    const deployTx = await factory.getDeployTransaction();
    deployTx.gasLimit = 800_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Multicall3 deployment reverted (tx: ${tx.hash})`);
    }

    // Best-effort verification
    try {
      const verifyUrl = `${this.networkConfig.explorerUrl}/api/contracts/verify`;
      await fetch(verifyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: receipt.contractAddress,
          sourceCode: MULTICALL_SOURCE_CODE,
          compilerVersion: 'v0.8.34+commit.1c8745a5',
          evmVersion: 'paris',
          optimizationRuns: 200,
        }),
      });
    } catch {
      // Explorer unavailable
    }

    return {
      multicallAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`,
    };
  }

  /**
   * Execute batch calls via a deployed Multicall3 contract.
   * @param multicallAddress - deployed Multicall3 contract
   * @param calls - array of {target, allowFailure?, callData}
   */
  async call(multicallAddress: string, calls: MulticallCall[]): Promise<MulticallResult[]> {
    const mc = new ethers.Contract(multicallAddress, MULTICALL_ABI, this.provider);
    const formatted = calls.map((c) => ({
      target: c.target,
      allowFailure: c.allowFailure ?? true,
      callData: c.callData,
    }));

    const results = await mc.aggregate3(formatted);
    return results.map((r: { success: boolean; returnData: string }) => ({
      success: r.success,
      returnData: r.returnData,
    }));
  }

  /**
   * Batch query ERC-20 balanceOf for multiple tokens.
   * @param multicallAddress - deployed Multicall3 contract
   * @param tokens - array of token addresses
   * @param owner - wallet address to check
   * @returns array of {token, balance} where balance is raw (not formatted)
   */
  async getTokenBalances(
    multicallAddress: string,
    tokens: string[],
    owner: string,
  ): Promise<{ token: string; balance: string }[]> {
    const iface = new ethers.Interface(['function balanceOf(address) view returns (uint256)']);
    const calls = tokens.map((token) => ({
      target: token,
      allowFailure: true,
      callData: iface.encodeFunctionData('balanceOf', [owner]),
    }));

    const results = await this.call(multicallAddress, calls);
    return results.map((r, i) => ({
      token: tokens[i],
      balance: r.success ? BigInt(r.returnData).toString() : '0',
    }));
  }

  /**
   * Batch query pool reserves for multiple AMM pools.
   * @param multicallAddress - deployed Multicall3 contract
   * @param pools - array of pool addresses
   */
  async getPoolReserves(
    multicallAddress: string,
    pools: string[],
  ): Promise<{ pool: string; reserveA: string; reserveB: string }[]> {
    const iface = new ethers.Interface(['function getReserves() view returns (uint256, uint256)']);
    const calls = pools.map((pool) => ({
      target: pool,
      allowFailure: true,
      callData: iface.encodeFunctionData('getReserves'),
    }));

    const results = await this.call(multicallAddress, calls);
    return results.map((r, i) => {
      if (r.success && r.returnData !== '0x') {
        const decoded = iface.decodeFunctionResult('getReserves', r.returnData);
        return { pool: pools[i], reserveA: decoded[0].toString(), reserveB: decoded[1].toString() };
      }
      return { pool: pools[i], reserveA: '0', reserveB: '0' };
    });
  }
}
