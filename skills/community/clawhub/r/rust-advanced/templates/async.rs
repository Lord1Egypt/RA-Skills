// Cargo.toml:
// tokio = { version = "1", features = ["full"] }
// anyhow = "1"
use anyhow::Result;
use std::time::Duration;

async fn work(n: u64) -> u64 {
    tokio::time::sleep(Duration::from_millis(50)).await;
    n * 2
}

#[tokio::main]
async fn main() -> Result<()> {
    let a = tokio::spawn(work(10));
    let b = tokio::spawn(work(20));

    let joined = tokio::time::timeout(Duration::from_secs(2), async {
        (a.await?, b.await?)
    })
    .await??;

    println!("{} {}", joined.0, joined.1);
    Ok(())
}
