#!/usr/bin/env node
/**
 * Multi-User Config Loader
 * Loads user-specific config from credentials/{USER_ID}.json
 */

const fs = require("fs");
const path = require("path");

function loadUserConfig(exitOnMissing = true) {
  const USER_ID = process.env.USER_ID || process.env.TELEGRAM_USER_ID;

  if (!USER_ID) {
    if (exitOnMissing) {
      console.error("❌ USER_ID or TELEGRAM_USER_ID environment variable required");
      console.error("   Set it when calling the script: USER_ID=1234567890 node trading.js ...");
      process.exit(1);
    }
    return { config: null, userId: null, credentialsPath: null, exists: false };
  }

  const credentialsPath = path.join(__dirname, "..", "credentials", `${USER_ID}.json`);

  if (!fs.existsSync(credentialsPath)) {
    if (exitOnMissing) {
      console.error(`❌ No config found for user ${USER_ID}`);
      console.error(`   Create: ${credentialsPath}`);
      console.error(`   Copy from: config.example.json`);
      process.exit(1);
    }
    return { config: null, userId: USER_ID, credentialsPath, exists: false };
  }

  try {
    const config = JSON.parse(fs.readFileSync(credentialsPath, "utf8"));
    return { config, userId: USER_ID, credentialsPath, exists: true };
  } catch (e) {
    if (exitOnMissing) {
      console.error(`❌ Failed to load config for user ${USER_ID}: ${e.message}`);
      process.exit(1);
    }
    return { config: null, userId: USER_ID, credentialsPath, exists: false, error: e.message };
  }
}

// Check if user is configured (soft mode, doesn't exit)
function checkUserConfigured() {
  return loadUserConfig(false);
}

function getStatePath(userId, filename = "state.json") {
  const stateDir = path.join(__dirname, "..", "state");
  if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
  }
  return path.join(stateDir, `${userId}.${filename}`);
}

module.exports = { loadUserConfig, checkUserConfigured, getStatePath };
