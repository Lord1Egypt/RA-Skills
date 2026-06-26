#!/usr/bin/env node
/**
 * Correction Detector Hook
 *
 * Detects when user corrects Claude and logs the correction for learning.
 * Triggers on patterns like "No, that's wrong", "Actually...", "Try again"
 *
 * Hook type: UserInputSubmit (or analyze assistant responses)
 */

const path = require('path');
const fs = require('fs');

// Correction patterns to detect
const CORRECTION_PATTERNS = [
  // Direct corrections
  /^no[,.]?\s*(that'?s?\s*)?(not|wrong|incorrect)/i,
  /^actually[,.]?\s/i,
  /^that'?s?\s*(not|wrong|incorrect)/i,
  /^wrong[,.]?\s/i,
  /^incorrect[,.]?\s/i,

  // Retry requests
  /try\s*(again|once\s*more)/i,
  /do\s*it\s*(again|over)/i,
  /redo\s*(that|this|it)/i,
  /start\s*over/i,

  // Misunderstanding indicators
  /that'?s?\s*not\s*what\s*i\s*(meant|asked|wanted)/i,
  /you\s*misunderstood/i,
  /i\s*meant\s/i,
  /let\s*me\s*(clarify|rephrase|explain)/i,

  // Negative feedback
  /that\s*doesn'?t?\s*(work|help)/i,
  /still\s*(not|wrong|broken|failing)/i,
  /same\s*(error|problem|issue)/i,

  // Explicit corrections
  /^instead[,.]?\s/i,
  /should\s*(be|have\s*been)\s/i,
  /^not\s+\w+[,.]?\s+but\s+/i,  // "Not X, but Y"
];

// Get paths
const CLAUDE_DIR = process.env.HOME + '/.claude';
const LOGS_DIR = path.join(CLAUDE_DIR, 'logs');
const CORRECTIONS_FILE = path.join(LOGS_DIR, 'corrections.jsonl');
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

function detectCorrection(userMessage) {
  for (const pattern of CORRECTION_PATTERNS) {
    if (pattern.test(userMessage)) {
      return {
        detected: true,
        pattern: pattern.toString(),
        type: categorizeCorrection(pattern)
      };
    }
  }
  return { detected: false };
}

function categorizeCorrection(pattern) {
  const patternStr = pattern.toString().toLowerCase();

  if (patternStr.includes('wrong') || patternStr.includes('incorrect') || patternStr.includes('not')) {
    return 'factual_error';
  }
  if (patternStr.includes('again') || patternStr.includes('redo') || patternStr.includes('over')) {
    return 'retry_request';
  }
  if (patternStr.includes('meant') || patternStr.includes('misunderstood') || patternStr.includes('clarify')) {
    return 'misunderstanding';
  }
  if (patternStr.includes('work') || patternStr.includes('error') || patternStr.includes('failing')) {
    return 'failed_solution';
  }
  return 'general_correction';
}

function logCorrection(userMessage, detection, context = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    user_message: userMessage.substring(0, 500), // Truncate for privacy
    correction_type: detection.type,
    pattern_matched: detection.pattern,
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown',
    context: context
  };

  appendJsonl(CORRECTIONS_FILE, entry);

  // Also add to learnings with learning type
  const learning = {
    timestamp: new Date().toISOString(),
    type: 'user_correction',
    category: detection.type,
    description: `User corrected: "${userMessage.substring(0, 100)}..."`,
    source: 'correction_detector',
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown'
  };

  appendJsonl(LEARNINGS_FILE, learning);

  return entry;
}

// Main execution
function main() {
  // Read user input from stdin (hook receives context)
  let input = '';

  if (process.stdin.isTTY) {
    // Running directly for testing
    const testMessages = [
      "No, that's wrong. The function should return a list.",
      "Actually, I meant the other file.",
      "Try again with the correct path.",
      "That's not what I asked for.",
      "Hello, how are you?" // Should NOT trigger
    ];

    console.log('Correction Detector Test:\n');
    for (const msg of testMessages) {
      const result = detectCorrection(msg);
      console.log(`"${msg}"`);
      console.log(`  Detected: ${result.detected}`);
      if (result.detected) {
        console.log(`  Type: ${result.type}`);
      }
      console.log('');
    }
    return;
  }

  // Read from stdin when used as hook
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
    try {
      const hookData = JSON.parse(input);
      const userMessage = hookData.user_message || hookData.content || '';

      const detection = detectCorrection(userMessage);

      if (detection.detected) {
        const logged = logCorrection(userMessage, detection, {
          previous_assistant_response: hookData.previous_response?.substring(0, 200)
        });

        console.log(`[Correction] Detected ${detection.type}: "${userMessage.substring(0, 50)}..."`);
      }
    } catch (e) {
      // Silent fail for hooks
    }
  });
}

// Export for testing
module.exports = { detectCorrection, logCorrection, CORRECTION_PATTERNS };

if (require.main === module) {
  main();
}
