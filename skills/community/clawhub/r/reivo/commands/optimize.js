const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const data = await client.get('/optimization');

  console.log('Optimization Tips');
  console.log('─'.repeat(40));

  if (!data.tips || data.tips.length === 0) {
    console.log('No optimization tips available — your usage looks efficient!');
    return;
  }

  for (const tip of data.tips) {
    const icon = tip.severity === 'high' ? '🔴' : tip.severity === 'medium' ? '🟡' : '🟢';
    console.log(`${icon} ${tip.title}`);
    console.log(`   ${tip.description}`);
    if (tip.estimatedSavingsUsd) {
      console.log(`   Estimated savings: $${tip.estimatedSavingsUsd.toFixed(2)}/month`);
    }
    console.log('');
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
