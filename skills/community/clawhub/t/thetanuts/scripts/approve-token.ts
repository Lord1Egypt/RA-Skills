#!/usr/bin/env npx tsx
/**
 * Approve ERC20 token spending for a spender contract.
 *
 * Seed is read from WDK_SEED env var (or --seed-file <path>) — never from argv.
 *
 * Usage:
 *   WDK_SEED="..." npx tsx approve-token.ts \
 *     --token <address> --spender <address> --amount <number> [--wait]
 *
 * For unlimited approvals, pass --max --confirm-max. The spender must be in the
 * Thetanuts allowlist unless --i-understand-risk is set.
 */

import WalletManagerEvm from '@tetherto/wdk-wallet-evm';
import { loadSeed } from './lib/load-seed';

const EVM_RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';

// Token addresses lower-cased to make lookups case-insensitive. Casing on
// Ethereum addresses is purely a checksum hint, not part of the identifier,
// so a case-sensitive lookup that silently falls back to 18 decimals would
// approve 10^12 × the intended amount for USDC (6 decimals).
const KNOWN_TOKENS: Record<string, { symbol: string; decimals: number }> = {
  '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913': { symbol: 'USDC', decimals: 6 },
  '0x4200000000000000000000000000000000000006': { symbol: 'WETH', decimals: 18 },
  '0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf': { symbol: 'cbBTC', decimals: 8 },
};

// Allowlist of vetted Thetanuts spender contracts. Spenders outside this list
// require --i-understand-risk to prevent the agent from being tricked into
// approving a hostile contract. Keys are lower-cased.
const KNOWN_SPENDERS: Record<string, string> = {
  '0x1adcd391cf15fb699ed29b1d394f4a64106886e5': 'Thetanuts RFQ Contract',
};

function lookupToken(addr: string): { symbol: string; decimals: number } | undefined {
  return KNOWN_TOKENS[addr.toLowerCase()];
}

function lookupSpender(addr: string): string | undefined {
  return KNOWN_SPENDERS[addr.toLowerCase()];
}

// Max uint256 for unlimited approval
const MAX_UINT256 = BigInt('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff');

interface ApproveTokenParams {
  token: string;
  spender: string;
  amount?: string;
  max: boolean;
  confirmMax: boolean;
  overrideAllowlist: boolean;
  decimals?: number;
  index: number;
  wait: boolean;
}

function parseArgs(args: string[]): ApproveTokenParams {
  const params: Partial<ApproveTokenParams> = {
    index: 0,
    max: false,
    confirmMax: false,
    overrideAllowlist: false,
    wait: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--token':
        params.token = args[++i];
        break;
      case '--spender':
        params.spender = args[++i];
        break;
      case '--amount':
        params.amount = args[++i];
        break;
      case '--max':
        params.max = true;
        break;
      case '--confirm-max':
        params.confirmMax = true;
        break;
      case '--i-understand-risk':
        params.overrideAllowlist = true;
        break;
      case '--decimals':
        params.decimals = parseInt(args[++i], 10);
        break;
      case '--index':
        params.index = parseInt(args[++i]) || 0;
        break;
      case '--wait':
        params.wait = true;
        break;
    }
  }

  const missing: string[] = [];
  if (!params.token) missing.push('--token <address>');
  if (!params.spender) missing.push('--spender <address>');
  if (!params.max && !params.amount) missing.push('--amount <number> or --max --confirm-max');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameters',
      missing,
      usage: 'WDK_SEED="..." npx tsx approve-token.ts --token <address> --spender <address> (--amount <number> | --max --confirm-max) [--wait]',
      example: 'WDK_SEED="word1 word2 ... word12" npx tsx approve-token.ts --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --spender 0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5 --amount 100 --wait',
      commonTokens: {
        USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        WETH: '0x4200000000000000000000000000000000000006',
        cbBTC: '0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf',
      },
      commonSpenders: {
        'Thetanuts RFQ': '0x1aDcD391CF15Fb699Ed29B1D394F4A64106886e5',
      },
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  if (!params.token!.match(/^0x[a-fA-F0-9]{40}$/)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Invalid token address format. Must be 0x followed by 40 hex characters.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  if (!params.spender!.match(/^0x[a-fA-F0-9]{40}$/)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Invalid spender address format. Must be 0x followed by 40 hex characters.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  // Block unlimited approvals unless explicitly confirmed.
  if (params.max && !params.confirmMax) {
    console.error(JSON.stringify({
      error: true,
      message: 'Unlimited (--max) approvals require --confirm-max to prevent accidental wallet drain risk. Prefer --amount <exact>.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  // Block spenders outside the Thetanuts allowlist unless overridden.
  if (!lookupSpender(params.spender!) && !params.overrideAllowlist) {
    console.error(JSON.stringify({
      error: true,
      message: 'Spender is not in the Thetanuts allowlist. Refusing to approve. Re-run with --i-understand-risk only if you have independently verified this contract address.',
      spender: params.spender,
      allowlist: KNOWN_SPENDERS,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  // Require explicit --decimals for tokens we don't have a metadata entry for,
  // so we never silently fall back to 18-decimal math on a 6-decimal token.
  if (!lookupToken(params.token!) && params.decimals === undefined) {
    console.error(JSON.stringify({
      error: true,
      message: 'Unknown token address. Pass --decimals <n> with the token\'s decimals so the approval amount is computed correctly. Common values: USDC=6, WETH=18, cbBTC=8.',
      token: params.token,
      knownTokens: KNOWN_TOKENS,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  if (params.decimals !== undefined && (!Number.isInteger(params.decimals) || params.decimals < 0 || params.decimals > 36)) {
    console.error(JSON.stringify({
      error: true,
      message: '--decimals must be an integer between 0 and 36.',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }

  return {
    token: params.token!,
    spender: params.spender!,
    amount: params.amount,
    max: params.max!,
    confirmMax: params.confirmMax!,
    overrideAllowlist: params.overrideAllowlist!,
    decimals: params.decimals,
    index: params.index!,
    wait: params.wait!,
  };
}

function formatAmount(amount: bigint, decimals: number): string {
  const divisor = BigInt(10 ** decimals);
  const integerPart = amount / divisor;
  const fractionalPart = amount % divisor;

  if (amount === MAX_UINT256) {
    return 'UNLIMITED';
  }

  const fractionalStr = fractionalPart.toString().padStart(decimals, '0');
  let trimmed = fractionalStr.replace(/0+$/, '');
  if (trimmed.length < 2) trimmed = fractionalStr.slice(0, 2);

  return `${integerPart}.${trimmed}`;
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

    // Resolve token metadata. If --decimals is supplied, it overrides the
    // known-tokens table (and is the only allowed source for unknown tokens —
    // parseArgs already rejected the unknown-and-no-decimals combination).
    const knownToken = lookupToken(params.token);
    const tokenInfo = knownToken
      ? { symbol: knownToken.symbol, decimals: params.decimals ?? knownToken.decimals }
      : { symbol: 'UNKNOWN', decimals: params.decimals! };
    const spenderName = lookupSpender(params.spender) || params.spender;

    let approvalAmount: bigint;
    if (params.max) {
      approvalAmount = MAX_UINT256;
    } else {
      const amountFloat = parseFloat(params.amount!);
      if (!Number.isFinite(amountFloat) || amountFloat < 0) {
        console.error(JSON.stringify({
          error: true,
          message: '--amount must be a non-negative number.',
          timestamp: new Date().toISOString(),
        }, null, 2));
        wallet.dispose?.();
        process.exit(1);
      }
      approvalAmount = BigInt(Math.floor(amountFloat * (10 ** tokenInfo.decimals)));
    }

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

    // Human-readable pre-broadcast preview — surfaced to stderr so the agent
    // (and any user watching the terminal) sees exactly what's being signed.
    console.error(JSON.stringify({
      preview: 'About to broadcast ERC-20 approval',
      from: address,
      token: { address: params.token, symbol: tokenInfo.symbol, decimals: tokenInfo.decimals },
      spender: { address: params.spender, name: spenderName, allowlisted: !!lookupSpender(params.spender) },
      allowance: { human: formatAmount(approvalAmount, tokenInfo.decimals), raw: approvalAmount.toString() },
    }));

    // Call WDK approve method
    const txResult = await account.approve({
      token: params.token,
      spender: params.spender,
      amount: approvalAmount,
    });

    const result: any = {
      approval: {
        hash: txResult.hash,
        token: params.token,
        tokenSymbol: tokenInfo.symbol,
        spender: params.spender,
        spenderName: spenderName,
        amount: approvalAmount.toString(),
        amountFormatted: formatAmount(approvalAmount, tokenInfo.decimals),
        from: address,
      },
      warning: `You are approving ${spenderName} to spend your ${tokenInfo.symbol}. Only approve contracts you trust. This approval can be revoked by approving 0.`,
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

      let receipt = null;
      const startTime = Date.now();
      const timeout = 60000;

      while (!receipt && (Date.now() - startTime) < timeout) {
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

        if (receipt.status === 1) {
          result.success = true;
          console.error('Approval confirmed!');
        } else {
          result.success = false;
          result.warning = 'Approval transaction REVERTED. Check BaseScan for details.';
        }
      } else {
        result.pending = true;
        result.warning = `Approval broadcast but not confirmed within 60s. Check BaseScan: https://basescan.org/tx/${txResult.hash}`;
      }
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    let errorMessage = error instanceof Error ? error.message : 'Unknown error';

    if (errorMessage.includes('insufficient funds')) {
      errorMessage = 'Insufficient ETH for gas. Fund your wallet with ETH on Base network.';
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
