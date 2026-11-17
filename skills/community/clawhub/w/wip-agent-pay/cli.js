#!/usr/bin/env node
// wip-pay CLI
// Your agent's wallet.
//
// Commands:
//   wip-pay pay <url>                  Pay for paywalled content
//   wip-pay fund <amount>              Fund wallet (Apple Pay)
//   wip-pay balance                    Check wallet balance
//   wip-pay history                    Transaction history
//   wip-pay budget                     View/set spending limits
//   wip-pay <amount> <service> [note]  Mint one-time URL
//
// Default: Pool Mode (Apple Pay per transaction, Parker's float)
// --wallet=cdp or --wallet=privy: Path 1 (self-custody, instant)

import { argv } from 'node:process';
import { pay, fund, mint, balance, history, budget } from './providers/index.js';

const args = argv.slice(2);
const command = args[0];

// --- Help ---
if (args.includes('--help') || args.length === 0) {
  console.log('\n  wip-pay ... your agent\'s wallet');
  console.log('\n  Commands:');
  console.log('    wip-pay pay <url>                  Pay for paywalled content');
  console.log('    wip-pay fund <amount>              Fund wallet (Apple Pay)');
  console.log('    wip-pay balance                    Check wallet balance');
  console.log('    wip-pay history                    Transaction history');
  console.log('    wip-pay budget                     View spending limits');
  console.log('    wip-pay budget set <daily> [perTx] Set spending limits');
  console.log('    wip-pay <amount> <service> [note]  Mint one-time URL');
  console.log('\n  Options:');
  console.log('    --wallet=cdp     Use your CDP wallet (instant, no Apple Pay)');
  console.log('    --wallet=privy   Use your Privy wallet (instant, no Apple Pay)');
  console.log('    (no flag)        Pool Mode: Apple Pay per transaction');
  console.log('\n  Pool Mode pricing:');
  console.log('    x402 price + Stripe fees + $0.25 flat fee');
  console.log('    Max $25 per transaction. Over $25 requires your own wallet.');
  console.log('\n  Examples:');
  console.log('    wip-pay pay https://morning-stew.../v1/issues/MS-3');
  console.log('    wip-pay pay https://morning-stew.../v1/issues/MS-3 --wallet=cdp');
  console.log('    wip-pay fund 10');
  console.log('    wip-pay balance');
  console.log('    wip-pay history');
  console.log('    wip-pay budget set 5.00 1.00');
  console.log('    wip-pay 0.10 morning-stew "MS-#8"');
  console.log('\n  Setup:');
  console.log('    See SETUP.md for configuration.\n');
  process.exit(0);
}

// Parse flags
const walletFlag = args.find(a => a.startsWith('--wallet='));
const wallet = walletFlag ? walletFlag.split('=')[1] : undefined; // undefined = Pool Mode
const cleanArgs = args.filter(a => !a.startsWith('--'));

// --- Pay ---
if (command === 'pay') {
  const url = cleanArgs[1];
  if (!url) {
    console.error('  Error: url is required. Usage: wip-pay pay <url>');
    process.exit(1);
  }

  const result = await pay(url, { wallet });

  // Path 1: wallet-signed payment (instant)
  if (result.success && !result.needsPayment) {
    if (result.free) {
      console.log(`\n  Content is free. No payment needed.\n`);
    } else {
      console.log(`\n  Paid: $${result.amount}`);
      console.log(`  Service: ${result.service}`);
      if (result.txHash) console.log(`  Tx: ${result.txHash}`);
      console.log();
    }
  }
  // Pool Mode: needs Apple Pay
  else if (result.success && result.needsPayment) {
    const p = result.pricing;
    console.log(`\n  x402 price:    $${p.x402Amount}`);
    console.log(`  Our fee:       $${p.poolFee}`);
    console.log(`  Stripe fee:    $${p.stripeFee}`);
    console.log(`  Total charge:  $${p.totalCharge}`);
    console.log(`  Service: ${result.service}`);
    console.log(`\n  Opening Apple Pay checkout...`);

    // Open checkout in browser
    try {
      const { execSync } = await import('node:child_process');
      execSync(`open "${result.checkoutUrl}"`, { stdio: 'ignore' });
      console.log('  (Opened in your browser)');
    } catch {
      console.log(`  Open this URL to pay: ${result.checkoutUrl}`);
    }

    // Wait for payment confirmation
    console.log('  Waiting for payment...\n');
    const { waitForPayment } = await import('./providers/passthrough.js');
    const confirmation = await waitForPayment(result.paymentId);

    if (confirmation.success) {
      console.log(`  Paid. Content received.\n`);
    } else {
      console.error(`  ${confirmation.error || 'Payment not completed.'}\n`);
      process.exit(1);
    }
  }
  // Over pool limit
  else if (result.overPoolLimit) {
    console.log(`\n  This costs $${result.amount}. That exceeds the $${result.poolMax} pool limit.`);
    console.log(`  Use your own wallet: wip-pay pay ${url} --wallet=cdp`);
    console.log(`  Or set up a user wallet: see SETUP.md\n`);
    process.exit(1);
  }
  // Error
  else {
    console.error(`\n  Payment failed: ${result.error || 'unknown error'}\n`);
    process.exit(1);
  }
}

// --- Fund (Apple Pay) ---
else if (command === 'fund') {
  const amount = parseFloat(cleanArgs[1]);
  if (isNaN(amount) || amount <= 0) {
    console.error('  Error: amount must be a positive number. Usage: wip-pay fund <amount>');
    process.exit(1);
  }

  const result = await fund(amount, { wallet });

  if (result.success) {
    console.log(`\n  Checkout ready. Open this URL to fund your wallet:`);
    console.log(`  ${result.checkoutUrl}`);
    console.log(`\n  Amount: $${result.amount}`);
    console.log(`  Wallet: ${result.wallet}\n`);

    // Try to open in browser
    try {
      const { execSync } = await import('node:child_process');
      execSync(`open "${result.checkoutUrl}"`, { stdio: 'ignore' });
      console.log('  (Opened in your browser)\n');
    } catch {
      // Not on macOS or open failed
    }
  } else {
    console.error(`\n  Funding failed: ${result.error || 'unknown error'}\n`);
    process.exit(1);
  }
}

// --- Balance ---
else if (command === 'balance') {
  const result = await balance({ wallet });

  if (result.error) {
    console.error(`\n  ${result.error}\n`);
    process.exit(1);
  }

  console.log(`\n  Wallet: ${wallet || 'pool'}`);
  console.log(`  Balance: $${result.balance || '0.00'}`);
  if (result.address) console.log(`  Address: ${result.address}`);
  console.log();
}

// --- History ---
else if (command === 'history') {
  const limit = parseInt(cleanArgs[1]) || 20;
  const result = await history({ wallet, limit });

  if (result.error) {
    console.error(`\n  ${result.error}\n`);
    process.exit(1);
  }

  console.log(`\n  Wallet: ${wallet || 'pool'}`);
  console.log(`  Recent transactions:\n`);

  if (!result.transactions || result.transactions.length === 0) {
    console.log('  No transactions yet.\n');
  } else {
    for (const tx of result.transactions) {
      const dir = tx.type === 'fund' ? '+' : '-';
      const date = new Date(tx.timestamp).toLocaleString();
      console.log(`  ${dir}$${tx.amount}  ${tx.service || tx.type}  ${date}`);
      if (tx.note) console.log(`    ${tx.note}`);
    }
    console.log();
  }
}

// --- Budget ---
else if (command === 'budget') {
  const subcommand = cleanArgs[1];

  if (subcommand === 'set') {
    const daily = parseFloat(cleanArgs[2]);
    const perTx = cleanArgs[3] ? parseFloat(cleanArgs[3]) : undefined;

    if (isNaN(daily) || daily <= 0) {
      console.error('  Error: daily limit required. Usage: wip-pay budget set <daily> [perTx]');
      process.exit(1);
    }

    const result = await budget({ wallet, daily, perTx });

    if (result.error) {
      console.error(`\n  ${result.error}\n`);
      process.exit(1);
    }

    console.log(`\n  Budget updated:`);
    console.log(`  Daily limit: $${result.daily}`);
    if (result.perTx) console.log(`  Per-transaction limit: $${result.perTx}`);
    console.log();
  } else {
    // View current budget
    const result = await budget({ wallet });

    if (result.error) {
      console.error(`\n  ${result.error}\n`);
      process.exit(1);
    }

    console.log(`\n  Wallet: ${wallet || 'pool'}`);
    console.log(`  Daily limit: $${result.daily || 'none'}`);
    console.log(`  Per-transaction limit: $${result.perTx || 'none'}`);
    console.log(`  Spent today: $${result.spentToday || '0.00'}`);
    console.log(`  Remaining today: $${result.remainingToday || result.daily || 'unlimited'}`);
    console.log();
  }
}

// --- Mint one-time URL (existing Mode B) ---
else {
  const amount = parseFloat(cleanArgs[0]);
  const service = cleanArgs[1];
  const note = cleanArgs[2] || '';

  if (isNaN(amount) || amount <= 0) {
    console.error('  Error: amount must be a positive number');
    process.exit(1);
  }
  if (!service) {
    console.error('  Error: service is required. Usage: wip-pay <amount> <service> [note]');
    process.exit(1);
  }

  const result = await mint(amount, service, note);

  if (result.success) {
    if (result.demo) {
      console.log(`  Demo URL (not real): ${result.url}\n`);
    } else {
      console.log(`\n  One-time URL (paste this back to your agent):`);
      console.log(`  ${result.url}\n`);
    }
  } else {
    console.error(`\n  Payment failed: ${result.error || 'unknown error'}\n`);
    process.exit(1);
  }
}
