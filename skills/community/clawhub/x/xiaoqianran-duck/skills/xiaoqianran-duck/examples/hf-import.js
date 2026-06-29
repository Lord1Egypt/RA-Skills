const DuckDBHelper = require('../lib/duckdb-helper');
const path = require('path');
const fs = require('fs');

async function main() {
  console.log('=== xiaoqianran-duck : HF import demo (using helper) ===\n');

  const helper = new DuckDBHelper(path.join(__dirname, '..', 'data.duckdb'));

  // Optional: set HF token for gated datasets
  // await helper.setHFTtoken('hf_your_token_here');
  // or put HF_TOKEN=... in .env next to data.duckdb

  const hfPath = 'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet';

  console.log(`Importing from: ${hfPath}`);
  const result = await helper.importFromHF(hfPath, 'imported_hf');

  console.log(`\n✅ Successfully imported ${result.rowCount} rows`);
  console.log(`Local DB: ${helper.dbPath}`);
  console.log(`File size: ${fs.existsSync(helper.dbPath) ? fs.statSync(helper.dbPath).size : 0} bytes\n`);

  const sample = await helper.query('SELECT * FROM imported_hf LIMIT 3');
  console.log('Sample data:');
  console.log(sample);

  console.log('\n=== Done ===');
  await helper.close();
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
