#!/usr/bin/env bun
// Change companion name and/or personality in ~/.claude.json
//
// Usage: bun rename.mjs [--name <name>] [--desc <personality>]

import { readFileSync, writeFileSync } from 'fs'
import { join } from 'path'
import { homedir } from 'os'

const args = process.argv.slice(2)
function getArg(name) {
  const i = args.indexOf(`--${name}`)
  return i >= 0 && i + 1 < args.length ? args[i + 1] : null
}

const name = getArg('name')
const desc = getArg('desc')

if (!name && !desc) {
  console.error('Usage: bun rename.mjs [--name <name>] [--desc <personality>]')
  console.error('At least one of --name or --desc is required.')
  process.exit(1)
}

const configPath = join(homedir(), '.claude.json')
try {
  const config = JSON.parse(readFileSync(configPath, 'utf8'))
  if (!config.companion) {
    console.error('No companion found in config. Run /buddy first to hatch one.')
    process.exit(1)
  }
  if (name) {
    const old = config.companion.name
    config.companion.name = name
    console.log(`name: "${old}" -> "${name}"`)
  }
  if (desc) {
    const old = config.companion.personality
    config.companion.personality = desc
    console.log(`personality: "${old}" -> "${desc}"`)
  }
  writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n')
  console.log(`\nUpdated ${configPath}`)
  console.log('Restart Claude Code for changes to take effect.')
} catch (e) {
  console.error(`Failed to update ${configPath}: ${e.message}`)
  process.exit(1)
}
