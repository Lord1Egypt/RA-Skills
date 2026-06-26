#!/usr/bin/env node
/**
 * Demo: AI Oracle Agent
 *
 * Shows how an AI agent can answer on-chain queries:
 * 1. Register with InferenceSubmit + QueryOnly permissions
 * 2. Estimate fees before submitting
 * 3. Submit queries and decode results
 * 4. Monitor spending with preflight checks
 *
 * In production, a paymaster would sponsor gas so the agent
 * doesn't need to hold QFC directly (M2 feature).
 *
 * Usage:
 *   export OWNER_PRIVATE_KEY=0x...
 *   node scripts/demo-ai-oracle.mjs
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
  console.log(`Oracle session key: ${sessionWallet.address}`);

  const client = new AgentWalletClient(NETWORK);

  // --- Register oracle agent ---

  console.log('\n[1/5] Registering oracle agent...');
  const reg = await client.register(ownerWallet, {
    agentId: 'oracle-1',
    agentAddress: sessionWallet.address,
    permissions: ['InferenceSubmit', 'QueryOnly'],
    dailyLimitQFC: '50',
    maxPerTxQFC: '5',
    depositQFC: '25',
  });
  console.log(`Registered: ${reg.explorerUrl}`);

  await client.issueSessionKey(ownerWallet, {
    agentId: 'oracle-1',
    sessionKeyAddress: sessionWallet.address,
    durationSeconds: 86400 * 3, // 3 days
  });
  console.log('Session key issued (3 day TTL)');

  // --- Oracle operates ---

  const oracle = new AgentWalletClient(NETWORK, {
    privateKey: sessionWallet.privateKey,
    agentId: 'oracle-1',
  });

  // Estimate fee first
  console.log('\n[2/5] Estimating fee...');
  const fee = await oracle.estimateFee('qfc-embed-small', 'TextEmbedding');
  console.log(`  Base fee: ${fee.baseFee} QFC`);
  console.log(`  GPU tier: ${fee.gpuTier}`);
  console.log(`  Est. time: ${fee.estimatedTimeMs}ms`);

  // Preflight check before spending
  console.log('\n[3/5] Preflight check...');
  const check = await oracle.preflight('oracle-1', {
    requiredPermission: 'InferenceSubmit',
    amountQFC: fee.baseFee,
  });
  console.log(`  Allowed: ${check.allowed}`);
  if (check.warnings.length > 0) {
    console.log(`  Warnings: ${check.warnings.join('; ')}`);
  }

  // Answer a query
  console.log('\n[4/5] Answering query via inference...');
  const result = await oracle.submitInference(
    'qfc-embed-small',
    'TextEmbedding',
    'What is the current gas price trend on QFC network?',
    '1',
  );
  console.log(`Task: ${result.taskId} — Status: ${result.status.status}`);

  // Check remaining budget
  console.log('\n[5/5] Agent spending report:');
  const info = await oracle.status('oracle-1');
  console.log(`  Deposit remaining: ${info.deposit} QFC`);
  console.log(`  Spent today: ${info.spentToday} QFC`);
  console.log(`  Daily budget left: ${(parseFloat(info.dailyLimit) - parseFloat(info.spentToday)).toFixed(4)} QFC`);

  console.log('\nDemo complete.');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
