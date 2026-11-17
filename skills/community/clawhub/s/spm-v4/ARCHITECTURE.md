# SPM v4 Node.js Architecture Reference

## Project Structure
```
src/
├── index.js          # Main exports
├── cli.js            # CLI entry point (spm init, attest, verify, etc.)
├── config/
│   ├── default.yaml  # Default configuration
│   ├── schema.js     # Config validation schema
│   └── loader.js     # Config loader (YAML → JS object)
├── engine/
│   ├── index.js      # State machine engine
│   ├── phases.js     # Phase definitions and transitions
│   └── workflow.js   # Workflow orchestration
├── event-store/
│   ├── index.js      # Event store main
│   ├── domains.js    # Audit / Integrity / Quality domains
│   └── storage.js    # File-based storage backend
├── security/
│   ├── index.js      # Security gate main
│   ├── policy.js     # Policy engine (YAML rules)
│   └── classifier.js # Command classification
├── wbs/
│   ├── index.js      # WBS ledger management
│   ├── attest.js     # SHA-256 hash attestation
│   └── merkle.js     # Merkle tree incremental hashing
├── hooks/
│   ├── index.js      # Hook registry and middleware
│   └── inject.js     # Context injection
├── session/
│   ├── index.js      # Session recovery
│   └── heartbeat.js  # Heartbeat log management
└── cli/
    ├── commands.js   # CLI command registry
    ├── init.js       # spm init
    ├── attest.js     # spm attest
    ├── verify.js     # spm verify
    ├── quality.js    # spm quality-check
    ├── status.js     # spm status
    └── doctor.js     # spm doctor (health check)
```

## Core API

### Engine
```js
const engine = new Engine(config);
engine.phase('planning');       // Enter planning phase
engine.transition('execute');   // Transition to execution phase
engine.currentPhase();          // Get current phase
```

### Event Store
```js
const store = new EventStore(config);
store.push('audit', event);     // Push to audit domain
store.query('quality', filter); // Query quality events
```

### Security Gate
```js
const gate = new SecurityGate(policy);
gate.check('rm -rf /');          // Returns { action: 'block', level: 'dangerous' }
```

### WBS
```js
const wbs = new WBS(config);
wbs.load('docs/spm/ledger.md');
wbs.update('task-3', { status: 'done' });
wbs.attest();                    // SHA-256 + Merkle
```

### CLI Commands
```bash
spm init <project-name>          # Initialize project
spm attest [ledger-path]         # Generate hash attestation
spm verify [ledger-path]         # Verify WBS integrity
spm quality-check [ledger-path]  # Run quality gates
spm status                       # Show current SPM state
spm doctor                       # Health check
```