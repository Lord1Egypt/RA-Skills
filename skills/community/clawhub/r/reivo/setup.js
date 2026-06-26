async function main() {
  console.log('');
  console.log('Reivo — AI Agent Cost Optimizer');
  console.log('================================');
  console.log('');

  // Check for REIVO_API_KEY
  const apiKey = process.env.REIVO_API_KEY;
  if (!apiKey) {
    console.log('⚠  REIVO_API_KEY not set.');
    console.log('');
    console.log('To get started:');
    console.log('  1. Sign up at https://app.reivo.dev');
    console.log('  2. Generate an API key in Settings (format: rv_...)');
    console.log('  3. Set the environment variable:');
    console.log('     export REIVO_API_KEY="rv_your_key_here"');
    console.log('');
    console.log('Then re-run: npx clawhub@latest run reivo');
    process.exit(1);
  }

  // Validate key format locally (no network call)
  if (!apiKey.startsWith('rv_') || apiKey.length < 12) {
    console.log('✗ Invalid API key format — expected rv_... (12+ chars)');
    process.exit(1);
  }

  console.log('✓ API key configured');
  console.log('');
  console.log('Setup complete! Available commands:');
  console.log('  "show costs"          — View spending overview');
  console.log('  "budget status"       — Check budget & loop status');
  console.log('  "set budget to $50"   — Set a spending limit');
  console.log('  "optimization tips"   — Get cost reduction suggestions');
  console.log('  "open dashboard"      — Open the web dashboard');
  console.log('');
}

main();
