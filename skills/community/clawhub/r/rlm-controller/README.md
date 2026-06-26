# RLM Controller

A safe, policy-driven framework for processing extremely long inputs using Retrieval-augmented Long-context Memory (RLM) patterns.

## Overview

**RLM Controller** enables LLM agents to process inputs that exceed typical context windows (50k+ characters) by:
- Storing input as external context files
- Intelligently slicing and searching content
- Spawning parallel subcalls for analysis
- Aggregating structured results with traceability

## Features

- 🧠 **Smart Slicing**: Keyword-based planning with fallback chunking
- 🔒 **Security-First**: Prompt injection mitigation, no code execution, strict limits
- ⚡ **Parallel Execution**: Async batch processing for speed
- 📊 **Full Traceability**: JSONL logging for every operation
- 🎯 **OpenClaw Native**: Designed for OpenClaw agent framework

## Quick Start

### 1. Store Long Input
```bash
python3 scripts/rlm_ctx.py store --infile input.txt --ctx-dir ./ctx
```

### 2. Generate Execution Plan
```bash
python3 scripts/rlm_auto.py \
  --ctx ./ctx/<ctx_id>.txt \
  --goal "analyze authentication logic" \
  --outdir ./run1
```

### 3. Create Async Batches (Optional)
```bash
python3 scripts/rlm_async_plan.py \
  --plan ./run1/plan.json \
  --batch-size 4 > ./run1/async_plan.json

python3 scripts/rlm_async_spawn.py \
  --async-plan ./run1/async_plan.json \
  --out ./run1/spawn.jsonl
```

### 4. Execute with OpenClaw
Use `sessions_spawn` to execute subcalls in parallel batches. See [docs/flows.md](docs/flows.md) for complete workflows.

## Architecture

```
rlm-controller/
├── scripts/           # Core utilities (~766 LOC)
│   ├── rlm_ctx.py            # Context store/peek/search/chunk
│   ├── rlm_plan.py           # Keyword-based slice planner
│   ├── rlm_auto.py           # Auto artifact generator
│   ├── rlm_async_plan.py     # Batch scheduler
│   ├── rlm_async_spawn.py    # Spawn manifest builder
│   ├── rlm_emit_toolcalls.py # Toolcall formatter
│   ├── rlm_batch_runner.py   # Assistant-driven executor
│   ├── rlm_runner.py         # JSONL orchestrator
│   ├── rlm_trace_summary.py  # Log summarizer
│   ├── rlm_path.py           # Shared path-validation helpers
│   ├── rlm_redact.py         # Secret pattern redaction
│   └── cleanup.sh            # Artifact cleanup
├── docs/              # Documentation
│   ├── flows.md              # Manual & async workflows
│   ├── policy.md             # Limits & decision rules
│   ├── security.md           # Security foundations
│   ├── security_checklist.md # Pre/during/post run checks
│   ├── security_audit_response.md # OpenClaw audit response
│   └── cleanup_ignore.txt    # Cleanup exclusions
└── SKILL.md           # OpenClaw skill manifest
```

## Security

RLM Controller is designed with **security-first principles**:

- ✅ **No code execution** - Only safelisted helper scripts
- ✅ **Prompt injection mitigation** - Input treated as data, not commands
- ✅ **Strict limits** - Max recursion: 1, max subcalls: 32, max slice: 16k chars
- ✅ **Bounded work** - Hard caps on batches and total slices
- ✅ **Least privilege** - Subcalls read-only by design

See [docs/security.md](docs/security.md) for detailed safeguards.

## Use Cases

- 📚 **Large Documentation**: Process entire codebases or API docs
- 📝 **Dense Logs**: Analyze thousands of log lines for patterns
- 🔍 **Repository Analysis**: Multi-file security audits
- 📊 **Dataset Processing**: Extract structured data from large files

## Requirements

- Python 3.7+
- OpenClaw framework (for `sessions_spawn` integration)
- Unix-like environment (bash scripts)

## Configuration

Default policies can be customized in [docs/policy.md](docs/policy.md):
- Max subcalls: 32
- Max slice size: 16k chars
- Batch size: 4
- Max recursion depth: 1

## OpenClaw Integration

This skill integrates with the [OpenClaw](https://github.com/Skywyze/openclaw) agent framework:
- Uses `sessions_spawn` for parallel subcalls
- Respects sub-agent constraints (no nested spawning)
- Compatible with OpenClaw's tool safety model

## Documentation

- [Getting Started Guide](docs/flows.md) - Manual & async workflows
- [Security Model](docs/security.md) - Threat model & mitigations
- [Policy Reference](docs/policy.md) - Limits & decision rules
- [Security Checklist](docs/security_checklist.md) - Operational guidance

## License

Licensed under the Apache License, Version 2.0. See [LICENCE.md](LICENCE.md) for details.

## Contributing

Contributions welcome! Please:
1. Review [docs/security.md](docs/security.md) for security requirements
2. Ensure all scripts pass basic smoke tests
3. Update documentation for any new features
4. Follow existing code style (Python PEP 8)

## Project Status

**Production Ready** - Fully functional for OpenClaw deployments.

Future enhancements:
- HTML trace viewer for log visualization
- Direct LLM API integration (currently requires OpenClaw)
- Additional output formats

## Credits

Developed as part of the OpenClaw ecosystem for safe, scalable agent operations.
