---
name: library-book-monitor
description: Monitor library book availability and get notified when books become available for borrowing. Supports Shenzhen Library and extensible for other libraries.
version: 1.0.0
author: openclaw-community
license: MIT
tools:
  - bash
  - read
  - write
  - web_search
  - web_fetch
triggers:
  - library
  - book monitor
  - 图书馆
  - book availability
  - 借书
  - 书籍监控
permissions:
  - network
  - filesystem
  - shell
entryPoint:
  type: natural
  prompt: |
    You are a Library Book Monitor skill. You help users track book availability 
    at libraries and get notified when books become available for borrowing.
    
    Capabilities:
    - Add books to monitoring list
    - Check book availability at Shenzhen Library
    - List all monitored books
    - Remove books from list
    - Toggle monitoring status
    - Start scheduled monitoring
    
    When a user asks to:
    - Add a book: Use bash to run "python main.py add --title <title> [--author <author>] [--monitor]"
    - List books: Use bash to run "python main.py list"
    - Check books: Use bash to run "python main.py check"
    - Remove a book: Use bash to run "python main.py remove <book_id>"
    - Toggle monitoring: Use bash to run "python main.py toggle <book_id>"
    - Start monitoring: Use bash to run "python main.py monitor"
---

# Library Book Monitor Skill

A skill to monitor library book availability and get notified when books become available for borrowing.

## When to Use

Use this skill when you want to:
- Track book availability at Shenzhen Library
- Get notified when a book becomes available for borrowing
- Monitor multiple books and their availability status
- Automate library book availability checking

## Setup

Before using this skill, ensure:
1. Python 3.8+ is installed
2. Dependencies are installed: `pip install -r requirements.txt`
3. Configuration file `config.yaml` is set up (copy from `config.yaml.example`)

## Commands

### Add a Book
```
Add book "Python Programming" by "Guido van Rossum" with monitoring enabled
```

### List All Books
```
List all monitored books
```

### Check Book Availability
```
Check availability of all books
```

### Remove a Book
```
Remove book with ID abc123
```

### Toggle Monitoring
```
Toggle monitoring for book abc123
```

### Start Scheduled Monitoring
```
Start monitoring scheduler
```

## Configuration

The skill uses `config.yaml` for settings:

```yaml
library:
  name: "Shenzhen Library"
  base_url: "https://www.szlib.org.cn/"
  search_url: "https://www.szlib.org.cn/opac/"
  timeout: 30

scheduler:
  enabled: true
  interval_minutes: 30
  retry_on_failure: true
  max_retries: 3

notification:
  enabled: true
  methods:
    - console
    - email
  email:
    smtp_server: smtp.qq.com
    smtp_port: 587
    sender: your_email@qq.com
    password: your_smtp_password
    recipients:
      - recipient@example.com
```

## Notes

- The skill supports Shenzhen Library by default
- Other libraries can be added by implementing custom scrapers
- Book data is stored in `book_list.json`
- Please set reasonable check intervals to avoid overloading library servers
