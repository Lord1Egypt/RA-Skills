#!/usr/bin/env node
// Create a token on superhero.com via the CommunityFactory contract
// This creates a new bonding-curve token (BCTSL token)
import { AeSdk, Node, MemoryAccount, Contract } from '@aeternity/aepp-sdk';
import fs from 'fs';
import BigNumber from 'bignumber.js';

const NODE_URL = 'https://mainnet.aeternity.io';

function loadAccount() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey);
}
const FACTORY_ADDRESS = 'ct_25cqTw85wkF5cbcozmHHUCuybnfH9WaRZXSgEcNNXG9LsCJWTN';

// Bonding curve constants (matches superhero-app frontend)
const BC_A = 0.001;
const BC_K = 0.00000001;
const BC_C = 0.0009999;
const DECIMALS = new BigNumber(10).pow(18);

function calculateTokensFromAE(aeAmount) {
  if (aeAmount <= 0) return new BigNumber(0);
  const f = (x) => BC_A * Math.exp(BC_K * x) - BC_C;
  const priceInDecimals = aeAmount; // AE amount is the price in whole-unit decimals
  let low = 0, high = 1e12, mid = 0;
  for (let i = 0; i < 1000; i++) {
    mid = (low + high) / 2;
    let sum = 0.5 * (f(0) + f(mid));
    const n = 100, h = mid / n;
    for (let j = 1; j < n; j++) sum += f(j * h);
    const integral = sum * h;
    if (Math.abs(integral - priceInDecimals) < 1e-3) break;
    if (integral < priceInDecimals) low = mid;
    else high = mid;
  }
  return new BigNumber(mid);
}

async function main() {
  const command = process.argv[2] || 'help';

  if (command === 'help') {
    console.log(`
Token Creation Commands:

  create <name> [buy_ae]
    Create a new bonding-curve token in the global Superhero collection.
    The collection is fetched automatically from the Superhero API.

    name     Token name (uppercase A-Z, digits 0-9, dash; max 20 chars)
    buy_ae   AE to spend on initial buy at creation (default: 0, no buy)
             The contract will receive this amount with 5% buffer.

  check <name>
    Check if a token already exists in the global collection.
    Also shows allowed characters and max name length.

  info <sale_address>
    Get info about an existing token by its sale address

Examples:
  node scripts/superhero-token-create.mjs create "MYTOKEN" 0.1
  node scripts/superhero-token-create.mjs check "MYTOKEN"

Note: Requires AE in wallet for gas. Initial buy is optional but establishes
      early liquidity and gives you an initial position at creation price.
`);
    process.exit(0);
  }

  const account = loadAccount();
  const node = new Node(NODE_URL);
  const aeSdk = new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
    accounts: [account],
  });

  const COMMUNITY_FACTORY_ACI = JSON.parse(
    fs.readFileSync('./contracts/CommunityFactory.aci.json', 'utf8')
  );

  const factory = await Contract.initialize({
    address: FACTORY_ADDRESS,
    aci: COMMUNITY_FACTORY_ACI,
    onAccount: aeSdk,
    onNode: aeSdk.api,
  });

  switch (command) {
    case 'create': {
      const tokenName = process.argv[3];
      const buyAe = parseFloat(process.argv[4]) || 0;

      if (!tokenName) {
        console.error('Usage: node scripts/superhero-token-create.mjs create <name> [buy_ae]');
        process.exit(1);
      }

      // Check balance first
      const balanceAetto = await aeSdk.getBalance(account.address);
      const balanceAe = new BigNumber(balanceAetto.toString()).dividedBy(1e18);
      if (buyAe > 0 && balanceAe.lt(buyAe + 0.01)) {
        console.error(JSON.stringify({ error: 'Insufficient balance', balance_ae: balanceAe.toFixed(4), required_ae: (buyAe + 0.01).toFixed(4) }));
        process.exit(1);
      }

      // Fetch the global collection from Superhero API
      const factorySchema = await fetch('https://api.superhero.com/api/factory').then(r => r.json());
      const collectionId = Object.values(factorySchema.collections)[0]?.id;
      if (!collectionId) throw new Error('Could not get collection from Superhero factory API');

      // Check if token already exists
      const exists = await factory.has_community(collectionId, tokenName)
        .then(res => res.decodedResult);
      if (exists) {
        console.error(JSON.stringify({ error: 'Token already exists', collection: collectionId, name: tokenName }));
        process.exit(1);
      }

      // Calculate initial buy: use on-chain bonding curve for accurate price
      let initialBuyTokenDecimals = '0';
      let initialBuyPriceAetto = '0';
      let tokenCount = new BigNumber(0);
      if (buyAe > 0) {
        const BONDING_CURVE_ACI = JSON.parse(fs.readFileSync('./contracts/BondingCurve.aci.json', 'utf8'));
        const bondingCurveAddress = await factory.bonding_curve().then(res => res.decodedResult);
        const bondingCurve = await Contract.initialize({
          address: bondingCurveAddress,
          aci: BONDING_CURVE_ACI,
          onAccount: aeSdk,
          onNode: aeSdk.api,
        });
        // Use client-side math to estimate token count, then ask on-chain for exact price
        tokenCount = calculateTokensFromAE(buyAe);
        const tokenDecimals = await bondingCurve.supported_decimals().then(res => res.decodedResult);
        initialBuyTokenDecimals = tokenCount.multipliedBy(new BigNumber(10).pow(Number(tokenDecimals))).toFixed(0);
        // Get actual on-chain price for that token count, then add 5% buffer
        const onChainPrice = await bondingCurve.calculate_buy_price(0n, BigInt(initialBuyTokenDecimals))
          .then(res => res.decodedResult);
        initialBuyPriceAetto = new BigNumber(onChainPrice.toString())
          .multipliedBy(1.05)
          .toFixed(0, BigNumber.ROUND_CEIL);
      }

      console.error(`Creating token "${tokenName}" in collection "${collectionId}"...`);
      console.error(`Wallet balance: ${balanceAe.toFixed(4)} AE`);
      if (buyAe > 0) {
        console.error(`Initial buy: ~${tokenCount.toFixed(2)} tokens for ${buyAe} AE (sending ${new BigNumber(initialBuyPriceAetto).dividedBy(1e18).toFixed(4)} AE with 5% buffer)`);
      } else {
        console.error('No initial buy — token will be created with zero supply.');
      }

      const metaInfoMap = new Map();
      const result = await factory.create_community(
        collectionId,
        tokenName,
        BigInt(initialBuyTokenDecimals),
        false, // is_private
        metaInfoMap,
        { amount: initialBuyPriceAetto },
      );

      const [daoAddress, tokenSaleAddress, communityManagementAddress] = result.decodedResult;

      console.log(JSON.stringify({
        success: true,
        token_name: tokenName,
        collection: collectionId,
        sale_address: tokenSaleAddress,
        dao_address: daoAddress,
        community_management_address: communityManagementAddress,
        initial_buy_ae: buyAe,
        estimated_tokens: tokenCount.toFixed(2),
        tx_hash: result.hash,
      }));
      break;
    }

    case 'check': {
      const name = process.argv[3];
      if (!name) {
        console.error('Usage: node scripts/superhero-token-create.mjs check <name>');
        process.exit(1);
      }
      // Fetch collection from Superhero API
      const factorySchema = await fetch('https://api.superhero.com/api/factory').then(r => r.json());
      const collection = Object.values(factorySchema.collections)[0];
      if (!collection) throw new Error('Could not get collection from Superhero factory API');

      const exists = await factory.has_community(collection.id, name).then(res => res.decodedResult);
      console.log(JSON.stringify({
        collection: collection.id,
        name,
        exists,
        allowed_name_length: collection.allowed_name_length,
        allowed_chars: 'A-Z, 0-9, - (dash)',
      }));
      break;
    }

    case 'info': {
      const saleAddress = process.argv[3];
      if (!saleAddress) {
        console.error('Usage: node scripts/superhero-token-create.mjs info <sale_address>');
        process.exit(1);
      }
      const url = `https://api.superhero.com/api/tokens/${encodeURIComponent(saleAddress)}`;
      const res = await fetch(url);
      if (!res.ok) {
        console.error(`API error: ${res.status}`);
        process.exit(1);
      }
      const data = await res.json();
      console.log(JSON.stringify(data, null, 2));
      break;
    }
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
