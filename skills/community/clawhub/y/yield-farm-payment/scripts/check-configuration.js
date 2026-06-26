#!/usr/bin/env node

/**
 * Configuration check script for Base Sepolia testing
 */

require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });

function checkConfiguration() {
  console.log('🔧 YieldFarmPayment - Configuration Check\n');
  
  console.log('='.repeat(80));
  console.log('📋 ENVIRONMENT CHECK');
  console.log('='.repeat(80));
  
  // Required variables
  const required = [
    'PRIVATE_KEY',
    'BASE_RPC_URL',
    'AAVE_V3_POOL_ADDRESS',
    'USDC_ADDRESS',
    'AAVE_USDC_TOKEN_ADDRESS'
  ];
  
  let allValid = true;
  
  required.forEach(key => {
    const value = process.env[key];
    
    if (!value || value.trim() === '' || value.includes('TODO:')) {
      console.log(`❌ ${key}: NOT SET or has TODO`);
      allValid = false;
    } else if (value === '0x...' || value === '0x0000000000000000000000000000000000000000') {
      console.log(`❌ ${key}: PLACEHOLDER value`);
      allValid = false;
    } else if (key === 'PRIVATE_KEY') {
      // Hide PRIVATE_KEY completely for security
      console.log(`✅ ${key}: 0x...`);
    } else {
      console.log(`✅ ${key}: ${value.substring(0, 20)}...`);
    }
  });
  
  console.log('\n' + '='.repeat(80));
  console.log('🌐 NETWORK CHECK');
  console.log('='.repeat(80));
  
  const rpcUrl = process.env.BASE_RPC_URL;
  if (rpcUrl && rpcUrl.includes('sepolia')) {
    console.log(`✅ Using TESTNET: ${rpcUrl}`);
    console.log('   • Safe for testing');
    console.log('   • Need testnet funds from faucet');
  } else if (rpcUrl && rpcUrl.includes('mainnet')) {
    console.log(`⚠️ Using MAINNET: ${rpcUrl}`);
    console.log('   • Real funds required');
    console.log('   • Higher risk');
    console.log('   • Start with testnet first');
  } else {
    console.log(`❌ RPC URL unclear: ${rpcUrl}`);
    allValid = false;
  }
  
  console.log('\n' + '='.repeat(80));
  console.log('⚙️ SETTINGS CHECK');
  console.log('='.repeat(80));
  
  const settings = [
    'DEFAULT_COLLATERAL_MULTIPLIER',
    'DEFAULT_BUFFER_PERCENTAGE',
    'MIN_COLLATERAL_MULTIPLIER',
    'MAX_COLLATERAL_MULTIPLIER',
    'MIN_BUFFER_PERCENTAGE',
    'MAX_BUFFER_PERCENTAGE',
    'ESTIMATED_APY'
  ];
  
  settings.forEach(key => {
    const value = process.env[key];
    console.log(`✅ ${key}: ${value}`);
  });
  
  console.log('\n' + '='.repeat(80));
  console.log('🎯 TESTING RECOMMENDATIONS');
  console.log('='.repeat(80));
  
  if (allValid) {
    console.log('\n✅ Configuration appears valid!');
    
    console.log('\nRecommended first test:');
    console.log('node scripts/cli.js --mode standard --amount 1 --recipient 0x... --collateral 5 --buffer 10');
    
    console.log('\nBefore testing:');
    console.log('1. Get ETH testnet: https://sepolia-faucet.pk910.de/');
    console.log('2. Get USDC test: https://faucet.circle.com/ (select Base Sepolia)');
    console.log('3. Verify wallet has funds');
    
  } else {
    console.log('\n❌ Configuration incomplete!');
    
    console.log('\nMissing/placeholder values detected.');
    console.log('Update .env with:');
    console.log('1. Actual contract addresses for Base Sepolia');
    console.log('2. Remove TODO comments');
    console.log('3. Verify private key is valid');
    
    console.log('\nTo find Aave Sepolia addresses:');
    console.log('Check: https://docs.aave.com/developers/deployed-contracts/v3-testnet-addresses');
  }
  
  console.log('\n' + '='.repeat(80));
  console.log('🚀 QUICK VALIDATION COMMAND');
  console.log('='.repeat(80));
  
  console.log('\nTest calculation without transaction:');
  console.log('node scripts/collateral-calculator.js --amount 1 --deadline 90');
  
  console.log('\nTest wallet connectivity:');
  console.log('node scripts/test-wallet.js');
  
  return allValid;
}

// Create wallet test script if needed
function createWalletTest() {
  const fs = require('fs');
  const path = require('path');
  
  const walletTest = `
const { privateKeyToAccount } = require('viem/accounts');
const { createPublicClient, http } = require('viem');
const { base } = require('viem/chains');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

async function testWallet() {
  console.log('🔐 Wallet Connectivity Test');
  
  try {
    const account = privateKeyToAccount(process.env.PRIVATE_KEY);
    console.log('✅ Private key valid');
    console.log('   Address: ' + account.address);
    
    const publicClient = createPublicClient({
      chain: base,
      transport: http(process.env.BASE_RPC_URL)
    });
    
    const balance = await publicClient.getBalance({ address: account.address });
    console.log('✅ RPC connected');
    console.log('   Balance: ' + (balance / 1e18) + ' ETH');
    
    return true;
  } catch (error) {
    console.error('❌ Error: ' + error.message);
    return false;
  }
}

if (require.main === module) {
  testWallet();
}
`;
  
  fs.writeFileSync(path.join(__dirname, 'test-wallet.js'), walletTest);
  console.log('✅ Created wallet test script');
}

// Run if called directly
if (require.main === module) {
  console.log('🔍 Checking YieldFarmPayment Configuration\n');
  
  try {
    const isValid = checkConfiguration();
    
    if (!isValid) {
      console.log('\nCreating additional test scripts...');
      createWalletTest();
    }
    
    console.log('\n' + '='.repeat(80));
    console.log('📊 SUMMARY');
    console.log('='.repeat(80));
    
    if (isValid) {
      console.log('\n✅ Ready for testing!');
      console.log('\nRun: node scripts/test-realistic-payment.js');
    } else {
      console.log('\n❌ Configuration needs updates');
      console.log('\nUpdate .env file before testing');
    }
    
  } catch (error) {
    console.error('\n❌ Check error:', error);
    process.exit(1);
  }
}

module.exports = { checkConfiguration };