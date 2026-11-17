# Changelog

All notable changes to WenYan will be documented in this file.

## [1.0.0] - 2026-09-01

### Added
- 8 classical Chinese writing styles (ruya, wuxia, sanguo, zhanguo, shiji, baihua, shijing, chan)
- Parameterized style engine with JSON configuration
- Vocabulary mapping system (modern -> classical)
- Forbidden word detection (50+ global taboo words)
- Sentence length validation per style
- Style drift detection (consecutive modern sentences)
- Quantified scoring system (0-100)
- Persistent state management (state.json)
- Semantic exit detection (not limited to keywords)
- Three intensity levels (1: 20%, 2: 60%, 3: 90%+)
- Regression test framework with 20 test cases
- Style comparison reference table
- Multi-language README (Chinese, English, Japanese)
- MIT-0 license with attribution notice

### Technical
- Python 3.x compatible
- No external dependencies
- Cross-platform (Windows/macOS/Linux)
