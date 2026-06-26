#!/usr/bin/env node
// View on-chain transactions for tokens — filter by token, account, or see all

import { MemoryAccount } from '@aeternity/aepp-sdk';

const API_BASE = 'https://api.superhero.com';

function loadAddress() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) return null;
  return new MemoryAccount(privateKey).address;
}

function buildQuery(params) {
  return Object.entries(params)
    .filter(([, v]) => v != null)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
}

async function fetchTransactions({ token_address, account_address, includes, limit, page }) {
  const query = buildQuery({ token_address, account_address, includes, limit, page });
  const url = `${API_BASE}/api/transactions${query ? `?${query}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) { console.error(`API error: ${res.status} ${await res.text()}`); process.exit(1); }
  return res.json();
}

function formatTx(tx) {
  return {
    type: tx.tx_type,
    hash: tx.tx_hash,
    account: tx.address,
    token_name: tx.token?.name,
    token_symbol: tx.token?.symbol,
    sale_address: tx.sale_address || tx.token?.sale_address,
    amount_ae: tx.amount?.ae,
    unit_price_ae: tx.unit_price?.ae,
    buy_price_ae: tx.buy_price?.ae,
    sell_price_ae: tx.sell_price?.ae,
    timestamp: tx.created_at,
    block_height: tx.block_height,
  };
}

async function main() {
  const command = process.argv[2] || 'help';

  switch (command) {
    case 'token': {
      // All transactions for a specific token
      const token_address = process.argv[3];
      if (!token_address) {
        console.error('Usage: node scripts/superhero-transactions.mjs token <sale_address> [limit] [page]');
        process.exit(1);
      }
      const limit = parseInt(process.argv[4]) || 20;
      const page = parseInt(process.argv[5]) || 1;
      const data = await fetchTransactions({ token_address, includes: 'token', limit, page });
      const txs = (data.items || data.data || []).map(formatTx);
      console.log(JSON.stringify({ token_address, page, limit, transactions: txs }, null, 2));
      break;
    }

    case 'account': {
      // All transactions by a specific account (defaults to own wallet)
      const account_address = process.argv[3] || loadAddress();
      if (!account_address) {
        console.error('No wallet configured and no address provided.');
        process.exit(1);
      }
      const limit = parseInt(process.argv[4]) || 20;
      const page = parseInt(process.argv[5]) || 1;
      const data = await fetchTransactions({ account_address, includes: 'token', limit, page });
      const txs = (data.items || data.data || []).map(formatTx);
      console.log(JSON.stringify({ account_address, page, limit, transactions: txs }, null, 2));
      break;
    }

    case 'mine': {
      // Shortcut: transactions by own wallet
      const account_address = loadAddress();
      if (!account_address) {
        console.error('No wallet found. Run: node scripts/superhero-wallet.mjs generate');
        process.exit(1);
      }
      const limit = parseInt(process.argv[3]) || 20;
      const page = parseInt(process.argv[4]) || 1;
      const data = await fetchTransactions({ account_address, includes: 'token', limit, page });
      const txs = (data.items || data.data || []).map(formatTx);
      console.log(JSON.stringify({ account_address, page, limit, transactions: txs }, null, 2));
      break;
    }

    case 'all': {
      // All recent transactions across the platform (useful for market pulse)
      const limit = parseInt(process.argv[3]) || 20;
      const page = parseInt(process.argv[4]) || 1;
      const data = await fetchTransactions({ includes: 'token', limit, page });
      const txs = (data.items || data.data || []).map(formatTx);
      console.log(JSON.stringify({ page, limit, transactions: txs }, null, 2));
      break;
    }

    case 'activity': {
      // Token + account filter combined — useful to check if a whale is buying a token
      const token_address = process.argv[3];
      const account_address = process.argv[4];
      if (!token_address || !account_address) {
        console.error('Usage: node scripts/superhero-transactions.mjs activity <token_address> <account_address> [limit]');
        process.exit(1);
      }
      const limit = parseInt(process.argv[5]) || 20;
      const data = await fetchTransactions({ token_address, account_address, includes: 'token', limit });
      const txs = (data.items || data.data || []).map(formatTx);
      console.log(JSON.stringify({ token_address, account_address, transactions: txs }, null, 2));
      break;
    }

    case 'help':
    default:
      console.log(`
Superhero Transactions Commands:

  token <sale_address> [limit] [page]
    All buy/sell transactions for a specific token
    Great for seeing who is buying and selling momentum tokens

  account [address] [limit] [page]
    All transactions by a specific account address
    Defaults to your wallet if no address given

  mine [limit] [page]
    Shortcut for your own wallet's transactions

  all [limit] [page]
    All recent platform transactions (market activity feed)

  activity <token_address> <account_address> [limit]
    Transactions for a specific token by a specific account
    Use to check if a whale or specific trader is accumulating

Examples:
  node scripts/superhero-transactions.mjs mine
  node scripts/superhero-transactions.mjs mine 50
  node scripts/superhero-transactions.mjs token ct_abc... 30
  node scripts/superhero-transactions.mjs account ak_xyz... 20
  node scripts/superhero-transactions.mjs all 20
  node scripts/superhero-transactions.mjs activity ct_abc... ak_xyz...
`);
      break;
  }
}

main().catch(err => {
  console.error(err.message || err);
  process.exit(1);
});
