#!/usr/bin/env node
/**
 * Initialize a new Second Brain vault.
 */

const fs = require('fs');
const path = require('path');
const { VAULT_PATH, requireWriteApproval } = require('./lib/common');

const FOLDERS = [
  '00-Inbox', '01-Daily', '02-Ideas', '03-Projects',
  '04-People', '05-Concepts', '06-Reading', '07-MOCs', '99-Archive'
];

const README_CONTENT = `# Second Brain

Personal knowledge management vault.
`;

const IGNORE_CONTENT = `# Second Brain Ignore Rules
README.md
CHANGELOG.md
LICENSE.md
templates/
.DS_Store
.git/
node_modules/
`;

function initVault(input = {}) {
  requireWriteApproval(input, 'allow_write');

  if (fs.existsSync(VAULT_PATH)) {
    const existingFiles = fs.readdirSync(VAULT_PATH).filter(f => !f.startsWith('.'));
    if (existingFiles.length > 0) {
      return { status: 'exists', path: VAULT_PATH, message: 'Vault already exists' };
    }
  }

  fs.mkdirSync(VAULT_PATH, { recursive: true });
  for (const folder of FOLDERS) {
    fs.mkdirSync(path.join(VAULT_PATH, folder), { recursive: true });
  }
  fs.writeFileSync(path.join(VAULT_PATH, 'README.md'), README_CONTENT, 'utf-8');
  fs.writeFileSync(path.join(VAULT_PATH, '.secondbrainignore'), IGNORE_CONTENT, 'utf-8');

  return {
    status: 'success',
    path: VAULT_PATH,
    folders: FOLDERS,
    message: 'Vault initialized successfully'
  };
}

const args = process.argv.slice(2);
const input = args.length > 0 ? JSON.parse(args[0]) : {};

try {
  const result = initVault(input);
  console.log(JSON.stringify(result, null, 2));
  if (result.status === 'error') process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
