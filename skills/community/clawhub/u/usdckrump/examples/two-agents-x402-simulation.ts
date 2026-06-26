/**
 * Simulate two OpenClaw agents: Agent A (Payer) pays Agent B (Receiver) with USDC.d via x402 + EVVM.
 * Agent A submits the payment; Agent B verifies receipt and balance.
 *
 * For a simpler x402-only demo (no EVVM), use: two-agents-x402-direct.ts
 *
 * Usage:
 *   AGENT_A_PRIVATE_KEY=0x... AGENT_B_PRIVATE_KEY=0x... npx tsx examples/two-agents-x402-simulation.ts
 */

import { ethers } from 'ethers';
import { payViaEVVM, checkPaymentStatus } from '../src/index.ts';

const RPC_URL = process.env.STORY_AENEID_RPC || 'https://aeneid.storyrpc.io';
const ADAPTER_ADDRESS = process.env.BRIDGE_EVVM_ADAPTER || '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314';
const USDC_DANCE_ADDRESS = process.env.BRIDGE_USDC_ADDRESS || '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40';
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

  const amountRaw = process.env.PAYMENT_AMOUNT || '500000'; // 0.5 USDC.d (6 decimals) so payer keeps some
  const receiptId = `x402_agent_a_to_b_${Date.now()}`;
  const now = Math.floor(Date.now() / 1000);
  const validAfter = now - 120; // 2 min in the past so chain clock skew doesn't break auth
  const validBefore = now + 3600;

  console.log('--- Two OpenClaw agents: x402 payment with USDC.d ---\n');
  console.log('Agent A (Payer):', addressA);
  console.log('Agent B (Receiver):', addressB);
  console.log('Amount:', ethers.formatUnits(amountRaw, 6), 'USDC.d');
  console.log('Receipt ID:', receiptId);
  console.log('');

  // --- Agent A: send payment via x402 + EVVM ---
  console.log('[Agent A] Submitting x402 + EVVM payment...');
  const result = await payViaEVVM({
    from: addressA,
    to: addressB,
    toIdentity: '',
    amount: amountRaw,
    receiptId,
    privateKey: agentAPrivateKey,
    adapterAddress: ADAPTER_ADDRESS,
    usdcDanceAddress: USDC_DANCE_ADDRESS,
    evvmCoreAddress: EVVM_CORE_ADDRESS,
    evvmId: EVVM_ID,
    rpcUrl: RPC_URL,
    useAsyncNonce: true,
    validAfter,
    validBefore,
  });
  console.log('[Agent A] Tx hash:', result.txHash);
  console.log('[Agent A] Done.\n');

  // --- Agent B: verify payment ---
  console.log('[Agent B] Checking payment status...');
  const status = await checkPaymentStatus(receiptId, ADAPTER_ADDRESS, RPC_URL);
  if (!status.exists) {
    console.error('[Agent B] Payment not found for receipt', receiptId);
    process.exit(1);
  }
  console.log('[Agent B] Received payment:');
  console.log('  From:', status.from);
  console.log('  To:', status.to);
  console.log('  Amount:', ethers.formatUnits(status.amount, 6), 'USDC.d');
  console.log('  Receipt ID:', receiptId);

  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const usdc = new ethers.Contract(
    USDC_DANCE_ADDRESS,
    ['function balanceOf(address) view returns (uint256)'],
    provider
  );
  const balanceB = await usdc.balanceOf(addressB);
  console.log('[Agent B] USDC.d balance after:', ethers.formatUnits(balanceB, 6));
  console.log('\n--- Simulation complete ---');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
