/**
 * Two OpenClaw agents: Agent A (Payer) pays Agent B (Receiver) via x402 + EVVM Native adapter.
 * Uses EVVMNativeX402Adapter by default: x402 auth verified on-chain, EVVM Core pay only (no EIP-3009 on token).
 *
 * Usage:
 *   AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-native.ts
 * Or with receiver key: AGENT_B_PRIVATE_KEY=0x... (optional; AGENT_B_ADDRESS is enough for recipient)
 *
 * Optional env: PAYMENT_AMOUNT (6 decimals, default 1000 = 0.001 USDC.k), STORY_AENEID_RPC
 */

import { ethers } from 'ethers';
import { payViaEVVM, checkPaymentStatus } from '../src/index.ts';

// EVVM Native x402 adapter (Story Aeneid) – no EIP-3009 on token
const NATIVE_ADAPTER = process.env.BRIDGE_EVVM_NATIVE_ADAPTER || '0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc';
const USDC_KRAMP = process.env.BRIDGE_USDC_ADDRESS || '0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5';
const RPC_URL = process.env.STORY_AENEID_RPC || 'https://aeneid.storyrpc.io';
const EVVM_CORE_ADDRESS = process.env.EVVM_CORE_ADDRESS || '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b';
const EVVM_ID = 1140;

function normalizePrivateKey(raw: string | undefined): string | undefined {
  if (!raw) return undefined;
  const hex = raw.trim().replace(/^0x/i, '').replace(/[^0-9a-fA-F]/g, '');
  return hex.length === 64 ? '0x' + hex.toLowerCase() : undefined;
}

async function main() {
  const agentAPrivateKey = normalizePrivateKey(process.env.AGENT_A_PRIVATE_KEY);
  const agentBPrivateKey = normalizePrivateKey(process.env.AGENT_B_PRIVATE_KEY);
  const addressBEnv = process.env.AGENT_B_ADDRESS?.trim();

  if (!agentAPrivateKey) {
    console.error('Set AGENT_A_PRIVATE_KEY (payer).');
    process.exit(1);
  }

  const walletA = new ethers.Wallet(agentAPrivateKey);
  const addressA = walletA.address;
  const addressB = agentBPrivateKey
    ? new ethers.Wallet(agentBPrivateKey).address
    : addressBEnv;
  if (!addressB) {
    console.error('Set AGENT_B_ADDRESS or AGENT_B_PRIVATE_KEY (receiver).');
    process.exit(1);
  }

  const amountRaw = process.env.PAYMENT_AMOUNT || '1000'; // 0.001 USDC.k (6 decimals)
  const receiptId = `x402_native_a_to_b_${Date.now()}`;
  const now = Math.floor(Date.now() / 1000);
  const validAfter = now - 120;
  const validBefore = now + 3600;

  console.log('--- Two agents: x402 + EVVM Native adapter (no EIP-3009 on token) ---\n');
  console.log('Adapter (native):', NATIVE_ADAPTER);
  console.log('Agent A (Payer):', addressA);
  console.log('Agent B (Receiver):', addressB);
  console.log('Amount:', ethers.formatUnits(amountRaw, 6), 'USDC.k');
  console.log('Receipt ID:', receiptId);
  console.log('');

  console.log('[Agent A] Submitting x402 + EVVM payment (native adapter)...');
  const result = await payViaEVVM({
    from: addressA,
    to: addressB,
    toIdentity: '',
    amount: amountRaw,
    receiptId,
    privateKey: agentAPrivateKey,
    adapterAddress: NATIVE_ADAPTER,
    usdcDanceAddress: USDC_KRAMP,
    evvmCoreAddress: EVVM_CORE_ADDRESS,
    evvmId: EVVM_ID,
    rpcUrl: RPC_URL,
    useAsyncNonce: true,
    useNativeAdapter: true,
    validAfter,
    validBefore,
  });
  console.log('[Agent A] Tx hash:', result.txHash);
  console.log('[Agent A] Done.\n');

  console.log('[Agent B] Checking payment status...');
  const status = await checkPaymentStatus(receiptId, NATIVE_ADAPTER, RPC_URL);
  if (!status.exists) {
    console.error('[Agent B] Payment not found for receipt', receiptId);
    process.exit(1);
  }
  console.log('[Agent B] Received payment:');
  console.log('  From:', status.from);
  console.log('  To:', status.to);
  console.log('  Amount:', ethers.formatUnits(status.amount, 6), 'USDC.k');
  console.log('  Receipt ID:', receiptId);

  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const usdc = new ethers.Contract(
    USDC_KRAMP,
    ['function balanceOf(address) view returns (uint256)'],
    provider
  );
  const balanceB = await usdc.balanceOf(addressB);
  console.log('[Agent B] USDC.k balance after:', ethers.formatUnits(balanceB, 6));
  console.log('\n--- Two-agent native x402 flow complete ---');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
