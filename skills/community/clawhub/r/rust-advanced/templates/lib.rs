// Library shape: no anyhow in the public API.
use thiserror::Error;

#[derive(Debug, Error)]
pub enum CoreError {
    #[error("empty input")]
    Empty,
}

pub fn normalize(input: &str) -> Result<String, CoreError> {
    let s = input.trim();
    if s.is_empty() {
        return Err(CoreError::Empty);
    }
    Ok(s.to_lowercase())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn trims_and_lowercases() {
        assert_eq!(normalize("  Hello  ").unwrap(), "hello");
    }

    #[test]
    fn rejects_empty() {
        assert!(normalize("   ").is_err());
    }
}
