#!/usr/bin/env node

/**
 * CLI for YieldFarmPayment Fixed Version
 * Uses the robust transaction manager with retry logic
 * Includes interactive confirmation and dry-run mode for transaction safety
 */

const { yieldFarmPayment } = require('./yield-farm-payment.js');
const { privateKeyToAccount } = require('viem/accounts');
const {
  displayTransactionPreview,
  validateTransaction,
  requestApproval,
  dryRunSimulation,
  closePrompt
} = require('./transaction-confirmation.js');
require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });

function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    mode: 'upfront',  // v1.0 ONLY supports upfront
    amount: null,
    recipient: null,
    collateral: parseFloat(process.env.DEFAULT_COLLATERAL_MULTIPLIER) || 10,
    buffer: parseFloat(process.env.DEFAULT_BUFFER_PERCENTAGE) || 8,
    dryRun: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '--mode':
      case '-m':
        params.mode = args[++i];
        break;
      case '--amount':
      case '-a':
        params.amount = parseFloat(args[++i]);
        break;
      case '--recipient':
      case '-r':
        params.recipient = args[++i];
        break;
      case '--collateral':
      case '-c':
        params.collateral = parseFloat(args[++i]);
        break;
      case '--buffer':
      case '-b':
        params.buffer = parseFloat(args[++i]);
        break;
      case '--dry-run':
        params.dryRun = true;
        break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
      default:
        if (arg.startsWith('--')) {
          console.warn(`⚠️ Unknown option: ${arg}`);
        }
    }
  }

  return params;
}

function printHelp() {
  console.log(`
🌾 YieldFarmPayment CLI - v1.0 (Upfront Mode Only)
   With Transaction Confirmation & Safety Features

USAGE:
  node scripts/cli.js [OPTIONS]

REQUIRED OPTIONS:
  --amount, -a      Amount to pay in USDC (e.g., 0.01)
  --recipient, -r   Recipient Ethereum address

OPTIONAL OPTIONS:
  --mode, -m        Payment mode: upfront ONLY in v1.0 (default: upfront)
  --collateral, -c  Collateral multiplier (e.g., 5 for 5x, default: 10)
  --buffer, -b      Buffer percentage (e.g., 8 for 8%, default: 8)
  --dry-run         Simulate transaction without sending on-chain

EXAMPLES:

  # Test with dry-run first (RECOMMENDED)
  node scripts/cli.js --dry-run --amount 0.1 --recipient 0x... --collateral 5

  # Upfront mode with interactive confirmation
  node scripts/cli.js --amount 0.1 --recipient 0x... --collateral 5 --buffer 8

  

SAFETY FEATURES:
  ✓ Transaction preview before signing
  ✓ Amount validation (max 1000 USDC payment + collateral up to ~21,600 USDC total)
  ✓ Recipient address verification
  ✓ Interactive confirmation ALWAYS required
  ✓ Dry-run mode for testing without on-chain execution
  ✓ Separate final confirmation for mainnet transactions
  ✓ Collateral multiplier limits (3x-20x)
  ✓ Buffer percentage validation (5%-20%)

WORKFLOW:
  1. Run with --dry-run to test parameters
  2. Run without --dry-run to execute real transaction
  3. Review the transaction preview carefully
  4. Confirm amount and recipient
  5. Transaction is sent and broadcasted to Base network

NOTES:
  • v1.0 ONLY supports 'upfront' mode (immediate payment)
  • Minimum collateral multiplier: ${process.env.MIN_COLLATERAL_MULTIPLIER || 3}x
  • Maximum collateral multiplier: ${process.env.MAX_COLLATERAL_MULTIPLIER || 20}x
  • Maximum amount: 1000 USDC
  • Network: ${process.env.BASE_RPC_URL?.includes('sepolia') ? 'Base Sepolia Testnet' : 'Base Mainnet'}
  `);
}

async function main() {
  const params = parseArgs();
  
  if (!params.amount || params.amount <= 0) {
    console.error('❌ Error: --amount is required and must be positive');
    printHelp();
    process.exit(1);
  }
  
  if (!params.recipient || !params.recipient.match(/^0x[a-fA-F0-9]{40}$/)) {
    console.error('❌ Error: --recipient must be a valid Ethereum address');
    printHelp();
    process.exit(1);
  }
  
  console.log('🚀 Starting YieldFarmPayment with Transaction Confirmation...\n');
  
  // Get sender address from PRIVATE_KEY
  let senderAddress = null;
  try {
    const account = privateKeyToAccount(process.env.PRIVATE_KEY);
    senderAddress = account.address;
  } catch (error) {
    console.error('❌ Error: Could not derive address from PRIVATE_KEY in .env');
    process.exit(1);
  }
  
  // Prepare confirmation parameters
  const confirmationParams = {
    amountToPay: params.amount,
    recipientAddress: params.recipient,
    senderAddress,
    collateralMultiplier: params.collateral,
    bufferPercentage: params.buffer,
    rpcUrl: process.env.BASE_RPC_URL,
    estimatedAPY: parseFloat(process.env.ESTIMATED_APY) || 0.03
  };
  
  // Handle dry-run mode
  if (params.dryRun) {
    const result = dryRunSimulation(confirmationParams);
    closePrompt();
    process.exit(result.success ? 0 : 1);
  }
  
  // Request user approval for real transaction (ALWAYS REQUIRED)
  const approved = await requestApproval(confirmationParams);
  closePrompt();
  
  if (!approved) {
    process.exit(1);
  }
  
  // Execute the actual payment
  try {
    const result = await yieldFarmPayment({
      mode: params.mode,
      amountToPay: params.amount,
      recipientAddress: params.recipient,
      collateralMultiplier: params.collateral,
      bufferPercentage: params.buffer
    });
    
    if (result.success) {
      console.log('\n✅ Payment completed successfully!');
      console.log(`📊 Transaction: ${result.transactionHash}`);
      
      // Handle different result structures based on mode
      if (result.dailyYield) {
        console.log(`🔄 Daily yield: ${result.dailyYield} USDC`);
      }
      
      if (result.paymentDurationDays) {
        console.log(`⏰ Estimated payment time: ${result.paymentDurationDays} days`);
      }
      
      if (result.recoveryDays) {
        console.log(`💰 Immediate payment: ${result.immediatePayment || 'sent'} USDC`);
        console.log(`🏦 Recovery collateral: ${result.recoveryCollateral || 'locked'} USDC`);
        console.log(`⏰ Estimated recovery time: ${result.recoveryDays} days`);
      }
      
      if (result.healthFactor) {
        console.log(`🏦 Health factor: ${result.healthFactor.toFixed(2)}`);
      }
      
      if (result.mode) {
        console.log(`🎯 Mode: ${result.mode}`);
      }
      
    } else {
      console.error('\n❌ Payment failed:');
      console.error(`   ${result.error}`);
      process.exit(1);
    }
  } catch (error) {
    console.error('\n❌ Unexpected error:');
    console.error(`   ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { parseArgs, printHelp };