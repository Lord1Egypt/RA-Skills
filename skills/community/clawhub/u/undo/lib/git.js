#!/usr/bin/env node
'use strict';

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const UNDO_DATA_DIR = path.join(
  process.env.XDG_DATA_HOME || path.join(require('os').homedir(), '.local', 'share'),
  'undo-skill',
  'repos'
);

/**
 * Get the hash identifier for a project path.
 */
function getProjectHash(projectPath) {
  const absPath = path.resolve(projectPath);
  return crypto.createHash('md5').update(absPath).digest('hex').slice(0, 12);
}

/**
 * Get the bare git repo path for a project.
 */
function getBareRepoPath(projectPath) {
  const hash = getProjectHash(projectPath);
  return path.join(UNDO_DATA_DIR, hash);
}

/**
 * Check if a project is already tracked.
 */
function isTracked(projectPath) {
  const barePath = getBareRepoPath(projectPath);
  return fs.existsSync(path.join(barePath, 'HEAD'));
}

/**
 * Read the project path mapping.
 */
function getProjectMapping() {
  const mappingPath = path.join(UNDO_DATA_DIR, 'projects.json');
  if (!fs.existsSync(mappingPath)) return {};
  try {
    return JSON.parse(fs.readFileSync(mappingPath, 'utf8'));
  } catch {
    return {};
  }
}

/**
 * Save the project path mapping.
 */
function saveProjectMapping(mapping) {
  fs.mkdirSync(UNDO_DATA_DIR, { recursive: true });
  const mappingPath = path.join(UNDO_DATA_DIR, 'projects.json');
  fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));
}

/**
 * Ensure the bare repo directory exists.
 */
function ensureBareRepoDir(barePath) {
  fs.mkdirSync(barePath, { recursive: true });
  fs.mkdirSync(UNDO_DATA_DIR, { recursive: true });
}

/**
 * Run a raw git command in a specific working directory.
 */
function runGit(args, cwd, allowFail = false) {
  try {
    const result = execSync(`git ${args}`, {
      encoding: 'utf8',
      cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: { ...process.env, GIT_TERMINAL_PROMPT: '0' }
    });
    return { success: true, stdout: result.trim() };
  } catch (err) {
    if (allowFail) {
      return { success: false, stdout: '', stderr: (err.stderr || err.message || '').trim() };
    }
    throw new Error(`git ${args} failed: ${(err.stderr || err.message || '').trim()}`);
  }
}

/**
 * Copy project files to destination, excluding common ignored directories/files.
 */
function copyProjectFiles(src, dest) {
  const IGNORE_NAMES = new Set(['.git', '.undo-git', '.DS_Store']);
  const IGNORE_DIR_NAMES = new Set(['node_modules', '.git', '.undo-git', 'dist', 'build', '.next', 'coverage', '.venv', 'venv']);

  function copyRecursive(srcDir, destDir) {
    let entries;
    try {
      entries = fs.readdirSync(srcDir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (IGNORE_NAMES.has(entry.name) || IGNORE_DIR_NAMES.has(entry.name)) continue;
      const srcPath = path.join(srcDir, entry.name);
      const destPath = path.join(destDir, entry.name);
      if (entry.isDirectory()) {
        if (IGNORE_DIR_NAMES.has(entry.name)) continue;
        fs.mkdirSync(destPath, { recursive: true });
        copyRecursive(srcPath, destPath);
      } else if (entry.isFile() || entry.isSymbolicLink()) {
        try {
          fs.copyFileSync(srcPath, destPath);
        } catch {
          // Skip files that can't be read
        }
      }
    }
  }

  fs.mkdirSync(dest, { recursive: true });
  copyRecursive(src, dest);
}

/**
 * Copy files from work tree back to project directory.
 * Handles: new files, modified files, deleted files.
 */
function copyBackToProject(workTree, projectPath) {
  const IGNORE_NAMES = new Set(['.git', '.undo-git', '.DS_Store', '_worktree']);
  const IGNORE_DIR_NAMES = new Set(['node_modules', '.git', '.undo-git', 'dist', 'build', '.next', 'coverage', '.venv', 'venv']);

  function getAllFiles(dir, base = '') {
    const files = new Map();
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return files;
    }
    for (const entry of entries) {
      if (IGNORE_NAMES.has(entry.name) || IGNORE_DIR_NAMES.has(entry.name)) continue;
      const relPath = path.join(base, entry.name);
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (IGNORE_DIR_NAMES.has(entry.name)) continue;
        for (const [k, v] of getAllFiles(fullPath, relPath)) {
          files.set(k, v);
        }
      } else if (entry.isFile()) {
        try {
          const stat = fs.statSync(fullPath);
          files.set(relPath, { size: stat.size, mtime: stat.mtimeMs });
        } catch {}
      }
    }
    return files;
  }

  const workFiles = getAllFiles(workTree);
  const projectFiles = getAllFiles(projectPath);

  // Delete files in project that no longer exist in work tree
  for (const [relPath] of projectFiles) {
    if (!workFiles.has(relPath)) {
      const fullPath = path.join(projectPath, relPath);
      try {
        if (fs.existsSync(fullPath)) fs.unlinkSync(fullPath);
      } catch {}
    }
  }

  // Copy/overwrite files from work tree to project
  for (const [relPath] of workFiles) {
    const srcPath = path.join(workTree, relPath);
    const destPath = path.join(projectPath, relPath);
    try {
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.copyFileSync(srcPath, destPath);
    } catch {}
  }

  // Clean up empty directories in project
  function removeEmptyDirs(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (IGNORE_NAMES.has(entry.name) || IGNORE_DIR_NAMES.has(entry.name)) continue;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        removeEmptyDirs(fullPath);
        try {
          if (fs.readdirSync(fullPath).length === 0) {
            fs.rmdirSync(fullPath);
          }
        } catch {}
      }
    }
  }
  removeEmptyDirs(projectPath);
}

/**
 * Get or create the work tree for a project.
 * Returns the work tree path and whether it was freshly created.
 */
function getOrCreateWorkTree(projectPath) {
  const barePath = getBareRepoPath(projectPath);
  const workTree = path.join(barePath, '_worktree');

  if (fs.existsSync(workTree)) {
    return { workTree, fresh: false };
  }

  // Clone bare repo to work tree
  runGit(`clone "${barePath}" "${workTree}"`, process.cwd());
  return { workTree, fresh: true };
}

/**
 * Sync work tree with current project state.
 * Resets work tree to bare repo HEAD, then copies current project files in.
 */
function syncWorkTree(workTree, projectPath) {
  // Reset to match bare repo
  runGit(`reset --hard HEAD`, workTree, true);
  runGit(`clean -fdx`, workTree, true);

  // Copy current project files into work tree
  copyProjectFiles(projectPath, workTree);
}

// ─────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────

/**
 * Initialize tracking for a project.
 * Returns: { success, initialized, barePath, message, data?: object }
 */
function initProject(projectPath) {
  const absPath = path.resolve(projectPath);
  const barePath = getBareRepoPath(absPath);

  if (isTracked(absPath)) {
    return {
      success: true,
      initialized: false,
      barePath,
      message: 'already_tracked',
      data: { project: absPath }
    };
  }

  try {
    ensureBareRepoDir(barePath);

    // Initialize bare repo
    runGit(`init --bare`, barePath);
    runGit(`config receive.denyCurrentBranch ignore`, barePath);
    runGit(`config http.postBuffer 524288000`, barePath);

    // Create initial commit via temp work tree
    const { workTree } = getOrCreateWorkTree(absPath);

    // Set up bare repo to accept pushes to main
    runGit(`symbolic-ref HEAD refs/heads/main`, barePath);

    copyProjectFiles(absPath, workTree);
    runGit(`add -A`, workTree);

    const statusResult = runGit(`status --porcelain`, workTree, true);
    if (!statusResult.stdout.trim()) {
      return {
        success: true,
        initialized: false,
        barePath,
        message: 'no_files_to_track',
        data: { project: absPath }
      };
    }

    runGit(`commit -m "initial commit"`, workTree);
    runGit(`push --set-upstream origin main`, workTree);

    // Record mapping
    const mapping = getProjectMapping();
    mapping[getProjectHash(absPath)] = absPath;
    saveProjectMapping(mapping);

    // Cleanup work tree (it'll be recreated as needed)
    if (fs.existsSync(workTree)) {
      fs.rmSync(workTree, { recursive: true, force: true });
    }

    return {
      success: true,
      initialized: true,
      barePath,
      message: 'initialized',
      data: { project: absPath }
    };
  } catch (err) {
    // Cleanup on failure
    if (fs.existsSync(barePath)) {
      fs.rmSync(barePath, { recursive: true, force: true });
    }
    return {
      success: false,
      initialized: false,
      barePath,
      message: `init_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

/**
 * Create a snapshot commit.
 * Returns: { success, committed, hash, message, data?: object }
 */
function createSnapshot(projectPath, description) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return {
      success: false,
      committed: false,
      hash: '',
      message: 'not_tracked',
      data: { project: absPath }
    };
  }

  const barePath = getBareRepoPath(absPath);
  const { workTree } = getOrCreateWorkTree(absPath);

  try {
    syncWorkTree(workTree, absPath);

    // Stage all changes
    runGit(`add -A`, workTree);

    // Check if there are actual changes
    const statusResult = runGit(`status --porcelain`, workTree, true);
    if (!statusResult.stdout.trim()) {
      return {
        success: true,
        committed: false,
        hash: '',
        message: 'no_changes',
        data: { project: absPath }
      };
    }

    // Parse changed files for the commit message body
    const changedFiles = statusResult.stdout.trim().split('\n').filter(Boolean).map(line => {
      const parts = line.trim().split(/\s+/);
      return { status: parts[0], path: parts.slice(1).join(' ') };
    });

    // Build structured commit message
    const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
    const commitSubject = `[auto] ${timestamp} | ${description}`;
    const commitBody = changedFiles.map(f => `  ${f.status} ${f.path}`).join('\n');
    const commitMessage = `${commitSubject}\n\n${commitBody}`;

    // Write commit message to file to avoid shell escaping issues
    const msgFile = path.join(barePath, '_msg');
    fs.writeFileSync(msgFile, commitMessage);

    runGit(`commit -F "${msgFile}"`, workTree);
    fs.unlinkSync(msgFile);

    // Get commit hash
    const hashResult = runGit(`rev-parse HEAD`, workTree);
    const hash = hashResult.stdout.slice(0, 7);

    // Push to bare repo
    runGit(`push origin main`, workTree);

    return {
      success: true,
      committed: true,
      hash,
      message: 'committed',
      data: {
        project: absPath,
        hash,
        description,
        timestamp,
        changedFiles: changedFiles.map(f => f.path),
        fileCount: changedFiles.length
      }
    };
  } catch (err) {
    return {
      success: false,
      committed: false,
      hash: '',
      message: `snapshot_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

/**
 * Get the commit history for a project.
 * Returns: { success, commits: Array<{hash, date, timestamp, description, files: Array<{status, path}>}, isCheckpoint: boolean}>, message }
 */
function getHistory(projectPath, limit = 20) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, commits: [], message: 'not_tracked', data: { project: absPath } };
  }

  const barePath = getBareRepoPath(absPath);

  try {
    // Get log with full details
    const logResult = runGit(
      `--git-dir="${barePath}" log -n ${limit} --format="COMMIT_START%n%H%n%ai%n%s%nCOMMIT_BODY_START" --name-status`,
      process.cwd(),
      true
    );

    if (!logResult.success) {
      return { success: false, commits: [], message: 'log_failed', data: { project: absPath } };
    }

    const commits = [];
    const blocks = logResult.stdout.split('COMMIT_START\n').filter(Boolean);

    for (const block of blocks) {
      const lines = block.trim().split('\n');
      const hash = lines[0] || '';
      const date = lines[1] || '';
      const subject = lines[2] || '';
      const bodyStartIdx = lines.findIndex(l => l === 'COMMIT_BODY_START');

      const files = [];
      if (bodyStartIdx !== -1) {
        for (let i = bodyStartIdx + 1; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line) continue;
          const m = line.match(/^([AMDRC])\t(.+)$/);
          if (m) {
            files.push({ status: m[1], path: m[2] });
          }
        }
      }

      // Extract timestamp for time-based undo
      let timestamp = null;
      const tsMatch = subject.match(/^\[auto\]\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})/);
      if (tsMatch) {
        const ts = new Date(tsMatch[1]);
        if (!isNaN(ts.getTime())) timestamp = ts.toISOString();
      }

      const isCheckpoint = subject.includes('checkpoint:') || subject.includes('🏁');
      const isInitial = subject.includes('initial commit');

      // Extract clean description
      const descMatch = subject.match(/\|\s+(.+)$/);
      const description = descMatch ? descMatch[1].trim() : subject;

      commits.push({
        hash: hash.slice(0, 7),
        fullHash: hash,
        date,
        timestamp,
        description,
        subject,
        files,
        isCheckpoint,
        isInitial
      });
    }

    return {
      success: true,
      commits: commits.reverse(), // oldest first for display
      message: 'ok',
      data: { project: absPath, count: commits.length }
    };
  } catch (err) {
    return { success: false, commits: [], message: `history_failed: ${err.message}`, data: { project: absPath } };
  }
}

/**
 * Get all checkpoint branches for a project.
 * Returns: { success, checkpoints: Array<{name, hash}>, message }
 */
function getCheckpoints(projectPath) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, checkpoints: [], message: 'not_tracked' };
  }

  const barePath = getBareRepoPath(absPath);

  try {
    const result = runGit(
      `--git-dir="${barePath}" branch --list "checkpoint/*" --format="%(objectname:short)|%(refname:short)"`,
      process.cwd()
    );

    const checkpoints = result.stdout.trim().split('\n').filter(Boolean).map(line => {
      const [hash, name] = line.split('|');
      return { name, hash };
    });

    return { success: true, checkpoints, message: 'ok' };
  } catch {
    return { success: false, checkpoints: [], message: 'list_failed' };
  }
}

/**
 * Undo N steps from HEAD.
 * Returns: { success, undone: boolean, targetHash, checkpointBranch, message, data?: object }
 */
function undoSteps(projectPath, steps = 1) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, undone: false, message: 'not_tracked', data: { project: absPath } };
  }

  const barePath = getBareRepoPath(absPath);
  const { workTree } = getOrCreateWorkTree(absPath);

  try {
    // Get target commit
    const targetResult = runGit(`--git-dir="${barePath}" rev-parse HEAD~${steps}`, process.cwd(), true);
    if (!targetResult.success) {
      return {
        success: false,
        undone: false,
        message: 'not_enough_history',
        data: { project: absPath, requested: steps }
      };
    }
    const targetHash = targetResult.stdout.trim();

    // Save current state to checkpoint branch
    const checkpointBranch = `checkpoint/undo-${Date.now()}`;
    runGit(`--git-dir="${barePath}" branch "${checkpointBranch}" HEAD`, process.cwd());

    // Reset work tree to target
    runGit(`reset --hard "${targetHash}"`, workTree);

    // Copy files back to project
    copyBackToProject(workTree, absPath);

    // Update bare repo main branch
    runGit(`push --force origin main`, workTree);

    return {
      success: true,
      undone: true,
      targetHash: targetHash.slice(0, 7),
      checkpointBranch: checkpointBranch,
      message: 'undone',
      data: {
        project: absPath,
        steps: steps,
        targetHash: targetHash.slice(0, 7),
        checkpointBranch
      }
    };
  } catch (err) {
    return {
      success: false,
      undone: false,
      message: `undo_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

/**
 * Undo to a specific checkpoint (branch).
 */
function undoToCheckpoint(projectPath, checkpointName) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, undone: false, message: 'not_tracked', data: { project: absPath } };
  }

  const barePath = getBareRepoPath(absPath);
  const { workTree } = getOrCreateWorkTree(absPath);

  try {
    const branchName = checkpointName.startsWith('checkpoint/') ? checkpointName : `checkpoint/${checkpointName}`;

    // Verify branch exists
    const refResult = runGit(`--git-dir="${barePath}" rev-parse "${branchName}"`, process.cwd(), true);
    if (!refResult.success) {
      return {
        success: false,
        undone: false,
        message: 'checkpoint_not_found',
        data: { project: absPath, checkpoint: checkpointName }
      };
    }
    const targetHash = refResult.stdout.trim();

    // Save current state
    const saveBranch = `checkpoint/undo-before-${Date.now()}`;
    runGit(`--git-dir="${barePath}" branch "${saveBranch}" HEAD`, process.cwd());

    // Reset to checkpoint
    runGit(`reset --hard "${targetHash}"`, workTree);
    copyBackToProject(workTree, absPath);
    runGit(`push --force origin main`, workTree);

    return {
      success: true,
      undone: true,
      targetHash: targetHash.slice(0, 7),
      checkpointBranch: saveBranch,
      message: 'undone_to_checkpoint',
      data: {
        project: absPath,
        checkpoint: checkpointName,
        targetHash: targetHash.slice(0, 7),
        saveBranch
      }
    };
  } catch (err) {
    return {
      success: false,
      undone: false,
      message: `undo_checkpoint_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

/**
 * Create a named checkpoint (branch at current HEAD).
 */
function createCheckpoint(projectPath, name) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, message: 'not_tracked', data: { project: absPath } };
  }

  const barePath = getBareRepoPath(absPath);
  const branchName = name.startsWith('checkpoint/') ? name : `checkpoint/${name}`;

  try {
    // Check if already exists
    const existing = runGit(`--git-dir="${barePath}" rev-parse "${branchName}"`, process.cwd(), true);
    if (existing.success) {
      return {
        success: false,
        message: 'checkpoint_exists',
        data: { project: absPath, checkpoint: name }
      };
    }

    runGit(`--git-dir="${barePath}" branch "${branchName}" HEAD`, process.cwd());

    return {
      success: true,
      message: 'checkpoint_created',
      data: { project: absPath, checkpoint: name, branch: branchName }
    };
  } catch (err) {
    return {
      success: false,
      message: `checkpoint_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

/**
 * Undo to a specific timestamp.
 */
function undoToTimestamp(projectPath, timestamp) {
  const absPath = path.resolve(projectPath);

  if (!isTracked(absPath)) {
    return { success: false, undone: false, message: 'not_tracked', data: { project: absPath } };
  }

  const barePath = getBareRepoPath(absPath);
  const { workTree } = getOrCreateWorkTree(absPath);

  try {
    const targetDate = new Date(timestamp);
    if (isNaN(targetDate.getTime())) {
      return {
        success: false,
        undone: false,
        message: 'invalid_timestamp',
        data: { project: absPath, timestamp }
      };
    }

    // Get commits in date order
    const logResult = runGit(
      `--git-dir="${barePath}" log --format="%H|%ai" --date-order`,
      process.cwd(),
      true
    );
    if (!logResult.success) {
      return { success: false, undone: false, message: 'log_failed', data: { project: absPath } };
    }

    const lines = logResult.stdout.trim().split('\n').filter(Boolean);
    let targetHash = null;

    for (const line of lines) {
      const [hash, dateStr] = line.split('|');
      const commitDate = new Date(dateStr);
      if (commitDate <= targetDate) {
        targetHash = hash;
        break;
      }
    }

    if (!targetHash) {
      return {
        success: false,
        undone: false,
        message: 'no_commits_before_timestamp',
        data: { project: absPath, timestamp }
      };
    }

    // Save current state
    const saveBranch = `checkpoint/undo-before-${Date.now()}`;
    runGit(`--git-dir="${barePath}" branch "${saveBranch}" HEAD`, process.cwd());

    // Reset to target
    runGit(`reset --hard "${targetHash}"`, workTree);
    copyBackToProject(workTree, absPath);
    runGit(`push --force origin main`, workTree);

    return {
      success: true,
      undone: true,
      targetHash: targetHash.slice(0, 7),
      checkpointBranch: saveBranch,
      message: 'undone_to_timestamp',
      data: {
        project: absPath,
        timestamp,
        targetHash: targetHash.slice(0, 7),
        saveBranch
      }
    };
  } catch (err) {
    return {
      success: false,
      undone: false,
      message: `undo_timestamp_failed: ${err.message}`,
      data: { project: absPath, error: err.message }
    };
  }
}

module.exports = {
  getProjectHash,
  getBareRepoPath,
  isTracked,
  getProjectMapping,
  initProject,
  createSnapshot,
  getHistory,
  getCheckpoints,
  undoSteps,
  undoToCheckpoint,
  undoToTimestamp,
  createCheckpoint,
  runGit,
  copyProjectFiles,
  copyBackToProject,
};
