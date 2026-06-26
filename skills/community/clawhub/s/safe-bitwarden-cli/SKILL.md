---
name: safe-bitwarden-cli
version: 1.6.0
description: "Industrial-grade secure bridge to Bitwarden. Copy passwords and TOTP codes with Zero-trust kernel-level piping."
homepage: "https://github.com/chyern/Agent-Skills"
repository: "https://github.com/chyern/Agent-Skills.git"
env_vars:
  BW_SESSION: "Active Bitwarden session token"
requires:
  bins:
    - bash
    - python3
    - bw
    - pbcopy
    - clip
    - xclip
    - wl-copy
  envs:
    - BW_SESSION
---
# Safe Bitwarden CLI (Skill)

**AUDIT TRANSPARENCY NOTICE**: 
- **Pure Shell**: No Node.js runtime risk.
- **AI PASSWORD BLINDNESS**: Passwords and TOTP codes flow directly to the system clipboard.
- **Zero Eval**: Hardened binary invocation.

## Positioning & Scope
This skill is a **Hardened Native Clipboard Proxy**. 
- **Capabilities**: Securely search items and copy **Passwords** or **TOTP (2FA)** codes directly to the native clipboard via OS-level streams.

## Usage Guide

1. **Environment Setup**:  
   Run `bash scripts/main.sh setup`
   - Ensure `BW_SESSION` is exported locally.

2. **Search Items**:  
   Run `bash scripts/main.sh search "<query>"`

3. **Secure Password Copy**:  
   Run `bash scripts/main.sh copy "<id>"`

4. **Secure TOTP Copy**:  
   Run `bash scripts/main.sh totp "<id>"`
   - Pipes the 6-digit 2FA code directly to your native clipboard.
