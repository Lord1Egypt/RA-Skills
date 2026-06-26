#!/usr/bin/env node
/**
 * SUPAH OpenClaw Skill - Basic Token Scan Example
 * 
 * Usage: node examples/basic-scan.js [token_address]
 */

const supah = require('../index.js');

async function main() {
  const address = process.argv[2] || '0x40ba93835789b9958ed588308c299fa27ddc5838'; // Default: SUPH (Creator.bid)
  
  console.log('🦸 SUPAH Token Scan\n');
  console.log(`Scanning: ${address}\n`);
  
  try {
    const result = await supah.scanToken(address);
    
    if (!result.success) {
      console.error('❌ Error:', result.error);
      process.exit(1);
    }
    
    const data = result.data;
    
    console.log(`Token: ${data.symbol} (${data.name})`);
    console.log(`Chain: Base\n`);
    
    console.log(`📊 Overall Score: ${data.score}/100`);
    
    // Risk level
    let risk = 'UNKNOWN';
    if (data.score >= 80) risk = '🟢 SAFE';
    else if (data.score >= 60) risk = '🟡 MODERATE';
    else risk = '🔴 HIGH RISK';
    
    console.log(`Risk Level: ${risk}\n`);
    
    // Gate breakdown
    console.log('Gate Breakdown:');
    console.log(`  SIG (Signals):     ${data.gates.sig}/100 ${data.gates.sig >= 70 ? '✅' : '⚠️'}`);
    console.log(`  TA (Technical):    ${data.gates.ta}/100 ${data.gates.ta >= 70 ? '✅' : '⚠️'}`);
    console.log(`  SEC (Security):    ${data.gates.sec}/100 ${data.gates.sec >= 70 ? '✅' : '⚠️'}`);
    console.log(`  PRED (Prediction): ${data.gates.pred}/100 ${data.gates.pred >= 70 ? '✅' : '⚠️'}`);
    console.log(`  NARR (Narrative):  ${data.gates.narr}/100 ${data.gates.narr >= 70 ? '✅' : '⚠️'}`);
    
    // Recommendation
    console.log('\n💡 Recommendation:');
    if (data.score >= 85) {
      console.log('   High conviction trade opportunity');
    } else if (data.score >= 70) {
      console.log('   Safe to trade with standard position sizing');
    } else if (data.score >= 60) {
      console.log('   Moderate risk - reduce position size');
    } else {
      console.log('   ⚠️ High risk - consider avoiding or use minimal size');
    }
    
    console.log('\n✅ Scan complete');
    
  } catch (error) {
    console.error('❌ Scan failed:', error.message);
    process.exit(1);
  }
}

main();
