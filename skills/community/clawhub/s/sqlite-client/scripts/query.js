#!/usr/bin/env node
/**
 * SQLite Database Query Helper Script
 * 
 * Usage:
 *   node query.js <db-path> <sql> [--json] [--limit N]
 * 
 * Examples:
 *   node query.js ./data.db "SELECT * FROM users"
 *   node query.js ./data.db "SELECT * FROM users" --json
 *   node query.js ./data.db "SELECT * FROM users" --limit 10
 */

const path = require('path')

async function main() {
  const args = process.argv.slice(2)
  if (args.length < 2) {
    console.error('Usage: node query.js <db-path> <sql> [--json] [--limit N]')
    process.exit(1)
  }

  const dbPath = path.resolve(args[0])
  let sql = args[1]
  let outputJson = false
  let limit = null

  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--json') outputJson = true
    if (args[i] === '--limit' && args[i + 1]) limit = parseInt(args[++i])
  }

  // Dynamically load sqlite3
  let sqlite3, open
  try {
    sqlite3 = require('sqlite3')
      ; ({ open } = require('sqlite'))
  } catch (e) {
    console.error('Missing dependencies. Please run: npm install sqlite3 sqlite')
    process.exit(1)
  }

  const db = await open({ filename: dbPath, driver: sqlite3.Database })

  try {
    // Determine SQL type
    const sqlUpper = sql.trim().toUpperCase()
    const isRead = sqlUpper.startsWith('SELECT') || sqlUpper.startsWith('PRAGMA')

    if (isRead) {
      if (limit && !sqlUpper.includes('LIMIT')) {
        sql += ` LIMIT ${limit}`
      }
      const rows = await db.all(sql)
      if (outputJson) {
        console.log(JSON.stringify(rows, null, 2))
      } else {
        if (rows.length === 0) {
          console.log('(No results)')
        } else {
          // Simple table output
          const cols = Object.keys(rows[0])
          const colWidths = cols.map(c => {
            const maxData = Math.max(...rows.map(r => String(r[c] ?? 'NULL').length))
            return Math.max(c.length, maxData, 4)
          })
          const sep = colWidths.map(w => '-'.repeat(w + 2)).join('+')
          console.log(sep)
          console.log('| ' + cols.map((c, i) => c.padEnd(colWidths[i])).join(' | ') + ' |')
          console.log(sep)
          for (const row of rows) {
            console.log('| ' + cols.map((c, i) => String(row[c] ?? 'NULL').padEnd(colWidths[i])).join(' | ') + ' |')
          }
          console.log(sep)
          console.log(`(${rows.length} row${rows.length !== 1 ? 's' : ''})`)
        }
      }
    } else {
      const result = await db.run(sql)
      if (outputJson) {
        console.log(JSON.stringify(result, null, 2))
      } else {
        if (result.lastID) console.log(`Inserted row ID: ${result.lastID}`)
        if (result.changes !== undefined) console.log(`Rows affected: ${result.changes}`)
      }
    }
  } finally {
    await db.close()
  }
}

main().catch(e => {
  console.error('Error:', e.message)
  process.exit(1)
})