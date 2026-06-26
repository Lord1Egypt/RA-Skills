const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const data = await client.get('/overview?days=30');

  console.log('Monthly Report');
  console.log('─'.repeat(40));

  if (data.totalCostUsd !== undefined) {
    console.log(`Total spend:      $${data.totalCostUsd.toFixed(2)}`);
  }
  if (data.totalRequests !== undefined) {
    console.log(`Total requests:   ${data.totalRequests.toLocaleString()}`);
  }
  if (data.savedUsd !== undefined) {
    console.log(`Saved by routing: $${data.savedUsd.toFixed(2)}`);
  }

  if (data.topModels && Array.isArray(data.topModels)) {
    console.log('');
    console.log('Model breakdown:');
    for (const m of data.topModels) {
      console.log(`  ${m.model}: $${m.costUsd.toFixed(2)} (${m.requests} req)`);
    }
  }

  if (data.topAgents && Array.isArray(data.topAgents)) {
    console.log('');
    console.log('Agent breakdown:');
    for (const a of data.topAgents.slice(0, 10)) {
      console.log(`  ${a.agentId}: $${a.costUsd.toFixed(2)} (${a.requests} req)`);
    }
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
