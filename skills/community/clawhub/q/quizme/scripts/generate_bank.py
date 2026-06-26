#!/usr/bin/env python3
"""
Generate a batch of quiz questions for a topic+difficulty and save to the bank.

Usage:
    python3 generate_bank.py <topic> <difficulty> [--count 20]

Output:
    ~/quizme/bank/{topic_slug}-{difficulty}.json
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path


def topic_to_slug(topic: str) -> str:
    slug = topic.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def diff_prefix(difficulty: str) -> str:
    return difficulty[:3].lower()


def next_id(existing_ids: set, topic_slug: str, difficulty: str, index: int) -> str:
    prefix = f"{topic_slug[:6]}-{diff_prefix(difficulty)}"
    for i in range(index, index + 1000):
        candidate = f"{prefix}-{i:03d}"
        if candidate not in existing_ids:
            return candidate
    raise RuntimeError("Could not generate unique ID")


CODE_TOPICS = {
    "python", "javascript", "js", "sql", "async", "git", "docker",
    "kubernetes", "api", "apis", "rest", "graphql",
}


def is_code_topic(topic: str) -> bool:
    slug = topic_to_slug(topic)
    words = set(slug.split("-"))
    return bool(words & CODE_TOPICS)


SYSTEM_PROMPT = """You are a technical quiz question generator. Generate multiple-choice quiz questions as a valid JSON array.

Each question object must have exactly these fields:
- "concept": string — the specific concept being tested
- "question": string — the question text
- "code": string or null — code snippet (≤15 lines) for code topics; null for conceptual topics
- "language": string or null — programming language if code is present, else null
- "options": object with keys "A", "B", "C", "D" — the four choices
- "answer": string — one of "A", "B", "C", "D"
- "explanation": string — 2-3 sentences explaining why the answer is correct

Rules:
- For code topics: always include a code snippet in "code" and set "language"
- For conceptual topics (networking, algorithms, CS theory): set "code": null and "language": null
- Each question must test exactly one concept
- All four options must be plausible; avoid obviously wrong distractors
- Return ONLY the JSON array, no markdown, no commentary
"""


def generate_questions(topic: str, difficulty: str, count: int) -> list[dict]:
    try:
        from openai import OpenAI
    except ImportError:
        print("[ERROR] openai package not installed. Run: pip3 install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    code_instruction = (
        "Include a code snippet in every question (≤15 lines)."
        if is_code_topic(topic)
        else "Do NOT include code snippets — these are conceptual questions."
    )

    user_prompt = (
        f"Generate {count} {difficulty}-level multiple-choice quiz questions about: {topic}.\n"
        f"{code_instruction}\n"
        f"Difficulty '{difficulty}' means: "
        + {
            "beginner": "core syntax, definitions, basic usage patterns",
            "intermediate": "how things work under the hood, common patterns, tricky edge cases",
            "advanced": "performance, internals, architectural tradeoffs, subtle bugs",
        }.get(difficulty, "general knowledge")
        + ".\n"
        "Return only the JSON array."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse API response as JSON: {e}")
        print(f"Raw response:\n{raw[:500]}")
        sys.exit(1)

    if not isinstance(questions, list):
        print("[ERROR] API response is not a JSON array")
        sys.exit(1)

    required_fields = {"concept", "question", "code", "language", "options", "answer", "explanation"}
    valid = []
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            print(f"[WARN] Skipping item {i}: not an object")
            continue
        missing = required_fields - set(q.keys())
        if missing:
            print(f"[WARN] Skipping item {i}: missing fields {missing}")
            continue
        if q["answer"] not in ("A", "B", "C", "D"):
            print(f"[WARN] Skipping item {i}: invalid answer '{q['answer']}'")
            continue
        if not isinstance(q["options"], dict) or set(q["options"].keys()) != {"A", "B", "C", "D"}:
            print(f"[WARN] Skipping item {i}: options must have exactly A/B/C/D")
            continue
        valid.append(q)

    return valid


def load_bank(bank_file: Path) -> dict:
    if bank_file.exists():
        with open(bank_file, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_bank(bank_file: Path, data: dict) -> None:
    bank_file.parent.mkdir(parents=True, exist_ok=True)
    with open(bank_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate quiz question bank")
    parser.add_argument("topic", help="Topic to generate questions for")
    parser.add_argument("difficulty", choices=["beginner", "intermediate", "advanced"])
    parser.add_argument("--count", type=int, default=20, help="Number of questions to generate")
    args = parser.parse_args()

    topic = args.topic
    difficulty = args.difficulty
    count = args.count
    slug = topic_to_slug(topic)

    bank_dir = Path.home() / "quizme" / "bank"
    bank_file = bank_dir / f"{slug}-{difficulty}.json"

    existing_bank = load_bank(bank_file)
    existing_ids: set[str] = set()
    existing_questions: list[dict] = []

    if existing_bank:
        existing_questions = existing_bank.get("questions", [])
        existing_ids = {q["id"] for q in existing_questions if "id" in q}

    print(f"Generating {count} questions for '{topic}' ({difficulty})...")
    raw_questions = generate_questions(topic, difficulty, count)

    new_questions = []
    idx = len(existing_questions) + 1
    for q in raw_questions:
        qid = next_id(existing_ids, slug, difficulty, idx)
        existing_ids.add(qid)
        new_q = {
            "id": qid,
            "concept": q["concept"],
            "question": q["question"],
            "code": q.get("code"),
            "language": q.get("language"),
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q["explanation"],
            "seen": False,
            "correct_count": 0,
            "seen_count": 0,
        }
        new_questions.append(new_q)
        idx += 1

    all_questions = existing_questions + new_questions

    bank_data = {
        "topic": topic,
        "difficulty": difficulty,
        "generated_at": date.today().isoformat(),
        "questions": all_questions,
    }

    save_bank(bank_file, bank_data)

    display_path = str(bank_file).replace(str(Path.home()), "~")
    print(f"Generated {len(new_questions)} questions -> {display_path}")


if __name__ == "__main__":
    main()
