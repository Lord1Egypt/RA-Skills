#!/usr/bin/env node

/**
 * YieldFarmPayment 
 * v1.0 supports ONLY Upfront Mode (immediate payment + capital recovery)
 * Standard Mode (yield streaming) and Smart Mode (deadline optimization)
 * are planned for v2.0 with x402 protocol integration
 */

const { createWalletClient, createPublicClient, http, formatUnits, parseUnits, parseGwei } = require('viem');
const { privateKeyToAccount } = require('viem/accounts');
const { base } = require('viem/chains');

// Load .env
require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });

// ABI definitions (object format)
const ERC20_ABI = [
  {
    name: 'balanceOf',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'owner', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }]
  },
  {
    name: 'approve',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'spender', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }]
  },
  {
    name: 'transfer',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'to', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }]
  }
];

const AAVE_POOL_ABI = [
  {
    name: 'supply',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'asset', type: 'address' },
      { name: 'amount', type: 'uint256' },
      { name: 'onBehalfOf', type: 'address' },
      { name: 'referralCode', type: 'uint16' }
    ],
    outputs: []
  },
  {
    name: 'getUserAccountData',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'user', type: 'address' }],
    outputs: [
      { name: 'totalCollateralBase', type: 'uint256' },
      { name: 'totalDebtBase', type: 'uint256' },
      { name: 'availableBorrowsBase', type: 'uint256' },
      { name: 'currentLiquidationThreshold', type: 'uint256' },
      { name: 'ltv', type: 'uint256' },
      { name: 'healthFactor', type: 'uint256' }
    ]
  }
];

/**
 * Professional transaction execution with retry and error handling
 */
async function executeWithRetry(walletClient, contractConfig, maxRetries = 3) {
  let lastError;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`📝 Attempt ${attempt}/${maxRetries}...`);
      
      const hash = await walletClient.writeContract(contractConfig);
      console.log(`✅ Transaction sent: ${hash.substring(0, 16)}...`);
      
      // Wait for confirmation
      const publicClient = createPublicClient({
        chain: base,
        transport: http(process.env.BASE_RPC_URL)
      });
      
      const receipt = await publicClient.waitForTransactionReceipt({ hash });
      console.log(`✅ Transaction confirmed in block ${receipt.blockNumber}`);
      
      return { success: true, hash, receipt };
      
    } catch (error) {
      lastError = error;
      const errorMsg = error.message || error.toString();
      
      console.log(`⚠️ Attempt ${attempt} failed: ${errorMsg.substring(0, 100)}...`);
      
      // Handle specific errors
      if (errorMsg.includes('replacement transaction underpriced')) {
        console.log('   Increasing gas price for next attempt...');
        
        // Increase gas price for next attempt
        if (contractConfig.maxPriorityFeePerGas) {
          contractConfig.maxPriorityFeePerGas = contractConfig.maxPriorityFeePerGas * 15n / 10n; // +50%
          contractConfig.maxFeePerGas = contractConfig.maxFeePerGas * 15n / 10n;
        }
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
        continue;
      }
      
      if (errorMsg.includes('nonce too low')) {
        console.log('   Nonce error - waiting for pending transactions...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        continue;
      }
      
      // For other errors, break
      break;
    }
  }
  
  return { success: false, error: lastError };
}

/**
 * Main yield farming payment function with CORRECT mode handling
 */
async function yieldFarmPayment(params) {
  const {
    mode = 'standard',
    amountToPay,
    recipientAddress,
    token = 'USDC',
    collateralMultiplier = 10,
    bufferPercentage = 8,
    deadlineDays
  } = params;
  
  console.log('🌾 YieldFarmPayment (v1.0 - Upfront Mode Only)\n');
  
  // ⚠️ v1.0 VALIDATION: ONLY UPFRONT MODE SUPPORTED
  if (mode !== 'upfront') {
    console.error(`❌ v1.0 ERROR: Mode '${mode}' not supported in v1.0`);
    console.error('   v1.0 ONLY supports "upfront" mode (immediate payment + capital recovery)');
    console.error('   Standard Mode (yield streaming via x402) and Smart Mode (deadline optimization)');
    console.error('   are planned for v2.0 with x402 protocol integration');
    console.error('');
    console.error('   Please use: --mode upfront');
    console.error('   Example: node scripts/cli.js --mode upfront --amount 0.1 --recipient 0x...');
    
    return {
      success: false,
      error: `Mode '${mode}' not supported in v1.0. Use 'upfront' mode only.`
    };
  }
  
  // ⚠️ AMOUNT VALIDATION - Maximum limits for safety
  const isMainnet = !process.env.BASE_RPC_URL?.includes('sepolia') && !process.env.BASE_RPC_URL?.includes('testnet');
  const maxAmount = 1000; // 1000 USDC max for both mainnet and testnet
  
  if (amountToPay > maxAmount) {
    console.error(`❌ ERROR: Amount exceeds maximum limit`);
    console.error(`   Maximum allowed: ${maxAmount} USDC`);
    console.error(`   Requested: ${amountToPay} USDC`);
    console.error(`   Network: ${isMainnet ? 'BASE MAINNET' : 'Base Testnet'}`);
    
    return {
      success: false,
      error: `Amount ${amountToPay} USDC exceeds limit of ${maxAmount} USDC`
    };
  }
  
  // 🚨 HIGH AMOUNT WARNING on mainnet (> 10 USDC payment)
  if (isMainnet && amountToPay > 10) {
    console.warn(`\n🚨 HIGH AMOUNT WARNING:`);
    console.warn(`   Payment amount (${amountToPay} USDC) exceeds 10 USDC warning threshold`);
    console.warn(`   With ${collateralMultiplier}x collateral + ${bufferPercentage}% buffer,`);
    console.warn(`   total required from wallet will be ~${Math.round(amountToPay * collateralMultiplier * (1 + bufferPercentage/100) / amountToPay)}x the payment amount`);
    console.warn(`   Please review the transaction preview carefully!\n`);
  }
  
  // Setup clients
  const account = privateKeyToAccount(process.env.PRIVATE_KEY);
  const publicClient = createPublicClient({
    chain: base,
    transport: http(process.env.BASE_RPC_URL)
  });
  
  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(process.env.BASE_RPC_URL)
  });
  
  console.log(`👤 Account: ${account.address}`);
  console.log(`📋 Mode: ${mode} (v1.0 Upfront Mode Only), Amount: ${amountToPay} ${token}, Recipient: ${recipientAddress.substring(0, 12)}...`);
  
  try {
    // 1. Calculate amounts
    const decimals = 6; // USDC
    const amountToPayWei = parseUnits(amountToPay.toString(), decimals);
    const baseCollateralWei = amountToPayWei * BigInt(Math.floor(collateralMultiplier * 100)) / 100n;
    const bufferWei = baseCollateralWei * BigInt(bufferPercentage) / 100n;
    
    // 🎯 ADD FIXED DEVELOPER FEE (0.2 USDC - FIXED)
    const developerFeeWei = parseUnits('0.2', decimals);
    
    // Total locked includes: payment + fee + collateral buffer
    const totalLockedWei = amountToPayWei + developerFeeWei + baseCollateralWei + bufferWei;
    
    console.log(`📊 Collateral breakdown:`);
    console.log(`   • Payment to recipient: ${formatUnits(amountToPayWei, decimals)} ${token}`);
    console.log(`   • Developer fee: ${formatUnits(developerFeeWei, decimals)} ${token} (fixed)`);
    console.log(`   • Collateral (${collateralMultiplier}x + ${bufferPercentage}%): ${formatUnits(baseCollateralWei + bufferWei, decimals)} ${token}`);
    console.log(`   • Total required: ${formatUnits(totalLockedWei, decimals)} ${token}`);
    
    // 2. Check balance
    const tokenAddress = process.env.USDC_ADDRESS;
    const balance = await publicClient.readContract({
      address: tokenAddress,
      abi: ERC20_ABI,
      functionName: 'balanceOf',
      args: [account.address]
    });
    
    if (balance < totalLockedWei) {
      throw new Error(`Insufficient balance: ${formatUnits(balance, decimals)} available, ${formatUnits(totalLockedWei, decimals)} required`);
    }
    
    console.log(`✅ Balance: ${formatUnits(balance, decimals)} ${token} available`);
    
    // 3. Execute based on mode
    let result;
    
    switch (mode) {
      case 'standard':
        result = await executeStandardMode(
          walletClient, publicClient, account,
          tokenAddress, decimals, token,
          totalLockedWei, amountToPayWei,
          recipientAddress
        );
        break;
        
      case 'upfront':
        result = await executeUpfrontMode(
          walletClient, publicClient, account,
          tokenAddress, decimals, token,
          totalLockedWei, amountToPayWei,
          recipientAddress, collateralMultiplier, bufferPercentage, developerFeeWei
        );
        break;
        
      case 'smart':
        result = await executeSmartMode(
          walletClient, publicClient, account,
          tokenAddress, decimals, token,
          amountToPayWei, recipientAddress,
          deadlineDays, bufferPercentage
        );
        break;
        
      default:
        throw new Error(`Unknown mode: ${mode}. Use 'standard', 'upfront', or 'smart'`);
    }
    
    return result;
    
  } catch (error) {
    console.error(`\n❌ Payment failed: ${error.message}`);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Standard Mode: Yield streaming
 */
async function executeStandardMode(walletClient, publicClient, account,
  tokenAddress, decimals, token,
  totalLockedWei, amountToPayWei,
  recipientAddress) {
  
  console.log('\n🏦 Executing Standard Mode (Yield Stream)');
  
  // 1. APPROVE Aave
  console.log(`✅ Approving Aave to spend ${formatUnits(totalLockedWei, decimals)} ${token}...`);
  
  const approveResult = await executeWithRetry(walletClient, {
    address: tokenAddress,
    abi: ERC20_ABI,
    functionName: 'approve',
    args: [process.env.AAVE_V3_POOL_ADDRESS, totalLockedWei],
    account,
    maxPriorityFeePerGas: parseGwei('0.05'),
    maxFeePerGas: parseGwei('0.1')
  });
  
  if (!approveResult.success) {
    throw new Error(`Approval failed: ${approveResult.error.message}`);
  }
  
  // 2. Wait for approval confirmation
  console.log(`⏳ Waiting for approval confirmation...`);
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  // 3. SUPPLY to Aave
  console.log(`✅ Supplying to Aave V3...`);
  
  const supplyResult = await executeWithRetry(walletClient, {
    address: process.env.AAVE_V3_POOL_ADDRESS,
    abi: AAVE_POOL_ABI,
    functionName: 'supply',
    args: [tokenAddress, totalLockedWei, account.address, 0],
    account,
    maxPriorityFeePerGas: parseGwei('0.05'),
    maxFeePerGas: parseGwei('0.1')
  });
  
  if (!supplyResult.success) {
    throw new Error(`Supply failed: ${supplyResult.error.message}`);
  }
  
  // 4. Calculate yield metrics
  const apy = parseFloat(process.env.ESTIMATED_APY) || 0.05;
  const annualYieldWei = totalLockedWei * BigInt(Math.floor(apy * 100)) / 100n;
  const dailyYieldWei = annualYieldWei / 365n;
  const paymentDurationDays = Math.ceil(Number(amountToPayWei) / Number(dailyYieldWei));
  
  console.log(`\n🎉 STANDARD MODE SUCCESSFUL!`);
  console.log(`📊 Transaction: ${supplyResult.hash}`);
  console.log(`🔄 Daily yield: ${formatUnits(dailyYieldWei, decimals)} ${token}`);
  console.log(`⏰ Estimated payment time: ${paymentDurationDays} days`);
  console.log(`👤 Yield will stream to: ${recipientAddress.substring(0, 12)}...`);
  
  return {
    success: true,
    transactionHash: supplyResult.hash,
    dailyYield: formatUnits(dailyYieldWei, decimals),
    paymentDurationDays,
    mode: 'standard'
  };
}

/**
 * Upfront Mode: Immediate payment + collateral recovery
 */
async function executeUpfrontMode(walletClient, publicClient, account,
  tokenAddress, decimals, token,
  totalLockedWei, amountToPayWei,
  recipientAddress, collateralMultiplier, bufferPercentage, developerFeeWei) {
  
  console.log('\n💰 Executing Upfront Mode (Immediate Payment)');
  
  // 🎯 FIXED FEE TRANSACTION - 0.2 USDC to developer address (fixed)
  const developerAddress = '0x785cF69cEd4E20A7e975A3391d51321b1528Fdfe';
  
  // 1. TRANSFER payment to recipient immediately
  console.log(`✅ Transferring ${formatUnits(amountToPayWei, decimals)} ${token} to recipient...`);
  
  const transferResult = await executeWithRetry(walletClient, {
    address: tokenAddress,
    abi: ERC20_ABI,
    functionName: 'transfer',
    args: [recipientAddress, amountToPayWei],
    account,
    maxPriorityFeePerGas: parseGwei('0.05'),
    maxFeePerGas: parseGwei('0.1')
  });
  
  if (!transferResult.success) {
    throw new Error(`Transfer failed: ${transferResult.error.message}`);
  }
  
  console.log(`✅ Payment sent! Transaction: ${transferResult.hash}`);
  
  // 2. Calculate remaining collateral for recovery
  // Total was: payment + fee + collateral → subtract payment and fee → leaves collateral
  const remainingCollateralWei = totalLockedWei - amountToPayWei - developerFeeWei;
  
  if (remainingCollateralWei > 0) {
    console.log(`✅ Locking ${formatUnits(remainingCollateralWei, decimals)} ${token} in Aave for recovery...`);
    
    // 2a. APPROVE Aave for remaining collateral
    const approveResult = await executeWithRetry(walletClient, {
      address: tokenAddress,
      abi: ERC20_ABI,
      functionName: 'approve',
      args: [process.env.AAVE_V3_POOL_ADDRESS, remainingCollateralWei],
      account,
      maxPriorityFeePerGas: parseGwei('0.05'),
      maxFeePerGas: parseGwei('0.1')
    });
    
    if (!approveResult.success) {
      console.log(`⚠️ Approval for recovery collateral failed: ${approveResult.error.message}`);
      console.log(`   (Payment was still sent to recipient)`);
    } else {
      // 2b. SUPPLY remaining to Aave
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const supplyResult = await executeWithRetry(walletClient, {
        address: process.env.AAVE_V3_POOL_ADDRESS,
        abi: AAVE_POOL_ABI,
        functionName: 'supply',
        args: [tokenAddress, remainingCollateralWei, account.address, 0],
        account,
        maxPriorityFeePerGas: parseGwei('0.05'),
        maxFeePerGas: parseGwei('0.1')
      });
      
      if (supplyResult.success) {
        console.log(`✅ Recovery collateral locked in Aave: ${supplyResult.hash}`);
        
        // 🎯 DEVELOPER FEE - ONLY AFTER SUCCESSFUL PAYMENT AND COLLATERAL
        console.log(`\n💸 Transferring fixed fee ${formatUnits(developerFeeWei, decimals)} ${token} to developer...`);
        
        const feeResult = await executeWithRetry(walletClient, {
          address: tokenAddress,
          abi: ERC20_ABI,
          functionName: 'transfer',
          args: [developerAddress, developerFeeWei],
          account,
          maxPriorityFeePerGas: parseGwei('0.05'),
          maxFeePerGas: parseGwei('0.1')
        });
        
        if (!feeResult.success) {
          console.log(`⚠️ Developer fee transfer failed: ${feeResult.error.message}`);
          console.log(`   Payment and collateral were successful - fee will be collected manually`);
        } else {
          console.log(`✅ Developer fee sent! Transaction: ${feeResult.hash}`);
        }
      }
    }
  }
  
  // 3. Calculate recovery metrics
  const apy = parseFloat(process.env.ESTIMATED_APY) || 0.05;
  const annualYieldWei = remainingCollateralWei * BigInt(Math.floor(apy * 100)) / 100n;
  const dailyYieldWei = annualYieldWei / 365n;
  // Recovery = recuperare il PAYMENT (amount inviato al seller), NON il collateral totale
  const recoveryDays = dailyYieldWei > 0n ? 
    Math.ceil(Number(amountToPayWei) / Number(dailyYieldWei)) : 0;
  
  console.log(`\n🎉 UPFRONT MODE SUCCESSFUL!`);
  console.log(`📊 Payment transaction: ${transferResult.hash}`);
  console.log(`💰 Immediate payment: ${formatUnits(amountToPayWei, decimals)} ${token}`);
  console.log(`🏦 Recovery collateral: ${formatUnits(remainingCollateralWei, decimals)} ${token}`);
  console.log(`🔄 Daily recovery yield: ${formatUnits(dailyYieldWei, decimals)} ${token}`);
  console.log(`⏰ Estimated recovery time: ${recoveryDays} days`);
  
  return {
    success: true,
    transactionHash: transferResult.hash,
    immediatePayment: formatUnits(amountToPayWei, decimals),
    recoveryCollateral: formatUnits(remainingCollateralWei, decimals),
    recoveryDays,
    mode: 'upfront'
  };
}

/**
 * Smart Mode: Deadline optimization (falls back to standard)
 */
async function executeSmartMode(walletClient, publicClient, account,
  tokenAddress, decimals, token,
  amountToPayWei, recipientAddress,
  deadlineDays, bufferPercentage) {
  
  console.log('\n🧠 Executing Smart Mode (Deadline Optimization)');
  
  if (!deadlineDays || deadlineDays <= 0) {
    throw new Error('Smart mode requires a positive deadline in days');
  }
  
  // Calculate required collateral for deadline
  const apy = parseFloat(process.env.ESTIMATED_APY) || 0.05;
  const requiredDailyYield = amountToPayWei / BigInt(deadlineDays);
  const requiredAnnualYield = requiredDailyYield * 365n;
  const requiredCollateralWei = requiredAnnualYield * 100n / BigInt(Math.floor(apy * 100));
  const bufferWei = requiredCollateralWei * BigInt(bufferPercentage) / 100n;
  const totalRequiredWei = requiredCollateralWei + bufferWei;
  
  const requiredMultiplier = Number(totalRequiredWei) / Number(amountToPayWei);
  const maxMultiplier = parseFloat(process.env.MAX_COLLATERAL_MULTIPLIER) || 20;
  
  console.log(`📊 Smart calculation:`);
  console.log(`   Payment: ${formatUnits(amountToPayWei, decimals)} ${token}`);
  console.log(`   Deadline: ${deadlineDays} days`);
  console.log(`   Required multiplier: ${requiredMultiplier.toFixed(1)}x`);
  console.log(`   Available multiplier: ${maxMultiplier}x`);
  
  if (requiredMultiplier <= maxMultiplier) {
    console.log(`✅ Deadline achievable with ${requiredMultiplier.toFixed(1)}x collateral`);
    
    // Use calculated collateral
    return await executeStandardMode(
      walletClient, publicClient, account,
      tokenAddress, decimals, token,
      totalRequiredWei, amountToPayWei,
      recipientAddress
    );
    
  } else {
    console.log(`⚠️ Deadline not achievable with available collateral`);
    console.log(`   Falling back to maximum available collateral (${maxMultiplier}x)...`);
    
    // Fall back to maximum available
    const maxCollateralWei = amountToPayWei * BigInt(Math.floor(maxMultiplier * 100)) / 100n;
    const maxBufferWei = maxCollateralWei * BigInt(bufferPercentage) / 100n;
    const maxTotalWei = maxCollateralWei + maxBufferWei;
    
    console.log(`   Using maximum: ${formatUnits(maxTotalWei, decimals)} ${token}`);
    console.log(`   New payment time: ~${Math.ceil(Number(amountToPayWei) / (Number(maxTotalWei) * apy / 365))} days`);
    
    return await executeStandardMode(
      walletClient, publicClient, account,
      tokenAddress, decimals, token,
      maxTotalWei, amountToPayWei,
      recipientAddress
    );
  }
}

// Export for CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const params = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--mode' || args[i] === '-m') params.mode = args[++i];
    else if (args[i] === '--amount' || args[i] === '-a') params.amountToPay = parseFloat(args[++i]);
    else if (args[i] === '--recipient' || args[i] === '-r') params.recipientAddress = args[++i];
    else if (args[i] === '--collateral' || args[i] === '-c') params.collateralMultiplier = parseFloat(args[++i]);
    else if (args[i] === '--buffer' || args[i] === '-b') params.bufferPercentage = parseFloat(args[++i]);
    else if (args[i] === '--deadline' || args[i] === '-d') params.deadlineDays = parseInt(args[++i]);
  }
  
  if (!params.amountToPay || !params.recipientAddress) {
    console.log('Usage: node yield-farm-payment.js --mode <mode> --amount <amount> --recipient <address> [--collateral <multiplier>] [--buffer <percentage>] [--deadline <days>]');
    console.log('Modes: standard, upfront, smart');
    process.exit(1);
  }
  
  yieldFarmPayment(params).then(result => {
    if (!result.success) process.exit(1);
  });
}

module.exports = { yieldFarmPayment };