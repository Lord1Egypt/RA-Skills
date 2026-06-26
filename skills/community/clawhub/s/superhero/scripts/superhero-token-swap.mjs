#!/usr/bin/env node
// Buy and sell tokens on superhero.com via bonding curve contracts
import { AeSdk, Node, MemoryAccount, formatAmount, AE_AMOUNT_FORMATS, Contract } from '@aeternity/aepp-sdk';
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
const SLIPPAGE_PERCENT = 3n;

function toTokenDecimals(count, denominationDecimals, decimals) {
  return new BigNumber(count.toString())
    .shiftedBy(Number(-denominationDecimals) - Number(-decimals))
    .toFixed();
}

async function initSaleContract(aeSdk, saleAddress) {
  const ACI = JSON.parse(
    fs.readFileSync('./contracts/AffiliationBondingCurveTokenSale.aci.json', 'utf8')
  );
  return await Contract.initialize({ aci: ACI, address: saleAddress, onAccount: aeSdk, onNode: aeSdk.api });
}

async function initTokenContract(aeSdk, tokenAddress) {
  const ACI = JSON.parse(
    fs.readFileSync('./contracts/FungibleTokenFull.aci.json', 'utf8')
  );
  return await Contract.initialize({ aci: ACI, address: tokenAddress, onAccount: aeSdk, onNode: aeSdk.api });
}

async function getTokenDecimals(saleContract, aeSdk) {
  const tokenAddress = await saleContract.token_contract().then(r => r.decodedResult);
  const tokenContract = await initTokenContract(aeSdk, tokenAddress);
  const meta = await tokenContract.meta_info().then(r => r.decodedResult);
  return { decimals: meta.decimals, tokenContract, tokenAddress };
}

async function createOrChangeAllowance(aeSdk, tokenContract, forAccount, amount) {
  const allowance = await tokenContract
    .allowance({ from_account: aeSdk.address, for_account: forAccount })
    .then(r => r.decodedResult)
    .catch(() => undefined);

  if (allowance === undefined) {
    await tokenContract.create_allowance(forAccount, amount);
  } else {
    const change = new BigNumber(amount).minus(allowance.toString()).toFixed();
    await tokenContract.change_allowance(forAccount, change);
  }
}

async function main() {
  const command = process.argv[2] || 'help';

  if (command === 'help') {
    console.log(`
Token Swap Commands:

  buy <sale_address> <amount>
    Buy tokens from a bonding curve

    sale_address   Token sale contract address (ct_...)
    amount         Number of tokens to buy (integer)

  sell <sale_address> <amount>
    Sell tokens back to the bonding curve

    sale_address   Token sale contract address (ct_...)
    amount         Number of tokens to sell (integer)

  price <sale_address> <amount>
    Get the current price for buying tokens (no transaction)

    sale_address   Token sale contract address (ct_...)
    amount         Number of tokens to price

  lookup <token_name_or_address>
    Look up token info from Superhero API (sale address, price, etc.)

Examples:
  node scripts/superhero-token-swap.mjs price ct_abc... 10
  node scripts/superhero-token-swap.mjs buy ct_abc... 5
  node scripts/superhero-token-swap.mjs sell ct_abc... 5
  node scripts/superhero-token-swap.mjs lookup "MyToken"

Note: Slippage is set to ${SLIPPAGE_PERCENT}%. Buy/sell require AE for gas.
`);
    process.exit(0);
  }

  if (command === 'lookup') {
    const query = process.argv[3];
    if (!query) {
      console.error('Usage: node scripts/superhero-token-swap.mjs lookup <token_name_or_address>');
      process.exit(1);
    }
    const url = `https://api.superhero.com/api/tokens/${encodeURIComponent(query)}`;
    const res = await fetch(url);
    if (!res.ok) {
      // Try searching by name in the list
      const listRes = await fetch(`https://api.superhero.com/api/tokens?limit=100`);
      if (listRes.ok) {
        const listData = await listRes.json();
        const matches = (listData.items || listData.data || []).filter(t =>
          t.name?.toLowerCase().includes(query.toLowerCase()) ||
          t.symbol?.toLowerCase().includes(query.toLowerCase())
        );
        if (matches.length > 0) {
          console.log(JSON.stringify(matches.map(t => ({
            name: t.name,
            symbol: t.symbol,
            sale_address: t.sale_address,
            price_ae: t.price,
            market_cap: t.market_cap,
            trending_score: t.trending_score,
          })), null, 2));
          process.exit(0);
        }
      }
      console.error(`Token not found: ${query}`);
      process.exit(1);
    }
    const data = await res.json();
    console.log(JSON.stringify({
      name: data.name,
      symbol: data.symbol,
      sale_address: data.sale_address,
      price_ae: data.price,
      market_cap: data.market_cap,
      holders_count: data.holders_count,
      trending_score: data.trending_score,
    }, null, 2));
    process.exit(0);
  }

  // Commands requiring wallet
  const account = loadAccount();
  const node = new Node(NODE_URL);
  const aeSdk = new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
    accounts: [account],
  });

  const saleAddress = process.argv[3];
  const amount = parseInt(process.argv[4]);
  if (!saleAddress || isNaN(amount) || amount <= 0) {
    console.error(`Usage: node scripts/superhero-token-swap.mjs ${command} <sale_address> <amount>`);
    process.exit(1);
  }

  const saleContract = await initSaleContract(aeSdk, saleAddress);
  const { decimals, tokenContract, tokenAddress } = await getTokenDecimals(saleContract, aeSdk);
  const countTokenDecimals = toTokenDecimals(amount, 0n, decimals);

  switch (command) {
    case 'price': {
      const priceAetto = await saleContract.price(countTokenDecimals).then(r => r.decodedResult);
      const priceAE = formatAmount(priceAetto.toString(), {
        denomination: AE_AMOUNT_FORMATS.AETTOS,
        targetDenomination: AE_AMOUNT_FORMATS.AE,
      });
      console.log(JSON.stringify({
        sale_address: saleAddress,
        amount: amount,
        price_ae: priceAE,
        price_aettos: priceAetto.toString(),
      }));
      break;
    }

    case 'buy': {
      const priceAetto = await saleContract.price(countTokenDecimals).then(r => r.decodedResult);
      const priceWithSlippage = new BigNumber(priceAetto.toString())
        .plus(new BigNumber(priceAetto.toString()).times(SLIPPAGE_PERCENT.toString()).div(100))
        .toFixed(0);

      console.error(`Buying ${amount} tokens for ~${new BigNumber(priceAetto.toString()).dividedBy(1e18).toFixed(6)} AE...`);
      const result = await saleContract.buy(countTokenDecimals, {
        amount: priceWithSlippage,
        omitUnknown: true,
      });

      console.log(JSON.stringify({
        success: true,
        action: 'buy',
        sale_address: saleAddress,
        amount: amount,
        price_aettos: priceAetto.toString(),
        tx_hash: result.hash,
      }));
      break;
    }

    case 'sell': {
      // Create allowance for the sale contract to spend our tokens
      const forAccount = saleAddress.replaceAll('ct_', 'ak_');
      await createOrChangeAllowance(aeSdk, tokenContract, forAccount, countTokenDecimals);

      // Get sell return and apply slippage
      const sellReturn = await saleContract.sell_return(countTokenDecimals).then(r => r.decodedResult);
      const minReturn = new BigNumber(sellReturn.toString())
        .minus(new BigNumber(sellReturn.toString()).times(SLIPPAGE_PERCENT.toString()).div(100))
        .toFixed(0);

      console.error(`Selling ${amount} tokens for ~${new BigNumber(sellReturn.toString()).dividedBy(1e18).toFixed(6)} AE...`);
      const result = await saleContract.sell(countTokenDecimals, minReturn, {
        omitUnknown: true,
      });

      console.log(JSON.stringify({
        success: true,
        action: 'sell',
        sale_address: saleAddress,
        amount: amount,
        return_aettos: sellReturn.toString(),
        tx_hash: result.hash,
      }));
      break;
    }

    default:
      console.error(`Unknown command: ${command}. Run with 'help' for usage.`);
      process.exit(1);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
