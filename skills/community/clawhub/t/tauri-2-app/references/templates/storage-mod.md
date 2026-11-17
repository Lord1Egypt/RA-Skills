# `src-tauri/src/storage/mod.rs`

Shared JSON-on-disk utilities used by `settings/`, `history/`, `error_log/`, and any other module that persists structured data. **Every persistent feature uses these primitives** — never raw `std::fs` against `app_data_dir`.

```rust
//! Shared storage utilities: paths, JSON I/O, IDs, timestamps, pruning.

use std::fs;
use std::path::PathBuf;
use chrono::Utc;
use serde::{de::DeserializeOwned, Serialize};
use tauri::{AppHandle, Manager};

/// Resolve and create the app data directory.
pub fn get_app_data_dir(app: &AppHandle) -> Result<PathBuf, String> {
    let dir = app
        .path()
        .app_data_dir()
        .map_err(|e| format!("Failed to get app data directory: {}", e))?;
    fs::create_dir_all(&dir)
        .map_err(|e| format!("Failed to create app data directory: {}", e))?;
    Ok(dir)
}

/// Resolve a path inside the app data directory.
pub fn get_storage_path(app: &AppHandle, filename: &str) -> Result<PathBuf, String> {
    Ok(get_app_data_dir(app)?.join(filename))
}

/// Load a `Vec<T>` from a JSON file. Returns empty on missing / invalid file
/// (logged at info / error level).
pub fn load_json<T: DeserializeOwned>(app: &AppHandle, filename: &str) -> Vec<T> {
    let path = match get_storage_path(app, filename) {
        Ok(p) => p,
        Err(e) => {
            tracing::error!("Storage path error for {}: {}", filename, e);
            return Vec::new();
        }
    };

    if !path.exists() {
        tracing::info!("Storage file {} not found, starting empty", filename);
        return Vec::new();
    }

    let content = match fs::read_to_string(&path) {
        Ok(c) => c,
        Err(e) => {
            tracing::error!("Failed to read {}: {}", filename, e);
            return Vec::new();
        }
    };

    match serde_json::from_str::<Vec<T>>(&content) {
        Ok(entries) => {
            tracing::info!("Loaded {} entries from {}", entries.len(), filename);
            entries
        }
        Err(e) => {
            tracing::error!("Failed to parse JSON for {}: {}", filename, e);
            Vec::new()
        }
    }
}

/// Save a slice as pretty-printed JSON to `filename` inside the app data dir.
pub fn save_json<T: Serialize>(
    app: &AppHandle,
    filename: &str,
    entries: &[T],
) -> Result<(), String> {
    let path = get_storage_path(app, filename)?;
    let json = serde_json::to_string_pretty(entries)
        .map_err(|e| format!("Failed to serialize: {}", e))?;
    fs::write(&path, json).map_err(|e| format!("Failed to write {}: {}", filename, e))?;
    tracing::info!("Saved {} entries to {}", entries.len(), path.display());
    Ok(())
}

/// Generate a unique ID from nanoseconds since epoch.
pub fn generate_id() -> String {
    format!("{:x}", Utc::now().timestamp_nanos_opt().unwrap_or(0))
}

/// Generate a unique ID with a prefix.
pub fn generate_id_with_prefix(prefix: &str) -> String {
    format!("{}{:x}", prefix, Utc::now().timestamp_nanos_opt().unwrap_or(0))
}

/// Current ISO 8601 timestamp (UTC).
pub fn get_timestamp() -> String {
    Utc::now().to_rfc3339()
}

/// Parse an RFC 3339 timestamp to seconds since epoch.
pub fn parse_timestamp_to_seconds(s: &str) -> Option<u64> {
    chrono::DateTime::parse_from_rfc3339(s)
        .ok()
        .map(|dt| dt.timestamp() as u64)
}

/// Trait for entries that carry a timestamp string.
pub trait Timestamped {
    fn timestamp(&self) -> &str;
}

/// Drop entries older than `days_to_keep` days. Unparseable timestamps are kept.
pub fn prune_entries_by_age<T: Timestamped>(entries: Vec<T>, days_to_keep: u64) -> Vec<T> {
    let cutoff = Utc::now().timestamp() as u64 - (days_to_keep * 24 * 3600);
    entries
        .into_iter()
        .filter(|e| match parse_timestamp_to_seconds(e.timestamp()) {
            Some(s) => s > cutoff,
            None => {
                tracing::warn!("Unparseable timestamp '{}', keeping entry", e.timestamp());
                true
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ids_are_unique_within_a_nanosecond_resolution() {
        let a = generate_id();
        std::thread::sleep(std::time::Duration::from_nanos(1));
        let b = generate_id();
        assert_ne!(a, b);
    }

    #[test]
    fn timestamp_is_rfc3339() {
        let ts = get_timestamp();
        assert!(chrono::DateTime::parse_from_rfc3339(&ts).is_ok());
    }

    #[test]
    fn prune_drops_old_entries() {
        struct E(String);
        impl Timestamped for E {
            fn timestamp(&self) -> &str { &self.0 }
        }
        let now = Utc::now();
        let old = now - chrono::Duration::days(10);
        let new = now - chrono::Duration::days(1);
        let entries = vec![
            E(old.to_rfc3339()),
            E(new.to_rfc3339()),
        ];
        let kept = prune_entries_by_age(entries, 5);
        assert_eq!(kept.len(), 1);
    }
}
```

## Why use `chrono`

The "hand-rolled date math" pattern (`seconds_since_epoch / 86400`, manual leap-year tables, manual month-length tables) is a classic anti-pattern. It looks small but every special case is a future bug — DST, leap seconds, century leap years, year-2038 on 32-bit platforms. `chrono` is ~200KB compressed, well-tested, and used everywhere. Skip the temptation to "save a dep".

## Error handling philosophy

`load_json` returns `Vec<T>` rather than `Result<Vec<T>, _>`. Reasoning:
- Missing files are normal (first run).
- Parse errors are rare but should not crash the app — log and start fresh.
- Callers always want to keep going with an empty list rather than abort.

`save_json` returns `Result<_, String>` because a failed save is a real user-visible problem the UI should surface.

If a domain genuinely needs `Result<Vec<T>, _>` semantics on load (e.g. settings that can't safely default), wrap this primitive in a domain-specific function that does the strictness check.
