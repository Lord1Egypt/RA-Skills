# UPGRADE.md — SPM Version Migration Guide

## v2.0 → v3.0 (Current)

### 🆕 New Features
- **WBS Hash Attestation**: SHA-256 integrity protection for your task ledger
- **Hook Auto-Injection**: Active tasks automatically injected into context before tool calls
- **Session Recovery Reports**: Auto-generated recovery guidance from heartbeat logs
- **Parallel Task Pointers**: `switch-ledger.sh` for multi-task isolation
- **SPM Minimal Mode**: 5-rule lightweight mode for small projects
- **Template/Script Separation**: Clear distinction between skill files and project files

### 🔧 New Scripts (copy to your project)

```bash
# From SPM skill directory:
cp scripts/*.sh scripts/*.py your-project/scripts/
# Or run init-spm.sh which copies them automatically
```

### 📝 WBS Ledger Changes

- New `Resume Point` column in Heartbeat Log (backward compatible)
- Hash attestation notice added to template
- Ledger now supports `---BEGIN/END WBS DATA---` delimiters for safe injection

### ⚙️ New Config Fields

```json
{
  "spm": {
    "mode": "full",          // "full" | "minimal"
    "attestation": {
      "enabled": true,
      "autoAttest": true     // Auto-attest after WBS updates
    },
    "hookInjection": {
      "enabled": true,
      "maxActiveTasks": 20,
      "maxChars": 1500
    }
  }
}
```

### 🚫 Breaking Changes
None — v3.0 is fully backward compatible with v2.0 ledgers.

### 🔄 Manual Migration Steps

1. **Copy new scripts**: `cp -r spm/scripts/ your-project/scripts/`
2. **Add Resume Point column** to your existing Heartbeat Log table
3. **Run attestation once**: `bash scripts/attest-wbs.sh`
4. **Update openclaw.json** with new config fields (optional)
5. **Done** — existing WBS ledgers work without modification

---

## v1.0 → v2.0 (Historical)

- Added five-phase lifecycle (Requirement → Planning → Execution → Quality → Delivery)
- Introduced WBS Task Ledger as single source of truth
- Added Heartbeat Logging (10min interval)
- Three-tier quality gates (Always/Ask/Never)
- 13 Superpowers workflows
- Subagent dispatch system
- Git worktree parallel isolation
