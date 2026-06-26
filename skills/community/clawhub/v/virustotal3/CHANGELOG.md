# Changelog

## 1.0.1 (2026-05-25)

### Fixed
- Addressed ClawHub security audit findings (privacy disclosure, trigger scope)
- Added privacy warning about data sharing with VirusTotal security partners
- Removed overly generic "is this safe" trigger to prevent accidental activation

### Added
- Mandatory user confirmation before any submission to VirusTotal
- Hash-first workflow recommendation (prefer hash lookups over file uploads)
- Privacy & Data Sharing section with submission guidelines

## 1.0.0 (2026-05-24)

### Added
- Initial release: file, URL, domain, and IP scanning via VirusTotal Public API v3
- Secure credential management and rate limit handling
