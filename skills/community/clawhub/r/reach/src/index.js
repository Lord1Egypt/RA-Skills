import dotenv from 'dotenv';
dotenv.config();

import { fetch } from './primitives/fetch.js';
import { act } from './primitives/act.js';
import { authenticate, getSession, listSessions } from './primitives/authenticate.js';
import { sign, getAddress } from './primitives/sign.js';
import { persist, recall, forget, listKeys } from './primitives/persist.js';
import { observe } from './primitives/observe.js';
import { pay } from './primitives/pay.js';
import { see } from './primitives/see.js';
import { detectCaptcha, solveCaptcha } from './primitives/captcha.js';
import { sendEmail, receiveEmail, getInbox, readEmail, markRead, markUnread, getUnreadCount, replyToEmail, deleteEmail, onEmail, clearEmailCallbacks } from './primitives/email.js';
import { importCookies, getExportInstructions } from './utils/cookie-import.js';
import { SessionRecorder, loadRecording, listRecordings, formatTimeline } from './utils/recorder.js';
import { saveForm, recallForm, getAutoFillData, autoFillPage, extractFormFields, forgetForm, listForms } from './utils/form-memory.js';
import { WebhookServer } from './utils/webhook-server.js';
import { parseCommand, executeCommand } from './natural.js';
import { Router } from './router/router.js';
import pool from './browser.js';

// Site skills
import code4rena from './sites/code4rena.js';
import upwork from './sites/upwork.js';
import github from './sites/github.js';
import immunefi from './sites/immunefi.js';
import exoskeletons from './sites/exoskeletons.js';

// Identity & activity
import { resolveIdentity, attachIdentity } from './utils/exo-identity.js';
import { logActivity, getActivity, getActivitySummary, clearActivity } from './utils/activity-reporter.js';

/**
 * Reach — Agent Web Interface
 *
 * 9 primitives: fetch, act, authenticate, sign, persist, observe, pay, see, email
 * Email inbox: receive, read, reply with threading, event callbacks
 * 1 router: picks the optimal interaction layer for each task
 * 4 site skills: code4rena, upwork, github, immunefi
 * Utilities: cookie import, session recording, form memory, webhook server, natural language
 * MCP server: src/mcp.js (run separately)
 *
 * Usage:
 *   import { Reach } from './src/index.js';
 *   const reach = new Reach();
 *   const content = await reach.fetch('https://example.com');
 *   await reach.close();
 */
class Reach {
  constructor(options = {}) {
    this.router = new Router();
    this.options = options;
    this.recorder = null;

    if (options.wallet?.privateKey) {
      process.env.PRIVATE_KEY = options.wallet.privateKey;
    }

    // Auto-start recording if requested
    if (options.record) {
      this.recorder = new SessionRecorder({ name: options.recordName });
      this.recorder.start();
    }

    // Site skills
    this.sites = {
      code4rena,
      upwork,
      github,
      immunefi,
      exoskeletons,
    };

    // Identity (auto-resolved if wallet provided)
    this.identity = null;
    this._identityPromise = null;

    if (options.wallet?.privateKey) {
      this._identityPromise = this._resolveIdentity();
    }
  }

  /**
   * Auto-resolve Exo identity from the configured wallet.
   * @private
   */
  async _resolveIdentity() {
    try {
      const { ethers } = await import('ethers');
      const wallet = new ethers.Wallet(process.env.PRIVATE_KEY);
      const identity = await resolveIdentity(wallet.address);
      attachIdentity(this, identity);
      if (identity) {
        console.log(`[Reach] Exo identity resolved: ${identity.name || 'Exo #' + identity.primaryExoId} (rep: ${identity.reputation})`);
      }
    } catch (e) {
      // Identity resolution is best-effort — don't block Reach startup
    }
  }

  /**
   * Wait for identity resolution to complete.
   * @returns {object|null} Identity object or null
   */
  async waitForIdentity() {
    if (this._identityPromise) await this._identityPromise;
    return this.identity;
  }

  // --- Primitives ---

  async fetch(url, options = {}) {
    const result = await fetch(url, options);
    this.recorder?.record('fetch', { url, ...options }, result);
    return result;
  }

  async act(url, action, params = {}) {
    const result = await act(url, action, params);
    this.recorder?.record('act', { url, action, ...params }, result);
    return result;
  }

  async authenticate(service, method, credentials = {}) {
    const result = await authenticate(service, method, credentials);
    this.recorder?.record('authenticate', { service, method }, result);
    return result;
  }

  async sign(payload, options = {}) {
    const result = await sign(payload, options);
    this.recorder?.record('sign', { type: options.type || 'message' }, result);
    return result;
  }

  persist(key, value, options = {}) {
    const result = persist(key, value, options);
    this.recorder?.record('persist', { key }, result);
    return result;
  }

  recall(key) {
    const result = recall(key);
    this.recorder?.record('recall', { key }, result);
    return result;
  }

  forget(key) {
    const result = forget(key);
    this.recorder?.record('forget', { key }, result);
    return result;
  }

  // --- Observe ---

  async observe(target, options = {}, callback) {
    const result = await observe(target, options, callback);
    this.recorder?.record('observe', { target, method: options.method || 'auto' }, { id: result.id, method: result.method });
    return result;
  }

  // --- Pay ---

  async pay(recipient, amount, options = {}) {
    const result = await pay(recipient, amount, options);
    this.recorder?.record('pay', { recipient, amount, token: options.token }, result);
    return result;
  }

  // --- Vision ---

  async see(url, question) {
    const result = await see(url, question);
    this.recorder?.record('see', { url, question }, result);
    return result;
  }

  // --- Email ---

  async email(to, subject, body, options = {}) {
    const result = await sendEmail(to, subject, body, options);
    this.recorder?.record('email', { to, subject }, result);
    return result;
  }

  /**
   * Get inbox entries with optional filtering.
   * @param {object} [options] - { unread, from, subject, localPart, limit, offset }
   * @returns {object[]} Array of inbox entries (use readEmail for full body)
   */
  getInbox(options = {}) {
    return getInbox(options);
  }

  /**
   * Read a specific email by messageId (full content including body).
   * @param {string} messageId
   * @returns {object|null}
   */
  readEmail(messageId) {
    return readEmail(messageId);
  }

  /**
   * Mark an email as read.
   * @param {string} messageId
   * @returns {boolean}
   */
  markRead(messageId) {
    return markRead(messageId);
  }

  /**
   * Get unread email count.
   * @returns {number}
   */
  getUnreadCount() {
    return getUnreadCount();
  }

  /**
   * Reply to an email with proper threading headers (In-Reply-To, References).
   * @param {string} messageId - The message ID to reply to
   * @param {string} body - Reply body
   * @param {object} [options] - Same as email() options
   * @returns {object} sendEmail result
   */
  async replyEmail(messageId, body, options = {}) {
    const result = await replyToEmail(messageId, body, options);
    this.recorder?.record('replyEmail', { messageId, bodyLength: body.length }, result);
    return result;
  }

  /**
   * Register a callback for incoming emails.
   * @param {function} callback - (emailData) => void
   * @returns {function} Unsubscribe function
   */
  onEmail(callback) {
    return onEmail(callback);
  }

  // --- CAPTCHA ---

  async detectCaptcha(page) {
    return detectCaptcha(page);
  }

  async solveCaptcha(page) {
    return solveCaptcha(page);
  }

  // --- Cookie Import ---

  importCookies(service, filePath, format = 'auto') {
    return importCookies(service, filePath, format);
  }

  getExportInstructions(browser = 'chrome') {
    return getExportInstructions(browser);
  }

  // --- Natural Language ---

  parseCommand(text) {
    return parseCommand(text);
  }

  async do(text) {
    return executeCommand(text, this);
  }

  // --- Convenience ---

  getAddress(privateKey) {
    return getAddress(privateKey);
  }

  getSession(service) {
    return getSession(service);
  }

  listSessions() {
    return listSessions();
  }

  listKeys() {
    return listKeys();
  }

  // --- Recording ---

  startRecording(name) {
    this.recorder = new SessionRecorder({ name });
    this.recorder.start();
    return this.recorder;
  }

  stopRecording() {
    if (!this.recorder) return null;
    const result = this.recorder.stop();
    this.recorder = null;
    return result;
  }

  // --- Router ---

  route(task) {
    return this.router.route(task);
  }

  /**
   * Execute a task through the router.
   * The router picks the primitive, this method calls it.
   */
  async execute(task) {
    const plan = this.router.route(task);
    console.log(`[Reach] Route: ${plan.primitive}.${plan.method} via ${plan.layer} — ${plan.reason}`);

    switch (plan.primitive) {
      case 'fetch':
        return this.fetch(plan.params.url || task.url, plan.params);
      case 'act':
        return this.act(plan.params.url || task.url, task.params?.action, plan.params);
      case 'authenticate':
        return this.authenticate(plan.params.service, plan.params.method, plan.params.credentials);
      case 'sign':
        return this.sign(task.params?.payload, plan.params);
      case 'persist':
        if (plan.method === 'persist') return this.persist(task.params?.key, task.params?.value, plan.params);
        return this.recall(task.params?.key);
      case 'observe':
        return this.observe(task.url, task.params, task.params?.callback);
      case 'pay':
        return this.pay(task.params?.recipient, task.params?.amount, plan.params);
      default:
        throw new Error(`Unknown primitive: ${plan.primitive}`);
    }
  }

  /**
   * Teach the router about a site.
   */
  learnSite(url, info) {
    this.router.learnSite(url, info);
  }

  // --- Activity Reporter ---

  logActivity(action) {
    // Auto-attach identity name if available
    if (this.identity && !action.identity) {
      action.identity = this.identity.name || `Exo #${this.identity.primaryExoId}`;
    }
    return logActivity(action);
  }

  getActivity(limit, type) {
    return getActivity(limit, type);
  }

  getActivitySummary() {
    return getActivitySummary();
  }

  // --- Lifecycle ---

  async close() {
    if (this.recorder?.isRecording()) {
      this.stopRecording();
    }
    await pool.close();
  }
}

export { Reach };
export default Reach;

// Also export individual primitives for direct use
export { fetch, act, authenticate, sign, persist, recall, forget, observe, pay, see };
export { sendEmail, receiveEmail, getInbox, readEmail, markRead, markUnread, getUnreadCount, replyToEmail, deleteEmail, onEmail } from './primitives/email.js';
export { detectCaptcha, solveCaptcha };
export { importCookies, getExportInstructions };
export { getAddress, getSession, listSessions, listKeys };
export { SessionRecorder, loadRecording, listRecordings, formatTimeline };
export { saveForm, recallForm, getAutoFillData, autoFillPage, extractFormFields, forgetForm, listForms };
export { WebhookServer };
export { parseCommand, executeCommand };

// Export site skills
export { code4rena, upwork, github, immunefi, exoskeletons };
export { resolveIdentity, attachIdentity };
export { logActivity, getActivity, getActivitySummary, clearActivity };
