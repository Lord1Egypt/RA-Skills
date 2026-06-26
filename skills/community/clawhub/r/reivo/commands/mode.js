const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const mode = process.argv[2];
  if (!mode || !['aggressive', 'balanced', 'quality'].includes(mode)) {
    console.log('Usage: mode <aggressive|balanced|quality>');
    console.log('');
    console.log('  aggressive — maximize savings, route to cheapest capable model');
    console.log('  balanced   — balance cost and quality (default)');
    console.log('  quality    — prefer original model, only route when confident');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  await client.post('/settings', { routingMode: mode });
  console.log(`✓ Routing mode set to: ${mode}`);
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
