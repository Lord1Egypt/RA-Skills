#!/usr/bin/env npx tsx
/**
 * Sign and broadcast an EVM transaction.
 * Seed is read from WDK_SEED env var (or --seed-file) — never from argv.
 *
 * Usage: WDK_SEED="..." npx tsx send-transaction.ts --to <address> --data <hex> [--value <wei>] [--wait]
 */

import WalletManagerEvm from '@tetherto/wdk-wallet-evm';
import { loadSeed } from './lib/load-seed';

const EVM_RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';

interface SendTransactionParams {
  to: string;
  data: string;
  value: string;
  index: number;
  gasLimit?: number;
  gasPrice?: bigint;
  wait: boolean;
  timeout: number;
}

function parseArgs(args: string[]): SendTransactionParams {
  const params: Partial<SendTransactionParams> = {
    value: '0',
    index: 0,
    wait: false,
    timeout: 60000,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--to':
        params.to = args[++i];
        break;
      case '--data':
        params.data = args[++i];
        break;
      case '--value':
        params.value = args[++i];
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
      case '--gas-limit':
        params.gasLimit = parseInt(args[++i]);
        break;
      case '--gas-price':
        const gweiValue = parseFloat(args[++i]);
        params.gasPrice = BigInt(Math.floor(gweiValue * 1e9));
        break;
      case '--wait':
        params.wait = true;
        break;
      case '--timeout':
        params.timeout = parseInt(args[++i]) || 60000;
        break;
    }
  }

  const missing: string[] = [];
  if (!params.to) missing.push('--to <address>');
  if (!params.data) missing.push('--data <hex>');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameters',
      missing,
      usage: 'WDK_SEED="..." npx tsx send-transaction.ts --to <address> --data <hex> [--value <wei>] [--gas-limit <number>] [--gas-price <gwei>] [--wait] [--timeout <ms>]',
      example: 'WDK_SEED="word1 word2 ... word12" npx tsx send-transaction.ts --to 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --data 0xb5da63e3... --wait',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  if (!params.to!.match(/^0x[a-fA-F0-9]{40}$/)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Invalid address format for --to parameter. Must be 0x followed by 40 hex characters.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  if (!params.data!.match(/^0x[a-fA-F0-9]*$/)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Invalid data format. Must be hex string starting with 0x.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  return {
    to: params.to!,
    data: params.data!,
    value: params.value!,
    index: params.index!,
    gasLimit: params.gasLimit,
    gasPrice: params.gasPrice,
    wait: params.wait!,
    timeout: params.timeout!,
  };
}

async function main() {
  const args = process.argv.slice(2);
  const { seed } = loadSeed(args);
  const params = parseArgs(args);

  const wallet = new WalletManagerEvm(seed, {
    provider: EVM_RPC_URL,
  });

  try {
    const account = await wallet.getAccount(params.index);
    const address = await account.getAddress();

    // Pre-check: ensure wallet has ETH for gas
    const ethBalance = await account.getBalance();
    if (ethBalance === 0n) {
      console.log(JSON.stringify({
        error: true,
        message: 'Wallet has 0 ETH on Base. You need ETH for gas fees. Bridge ETH to Base via bridge.base.org.',
        address,
        timestamp: new Date().toISOString(),
      }, null, 2));
      wallet.dispose?.();
      process.exit(1);
    }

    console.error('Signing and broadcasting transaction...');

    // Build transaction object
    const tx: {
      to: string;
      value: bigint;
      data: string;
      gasLimit?: bigint;
      gasPrice?: bigint;
    } = {
      to: params.to,
      value: BigInt(params.value),
      data: params.data,
    };

    // Add optional gas parameters
    if (params.gasLimit) {
      tx.gasLimit = BigInt(params.gasLimit);
    }
    if (params.gasPrice) {
      tx.gasPrice = params.gasPrice;
    }

    // Send transaction using WDK
    const txResult = await account.sendTransaction(tx);

    const result: any = {
      transaction: {
        hash: txResult.hash,
        from: address,
        to: params.to,
        value: params.value,
        data: params.data.length > 66 ? params.data.slice(0, 66) + '...' : params.data,
      },
      warning: 'This transaction is IRREVERSIBLE. Once broadcast, it cannot be cancelled or reversed. Ensure the destination and amount are correct.',
      network: {
        name: 'Base Mainnet',
        chainId: 8453,
        rpcUrl: EVM_RPC_URL,
      },
      timestamp: new Date().toISOString(),
    };

    // Wait for confirmation if requested
    if (params.wait) {
      console.error('Waiting for confirmation...');

      const startTime = Date.now();
      let receipt = null;

      while (!receipt && (Date.now() - startTime) < params.timeout) {
        receipt = await account.getTransactionReceipt(txResult.hash);
        if (!receipt) {
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      }

      if (receipt) {
        result.receipt = {
          status: receipt.status,
          blockNumber: receipt.blockNumber,
          gasUsed: receipt.gasUsed?.toString(),
          transactionIndex: receipt.index,
        };

        if (receipt.status === 0) {
          result.warning = 'Transaction REVERTED. The operation failed on-chain. Check the transaction on BaseScan for details.';
        }
      } else {
        result.pending = true;
        result.warning = `Transaction broadcast but not confirmed within ${params.timeout}ms. Check BaseScan: https://basescan.org/tx/${txResult.hash}`;
      }
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    // Parse common error messages
    let errorMessage = error instanceof Error ? error.message : 'Unknown error';

    if (errorMessage.includes('insufficient funds')) {
      errorMessage = 'Insufficient ETH for gas. Fund your wallet with ETH on Base network.';
    } else if (errorMessage.includes('transfer amount exceeds allowance')) {
      errorMessage = 'Insufficient token allowance. Run approve-token.ts first to approve token spending.';
    } else if (errorMessage.includes('transfer amount exceeds balance')) {
      errorMessage = 'Insufficient token balance. Check your balance with get-balance.ts.';
    } else if (errorMessage.includes('nonce')) {
      errorMessage = 'Nonce error. A previous transaction may be pending. Wait and try again.';
    }

    console.error(JSON.stringify({
      error: true,
      message: errorMessage,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  } finally {
    wallet.dispose?.();
  }
}

main();
