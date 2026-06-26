import nodeFetch from 'node-fetch';
import fs from 'fs';
import path from 'path';

/**
 * Email primitive — send, receive, and manage email.
 *
 * Outbound: Resend API (ollie@exoagent.xyz or agent@mfer.one)
 * Inbound: Webhook receives JSON from Cloudflare Email Worker
 * Storage: data/inbox/ with index.json + individual message files
 *
 * Requires RESEND_API_KEY in .env
 */

const RESEND_API_URL = 'https://api.resend.com/emails';
const DEFAULT_FROM = 'ollie@exoagent.xyz';

// Inbox storage
const DATA_DIR = path.join(process.cwd(), 'data');
const INBOX_DIR = path.join(DATA_DIR, 'inbox');
const INDEX_FILE = path.join(INBOX_DIR, 'index.json');
const MAX_INBOX_SIZE = 1000;
const MAX_BODY_SIZE = 100 * 1024; // 100KB per email body

// In-memory inbox (loaded from disk on first access)
let inbox = null;
let emailCallbacks = [];

/**
 * Ensure inbox directory exists and load index.
 */
function ensureInbox() {
  if (inbox !== null) return;

  if (!fs.existsSync(INBOX_DIR)) {
    fs.mkdirSync(INBOX_DIR, { recursive: true });
  }

  if (fs.existsSync(INDEX_FILE)) {
    try {
      inbox = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf-8'));
    } catch {
      inbox = [];
    }
  } else {
    inbox = [];
  }
}

/**
 * Save inbox index to disk.
 */
function saveIndex() {
  ensureInbox();
  fs.writeFileSync(INDEX_FILE, JSON.stringify(inbox, null, 2));
}

/**
 * Save an individual email to disk.
 */
function saveEmailFile(emailData) {
  ensureInbox();
  const safeId = sanitizeFilename(emailData.messageId);
  const filePath = path.join(INBOX_DIR, `${safeId}.json`);
  fs.writeFileSync(filePath, JSON.stringify(emailData, null, 2));
}

/**
 * Load an individual email from disk.
 */
function loadEmailFile(messageId) {
  ensureInbox();
  const safeId = sanitizeFilename(messageId);
  const filePath = path.join(INBOX_DIR, `${safeId}.json`);
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

/**
 * Sanitize a message ID for use as a filename.
 */
function sanitizeFilename(id) {
  return id.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').slice(0, 200);
}

// ─── Outbound ─────────────────────────────────────────────

/**
 * Send an email.
 *
 * @param {string} to - Recipient email address
 * @param {string} subject - Email subject
 * @param {string} body - Email body (plain text or HTML)
 * @param {object} [options]
 * @param {string} [options.from] - Sender address (default: ollie@exoagent.xyz)
 * @param {boolean} [options.html] - Treat body as HTML (default: false, auto-detected)
 * @param {string} [options.replyTo] - Reply-to address
 * @param {string[]} [options.cc] - CC recipients
 * @param {string[]} [options.bcc] - BCC recipients
 * @param {string} [options.apiKey] - Resend API key (falls back to RESEND_API_KEY env)
 * @param {object} [options.headers] - Custom headers (e.g. In-Reply-To, References)
 * @returns {object} { success, id, to, subject }
 */
export async function sendEmail(to, subject, body, options = {}) {
  const {
    from = DEFAULT_FROM,
    html: isHtml,
    replyTo,
    cc,
    bcc,
    apiKey,
    headers: customHeaders,
  } = options;

  const resendKey = apiKey || process.env.RESEND_API_KEY;
  if (!resendKey) {
    throw new Error('No Resend API key. Set RESEND_API_KEY in .env');
  }

  if (!to || !subject || !body) {
    throw new Error('sendEmail requires to, subject, and body');
  }

  // Auto-detect HTML
  const bodyIsHtml = isHtml !== undefined ? isHtml : body.includes('<') && body.includes('>');

  const payload = {
    from,
    to: Array.isArray(to) ? to : [to],
    subject,
  };

  if (bodyIsHtml) {
    payload.html = body;
  } else {
    payload.text = body;
  }

  if (replyTo) payload.reply_to = replyTo;
  if (cc) payload.cc = Array.isArray(cc) ? cc : [cc];
  if (bcc) payload.bcc = Array.isArray(bcc) ? bcc : [bcc];
  if (customHeaders) payload.headers = customHeaders;

  console.log(`[email] Sending to ${to}: "${subject}"`);

  const response = await nodeFetch(RESEND_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${resendKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const result = await response.json();

  if (!response.ok) {
    const errorMsg = result.message || result.error || JSON.stringify(result);
    console.log(`[email] Failed: ${errorMsg}`);
    return {
      success: false,
      error: errorMsg,
      statusCode: response.status,
    };
  }

  console.log(`[email] Sent successfully. ID: ${result.id}`);

  return {
    success: true,
    id: result.id,
    to,
    subject,
    from,
  };
}

// ─── Inbound ──────────────────────────────────────────────

/**
 * Receive an incoming email (called by webhook handler).
 *
 * @param {object} emailData - { from, to, subject, body, timestamp, messageId, localPart, inReplyTo, references, date }
 * @returns {object} The stored email entry
 */
export function receiveEmail(emailData) {
  ensureInbox();

  // Sanitize body size
  if (emailData.body && emailData.body.length > MAX_BODY_SIZE) {
    emailData.body = emailData.body.slice(0, MAX_BODY_SIZE) + '\n\n[... truncated]';
  }

  // Build the inbox entry
  const entry = {
    messageId: emailData.messageId || `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
    from: emailData.from,
    to: emailData.to,
    localPart: emailData.localPart || emailData.to?.split('@')[0],
    subject: emailData.subject || '(no subject)',
    timestamp: emailData.timestamp || new Date().toISOString(),
    inReplyTo: emailData.inReplyTo || null,
    references: emailData.references || null,
    read: false,
  };

  // Save the full email to its own file
  saveEmailFile({ ...entry, body: emailData.body });

  // Add to index (without body to keep index small)
  inbox.push(entry);

  // Cap inbox size
  while (inbox.length > MAX_INBOX_SIZE) {
    const removed = inbox.shift();
    // Delete the old email file
    const safeId = sanitizeFilename(removed.messageId);
    const filePath = path.join(INBOX_DIR, `${safeId}.json`);
    try { fs.unlinkSync(filePath); } catch {}
  }

  saveIndex();

  console.log(`[email] Received: ${entry.from} -> ${entry.to} "${entry.subject}"`);

  // Trigger callbacks
  for (const cb of emailCallbacks) {
    try {
      cb({ ...entry, body: emailData.body });
    } catch (err) {
      console.log(`[email] Callback error: ${err.message}`);
    }
  }

  return entry;
}

/**
 * Get inbox entries with optional filtering.
 *
 * @param {object} [options]
 * @param {boolean} [options.unread] - Only unread emails
 * @param {string} [options.from] - Filter by sender (partial match)
 * @param {string} [options.subject] - Filter by subject (partial match)
 * @param {string} [options.localPart] - Filter by recipient local part (agent name)
 * @param {number} [options.limit] - Max results (default: 50)
 * @param {number} [options.offset] - Skip N results (default: 0)
 * @returns {object[]} Array of inbox entries (without body — use readEmail for full content)
 */
export function getInbox(options = {}) {
  ensureInbox();

  let results = [...inbox];

  // Apply filters
  if (options.unread) {
    results = results.filter(e => !e.read);
  }
  if (options.from) {
    const fromLower = options.from.toLowerCase();
    results = results.filter(e => e.from.toLowerCase().includes(fromLower));
  }
  if (options.subject) {
    const subjectLower = options.subject.toLowerCase();
    results = results.filter(e => e.subject.toLowerCase().includes(subjectLower));
  }
  if (options.localPart) {
    const lpLower = options.localPart.toLowerCase();
    results = results.filter(e => e.localPart && e.localPart.toLowerCase() === lpLower);
  }

  // Sort newest first
  results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  // Pagination
  const offset = options.offset || 0;
  const limit = options.limit || 50;
  results = results.slice(offset, offset + limit);

  return results;
}

/**
 * Read a specific email by messageId (returns full content including body).
 *
 * @param {string} messageId
 * @returns {object|null} Full email data or null if not found
 */
export function readEmail(messageId) {
  ensureInbox();
  return loadEmailFile(messageId);
}

/**
 * Mark an email as read.
 *
 * @param {string} messageId
 * @returns {boolean} true if found and updated
 */
export function markRead(messageId) {
  ensureInbox();
  const entry = inbox.find(e => e.messageId === messageId);
  if (!entry) return false;
  entry.read = true;
  saveIndex();
  return true;
}

/**
 * Mark an email as unread.
 *
 * @param {string} messageId
 * @returns {boolean} true if found and updated
 */
export function markUnread(messageId) {
  ensureInbox();
  const entry = inbox.find(e => e.messageId === messageId);
  if (!entry) return false;
  entry.read = false;
  saveIndex();
  return true;
}

/**
 * Get unread email count.
 *
 * @returns {number}
 */
export function getUnreadCount() {
  ensureInbox();
  return inbox.filter(e => !e.read).length;
}

/**
 * Reply to an email with proper threading headers.
 *
 * @param {string} messageId - The message ID to reply to
 * @param {string} body - Reply body
 * @param {object} [options] - Same options as sendEmail (from, html, etc.)
 * @returns {object} sendEmail result
 */
export async function replyToEmail(messageId, body, options = {}) {
  ensureInbox();

  // Load the original email
  const original = loadEmailFile(messageId);
  if (!original) {
    throw new Error(`Email not found: ${messageId}`);
  }

  // Build threading headers
  const headers = {
    'In-Reply-To': original.messageId,
    'References': original.references
      ? `${original.references} ${original.messageId}`
      : original.messageId,
  };

  // Build reply subject
  const subject = original.subject.startsWith('Re:')
    ? original.subject
    : `Re: ${original.subject}`;

  // Reply to the sender, using the original recipient as from address
  const from = options.from || (original.to ? original.to : DEFAULT_FROM);
  const replyTo = options.replyTo || from;

  const result = await sendEmail(original.from, subject, body, {
    ...options,
    from,
    replyTo,
    headers: { ...headers, ...(options.headers || {}) },
  });

  // Mark original as read
  markRead(messageId);

  return result;
}

/**
 * Delete an email from the inbox.
 *
 * @param {string} messageId
 * @returns {boolean} true if found and deleted
 */
export function deleteEmail(messageId) {
  ensureInbox();
  const idx = inbox.findIndex(e => e.messageId === messageId);
  if (idx === -1) return false;

  inbox.splice(idx, 1);
  saveIndex();

  // Delete the file
  const safeId = sanitizeFilename(messageId);
  const filePath = path.join(INBOX_DIR, `${safeId}.json`);
  try { fs.unlinkSync(filePath); } catch {}

  return true;
}

// ─── Event System ─────────────────────────────────────────

/**
 * Register a callback for incoming emails.
 *
 * @param {function} callback - (emailData) => void
 * @returns {function} Unsubscribe function
 */
export function onEmail(callback) {
  emailCallbacks.push(callback);
  return () => {
    emailCallbacks = emailCallbacks.filter(cb => cb !== callback);
  };
}

/**
 * Clear all email callbacks.
 */
export function clearEmailCallbacks() {
  emailCallbacks = [];
}

// ─── Remote Inbox (Cloudflare KV API) ────────────────────

/**
 * Base URL and API key for the Cloudflare KV email worker.
 * Set MFER_EMAIL_API_URL and MFER_EMAIL_API_KEY in .env
 *
 * Production URL: https://mfer-one-email.<account>.workers.dev
 */
const REMOTE_API_URL = process.env.MFER_EMAIL_API_URL || '';
const REMOTE_API_KEY = process.env.MFER_EMAIL_API_KEY || '';

/**
 * Internal helper for remote API calls.
 */
async function remoteRequest(method, path, body = null) {
  if (!REMOTE_API_URL) {
    throw new Error('MFER_EMAIL_API_URL not set in .env');
  }
  if (!REMOTE_API_KEY) {
    throw new Error('MFER_EMAIL_API_KEY not set in .env');
  }

  const url = `${REMOTE_API_URL.replace(/\/$/, '')}${path}`;
  const options = {
    method,
    headers: {
      'X-Api-Key': REMOTE_API_KEY,
      'Content-Type': 'application/json',
    },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await nodeFetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || `Remote API error: ${response.status}`);
  }

  return data;
}

/**
 * Fetch inbox from Cloudflare KV email API.
 *
 * @param {string} name - Local part (e.g., "ollie" for ollie@mfer.one)
 * @param {object} [options]
 * @param {boolean} [options.unread] - Only unread emails
 * @param {string} [options.from] - Filter by sender
 * @param {number} [options.limit] - Max results (default: 50)
 * @param {number} [options.offset] - Skip N results
 * @returns {object} { name, emails, total, offset, limit }
 */
export async function getRemoteInbox(name, options = {}) {
  const params = new URLSearchParams();
  if (options.unread) params.set('unread', 'true');
  if (options.from) params.set('from', options.from);
  if (options.limit) params.set('limit', String(options.limit));
  if (options.offset) params.set('offset', String(options.offset));

  const qs = params.toString();
  const path = `/inbox/${encodeURIComponent(name)}${qs ? '?' + qs : ''}`;
  return await remoteRequest('GET', path);
}

/**
 * Read a specific email from the remote inbox.
 *
 * @param {string} name - Local part
 * @param {string} messageId - The message ID
 * @returns {object} Full email data
 */
export async function readRemoteEmail(name, messageId) {
  return await remoteRequest('GET', `/inbox/${encodeURIComponent(name)}/${encodeURIComponent(messageId)}`);
}

/**
 * Mark a remote email as read.
 *
 * @param {string} name - Local part
 * @param {string} messageId - The message ID
 * @returns {object} { success, messageId, read }
 */
export async function markRemoteRead(name, messageId) {
  return await remoteRequest('POST', `/inbox/${encodeURIComponent(name)}/${encodeURIComponent(messageId)}/read`);
}

/**
 * Delete a remote email.
 *
 * @param {string} name - Local part
 * @param {string} messageId - The message ID
 * @returns {object} { success, messageId, deleted }
 */
export async function deleteRemoteEmail(name, messageId) {
  return await remoteRequest('DELETE', `/inbox/${encodeURIComponent(name)}/${encodeURIComponent(messageId)}`);
}

/**
 * Get unread count from remote inbox.
 *
 * @param {string} name - Local part
 * @returns {object} { name, unread }
 */
export async function getRemoteUnreadCount(name) {
  return await remoteRequest('GET', `/inbox/${encodeURIComponent(name)}/unread`);
}

// ─── Testing Helpers ──────────────────────────────────────

/**
 * Reset inbox state (for testing).
 */
export function _resetInbox() {
  inbox = null;
  emailCallbacks = [];
}

export default {
  // Local
  sendEmail,
  receiveEmail,
  getInbox,
  readEmail,
  markRead,
  markUnread,
  getUnreadCount,
  replyToEmail,
  deleteEmail,
  onEmail,
  clearEmailCallbacks,
  // Remote (Cloudflare KV)
  getRemoteInbox,
  readRemoteEmail,
  markRemoteRead,
  deleteRemoteEmail,
  getRemoteUnreadCount,
};
