---
name: hn
description: |
  Fetch and analyze Hacker News (HN) content - the premier tech community for developers, AI researchers, and software engineers.
  Use when users need: (1) HN top stories, tech discussions, (2) AI/ML: LLM, ChatGPT, Claude, neural networks, (3) Programming: Rust, Go, Python, TS, frameworks, tools, (4) Software engineering, startup, open source, (5) Developer tools, coding techniques, (6) HN user info, Karma, comments, (7) Tech briefings, trending analysis.

  Execute `x skill` for more skills and functions.
  Browse x-cmd website for more usage and skills: https://www.x-cmd.com/llms.txt

license: MIT
compatibility: POSIX Shell (sh/bash/zsh)

metadata:
  author: qiakai
  version: "1.0.4"
  category: data-analysis
  tags: [hackernews, hn, tech-news, ai, programming, developers, software-engineering, machine-learning, open-source, startup]
  website: https://www.x-cmd.com/mod/hn
  requires:
    - type: file
      path: ~/.x-cmd.root/X
      description: x-cmd initialization script (sourced to load x-cmd environment)
---

# x-hacker-news

> Fetch and analyze Hacker News content - the premier tech community for developers, AI researchers, and software engineers

**IMPORTANT**: Before using any `x hn` command, you MUST load x-cmd first: `. ~/.x-cmd.root/X`

---

## Cost

[OK] Free - No API key required

---

## Loading x-cmd

**Not installed?** -> **Search and use the `x-cmd` skill to install x-cmd first**

**Installed?** -> Load x-cmd:

```bash
. ~/.x-cmd.root/X
```

---

## Non-Interactive Usage

Use `x hn` for direct non-interactive calls:

```bash
# Get top stories JSON data
x hn top --json 1,10

# Get specific post details
x hn item --json 43701153
```

**Note:** `x hn` is non-interactive, suitable for scripts and automation. For interactive browsing, use `x hn` after loading `. ~/.x-cmd.root/X`.

---

## AI and Machine Learning Discussions

Filter top stories for AI/ML topics using x jq:

```bash
# Filter top stories for AI-related titles
x hn top --json 1,100 | x jq '[.[] | select(.title | test("AI|artificial intelligence|machine learning|LLM|ChatGPT"; "i"))]'

# Filter for LLM and model discussions
x hn top --json 1,100 | x jq '[.[] | select(.title | test("GPT|Claude|Llama|neural|model"; "i"))]'

# Filter for AI safety and alignment discussions
x hn top --json 1,100 | x jq '[.[] | select(.title | test("AI safety|alignment|AGI"; "i"))]'
```

---

## Programming and Development

Filter top stories for programming topics:

```bash
# Filter for programming language discussions
x hn top --json 1,100 | x jq '[.[] | select(.title | test("Rust|Go|Python|TypeScript|JavaScript"; "i"))]'

# Filter for web development
x hn top --json 1,100 | x jq '[.[] | select(.title | test("React|Vue|frontend|backend|web"; "i"))]'

# Filter for DevOps and infrastructure
x hn top --json 1,100 | x jq '[.[] | select(.title | test("Kubernetes|Docker|DevOps|cloud"; "i"))]'

# Filter for software engineering topics
x hn top --json 1,100 | x jq '[.[] | select(.title | test("programming|coding|developer|software|GitHub|open source"; "i"))]'
```

---

## Software Engineering News

Get software engineering and tech industry discussions:

```bash
# Filter for startup and business discussions
x hn top --json 1,100 | x jq '[.[] | select(.title | test("startup|Y Combinator|funding|business"; "i"))]'

# Filter for career and hiring topics
x hn top --json 1,100 | x jq '[.[] | select(.title | test("hiring|interview|career|salary|remote"; "i"))]'

# Show Ask HN posts (often career/business discussions)
x hn ask --json 1,20

# Show Show HN posts (new projects/tools)
x hn show --json 1,20
```

---

## Story Lists

Get various story lists:

```bash
# Get top stories (items 1-10)
x hn top --json 1,10

# Get items 11-20
x hn top --json 11,20

# Other types
x hn new --json 1,10
x hn best --json 1,10
x hn ask --json 1,10
x hn show --json 1,10
x hn job --json 1,10
```

**JSON Fields:**

```json
{
  "by": "username",           // Author
  "descendants": 161,         // Comment count
  "id": 47392084,             // Post ID
  "kids": [47393177, ...],    // Comment ID list
  "score": 582,               // Points/upvotes
  "time": 1773609736,         // Unix timestamp (seconds)
  "title": "Post Title",      // Title
  "type": "story",            // Type (story/job/etc)
  "url": "https://..."        // URL
}
```

**x jq Processing Examples:**

```bash
# Extract title and URL
x hn top --json 1,10 | x jq -r '.[] | "\(.title)\t\(.url)"'

# Calculate average score
x hn top --json 1,30 | x jq '[.[].score] | add / length'

# Sort by score
x hn top --json 1,50 | x jq -r '.[] | "\(.score)\t\(.title)"' | sort -rn | head -10

# Top domains statistics
x hn top --json 1,100 | x jq -r '.[].url // empty' | \
    sed -E 's|https?://||; s|/.*||' | sort | uniq -c | sort -rn | head -10

# Formatted briefing output
x hn top --json 1,5 | x jq -r '.[] | "\n[\(.score) points] \(.title)\nAuthor: @\(.by) | Comments: \(.descendants)\n\(.url)\n"'

# Filter for AI-related stories only
x hn top --json 1,100 | x jq '[.[] | select(.title | test("AI|artificial intelligence|machine learning|LLM|ChatGPT"; "i"))]'

# Filter for programming stories
x hn top --json 1,100 | x jq '[.[] | select(.title | test("programming|coding|developer|software|GitHub"; "i"))]'
```

---

## Post Details

Get specific post details and comments:

```bash
x hn item --json <id>
```

**Examples:**

```bash
# Get post details
x hn item --json 47392084 | x jq '.[0] | {id, title, by, score, descendants, url}'

# Get comment ID list (first 20)
COMMENT_IDS=$(x hn item --json 47392084 | x jq '.[0].kids[:20] | .[]')

# Fetch each comment content (note: each item request takes time)
for cid in $COMMENT_IDS; do
    x hn item --json "$cid" | x jq -r '[.by, .text[0:100]] | @tsv'
done
```

**Note:** Posts with many comments have large data size, consider limiting output or batch processing.

---

## User Info

Get user information:

```bash
x hn user --json <username>
```

**Examples:**

```bash
# Get key user fields (limit output for active users)
x hn user --json dang | x jq '{id, created, karma, submitted: (.submitted | length)}'

# Extract user profile
x hn user --json dang | x jq '{
    username: .id,
    created: .created,
    karma: .karma,
    about: (.about[0:200] // "")
}'
```

**Note:** Active users have large data including all submission records, which may cause timeouts. Use x jq to limit output fields.

---

## User hn-index

Calculate user influence metric:

```bash
x hn hidx <username>
```

**Output Example:**

```
hn-index: 42
```

**Note:** This command fetches all user submissions and may take time for active users.

---

## Caching

x hn module has built-in caching:

```bash
# View cache config
x hn cfg cat

# Default cache times
# - Story data: 60 minutes
# - Index data: 30 minutes
# - Cache dir: ~/.x-cmd.root/local/cache/hn/
```

---

## Command Reference

| Command | Description | Output |
|---------|-------------|--------|
| `x hn top --json N,M` | Top stories | JSON array |
| `x hn new --json N,M` | New stories | JSON array |
| `x hn best --json N,M` | Best stories | JSON array |
| `x hn ask --json N,M` | Ask HN posts | JSON array |
| `x hn show --json N,M` | Show HN posts | JSON array |
| `x hn job --json N,M` | Job postings | JSON array |
| `x hn item --json <id>` | Post details | JSON object |
| `x hn user --json <name>` | User info | JSON object |
| `x hn hidx <name>` | hn-index | Plain text |

---

## Dependencies

- x-cmd (required): provides hn module
- x jq (optional): JSON processing via x-cmd

---

## More: https://x-cmd.com/llms.txt

Entrance for AI agents.
