#!/usr/bin/env node
/**
 * SUPAH OpenClaw Skill - Signal Feed Example
 * 
 * Get high-conviction trading signals (score ≥85)
 * 
 * Usage: node examples/signal-feed.js [minScore]
 */

const supah = require('../index.js');

async function main() {
  const minScore = parseInt(process.argv[2]) || 85;
  
  console.log('🦸 SUPAH Signal Feed\n');
  console.log(`Minimum score: ${minScore}\n`);
  
  try {
    const result = await supah.getSignals({ minScore });
    
    if (!result.success) {
      console.error('❌ Error:', result.error);
      process.exit(1);
    }
    
    const signals = result.data;
    
    if (signals.length === 0) {
      console.log('No signals found above threshold');
      process.exit(0);
    }
    
    console.log(`Found ${signals.length} signals:\n`);
    
    signals.forEach((signal, i) => {
      console.log(`${i + 1}. ${signal.symbol} (${signal.name})`);
      console.log(`   Score: ${signal.score}/100`);
      console.log(`   Gates: SIG=${signal.gates.sig} TA=${signal.gates.ta} SEC=${signal.gates.sec}`);
      console.log(`   Address: ${signal.address}`);
      console.log(`   Market Cap: $${signal.marketCap?.toLocaleString() || 'N/A'}`);
      console.log();
    });
    
    console.log('✅ Signal feed retrieved');
    
  } catch (error) {
    console.error('❌ Failed to get signals:', error.message);
    process.exit(1);
  }
}

main();
