#!/usr/bin/env node
/**
 * Enhanced Failure Logger
 *
 * Captures detailed context when tools/commands fail:
 * - Error type and message
 * - What was being attempted
 * - Recovery action taken
 * - Related learnings
 *
 * Hook type: PostToolUse
 */

const path = require('path');
const fs = require('fs');

const CLAUDE_DIR = process.env.HOME + '/.claude';
const LOGS_DIR = path.join(CLAUDE_DIR, 'logs');
const FAILURES_FILE = path.join(LOGS_DIR, 'failures_detailed.jsonl');
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

// Categorize error types
function categorizeError(error, toolName) {
  const errorStr = (error || '').toLowerCase();

  if (errorStr.includes('permission denied') || errorStr.includes('access denied')) {
    return 'permission_error';
  }
  if (errorStr.includes('not found') || errorStr.includes('no such file')) {
    return 'not_found';
  }
  if (errorStr.includes('timeout') || errorStr.includes('timed out')) {
    return 'timeout';
  }
  if (errorStr.includes('connection') || errorStr.includes('network')) {
    return 'network_error';
  }
  if (errorStr.includes('syntax') || errorStr.includes('parse')) {
    return 'syntax_error';
  }
  if (errorStr.includes('memory') || errorStr.includes('oom')) {
    return 'resource_error';
  }
  if (errorStr.includes('api') || errorStr.includes('rate limit') || errorStr.includes('quota')) {
    return 'api_error';
  }
  if (toolName === 'Bash' || toolName === 'bash') {
    return 'command_failed';
  }
  if (toolName === 'Edit' || toolName === 'Write') {
    return 'file_operation_failed';
  }
  if (toolName === 'Task') {
    return 'agent_failed';
  }

  return 'unknown_error';
}

// Extract useful context from tool input
function extractContext(toolInput, toolName) {
  const context = {
    tool: toolName,
    attempted_action: null,
    target: null
  };

  try {
    if (typeof toolInput === 'string') {
      toolInput = JSON.parse(toolInput);
    }

    switch (toolName) {
      case 'Bash':
        context.attempted_action = 'execute_command';
        context.target = toolInput.command?.substring(0, 200);
        break;
      case 'Read':
        context.attempted_action = 'read_file';
        context.target = toolInput.file_path;
        break;
      case 'Write':
        context.attempted_action = 'write_file';
        context.target = toolInput.file_path;
        break;
      case 'Edit':
        context.attempted_action = 'edit_file';
        context.target = toolInput.file_path;
        break;
      case 'Task':
        context.attempted_action = 'spawn_agent';
        context.target = toolInput.subagent_type;
        break;
      case 'WebFetch':
        context.attempted_action = 'fetch_url';
        context.target = toolInput.url;
        break;
      case 'Grep':
        context.attempted_action = 'search_pattern';
        context.target = toolInput.pattern;
        break;
      default:
        context.attempted_action = `use_${toolName.toLowerCase()}`;
    }
  } catch (e) {
    // Silent fail
  }

  return context;
}

// Suggest recovery actions based on error type
function suggestRecovery(errorType, context) {
  const suggestions = {
    permission_error: 'Check file permissions or run with elevated privileges',
    not_found: 'Verify path exists, check for typos, or create the resource',
    timeout: 'Increase timeout, check network, or retry with backoff',
    network_error: 'Check connectivity, verify URLs, or use offline fallback',
    syntax_error: 'Review syntax, check documentation, validate input format',
    resource_error: 'Free up resources, reduce batch size, or stream data',
    api_error: 'Check API key, respect rate limits, or use fallback service',
    command_failed: 'Check command syntax, verify dependencies installed',
    file_operation_failed: 'Verify path, check permissions, ensure disk space',
    agent_failed: 'Simplify task, provide more context, or try different agent',
    unknown_error: 'Review error message, check logs, search for similar issues'
  };

  return suggestions[errorType] || suggestions.unknown_error;
}

function logFailure(toolName, toolInput, error, exitCode) {
  const errorType = categorizeError(error, toolName);
  const context = extractContext(toolInput, toolName);
  const recovery = suggestRecovery(errorType, context);

  const entry = {
    timestamp: new Date().toISOString(),
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown',
    tool: toolName,
    error_type: errorType,
    error_message: (error || '').substring(0, 500),
    exit_code: exitCode,
    context: context,
    suggested_recovery: recovery,
    learned: false // Will be updated if recovery succeeds
  };

  appendJsonl(FAILURES_FILE, entry);

  // Also add to learnings
  const learning = {
    timestamp: new Date().toISOString(),
    type: 'tool_failure',
    category: errorType,
    tool: toolName,
    description: `${toolName} failed: ${errorType} - ${context.attempted_action || 'unknown action'}`,
    context: context.target?.substring(0, 100),
    recovery_suggestion: recovery,
    source: 'enhanced_failure_logger',
    session_id: process.env.CLAUDE_SESSION_ID || 'unknown'
  };

  appendJsonl(LEARNINGS_FILE, learning);

  return entry;
}

// Main execution
function main() {
  let input = '';

  if (process.stdin.isTTY) {
    // Test mode
    console.log('Enhanced Failure Logger Test:\n');

    const testCases = [
      { tool: 'Bash', error: 'permission denied: /etc/passwd', exit: 1 },
      { tool: 'Read', error: 'no such file or directory: /foo/bar.txt', exit: 1 },
      { tool: 'WebFetch', error: 'connection timeout after 30s', exit: 1 },
      { tool: 'Task', error: 'agent failed to complete task', exit: 1 }
    ];

    for (const tc of testCases) {
      const type = categorizeError(tc.error, tc.tool);
      const recovery = suggestRecovery(type, {});
      console.log(`Tool: ${tc.tool}`);
      console.log(`Error: ${tc.error}`);
      console.log(`Type: ${type}`);
      console.log(`Recovery: ${recovery}`);
      console.log('');
    }
    return;
  }

  // Hook mode
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
    try {
      const hookData = JSON.parse(input);

      // Check if this is a failure
      const isFailure =
        hookData.exit_code !== 0 ||
        hookData.error ||
        (hookData.result && hookData.result.includes('error')) ||
        (hookData.result && hookData.result.includes('failed'));

      if (isFailure) {
        const logged = logFailure(
          hookData.tool_name || hookData.tool || 'unknown',
          hookData.tool_input || hookData.input || {},
          hookData.error || hookData.result || '',
          hookData.exit_code
        );

        console.log(`[Failure] ${logged.error_type}: ${logged.tool} - ${logged.suggested_recovery}`);
      }
    } catch (e) {
      // Silent fail
    }
  });
}

module.exports = { categorizeError, extractContext, suggestRecovery, logFailure };

if (require.main === module) {
  main();
}
