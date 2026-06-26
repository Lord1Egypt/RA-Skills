const { DashboardClient } = require('../lib/dashboard-client.js');
const { formatStatus } = require('../lib/formatter.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const days = parseInt(process.argv[2], 10) || 7;
  const data = await client.get(`/overview?days=${days}`);

  console.log(`Cost Overview (last ${days} days)`);
  console.log('─'.repeat(40));

  if (data.totalCostUsd !== undefined) {
    console.log(`Total spend:    $${data.totalCostUsd.toFixed(2)}`);
  }
  if (data.totalRequests !== undefined) {
    console.log(`Requests:       ${data.totalRequests.toLocaleString()}`);
  }
  if (data.savedUsd !== undefined) {
    console.log(`Saved by routing: $${data.savedUsd.toFixed(2)}`);
  }
  if (data.daily && Array.isArray(data.daily)) {
    console.log('');
    console.log('Daily breakdown:');
    for (const d of data.daily) {
      const bar = '█'.repeat(Math.max(1, Math.round((d.costUsd / (data.totalCostUsd || 1)) * 20)));
      console.log(`  ${d.date}  ${bar}  $${d.costUsd.toFixed(2)}`);
    }
  }
  if (data.topModels && Array.isArray(data.topModels)) {
    console.log('');
    console.log('Top models by cost:');
    for (const m of data.topModels.slice(0, 5)) {
      console.log(`  ${m.model}: $${m.costUsd.toFixed(2)} (${m.requests} req)`);
    }
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
