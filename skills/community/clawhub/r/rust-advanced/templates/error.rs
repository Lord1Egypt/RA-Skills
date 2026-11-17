// Cargo.toml: thiserror = "2"
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("io: {0}")]
    Io(#[from] std::io::Error),

    #[error("json: {0}")]
    Json(#[from] serde_json::Error),

    #[error("invalid config: {0}")]
    Config(String),
}

pub fn load(path: &str) -> Result<String, AppError> {
    let text = std::fs::read_to_string(path)?;
    if text.trim().is_empty() {
        return Err(AppError::Config("empty file".into()));
    }
    Ok(text)
}
