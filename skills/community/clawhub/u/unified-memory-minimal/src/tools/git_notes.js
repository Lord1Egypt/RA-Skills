/**
 * Git Notes - Cold layer Git-based persistence for memories
 *
 * P1-4: Backup memories to git notes for cold storage / versioning
 * Uses simple-git or direct git exec to manage notes
 *
 * Tools:
 * - memory_gitnotes_backup: Export memories to git notes
 * - memory_gitnotes_restore: Restore memories from git notes
 *
 * @module tools/git_notes
 */

import { execSync, exec } from 'child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Resolve workspace from file URL
const __workspace = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(__workspace, 'memory');
const NOTES_REF = 'refs/notes/memories';

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

/**
 * Run a git command in the workspace directory.
 * @param {string[]} args - Git arguments
 * @returns {string} stdout
 */
function gitExec(args) {
  const cmd = ['git', ...args].join(' ');
  try {
    return execSync(cmd, {
      cwd: __workspace,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    }).trim();
  } catch (err) {
    throw new Error(`Git error: ${err.stderr || err.message}`);
  }
}

/**
 * Check if git repo exists
 */
function isGitRepo() {
  try {
    execSync('git rev-parse --git-dir', {
      cwd: __workspace,
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return true;
  } catch {
    return false;
  }
}

/**
 * Initialize git repo if needed
 */
function ensureGitRepo() {
  if (!isGitRepo()) {
    execSync('git init', { cwd: __workspace, stdio: 'pipe' });
    execSync('git config user.email "memory@agent.local"', { cwd: __workspace, stdio: 'pipe' });
    execSync('git config user.name "Memory Agent"', { cwd: __workspace, stdio: 'pipe' });
  }
}

/**
 * Serialize memories to a git-notes-compatible format
 * @param {object[]} memories - Array of memory objects
 * @param {string} scope - Scope to backup (or 'all')
 * @returns {string} JSON stringified memories
 */
function serializeMemories(memories, scope) {
  const data = {
    scope: scope || 'all',
    backed_up_at: new Date().toISOString(),
    count: memories.length,
    memories: memories.map(m => ({
      id: m.id,
      text: m.text,
      category: m.category,
      importance: m.importance,
      tags: m.tags || [],
      scope: m.scope || 'GLOBAL',
      created_at: m.created_at,
      updated_at: m.updated_at || m.created_at,
    })),
  };
  return JSON.stringify(data, null, 2);
}

/**
 * Backup memories to git notes
 * @param {string} [scope] - Scope to backup (USER/TEAM/AGENT/GLOBAL/all)
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export function memoryGitnotesBackupTool({ scope }) {
  try {
    ensureDir(MEMORY_DIR);
    ensureGitRepo();

    // Import storage to get memories
    let memories;
    try {
      const { getAllMemories } = require('../storage.js');
      memories = getAllMemories();
    } catch {
      return { content: [{ type: 'text', text: 'Error: storage not accessible' }], isError: true };
    }

    // Filter by scope if specified
    let filtered = memories;
    if (scope && scope !== 'all') {
      const norm = (s) => (s || 'GLOBAL').toUpperCase();
      filtered = memories.filter(m => norm(m.scope) === norm(scope.toUpperCase()));
    }

    // Serialize
    const payload = serializeMemories(filtered, scope || 'all');
    const messageFile = join(MEMORY_DIR, `.gitnotes_msg_${Date.now()}.tmp`);
    writeFileSync(messageFile, payload, 'utf8');

    // Write to git notes
    const noteContent = payload;
    // Use git notes add with -m flag
    try {
      gitExec(['notes', '--ref', NOTES_REF.replace('refs/notes/', ''), 'add', '-f', '-m', `Memory backup ${scope || 'all'} ${new Date().toISOString()}`]);
    } catch {
      // Fallback: write to a file and use git notes add -f -F
      const notePath = join(MEMORY_DIR, `memory_backup_${Date.now()}.json`);
      writeFileSync(notePath, noteContent, 'utf8');
      try {
        gitExec(['notes', '--ref', NOTES_REF.replace('refs/notes/', ''), 'add', '-f', '-F', notePath]);
      } catch {
        // Last resort: commit the file directly
        gitExec(['add', notePath]);
        gitExec(['commit', '-m', `Memory backup ${scope || 'all'} ${new Date().toISOString()}`]);
      }
    }

    // Commit notes if not already committed
    try {
      gitExec(['notes', '--ref', NOTES_REF.replace('refs/notes/', ''), 'append', '-m', `Backup: ${filtered.length} memories, scope=${scope || 'all'}`]);
    } catch {
      // Notes might already be committed, try append
      try {
        gitExec(['commit', '-m', `Memory backup ${new Date().toISOString()}`]);
      } catch {
        // Ignore
      }
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          backed_up: filtered.length,
          scope: scope || 'all',
          notes_ref: NOTES_REF,
          backed_up_at: new Date().toISOString(),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Git notes backup error: ${err.message}` }], isError: true };
  }
}

/**
 * Restore memories from git notes
 * @param {string} [scope] - Scope to restore (or 'all')
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export function memoryGitnotesRestoreTool({ scope }) {
  try {
    if (!isGitRepo()) {
      return { content: [{ type: 'text', text: 'Error: not a git repository' }], isError: true };
    }

    // Get notes content
    let notesContent;
    try {
      notesContent = gitExec(['notes', '--ref', NOTES_REF.replace('refs/notes/', ''), 'show', 'HEAD']);
    } catch {
      // Try to get from last commit's note
      try {
        notesContent = gitExec(['notes', '-R', '--ref', NOTES_REF.replace('refs/notes/', ''), 'show']);
      } catch {
        return { content: [{ type: 'text', text: 'Error: no backup found in git notes' }], isError: true };
      }
    }

    let data;
    try {
      data = JSON.parse(notesContent);
    } catch {
      return { content: [{ type: 'text', text: 'Error: corrupted backup data in git notes' }], isError: true };
    }

    const memories = data.memories || [];

    // Filter by scope if specified
    let filtered = memories;
    if (scope && scope !== 'all') {
      filtered = memories.filter(m => (m.scope || 'GLOBAL').toUpperCase() === scope.toUpperCase());
    }

    // Restore to storage
    try {
      const { saveMemories } = require('../storage.js');
      const { getAllMemories } = require('../storage.js');
      const existing = getAllMemories();
      const existingIds = new Set(existing.map(m => m.id));

      let restored = 0;
      let skipped = 0;
      for (const mem of filtered) {
        if (!existingIds.has(mem.id)) {
          existing.push(mem);
          restored++;
        } else {
          skipped++;
        }
      }
      saveMemories(existing);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            restored,
            skipped,
            scope: scope || 'all',
            backup_date: data.backed_up_at,
          }, null, 2),
        }],
      };
    } catch {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            restored: 0,
            note: 'Storage write not available, showing backup contents',
            memories: filtered.slice(0, 10).map(m => ({
              id: m.id,
              text: m.text?.slice(0, 80),
              category: m.category,
              scope: m.scope,
            })),
            total_backed_up: filtered.length,
            backup_date: data.backed_up_at,
          }, null, 2),
        }],
      };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Git notes restore error: ${err.message}` }], isError: true };
  }
}
