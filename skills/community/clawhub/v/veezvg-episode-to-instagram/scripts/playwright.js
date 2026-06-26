const path = require('path');

const candidates = [
  'playwright-core',
  path.join('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core'),
  path.join('/usr/local/lib/node_modules/openclaw/node_modules/playwright-core')
];

for (const candidate of candidates) {
  try {
    module.exports = require(candidate);
    return;
  } catch {}
}

throw new Error(
  'Could not resolve playwright-core. Install it locally with `npm install` or use an OpenClaw installation that bundles playwright-core.'
);
