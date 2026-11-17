# `src-tauri/src/encryption/mod.rs` (optional)

Authenticated encryption for API keys / tokens / other secrets at rest. Pattern: AES-256-GCM ciphertext + Argon2id-derived key from a per-install salt + a hardware-bound machine ID for additional binding.

Only generate this module if the user explicitly asked for it. Many apps don't need it (they store no secrets) or use OS-native keychains (`security-framework` on macOS, Windows DPAPI, Linux Secret Service) instead.

```rust
//! Encrypted secrets at rest. AES-256-GCM + Argon2id + hardware-bound salt.
//!
//! Threat model: protects against casual disk reads (backup syncs, malware
//! grepping files, accidental leaks via shared screenshots). Does NOT protect
//! against a privileged process on the same machine. For higher assurance,
//! integrate the OS-native keychain.

use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm, Nonce,
};
use argon2::{Algorithm, Argon2, Params, Version};
use base64::{engine::general_purpose::STANDARD as BASE64, Engine};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EncryptedApiKey {
    pub ciphertext: String,  // base64
    pub nonce: String,       // base64 (12 bytes)
    pub salt: String,        // base64 (≥16 bytes)
}

#[derive(Debug, thiserror::Error)]
pub enum EncryptionError {
    #[error("key derivation failed: {0}")]
    KeyDerivation(String),
    #[error("encryption failed: {0}")]
    Encrypt(String),
    #[error("decryption failed: {0}")]
    Decrypt(String),
    #[error("invalid base64: {0}")]
    Base64(#[from] base64::DecodeError),
    #[error("invalid machine ID: {0}")]
    MachineId(String),
}

/// Hardware-bound machine identifier. Combined with the per-install salt.
fn get_machine_id() -> Result<String, EncryptionError> {
    #[cfg(target_os = "macos")]
    {
        let out = std::process::Command::new("ioreg")
            .args(["-rd1", "-c", "IOPlatformExpertDevice"])
            .output()
            .map_err(|e| EncryptionError::MachineId(e.to_string()))?;
        let s = String::from_utf8_lossy(&out.stdout);
        for line in s.lines() {
            if line.contains("IOPlatformUUID") {
                if let (Some(a), Some(b)) = (line.find('"'), line.rfind('"')) {
                    if a != b { return Ok(line[a + 1..b].to_string()); }
                }
            }
        }
        Err(EncryptionError::MachineId("IOPlatformUUID not found".into()))
    }

    #[cfg(target_os = "windows")]
    {
        use std::os::windows::process::CommandExt;
        const CREATE_NO_WINDOW: u32 = 0x08000000;
        let out = std::process::Command::new("cmd")
            .creation_flags(CREATE_NO_WINDOW)
            .args(["/C", "wmic csproduct get uuid"])
            .output()
            .map_err(|e| EncryptionError::MachineId(e.to_string()))?;
        let s = String::from_utf8_lossy(&out.stdout);
        for line in s.lines().map(str::trim) {
            if !line.is_empty() && !line.contains("UUID") {
                return Ok(line.to_string());
            }
        }
        Err(EncryptionError::MachineId("UUID not found".into()))
    }

    #[cfg(target_os = "linux")]
    {
        // /etc/machine-id is stable per install on most distros.
        match std::fs::read_to_string("/etc/machine-id") {
            Ok(s) => Ok(s.trim().to_string()),
            Err(_) => Err(EncryptionError::MachineId("/etc/machine-id unavailable".into())),
        }
    }
}

fn derive_key(machine_id: &str, salt: &[u8]) -> Result<[u8; 32], EncryptionError> {
    // Argon2id parameters tuned for ~300ms on a modern laptop. Tune as the
    // user-facing latency budget allows.
    let params = Params::new(64 * 1024, 3, 1, Some(32))
        .map_err(|e| EncryptionError::KeyDerivation(e.to_string()))?;
    let argon2 = Argon2::new(Algorithm::Argon2id, Version::V0x13, params);

    let mut key = [0u8; 32];
    argon2
        .hash_password_into(machine_id.as_bytes(), salt, &mut key)
        .map_err(|e| EncryptionError::KeyDerivation(e.to_string()))?;
    Ok(key)
}

pub fn encrypt_api_key(plaintext: &str) -> Result<EncryptedApiKey, EncryptionError> {
    let machine_id = get_machine_id()?;

    // Per-encryption salt; never reuse.
    let mut salt = [0u8; 16];
    use rand::RngCore;
    rand::rngs::OsRng.fill_bytes(&mut salt);

    let key_bytes = derive_key(&machine_id, &salt)?;
    let cipher = Aes256Gcm::new_from_slice(&key_bytes)
        .map_err(|e| EncryptionError::Encrypt(e.to_string()))?;

    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
    let ciphertext = cipher
        .encrypt(&nonce, plaintext.as_bytes())
        .map_err(|e| EncryptionError::Encrypt(e.to_string()))?;

    Ok(EncryptedApiKey {
        ciphertext: BASE64.encode(&ciphertext),
        nonce: BASE64.encode(nonce),
        salt: BASE64.encode(salt),
    })
}

pub fn decrypt_api_key(enc: &EncryptedApiKey) -> Result<String, EncryptionError> {
    let machine_id = get_machine_id()?;
    let salt = BASE64.decode(&enc.salt)?;
    let nonce_bytes = BASE64.decode(&enc.nonce)?;
    let ciphertext = BASE64.decode(&enc.ciphertext)?;

    let key_bytes = derive_key(&machine_id, &salt)?;
    let cipher = Aes256Gcm::new_from_slice(&key_bytes)
        .map_err(|e| EncryptionError::Decrypt(e.to_string()))?;

    let nonce = Nonce::from_slice(&nonce_bytes);
    let plaintext = cipher
        .decrypt(nonce, ciphertext.as_ref())
        .map_err(|e| EncryptionError::Decrypt(e.to_string()))?;

    String::from_utf8(plaintext).map_err(|e| EncryptionError::Decrypt(e.to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trip() {
        let secret = "sk-test-1234567890";
        let encrypted = encrypt_api_key(secret).expect("encrypt");
        let decrypted = decrypt_api_key(&encrypted).expect("decrypt");
        assert_eq!(decrypted, secret);
    }

    #[test]
    fn different_ciphertext_each_time() {
        // Different salts + nonces should produce different ciphertexts.
        let a = encrypt_api_key("same secret").unwrap();
        let b = encrypt_api_key("same secret").unwrap();
        assert_ne!(a.ciphertext, b.ciphertext);
    }
}
```

## Dependencies needed in `Cargo.toml`

```toml
aes-gcm = "<latest>"
argon2 = "<latest>"
base64 = "<latest>"
rand = "<latest>"
thiserror = "<latest>"
```

## Auto-migrate plaintext on load

When deserializing settings, detect legacy plaintext API keys and re-encrypt:

```rust
// In settings/storage.rs deserialize_settings(&Value):
if let Some(v) = json.get("openaiApiKey") {
    if let Some(obj) = v.as_object() {
        if let (Some(ct), Some(n), Some(s)) = (
            obj.get("ciphertext").and_then(|x| x.as_str()),
            obj.get("nonce").and_then(|x| x.as_str()),
            obj.get("salt").and_then(|x| x.as_str()),
        ) {
            settings.openai_api_key = Some(EncryptedApiKey {
                ciphertext: ct.into(), nonce: n.into(), salt: s.into(),
            });
        }
    } else if let Some(plaintext) = v.as_str() {
        // Try parsing as already-encrypted JSON string first.
        if let Ok(enc) = serde_json::from_str::<EncryptedApiKey>(plaintext) {
            settings.openai_api_key = Some(enc);
        } else if !plaintext.is_empty() {
            // Legacy plaintext — auto-migrate.
            tracing::warn!("Found plaintext API key — migrating to encrypted format");
            if let Ok(enc) = crate::encryption::encrypt_api_key(plaintext) {
                settings.openai_api_key = Some(enc);
            }
        }
    }
}
```

## Threat model — be honest

This module protects against:
- Disk reads by other users on a shared machine (when filesystem permissions are correct).
- Stolen settings files / backup leaks.
- Casual scanning by malware that doesn't escalate privileges.

This module does **not** protect against:
- A privileged process on the same user account (it can read `IOPlatformUUID` and reproduce the same key).
- A debugger attached to the running app (memory has plaintext after decrypt).
- Hardware-level attacks (cold boot, side channels).

For higher assurance, integrate the OS keychain:
- macOS: `security-framework` crate, `SecKeychainItem`.
- Windows: `windows-sys` + DPAPI (`CryptProtectData`).
- Linux: `libsecret` via the `secret-service` crate.

Document the threat model in your project's `SECURITY.md` so users have realistic expectations.
