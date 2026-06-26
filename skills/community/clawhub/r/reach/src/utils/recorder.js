import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RECORDINGS_DIR = path.join(__dirname, '..', '..', 'data', 'recordings');

fs.mkdirSync(RECORDINGS_DIR, { recursive: true });

/**
 * Session Recorder — records every action Reach takes for replay/audit.
 *
 * Usage:
 *   const recorder = new SessionRecorder();
 *   recorder.start();
 *   recorder.record('fetch', { url: 'https://example.com' }, result);
 *   const log = recorder.stop();
 */
class SessionRecorder {
  constructor(options = {}) {
    this.name = options.name || `session-${Date.now()}`;
    this.entries = [];
    this.recording = false;
    this.startTime = null;
    this.metadata = options.metadata || {};
  }

  /**
   * Start recording.
   */
  start() {
    this.recording = true;
    this.startTime = Date.now();
    this.entries = [];
    console.log(`[recorder] Session started: ${this.name}`);
    return this;
  }

  /**
   * Record an action.
   *
   * @param {string} action - Action name (e.g. 'fetch', 'act', 'authenticate')
   * @param {object} input - Input parameters
   * @param {*} output - Result of the action
   * @param {object} [meta] - Additional metadata
   */
  record(action, input = {}, output = null, meta = {}) {
    if (!this.recording) return;

    const entry = {
      timestamp: new Date().toISOString(),
      elapsed: Date.now() - this.startTime,
      action,
      input: sanitizeInput(input),
      output: summarizeOutput(output),
      ...meta,
    };

    this.entries.push(entry);
    return entry;
  }

  /**
   * Record an error.
   */
  recordError(action, input, error) {
    return this.record(action, input, null, {
      error: error.message || String(error),
      stack: error.stack?.split('\n').slice(0, 3).join('\n'),
    });
  }

  /**
   * Stop recording and save to file.
   *
   * @returns {object} { name, entries, duration, file }
   */
  stop() {
    this.recording = false;
    const duration = Date.now() - this.startTime;

    const session = {
      name: this.name,
      startedAt: new Date(this.startTime).toISOString(),
      stoppedAt: new Date().toISOString(),
      duration,
      durationHuman: formatDuration(duration),
      entryCount: this.entries.length,
      metadata: this.metadata,
      entries: this.entries,
    };

    // Save to file
    const filename = `${this.name}.json`;
    const filepath = path.join(RECORDINGS_DIR, filename);
    fs.writeFileSync(filepath, JSON.stringify(session, null, 2));

    console.log(`[recorder] Session stopped: ${this.name} (${this.entries.length} entries, ${session.durationHuman})`);
    console.log(`[recorder] Saved: ${filepath}`);

    return { ...session, file: filepath };
  }

  /**
   * Get current entries without stopping.
   */
  getEntries() {
    return [...this.entries];
  }

  /**
   * Is the recorder currently recording?
   */
  isRecording() {
    return this.recording;
  }
}

/**
 * Load a saved session recording.
 *
 * @param {string} nameOrPath - Session name or full file path
 * @returns {object} Session data
 */
export function loadRecording(nameOrPath) {
  let filepath;

  if (path.isAbsolute(nameOrPath)) {
    filepath = nameOrPath;
  } else {
    // Try exact filename
    filepath = path.join(RECORDINGS_DIR, nameOrPath);
    if (!fs.existsSync(filepath)) {
      // Try with .json extension
      filepath = path.join(RECORDINGS_DIR, `${nameOrPath}.json`);
    }
  }

  if (!fs.existsSync(filepath)) {
    throw new Error(`Recording not found: ${nameOrPath}`);
  }

  return JSON.parse(fs.readFileSync(filepath, 'utf-8'));
}

/**
 * List all saved recordings.
 *
 * @returns {Array<{ name, file, startedAt, entryCount, duration }>}
 */
export function listRecordings() {
  if (!fs.existsSync(RECORDINGS_DIR)) return [];

  const files = fs.readdirSync(RECORDINGS_DIR).filter(f => f.endsWith('.json'));
  const recordings = [];

  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(RECORDINGS_DIR, file), 'utf-8'));
      recordings.push({
        name: data.name,
        file,
        startedAt: data.startedAt,
        entryCount: data.entryCount,
        duration: data.durationHuman,
      });
    } catch {
      recordings.push({ name: file, file, error: 'Could not parse' });
    }
  }

  return recordings.sort((a, b) => (b.startedAt || '').localeCompare(a.startedAt || ''));
}

/**
 * Format a recording as a human-readable timeline.
 *
 * @param {object} session - Session data from loadRecording
 * @returns {string} Formatted timeline
 */
export function formatTimeline(session) {
  const lines = [];

  lines.push(`Session: ${session.name}`);
  lines.push(`Started: ${session.startedAt}`);
  lines.push(`Duration: ${session.durationHuman}`);
  lines.push(`Actions: ${session.entryCount}`);
  lines.push('');
  lines.push('Timeline:');
  lines.push('-'.repeat(60));

  for (const entry of session.entries) {
    const time = `+${formatDuration(entry.elapsed)}`;
    const action = entry.action.toUpperCase().padEnd(12);
    const icon = entry.error ? 'X' : 'O';

    let detail = '';
    if (entry.input?.url) {
      detail = entry.input.url;
    } else if (entry.input?.key) {
      detail = `key="${entry.input.key}"`;
    } else if (entry.input?.service) {
      detail = `service=${entry.input.service}`;
    } else if (entry.input?.target) {
      detail = entry.input.target;
    } else {
      detail = JSON.stringify(entry.input).substring(0, 60);
    }

    lines.push(`  ${time.padEnd(10)} [${icon}] ${action} ${detail}`);

    if (entry.error) {
      lines.push(`             ERROR: ${entry.error}`);
    }

    if (entry.output) {
      const summary = typeof entry.output === 'string'
        ? entry.output.substring(0, 80)
        : JSON.stringify(entry.output).substring(0, 80);
      lines.push(`             -> ${summary}`);
    }
  }

  lines.push('-'.repeat(60));
  return lines.join('\n');
}

/**
 * Sanitize input for recording — remove sensitive data.
 */
function sanitizeInput(input) {
  if (!input || typeof input !== 'object') return input;

  const sanitized = { ...input };

  // Remove sensitive fields
  const sensitiveKeys = ['password', 'privateKey', 'apiKey', 'secret', 'token', 'credentials'];
  for (const key of sensitiveKeys) {
    if (key in sanitized) {
      sanitized[key] = '[REDACTED]';
    }
    // Check nested credentials object
    if (sanitized.credentials && typeof sanitized.credentials === 'object') {
      const creds = { ...sanitized.credentials };
      for (const k of sensitiveKeys) {
        if (k in creds) creds[k] = '[REDACTED]';
      }
      sanitized.credentials = creds;
    }
  }

  return sanitized;
}

/**
 * Summarize output for recording — truncate large data.
 */
function summarizeOutput(output) {
  if (output === null || output === undefined) return null;

  if (typeof output === 'string') {
    return output.length > 500 ? output.substring(0, 500) + '...' : output;
  }

  if (typeof output === 'object') {
    const summary = {};
    for (const [key, value] of Object.entries(output)) {
      if (typeof value === 'string' && value.length > 200) {
        summary[key] = value.substring(0, 200) + '...';
      } else if (Array.isArray(value)) {
        summary[key] = `[Array(${value.length})]`;
      } else {
        summary[key] = value;
      }
    }
    return summary;
  }

  return output;
}

/**
 * Format milliseconds to human-readable duration.
 */
function formatDuration(ms) {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  const mins = Math.floor(ms / 60000);
  const secs = Math.floor((ms % 60000) / 1000);
  return `${mins}m${secs}s`;
}

export { SessionRecorder, RECORDINGS_DIR };
export default SessionRecorder;
