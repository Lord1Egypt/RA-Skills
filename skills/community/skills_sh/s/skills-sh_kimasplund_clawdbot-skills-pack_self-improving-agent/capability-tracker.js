#!/usr/bin/env node
/**
 * Missing Capability Tracker
 *
 * Detects when user requests functionality that isn't available:
 * - "Can you X?" where X isn't possible
 * - Requests for unavailable tools/features
 * - Repeated requests for same missing feature
 *
 * Tracks frequency to identify high-value skill gaps.
 */

const path = require('path');
const fs = require('fs');

const CLAUDE_DIR = process.env.HOME + '/.claude';
const LOGS_DIR = path.join(CLAUDE_DIR, 'logs');
const CAPABILITIES_FILE = path.join(LOGS_DIR, 'missing_capabilities.jsonl');
const CAPABILITIES_SUMMARY = path.join(LOGS_DIR, 'capability_gaps.json');
const LEARNINGS_FILE = path.join(LOGS_DIR, 'learnings.jsonl');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function appendJsonl(file, data) {
  ensureDir(path.dirname(file));
  fs.appendFileSync(file, JSON.stringify(data) + '\n');
}

function readJson(file) {
  try {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    }
  } catch (e) {}
  return {};
}

function writeJson(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

// Patterns that indicate a capability request
const CAPABILITY_REQUEST_PATTERNS = [
  /can\s+you\s+(\w+[\w\s]+)\??/i,
  /do\s+you\s+(have|support|know\s+how\s+to)\s+(\w+[\w\s]+)\??/i,
  /is\s+(it|there)\s+(a\s+way|possible)\s+to\s+(\w+[\w\s]+)\??/i,
  /how\s+(do\s+i|can\s+i|to)\s+(\w+[\w\s]+)\??/i,
  /i\s+(need|want)\s+(you\s+to\s+)?(\w+[\w\s]+)/i,
];

// Patterns that indicate the capability is missing
const MISSING_CAPABILITY_RESPONSES = [
  /i\s+(can'?t|cannot|don'?t\s+have|am\s+not\s+able)/i,
  /that'?s?\s+not\s+(possible|available|supported)/i,
  /i\s+don'?t\s+have\s+(access|the\s+ability)/i,
  /unfortunately/i,
  /outside\s+(my|of\s+my)\s+(capabilities|abilities)/i,
  /no\s+tool\s+(for|to)/i,
  /not\s+currently\s+(supported|available)/i,
];

// Categorize the type of capability
function categorizeCapability(request) {
  const requestLower = request.toLowerCase();

  if (requestLower.includes('browse') || requestLower.includes('internet') || requestLower.includes('web')) {
    return 'web_browsing';
  }
  if (requestLower.includes('image') || requestLower.includes('picture') || requestLower.includes('photo')) {
    return 'image_processing';
  }
  if (requestLower.includes('video') || requestLower.includes('audio') || requestLower.includes('media')) {
    return 'media_processing';
  }
  if (requestLower.includes('email') || requestLower.includes('send') || requestLower.includes('message')) {
    return 'communication';
  }
  if (requestLower.includes('database') || requestLower.includes('sql') || requestLower.includes('query')) {
    return 'database_access';
  }
  if (requestLower.includes('api') || requestLower.includes('endpoint') || requestLower.includes('service')) {
    return 'external_api';
  }
  if (requestLower.includes('file') || requestLower.includes('folder') || requestLower.includes('directory')) {
    return 'file_system';
  }
  if (requestLower.includes('install') || requestLower.includes('package') || requestLower.includes('dependency')) {
    return 'package_management';
  }
  if (requestLower.includes('run') || requestLower.includes('execute') || requestLower.includes('start')) {
    return 'execution';
  }
  if (requestLower.includes('remember') || requestLower.includes('recall') || requestLower.includes('memory')) {
    return 'memory_persistence';
  }

  return 'other';
}

// Extract what capability was requested
function extractCapability(userMessage) {
  for (const pattern of CAPABILITY_REQUEST_PATTERNS) {
    const match = userMessage.match(pattern);
    if (match) {
      // Get the captured group (the capability description)
      const capability = match[match.length - 1] || match[1];
      return capability.trim().substring(0, 100);
    }
  }
  return null;
}

// Check if response indicates missing capability
function isMissingCapabilityResponse(response) {
  for (const pattern of MISSING_CAPABILITY_RESPONSES) {
    if (pattern.test(response)) {
      return true;
    }
  }
  return false;
}

// Log a missing capability
function logMissingCapability(userRequest, capability, category) {
  const entry = {
    timestamp: new Date().toISOString(),
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown',
    user_request: userRequest.substring(0, 300),
    capability_requested: capability,
    category: category,
  };

  appendJsonl(CAPABILITIES_FILE, entry);

  // Update summary counts
  const summary = readJson(CAPABILITIES_SUMMARY);
  if (!summary.capabilities) summary.capabilities = {};
  if (!summary.categories) summary.categories = {};
  if (!summary.total_requests) summary.total_requests = 0;

  // Track by specific capability
  const capKey = capability.toLowerCase().replace(/[^a-z0-9]+/g, '_');
  if (!summary.capabilities[capKey]) {
    summary.capabilities[capKey] = {
      description: capability,
      category: category,
      count: 0,
      first_seen: entry.timestamp,
      last_seen: entry.timestamp
    };
  }
  summary.capabilities[capKey].count++;
  summary.capabilities[capKey].last_seen = entry.timestamp;

  // Track by category
  summary.categories[category] = (summary.categories[category] || 0) + 1;
  summary.total_requests++;

  writeJson(CAPABILITIES_SUMMARY, summary);

  // Add to learnings
  const learning = {
    timestamp: new Date().toISOString(),
    type: 'missing_capability',
    category: category,
    description: `User requested unavailable capability: ${capability}`,
    request_count: summary.capabilities[capKey].count,
    source: 'capability_tracker',
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown'
  };

  appendJsonl(LEARNINGS_FILE, learning);

  return entry;
}

// Get top missing capabilities (for review)
function getTopMissingCapabilities(limit = 10) {
  const summary = readJson(CAPABILITIES_SUMMARY);
  if (!summary.capabilities) return [];

  const sorted = Object.entries(summary.capabilities)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, limit)
    .map(([key, data]) => ({
      capability: data.description,
      category: data.category,
      count: data.count,
      first_seen: data.first_seen,
      last_seen: data.last_seen
    }));

  return sorted;
}

// Main execution
function main() {
  const args = process.argv.slice(2);

  // Command mode: show top missing capabilities
  if (args[0] === '--report') {
    const top = getTopMissingCapabilities(15);
    console.log('\n=== Top Missing Capabilities ===\n');
    if (top.length === 0) {
      console.log('No missing capabilities tracked yet.');
    } else {
      for (const cap of top) {
        console.log(`[${cap.count}x] ${cap.capability}`);
        console.log(`    Category: ${cap.category}`);
        console.log(`    Last requested: ${cap.last_seen.split('T')[0]}`);
        console.log('');
      }
    }

    const summary = readJson(CAPABILITIES_SUMMARY);
    if (summary.categories) {
      console.log('=== By Category ===\n');
      const cats = Object.entries(summary.categories).sort((a, b) => b[1] - a[1]);
      for (const [cat, count] of cats) {
        console.log(`  ${cat}: ${count}`);
      }
    }
    return;
  }

  // Test mode
  if (process.stdin.isTTY) {
    console.log('Capability Tracker Test:\n');

    const testMessages = [
      "Can you browse the web and find information?",
      "Do you have access to send emails?",
      "Is there a way to process images?",
      "How can I make you remember this for next time?",
      "Hello, how are you?" // Should NOT trigger
    ];

    for (const msg of testMessages) {
      const cap = extractCapability(msg);
      if (cap) {
        const category = categorizeCapability(cap);
        console.log(`"${msg}"`);
        console.log(`  Capability: ${cap}`);
        console.log(`  Category: ${category}`);
        console.log('');
      } else {
        console.log(`"${msg}"`);
        console.log(`  No capability request detected`);
        console.log('');
      }
    }
    return;
  }

  // Hook mode
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
    try {
      const hookData = JSON.parse(input);

      // Check if this is a capability request that we couldn't fulfill
      const userMessage = hookData.user_message || '';
      const assistantResponse = hookData.assistant_response || '';

      const capability = extractCapability(userMessage);
      if (capability && isMissingCapabilityResponse(assistantResponse)) {
        const category = categorizeCapability(capability);
        const logged = logMissingCapability(userMessage, capability, category);
        console.log(`[Capability Gap] ${category}: ${capability}`);
      }
    } catch (e) {
      // Silent fail
    }
  });
}

module.exports = {
  extractCapability,
  categorizeCapability,
  isMissingCapabilityResponse,
  logMissingCapability,
  getTopMissingCapabilities
};

if (require.main === module) {
  main();
}
