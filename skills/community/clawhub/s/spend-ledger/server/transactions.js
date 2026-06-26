import { createHash, randomBytes } from "node:crypto";
import { readFileSync, appendFileSync, existsSync, mkdirSync, openSync, closeSync, unlinkSync } from "node:fs";
import { dirname, resolve } from "node:path";

const DEFAULT_LOG_PATH = resolve(
  process.env.SPEND_LEDGER_LOG ||
    new URL("../data/transactions.jsonl", import.meta.url).pathname
);

// ── File locking ──────────────────────────────────────────────────────────────
// The hash chain requires read-prev-hash → compute → append to be atomic
// across processes. We use an O_EXCL lockfile to serialize writers.

function acquireLock(logPath, retries = 20, delayMs = 50) {
  const lockPath = logPath + ".lock";
  for (let i = 0; i < retries; i++) {
    try {
      const fd = openSync(lockPath, "wx"); // O_WRONLY | O_CREAT | O_EXCL
      closeSync(fd);
      return lockPath;
    } catch (err) {
      if (err.code !== "EEXIST") throw err;
      // Lock held by another process — busy wait
      const deadline = Date.now() + delayMs;
      while (Date.now() < deadline) { /* spin */ }
    }
  }
  throw new Error(`Could not acquire lock on ${logPath} after ${retries} retries`);
}

function releaseLock(lockPath) {
  try { unlinkSync(lockPath); } catch { /* already gone */ }
}

function sha256(data) {
  return createHash("sha256").update(data).digest("hex");
}

function generateId() {
  const ts = Math.floor(Date.now() / 1000);
  const rand = randomBytes(2).toString("hex");
  return `txn_${ts}_${rand}`;
}

/**
 * Read the last line of the JSONL log to get the previous hash.
 * Returns "genesis" if the log is empty or doesn't exist.
 */
function getLastHash(logPath) {
  if (!existsSync(logPath)) return "genesis";
  const content = readFileSync(logPath, "utf-8").trimEnd();
  if (!content) return "genesis";
  const lines = content.split("\n");
  const lastLine = lines[lines.length - 1];
  return sha256(lastLine);
}

/**
 * Check if a transaction with the given tx_hash or idempotency_key already exists.
 *
 * @param {string|null} txHash
 * @param {string|null} idempotencyKey
 * @param {string} logPath
 * @returns {boolean}
 */
function isDuplicate(txHash, idempotencyKey, logPath) {
  if (!txHash && !idempotencyKey) return false;
  const txns = readAllTransactions(logPath);
  return txns.some(
    (t) =>
      (txHash && t.tx_hash === txHash) ||
      (idempotencyKey && t.idempotency_key === idempotencyKey)
  );
}

/**
 * Append a transaction record to the JSONL log with hash chaining.
 * Deduplicates by tx_hash and idempotency_key — returns null if duplicate found.
 *
 * @param {object} txn - Transaction fields (service, amount, context, etc.)
 * @param {string} [logPath] - Path to the JSONL log file
 * @returns {object|null} The complete transaction record, or null if deduplicated
 */
export function appendTransaction(txn, logPath = DEFAULT_LOG_PATH) {
  const dir = dirname(logPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  const lockPath = acquireLock(logPath);
  try {
    // Deduplication — must happen inside the lock so we see the latest state
    if (isDuplicate(txn.tx_hash || null, txn.idempotency_key || null, logPath)) {
      return null;
    }

    const prevHash = getLastHash(logPath);

    const record = {
      id: txn.id || generateId(),
      timestamp: txn.timestamp || new Date().toISOString(),
      prev_hash: `sha256:${prevHash}`,
      service: txn.service || { url: null, name: "unknown", category: null },
      amount: txn.amount || { value: "0", currency: "unknown", chain: null },
      tx_hash: txn.tx_hash || null,
      idempotency_key: txn.idempotency_key || null,
      receipt_url: txn.receipt_url || null,
      confirmation_id: txn.confirmation_id || null,
      context: {
        session_key: null,
        skill: null,
        user_request: null,
        tool_name: null,
        tool_args_summary: null,
        input_hash: null,
        ...txn.context,
      },
      execution_time_ms: txn.execution_time_ms ?? null,
      failure_type: txn.failure_type || null,
      status: txn.status || "confirmed",
      source: txn.source || "auto",
    };

    const line = JSON.stringify(record);
    appendFileSync(logPath, line + "\n", { mode: 0o600 });

    return record;
  } finally {
    releaseLock(lockPath);
  }
}

/**
 * Read all transactions from the JSONL log.
 *
 * @param {string} [logPath] - Path to the JSONL log file
 * @returns {object[]} Array of transaction records
 */
export function readAllTransactions(logPath = DEFAULT_LOG_PATH) {
  if (!existsSync(logPath)) return [];
  const content = readFileSync(logPath, "utf-8").trimEnd();
  if (!content) return [];
  return content.split("\n").map((line) => JSON.parse(line));
}

/**
 * Query transactions with optional filters.
 *
 * @param {object} filters
 * @param {string} [filters.from] - ISO date string, inclusive start
 * @param {string} [filters.to] - ISO date string, inclusive end
 * @param {string} [filters.service] - Substring match on service name or URL
 * @param {string} [filters.skill] - Substring match on triggering skill
 * @param {string} [filters.status] - Exact match on status
 * @param {string} [filters.source] - Exact match on source ("auto" or "manual")
 * @param {string} [logPath]
 * @returns {object[]} Filtered transaction records
 */
export function queryTransactions(filters = {}, logPath = DEFAULT_LOG_PATH) {
  let txns = readAllTransactions(logPath);

  if (filters.from) {
    const from = new Date(filters.from);
    txns = txns.filter((t) => new Date(t.timestamp) >= from);
  }
  if (filters.to) {
    const to = new Date(filters.to);
    // Date-only strings parse as midnight UTC; extend to end of that day
    if (!filters.to.includes("T")) to.setUTCHours(23, 59, 59, 999);
    txns = txns.filter((t) => new Date(t.timestamp) <= to);
  }
  if (filters.service) {
    const s = filters.service.toLowerCase();
    txns = txns.filter(
      (t) =>
        (t.service?.name || "").toLowerCase().includes(s) ||
        (t.service?.url || "").toLowerCase().includes(s)
    );
  }
  if (filters.skill) {
    const sk = filters.skill.toLowerCase();
    txns = txns.filter((t) =>
      (t.context?.skill || "").toLowerCase().includes(sk)
    );
  }
  if (filters.status) {
    txns = txns.filter((t) => t.status === filters.status);
  }
  if (filters.source) {
    txns = txns.filter((t) => t.source === filters.source);
  }

  return txns;
}

/**
 * Compute summary rollups from a list of transactions.
 *
 * @param {object[]} txns - Transaction records
 * @param {"daily"|"weekly"|"monthly"} period
 * @returns {object} { periods: { [key]: { total, count, currency } }, grand_total, grand_count }
 */
export function summarize(txns, period = "daily") {
  const buckets = {};

  for (const t of txns) {
    const d = new Date(t.timestamp);
    let key;
    if (period === "daily") {
      key = d.toISOString().slice(0, 10);
    } else if (period === "weekly") {
      const day = d.getDay() || 7;
      const monday = new Date(d);
      monday.setDate(d.getDate() - day + 1);
      key = `week-${monday.toISOString().slice(0, 10)}`;
    } else {
      key = d.toISOString().slice(0, 7);
    }

    if (!buckets[key]) buckets[key] = { total: 0, count: 0, currency: null };
    buckets[key].total += parseFloat(t.amount?.value || "0");
    buckets[key].count += 1;
    if (t.amount?.currency) buckets[key].currency = t.amount.currency;
  }

  for (const b of Object.values(buckets)) {
    b.total = Math.round(b.total * 1e8) / 1e8;
  }

  const grandTotal =
    Math.round(
      txns.reduce((sum, t) => sum + parseFloat(t.amount?.value || "0"), 0) *
        1e8
    ) / 1e8;

  return {
    periods: buckets,
    grand_total: grandTotal,
    grand_count: txns.length,
  };
}

/**
 * Group transactions by a field and compute totals.
 *
 * @param {object[]} txns
 * @param {"service"|"skill"|"tool"} field
 * @returns {object[]} Array of { name, total, count, currency }, sorted by total desc
 */
export function groupBy(txns, field = "service") {
  const groups = {};

  for (const t of txns) {
    let key;
    if (field === "service") key = t.service?.name || t.service?.url || "unknown";
    else if (field === "skill") key = t.context?.skill || "unknown";
    else if (field === "tool") key = t.context?.tool_name || "unknown";
    else key = "unknown";

    if (!groups[key]) groups[key] = { name: key, total: 0, count: 0, currency: null };
    groups[key].total += parseFloat(t.amount?.value || "0");
    groups[key].count += 1;
    if (t.amount?.currency) groups[key].currency = t.amount.currency;
  }

  const result = Object.values(groups);
  for (const g of result) {
    g.total = Math.round(g.total * 1e8) / 1e8;
  }
  return result.sort((a, b) => b.total - a.total);
}

/**
 * Verify the hash chain integrity of the transaction log.
 *
 * @param {string} [logPath]
 * @returns {{ valid: boolean, brokenAt: number|null, total: number }}
 */
export function verifyChain(logPath = DEFAULT_LOG_PATH) {
  const txns = readAllTransactions(logPath);
  if (txns.length === 0) return { valid: true, brokenAt: null, total: 0 };

  if (txns[0].prev_hash !== "sha256:genesis") {
    return { valid: false, brokenAt: 0, total: txns.length };
  }

  const lines = readFileSync(logPath, "utf-8").trimEnd().split("\n");

  for (let i = 1; i < txns.length; i++) {
    const expectedHash = `sha256:${sha256(lines[i - 1])}`;
    if (txns[i].prev_hash !== expectedHash) {
      return { valid: false, brokenAt: i, total: txns.length };
    }
  }

  return { valid: true, brokenAt: null, total: txns.length };
}

/**
 * Export transactions to CSV format.
 *
 * @param {object[]} txns
 * @returns {string} CSV string
 */
export function toCSV(txns) {
  const headers = [
    "id",
    "timestamp",
    "service_name",
    "service_url",
    "amount",
    "currency",
    "chain",
    "tx_hash",
    "receipt_url",
    "confirmation_id",
    "skill",
    "tool",
    "execution_time_ms",
    "failure_type",
    "status",
    "source",
  ];

  const rows = txns.map((t) =>
    [
      t.id,
      t.timestamp,
      t.service?.name || "",
      t.service?.url || "",
      t.amount?.value || "0",
      t.amount?.currency || "",
      t.amount?.chain || "",
      t.tx_hash || "",
      t.receipt_url || "",
      t.confirmation_id || "",
      t.context?.skill || "",
      t.context?.tool_name || "",
      t.execution_time_ms ?? "",
      t.failure_type || "",
      t.status,
      t.source || "auto",
    ]
      .map((v) => `"${String(v).replace(/"/g, '""')}"`)
      .join(",")
  );

  return [headers.join(","), ...rows].join("\n");
}

/**
 * Compute a SHA-256 hash of the input arguments for loop detection.
 *
 * @param {string|object} toolArgs
 * @returns {string} hex hash
 */
export function hashInput(toolArgs) {
  const str = typeof toolArgs === "string" ? toolArgs : JSON.stringify(toolArgs || "");
  return sha256(str);
}
