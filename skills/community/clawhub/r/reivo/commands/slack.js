const { DashboardClient } = require('../lib/dashboard-client.js');

async function main() {
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('REIVO_API_KEY not set. Run setup first.');
    process.exit(1);
  }

  const webhookUrl = process.argv[2];
  if (!webhookUrl) {
    console.log('Usage: slack <webhook-url>');
    console.log('Example: slack https://hooks.slack.com/services/T.../B.../xxx');
    process.exit(1);
  }

  const client = new DashboardClient(apiKey);
  await client.post('/settings', { slackWebhookUrl: webhookUrl });
  console.log('✓ Slack notifications configured');
  console.log('  You will receive alerts for: budget warnings, loop detection, anomalies');
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
