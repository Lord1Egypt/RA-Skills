#!/usr/bin/env bun
// Brute-force a target species + rarity for Claude Code /buddy companion.
// Requires Bun (uses Bun.hash which matches Claude Code's internal hashing).
//
// Usage: bun reroll.mjs [--species <name>] [--rarity <level>] [--max <iterations>] [--apply]
//   --species   Target species (default: dragon)
//   --rarity    Minimum rarity: common|uncommon|rare|epic|legendary (default: legendary)
//   --max       Max iterations (default: 1000000)
//   --apply     Write the found userID to ~/.claude.json and clear companion

import { randomBytes } from 'crypto'
import { readFileSync, writeFileSync } from 'fs'
import { execFileSync } from 'child_process'
import { join } from 'path'
import { homedir } from 'os'

const MIN_VERSION = '2.1.89'
const SALT = 'friend-2026-401'

function checkCCVersion() {
  try {
    const out = execFileSync('claude', ['--version'], { encoding: 'utf8' }).trim()
    const match = out.match(/^(\d+\.\d+\.\d+)/)
    if (!match) {
      console.error(`Could not parse Claude Code version from: ${out}`)
      process.exit(1)
    }
    const ver = match[1]
    const [ma, mi, pa] = ver.split('.').map(Number)
    const [rma, rmi, rpa] = MIN_VERSION.split('.').map(Number)
    if (ma < rma || (ma === rma && mi < rmi) || (ma === rma && mi === rmi && pa < rpa)) {
      console.error(`Claude Code ${ver} detected. Buddy system requires >= ${MIN_VERSION}.`)
      console.error(`Please update: npm install -g @anthropic-ai/claude-code`)
      process.exit(1)
    }
    console.log(`Claude Code ${ver} detected (>= ${MIN_VERSION} required) ✓`)
  } catch (e) {
    if (e.code === 'ENOENT') {
      console.error(`"claude" command not found. Is Claude Code installed?`)
      process.exit(1)
    }
    throw e
  }
}

checkCCVersion()

const SPECIES = [
  'duck','goose','blob','cat','dragon','octopus','owl',
  'penguin','turtle','snail','ghost','axolotl','capybara','cactus',
  'robot','rabbit','mushroom','chonk'
]

const RARITIES = ['common','uncommon','rare','epic','legendary']
const RARITY_WEIGHTS = { common:60, uncommon:25, rare:10, epic:4, legendary:1 }
const RARITY_RANK = { common:0, uncommon:1, rare:2, epic:3, legendary:4 }

const EYES = ['·','✦','×','◉','@','°']
const HATS = ['none','crown','tophat','beanie','wizard','party','flower','bow']

function mulberry32(seed) {
  let a = seed >>> 0
  return function() {
    a |= 0; a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function hashString(s) {
  return Number(BigInt(Bun.hash(s)) & 0xffffffffn)
}

function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)] }

function rollRarity(rng) {
  let roll = rng() * 100
  for (const r of RARITIES) { roll -= RARITY_WEIGHTS[r]; if (roll < 0) return r }
  return 'common'
}

function rollCompanion(uid) {
  const rng = mulberry32(hashString(uid + SALT))
  const rarity = rollRarity(rng)
  const species = pick(rng, SPECIES)
  const eyes = pick(rng, EYES)
  const hat = pick(rng, HATS)
  const shiny = rng() < 0.01
  return { rarity, species, eyes, hat, shiny }
}

// Parse args
const args = process.argv.slice(2)
function getArg(name, def) {
  const i = args.indexOf(`--${name}`)
  return i >= 0 && i + 1 < args.length ? args[i + 1] : def
}
const hasFlag = (name) => args.includes(`--${name}`)

const targetSpecies = getArg('species', 'dragon').toLowerCase()
const targetRarity = getArg('rarity', 'legendary').toLowerCase()
const maxIter = parseInt(getArg('max', '1000000'))
const shouldApply = hasFlag('apply')

if (!SPECIES.includes(targetSpecies)) {
  console.error(`Unknown species: ${targetSpecies}\nAvailable: ${SPECIES.join(', ')}`)
  process.exit(1)
}
if (!RARITIES.includes(targetRarity)) {
  console.error(`Unknown rarity: ${targetRarity}\nAvailable: ${RARITIES.join(', ')}`)
  process.exit(1)
}

const targetRank = RARITY_RANK[targetRarity]
console.log(`Searching for ${targetRarity} ${targetSpecies} (max ${maxIter} iterations)...\n`)

let best = null

for (let i = 0; i < maxIter; i++) {
  const uid = randomBytes(32).toString('hex')
  const comp = rollCompanion(uid)

  if (comp.species === targetSpecies && RARITY_RANK[comp.rarity] >= targetRank) {
    if (!best || RARITY_RANK[comp.rarity] > RARITY_RANK[best.rarity]) {
      best = { ...comp, uid }
      const shinyTag = comp.shiny ? ' [SHINY]' : ''
      console.log(`found: ${comp.rarity} ${comp.species} (eyes:${comp.eyes} hat:${comp.hat}${shinyTag}) -> ${uid}`)
      if (comp.rarity === 'legendary') break
    }
  }
}

if (!best) {
  console.log(`\nNo ${targetRarity}+ ${targetSpecies} found in ${maxIter} iterations. Try increasing --max.`)
  process.exit(1)
}

console.log(`\nBest: ${best.rarity} ${best.species} (eyes:${best.eyes} hat:${best.hat}${best.shiny ? ' SHINY' : ''})`)
console.log(`userID: ${best.uid}`)

if (shouldApply) {
  const configPath = join(homedir(), '.claude.json')
  try {
    const config = JSON.parse(readFileSync(configPath, 'utf8'))
    const oldUid = config.userID
    config.userID = best.uid
    delete config.accountUuid
    config.companion = null
    writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n')
    console.log(`\nApplied to ${configPath}`)
    console.log(`  old userID: ${oldUid}`)
    console.log(`  new userID: ${best.uid}`)
    console.log(`  companion: cleared`)
    console.log(`\nRestart Claude Code and run /buddy to hatch your new companion!`)
  } catch (e) {
    console.error(`\nFailed to update ${configPath}: ${e.message}`)
    process.exit(1)
  }
} else {
  console.log(`\nTo apply, rerun with --apply or manually set userID in ~/.claude.json`)
}
