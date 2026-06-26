# Automation Patterns

## Weekly Cleanup Cron

Add to crontab for automatic screenshot organization:

```bash
# Weekly: Move old screenshots to archive (Sundays at 9am)
0 9 * * 0 cd ~/Documents/Skreenshot && python scripts/archive_old_screenshots.py --days 30
```

## Hazel Rules (macOS)

Hazel can auto-sort screenshots based on rules:

**Rule 1: Move to dated folders**
- If name matches `Screenshot .*`
- Created date is not in last 7 days
- → Move to `~/Pictures/Screenshots/YYYY/MM/`

**Rule 2: Tag receipts**
- If name contains `receipt` OR OCR contains "invoice", "total", "$"
- → Add tag: receipts
- → Move to `~/Pictures/Screenshots/receipts/`

**Rule 3: Delete old screenshots**
- If created date > 1 year ago
- AND not in any tagged folder
- → Move to Trash

## Keyboard Maestro Macros

**Macro: Quick Screenshot Sort**
1. Trigger: Hot key (Cmd+Opt+S)
2. Action: Run script `rename_screenshots.py --tags quick`
3. Action: Move to `~/Pictures/Screenshots/quick/`

**Macro: Search Last Screenshot**
1. Trigger: Hot key (Cmd+Opt+F)
2. Action: Get last screenshot from Desktop
3. Action: OCR and display in alert
4. Action: Copy OCR text to clipboard

## Shell Aliases

Add to `~/.zshrc`:

```bash
# Quick screenshot search
alias ss-search='textsnip -i ~/Desktop/Screenshot*.png | grep -i'

# List recent screenshots
alias ss-recent='find ~/Desktop -name "Screenshot*.png" -mtime -7 | head -20'

# Organize Desktop screenshots
alias ss-organize='cd ~/Documents/Skreenshot && python scripts/archive_old_screenshots.py'
```

## Shortcuts App (iOS/macOS)

**Shortcut: Screenshot Tagger**
1. Input: Selected screenshot(s)
2. Action: Run Python script with tag parameter
3. Output: Moved to categorized folder

**Shortcut: Find Screenshot**
1. Input: Search term (text)
2. Action: OCR search across Pictures/Screenshots
3. Action: Return matching files
4. Output: Quick Look preview
