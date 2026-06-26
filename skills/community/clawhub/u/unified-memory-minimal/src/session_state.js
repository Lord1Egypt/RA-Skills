/**
 * session_state.js - Session State RAM Layer
 * 
 * Manages SESSION-STATE.md at workspace root (survives compaction).
 * Provides hot RAM layer for current task context, key decisions, and pending actions.
 * Inspired by Elite Longterm Memory's session state approach.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const SESSION_STATE_FILE = join(WORKSPACE, 'SESSION-STATE.md');

// Ensure workspace directory exists
if (!existsSync(WORKSPACE)) {
  mkdirSync(WORKSPACE, { recursive: true });
}

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} SessionAction
 * @property {string} text
 * @property {boolean} done
 * @property {string} created_at
 */

/**
 * @typedef {Object} SessionState
 * @property {string|null} task
 * @property {Record<string, string>} context
 * @property {SessionAction[]} actions
 * @property {string} updated_at
 */

// ============================================================================
// Markdown Serialization
// ============================================================================

/**
 * Serialize SessionState to markdown format
 * @param {SessionState} state
 * @returns {string}
 */
function serializeMarkdown(state) {
  const lines = ['# SESSION-STATE.md', ''];
  
  lines.push('## Current Task');
  lines.push(state.task || '_No active task_');
  lines.push('');
  
  lines.push('## Key Context');
  if (Object.keys(state.context).length === 0) {
    lines.push('_No context recorded_');
  } else {
    for (const [key, value] of Object.entries(state.context)) {
      lines.push(`- ${key}: ${value}`);
    }
  }
  lines.push('');
  
  lines.push('## Pending Actions');
  if (state.actions.length === 0) {
    lines.push('_No pending actions_');
  } else {
    for (const action of state.actions) {
      const checkbox = action.done ? '[x]' : '[ ]';
      lines.push(`- ${checkbox} ${action.text}`);
    }
  }
  lines.push('');
  
  return lines.join('\n');
}

/**
 * Parse markdown format to SessionState
 * @param {string} content
 * @returns {SessionState}
 */
function parseMarkdown(content) {
  const state = {
    task: null,
    context: {},
    actions: [],
    updated_at: new Date().toISOString(),
  };
  
  if (!content || !content.trim()) return state;
  
  const lines = content.split('\n');
  let currentSection = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    
    // Detect section headers
    if (trimmed === '## Current Task') {
      currentSection = 'task';
      continue;
    }
    if (trimmed === '## Key Context') {
      currentSection = 'context';
      continue;
    }
    if (trimmed === '## Pending Actions') {
      currentSection = 'actions';
      continue;
    }
    
    // Skip empty lines and non-content
    if (!trimmed || trimmed === '# SESSION-STATE.md') continue;
    
    if (currentSection === 'task') {
      if (trimmed !== '_No active task_') {
        state.task = trimmed;
      }
    } else if (currentSection === 'context') {
      // Parse: "- key: value"
      const match = trimmed.match(/^-\s+(.+?):\s+(.+)$/);
      if (match) {
        state.context[match[1]] = match[2];
      }
    } else if (currentSection === 'actions') {
      // Parse: "- [x] action text" or "- [ ] action text"
      const actionMatch = trimmed.match(/^-\s+\[([ x])\]\s+(.+)$/);
      if (actionMatch) {
        state.actions.push({
          done: actionMatch[1] === 'x',
          text: actionMatch[2],
          created_at: state.updated_at,
        });
      }
    }
  }
  
  return state;
}

// ============================================================================
// File Operations
// ============================================================================

/**
 * Load session state from SESSION-STATE.md
 * @returns {SessionState}
 */
function loadState() {
  try {
    if (!existsSync(SESSION_STATE_FILE)) {
      return getDefaultState();
    }
    const content = readFileSync(SESSION_STATE_FILE, 'utf-8');
    return parseMarkdown(content);
  } catch (err) {
    console.error(`[session_state] Failed to load: ${err.message}`);
    return getDefaultState();
  }
}

/**
 * Save session state to SESSION-STATE.md
 * @param {SessionState} state
 */
function saveState(state) {
  try {
    state.updated_at = new Date().toISOString();
    const content = serializeMarkdown(state);
    writeFileSync(SESSION_STATE_FILE, content, 'utf-8');
  } catch (err) {
    console.error(`[session_state] Failed to save: ${err.message}`);
  }
}

/**
 * Get default empty state
 * @returns {SessionState}
 */
function getDefaultState() {
  return {
    task: null,
    context: {},
    actions: [],
    updated_at: new Date().toISOString(),
  };
}

// ============================================================================
// Public API
// ============================================================================

/**
 * Update the current task
 * @param {string} task
 */
export function setCurrentTask(task) {
  const state = loadState();
  state.task = task;
  saveState(state);
}

/**
 * Add a key-context pair to the context section
 * @param {string} key
 * @param {string} value
 */
export function addContext(key, value) {
  const state = loadState();
  state.context[key] = value;
  saveState(state);
}

/**
 * Add a pending action
 * @param {string} action
 */
export function addAction(action) {
  const state = loadState();
  state.actions.push({
    text: action,
    done: false,
    created_at: new Date().toISOString(),
  });
  saveState(state);
}

/**
 * Mark an action as complete (matches by text content)
 * @param {string} actionText
 * @returns {boolean} true if found and marked done
 */
export function completeAction(actionText) {
  const state = loadState();
  const normalizedSearch = actionText.trim().toLowerCase();
  
  const action = state.actions.find(a => 
    a.text.toLowerCase() === normalizedSearch ||
    a.text.toLowerCase().includes(normalizedSearch) ||
    normalizedSearch.includes(a.text.toLowerCase())
  );
  
  if (action) {
    action.done = true;
    saveState(state);
    return true;
  }
  return false;
}

/**
 * Read and return the current session state
 * @returns {SessionState}
 */
export function getSessionState() {
  return loadState();
}

/**
 * Clear all session state (reset to defaults)
 */
export function clearState() {
  saveState(getDefaultState());
}

// ============================================================================
// MCP Tool Handler
// ============================================================================

/**
 * Handle memory_session MCP tool calls
 * @param {object} args
 * @param {string} [args.action]
 * @param {string} [args.task]
 * @param {string} [args.key]
 * @param {string} [args.value]
 * @param {string} [args.action_text]
 * @returns {Promise<{content: Array<{type: string, text: string}>, isError?: boolean}>}
 */
export async function memorySessionTool(args) {
  const { action } = args;
  
  try {
    switch (action) {
      case 'get': {
        const state = getSessionState();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(state, null, 2),
          }],
        };
      }
      
      case 'set_task': {
        if (!args.task) {
          return { content: [{ type: 'text', text: 'Error: task is required' }], isError: true };
        }
        setCurrentTask(args.task);
        return { content: [{ type: 'text', text: JSON.stringify({ success: true, task: args.task }) }] };
      }
      
      case 'add_context': {
        if (!args.key) {
          return { content: [{ type: 'text', text: 'Error: key is required' }], isError: true };
        }
        if (!args.value) {
          return { content: [{ type: 'text', text: 'Error: value is required' }], isError: true };
        }
        addContext(args.key, args.value);
        return { content: [{ type: 'text', text: JSON.stringify({ success: true, key: args.key, value: args.value }) }] };
      }
      
      case 'add_action': {
        if (!args.action_text) {
          return { content: [{ type: 'text', text: 'Error: action_text is required' }], isError: true };
        }
        addAction(args.action_text);
        return { content: [{ type: 'text', text: JSON.stringify({ success: true, action: args.action_text }) }] };
      }
      
      case 'complete_action': {
        if (!args.action_text) {
          return { content: [{ type: 'text', text: 'Error: action_text is required' }], isError: true };
        }
        const found = completeAction(args.action_text);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: found, action_text: args.action_text, message: found ? 'Action marked as done' : 'Action not found' }),
          }],
        };
      }
      
      case 'clear': {
        clearState();
        return { content: [{ type: 'text', text: JSON.stringify({ success: true, message: 'Session state cleared' }) }] };
      }
      
      default:
        return {
          content: [{ type: 'text', text: `Error: Unknown action '${action}'. Valid actions: get, set_task, add_context, add_action, complete_action, clear` }],
          isError: true,
        };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Session state error: ${err.message}` }], isError: true };
  }
}

export default { memorySessionTool };
