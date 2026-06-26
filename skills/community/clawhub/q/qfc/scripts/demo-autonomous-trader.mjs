#!/usr/bin/env node
/**
 * Demo: Autonomous Trader Agent
 *
 * Shows how an AI agent can:
 * 1. Be registered by an owner with Transfer + InferenceSubmit permissions
 * 2. Receive a session key (no owner key needed after this point)
 * 3. Run sentiment analysis via inference
 * 4. Execute trades based on results
 *
 * Usage:
 *   export OWNER_PRIVATE_KEY=0x...
 *   node scripts/demo-autonomous-trader.mjs
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
  console.log(`Owner: ${ownerWallet.address}`);

  // --- Phase 1: Owner sets up the agent ---

  const client = new AgentWalletClient(NETWORK);

  // Generate a session key for the agent
  const sessionWallet = ethers.Wallet.createRandom();
  console.log(`Session key address: ${sessionWallet.address}`);

  // Register the agent
  console.log('\n[1/4] Registering agent...');
  const reg = await client.register(ownerWallet, {
    agentId: 'trader-1',
    agentAddress: sessionWallet.address,
    permissions: ['InferenceSubmit', 'Transfer'],
    dailyLimitQFC: '100',
    maxPerTxQFC: '10',
    depositQFC: '50',
  });
  console.log(`Registered: ${reg.explorerUrl}`);

  // Issue session key (valid for 24 hours)
  console.log('\n[2/4] Issuing session key...');
  const keyTx = await client.issueSessionKey(ownerWallet, {
    agentId: 'trader-1',
    sessionKeyAddress: sessionWallet.address,
    durationSeconds: 86400,
  });
  console.log(`Session key issued: ${keyTx.explorerUrl}`);

  // --- Phase 2: Agent operates autonomously ---

  const agentClient = new AgentWalletClient(NETWORK, {
    privateKey: sessionWallet.privateKey,
    agentId: 'trader-1',
  });

  // Run sentiment analysis
  console.log('\n[3/4] Submitting inference (sentiment analysis)...');
  const result = await agentClient.submitInference(
    'qfc-embed-small',
    'TextEmbedding',
    'Bitcoin price surging, market sentiment very bullish, institutional buying detected',
    '0.1',
  );
  console.log(`Task: ${result.taskId} — Status: ${result.status.status}`);
  if (result.decoded) {
    console.log('Result:', JSON.stringify(result.decoded.output, null, 2));
  }

  // Check agent status
  console.log('\n[4/4] Agent status:');
  const info = await agentClient.status('trader-1');
  console.log(`  Active: ${info.active}`);
  console.log(`  Deposit: ${info.deposit} QFC`);
  console.log(`  Spent today: ${info.spentToday} QFC`);
  console.log(`  Daily limit: ${info.dailyLimit} QFC`);

  console.log('\nDemo complete.');
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
