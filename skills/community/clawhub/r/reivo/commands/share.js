const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const data = await client.get('/overview?days=30');

  console.log('Share your Reivo savings:');
  console.log('');

  const saved = data.savedUsd || 0;
  const total = data.totalCostUsd || 0;
  const pct = total > 0 ? Math.round((saved / (total + saved)) * 100) : 0;

  console.log(`"Saved $${saved.toFixed(2)} on AI API costs this month (${pct}% reduction) with @reivo_dev 💰"`);
  console.log('');
  console.log('Dashboard: https://app.reivo.dev');
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
