# CLAUDE.md

This file provides context for AI coding agents working with this repository.

## Repository Purpose

Space Query Skill - Multi-platform query builder for network asset discovery (空间测绘) platforms.

## Supported Platforms

- **FOFA** (fofa.info) - Global coverage, protocol details
- **Quake** (quake.360.net) - China-focused, threat intelligence
- **ZoomEye** (zoomeye.org) - Detailed service fingerprints
- **Shodan** (shodan.io) - International IoT, vulnerability correlation

## Key Features

- CVE/vulnerability search with correct methodology
- Platform-specific query syntax
- Progressive disclosure (SKILL.md → resources/)
- Multi-platform query translation

## Important Conventions

1. **CVE Queries**: Always extract platform-specific product IDs, never search CVE ID directly in body/content
2. **Operator Precedence**: `() > == > = > != > && > ||`
3. **Progressive Disclosure**: Keep SKILL.md under 500 lines, detailed fields in resources/

## File Structure

```
SKILL.md           # Main skill file (loaded on trigger)
resources/         # Detailed field references
  fields.md       # Platform-specific field mappings
scripts/          # Helper scripts (future)
```

## Working with CVEs

When given a CVE:
1. WebSearch for official platform queries first
2. Check platform blogs, security sites, GitHub PoCs
3. Extract platform-specific product IDs
4. Build queries using official product identifiers

See `SKILL.md` for detailed workflow.
