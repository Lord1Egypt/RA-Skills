// Cargo.toml:
// [package]
// name = "app"
// version = "0.1.0"
// edition = "2024"
//
// [dependencies]
// anyhow = "1"
// clap = { version = "4", features = ["derive"] }
// serde = { version = "1", features = ["derive"] }
// serde_json = "1"

use anyhow::{Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Parser)]
struct Cli {
    /// JSON input file
    #[arg(long)]
    input: PathBuf,

    /// JSON output file
    #[arg(long, default_value = "out.json")]
    out: PathBuf,
}

#[derive(Debug, Serialize, Deserialize)]
struct Record {
    id: u64,
    name: String,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let raw = std::fs::read_to_string(&cli.input)
        .with_context(|| format!("read {}", cli.input.display()))?;
    let record: Record = serde_json::from_str(&raw).context("parse JSON")?;
    let pretty = serde_json::to_string_pretty(&record)?;
    std::fs::write(&cli.out, pretty).with_context(|| format!("write {}", cli.out.display()))?;
    println!("{}", cli.out.display());
    Ok(())
}
