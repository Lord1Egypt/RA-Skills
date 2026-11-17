#!/usr/bin/env node

import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { launchStealthBrowser } from './stealth.js'

function parseArgs(argv) {
  const args = {}

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i]
    if (!token.startsWith('--')) continue

    const key = token.slice(2)
    const next = argv[i + 1]
    if (next && !next.startsWith('--')) {
      args[key] = next
      i += 1
    } else {
      args[key] = true
    }
  }

  return args
}

function usage() {
  return `Usage: node scripts/cli.js --url <https://...> [options]

Options:
  --url <url>              required URL
  --screenshot <path>      save a PNG of the page
  --html <path>            save page HTML
  --wait-selector <css>    wait for selector before capture
  --timeout <ms>           navigation timeout (default: 30000)
  --headed                 visible browser
  --proxy <server>         proxy, e.g. http://127.0.0.1:8080
  --json                   print JSON result to stdout
`
}

async function ensureParentDir(filePath) {
  await mkdir(dirname(filePath), { recursive: true })
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const url = args.url

  if (!url || args.help) {
    process.stderr.write(usage())
    process.exitCode = url ? 0 : 1
    return
  }

  const timeout = args.timeout ? Number(args.timeout) : 30_000
  const screenshotPath = args.screenshot ? resolve(String(args.screenshot)) : null
  const htmlPath = args.html ? resolve(String(args.html)) : null
  const jsonMode = Boolean(args.json)

  const { browser, page } = await launchStealthBrowser({
    headless: args.headed ? false : undefined,
    proxy: args.proxy ? String(args.proxy) : undefined,
  })

  try {
    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout,
    })

    if (args['wait-selector']) {
      await page.waitForSelector(String(args['wait-selector']), { timeout })
    }

    if (screenshotPath) {
      await ensureParentDir(screenshotPath)
      await page.screenshot({ path: screenshotPath, fullPage: true })
    }

    if (htmlPath) {
      await ensureParentDir(htmlPath)
      await writeFile(htmlPath, await page.content(), 'utf8')
    }

    const result = {
      url: page.url(),
      title: await page.title(),
      screenshot: screenshotPath,
      html: htmlPath,
    }

    if (jsonMode) {
      process.stdout.write(`${JSON.stringify(result)}\n`)
    } else {
      process.stdout.write(`${result.title} — ${result.url}\n`)
      if (screenshotPath) process.stdout.write(`screenshot: ${screenshotPath}\n`)
      if (htmlPath) process.stdout.write(`html: ${htmlPath}\n`)
    }
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error.message}\n`)
  process.exitCode = 1
})
