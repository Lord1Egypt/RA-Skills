/**
 * state-log.js
 * Usage: node state-log.js "CATEGORY" "Your message here"
 * Example: node state-log.js "ACTION" "Updated auth logic in user.ts"
 */

const fs = require('fs');
const path = require('path');

// Configuration
const LOG_FILE = path.join(__dirname, '..', 'STATE.log');
const MAX_LOG_SIZE_MB = 5;

// Get args
const args = process.argv.slice(2);
const category = args[0] ? args[0].toUpperCase() : 'INFO';
const message = args[1] || 'No message provided';

// Timestamp
const timestamp = new Date().toISOString();

// Format: [TIMESTAMP] [CATEGORY] Message
const logEntry = `[${timestamp}] [${category}] ${message}\n`;

try {
  // Simple rotation: if too big, archive and start fresh
  if (fs.existsSync(LOG_FILE)) {
    const stats = fs.statSync(LOG_FILE);
    if (stats.size > MAX_LOG_SIZE_MB * 1024 * 1024) {
      fs.renameSync(LOG_FILE, `${LOG_FILE}.old`);
    }
  }

  fs.appendFileSync(LOG_FILE, logEntry);
  console.log(`Logged: ${category}`);
} catch (err) {
  console.error('Failed to write to state log:', err);
  process.exit(1);
}
