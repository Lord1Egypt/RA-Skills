const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const action = process.argv[2] || 'status';

  if (action === 'set') {
    const amount = parseFloat(process.argv[3]);
    if (isNaN(amount) || amount <= 0) {
      console.log('Usage: budget set <amount>');
      console.log('Example: budget set 50');
      process.exit(1);
    }
    const result = await client.post('/settings', { budgetLimitUsd: amount });
    console.log(`✓ Budget set to $${amount.toFixed(2)}`);
    return;
  }

  if (action === 'clear') {
    await client.post('/settings', { budgetLimitUsd: null });
    console.log('✓ Budget limit removed');
    return;
  }

  // Default: show status
  const data = await client.get('/defense-status');
  if (data.budget) {
    const pct = data.budget.limitUsd > 0
      ? Math.round((data.budget.usedUsd / data.budget.limitUsd) * 100)
      : 0;
    const bar = '█'.repeat(Math.min(20, Math.round(pct / 5))) + '░'.repeat(Math.max(0, 20 - Math.round(pct / 5)));
    console.log(`Budget: $${data.budget.usedUsd.toFixed(2)} / $${data.budget.limitUsd.toFixed(2)} (${pct}%)`);
    console.log(`  [${bar}]`);
  }
  if (data.loops) {
    console.log(`Loops detected: ${data.loops.today || 0} today, ${data.loops.week || 0} this week`);
  }
  if (data.blocked) {
    console.log(`Requests blocked: ${data.blocked.today || 0} today, ${data.blocked.week || 0} this week`);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
