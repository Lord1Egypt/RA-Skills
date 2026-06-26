#!/usr/bin/env node
/**
 * WALVIS wallet-setup script
 * Sui wallet initialization helper for testnet/mainnet
 *
 * Usage:
 *   wallet-setup generate           - generate new keypair
 *   wallet-setup info               - show wallet info from manifest
 *   wallet-setup balance            - check SUI balance
 *   wallet-setup faucet             - request testnet faucet
 */

import { readManifest, writeManifest } from './storage.js';

const TESTNET_FAUCET = 'https://faucet.testnet.sui.io/gas';
const TESTNET_RPC = 'https://fullnode.testnet.sui.io:443';
const MAINNET_RPC = 'https://fullnode.mainnet.sui.io:443';

function getRpcUrl(network: string): string {
  return network === 'mainnet' ? MAINNET_RPC : TESTNET_RPC;
}

export async function getBalance(address: string, network: string): Promise<string> {
  const rpc = getRpcUrl(network);
  const res = await fetch(rpc, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'suix_getBalance',
      params: [address, '0x2::sui::SUI'],
    }),
  });

  const data = await res.json() as {
    result?: { totalBalance: string };
    error?: { message: string };
  };

  if (data.error) throw new Error(data.error.message);
  const mist = BigInt(data.result?.totalBalance ?? '0');
  const sui = Number(mist) / 1_000_000_000;
  return `${sui.toFixed(4)} SUI`;
}

export async function requestFaucet(address: string): Promise<void> {
  const res = await fetch(TESTNET_FAUCET, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ FixedAmountRequest: { recipient: address } }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Faucet request failed: ${res.status} ${text}`);
  }
  console.log('✓ Faucet request submitted. Funds should arrive shortly.');
}

// CLI entry point
const [,, cmd] = process.argv;

if (cmd === 'info') {
  try {
    const manifest = readManifest();
    console.log(`Address:  ${manifest.suiAddress ?? 'not set'}`);
    console.log(`Network:  ${manifest.network}`);
    console.log(`Agent:    ${manifest.agent}`);
  } catch (err) {
    console.error((err as Error).message);
    process.exit(1);
  }
} else if (cmd === 'balance') {
  try {
    const manifest = readManifest();
    if (!manifest.suiAddress) { console.error('No wallet address configured.'); process.exit(1); }
    const balance = await getBalance(manifest.suiAddress, manifest.network);
    console.log(`Balance: ${balance}`);
  } catch (err) {
    console.error((err as Error).message);
    process.exit(1);
  }
} else if (cmd === 'faucet') {
  try {
    const manifest = readManifest();
    if (!manifest.suiAddress) { console.error('No wallet address configured.'); process.exit(1); }
    if (manifest.network !== 'testnet') { console.error('Faucet only available on testnet.'); process.exit(1); }
    await requestFaucet(manifest.suiAddress);
  } catch (err) {
    console.error((err as Error).message);
    process.exit(1);
  }
} else {
  console.error('Usage: wallet-setup info|balance|faucet');
  process.exit(1);
}
