from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import Path

from robin.config import state_dir, topics_path
from robin.index import ensure_entry_in_index
from robin.models import Entry
from robin.parser import RobinEntryParseError, SEPARATOR, load_all_entries, parse_entry, topic_slug, topic_to_filename
from robin.serializer import serialize_entry


@dataclass(slots=True)
class EntryMatch:
    entry: Entry
    filepath: Path
    chunk_index: int
    raw_chunk: str


class EntryOperationError(ValueError):
    pass


def normalize_body(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def duplicate_candidates(entries: list[Entry], entry: Entry) -> list[Entry]:
    source = entry.source.strip().lower()
    media_source = entry.media_source.strip().lower()
    body = normalize_body(entry.body)
    matches: list[Entry] = []

    for candidate in entries:
        if candidate.entry_id == entry.entry_id:
            continue
        if source and candidate.source.strip().lower() == source:
            matches.append(candidate)
            continue
        if media_source and candidate.media_source.strip().lower() == media_source:
            matches.append(candidate)
            continue
        if body and normalize_body(candidate.body) == body:
            matches.append(candidate)

    return matches


def duplicate_payload(matches: list[Entry]) -> list[dict]:
    return [
        {
            "id": entry.entry_id,
            "topic": entry.topic,
            "date_added": entry.date_added,
            "source": entry.source,
            "media_source": entry.media_source,
            "description": entry.description,
        }
        for entry in matches
    ]


def _topic_files(config: dict, explicit_state_dir: str | None) -> list[Path]:
    base = topics_path(config, explicit_state_dir)
    if not base.exists():
        return []
    return sorted(base.glob("*.md"))


def _load_topic_chunks(filepath: Path) -> list[EntryMatch]:
    content = filepath.read_text(encoding="utf-8")
    if not content.strip():
        return []

    matches: list[EntryMatch] = []
    for chunk_index, chunk in enumerate(content.split(SEPARATOR), start=1):
        if not chunk.strip():
            continue
        raw_chunk = chunk.strip()
        try:
            entry = parse_entry(raw_chunk.lstrip(), filepath.stem)
        except ValueError as exc:
            raise RobinEntryParseError(filepath, chunk_index, str(exc)) from exc
        matches.append(EntryMatch(entry=entry, filepath=filepath, chunk_index=chunk_index, raw_chunk=raw_chunk))
    return matches


def _find_entry_matches(config: dict, explicit_state_dir: str | None, entry_id: str) -> list[EntryMatch]:
    matches: list[EntryMatch] = []
    for filepath in _topic_files(config, explicit_state_dir):
        for chunk in _load_topic_chunks(filepath):
            if chunk.entry.entry_id == entry_id:
                matches.append(chunk)
    return matches


def _write_chunks(filepath: Path, chunks: list[str]) -> None:
    if chunks:
        filepath.write_text(SEPARATOR.join(chunks) + "\n", encoding="utf-8")
    elif filepath.exists():
        filepath.unlink()


def _remove_match(match: EntryMatch) -> None:
    chunks = _load_topic_chunks(match.filepath)
    remaining = [chunk.raw_chunk for chunk in chunks if chunk.entry.entry_id != match.entry.entry_id]
    _write_chunks(match.filepath, remaining)


def _require_single_match(config: dict, explicit_state_dir: str | None, entry_id: str) -> EntryMatch:
    matches = _find_entry_matches(config, explicit_state_dir, entry_id)
    if not matches:
        raise EntryOperationError(f"Entry '{entry_id}' not found.")
    if len(matches) > 1:
        raise EntryOperationError(f"Entry '{entry_id}' appears more than once. Run robin-doctor before mutating entries.")
    return matches[0]


def validate_destination_topic(topic: str) -> str:
    slug = topic_slug(topic)
    if not topic.strip() or slug == "untitled":
        raise EntryOperationError("Move requires a non-empty topic that normalizes to a valid filename.")
    return slug


def delete_entry(config: dict, explicit_state_dir: str | None, index: dict, entry_id: str) -> dict:
    match = _require_single_match(config, explicit_state_dir, entry_id)
    _remove_match(match)
    index.setdefault("items", {}).pop(entry_id, None)
    return {
        "status": "deleted",
        "id": match.entry.entry_id,
        "topic": match.entry.topic,
        "filename": match.filepath.name,
    }


def move_entry(config: dict, explicit_state_dir: str | None, index: dict, entry_id: str, topic: str) -> dict:
    dest_topic = validate_destination_topic(topic)
    match = _require_single_match(config, explicit_state_dir, entry_id)
    from_filename = match.filepath.name
    to_filename = topic_to_filename(topic)

    if match.entry.topic != dest_topic:
        _remove_match(match)
        moved = replace(match.entry, topic=dest_topic)
        dest_path = topics_path(config, explicit_state_dir) / to_filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        serialized = serialize_entry(moved)
        if dest_path.exists():
            content = dest_path.read_text(encoding="utf-8").rstrip()
            out = content + SEPARATOR + serialized if content else serialized
        else:
            out = serialized
        dest_path.write_text(out + "\n", encoding="utf-8")
    else:
        moved = match.entry

    ensure_entry_in_index(moved, index)
    index["items"][entry_id]["topic"] = moved.topic
    index["items"][entry_id]["date"] = moved.date_added
    return {
        "status": "moved",
        "id": moved.entry_id,
        "from_topic": match.entry.topic,
        "to_topic": moved.topic,
        "from_filename": from_filename,
        "to_filename": to_filename,
    }


def load_entries_for_dedupe(config: dict, explicit_state_dir: str | None) -> list[Entry]:
    return load_all_entries(config, explicit_state_dir)


def remove_new_media_if_present(explicit_state_dir: str | None, media_source: str) -> None:
    if not media_source.strip() or media_source.startswith(("http://", "https://")):
        return
    media_path = (state_dir(explicit_state_dir) / media_source).resolve()
    try:
        media_path.relative_to(state_dir(explicit_state_dir))
    except ValueError:
        return
    try:
        if media_path.is_file():
            media_path.unlink()
    except OSError:
        return
