#!/usr/bin/env node
/**
 * Demo: Content Generator Agent
 *
 * Shows how an AI agent with INFERENCE-only permission can:
 * 1. Be registered with minimal permissions (InferenceSubmit only)
 * 2. Generate content on a schedule using session keys
 * 3. Cannot transfer funds (permission denied)
 *
 * Usage:
 *   export OWNER_PRIVATE_KEY=0x...
 *   node scripts/demo-content-generator.mjs
 */

import { ethers } from 'ethers';
import { AgentWalletClient } from '../dist/agent-wallet.js';

const NETWORK = 'testnet';

async function main() {
  const ownerKey = process.env.OWNER_PRIVATE_KEY;
  if (!ownerKey) {
    console.error('Set OWNER_PRIVATE_KEY environment variable');
    process.exit(1);
  }

  const ownerWallet = new ethers.Wallet(ownerKey);
  const sessionWallet = ethers.Wallet.createRandom();

  console.log(`Owner: ${ownerWallet.address}`);
  console.log(`Session key: ${sessionWallet.address}`);

  // --- Owner setup ---

  const client = new AgentWalletClient(NETWORK);

  console.log('\n[1/3] Registering content-gen agent (InferenceSubmit only)...');
  const reg = await client.register(ownerWallet, {
    agentId: 'content-gen-1',
    agentAddress: sessionWallet.address,
    permissions: ['InferenceSubmit'],  // No Transfer!
    dailyLimitQFC: '10',
    maxPerTxQFC: '1',
    depositQFC: '5',
  });
  console.log(`Registered: ${reg.explorerUrl}`);

  await client.issueSessionKey(ownerWallet, {
    agentId: 'content-gen-1',
    sessionKeyAddress: sessionWallet.address,
    durationSeconds: 86400 * 7, // 7 days
  });
  console.log('Session key issued (7 day TTL)');

  // --- Agent generates content ---

  const agentClient = new AgentWalletClient(NETWORK, {
    privateKey: sessionWallet.privateKey,
    agentId: 'content-gen-1',
  });

  console.log('\n[2/3] Generating content via inference...');
  const result = await agentClient.submitInference(
    'qfc-embed-small',
    'TextGeneration',
    'Write a short blog post about decentralized AI compute networks',
    '0.5',
  );
  console.log(`Task: ${result.taskId} — Status: ${result.status.status}`);

  // --- Verify Transfer permission is denied ---

  console.log('\n[3/3] Testing Transfer permission (should be denied)...');
  const check = await agentClient.preflight('content-gen-1', {
    requiredPermission: 'Transfer',
    amountQFC: '1',
  });
  console.log(`Transfer allowed: ${check.allowed}`);
  if (!check.allowed) {
    console.log(`Denied reasons: ${check.reasons.join('; ')}`);
  }

  console.log('\nDemo complete.');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
