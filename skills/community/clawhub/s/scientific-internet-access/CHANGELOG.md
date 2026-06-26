# Changelog

## [1.8.4] - 2026-05-03
### Fixed
- tester.py: use ipaddress module for complete private IP detection (covers 172.16.0.0/12 and all RFC1918)
- Removed incomplete string-prefix approach; full ipaddress.is_private/is_loopback/etc.


## [1.8.3] - 2026-05-03
### Fixed
- tester.py: DNS resolve hostnames before testing; reject resolved private/reserved IPs
- Narrowed ALLOWED_PORTS to proxy-only ports (removed SSH/MySQL/VNC)
- ClawHub hostname resolution finding resolved


## [1.8.2] - 2026-05-03
### Fixed
- tester.py: address filtering (private/loopback/link-local/reserved blocked), port allowlist, confirmation prompt
- ClawHub scan: resolve "Tool Misuse" finding re arbitrary TCP connections


## [1.8.0] - 2026-05-03
### Added
- I-Lang v3.0 ::DNA{} behavioral DNA integration
- ::GENE{} strict behavior constraints for all output
- Protocol: I-Lang embedded in SKILL.md

### Changed
- License MIT → MIT-0 (no attribution required)
- ClawHub moderation: clean pass
- Sharing flow: recommends clawhub install

### Fixed
- Removed hardcoded proxy links (tg://) for moderation compliance
- Unified Telegram proxy guidance across both skills

## [1.2.0] - 2026-02-27
### Added
- Initial release
- Scraper: 10+ GitHub node sources
- Tester: 20-thread parallel TCP speed testing
- Formatter: Clash/V2Ray/Surge/Shadowrocket/Base64 output
- OpenClaw SKILL.md with bilingual trigger words
- GitHub Actions auto-publish to ClawHub
