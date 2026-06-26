# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.3] - 2026-04-13

### Changed
- Added think=False parameter to ensure analysis content is in content field
- Disabled thinking field output for cleaner responses and simpler code
- Source field now primarily 'content_direct' (thinking field as fallback)

### Fixed
- Resolved inconsistency between ollama library and direct HTTP API behavior
- Ensured reliable content extraction regardless of API default settings

## [1.1.2] - 2026-04-13

### Fixed
- Improved source field accuracy to reflect actual content origin
- source now shows 'content_direct', 'thinking_cleaned', or 'no_content'
- Fixed logic where empty content string incorrectly showed 'content' source

## [1.1.1] - 2026-04-13

### Fixed
- Added missing 'source' field to all response cases
- Unified error response structure with consistent fields
- Fixed KeyError in main.py when accessing result['source']
- All error cases now include 'success': false and 'source' field

## [1.1.0] - 2026-04-13

### Changed
- Uses /api/chat endpoint for direct content extraction
- Simplified architecture without complex thinking field processing
- Default English prompt "Describe this image"
- Removed regex dependencies for cleaner code
- Updated documentation with new technical approach

### Performance
- Direct content field access improves reliability
- Reduced edge cases in output processing
- Maintains ~30 second response time (hardware dependent)

## [1.0.0] - 2026-04-12

### Added
- Initial release of Vision Tool skill
- Image recognition using Ollama + qwen3.5:4b
- Automatic cleaning of thinking field output
- Multi-channel support (WeChat, Telegram, Discord, etc.)
- JSON and text output formats
- Comprehensive error handling
- Development environment setup documentation

### Features
- ✅ Smart cleaning of qwen3.5:4b thinking field
- ✅ Easy to use: `vision image.jpg` command
- ✅ High-quality, detailed analysis results
- ✅ Full error recovery and reporting
- ✅ Works with all OpenClaw channels

### Technical Details
- Built with Python 3.8+
- Uses requests library for HTTP calls
- Structured as OpenClaw skill with proper metadata
- Includes tests and development tools
- MIT licensed
