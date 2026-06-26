#!/usr/bin/env node
/**
 * Check whether Git staged source files have corresponding unit test files.
 * Outputs the paths of source files missing tests (one per line) for use by pre-commit hooks.
 *
 * Usage: node check-missing-tests.js [project-dir]
 *
 * Logic:
 *   1. Get staged .ts/.tsx/.vue source files via git diff --cached
 *   2. Exclude non-business files (test files, configs, stories, etc.)
 *   3. Check whether a corresponding .test.ts/.test.tsx exists under tests/unit/
 *   4. Output file paths that are missing tests
 *
 * Exit codes:
 *   0 — All files have tests (or no files need checking)
 *   1 — Some files are missing tests (paths printed to stdout)
 */

import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'

const projectDir = path.resolve(process.argv[2] || process.cwd())

// Safety check: validate directory
if (!fs.existsSync(projectDir) || !fs.statSync(projectDir).isDirectory()) {
  console.error('Error: Invalid project directory.')
  process.exit(1)
}

// Safety check: verify we are inside a Git repository
try {
  execSync('git rev-parse --is-inside-work-tree', { cwd: projectDir, stdio: 'ignore' })
} catch (e) {
  console.error('Error: Not a Git repository.')
  process.exit(1)
}

// Get the list of staged files (added and modified only)
function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only --diff-filter=ACM', {
      cwd: projectDir,
      encoding: 'utf-8',
    })
    // Git path output always uses forward slashes (/). Ensure consistency on Windows.
    return output.trim().split('\n').filter(Boolean).map(f => f.replace(/\\/g, '/'))
  } catch {
    return []
  }
}

// Determine whether a file is business source code that needs tests
function isBusinessSource(filePath) {
  // Normalize paths to forward slashes for consistent pattern matching
  const normalizedPath = filePath.replace(/\\/g, '/')

  // Only consider files under the src/ directory
  if (!normalizedPath.startsWith('src/')) return false

  // Only consider .ts / .tsx / .vue files
  if (!/\.(ts|tsx|vue)$/.test(normalizedPath)) return false

  // Exclude test files, stories, type declarations, pure re-export index files
  const excludePatterns = [
    /\.test\./,
    /\.spec\./,
    /\.stories\./,
    /\.d\.ts$/,
    /\/index\.(ts|tsx)$/,  // Pure re-export index files
    /\/types\//,           // Type definition directories
    /\/constants\//,       // Constants directories
  ]

  return !excludePatterns.some(p => p.test(normalizedPath))
}

// Derive the test file path from the source file path
// src/utils/format.ts → tests/unit/utils/format.test.ts
// src/components/Button.tsx → tests/unit/components/Button.test.tsx
function getTestFilePath(srcPath) {
  const relativePath = srcPath.replace(/^src\//, '')
  const ext = path.extname(relativePath)
  const withoutExt = relativePath.slice(0, -ext.length)

  // .vue files use .test.ts for their tests
  const testExt = ext === '.vue' ? '.test.ts' : `.test${ext}`
  return path.join('tests', 'unit', withoutExt + testExt)
}

// Main logic
const stagedFiles = getStagedFiles()
const businessFiles = stagedFiles.filter(isBusinessSource)

const missingTests = businessFiles.filter(srcFile => {
  const testFile = getTestFilePath(srcFile)
  const fullPath = path.join(projectDir, testFile)
  return !fs.existsSync(fullPath)
})

if (missingTests.length > 0) {
  missingTests.forEach(f => console.log(f))
  process.exit(1)
} else {
  process.exit(0)
}
