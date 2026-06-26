const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  const data = await client.get('/defense-status');

  console.log('Defense Status');
  console.log('─'.repeat(40));

  if (data.budget) {
    const { usedUsd, limitUsd } = data.budget;
    const pct = limitUsd > 0 ? Math.round((usedUsd / limitUsd) * 100) : 0;
    const filled = Math.min(20, Math.round(pct / 5));
    const bar = '█'.repeat(filled) + '░'.repeat(20 - filled);
    console.log(`Budget: $${usedUsd.toFixed(2)} / $${limitUsd.toFixed(2)} (${pct}%)`);
    console.log(`  [${bar}]`);
    if (pct >= 80) {
      console.log('  ⚠  Budget usage is high!');
    }
  } else {
    console.log('Budget: No limit set');
  }

  console.log('');
  if (data.loops) {
    console.log(`Loops detected:    ${data.loops.today || 0} today, ${data.loops.week || 0} this week`);
  }
  if (data.blocked) {
    console.log(`Requests blocked:  ${data.blocked.today || 0} today, ${data.blocked.week || 0} this week`);
  }
  if (data.anomalies) {
    console.log(`Anomalies:         ${data.anomalies.today || 0} today, ${data.anomalies.week || 0} this week`);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
