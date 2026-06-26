# openclaw-evidenceops

> Forensic-grade evidence management for OpenClaw with chain of custody

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org/)

## Overview

EvidenceOps provides a complete solution for forensic evidence handling in OpenClaw:

- **Skill** (`evidenceops`) - Runbook for media triage and chain of custody
- **Plugin** (`@openclaw/evidence-vault`) - Vault backend with pluggable storage drivers

### Features

- 🔒 **Immutable Storage** - Append-only vault with cryptographic hashes
- 🔗 **Chain of Custody** - Tamper-evident hash chain for all operations
- 📋 **Audit Trail** - Complete JSONL logging with secret redaction
- 🔍 **Integrity Verification** - Verify evidence hasn't been modified
- 📦 **Export** - Generate archives with hash verification
- 🏷️ **Sensitivity Tagging** - Classify evidence by confidentiality
- ⏱️ **Retention Policies** - Configurable retention with legal hold

## Repository Structure

```
openclaw-evidenceops/
├── skill-evidenceops/           # Skill for ClawHub
│   ├── SKILL.md                 # Main skill definition
│   ├── templates/               # Schemas and examples
│   │   ├── manifest.schema.json
│   │   ├── case-manifest.example.json
│   │   └── chain-of-custody.example.md
│   └── docs/
│       ├── SECURITY.md
│       └── PRIVACY.md
│
├── plugin-evidence-vault/       # Plugin for OpenClaw
│   ├── src/
│   │   ├── index.ts             # Entry point
│   │   ├── types.ts             # Type definitions
│   │   ├── drivers/             # Storage drivers
│   │   │   ├── interface.ts
│   │   │   ├── filesystem.ts    # Local storage
│   │   │   └── s3.ts            # S3/MinIO storage
│   │   ├── tools/               # OpenClaw tools
│   │   │   └── index.ts
│   │   └── utils/               # Utilities
│   │       ├── crypto.ts
│   │       ├── path.ts
│   │       └── redaction.ts
│   ├── tests/
│   ├── package.json
│   └── tsconfig.json
│
├── docs/
│   └── DESIGN.md                # Architecture and threat model
│
├── examples/
│   ├── config/
│   │   └── openclaw.example.yaml
│   └── demo/
│       └── sample-manifest.json
│
├── .github/workflows/
│   ├── ci.yml
│   └── security.yml
│
├── README.md
└── LICENSE
```

## Quick Start

### 1. Install the Plugin

```bash
cd plugin-evidence-vault
npm install
npm run build
```

### 2. Configure OpenClaw

```yaml
# ~/.openclaw/openclaw.yaml
plugins:
  evidence-vault:
    driver: filesystem
    basePath: /var/evidence-vault
    maxFileSizeBytes: 524288000
    defaultRetentionDays: 2555
    channelAllowlist:
      - whatsapp
      - telegram
    requirePairing: true
```

### 3. Install the Skill

```bash
# Via ClawHub (when published)
openclaw skill install evidenceops

# Or manually
cp -r skill-evidenceops ~/.openclaw/skills/evidenceops
```

### 4. Use in OpenClaw

```
User: I need to add this image as evidence for case-2026-001
OpenClaw: [Uses evidenceops skill to ingest with chain of custody]
```

## Plugin API

### Tools

| Tool | Description |
|------|-------------|
| `evidence.ingest` | Ingest file into vault |
| `evidence.verify` | Verify evidence integrity |
| `evidence.manifest` | Get case manifest |
| `evidence.export` | Export case as archive |
| `evidence.access_log` | Get audit trail |

### Example Usage

```typescript
import { initializeVault } from '@openclaw/evidence-vault';

const vault = await initializeVault({
  driver: 'filesystem',
  basePath: '/var/evidence-vault',
});

// Ingest evidence
const result = await vault.ingest({
  filePath: '/tmp/photo.jpg',
  filename: 'incident_photo.jpg',
  caseId: 'case-2026-001',
  channel: 'whatsapp',
  sender: 'user-123',
});

console.log(result);
// {
//   success: true,
//   evidenceId: 'ev-abc123...',
//   sha256: 'a1b2c3...',
//   vaultUrl: 'file:///var/evidence-vault/...',
//   timestamp: '2026-02-17T10:30:00.000Z'
// }

// Verify integrity
const verify = await vault.verify({
  evidenceId: result.evidenceId,
});

// Get manifest
const manifest = await vault.manifest({
  caseId: 'case-2026-001',
});

// Export case
const exportResult = await vault.export({
  caseId: 'case-2026-001',
  format: 'zip',
});
```

## Storage Drivers

### Filesystem Driver (Default)

Local storage with append-only mode:

```yaml
plugins:
  evidence-vault:
    driver: filesystem
    basePath: /var/evidence-vault
```

Features:
- Append-only storage
- Hash chain in manifests
- JSONL audit logs
- No external dependencies

### S3/MinIO Driver

Cloud storage with Object Lock support:

```yaml
plugins:
  evidence-vault:
    driver: s3
    s3:
      endpoint: https://s3.example.com  # Optional for MinIO
      bucket: evidence-vault
      region: us-east-1
      objectLock: true
```

Features:
- S3 Object Lock for immutability
- Versioning support
- Metadata storage
- Presigned URLs for access

## Security

### Key Protections

1. **Path Traversal Prevention** - All paths validated
2. **Immutable Originals** - Read-only after ingest
3. **Hash Chain** - Tamper detection
4. **Secret Redaction** - No secrets in logs
5. **Channel Controls** - Allowlist/denylist enforcement

See [SECURITY.md](skill-evidenceops/docs/SECURITY.md) for details.

## Privacy

### Data Protection

- Local-first (no cloud sync)
- PII redaction in logs
- Configurable retention
- LGPD/GDPR compliant

See [PRIVACY.md](skill-evidenceops/docs/PRIVACY.md) for details.

## Development

### Setup

```bash
git clone https://github.com/openclaw/openclaw-evidenceops.git
cd openclaw-evidenceops/plugin-evidence-vault
npm install
```

### Build

```bash
npm run build
```

### Test

```bash
npm test
npm run test:coverage
```

### Lint

```bash
npm run lint
npm run typecheck
```

## Documentation

- [DESIGN.md](docs/DESIGN.md) - Architecture and threat model
- [SKILL.md](skill-evidenceops/SKILL.md) - Skill documentation
- [SECURITY.md](skill-evidenceops/docs/SECURITY.md) - Security policy
- [PRIVACY.md](skill-evidenceops/docs/PRIVACY.md) - Privacy policy

## Publishing

### Skill to ClawHub

1. Validate skill structure
2. Ensure SKILL.md has correct frontmatter
3. Follow ClawHub submission process (see official docs)

### Plugin to npm

```bash
cd plugin-evidence-vault
npm version patch  # or minor, major
npm publish
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and lint
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE)

## Support

- **Issues:** [GitHub Issues](https://github.com/openclaw/openclaw-evidenceops/issues)
- **Discussions:** [GitHub Discussions](https://github.com/openclaw/openclaw-evidenceops/discussions)

## Acknowledgments

Built for the OpenClaw community with security and privacy as core principles.
