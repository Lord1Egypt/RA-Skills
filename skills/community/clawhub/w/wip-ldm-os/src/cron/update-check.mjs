#!/usr/bin/env node
/**
 * LDM OS Update Checker Cron
 * Runs every 6 hours via LaunchAgent.
 * Checks npm for newer versions of registered extensions
 * and broadcasts a message if updates are available.
 */

import { checkForUpdates } from '../../lib/updates.mjs';
import { sendMessage } from '../../lib/messages.mjs';

async function main() {
  const result = checkForUpdates();
  if (result.updatesAvailable > 0) {
    const summary = result.updates
      .map(u => `${u.name}: ${u.currentVersion} -> ${u.latestVersion}`)
      .join(', ');
    sendMessage({
      from: 'ldm-update-checker',
      to: 'all',
      body: `Updates available: ${summary}`,
      type: 'update-available',
    });
  }
  console.log(`Checked ${result.checked} extensions. ${result.updatesAvailable} update(s) available.`);
}

main().catch(e => { console.error(e.message); process.exit(1); });
