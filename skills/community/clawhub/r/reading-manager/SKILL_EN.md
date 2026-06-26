---
version: "1.0.0"
---

---
name: reading-manager
description: "Personal reading management system for tracking books, articles, reading progress, notes, and generating reading reports. Use when: (1) recording books and articles to read, (2) tracking reading progress by pages or percentage, (3) taking reading notes and highlights, (4) managing reading lists (want to read, reading, finished), (5) generating reading statistics and reports, (6) setting reading goals and reminders."
---

# Reading Manager

A personal reading management system for tracking books, monitoring reading progress, managing notes, and generating comprehensive reading reports.

## Description

Reading Manager helps you organize your reading life by tracking books and articles, recording reading progress, taking notes and highlights, and generating insightful statistics about your reading habits. Whether you're building a personal library, working through a reading list, or simply want to understand your reading patterns better, this skill provides the tools you need.

## Installation

```bash
cd ~/.openclaw/workspace/skills/reading-manager
pip install -e .
```

## Usage

### Book Management

```bash
# Add a book by ISBN (auto-fetches metadata)
reading book add --isbn 9787115428028

# Add a book manually
reading book add --title "Computer Systems: A Programmer's Perspective" --author "Randal E. Bryant" --pages 800

# Add an article from URL
reading book add --url https://example.com/article --type article

# List all books
reading book list

# Show book details
reading book show 1

# Update book information
reading book update 1 --status reading --rating 5

# Delete a book
reading book delete 1
```

### Reading Progress

```bash
# Update reading progress by page
reading progress update 1 --page 150

# Update reading progress by percentage
reading progress update 1 --percent 25

# View current progress
reading progress show 1

# Log reading time
reading progress time 1 --minutes 45

# View reading history
reading progress history 1
```

### Reading Notes

```bash
# Add a note
reading note add 1 --content "This is an important concept" --page 120 --tags "important,concept"

# Add a highlight
reading note highlight 1 --content "Key paragraph text" --page 120 --color yellow

# List all notes for a book
reading note list 1

# Search notes by tag
reading note search --tag important

# Export notes to Markdown
reading note export 1 --output notes.md
```

### Reading Lists

```bash
# View want-to-read list
reading list want

# View currently-reading list
reading list reading

# View finished books list
reading list finished

# Move book between lists
reading list move 1 --to finished

# Create a custom reading list
reading list create "Tech Books" --description "Programming and technology related books"
reading list add-book "Tech Books" 1
```

### Reading Reports

```bash
# Generate monthly report
reading report monthly 2024-01

# Generate yearly report
reading report yearly 2024

# View reading statistics
reading report stats

# View reading trends
reading report trend --days 30
```

### Reading Goals

```bash
# Set yearly reading goal
reading goal set-yearly 50

# Set monthly reading goal
reading goal set-monthly 4

# Check goal progress
reading goal status

# View historical goal completion
reading goal history
```

### Search & Discovery

```bash
# Search books online
reading search "computer systems" --source google
reading search "计算机系统" --source douban

# Search local library
reading search-local "computer"

# Search by author
reading search --author "Yu Hua"
```

## Features

### Book/Article Management
- Add books via ISBN, URL, or manual entry
- Automatic metadata retrieval (Google Books API / Douban API)
- Article link collection and management
- Support for multiple types: books, articles, papers, documents

### Reading Progress Tracking
- Page-based progress recording
- Percentage calculation
- Reading time statistics
- Reading speed analysis

### Reading Notes
- Highlight recording with color coding
- Annotation management
- Tag-based organization
- Markdown export support

### Reading Lists
- Want to Read
- Currently Reading
- Finished
- Custom reading lists

### Reading Reports
- Monthly/yearly reading statistics
- Reading trend analysis
- Book type distribution
- Reading duration reports

### Reading Goals
- Annual reading goal setting
- Daily/weekly reading reminders
- Goal completion progress tracking

## Configuration

Database location: `~/.config/reading-manager/reading.db`

```bash
# View database path
reading data path

# Export data
reading data export --format json --output backup.json

# Import data
reading data import backup.json
```

## Examples

### Scenario 1: Starting a New Book

```bash
# Add book by ISBN
reading book add --isbn 9780134685991

# Update status to "reading"
reading book update 1 --status reading

# Log progress as you read
reading progress update 1 --page 50
reading progress time 1 --minutes 30

# Add notes along the way
reading note add 1 --content "Chapter 2 explains memory hierarchy" --page 50 --tags "memory,architecture"
```

### Scenario 2: Completing a Book

```bash
# Mark as finished
reading book update 1 --status finished --rating 5

# View your notes
reading note list 1

# Export notes for future reference
reading note export 1 --output "computer-systems-notes.md"
```

### Scenario 3: Monthly Review

```bash
# Check what you've read
reading report monthly 2024-03

# View statistics
reading report stats

# Check goal progress
reading goal status
```

### Scenario 4: Building a Reading List

```bash
# Create a themed list
reading list create "AI Learning Path" --description "Books for learning AI/ML"

# Add books to the list
reading list add-book "AI Learning Path" 1
reading list add-book "AI Learning Path" 2

# View the list
reading list show "AI Learning Path"
```

## Technical Details

### Technology Stack
- **Python 3.8+**
- **SQLite** - Local database storage
- **Click** - CLI framework
- **Rich** - Terminal formatting
- **requests** - API calls

### Data Models

#### Books Table
```python
{
    id: int
    title: str              # Book title
    subtitle: str           # Subtitle
    authors: str            # Authors (JSON array)
    isbn10: str
    isbn13: str
    publisher: str          # Publisher
    published_date: str     # Publication date
    page_count: int         # Total pages
    description: str        # Description/summary
    cover_url: str          # Cover image URL
    categories: str         # Categories (JSON array)
    source_type: str        # Source: book, article, paper
    source_url: str         # Source URL
    status: str             # Status: want, reading, finished
    rating: int             # Rating 1-5
    started_at: str         # Start reading date
    finished_at: str        # Completion date
    created_at: str
    updated_at: str
}
```

#### Reading Progress Table
```python
{
    id: int
    book_id: int
    current_page: int       # Current page
    total_pages: int        # Total pages
    percent: float          # Percentage
    minutes_read: int       # Reading duration (minutes)
    recorded_at: str
    notes: str
}
```

#### Notes Table
```python
{
    id: int
    book_id: int
    content: str            # Note content
    page: int               # Page number
    note_type: str          # Type: note, highlight
    highlight_color: str    # Highlight color
    tags: str               # Tags (JSON array)
    created_at: str
}
```

#### Lists Table
```python
{
    id: int
    name: str               # List name
    description: str        # Description
    book_ids: str           # Book IDs (JSON array)
    created_at: str
}
```

#### Goals Table
```python
{
    id: int
    year: int               # Year
    month: int              # Month (null for yearly goals)
    target_count: int       # Target number
    completed_count: int    # Completed count
    created_at: str
}
```

## API Integration

The skill supports multiple book metadata APIs:

- **Google Books API** - Default for ISBN lookup
- **Douban API** - Chinese book database

Configure your preferred source using the `--source` flag in search commands.

## License

Part of the OpenClaw skills ecosystem.