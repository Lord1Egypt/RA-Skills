#!/usr/bin/env node
// The driver: fixture -> tape -> vhs -> output -> optimize -> cleanup.
// See ../../references/recipe-catalog-pattern.md § "The driver".
//
// Usage:
//   tsx screenshot.ts --list             list every recipe
//   tsx screenshot.ts --recipe ui-home   regenerate one recipe
//   tsx screenshot.ts                    regenerate everything

import { execSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { RECIPES, type Recipe } from './recipes'
import { buildTape } from './tape'

const OUTPUT_DIR = join(process.cwd(), 'captures')
const PINNED_NOW = '2024-01-15T12:00:00Z' // fixed "now" so relative dates never drift between runs

function materializeFixture(scenario: string | null): string | undefined {
  if (!scenario) return undefined
  // TODO: build the named fixture here. If this app operates on a git repo,
  // use https://github.com/gfargo/git-scenarios instead of hand-rolled
  // `git init`/`git commit` calls — that's exactly the problem it solves.
  return mkdtempSync(join(tmpdir(), `${scenario}-`))
}

function run(recipe: Recipe): void {
  const fixture = materializeFixture(recipe.scenario)
  try {
    const tape = buildTape(recipe, { fixturePath: fixture, pinnedNow: PINNED_NOW })
    const tapePath = join(OUTPUT_DIR, `${recipe.name}.tape`)
    writeFileSync(tapePath, tape)

    execSync(`vhs "${tapePath}"`, { cwd: OUTPUT_DIR, stdio: 'inherit' })

    // GIF optimization lives HERE, in the driver — not as a manual afterthought
    // — so "regenerate everything" can never silently re-bloat every GIF.
    if (recipe.emitGif) {
      const gifPath = join(OUTPUT_DIR, `${recipe.name}.gif`)
      try {
        execSync(`gifsicle -O3 --batch "${gifPath}"`, { stdio: 'inherit' })
      } catch {
        console.warn(`· gifsicle not found — ${recipe.name}.gif left unoptimized (brew install gifsicle)`)
      }
    }

    console.log(`· ${recipe.name} -> captures/${recipe.name}.${recipe.emitGif ? 'gif' : 'png'}`)
  } finally {
    if (fixture) rmSync(fixture, { recursive: true, force: true })
  }
}

function main(): void {
  const args = process.argv.slice(2)
  mkdirSync(OUTPUT_DIR, { recursive: true })

  if (args.includes('--list')) {
    for (const r of RECIPES) console.log(`${r.name}\t${r.description}`)
    return
  }

  const recipeFlagIndex = args.indexOf('--recipe')
  if (recipeFlagIndex !== -1) {
    const name = args[recipeFlagIndex + 1]
    const recipe = RECIPES.find((r) => r.name === name)
    if (!recipe) {
      console.error(`no recipe named "${name}" — try --list`)
      process.exitCode = 1
      return
    }
    run(recipe)
    return
  }

  for (const recipe of RECIPES) run(recipe)
}

main()
