#!/usr/bin/env node
// Comment on a superhero.com post via Tipping_v3 contract (on-chain)
// Comments are on-chain posts with "comment:<post_id>" as the first media entry
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
const API_BASE = 'https://api.superhero.com';

async function main() {
  const command = process.argv[2] || 'help';

  switch (command) {
    case 'post': {
      // Post a comment (reply) on a post — on-chain via Tipping_v3
      const postId = process.argv[3];
      const content = process.argv[4];
      if (!postId || !content) {
        console.error('Usage: node scripts/superhero-comment.mjs post <post_id> "<content>"');
        process.exit(1);
      }

      const account = loadAccount();
      const node = new Node(NODE_URL);
      const aeSdk = new AeSdk({
        nodes: [{ name: 'mainnet', instance: node }],
        accounts: [account],
      });

      const aci = JSON.parse(fs.readFileSync('./contracts/Tipping_v3.aci.json', 'utf8'));
      const contract = await Contract.initialize({ aci, address: CONTRACT_ADDRESS, onAccount: aeSdk, onNode: aeSdk.api });

      // Comments encode the parent post ID as special first media entry
      const media = [`comment:${postId}`];
      console.error(`Posting comment on post ${postId}...`);
      const result = await contract.post_without_tip(content, media, { onAccount: account });

      console.log(JSON.stringify({
        success: true,
        comment_post_id: result.decodedResult?.toString() || null,
        parent_post_id: postId,
        content,
        tx_hash: result.hash,
      }));
      break;
    }

    case 'get': {
      // Get comments for a post
      const postId = process.argv[3];
      const limit = parseInt(process.argv[4]) || 20;
      const page = parseInt(process.argv[5]) || 1;
      if (!postId) {
        console.error('Usage: node scripts/superhero-comment.mjs get <post_id> [limit] [page]');
        process.exit(1);
      }
      const url = `${API_BASE}/api/posts/${encodeURIComponent(postId)}/comments?limit=${limit}&page=${page}`;
      const res = await fetch(url);
      if (!res.ok) {
        console.error(`API error: ${res.status} ${res.statusText}`);
        process.exit(1);
      }
      const data = await res.json();
      console.log(JSON.stringify(data, null, 2));
      break;
    }

    case 'help':
    default:
      console.log(`
Superhero.com Comment Commands:

  post <post_id> "<content>"
    Post a comment (reply) on an existing post. On-chain via Tipping_v3.
    Costs a small amount of AE for gas (~0.00001 AE).

  get <post_id> [limit] [page]
    Read comments on a post (read-only, no wallet needed).

Examples:
  node scripts/superhero-comment.mjs post 3903 "Great post!"
  node scripts/superhero-comment.mjs get 3903
  node scripts/superhero-comment.mjs get 3903 50 2
`);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
