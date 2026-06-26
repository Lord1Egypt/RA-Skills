/**
 * Session Password - Core Authentication Module v1.0.0
 * Author: squallsol
 * 
 * Implements: timeout check, failed attempt lockout, auto-refresh, email recovery
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

const PASSPHRASE_FILE = path.join(MEMORY_DIR, 'passphrase.json');
const AUTH_STATE_FILE = path.join(MEMORY_DIR, 'auth-state.json');
const AUDIT_LOG_FILE = path.join(MEMORY_DIR, 'auth-audit.log');

// ═══════════════════════════════════════════════════
// File Operations
// ═══════════════════════════════════════════════════

function loadJson(file, defaultValue = {}) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return defaultValue;
  }
}

function saveJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  fs.chmodSync(file, 0o600);
}

function appendLog(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  fs.appendFileSync(AUDIT_LOG_FILE, logLine);
}

// ═══════════════════════════════════════════════════
// Core Functions
// ═══════════════════════════════════════════════════

/**
 * Get current authentication state
 */
function getAuthState() {
  return loadJson(AUTH_STATE_FILE, {
    authenticated: false,
    authenticatedAt: null,
    lastActiveAt: null,
    failedAttempts: 0,
    lockedUntil: null
  });
}

/**
 * Get passphrase configuration
 */
function getConfig() {
  return loadJson(PASSPHRASE_FILE, {
    timeoutMinutes: 60,
    autoRefresh: true
  });
}

/**
 * Check if session is locked due to failed attempts
 */
function isLocked() {
  const state = getAuthState();
  if (!state.lockedUntil) return { locked: false };
  
  const now = Date.now();
  if (now < state.lockedUntil) {
    const remainingMs = state.lockedUntil - now;
    const remainingMin = Math.ceil(remainingMs / 60000);
    return { locked: true, remainingMinutes: remainingMin };
  }
  
  // Lock expired, reset
  state.lockedUntil = null;
  state.failedAttempts = 0;
  saveJson(AUTH_STATE_FILE, state);
  return { locked: false };
}

/**
 * Check if authentication has timed out
 */
function isTimedOut() {
  const state = getAuthState();
  const config = getConfig();
  
  if (!state.authenticated || !state.lastActiveAt) {
    return { timedOut: true, reason: 'not_authenticated' };
  }
  
  const timeoutMs = (config.timeoutMinutes || 60) * 60 * 1000;
  const now = Date.now();
  const elapsed = now - state.lastActiveAt;
  
  if (elapsed > timeoutMs) {
    const elapsedMin = Math.floor(elapsed / 60000);
    return { timedOut: true, elapsedMinutes: elapsedMin, configTimeout: config.timeoutMinutes };
  }
  
  return { timedOut: false, elapsedMinutes: Math.floor(elapsed / 60000) };
}

/**
 * Refresh lastActiveAt (auto-refresh)
 */
function refreshActivity() {
  const config = getConfig();
  if (!config.autoRefresh) return false;
  
  const state = getAuthState();
  if (!state.authenticated) return false;
  
  state.lastActiveAt = Date.now();
  saveJson(AUTH_STATE_FILE, state);
  return true;
}

/**
 * Record failed authentication attempt
 * Returns lock info if threshold reached
 */
function recordFailedAttempt() {
  const state = getAuthState();
  state.failedAttempts = (state.failedAttempts || 0) + 1;
  
  const MAX_ATTEMPTS = 5;
  const LOCK_DURATION_MS = 15 * 60 * 1000; // 15 minutes
  
  if (state.failedAttempts >= MAX_ATTEMPTS) {
    state.lockedUntil = Date.now() + LOCK_DURATION_MS;
    saveJson(AUTH_STATE_FILE, state);
    appendLog(`LOCKOUT: Failed attempts reached ${MAX_ATTEMPTS}`);
    return { locked: true, lockDurationMinutes: 15 };
  }
  
  saveJson(AUTH_STATE_FILE, state);
  appendLog(`FAILED_AUTH: Attempt ${state.failedAttempts}/${MAX_ATTEMPTS}`);
  return { locked: false, attemptsRemaining: MAX_ATTEMPTS - state.failedAttempts };
}

/**
 * Record successful authentication
 */
function recordSuccess() {
  const state = {
    authenticated: true,
    authenticatedAt: Date.now(),
    lastActiveAt: Date.now(),
    failedAttempts: 0,
    lockedUntil: null
  };
  saveJson(AUTH_STATE_FILE, state);
  appendLog('AUTH_SUCCESS');
  return state;
}

/**
 * Clear authentication (logout)
 */
function clearAuth() {
  const state = {
    authenticated: false,
    authenticatedAt: null,
    lastActiveAt: null,
    failedAttempts: 0,
    lockedUntil: null
  };
  saveJson(AUTH_STATE_FILE, state);
  appendLog('AUTH_CLEARED');
  return state;
}

/**
 * Verify passphrase using SHA256 or bcrypt
 */
function verifyPassphrase(input) {
  const config = getConfig();
  const hash = config.passphraseHash;
  
  if (!hash) {
    return { valid: false, error: 'no_passphrase_configured' };
  }
  
  // Detect hash algorithm
  if (hash.startsWith('$2b$') || hash.startsWith('$2a$')) {
    // bcrypt hash
    try {
      const bcrypt = require('bcrypt');
      const valid = bcrypt.compareSync(input, hash);
      return { valid, algorithm: 'bcrypt' };
    } catch (e) {
      return { valid: false, error: 'bcrypt_not_available' };
    }
  } else {
    // SHA256 hash
    const inputHash = crypto.createHash('sha256').update(input).digest('hex');
    const valid = inputHash === hash;
    return { valid, algorithm: 'sha256' };
  }
}

/**
 * Verify security answer
 */
function verifySecurityAnswer(input) {
  const config = getConfig();
  const hash = config.securityAnswerHash;
  
  if (!hash) {
    return { valid: false, error: 'no_security_question_configured' };
  }
  
  if (hash.startsWith('$2b$') || hash.startsWith('$2a$')) {
    try {
      const bcrypt = require('bcrypt');
      return { valid: bcrypt.compareSync(input, hash), algorithm: 'bcrypt' };
    } catch (e) {
      return { valid: false, error: 'bcrypt_not_available' };
    }
  } else {
    const inputHash = crypto.createHash('sha256').update(input).digest('hex');
    return { valid: inputHash === hash, algorithm: 'sha256' };
  }
}

/**
 * Get security question
 */
function getSecurityQuestion() {
  const config = getConfig();
  return config.securityQuestion || null;
}

/**
 * Get recovery email
 */
function getRecoveryEmail() {
  const config = getConfig();
  return config.securityEmail || null;
}

/**
 * Full authentication check (for heartbeat)
 * Returns status and required action
 */
function checkAuthStatus() {
  // Check lock first
  const lockStatus = isLocked();
  if (lockStatus.locked) {
    return {
      ok: false,
      action: 'locked',
      message: `账户已锁定，请 ${lockStatus.remainingMinutes} 分钟后重试`
    };
  }
  
  // Check timeout
  const timeoutStatus = isTimedOut();
  if (timeoutStatus.timedOut) {
    if (timeoutStatus.reason === 'not_authenticated') {
      return {
        ok: false,
        action: 'authenticate',
        message: '请输入口令以继续'
      };
    }
    
    // Clear expired auth
    clearAuth();
    return {
      ok: false,
      action: 'reauthenticate',
      message: `认证已超时（超过 ${timeoutStatus.elapsedMinutes} 分钟），请重新输入口令`
    };
  }
  
  // Auth valid - refresh activity
  refreshActivity();
  
  return {
    ok: true,
    action: 'none',
    elapsedMinutes: timeoutStatus.elapsedMinutes
  };
}

// ═══════════════════════════════════════════════════
// CLI Interface
// ═══════════════════════════════════════════════════

if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'status':
      console.log(JSON.stringify(checkAuthStatus(), null, 2));
      break;
      
    case 'verify':
      const password = args[1];
      if (!password) {
        console.log(JSON.stringify({ error: 'password_required' }, null, 2));
        process.exit(1);
      }
      console.log(JSON.stringify(verifyPassphrase(password), null, 2));
      break;
      
    case 'refresh':
      const refreshed = refreshActivity();
      console.log(JSON.stringify({ refreshed }, null, 2));
      break;
      
    case 'clear':
      clearAuth();
      console.log(JSON.stringify({ cleared: true }, null, 2));
      break;
      
    default:
      console.log(`
Usage: node auth-core.js <command>

Commands:
  status    - Check authentication status
  verify <password> - Verify passphrase
  refresh   - Refresh lastActiveAt
  clear     - Clear authentication state
`);
  }
}

module.exports = {
  getAuthState,
  getConfig,
  isLocked,
  isTimedOut,
  refreshActivity,
  recordFailedAttempt,
  recordSuccess,
  clearAuth,
  verifyPassphrase,
  verifySecurityAnswer,
  getSecurityQuestion,
  getRecoveryEmail,
  checkAuthStatus,
  appendLog
};
