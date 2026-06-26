#!/usr/bin/env bun
// OAuth setup helper for Pro/Max subscribers to enable buddy reroll.
// By logging in via CLAUDE_CODE_OAUTH_TOKEN, accountUuid is NOT written
// to ~/.claude.json, so /buddy falls back to userID (which can be replaced).
//
// Usage:
//   bun oauth-setup.mjs --check     Check if accountUuid exists (exit 1 = needs setup)
//   bun oauth-setup.mjs --prepare   Backup config and reset to minimal state
//   bun oauth-setup.mjs --verify    Verify config has no accountUuid after OAuth login
//   bun oauth-setup.mjs --restore   Restore backup if something goes wrong

import { readFileSync, writeFileSync, copyFileSync, existsSync } from 'fs'
import { join } from 'path'
import { homedir } from 'os'

const configPath = join(homedir(), '.claude.json')
const backupPath = join(homedir(), '.claude.json.oauth-backup')

const args = process.argv.slice(2)
const hasFlag = (name) => args.includes(`--${name}`)

if (hasFlag('check')) {
  try {
    if (!existsSync(configPath)) {
      console.log('No config file found. Standard reroll will work.')
      process.exit(0)
    }
    const config = JSON.parse(readFileSync(configPath, 'utf8'))
    if (config.accountUuid) {
      console.log(`accountUuid found: ${config.accountUuid}`)
      console.log('This is a Pro/Max account. OAuth setup required for buddy reroll.')
      process.exit(1)
    }
    console.log('No accountUuid found. Standard reroll will work.')
    process.exit(0)
  } catch (e) {
    // Malformed JSON or read error — no accountUuid to worry about
    console.log(`Warning: could not parse ${configPath}: ${e.message}`)
    console.log('Proceeding with standard reroll.')
    process.exit(0)
  }
}

if (hasFlag('prepare')) {
  if (existsSync(configPath)) {
    copyFileSync(configPath, backupPath)
    console.log(`Backed up: ${configPath} -> ${backupPath}`)
  }

  const minimalConfig = { hasCompletedOnboarding: true, theme: "dark" }
  writeFileSync(configPath, JSON.stringify(minimalConfig, null, 2) + '\n')
  console.log(`Reset ${configPath} to minimal config`)
  console.log('accountUuid removed. Ready for OAuth login.')
}

if (hasFlag('verify')) {
  try {
    const config = JSON.parse(readFileSync(configPath, 'utf8'))
    if (config.accountUuid) {
      console.error('FAIL: accountUuid still present. OAuth setup did not work.')
      console.error('Make sure you used CLAUDE_CODE_OAUTH_TOKEN env var when starting claude.')
      process.exit(1)
    }
    if (!config.userID) {
      console.error('FAIL: userID not found. Did you start claude with CLAUDE_CODE_OAUTH_TOKEN?')
      process.exit(1)
    }
    console.log(`OK: no accountUuid, userID=${config.userID}`)
    console.log('Ready for reroll!')
  } catch (e) {
    console.error(`Failed to read ${configPath}: ${e.message}`)
    process.exit(1)
  }
}

if (hasFlag('restore')) {
  if (!existsSync(backupPath)) {
    console.error(`No backup found at ${backupPath}`)
    process.exit(1)
  }
  copyFileSync(backupPath, configPath)
  console.log(`Restored ${configPath} from ${backupPath}`)
}
