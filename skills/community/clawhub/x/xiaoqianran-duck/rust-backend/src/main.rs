use duckdb::{Connection, Result};
use std::env;

fn main() -> Result<()> {
    let db_path = env::args().nth(1).unwrap_or_else(|| "data.duckdb".to_string());
    let conn = Connection::open(&db_path)?;

    println!("Connected to DuckDB: {}", db_path);

    // Load extensions (httpfs for HF, excel for xlsx)
    conn.execute_batch("INSTALL httpfs; LOAD httpfs;")?;
    conn.execute_batch("INSTALL excel; LOAD excel;")?;
    println!("Extensions loaded.");

    // Example 1: Import from Hugging Face
    println!("\n--- Importing from Hugging Face ---");
    let hf_path = "hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet";
    conn.execute(&format!(
        "CREATE OR REPLACE TABLE hf_example AS SELECT * FROM '{}'",
        hf_path
    ), [])?;

    let count: i64 = conn.query_row("SELECT COUNT(*) FROM hf_example", [], |row| row.get(0))?;
    println!("HF rows imported: {}", count);

    // Example 2: Local CSV (create a temp one)
    println!("\n--- Local CSV example ---");
    std::fs::write("/tmp/rust_sample.csv", "id,name\n1,duck\n2,quack\n").ok();
    conn.execute(
        "CREATE OR REPLACE TABLE local_csv AS SELECT * FROM read_csv_auto('/tmp/rust_sample.csv')",
        [],
    )?;

    let rows: Vec<(i32, String)> = conn
        .prepare("SELECT * FROM local_csv")?
        .query_map([], |row| Ok((row.get(0)?, row.get(1)?)))?
        .collect::<Result<Vec<_>>>()?;

    println!("Local CSV sample: {:?}", rows);

    println!("\n✅ Rust + DuckDB + HF + local files working!");
    println!("This can be the backend for a Tauri app.");

    Ok(())
}
