# Usage

## Basic
```bash
python3 /Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/scrapling_fetch.py <url> 30000
```

## JSON output
```bash
python3 /Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/scrapling_fetch.py <url> 30000 --json
```

## Wrapper
```bash
/Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/fetch-web-content <url> 30000
```

## Batch mode
```bash
python3 /Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/scrapling_fetch.py --batch urls.txt 20000 --json
```

## Site selector overrides
```bash
python3 /Users/zzd/.openclaw/workspace/skills/scrapling-web-fetch/scripts/scrapling_fetch.py <url> 30000 --selectors /path/to/site-overrides.json
```
