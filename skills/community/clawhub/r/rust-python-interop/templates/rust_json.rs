// Cargo.toml: serde_json = "1"
use std::io::{self, Read, Write};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let value: serde_json::Value = serde_json::from_str(&input)?;
    let response = serde_json::json!({
        "ok": true,
        "echo": value,
    });

    writeln!(io::stdout(), "{}", serde_json::to_string(&response)?)?;
    Ok(())
}
