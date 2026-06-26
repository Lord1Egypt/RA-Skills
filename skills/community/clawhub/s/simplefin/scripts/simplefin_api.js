#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Parse arguments
const args = process.argv.slice(2);
if (args.length < 2 && args[0] !== 'claim') {
  console.error("Usage: simplefin_api.js <access_url> <action> [options]");
  console.error("       simplefin_api.js claim <setup_token>");
  console.error("Actions: accounts, transactions, claim");
  console.error("Options for transactions: --start-date <YYYY-MM-DD> --end-date <YYYY-MM-DD> --account <account_id>");
  process.exit(1);
}

if (args[0] === 'claim') {
  const setupToken = args[1];
  if (!setupToken) {
    console.error("Missing setup token");
    process.exit(1);
  }
  try {
    const claimUrl = Buffer.from(setupToken, 'base64').toString('utf8');
    const cmd = `curl -s -H "Content-Length: 0" -X POST "${claimUrl}"`;
    const accessUrl = execSync(cmd).toString().trim();
    if (accessUrl.startsWith('http')) {
      console.log(accessUrl);
    } else {
      console.error("Failed to claim token: " + accessUrl);
      process.exit(1);
    }
  } catch (e) {
    console.error("Error claiming token: " + e.message);
    process.exit(1);
  }
  process.exit(0);
}

const url = args[0];
const action = args[1];

let startDate = null;
let endDate = null;
let accountFilter = null;

for (let i = 2; i < args.length; i++) {
  if (args[i] === '--start-date') startDate = args[++i];
  if (args[i] === '--end-date') endDate = args[++i];
  if (args[i] === '--account') accountFilter = args[++i];
}

function fetchFromApi(endpointUrl) {
  try {
    const parts = new URL(url);
    const auth = Buffer.from(`${parts.username}:${parts.password}`).toString('base64');
    
    // Construct the actual API URL. simplefin URLs typically look like:
    // https://username:password@beta-bridge.simplefin.org/simplefin
    const baseUrl = `${parts.origin}${parts.pathname}`;
    const targetUrl = `${baseUrl}${endpointUrl}`;
    
    const cmd = `curl -s -H "Authorization: Basic ${auth}" "${targetUrl}"`;
    const output = execSync(cmd).toString();
    return JSON.parse(output);
  } catch (e) {
    console.error("Error fetching data from SimpleFIN:");
    console.error(e.message);
    process.exit(1);
  }
}

if (action === 'accounts') {
  const data = fetchFromApi('/accounts');
  console.log(JSON.stringify(data.accounts.map(a => ({
    id: a.id,
    name: a.name,
    currency: a.currency,
    balance: a.balance,
    org: a.org.name
  })), null, 2));
} else if (action === 'transactions') {
  let endpoint = '/accounts';
  const queryParams = [];
  if (startDate) {
    queryParams.push(`start-date=${Math.floor(new Date(startDate).getTime() / 1000)}`);
  }
  if (endDate) {
    queryParams.push(`end-date=${Math.floor(new Date(endDate).getTime() / 1000)}`);
  }
  if (queryParams.length > 0) {
    endpoint += `?${queryParams.join('&')}`;
  }
  
  const data = fetchFromApi(endpoint);
  
  let result = [];
  for (const account of data.accounts) {
    if (accountFilter && account.id !== accountFilter && !account.name.includes(accountFilter)) continue;
    
    for (const t of (account.transactions || [])) {
      result.push({
        accountId: account.id,
        accountName: account.name,
        id: t.id,
        posted: new Date(t.posted * 1000).toISOString().split('T')[0],
        amount: t.amount,
        description: t.description
      });
    }
  }
  
  // Sort by posted date descending
  result.sort((a, b) => new Date(b.posted) - new Date(a.posted));
  console.log(JSON.stringify(result, null, 2));
} else {
  console.error("Unknown action:", action);
  process.exit(1);
}
