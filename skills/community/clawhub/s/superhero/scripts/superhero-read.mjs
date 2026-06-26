#!/usr/bin/env node
// Read posts, profile data from superhero.com via æternity middleware
import { MemoryAccount } from '@aeternity/aepp-sdk';

const CONTRACT_ADDRESS = 'ct_2Hyt9ZxzXra5NAzhePkRsDPDWppoatVD7CtHnUoHVbuehwR8Nb';
const MIDDLEWARE_URL = 'https://mainnet.aeternity.io/mdw/v3';

function getWalletAddress() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey).address;
}

async function getPostsFromAddress(address, limit = 20) {
  const url = `${MIDDLEWARE_URL}/accounts/${address}/activities?limit=${limit * 2}`;
  const response = await fetch(url);
  const data = await response.json();

  if (!data.data || !Array.isArray(data.data)) {
    console.error('Unexpected API response:', JSON.stringify(data));
    return [];
  }

  return data.data
    .filter(activity =>
      activity.type === 'ContractCallTxEvent' &&
      activity.payload?.tx?.contract_id === CONTRACT_ADDRESS &&
      activity.payload?.tx?.function === 'post_without_tip'
    )
    .map(activity => {
      const tx = activity.payload.tx;
      return {
        txHash: activity.payload.hash,
        postId: tx.return?.value || null,
        content: tx.arguments[0]?.value || '',
        links: tx.arguments[1]?.value?.map(v => v.value) || [],
        timestamp: new Date(activity.payload.micro_time).toISOString(),
        height: activity.height,
      };
    })
    .slice(0, limit);
}

async function main() {
  const command = process.argv[2] || 'help';
  const arg = process.argv[3];
  const limit = parseInt(process.argv[4]) || 20;

  switch (command) {
    case 'my-posts': {
      const address = getWalletAddress();
      console.error(`Fetching posts from ${address}...`);
      const posts = await getPostsFromAddress(address, limit);
      console.log(JSON.stringify(posts, null, 2));
      break;
    }

    case 'profile': {
      if (!arg) {
        console.error('Usage: node scripts/superhero-read.mjs profile <address>');
        process.exit(1);
      }
      console.error(`Fetching profile for ${arg}...`);
      const posts = await getPostsFromAddress(arg, 50);
      console.log(JSON.stringify({
        address: arg,
        postCount: posts.length,
        latestPost: posts[0] || null,
        posts: posts.slice(0, 10),
      }, null, 2));
      break;
    }

    case 'latest': {
      const address = getWalletAddress();
      console.error(`Fetching latest ${limit} posts...`);
      const posts = await getPostsFromAddress(address, limit);
      console.log(JSON.stringify(posts, null, 2));
      break;
    }

    case 'search': {
      if (!arg) {
        console.error('Usage: node scripts/superhero-read.mjs search <keyword>');
        process.exit(1);
      }
      const address = getWalletAddress();
      console.error(`Searching posts for "${arg}"...`);
      const posts = await getPostsFromAddress(address, limit);
      const matches = posts.filter(p =>
        p.content.toLowerCase().includes(arg.toLowerCase())
      );
      console.log(JSON.stringify({ keyword: arg, found: matches.length, posts: matches }, null, 2));
      break;
    }

    case 'help':
    default:
      console.log(`
Superhero.com Read Commands:

  my-posts [limit]           Get your posts (default: 20)
  profile <address> [limit]  Get posts from specific address
  latest [limit]             Get your latest posts
  search <keyword> [limit]   Search your posts for keyword

Examples:
  node scripts/superhero-read.mjs my-posts
  node scripts/superhero-read.mjs my-posts 50
  node scripts/superhero-read.mjs profile ak_...
  node scripts/superhero-read.mjs latest 5
  node scripts/superhero-read.mjs search "AI agents"

Note: Reads from æternity middleware API. Comments are off-chain.
`);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });