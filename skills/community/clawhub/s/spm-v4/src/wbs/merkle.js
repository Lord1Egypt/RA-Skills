/**
 * SPM v4 — Merkle tree for incremental WBS hashing.
 *
 * Builds a Merkle tree from WBS task objects. Each task node is
 * hashed individually (SHA-256 of its canonical representation).
 * The root hash is SHA-256 of the concatenation of all leaf hashes,
 * sorted by task ID for determinism.
 *
 * Enables pinpoint tampering detection: if a single task is altered,
 * only that node's hash and the root hash change.
 *
 * @module wbs/merkle
 */

import { createHash } from 'node:crypto';

// ──────────────────────────────────────────────
// Types (JSDoc)
// ──────────────────────────────────────────────

/**
 * @typedef {Object} MerkleNode
 * @property {string} id      — Task identifier (e.g. "WB-001")
 * @property {string} hash    — SHA-256 hex digest of this node
 * @property {string} content — Canonical string used to produce the hash
 */

/**
 * @typedef {Object} MerkleTree
 * @property {string} rootHash   — SHA-256 of the concatenated leaf hashes
 * @property {number} nodeCount  — Number of leaf nodes
 * @property {string} timestamp  — ISO-8601 timestamp of when the tree was built
 * @property {Map<string, MerkleNode>} nodes — Map of task ID → MerkleNode
 */

// ──────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────

/**
 * Build the canonical string representation of a task for hashing.
 *
 * Uses a deterministic field order regardless of object key ordering.
 *
 * @param {object} task — A WBS task with id, workPackage, dependencies,
 *        status, contextBrief, exitCriteria, evidence
 * @returns {string} Canonical string
 */
function canonicalTask(task) {
  const deps = Array.isArray(task.dependencies)
    ? [...task.dependencies].sort().join(',')
    : '';

  return [
    `id:${task.id}`,
    `wp:${task.workPackage ?? ''}`,
    `deps:${deps}`,
    `status:${task.status ?? ''}`,
    `ctx:${task.contextBrief ?? ''}`,
    `exit:${task.exitCriteria ?? ''}`,
    `ev:${task.evidence ?? ''}`,
  ].join('|');
}

/**
 * Compute the SHA-256 hex digest of a string.
 *
 * @param {string} data — Input data
 * @returns {string} Hex-encoded SHA-256 (64 characters)
 */
function sha256(data) {
  return createHash('sha-256').update(data, 'utf-8').digest('hex');
}

// ──────────────────────────────────────────────
// MerkleTree Class
// ──────────────────────────────────────────────

export class MerkleTree {
  /** @type {Map<string, MerkleNode>} */
  #nodes;
  /** @type {string | null} */
  #rootHash;
  /** @type {number} */
  #nodeCount;
  /** @type {string} */
  #timestamp;

  /**
   * Create an empty Merkle tree.
   */
  constructor() {
    this.#nodes = new Map();
    this.#rootHash = null;
    this.#nodeCount = 0;
    this.#timestamp = new Date().toISOString();
  }

  /**
   * Build the Merkle tree from an array of WBS tasks.
   *
   * Each task is hashed individually. The root hash is computed as
   * SHA-256 of all leaf hashes concatenated in sorted task-ID order.
   *
   * Calling `buildTree` resets any previously built tree state.
   *
   * @param {object[]} tasks — Array of WBS task objects
   * @returns {MerkleTree} A frozen snapshot of the built tree
   */
  buildTree(tasks) {
    this.#nodes.clear();
    this.#timestamp = new Date().toISOString();

    // Sort tasks by id for deterministic ordering
    const sorted = [...tasks].sort((a, b) => String(a.id).localeCompare(String(b.id)));

    for (const task of sorted) {
      const content = canonicalTask(task);
      const hash = sha256(content);
      this.#nodes.set(task.id, { id: task.id, hash, content });
    }

    this.#nodeCount = this.#nodes.size;

    // Compute root hash from all leaf hashes in sorted order
    const leafHashes = sorted
      .map((t) => this.#nodes.get(t.id).hash)
      .join('');
    this.#rootHash = this.#nodes.size > 0 ? sha256(leafHashes) : null;

    return this.getSnapshot();
  }

  /**
   * Verify that a specific task's hash matches its current state.
   *
   * Recomputes the hash for the given task and compares it against
   * the stored node hash in the tree.
   *
   * @param {string} taskId    — Task identifier to verify
   * @param {object} taskData  — Current task data to compute hash from
   * @returns {{ valid: boolean, expected: string, actual: string }}
   *          `valid` is true iff the computed hash matches the stored hash.
   *          `expected` is the hash stored in the tree.
   *          `actual` is the hash computed from the provided task data.
   * @throws {Error} If taskId is not in the tree
   */
  verifyNode(taskId, taskData) {
    const node = this.#nodes.get(taskId);
    if (!node) {
      throw new Error(`verifyNode: task "${taskId}" not found in Merkle tree`);
    }

    const content = canonicalTask(taskData);
    const actual = sha256(content);

    return {
      valid: actual === node.hash,
      expected: node.hash,
      actual,
    };
  }

  /**
   * Get the root hash of the Merkle tree.
   *
   * @returns {string | null} The root hash, or `null` if the tree is empty
   */
  getRootHash() {
    return this.#rootHash;
  }

  /**
   * Get a frozen snapshot of the current Merkle tree.
   *
   * @returns {MerkleTree} Snapshot with rootHash, nodeCount, timestamp, and nodes map
   */
  getSnapshot() {
    const nodesObj = {};
    for (const [id, node] of this.#nodes) {
      nodesObj[id] = { ...node };
    }

    return Object.freeze({
      rootHash: this.#rootHash,
      nodeCount: this.#nodeCount,
      timestamp: this.#timestamp,
      nodes: nodesObj,
    });
  }

  /**
   * Generate a human-readable summary of the Merkle tree.
   *
   * @returns {string} Summary text
   */
  summarize() {
    const lines = [
      'Merkle Tree Summary',
      `  Root Hash: ${this.#rootHash ?? '— (empty tree)'}`,
      `  Node Count: ${this.#nodeCount}`,
      `  Timestamp: ${this.#timestamp}`,
      '',
    ];

    const sortedIds = [...this.#nodes.keys()].sort();
    for (const id of sortedIds) {
      const node = this.#nodes.get(id);
      lines.push(`  ${id}: ${node.hash.slice(0, 16)}...`);
    }

    return lines.join('\n');
  }

  /**
   * Export the tree data for serialization (e.g., writing to disk).
   *
   * @returns {object} Plain object representation
   */
  toJSON() {
    const nodes = {};
    for (const [id, node] of this.#nodes) {
      nodes[id] = { ...node };
    }

    return {
      rootHash: this.#rootHash,
      nodeCount: this.#nodeCount,
      timestamp: this.#timestamp,
      nodes,
    };
  }

  /**
   * Import tree data from a previously exported JSON object.
   *
   * @param {object} json — Object with the same shape as `toJSON()` output
   * @returns {void}
   */
  fromJSON(json) {
    this.#nodes.clear();
    this.#rootHash = json.rootHash ?? null;
    this.#nodeCount = json.nodeCount ?? 0;
    this.#timestamp = json.timestamp ?? new Date().toISOString();

    if (json.nodes) {
      for (const [id, node] of Object.entries(json.nodes)) {
        this.#nodes.set(id, { id: String(node.id), hash: String(node.hash), content: String(node.content) });
      }
    }
  }
}

// ──────────────────────────────────────────────
// Standalone Functions
// ──────────────────────────────────────────────

/**
 * Convenience: build a Merkle tree from tasks and return its root hash.
 *
 * @param {object[]} tasks — Array of WBS task objects
 * @returns {string | null} Root SHA-256 hex digest
 *
 * @example
 * import { buildTree, getRootHash } from './merkle.js';
 * const tree = new MerkleTree();
 * tree.buildTree(tasks);
 * console.log('Root:', tree.getRootHash());
 */
export { MerkleTree as MerkleWBS };

/**
 * Compute the hash for a single task without building a full tree.
 *
 * Useful for quick verifications or when only one task's integrity
 * needs checking.
 *
 * @param {object} task — A WBS task object
 * @returns {string} SHA-256 hex digest of the task's canonical form
 *
 * @example
 * import { hashTask } from './merkle.js';
 * const h = hashTask({ id: 'WB-001', workPackage: 'Init' });
 * console.log(h); // "abc123..."
 */
export function hashTask(task) {
  const content = canonicalTask(task);
  return sha256(content);
}