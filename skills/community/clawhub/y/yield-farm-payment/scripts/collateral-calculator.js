#!/usr/bin/env node

/**
 * Collateral Calculator Utility
 * Calculates optimal collateral multiplier for deadline-based payments
 */

const { parseUnits, formatUnits } = require('viem');

/**
 * Calculate optimal collateral for deadline
 */
function calculateOptimalCollateral({
  amountToPay,
  deadlineDays,
  bufferPercentage = 8,
  estimatedAPY = 0.05,
  token = 'USDC'
}) {
  console.log('🧮 Collateral Optimization Calculator\n');
  
  // Validate inputs
  if (!amountToPay || amountToPay <= 0) {
    throw new Error('amountToPay must be positive');
  }
  if (!deadlineDays || deadlineDays <= 0) {
    throw new Error('deadlineDays must be positive');
  }
  if (bufferPercentage < 3 || bufferPercentage > 20) {
    throw new Error('bufferPercentage must be between 3% and 20%');
  }
  
  const decimals = token === 'USDC' ? 6 : 6;
  const amountToPayWei = parseUnits(amountToPay.toString(), decimals);
  
  // Calculate required daily yield to meet deadline
  const requiredDailyYield = Number(formatUnits(amountToPayWei, decimals)) / deadlineDays;
  
  // Calculate required capital to generate that daily yield
  const dailyRate = estimatedAPY / 365;
  const requiredCapital = requiredDailyYield / dailyRate;
  
  // Calculate collateral multiplier
  const collateralMultiplier = requiredCapital / amountToPay;
  
  // Apply buffer
  const bufferMultiplier = 1 + bufferPercentage / 100;
  const totalCapitalRequired = requiredCapital * bufferMultiplier;
  const totalLockedWei = parseUnits(totalCapitalRequired.toString(), decimals);
  
  // Calculate actual payment time with buffer
  const actualDailyYield = totalCapitalRequired * estimatedAPY / 365;
  const actualPaymentDays = amountToPay / actualDailyYield;
  const daysBeforeDeadline = deadlineDays - actualPaymentDays;
  
  // Round to reasonable values
  const roundedMultiplier = Math.ceil(collateralMultiplier * 10) / 10; // Round to 1 decimal
  const minMultiplier = process.env.MIN_COLLATERAL_MULTIPLIER || 3;
  const maxMultiplier = process.env.MAX_COLLATERAL_MULTIPLIER || 50;
  
  let finalMultiplier = Math.max(minMultiplier, roundedMultiplier);
  finalMultiplier = Math.min(maxMultiplier, finalMultiplier);
  
  // Recalculate with final multiplier
  const finalCapitalRequired = amountToPay * finalMultiplier;
  const finalBufferAmount = finalCapitalRequired * bufferPercentage / 100;
  const finalTotalLocked = finalCapitalRequired + finalBufferAmount;
  
  const finalDailyYield = finalTotalLocked * estimatedAPY / 365;
  const finalPaymentDays = amountToPay / finalDailyYield;
  const finalDaysBeforeDeadline = deadlineDays - finalPaymentDays;
  
  console.log('📊 Input Parameters:');
  console.log(`   Payment amount: ${amountToPay} ${token}`);
  console.log(`   Deadline: ${deadlineDays} days (${(deadlineDays/30).toFixed(1)} months)`);
  console.log(`   Buffer: ${bufferPercentage}%`);
  console.log(`   Estimated APY: ${(estimatedAPY * 100).toFixed(2)}%`);
  console.log('');
  
  console.log('🔍 Calculation Results:');
  console.log(`   Required daily yield: ${requiredDailyYield.toFixed(4)} ${token}/day`);
  console.log(`   Capital needed (no buffer): ${requiredCapital.toFixed(2)} ${token}`);
  console.log(`   Theoretical multiplier: ${collateralMultiplier.toFixed(1)}x`);
  console.log('');
  
  console.log('🎯 Optimized Configuration:');
  console.log(`   Collateral multiplier: ${finalMultiplier.toFixed(1)}x`);
  console.log(`   Base collateral: ${finalCapitalRequired.toFixed(2)} ${token}`);
  console.log(`   Buffer (${bufferPercentage}%): ${finalBufferAmount.toFixed(2)} ${token}`);
  console.log(`   Total to lock: ${finalTotalLocked.toFixed(2)} ${token}`);
  console.log('');
  
  console.log('⏰ Payment Timeline:');
  console.log(`   Daily yield: ${finalDailyYield.toFixed(4)} ${token}/day`);
  console.log(`   Estimated payment time: ${Math.ceil(finalPaymentDays)} days`);
  console.log(`   Days before deadline: ${Math.floor(finalDaysBeforeDeadline)} days`);
  
  if (finalDaysBeforeDeadline < 0) {
    console.log(`   ⚠️ WARNING: Payment will exceed deadline by ${Math.abs(Math.floor(finalDaysBeforeDeadline))} days`);
    console.log(`   Consider increasing buffer or accepting longer payment time`);
  } else if (finalDaysBeforeDeadline < 7) {
    console.log(`   ⚠️ WARNING: Narrow margin (${Math.floor(finalDaysBeforeDeadline)} days before deadline)`);
    console.log(`   Consider increasing buffer to ${Math.min(20, bufferPercentage + 2)}%`);
  } else {
    console.log(`   ✅ Comfortable margin: ${Math.floor(finalDaysBeforeDeadline)} days before deadline`);
  }
  
  console.log('');
  console.log('💡 Recommendation:');
  
  if (finalMultiplier >= 40) {
    console.log(`   High collateral required (${finalMultiplier.toFixed(1)}x). Consider:`);
    console.log(`   • Extending deadline if possible`);
    console.log(`   • Using upfront mode for immediate payment`);
    console.log(`   • Accepting longer payment time with lower collateral`);
  } else if (finalMultiplier <= 5) {
    console.log(`   Low collateral (${finalMultiplier.toFixed(1)}x). Safe options:`);
    console.log(`   • Can increase buffer for more safety`);
    console.log(`   • Payment will be comfortable within deadline`);
  } else {
    console.log(`   Balanced configuration (${finalMultiplier.toFixed(1)}x).`);
    console.log(`   • Good balance of capital efficiency and timeline safety`);
  }
  
  return {
    amountToPay,
    deadlineDays,
    bufferPercentage,
    estimatedAPY,
    requiredDailyYield,
    requiredCapital,
    collateralMultiplier: finalMultiplier,
    baseCollateral: finalCapitalRequired,
    bufferAmount: finalBufferAmount,
    totalLocked: finalTotalLocked,
    dailyYield: finalDailyYield,
    estimatedPaymentDays: Math.ceil(finalPaymentDays),
    daysBeforeDeadline: Math.floor(finalDaysBeforeDeadline),
    meetsDeadline: finalDaysBeforeDeadline >= 0,
    token
  };
}

/**
 * Generate CLI command for optimal configuration
 */
function generateCLICommand(results) {
  const command = `node scripts/cli.js \\
  --mode standard \\
  --amount ${results.amountToPay} \\
  --recipient 0xRecipientAddress \\
  --token ${results.token} \\
  --collateral ${results.collateralMultiplier.toFixed(1)} \\
  --buffer ${results.bufferPercentage}`;
  
  return command;
}

/**
 * Calculate for multiple deadlines (comparison)
 */
function compareDeadlines({
  amountToPay,
  deadlines = [30, 90, 180, 365],
  bufferPercentage = 8,
  estimatedAPY = 0.05,
  token = 'USDC'
}) {
  console.log('⚖️ Deadline Comparison Analysis\n');
  console.log(`Payment: ${amountToPay} ${token}, Buffer: ${bufferPercentage}%, APY: ${(estimatedAPY * 100).toFixed(2)}%\n`);
  
  console.log('| Deadline | Months | Collateral | Capital Required | Payment Time | Margin |');
  console.log('|----------|--------|------------|------------------|--------------|--------|');
  
  const results = [];
  
  for (const deadlineDays of deadlines) {
    const calc = calculateOptimalCollateral({
      amountToPay,
      deadlineDays,
      bufferPercentage,
      estimatedAPY,
      token
    });
    
    const months = (deadlineDays / 30).toFixed(1);
    const margin = calc.daysBeforeDeadline;
    const marginStatus = margin >= 7 ? '✅' : margin >= 0 ? '⚠️' : '❌';
    
    console.log(`| ${deadlineDays} days | ${months} | ${calc.collateralMultiplier.toFixed(1)}x | ${calc.totalLocked.toFixed(0)} ${token} | ${calc.estimatedPaymentDays} days | ${marginStatus} ${margin} days |`);
    
    results.push(calc);
  }
  
  console.log('\n📈 Recommendations:');
  
  // Find optimal deadline (balance of collateral and margin)
  const optimal = results.reduce((best, current) => {
    const currentScore = (current.daysBeforeDeadline * 2) - (current.collateralMultiplier * 10);
    const bestScore = (best.daysBeforeDeadline * 2) - (best.collateralMultiplier * 10);
    return currentScore > bestScore ? current : best;
  });
  
  console.log(`\n🎯 Optimal deadline: ${optimal.deadlineDays} days (${(optimal.deadlineDays/30).toFixed(1)} months)`);
  console.log(`   • Collateral: ${optimal.collateralMultiplier.toFixed(1)}x`);
  console.log(`   • Capital: ${optimal.totalLocked.toFixed(0)} ${token}`);
  console.log(`   • Margin: ${optimal.daysBeforeDeadline} days before deadline`);
  
  return { results, optimal };
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🧮 Collateral Calculator CLI

Usage:
  node collateral-calculator.js [options]

Options:
  --amount <amount>         Payment amount (required)
  --deadline <days>         Deadline in days (required)
  --buffer <percent>        Buffer percentage (default: 8)
  --apy <percent>           Estimated APY percentage (default: 5)
  --token <token>           Token: USDC or USDT (default: USDC)
  --compare                 Compare multiple deadlines
  --help                    Show this help

Examples:
  # Calculate for specific deadline
  node collateral-calculator.js --amount 150 --deadline 180 --buffer 10

  # Compare multiple deadlines
  node collateral-calculator.js --amount 150 --compare

  # Custom APY
  node collateral-calculator.js --amount 150 --deadline 90 --apy 7
    `);
    process.exit(0);
  }
  
  const params = {
    amountToPay: null,
    deadlineDays: null,
    bufferPercentage: 8,
    estimatedAPY: 0.05,
    token: 'USDC',
    compare: false
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--amount':
        params.amountToPay = parseFloat(args[++i]);
        break;
      case '--deadline':
        params.deadlineDays = parseInt(args[++i]);
        break;
      case '--buffer':
        params.bufferPercentage = parseFloat(args[++i]);
        break;
      case '--apy':
        params.estimatedAPY = parseFloat(args[++i]) / 100;
        break;
      case '--token':
        params.token = args[++i].toUpperCase();
        break;
      case '--compare':
        params.compare = true;
        break;
    }
  }
  
  try {
    if (params.compare) {
      compareDeadlines(params);
    } else {
      if (!params.amountToPay || !params.deadlineDays) {
        console.error('Error: --amount and --deadline are required');
        process.exit(1);
      }
      
      const results = calculateOptimalCollateral(params);
      
      console.log('\n' + '='.repeat(80));
      console.log('🚀 READY-TO-USE CONFIGURATION');
      console.log('='.repeat(80));
      
      console.log(`\nCLI Command:`);
      console.log(generateCLICommand(results));
      
      console.log(`\nJavaScript API:`);
      console.log(`yieldFarmPayment({
  mode: 'standard',
  amountToPay: ${results.amountToPay},
  recipientAddress: '0xRecipientAddress',
  token: '${results.token}',
  collateralMultiplier: ${results.collateralMultiplier.toFixed(1)},
  bufferPercentage: ${results.bufferPercentage}
});`);
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

module.exports = {
  calculateOptimalCollateral,
  compareDeadlines,
  generateCLICommand
};