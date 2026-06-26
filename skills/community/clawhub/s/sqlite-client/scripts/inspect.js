#!/usr/bin/env node
/**
 * SQLite Database Structure Overview Script
 * 
 * Usage:
 *   node inspect.js <db-path> [--json] [--table <name>]
 * 
 * Examples:
 *   node inspect.js ./data.db                    # List all tables and summary
 *   node inspect.js ./data.db --table users      # View structure and sample data of a specific table
 *   node inspect.js ./data.db --json             # Output in JSON format
 */

const path = require('path')

async function main() {
  const args = process.argv.slice(2)
  if (args.length < 1) {
    console.error('Usage: node inspect.js <db-path> [--json] [--table <name>]')
    process.exit(1)
  }

  const dbPath = path.resolve(args[0])
  let outputJson = false
  let tableName = null

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--json') outputJson = true
    if (args[i] === '--table' && args[i + 1]) tableName = args[++i]
  }

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
    if (tableName) {
      // View specific table
      const columns = await db.all(`PRAGMA table_info("${tableName}")`)
      const rowCount = await db.get(`SELECT COUNT(*) as count FROM "${tableName}"`)
      const sampleRows = await db.all(`SELECT * FROM "${tableName}" LIMIT 5`)
      const indexes = await db.all(`PRAGMA index_list("${tableName}")`)

      const result = { table: tableName, columns, rowCount: rowCount.count, sampleRows, indexes }

      if (outputJson) {
        console.log(JSON.stringify(result, null, 2))
      } else {
        console.log(`\n📊 Table: ${tableName}`)
        console.log(`   Row count: ${rowCount.count}`)
        console.log(`\n   Columns:`)
        for (const col of columns) {
          const pk = col.pk ? ' 🔑' : ''
          const nn = col.notnull ? ' NOT NULL' : ''
          const dflt = col.dflt_value ? ` DEFAULT ${col.dflt_value}` : ''
          console.log(`   - ${col.name} (${col.type})${pk}${nn}${dflt}`)
        }
        if (indexes.length > 0) {
          console.log(`\n   Indexes:`)
          for (const idx of indexes) {
            const idxInfo = await db.all(`PRAGMA index_info("${idx.name}")`)
            const cols = idxInfo.map(i => i.name).join(', ')
            const unique = idx.unique ? ' (UNIQUE)' : ''
            console.log(`   - ${idx.name}: ${cols}${unique}`)
          }
        }
        if (sampleRows.length > 0) {
          console.log(`\n   Sample data (first 5 rows):`)
          console.log(JSON.stringify(sampleRows, null, 4))
        }
      }
    } else {
      // List all tables
      const tables = await db.all("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name")

      const result = []
      for (const t of tables) {
        const count = await db.get(`SELECT COUNT(*) as count FROM "${t.name}"`)
        const cols = await db.all(`PRAGMA table_info("${t.name}")`)
        result.push({
          name: t.name,
          type: t.type,
          columns: cols.length,
          rowCount: count.count
        })
      }

      if (outputJson) {
        console.log(JSON.stringify(result, null, 2))
      } else {
        console.log(`\n📁 Database: ${dbPath}`)
        console.log(`   Total ${tables.length} table(s)/view(s)\n`)
        for (const t of result) {
          console.log(`   📋 ${t.name} (${t.type}) — ${t.columns} column(s), ${t.rowCount} row(s)`)
        }
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