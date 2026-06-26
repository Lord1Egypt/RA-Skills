'use strict';

const path = require('path');
const fs = require('fs');
const constants = require('./constants');

const ENV_PATH = path.join(__dirname, '..', 'config', '.env');

if (!fs.existsSync(ENV_PATH)) {
  throw new Error(
    `Platform config file not found: ${ENV_PATH}\n` +
    `This file contains API gateway URL and server public key (not user credentials).\n` +
    `Possible causes:\n` +
    `  1. Skill package is incomplete — config/ directory was excluded during packaging.\n` +
    `     Fix: Ensure pack-skill.ps1 includes config/.env in the package.\n` +
    `  2. Manual installation — config/.env was not copied.\n` +
    `     Fix: Copy config/.env.example to config/.env and fill in the values.\n` +
    `  See references/credential-setup-guide.md for details.`
  );
}

require('dotenv').config({ path: ENV_PATH });

function getApiUrl() {
  const url = process.env[constants.ENV_API_URL];
  if (!url) throw new Error(
    `${constants.ENV_API_URL} not configured.\n` +
    `This value should come from config/.env. If the file exists but this variable is missing, ` +
    `add it to config/.env or set it as an environment variable.`
  );
  return url;
}

function getServerPublicKey() {
  const key = process.env[constants.ENV_GM_SERVER_PUBLIC_KEY];
  if (!key) throw new Error(
    `${constants.ENV_GM_SERVER_PUBLIC_KEY} not configured.\n` +
    `This value should come from config/.env. If the file exists but this variable is missing, ` +
    `add it to config/.env or set it as an environment variable.`
  );
  return key;
}

function validate() {
  const errors = [];

  const apiUrl = process.env[constants.ENV_API_URL];
  if (!apiUrl) {
    errors.push(`${constants.ENV_API_URL} is required in config/.env`);
  } else if (!apiUrl.startsWith('https://')) {
    errors.push(`${constants.ENV_API_URL} must use HTTPS protocol (HTTP is not allowed for payment security)`);
  }

  const serverPublicKey = process.env[constants.ENV_GM_SERVER_PUBLIC_KEY] || '';
  if (serverPublicKey && serverPublicKey.length !== constants.SM2_PUBLIC_KEY_LENGTH) {
    errors.push(
      `${constants.ENV_GM_SERVER_PUBLIC_KEY} length should be ${constants.SM2_PUBLIC_KEY_LENGTH} (04 prefix + 128 hex), got ${serverPublicKey.length}`
    );
  }

  if (errors.length > 0) {
    throw new Error(`Configuration errors:\n  - ${errors.join('\n  - ')}`);
  }
}

module.exports = {
  getApiUrl,
  getServerPublicKey,
  validate,
};
