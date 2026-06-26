# visible-text-extractor 1.0.0

## Highlights
- First polished public release
- Extract visible text from URLs, screenshots, image directories, and GIFs
- Special handling for WeChat / 公众号 article URLs
- OCR cleanup and section reconstruction for noisy image text
- One-step pipeline that outputs raw JSON, clean JSON, clean markdown, and a Word document

## Positioning
This is a deliverable-oriented extraction skill: the goal is not merely to dump OCR, but to produce something a human can read and share.

## Notes
- Best results come from public, accessible content
- Browser fallback and OCR quality still depend on local runtime availability
- The skill degrades honestly when a page is blocked or partially inaccessible
