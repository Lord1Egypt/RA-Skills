# text-scan

## Description

Search for relevant information in text files without reading the entire file. Returns matching lines with context, scored by relevance. Useful for quickly finding specific information in large files.

## When to Use

- You need to find a specific piece of information in a file but don't know the exact location
- You want to scan multiple files for relevant content before deciding which to read fully
- Marek wants you to extract specific lines from large files
- You're doing research and need to quickly scan through notes, logs, or documents
- The file is very large and reading it entirely would waste tokens/time

## How It Works

The script uses token-based matching with scoring:
- Exact token matches score 2 points
- Substring/partial matches score 1 point  
- Phrase matches (adjacent query terms found together in the line) score 3 points
- Results are sorted by score and limited

## Usage

```bash
# Basic search
python3 <skill_dir>/scripts/text-scan.py <file> --query "<search terms>"

# Brief format (line number + content)
python3 <skill_dir>/scripts/text-scan.py <file> --query "<search terms>" --brief

# JSON output (for programmatic use)
python3 <skill_dir>/scripts/text-scan.py <file> --query "<search terms>" --json

# Custom context window
python3 <skill_dir>/scripts/text-scan.py <file> --query "<search terms>" --before 3 --lines 5

# From stdin
cat <file> | python3 <skill_dir>/scripts/text-scan.py --query "<search terms>"
```

## Examples

```bash
# Find the runway in STATE.md
python3 <skill_dir>/scripts/text-scan.py /home/marek/.openclaw/workspace/STATE.md --query "runway"

# Find today's work hours
python3 <skill_dir>/scripts/text-scan.py /home/marek/.openclaw/workspace/STATE.md --query "today work hours"

# Find all log entries about a topic
python3 <skill_dir>/scripts/text-scan.py /home/marek/.openclaw/workspace/LOG.md --query "weather"
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--query, -q` | Search query (keywords) | required |
| `--lines, -a` | Lines after each match | 5 |
| `--before, -b` | Lines before each match | 2 |
| `--max-results, -n` | Maximum results to return | 5 |
| `--json` | JSON output format | false |
| `--brief` | Brief format only | false |
| `--fuzzy` | Enable fuzzy matching | false |
| `--output, -o` | Write results to file | stdout |

## Integration with OpenClaw

This skill integrates with the standard `read` tool workflow:
1. Use `text-scan` to quickly find relevant lines in a file
2. If the result is significant, use `read` to load the full file context
3. This reduces token usage by avoiding reading unnecessary content

## Tips

- Use shorter queries for broader matches, longer phrases for precision
- The `--brief` flag is fastest for quick scans
- `--json` output is useful for scripting/automation
- Combine with `find` to scan multiple files: `find . -name "*.md" | xargs ...`
- Score 3+ matches are usually high-confidence — worth reading in full
