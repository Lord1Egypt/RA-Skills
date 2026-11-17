# Screenshot Organizer

## The Problem

Screenshots are the junk drawer of digital life. We take them constantly — to save a recipe, capture an error message, remember a parking spot, save a funny text — and they accumulate in a single folder with meaningless filenames. The result:

- **The average smartphone user has 200-500+ screenshots** taking up 1-5 GB of storage
- **Finding a specific screenshot is nearly impossible** — you scroll through hundreds of unnamed files
- **30-40% are duplicates** (same screenshot saved twice, or re-taken after a failed capture)
- **Zero searchability** — you can't search "find the screenshot with my flight confirmation" because the text is trapped in image pixels
- **No organization** — memes, receipts, and work documents all jumbled together

## Who Needs This

- **Everyone with a smartphone** — screenshots accumulate for all 6.8 billion smartphone users
- **Knowledge workers** who screenshot error messages, code snippets, and meeting notes
- **Online shoppers** who screenshot receipts, tracking numbers, and product pages
- **Students** who screenshot lecture slides, study materials, and assignments
- **People with limited storage** who need to reclaim space from duplicate screenshots

## How It Works

### Deduplication Scanner (`scripts/dedup_scanner.py`)
```bash
# Scan for duplicates
python scripts/dedup_scanner.py scan --dir ~/Pictures/Screenshots

# Show duplicate report
python scripts/dedup_scanner.py report --dir ~/Pictures/Screenshots

# Generate deletion plan (dry run)
python scripts/dedup_scanner.py plan --dir ~/Pictures/Screenshots --dry-run
```

### OCR Text Extractor (`scripts/ocr_extractor.py`)
```bash
# Extract text from all screenshots
python scripts/ocr_extractor.py extract --dir ~/Pictures/Screenshots

# Search for a specific screenshot
python scripts/ocr_extractor.py search --index index.json "flight confirmation"

# Detect URLs, emails, phone numbers
python scripts/ocr_extractor.py entities --index index.json
```

### Full Organizer (`scripts/screenshot_organizer.py`)
```bash
# Full organization run
python scripts/screenshot_organizer.py organize --dir ~/Pictures/Screenshots

# Generate report only (no changes)
python scripts/screenshot_organizer.py report --dir ~/Pictures/Screenshots
```

### Sample Output

```
$ python scripts/screenshot_organizer.py report --dir ~/Screenshots

📊 SCREENSHOT ORGANIZATION REPORT
═══════════════════════════════════════

📁 Total screenshots: 247
💾 Total size: 1.2 GB

DEDUPLICATION:
  Exact duplicates: 12 (saving ~45 MB)
  Near-duplicates: 8 pairs flagged for review
  Reclaimable: ~85 MB

CONTENT CATEGORIES:
  💬 Chat/Social:      68 (28%)
  🧾 Receipt/Payment:  45 (18%)
  🐛 Error/Bug:        28 (11%)
  📄 Document:         22 (9%)
  🎭 Meme:             19 (8%)
  💻 Code:             15 (6%)
  🗺️ Map:              12 (5%)
  ❓ Other:             38 (15%)

PROPOSED FOLDER STRUCTURE:
  Screenshots/
  ├── Chats/          (68 files)
  ├── Receipts/       (45 files)
  ├── Errors/         (28 files)
  ├── Documents/      (22 files)
  ├── Memes/          (19 files)
  ├── Code/           (15 files)
  ├── Maps/           (12 files)
  └── Unsorted/       (38 files)

SEARCH INDEX: 235 unique images, 4,892 words extracted
```

## Real-World Example

Lisa needs to find a screenshot of a bank transfer confirmation from 3 months ago. She has 400+ screenshots. Instead of scrolling for 30 minutes, she runs:

```bash
$ python scripts/ocr_extractor.py search --index index.json "bank transfer"
```

The tool searches the OCR index and returns:
```
🎯 FOUND 3 MATCHES:

1. Screenshot_20260512_143022.png (95% match)
   "Bank of America | Transfer Confirmation | Amount: $2,500..."
   Date: May 12, 2026
   📁 Location: ~/Screenshots/

2. Screenshot_20260515_091200.png (78% match)
   "Your transfer of $2,500 was completed..."
   Date: May 15, 2026

3. Screenshot_20260601_103045.png (65% match)
   "Monthly bank statement..."
   Date: Jun 1, 2026
```

Found in 2 seconds instead of 30 minutes.

## License

MIT — see [LICENSE](LICENSE)
