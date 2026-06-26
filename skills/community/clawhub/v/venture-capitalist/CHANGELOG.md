# Changelog

All notable changes to the ZhenCap MCP Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.1] - 2026-04-01

### Security Fixes

- **CRITICAL**: Fixed Authorization header bug - no longer sends "Bearer undefined" when API key is not set
- Enhanced privacy documentation transparency
- Clarified authentication model and free tier mechanism
- Addressed all ClawHub Security findings from v2.0.0 review

### Fixed

- Authorization header now only added when ZHENCAP_API_KEY environment variable is set
- Removed analyze_bp tool (backend endpoint not yet available)
- Fixed privacy documentation contradictions regarding data collection
- Corrected manifest.json authentication requirements (requiresAuth: false)

### Changed

- Updated manifest.json: requiresAuth changed from true to false (auth is optional)
- Enhanced SKILL.md with comprehensive Privacy & Security section
- Added detailed Authentication section explaining free vs paid tiers
- Added "How Free Tier Works" documentation
- Improved clarity around what data is collected and transmitted
- Updated description to remove mention of BP analysis (coming soon)

### Documentation

- Added CHANGELOG.md (this file)
- Expanded privacy policy information with links to www.zhencap.com/privacy
- Added comprehensive authentication guide for both free and paid tiers
- Clarified free tier quota tracking mechanism (IP-based rate limiting)
- Updated README.md to match SKILL.md changes
- Added SECURITY-FIX-REPORT-v2.0.1.md documenting security improvements

### Removed

- analyze_bp tool (will be re-added when backend endpoint is ready)
- analyzeBP method from index.js
- Contradictory privacy claims about BP text collection

---

## [2.0.0] - 2026-03-31

### Breaking Changes

- **COMPLETE REWRITE**: v1.0.0 was a document analysis tool, v2.0.0 is a cloud API client
- Removed all local document processing capabilities
- Removed slash commands (/vc analyze, /vc report, /vc deck)
- Changed from command-based interface to tool-based interface
- Now requires internet connection to ZhenCap API servers

### Added

- Cloud-powered investment analysis via ZhenCap API
- Market size estimation with TAM/SAM/SOM calculations
- Competitor analysis with SWOT mapping
- Valuation modeling using Comparable Companies method
- Multi-dimensional risk scoring (market, team, technology, financial)
- Free tier: 50 API calls per month without registration
- Optional API key authentication for paid unlimited usage
- MCP tool interface compatible with Claude Desktop, Cline, OpenClaw

### Changed

- Architecture: From local processing to API client
- Authentication: JWT-based authentication for paid tier
- Pricing model: Free tier (50/month) + paid tier (pay-per-call)
- Documentation: Complete rewrite for v2.0.0 API client model

### Migration

- See MIGRATION-v1-to-v2.md for detailed upgrade instructions
- Users who need local document processing should stay on v1.0.0
- Users who need market intelligence should upgrade to v2.0.0

---

## [1.0.0] - 2025-12-15

### Initial Release

- Document analysis for pitch decks and business plans
- Local processing only (no cloud dependencies)
- Commands: /vc analyze, /vc report, /vc deck
- PDF, PPTX, DOCX format support
- Markdown report generation
- No API key required (fully local)

---

## Security Policy

If you discover a security vulnerability, please email security@zhencap.com instead of using the issue tracker.

---

## Upgrade Guide

### From v2.0.0 to v2.0.1

This is a security patch release. No breaking changes.

**Required actions:**
- None - just update to v2.0.1

**What changed:**
- Authorization header fix (internal improvement)
- Documentation improvements
- analyze_bp tool removed (was not working)

**To upgrade:**
```bash
clawhub update venture-capitalist
```

### From v1.0.0 to v2.0.0

This is a major breaking change. See MIGRATION-v1-to-v2.md for full details.

**Key differences:**
- v1.0.0: Local document processing
- v2.0.0: Cloud API client

**Recommendation:**
- Stay on v1.0.0 if you need offline document analysis
- Upgrade to v2.0.0 if you need market intelligence and API integration
