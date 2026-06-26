/**
 * Simulate two OpenClaw agents with x402 only: Agent A (Payer) signs EIP-3009 and sends USDC.d
 * directly to Agent B (Receiver) via BridgeUSDC.transferWithAuthorization. No EVVM adapter.
 *
 * Usage:
 *   AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-direct.ts
 */

import { ethers } from 'ethers';
import { generateX402Signature } from '../src/x402-signer.ts';

const RPC_URL = process.env.STORY_AENEID_RPC || 'https://aeneid.storyrpc.io';
const USDC_DANCE_ADDRESS = process.env.BRIDGE_USDC_ADDRESS || '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40';
const CHAIN_ID = 1315;

const BRIDGE_USDC_ABI = [
  'function transferWithAuthorization(address from, address to, uint256 amount, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s)',
  'function balanceOf(address) view returns (uint256)'
];

async function main() {
  const agentAPrivateKey = process.env.AGENT_A_PRIVATE_KEY?.startsWith('0x')
    ? process.env.AGENT_A_PRIVATE_KEY
    : process.env.AGENT_A_PRIVATE_KEY
      ? '0x' + process.env.AGENT_A_PRIVATE_KEY
      : undefined;
  const addressB = process.env.AGENT_B_ADDRESS ?? (process.env.AGENT_B_PRIVATE_KEY
    ? new ethers.Wallet(
        process.env.AGENT_B_PRIVATE_KEY.startsWith('0x')
          ? process.env.AGENT_B_PRIVATE_KEY
          : '0x' + process.env.AGENT_B_PRIVATE_KEY
      ).address
    : undefined);

  if (!agentAPrivateKey || !addressB) {
    console.error('Set AGENT_A_PRIVATE_KEY and AGENT_B_ADDRESS (or AGENT_B_PRIVATE_KEY).');
    process.exit(1);
  }

  const walletA = new ethers.Wallet(agentAPrivateKey, new ethers.JsonRpcProvider(RPC_URL));
  const addressA = walletA.address;
  const amountRaw = process.env.PAYMENT_AMOUNT || '500000'; // 0.5 USDC.d
  const now = Math.floor(Date.now() / 1000);
  const validAfter = now - 120;
  const validBefore = now + 3600;
  const nonce = ethers.keccak256(ethers.toUtf8Bytes(`x402_direct_${Date.now()}`));

  console.log('--- Two agents: x402 direct USDC.d transfer (no EVVM) ---\n');
  console.log('Agent A (Payer):', addressA);
  console.log('Agent B (Receiver):', addressB);
  console.log('Amount:', ethers.formatUnits(amountRaw, 6), 'USDC.d\n');

  const x402Sig = await generateX402Signature({
    from: addressA,
    to: addressB,
    amount: amountRaw,
    validAfter,
    validBefore,
    nonce,
    usdcDanceAddress: USDC_DANCE_ADDRESS,
    chainId: CHAIN_ID,
    privateKey: agentAPrivateKey
  });

  const usdc = new ethers.Contract(USDC_DANCE_ADDRESS, BRIDGE_USDC_ABI, walletA);
  const tx = await usdc.transferWithAuthorization(
    addressA,
    addressB,
    amountRaw,
    validAfter,
    validBefore,
    nonce,
    x402Sig.v,
    x402Sig.r,
    x402Sig.s
  );
  console.log('[Agent A] Tx hash:', tx.hash);
  await tx.wait();
  console.log('[Agent A] Confirmed.\n');

  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const balanceB = await new ethers.Contract(USDC_DANCE_ADDRESS, ['function balanceOf(address) view returns (uint256)'], provider).balanceOf(addressB);
  console.log('[Agent B] USDC.d balance after:', ethers.formatUnits(balanceB, 6));
  console.log('\n--- Done ---');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
