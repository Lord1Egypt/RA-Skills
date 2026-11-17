---
name: requirement-guide
version: 1.0.0
description: A conversational requirement clarification tool with structured questioning and document generation.
author: Terr123123
license: MIT
tags:
  - requirements
  - clarification
  - dialogue
  - document-generation
permissions:
  - read_session_files
  - write_session_files
  - generate_requirement_documents
security_notes:
  - Does not access the network
  - Session files are user-controlled
  - No external dependencies beyond the standard library
frameworks:
  - openclaw
---

# Requirement Guide

A conversational requirement clarification tool that guides users through
structured questioning across six dimensions and assembles a structured
requirement document from the gathered answers.

## Features

- **Structured Questioning** — Six preset dimensions drive a guided dialogue
- **Session Management** — Track active, completed, and abandoned sessions
- **Required vs Optional** — Distinguish mandatory elements from nice-to-haves
- **Document Generation** — Assemble a requirement document with completeness scoring
- **Persistence** — Save/load sessions and documents as JSON for resumable workflows
- **Thread-Safe** — Concurrent calls do not corrupt session state
- **Zero Dependencies** — Pure standard library (only `pytest` for tests)

## Question Dimensions

| Dimension | Elements |
|-----------|----------|
| `basic_info` | project_name, version, author |
| `background` | problem, goal, context |
| `functional` | features, user_roles, workflows |
| `non_functional` | performance, security, usability |
| `data` | entities, interfaces, storage |
| `acceptance` | criteria, timeline, constraints |

## Installation

```bash
openclaw skills install requirement-guide
```

## Quick Start

```python
from src import RequirementGuide

guide = RequirementGuide()

# Start a guided session
session = guide.start_session("Inventory Management System")

# Ask questions and process answers
question = guide.ask_question(session.id)
print(question.text)            # "What is the project name?"
answer = guide.process_answer(session.id, "StockFlow")
print(answer.processed)         # True

# Continue the dialogue...
while True:
    q = guide.ask_question(session.id)
    if q is None:
        break
    guide.process_answer(session.id, "..." if q.required else "-")

# Generate the requirement document
doc = guide.generate_document(session.id)
print(doc.title)                # "Inventory Management System"
print(doc.completeness)         # 1.0
```

## API

### RequirementGuide

| Method | Description |
|--------|-------------|
| `start_session(topic: str) -> Session` | Start a new requirement gathering session |
| `ask_question(session_id: str) -> Question \| None` | Return the next unanswered question |
| `process_answer(session_id: str, answer: str) -> Answer` | Process a user answer for the active question |
| `generate_document(session_id: str) -> RequirementDocument` | Assemble a requirement document from gathered answers |
| `get_session_status(session_id: str) -> SessionStatus` | Return the current session status |
| `completeness(session_id: str) -> float` | Return the completeness ratio (0.0 - 1.0) |
| `abandon_session(session_id: str) -> Session` | Mark a session as abandoned |
| `save_session(session_id: str, path: str) -> str` | Persist a session to JSON |
| `load_session(path: str) -> Session` | Load a session from JSON |
| `save_document(session_id: str, path: str) -> str` | Persist the requirement document to JSON |

### Data Models

- **Session** — `id`, `topic`, `status`, `questions_asked`, `answers`, `elements`
- **Question** — `id`, `dimension`, `text`, `required`
- **Answer** — `question_id`, `content`, `processed`
- **RequirementDocument** — `title`, `elements`, `completeness`
- **SessionStatus** — `ACTIVE`, `COMPLETED`, `ABANDONED`

## Testing

```bash
cd d:\openclaw-skills\business-stack\requirement-guide
python -m pytest tests/ -v --tb=short
```

## License

MIT License — Free for personal and commercial use.

## Author

Terr123123
