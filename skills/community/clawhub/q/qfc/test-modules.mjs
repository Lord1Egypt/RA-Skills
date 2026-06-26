/**
 * Integration test for all QFC OpenClaw modules.
 * Run: node test-modules.mjs
 */

import {
  QFCFaucet,
  QFCChain,
  QFCNetwork,
  QFCStaking,
  QFCEpoch,
} from './dist/index.js';

async function main() {
  console.log('=== QFC OpenClaw Modules Test ===\n');

  // 1. Faucet
  try {
    const faucet = new QFCFaucet('testnet');
    const addr = '0x' + '1'.repeat(40);
    const result = await faucet.requestQFC(addr, '10');
    console.log(`1. Faucet: requested ${result.amount} QFC → txHash: ${result.txHash}`);
  } catch (e) {
    console.log(`1. Faucet: ${e.message}`);
  }

  // 2. Chain
  try {
    const chain = new QFCChain('testnet');
    const blockNum = await chain.getBlockNumber();
    const block = await chain.getBlock('latest');
    console.log(`2. Chain: block #${block.number}, ${block.transactionCount} txs`);
  } catch (e) {
    console.log(`2. Chain: ${e.message}`);
  }

  // 3. Network
  try {
    const net = new QFCNetwork('testnet');
    const info = await net.getNodeInfo();
    const state = await net.getNetworkState();
    console.log(`3. Network: node ${info.version}, ${info.peerCount} peers, ${state}`);
  } catch (e) {
    console.log(`3. Network: ${e.message}`);
  }

  // 4. Staking
  try {
    const staking = new QFCStaking('testnet');
    const validators = await staking.getValidators();
    const totalStake = validators.reduce((sum, v) => sum + parseFloat(v.stake), 0);
    console.log(`4. Staking: ${validators.length} validators, total stake ${totalStake} QFC`);
  } catch (e) {
    console.log(`4. Staking: ${e.message}`);
  }

  // 5. Epoch
  try {
    const epoch = new QFCEpoch('testnet');
    const info = await epoch.getCurrentEpoch();
    const finalized = await epoch.getFinalizedBlock();
    console.log(`5. Epoch: epoch #${info.number}, finalized block #${finalized}`);
  } catch (e) {
    console.log(`5. Epoch: ${e.message}`);
  }

  console.log('\n=== Done ===');
}

main().catch(console.error);
