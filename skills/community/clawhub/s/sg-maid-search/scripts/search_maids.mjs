#!/usr/bin/env node

// Search the Sunrise Link domestic maid database.
// Usage: echo '{"nationality":"Philippines","minSalary":600}' | node search_maids.mjs
// Reads JSON filters from stdin (or argv[2] when run interactively in a TTY).
// Requires Node.js 18+ (uses built-in fetch). Zero third-party dependencies.

const API_BASE_URL = 'https://www.sunriselink.sg'
const API_PATH = '/api/public/v1/helpers'

const VALID_PARAMS = new Set([
  'nationality', 'religion', 'languages',
  'minAge', 'maxAge', 'minSalary', 'maxSalary',
  'hasSgExperience',
  'needsInfantCare', 'needsExperiencedInfantCare',
  'needsElderlyCare', 'needsExperiencedElderlyCare',
  'needsDisabledCare',
  'needsCooking', 'needsExperiencedCooking',
  'needsHousework',
])

function buildUrl(filters) {
  const url = new URL(API_PATH, API_BASE_URL)

  for (const [key, value] of Object.entries(filters)) {
    if (!VALID_PARAMS.has(key)) continue
    if (value === undefined || value === null) continue

    if (key === 'languages' && Array.isArray(value)) {
      for (const lang of value) {
        url.searchParams.append('languages', lang)
      }
    } else if (typeof value === 'boolean') {
      url.searchParams.set(key, String(value))
    } else {
      url.searchParams.set(key, String(value))
    }
  }

  return url.toString()
}

async function readStdin() {
  return new Promise((resolve) => {
    let data = ''
    process.stdin.setEncoding('utf8')
    process.stdin.on('data', chunk => { data += chunk })
    process.stdin.on('end', () => resolve(data.trim()))
    // Fall back to argv if stdin is a TTY (direct CLI usage)
    if (process.stdin.isTTY) resolve(process.argv[2] ?? '')
  })
}

async function main() {
  const input = await readStdin()

  if (!input) {
    console.error('Usage: node search_maids.mjs \'{"nationality":"Philippines"}\'')
    process.exit(1)
  }

  let filters
  try {
    filters = JSON.parse(input)
  } catch {
    console.error('Error: Invalid JSON input')
    process.exit(1)
  }

  const url = buildUrl(filters)

  let response
  try {
    response = await fetch(url)
  } catch (err) {
    console.error(`Error: Failed to connect to API — ${err.message}`)
    process.exit(1)
  }

  if (!response.ok) {
    const body = await response.text().catch(() => '')
    console.error(`Error: API returned ${response.status} — ${body}`)
    process.exit(1)
  }

  const data = await response.json()
  console.log(JSON.stringify(data, null, 2))
}

main()
