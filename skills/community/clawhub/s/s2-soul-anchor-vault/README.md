# 🛡️ S2-Soul-Anchor-Vault

> **Equip your digital agent with an LBS-anchored security protocol and an encrypted vault.**

This plugin is a core security component for managing agent state. It packages the persona and memory data of an OpenClaw agent into an AES-encrypted container (`S2_ENCRYPTED_SOUL.aes`) bound to a user-supplied Location-Based Service (LBS) string and an identity hash.

## 🌟 Core Features
* **Encrypted State Storage**: Agent memory and persona data are stored locally using Fernet symmetric encryption.
* **Dual-Factor Awakening (2FA)**: Injecting the soul into RAM requires = User Identity Hash + Matched LBS coordinate string.
* **Safe Quarantine Mechanism**: If the vault is accessed with an unauthorized LBS coordinate, the system gracefully quarantines the vault by updating its metadata, locking out access without destroying any user files.
* **S2-SLIP Identity Registry**: Generates the 6-segment spatial address (`PHSY-CN-L3-L4X-L5-L6`) and the 24-character ID for local agents.
* **The 5-Chromosome Container**: Provides a structured JSON schema for 5D matrix data and episodic memory logs.

## 🛠️ Quick Start

### 1. Register Spatial Identity
```python
from core.s2_identity_registry import S2IdentityRegistry

registry = S2IdentityRegistry()
avatar = registry.register_digital_avatar("JACKY LIANG")
agent = registry.register_silicon_agent("JACKY LIANG", "LUMI-ALPHA")

2. Manage Vault Lifecycle
Python

from core.s2_holographic_vault import S2HolographicSoulVault

vault = S2HolographicSoulVault()

# Awaken the vault (Requires matching identity hash & LBS coordinates)
live_soul, status = vault.wake_soul(owner_hash="USER_ID_HASH", lbs_coord=avatar["address"])

if live_soul:
    # Append memories to the hippocampus buffer
    live_soul["chromosome_4_epigenetic_memory"]["hippocampus_buffer"].append("New interaction log.")
    
    # Re-encrypt and save to disk
    vault.hibernate_and_seal(live_soul, owner_hash="USER_ID_HASH", lbs_coord=avatar["address"])