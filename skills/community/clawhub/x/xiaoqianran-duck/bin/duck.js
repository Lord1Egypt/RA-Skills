#!/usr/bin/env node
const DuckDBHelper = require('../lib/duckdb-helper');
const path = require('path');

const helper = new DuckDBHelper(process.env.DUCKDB_PATH || 'data.duckdb');

const args = process.argv.slice(2);
const cmd = args[0];

async function run() {
  await helper.connect();

  if (!cmd) {
    console.log('Usage: duck <command> [args]');
    console.log('Commands: import, hf, query, tables, describe, export, help');
    console.log('Example: node bin/duck.js import ./data.csv');
    console.log('Example: node bin/duck.js hf hf://datasets/.../data.parquet');
    return;
  }

  try {
    switch (cmd) {
      case 'import': {
        const file = args[1];
        if (!file) throw new Error('Please provide a file path');
        const res = await helper.importFile(file);
        console.log('✅ Imported:', res);
        break;
      }
      case 'hf': {
        const hfPath = args[1];
        if (!hfPath) throw new Error('Please provide hf:// path');
        const table = args[2];
        const res = await helper.importFromHF(hfPath, table);
        console.log('✅ Imported from HF:', res);
        break;
      }
      case 'query': {
        const sql = args.slice(1).join(' ');
        if (!sql) throw new Error('Please provide SQL query');
        const rows = await helper.query(sql);
        console.log(rows);
        break;
      }
      case 'tables': {
        const tables = await helper.listTables();
        console.log('Tables:', tables);
        break;
      }
      case 'describe':
      case 'desc': {
        const table = args[1];
        if (!table) throw new Error('Please provide table name');
        const info = await helper.getTableInfo(table);
        console.log(info);
        break;
      }
      case 'export': {
        const table = args[1];
        const out = args[2] || `${table}.parquet`;
        const fmt = args[3] || 'parquet';
        const res = await helper.exportTable(table, out, fmt);
        console.log('✅ Exported to', res);
        break;
      }
      case 'help':
      default:
        console.log('Available commands:');
        console.log('  import <file>          Import local file (csv/json/parquet/xlsx)');
        console.log('  hf <hf-path> [table]   Import from Hugging Face');
        console.log('  query "SELECT ..."     Run a SQL query');
        console.log('  tables                 List tables');
        console.log('  describe <table>       Describe table schema');
        console.log('  export <table> [file] [format]   Export table');
        break;
    }
  } catch (err) {
    console.error('Error:', err.message);
  } finally {
    await helper.close();
  }
}

run();
