const DuckDBHelper = require('../lib/duckdb-helper');
const path = require('path');
const fs = require('fs');

async function main() {
  console.log('=== xiaoqianran-duck : Local File Import Demo ===\n');

  const helper = new DuckDBHelper(path.join(__dirname, '..', 'data.duckdb'));

  // Create sample files for demo
  const csvPath = path.join(__dirname, 'sample.csv');
  const jsonPath = path.join(__dirname, 'sample.json');
  const parquetPath = path.join(__dirname, 'sample.parquet');

  // Generate sample CSV
  fs.writeFileSync(csvPath, 'name,age,city\nAlice,28,Beijing\nBob,35,Shanghai\nCharlie,22,Shenzhen\n');

  // Generate sample JSON
  fs.writeFileSync(jsonPath, JSON.stringify([
    { product: 'Laptop', price: 5999, category: 'Electronics' },
    { product: 'Mouse', price: 99, category: 'Accessories' }
  ], null, 2));

  try {
    console.log('1. Importing CSV...');
    const csvResult = await helper.importFile(csvPath);
    console.log('   Result:', csvResult);

    console.log('\n2. Importing JSON...');
    const jsonResult = await helper.importFile(jsonPath);
    console.log('   Result:', jsonResult);

    console.log('\n3. Importing from Hugging Face (Parquet)...');
    const hfResult = await helper.importFromHF(
      'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet',
      'hf_sounds'
    );
    console.log('   Result:', hfResult);

    console.log('\n4. Listing tables in data.duckdb:');
    const tables = await helper.listTables();
    console.log('   Tables:', tables);

    console.log('\n5. Sample query on imported data:');
    const sample = await helper.query('SELECT * FROM sample LIMIT 3');
    console.log('   Sample rows:', sample);

    console.log('\n6. Exporting to Parquet...');
    const exportPath = path.join(__dirname, '..', 'exported_data.parquet');
    const exported = await helper.exportTable('hf_sounds', exportPath, 'parquet');
    console.log('   Exported to:', exported);

  } catch (err) {
    console.error('Error during demo:', err.message);
  } finally {
    await helper.close();
    // Clean up samples
    [csvPath, jsonPath].forEach(f => { if (fs.existsSync(f)) fs.unlinkSync(f); });
  }

  console.log('\n=== Demo completed. Check data.duckdb ===');
}

main().catch(console.error);
