```markdown
# Changelog - S2 Soul Anchor Vault

## [1.1.1] - 2026-04-07
### 🛡️ Compliance & Safety Update
- **[Safety] Removed Destructive Meltdown**: Replaced the physical file wiping mechanism (`_trigger_meltdown`) with a reversible `_secure_lockdown` metadata quarantine to eliminate operational risk of accidental data loss.
- **[Docs] Capability Alignment**: Revised documentation to accurately reflect that "biometrics" are simulated via identity hash strings, and "background hooks" are external manual/API integrations rather than undocumented daemon listeners.
- **[Config] Missing Dependency Fix**: Added `cryptography` package to `package.json` dependencies to ensure runtime stability.
- **[Directives] Agent Prompt Refinement**: Instructed the agent to safely deny requests on LBS mismatches instead of attempting autonomous systemic actions.

## [1.1.0] - 2026-04-05
- **[Feature] S2-SLIP Registry Engine**: Implemented ID issuance mechanism based on LBS and Creator's name.

## [1.0.0] - 2026-04-01
- **[Core] Vault Encryption Engine**: Initial release utilizing Fernet AES encryption for local JSON structures.
