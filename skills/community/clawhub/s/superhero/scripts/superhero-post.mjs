#!/usr/bin/env node
// Post to superhero.com via Tipping_v3 contract on æternity mainnet
import { AeSdk, Node, MemoryAccount, Contract } from '@aeternity/aepp-sdk';
import fs from 'fs';

const CONTRACT_ADDRESS = 'ct_2Hyt9ZxzXra5NAzhePkRsDPDWppoatVD7CtHnUoHVbuehwR8Nb';
const NODE_URL = 'https://mainnet.aeternity.io';

function loadAccount() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey);
}

async function main() {
  const content = process.argv[2];

  if (!content || content === 'help') {
    console.log(`
Post Commands:

  node scripts/superhero-post.mjs "<content>" [link1] [link2] ...

    content    Post text (required)
    link1...   Optional media URLs to attach

Examples:
  node scripts/superhero-post.mjs "Hello from Æ"
  node scripts/superhero-post.mjs "Check this out" "https://example.com"
  node scripts/superhero-post.mjs "Multiple links" "https://a.com" "https://b.com"

Note: Each post costs a small amount of AE for gas (~0.00001 AE).
`);
    process.exit(0);
  }

  const links = process.argv.slice(3);

  const account = loadAccount();

  const node = new Node(NODE_URL);
  const aeSdk = new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
    accounts: [account],
  });

  const aci = JSON.parse(fs.readFileSync('./contracts/Tipping_v3.aci.json', 'utf8'));
  const contract = await Contract.initialize({ aci, address: CONTRACT_ADDRESS, onAccount: aeSdk, onNode: aeSdk.api });

  console.error(`Posting "${content.slice(0, 60)}${content.length > 60 ? '...' : ''}" with ${links.length} link(s)...`);
  const result = await contract.post_without_tip(content, links, { onAccount: account });

  console.log(JSON.stringify({
    success: true,
    post_id: result.decodedResult?.toString() || null,
    content,
    links,
    tx_hash: result.hash,
  }));
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
