#!/usr/bin/env node
/**
 * Detect frontend project framework, language, package manager, and other details.
 * Outputs JSON: { framework, typescript, packageManager, hasVitest, hasMSW, hasTestingLibrary }
 */

import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

function detectFramework(projectDir) {
  const result = {
    os: process.platform,
    framework: 'unknown',
    isNext: false,
    typescript: false,
    hasTsConfig: false,
    packageManager: 'npm',
    hasGit: false,
    hasVitest: false,
    hasVitestUI: false,
    hasMSW: false,
    hasTestingLibrary: false,
  }

  // Check if Git is available
  try {
    execSync('git --version', { stdio: 'ignore' })
    result.hasGit = true
  } catch (e) {
    result.hasGit = false
  }

  const pkgPath = path.join(projectDir, 'package.json')
  if (!fs.existsSync(pkgPath)) {
    return result
  }

  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'))
  const allDeps = {
    ...pkg.dependencies,
    ...pkg.devDependencies,
  }

  // Detect framework
  if (allDeps['next']) {
    result.framework = 'react'
    result.isNext = true
  } else if (allDeps['react'] || allDeps['react-dom']) {
    result.framework = 'react'
  } else if (allDeps['vue'] || allDeps['nuxt']) {
    result.framework = 'vue'
  }

  // Detect TypeScript and tsconfig
  result.hasTsConfig = fs.existsSync(path.join(projectDir, 'tsconfig.json'))
  if (allDeps['typescript'] || result.hasTsConfig) {
    result.typescript = true
  }

  // Detect package manager
  if (fs.existsSync(path.join(projectDir, 'pnpm-lock.yaml'))) {
    result.packageManager = 'pnpm'
  } else if (fs.existsSync(path.join(projectDir, 'yarn.lock'))) {
    result.packageManager = 'yarn'
  } else {
    result.packageManager = 'npm'
  }

  // Detect existing test tools
  result.hasVitest = 'vitest' in allDeps
  result.hasMSW = 'msw' in allDeps
  result.hasTestingLibrary = Object.keys(allDeps).some(k => k.startsWith('@testing-library/'))

  return result
}

const projectDir = path.resolve(process.argv[2] || process.cwd())

// Safety check: validate project directory
if (!fs.existsSync(projectDir) || !fs.statSync(projectDir).isDirectory()) {
  console.error('Error: Invalid project directory.')
  process.exit(1)
}

const result = detectFramework(projectDir)
console.log(JSON.stringify(result, null, 2))
