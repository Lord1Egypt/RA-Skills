/**
 * git_notes.js - Enhanced Git Notes Integration for Permanent Knowledge Storage
 *
 * Stores decisions, learnings, and context as git notes attached to commits.
 * Branch-aware: tracks which branch notes were created on.
 *
 * Data structure stored in notes/refs:
 * {
 *   commit: string,
 *   category: 'decision' | 'learning' | 'context',
 *   content: string,
 *   branch: string,
 *   created_at: string,
 *   tags: string[]
 * }
 *
 * @module git_notes
 */

import { execSync, exec } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = join(fileURLToPath(import.meta.url), '..');
const WORKSPACE = process.env.HOME || '/root';

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} GitNote
 * @property {string} commit
 * @property {string} category  // 'decision', 'learning', 'context'
 * @property {string} content
 * @property {string} branch
 * @property {string} created_at
 * @property {string[]} tags
 */

// ============================================================================
// Git Helpers
// ============================================================================

/**
 * Run a git command, return stdout or throw
 * @param {string[]} args
 * @param {string} [cwd]
 * @returns {string}
 */
function gitExec(args, cwd = WORKSPACE) {
  const cmd = ['git', ...args];
  try {
    return execSync(cmd.join(' '), {
      cwd,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    }).trim();
  } catch (err) {
    throw new Error(`Git error: ${err.stderr || err.message}`);
  }
}

/**
 * Check if we're in a git repo
 * @returns {boolean}
 */
function isGitRepo(cwd = WORKSPACE) {
  try {
    execSync('git rev-parse --git-dir', { cwd, stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Get current branch name
 * @param {string} [cwd]
 * @returns {string}
 */
function getCurrentBranch(cwd = WORKSPACE) {
  try {
    return gitExec(['branch', '--show-current'], cwd);
  } catch {
    return 'unknown';
  }
}

/**
 * Get the default notes ref name (without "refs/notes/")
 */
const NOTES_REF = 'memory';

// ============================================================================
// Note Serialization
// ============================================================================

/**
 * Build a structured note object
 * @param {string} commitHash
 * @param {string} content
 * @param {string} [category]
 * @param {string[]} [tags]
 * @returns {GitNote}
 */
function buildNote(commitHash, content, category = 'context', tags = []) {
  return {
    commit: commitHash,
    category,
    content,
    branch: getCurrentBranch(),
    created_at: new Date().toISOString(),
    tags,
  };
}

/**
 * Serialize a GitNote to string for storing in git note
 * @param {GitNote} note
 * @returns {string}
 */
function serializeNote(note) {
  return JSON.stringify(note);
}

/**
 * Deserialize a note from git note content
 * @param {string} raw
 * @returns {GitNote|null}
 */
function deserializeNote(raw) {
  try {
    const note = JSON.parse(raw);
    if (!note.commit || !note.content) return null;
    return note;
  } catch {
    return null;
  }
}

// ============================================================================
// Core Git Notes Operations
// ============================================================================

/**
 * Add a decision note to a commit
 * @param {string} commitHash - Target commit hash (or 'HEAD' for current)
 * @param {string} decision - Decision text
 * @param {string} [category='decision'] - Category: decision, learning, context
 * @returns {Promise<string>} - The commit hash the note was attached to
 */
export async function addDecisionNote(commitHash, decision, category = 'decision') {
  if (!isGitRepo()) {
    throw new Error('Not a git repository');
  }

  const note = buildNote(commitHash, decision, category);
  const noteContent = serializeNote(note);

  // Use git notes add with -m flag for inline content
  try {
    gitExec(['notes', '--ref', NOTES_REF, 'add', commitHash, '-f', '-m', noteContent]);
  } catch (err) {
    // If note already exists and -f didn't work, try removing first
    try {
      gitExec(['notes', '--ref', NOTES_REF, 'remove', commitHash]);
    } catch {
      // Ignore remove errors
    }
    gitExec(['notes', '--ref', NOTES_REF, 'add', commitHash, '-m', noteContent]);
  }

  return commitHash;
}

/**
 * Show the note attached to a commit
 * @param {string} commitHash
 * @returns {Promise<string|null>} - Note content or null if no note
 */
export async function showNote(commitHash) {
  if (!isGitRepo()) {
    return null;
  }

  try {
    const raw = gitExec(['notes', '--ref', NOTES_REF, 'show', commitHash]);
    const note = deserializeNote(raw);
    return note ? note.content : raw;
  } catch {
    return null;
  }
}

/**
 * List all notes, optionally filtered by category
 * @param {{ category?: string, limit?: number }} [options]
 * @returns {Promise<Array<{commit: string, note: string, category?: string, created_at: string}>>}
 */
export async function listNotes(options = {}) {
  const { category, limit = 100 } = options;

  if (!isGitRepo()) {
    return [];
  }

  try {
    // Get list of all commits that have notes
    const output = gitExec(['notes', '--ref', NOTES_REF, 'list']);
    if (!output) return [];

    const lines = output.split('\n').filter(Boolean).slice(0, limit);
    const results = [];

    for (const line of lines) {
      // Format: "<commit hash>\n<note content>"
      const parts = line.split(/\s+/);
      const commitHash = parts[0];

      try {
        const raw = gitExec(['notes', '--ref', NOTES_REF, 'show', commitHash]);
        const note = deserializeNote(raw);

        if (note) {
          // Filter by category if specified
          if (category && note.category !== category) continue;

          results.push({
            commit: note.commit,
            note: note.content,
            category: note.category,
            created_at: note.created_at,
            branch: note.branch,
            tags: note.tags || [],
          });
        } else {
          // Raw note (no structured format)
          results.push({
            commit: commitHash,
            note: raw,
            created_at: new Date().toISOString(),
          });
        }
      } catch {
        // Skip commits with unreadable notes
      }
    }

    return results;
  } catch {
    return [];
  }
}

/**
 * Add a tag to an existing note on a commit
 * @param {string} commitHash
 * @param {string} tag
 * @returns {Promise<void>}
 */
export async function tagNote(commitHash, tag) {
  if (!isGitRepo()) {
    throw new Error('Not a git repository');
  }

  // Get existing note
  let note;
  try {
    const raw = gitExec(['notes', '--ref', NOTES_REF, 'show', commitHash]);
    note = deserializeNote(raw);
  } catch {
    throw new Error(`No note found on commit ${commitHash}`);
  }

  if (!note) {
    throw new Error(`No structured note found on commit ${commitHash}`);
  }

  // Add tag if not already present
  if (!note.tags) note.tags = [];
  if (!note.tags.includes(tag)) {
    note.tags.push(tag);
  }

  // Update the note
  const noteContent = serializeNote(note);
  try {
    gitExec(['notes', '--ref', NOTES_REF, 'remove', commitHash]);
  } catch {
    // Ignore
  }
  gitExec(['notes', '--ref', NOTES_REF, 'add', commitHash, '-m', noteContent]);
}

/**
 * Get all notes grouped by branch
 * @returns {Promise<Array<{branch: string, notes: GitNote[]}>>}
 */
export async function getBranchNotes() {
  if (!isGitRepo()) {
    return [];
  }

  const allNotes = await listNotes({ limit: 500 });
  const branchMap = new Map();

  for (const note of allNotes) {
    const branch = note.branch || 'unknown';
    if (!branchMap.has(branch)) {
      branchMap.set(branch, []);
    }
    branchMap.get(branch).push(note);
  }

  return Array.from(branchMap.entries()).map(([branch, notes]) => ({
    branch,
    notes,
  }));
}

/**
 * Search notes content for a query string
 * @param {string} query
 * @returns {Promise<GitNote[]>}
 */
export async function searchNotes(query) {
  if (!isGitRepo()) {
    return [];
  }

  const allNotes = await listNotes({ limit: 500 });
  const lowerQuery = query.toLowerCase();

  return allNotes.filter(note => {
    const contentMatch = note.note?.toLowerCase().includes(lowerQuery);
    const tagMatch = note.tags?.some(t => t.toLowerCase().includes(lowerQuery));
    const categoryMatch = note.category?.toLowerCase().includes(lowerQuery);
    return contentMatch || tagMatch || categoryMatch;
  });
}

// ============================================================================
// MCP Tool Handler
// ============================================================================

/**
 * Handle memory_git_notes MCP tool calls
 * @param {object} args
 * @param {string} [args.action] - add|show|list|tag|branch_notes|search
 * @param {string} [args.commit_hash] - Commit hash (for add|show|tag)
 * @param {string} [args.decision] - Decision text (for add)
 * @param {string} [args.category] - Category (for add, default: decision)
 * @param {string} [args.tag] - Tag to add (for tag action)
 * @param {string} [args.query] - Search query (for search action)
 * @param {number} [args.limit] - Max results (for list, default: 100)
 * @returns {Promise<{content: Array<{type: string, text: string}>, isError?: boolean}>}
 */
export async function memoryGitNotesTool(args) {
  const { action } = args;

  try {
    // Handle non-async actions first
    if (!isGitRepo()) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ error: 'Not a git repository', hint: 'Initialize git in the workspace to use git notes' }) }],
        isError: true,
      };
    }

    switch (action) {
      case 'add': {
        if (!args.commit_hash) {
          return { content: [{ type: 'text', text: 'Error: commit_hash is required for add action' }], isError: true };
        }
        if (!args.decision) {
          return { content: [{ type: 'text', text: 'Error: decision is required for add action' }], isError: true };
        }
        const commitHash = await addDecisionNote(args.commit_hash, args.decision, args.category || 'decision');
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: true,
              commit: commitHash,
              category: args.category || 'decision',
              branch: getCurrentBranch(),
              created_at: new Date().toISOString(),
            }),
          }],
        };
      }

      case 'show': {
        if (!args.commit_hash) {
          return { content: [{ type: 'text', text: 'Error: commit_hash is required for show action' }], isError: true };
        }
        const note = await showNote(args.commit_hash);
        if (!note) {
          return { content: [{ type: 'text', text: JSON.stringify({ commit: args.commit_hash, note: null, message: 'No note found on this commit' }) }] };
        }
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              commit: args.commit_hash,
              note,
              category: 'context',
              branch: getCurrentBranch(),
            }),
          }],
        };
      }

      case 'list': {
        const notes = await listNotes({ category: args.category, limit: args.limit || 100 });
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              count: notes.length,
              current_branch: getCurrentBranch(),
              notes,
            }, null, 2),
          }],
        };
      }

      case 'tag': {
        if (!args.commit_hash) {
          return { content: [{ type: 'text', text: 'Error: commit_hash is required for tag action' }], isError: true };
        }
        if (!args.tag) {
          return { content: [{ type: 'text', text: 'Error: tag is required for tag action' }], isError: true };
        }
        await tagNote(args.commit_hash, args.tag);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: true,
              commit: args.commit_hash,
              tag: args.tag,
              message: `Tag '${args.tag}' added to note on ${args.commit_hash}`,
            }),
          }],
        };
      }

      case 'branch_notes': {
        const branchNotes = await getBranchNotes();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              current_branch: getCurrentBranch(),
              branches: branchNotes,
            }, null, 2),
          }],
        };
      }

      case 'search': {
        if (!args.query) {
          return { content: [{ type: 'text', text: 'Error: query is required for search action' }], isError: true };
        }
        const results = await searchNotes(args.query);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              query: args.query,
              count: results.length,
              results,
            }, null, 2),
          }],
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Error: Unknown action '${action}'. Valid actions: add, show, list, tag, branch_notes, search` }],
          isError: true,
        };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Git notes error [${action}]: ${err.message}` }], isError: true };
  }
}

export default { memoryGitNotesTool };
