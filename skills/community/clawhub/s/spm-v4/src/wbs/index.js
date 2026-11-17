/**
 * SPM v4 — WBS (Work Breakdown Structure) ledger management.
 *
 * Parses a WBS Markdown ledger into a structured task collection.
 * Supports loading, updating, adding, and querying tasks with
 * status validation, dependency integrity, and circular-dependency
 * detection.
 *
 * Task fields:
 *   - id              — Unique task identifier (e.g. "WB-001")
 *   - workPackage     — Human-readable title / work description
 *   - dependencies[]  — Array of task IDs this task depends on
 *   - status          — One of: todo | doing | done | blocked | skipped
 *   - contextBrief    — Short description of context / motivation
 *   - exitCriteria    — Conditions that define completion
 *   - evidence        — Proof / artifact references (required when status === 'done')
 *
 * Status transitions:
 *   todo → doing → done | blocked | skipped
 *
 * @module wbs
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve as resolvePath, dirname } from 'node:path';

// ──────────────────────────────────────────────
// Constants
// ──────────────────────────────────────────────

/** Allowed status values. */
export const STATUSES = Object.freeze(['todo', 'doing', 'done', 'blocked', 'skipped']);

/** Allowed status transitions. */
export const STATUS_TRANSITIONS = Object.freeze({
  todo:    ['doing', 'blocked', 'skipped'],
  doing:   ['done', 'blocked', 'skipped'],
  done:    [],
  blocked: ['todo', 'doing'],
  skipped: [],
});

// ──────────────────────────────────────────────
// Errors
// ──────────────────────────────────────────────

/** Error thrown on invalid WBS operations. */
export class WBSError extends Error {
  /**
   * @param {'INVALID_TRANSITION'|'MISSING_DEPENDENCY'|'CIRCULAR_DEPENDENCY'|'NO_EVIDENCE'|'PARSE_ERROR'|'LOAD_ERROR'|'DUPLICATE_TASK'} code    — Machine‑readable error code
   * @param {string} message — Human‑readable description
   * @param {object} [details={}] — Optional metadata (e.g. taskId, status)
   */
  constructor(code, message, details = {}) {
    super(`[${code}] ${message}`);
    this.name = 'WBSError';
    this.code = code;
    this.details = details;
  }
}

// ──────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────

/**
 * Parse a single field line like `- **Field**: value`.
 *
 * @param {string} line — A line from the markdown ledger
 * @returns {{ key: string, value: string } | null}
 */
function parseFieldLine(line) {
  const match = line.match(/^-\s+\*\*([^*]+)\*\*:\s*(.*)$/);
  if (!match) return null;
  return { key: match[1].trim().toLowerCase(), value: match[2].trim() };
}

/**
 * Parse a WBS ledger markdown string into an array of task objects.
 *
 * Expected format:
 * ```md
 * ## WB-001: Work package title
 * - **Status**: doing
 * - **Dependencies**: WB-002, WB-003
 * - **Context**: Brief context description
 * - **Exit Criteria**: Conditions for completion
 * - **Evidence**: Proof of completion
 * ```
 *
 * Fields "Dependencies", "Context", "Exit Criteria", and "Evidence"
 * are optional. If "Dependencies" equals "none", an empty array is used.
 *
 * @param {string} content — Raw markdown ledger content
 * @returns {object[]} Parsed tasks
 * @throws {WBSError} On malformed content
 */
export function parseLedger(content) {
  const lines = content.split('\n');
  /** @type {object[]} */
  const tasks = [];
  /** @type {object|null} */
  let current = null;

  for (const raw of lines) {
    const line = raw.trimEnd();

    // Task heading: ## WB-001: Title
    const headingMatch = line.match(/^##\s+(\S+):\s*(.*)$/);
    if (headingMatch) {
      if (current) {
        validateTaskStructure(current);
        tasks.push(current);
      }
      current = {
        id: headingMatch[1],
        workPackage: headingMatch[2].trim(),
        dependencies: [],
        status: 'todo',
        contextBrief: '',
        exitCriteria: '',
        evidence: '',
      };
      continue;
    }

    if (!current) continue;

    const field = parseFieldLine(line);
    if (!field) continue;

    switch (field.key) {
      case 'status':
        if (STATUSES.includes(field.value.toLowerCase())) {
          current.status = field.value.toLowerCase();
        }
        break;
      case 'dependencies':
        if (field.value.toLowerCase() === 'none' || field.value === '') {
          current.dependencies = [];
        } else {
          current.dependencies = field.value
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean);
        }
        break;
      case 'context':
        current.contextBrief = field.value;
        break;
      case 'exit criteria':
        current.exitCriteria = field.value;
        break;
      case 'evidence':
        current.evidence = field.value;
        break;
      // no default — ignore unrecognised fields
    }
  }

  // Push the last task
  if (current) {
    validateTaskStructure(current);
    tasks.push(current);
  }

  return tasks;
}

/**
 * Basic structural validation for a single parsed task.
 *
 * @param {object} task — Parsed task object
 * @throws {WBSError} If required fields are missing
 */
function validateTaskStructure(task) {
  if (!task.id) {
    throw new WBSError('PARSE_ERROR', 'Task missing id field');
  }
  if (!task.workPackage) {
    throw new WBSError('PARSE_ERROR', `Task "${task.id}" missing work package title`);
  }
}

// ──────────────────────────────────────────────
// WBS Class
// ──────────────────────────────────────────────

export class WBS {
  /** @type {Map<string, object>} */
  #tasks;
  /** @type {string | null} */
  #ledgerPath;

  /**
   * Create a new WBS instance.
   *
   * @param {object} [config={}] — Optional configuration
   * @param {string} [config.ledgerPath] — Default ledger file path
   */
  constructor(config = {}) {
    this.#tasks = new Map();
    this.#ledgerPath = config.ledgerPath ?? null;
  }

  // ── Loading ──────────────────────────────────

  /**
   * Load a WBS ledger from a file path.
   *
   * Reads the file, parses the markdown content, and populates the
   * internal task map. Also validates all dependency references and
   * checks for circular dependencies.
   *
   * @param {string} [filePath] — Path to the markdown ledger file.
   *        Falls back to the path provided at construction time.
   * @returns {object[]} The loaded tasks
   * @throws {WBSError} If file cannot be read, parsed, or validated
   */
  load(filePath) {
    const path = filePath ?? this.#ledgerPath;
    if (!path) {
      throw new WBSError('LOAD_ERROR', 'No ledger path provided');
    }

    let content;
    try {
      content = readFileSync(resolvePath(path), 'utf-8');
    } catch (err) {
      throw new WBSError('LOAD_ERROR', `Cannot read ledger file "${path}": ${err.message}`);
    }

    const tasks = parseLedger(content);
    this.#tasks.clear();

    for (const task of tasks) {
      if (this.#tasks.has(task.id)) {
        throw new WBSError('DUPLICATE_TASK', `Duplicate task id "${task.id}"`);
      }
      this.#tasks.set(task.id, task);
    }

    // Validate dependencies
    this.#validateAllDependencies();
    // Validate no circular dependencies
    this.#detectCircularDependencies();

    this.#ledgerPath = path;
    return this.getAllTasks();
  }

  /**
   * Load WBS tasks directly from a content string (for testing / in-memory use).
   *
   * @param {string} content — Markdown ledger content
   * @returns {object[]} The loaded tasks
   */
  loadFromString(content) {
    const tasks = parseLedger(content);
    this.#tasks.clear();

    for (const task of tasks) {
      if (this.#tasks.has(task.id)) {
        throw new WBSError('DUPLICATE_TASK', `Duplicate task id "${task.id}"`);
      }
      this.#tasks.set(task.id, task);
    }

    this.#validateAllDependencies();
    this.#detectCircularDependencies();

    return this.getAllTasks();
  }

  // ── Task CRUD ────────────────────────────────

  /**
   * Retrieve a single task by id.
   *
   * @param {string} id — Task identifier (e.g. "WB-001")
   * @returns {object | undefined} The task object, or undefined if not found
   */
  getTask(id) {
    const task = this.#tasks.get(id);
    return task ? { ...task } : undefined;
  }

  /**
   * Retrieve all tasks as a shallow-copied array.
   *
   * @returns {object[]} All tasks
   */
  getAllTasks() {
    return Array.from(this.#tasks.values()).map((t) => ({ ...t }));
  }

  /**
   * Add a new task to the ledger.
   *
   * Validates the task structure, default status, checks for duplicate
   * ids, and verifies that all dependency references exist.
   *
   * @param {object} task — The task to add
   * @param {string} task.id — Unique task identifier
   * @param {string} task.workPackage — Work package title
   * @param {string[]} [task.dependencies] — Array of dependency task IDs
   * @param {string} [task.status='todo'] — Current status
   * @param {string} [task.contextBrief=''] — Context description
   * @param {string} [task.exitCriteria=''] — Completion criteria
   * @param {string} [task.evidence=''] — Completion evidence
   * @returns {object} The added task (shallow copy)
   * @throws {WBSError} If task id already exists or dependencies invalid
   */
  addTask(task) {
    const id = task.id;

    if (!id || !task.workPackage) {
      throw new WBSError('PARSE_ERROR', 'Task must have id and workPackage');
    }

    if (this.#tasks.has(id)) {
      throw new WBSError('DUPLICATE_TASK', `Task "${id}" already exists`);
    }

    const normalized = {
      id,
      workPackage: task.workPackage,
      dependencies: Array.isArray(task.dependencies) ? [...task.dependencies] : [],
      status: STATUSES.includes(task.status) ? task.status : 'todo',
      contextBrief: task.contextBrief ?? '',
      exitCriteria: task.exitCriteria ?? '',
      evidence: task.evidence ?? '',
    };

    // Validate that dependency ids exist (but not the new one yet — other tasks
    // can't depend on it before it is added)
    for (const depId of normalized.dependencies) {
      if (!this.#tasks.has(depId)) {
        throw new WBSError(
          'MISSING_DEPENDENCY',
          `Task "${id}" depends on unknown task "${depId}"`,
        );
      }
    }

    // Check that adding this task doesn't create a cycle (temporarily insert
    // and run cycle detection)
    this.#tasks.set(id, normalized);
    try {
      this.#detectCircularDependencies();
    } catch (err) {
      this.#tasks.delete(id);
      throw err;
    }

    return { ...normalized };
  }

  /**
   * Update one or more fields on an existing task.
   *
   * Performs validation on status transitions, requirement that done
   * tasks have evidence, and re-validates dependency integrity after
   * changes.
   *
   * @param {string} taskId — Task identifier to update
   * @param {object} changes — Fields to update (partial task object)
   * @param {string} [changes.status] — New status value
   * @param {string[]} [changes.dependencies] — New dependency array
   * @param {string} [changes.workPackage] — New work package title
   * @param {string} [changes.contextBrief] — New context
   * @param {string} [changes.exitCriteria] — New exit criteria
   * @param {string} [changes.evidence] — New evidence
   * @returns {object} The updated task (shallow copy)
   * @throws {WBSError} If task not found or validation fails
   */
  update(taskId, changes) {
    const task = this.#tasks.get(taskId);
    if (!task) {
      throw new WBSError(
        'MISSING_DEPENDENCY',
        `Cannot update: task "${taskId}" not found`,
        { taskId },
      );
    }

    // Validate status transition
    if (changes.status && changes.status !== task.status) {
      const allowed = STATUS_TRANSITIONS[task.status];
      if (!allowed || !allowed.includes(changes.status)) {
        throw new WBSError(
          'INVALID_TRANSITION',
          `Cannot transition task "${taskId}" from "${task.status}" to "${changes.status}"`,
          { taskId, from: task.status, to: changes.status },
        );
      }
    }

    // Apply changes to a working copy for dependency validation
    const updatedDeps = changes.dependencies ?? task.dependencies;
    for (const depId of updatedDeps) {
      if (!this.#tasks.has(depId) && depId !== taskId) {
        throw new WBSError(
          'MISSING_DEPENDENCY',
          `Task "${taskId}" depends on unknown task "${depId}"`,
          { taskId, dependencyId: depId },
        );
      }
    }

    // Check for cycles (temporarily update deps, run cycle detection)
    if (changes.dependencies) {
      const origDeps = task.dependencies;
      task.dependencies = [...changes.dependencies];
      try {
        this.#detectCircularDependencies();
      } catch (err) {
        task.dependencies = origDeps;
        throw err;
      }
    }

    // Apply all remaining changes
    if (changes.status !== undefined) task.status = changes.status;
    if (changes.workPackage !== undefined) task.workPackage = changes.workPackage;
    if (changes.dependencies !== undefined) task.dependencies = [...changes.dependencies];
    if (changes.contextBrief !== undefined) task.contextBrief = changes.contextBrief;
    if (changes.exitCriteria !== undefined) task.exitCriteria = changes.exitCriteria;
    if (changes.evidence !== undefined) task.evidence = changes.evidence;

    // Validate done tasks have evidence
    if (task.status === 'done' && !task.evidence) {
      throw new WBSError(
        'NO_EVIDENCE',
        `Task "${taskId}" is done but has no evidence`,
        { taskId },
      );
    }

    return { ...task };
  }

  // ── Serialization ────────────────────────────

  /**
   * Serialize all tasks back to the markdown ledger format.
   *
   * @returns {string} Markdown representation of the WBS ledger
   */
  serialize() {
    const tasks = this.getAllTasks();
    const lines = ['# SPM WBS Ledger', ''];

    for (const t of tasks) {
      lines.push(`## ${t.id}: ${t.workPackage}`);
      lines.push(`- **Status**: ${t.status}`);
      lines.push(
        `- **Dependencies**: ${t.dependencies.length > 0 ? t.dependencies.join(', ') : 'none'}`,
      );
      if (t.contextBrief) lines.push(`- **Context**: ${t.contextBrief}`);
      if (t.exitCriteria) lines.push(`- **Exit Criteria**: ${t.exitCriteria}`);
      if (t.evidence) lines.push(`- **Evidence**: ${t.evidence}`);
      lines.push('');
    }

    return lines.join('\n');
  }

  // ── Internal validation ──────────────────────

  /**
   * Validate that all dependency references point to existing tasks.
   *
   * @throws {WBSError} If any dependency is missing
   */
  #validateAllDependencies() {
    for (const [id, task] of this.#tasks) {
      for (const depId of task.dependencies) {
        if (!this.#tasks.has(depId)) {
          throw new WBSError(
            'MISSING_DEPENDENCY',
            `Task "${id}" depends on unknown task "${depId}"`,
            { taskId: id, dependencyId: depId },
          );
        }
      }
    }
  }

  /**
   * Detect circular dependencies among all tasks using DFS.
   *
   * @throws {WBSError} If a cycle is found
   */
  #detectCircularDependencies() {
    const visited = new Set();
    const inStack = new Set();

    /**
     * DFS traversal to find cycles.
     * @param {string} nodeId
     * @throws {WBSError} On cycle detection
     */
    const dfs = (nodeId) => {
      visited.add(nodeId);
      inStack.add(nodeId);

      const task = this.#tasks.get(nodeId);
      if (task) {
        for (const depId of task.dependencies) {
          if (!visited.has(depId)) {
            dfs(depId);
          } else if (inStack.has(depId)) {
            throw new WBSError(
              'CIRCULAR_DEPENDENCY',
              `Circular dependency detected involving tasks "${[...inStack].join(' → ')} → ${depId}"`,
              { cycle: [...inStack, depId] },
            );
          }
        }
      }

      inStack.delete(nodeId);
    };

    for (const id of this.#tasks.keys()) {
      if (!visited.has(id)) {
        dfs(id);
      }
    }
  }
}