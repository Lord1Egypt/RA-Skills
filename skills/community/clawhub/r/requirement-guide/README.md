# Requirement Guide

A conversational requirement clarification tool that guides users through
structured questioning across six dimensions and assembles a structured
requirement document from the gathered answers.

Built as an [OpenClaw](https://openclaw.ai) Skill.

## Why

Capturing requirements is error-prone: people forget dimensions, skip
non-functional concerns, and leave acceptance criteria implicit.
Requirement Guide drives a predictable, question-by-question dialogue and
turns the answers into a completeness-scored document.

## Features

- **Structured Questioning** — Six preset dimensions drive a guided dialogue
- **Session Management** — Track active, completed, and abandoned sessions
- **Required vs Optional** — Distinguish mandatory elements from nice-to-haves
- **Document Generation** — Assemble a document with completeness scoring
- **Persistence** — Save/load sessions and documents as JSON
- **Thread-Safe** — Concurrent calls do not corrupt session state
- **Zero Runtime Dependencies** — Pure standard library

## Question Dimensions

| Dimension | Elements |
|-----------|----------|
| `basic_info` | project_name, version, author |
| `background` | problem, goal, context |
| `functional` | features, user_roles, workflows |
| `non_functional` | performance, security, usability |
| `data` | entities, interfaces, storage |
| `acceptance` | criteria, timeline, constraints |

## Quick Start

```python
from src import RequirementGuide

guide = RequirementGuide()
session = guide.start_session("Inventory Management System")

question = guide.ask_question(session.id)
print(question.text)                       # What is the project name?
guide.process_answer(session.id, "StockFlow")

# Continue until all questions are answered
while True:
    q = guide.ask_question(session.id)
    if q is None:
        break
    guide.process_answer(session.id, "..." if q.required else "-")

doc = guide.generate_document(session.id)
print(doc.title, doc.completeness)         # Inventory Management System 1.0
```

## API

### RequirementGuide

| Method | Description |
|--------|-------------|
| `start_session(topic) -> Session` | Start a new requirement gathering session |
| `ask_question(session_id) -> Question \| None` | Return the next unanswered question |
| `process_answer(session_id, answer) -> Answer` | Process a user answer for the active question |
| `generate_document(session_id) -> RequirementDocument` | Assemble a requirement document |
| `get_session_status(session_id) -> SessionStatus` | Return the current session status |
| `completeness(session_id) -> float` | Return the completeness ratio (0.0 - 1.0) |
| `abandon_session(session_id) -> Session` | Mark a session as abandoned |
| `save_session(session_id, path) -> str` | Persist a session to JSON |
| `load_session(path) -> Session` | Load a session from JSON |
| `save_document(session_id, path) -> str` | Persist the requirement document to JSON |

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

The test suite contains ~80 tests across four files:

| File | Focus | Count |
|------|-------|-------|
| `test_core.py` | Basic functionality | 25 |
| `test_unit_extended.py` | Boundary, exceptions, concurrency | ~30 |
| `test_integration.py` | Serialization & persistence | 15 |
| `test_e2e.py` | End-to-end flows | 10 |

## File Structure

```
src/
├── __init__.py
├── models.py      # Data models
├── core.py        # RequirementGuide main class
tests/
├── __init__.py
├── test_core.py
├── test_unit_extended.py
├── test_integration.py
├── test_e2e.py
SKILL.md
LICENSE
README.md
```

## License

MIT License — see [LICENSE](LICENSE).
