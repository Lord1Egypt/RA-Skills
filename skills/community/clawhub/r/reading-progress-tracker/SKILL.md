---
name: reading-progress-tracker
description: Organize reading into Now, Next, Later, and Drop, then track current position, format, purpose, next stopping point, and lightweight session notes. Use when the user wants a simple manual reading dashboard that supports print, ebook, and audiobook without turning reading into homework.
---

# Reading Progress Tracker

## Overview

Use this skill to keep reading visible, lightweight, and honest. It helps the user track where they are, why they are reading a book, what the next stopping point is, and whether a book should stay active, move later, or be dropped.

This skill is descriptive only. It does not sync Goodreads, Kindle, audiobooks, or external reading apps.

## Trigger

Use this skill when the user wants to:
- organize books into Now, Next, Later, and Drop
- remember where they stopped reading
- keep short session notes that actually get revisited
- give each active book a purpose
- make peace with pausing or dropping books

### Example prompts
- "Build me a reading dashboard"
- "Track my current books and where I left off"
- "Help me stop hoarding books without reading them"
- "Turn these notes into a simple reading log"

## Workflow

1. Sort books into Now, Next, Later, and Drop.
2. Clarify why each current book matters.
3. Track format, progress, pace, and next stopping point.
4. Capture one idea, one quote or example, and one question after each session.
5. Review whether a book should continue, be skimmed, or be abandoned.
6. Keep the system light enough to support real reading momentum.

## Inputs

The user can provide any mix of:
- current books
- queue books
- purpose for reading
- print, ebook, or audiobook format
- pages, chapters, or percentage progress
- quotes, ideas, and questions
- books they want to pause or drop

## Outputs

Return a markdown dashboard with:
- current reads and their status
- one lightweight session note
- queue sections for Next, Later, and Drop or pause

## Safety

- Keep tracking light enough that it does not become homework.
- Allow non-linear reading for reference books.
- Support print, ebook, and audiobook without forcing one metric.
- Make it acceptable to pause or drop a book when the fit is wrong.

## Acceptance Criteria

- Return markdown text.
- Give every active book a purpose and progress status.
- Include a session note with one idea, one quote or example, and one question.
- Include a queue that makes continuing, pausing, or dropping feel usable.
