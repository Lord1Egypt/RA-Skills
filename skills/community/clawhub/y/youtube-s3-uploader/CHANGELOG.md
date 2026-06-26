# Changelog

## v3.0.3 (2026-03-27)

### Fixed
- **Filename restriction**: Added `--restrict-filenames` parameter to all yt-dlp commands
- **Twitter/X compatibility**: Prevents download failures due to excessively long filenames
- **System error prevention**: Avoids `[Errno 36] File name too long` errors on certain platforms

### Affected Files
- `scripts/video-to-s3-universal.js`: Lines 318, 322
- `scripts/youtube-to-s3.js`: Lines 263, 267

### Technical Details
- Added `--restrict-filenames` flag to all yt-dlp download commands
- Ensures compatibility with platforms that generate long filenames (Twitter/X, YouTube with Chinese titles)
- Maintains existing filename cleaning logic (removes whitespace, special characters)
- Backward compatible: ✅ No breaking changes

## v3.0.2 (2026-03-26)

### Fixed
- **Filename whitespace**: Changed from merging multiple spaces to removing all whitespace characters
- **Consistency**: Ensures no spaces in generated filenames
- **Affected files**: `video-to-s3-universal.js`, `youtube-to-s3.js`

## v3.0.1 (2026-03-26)

### Fixed
- **Filename cleaning**: Removes all punctuation marks, emojis, and special characters from filenames
- **Chinese punctuation**: Proper handling of Chinese punctuation marks (【】·、，。！？《》：；等)
- **Emoji removal**: Removes all emojis and special Unicode characters
- **S3 compatibility**: Ensures clean filenames for better S3 compatibility

### Technical Details
- Enhanced regex patterns for comprehensive character removal
- Extended Unicode range for emoji detection (U+1F300 to U+1F9FF)
- Maintains Chinese characters, letters, numbers, and spaces
- Preserves readability while removing clutter

## v3.0.0 (2026-03-25)

### Added
- **Universal video downloader**: Supports YouTube, Twitter/X, TikTok, Douyin, Bilibili, and 1000+ websites via yt-dlp
- **Platform detection**: Automatically detects video platform
- **New command**: `video-to-s3-universal.js` for universal video downloading
- **Backward compatibility**: `youtube-to-s3.js` still works for YouTube-specific use

### Changed
- **Complete rewrite**: From YouTube-specific to universal video downloader
- **Improved architecture**: Better separation of concerns
- **Enhanced error handling**: More robust error recovery

## v2.0.0 (2026-03-25)

### Added
- **S3 Multipart Upload**: Uses multipart upload for all file sizes
- **Memory optimization**: Chunked reading to avoid memory overflow
- **Error recovery**: Automatic retry mechanism
- **Smart chunk sizing**: Adjusts based on file size

### Fixed
- **Help system**: Proper `--help` display
- **Consistent API**: Always uses multipart upload
- **Cleaner codebase**: Removed compatibility layers

## v1.0.0 (2026-03-25)

### Initial Release
- Basic YouTube video download and S3 upload
- Simple PUT upload for small files
- Foundation for future improvements

