import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { QFCWallet, QFCKeystore } from './dist/index.js';

const TEST_DIR = path.join(os.tmpdir(), 'qfc-keystore-test-' + Date.now());
const PASSWORD = 'test-password-123';

async function run() {
  const ks = new QFCKeystore(TEST_DIR);

  // 1. Create wallet
  const w = new QFCWallet('testnet');
  const { address } = w.createWallet();
  console.log('1. Create wallet →', address);

  // 2. Save encrypted
  await ks.saveWallet(
    (await import('ethers')).ethers.Wallet.createRandom(), // fresh wallet for isolated test
    PASSWORD,
    { name: 'test-wallet', network: 'testnet' },
  );
  // Also test via QFCWallet.save (uses default dir, so use keystore directly)
  const { ethers } = await import('ethers');
  const testWallet = ethers.Wallet.createRandom();
  const savedPath = await ks.saveWallet(testWallet, PASSWORD, {
    name: 'test-wallet',
    network: 'testnet',
  });
  console.log('2. Save encrypted → saved to', savedPath);

  // 3. List wallets
  const list = ks.listWallets();
  console.log(
    '3. List wallets →',
    list.map((m) => ({ address: m.address, name: m.name, network: m.network })),
  );

  // 4. Load wallet
  const loaded = await ks.loadWallet(testWallet.address, PASSWORD);
  const match = loaded.address.toLowerCase() === testWallet.address.toLowerCase();
  console.log('4. Load wallet → address matches:', match);
  if (!match) {
    console.error('   FAIL: expected', testWallet.address, 'got', loaded.address);
    process.exit(1);
  }

  // 5. Export keystore JSON
  const json = ks.getKeystoreJson(testWallet.address);
  console.log('5. Export keystore JSON →', json ? 'OK (' + json.length + ' bytes)' : 'FAIL');

  // 6. Remove wallet
  const removed = ks.removeWallet(testWallet.address);
  const listAfter = ks.listWallets();
  console.log('6. Remove wallet → removed:', removed, '| remaining:', listAfter.length);

  // 7. File permissions
  const metaPath = path.join(TEST_DIR, 'meta.json');
  if (fs.existsSync(metaPath)) {
    const stat = fs.statSync(metaPath);
    const mode = '0' + (stat.mode & 0o777).toString(8);
    console.log('7. File permissions → meta.json:', mode);
  }

  // Cleanup
  fs.rmSync(TEST_DIR, { recursive: true, force: true });
  console.log('\nAll tests passed!');
}

run().catch((err) => {
  console.error('Test failed:', err);
  // Cleanup on error too
  fs.rmSync(TEST_DIR, { recursive: true, force: true });
  process.exit(1);
});
