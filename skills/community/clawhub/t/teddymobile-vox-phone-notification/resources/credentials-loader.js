const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_CREDENTIALS_PATH = path.join(os.homedir(), '.teddymobile', 'credentials.json');

function resolveCredentialsPath(explicitPath) {
  return explicitPath || process.env.VOX_CREDENTIALS_FILE || DEFAULT_CREDENTIALS_PATH;
}

function readJsonFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }

  const raw = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(raw);
}

function fromEnvironment() {
  return {
    VOX_APP_ID: process.env.VOX_APP_ID,
    VOX_SECRET: process.env.VOX_SECRET,
    VOX_BOT_ID: process.env.VOX_BOT_ID,
    VOX_OUTBOUND_NUMBER: process.env.VOX_OUTBOUND_NUMBER,
    VOX_CALLBACK_URL: process.env.VOX_CALLBACK_URL,
  };
}

function compact(object) {
  return Object.fromEntries(
    Object.entries(object).filter(([, value]) => value != null && value !== '')
  );
}

function loadVoxCredentials(options = {}) {
  const credentialsPath = resolveCredentialsPath(options.credentialsPath);
  const envCredentials = compact(fromEnvironment());
  const fileCredentials = compact(readJsonFile(credentialsPath) || {});

  const merged = {
    ...fileCredentials,
    ...envCredentials,
  };

  const requiredKeys = options.requiredKeys || [
    'VOX_APP_ID',
    'VOX_SECRET',
    'VOX_BOT_ID',
    'VOX_OUTBOUND_NUMBER',
  ];

  const missingKeys = requiredKeys.filter((key) => !merged[key]);

  if (missingKeys.length > 0) {
    throw new Error(
      `Missing required Vox credentials: ${missingKeys.join(', ')}. ` +
        `Checked environment variables first, then credentials file: ${credentialsPath}`
    );
  }

  return {
    appId: merged.VOX_APP_ID,
    secret: merged.VOX_SECRET,
    botid: merged.VOX_BOT_ID,
    outboundNumber: merged.VOX_OUTBOUND_NUMBER,
    callbackUrl: merged.VOX_CALLBACK_URL,
    raw: merged,
    credentialsPath,
  };
}

module.exports = {
  DEFAULT_CREDENTIALS_PATH,
  resolveCredentialsPath,
  loadVoxCredentials,
};
