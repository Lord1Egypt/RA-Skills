#!/usr/bin/env node
// Copies only the web-ready, "published" captures into a docs/site asset
// folder. Keep an explicit allow-list + filename map so the catalog can hold
// internal/debug captures that never ship. Run on release or when visuals
// change — not on every capture regeneration.
// See ../../references/recipe-catalog-pattern.md § "The sync step".

import { copyFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'

// recipe name -> published filename on the docs site. Empty by default —
// fill in once you have real recipes and a real site to publish into.
const PUBLISHED: Record<string, string> = {
  // 'demo-workflow': 'hero.gif',
  // 'ui-home': 'home.png',
}

const CAPTURES_DIR = join(process.cwd(), 'captures')
const SITE_ASSET_DIR = process.env.SITE_ASSET_DIR ?? join(process.cwd(), '../docs-site/public/demos')

function main(): void {
  const entries = Object.entries(PUBLISHED)
  if (entries.length === 0) {
    console.log('· PUBLISHED is empty — nothing to sync (edit syncScreenshots.ts)')
    return
  }

  mkdirSync(SITE_ASSET_DIR, { recursive: true })

  for (const [recipeName, siteFilename] of entries) {
    const ext = siteFilename.split('.').pop()
    const src = join(CAPTURES_DIR, `${recipeName}.${ext}`)
    const dest = join(SITE_ASSET_DIR, siteFilename)
    copyFileSync(src, dest)
    console.log(`· synced ${recipeName} -> ${dest}`)
  }
}

main()
