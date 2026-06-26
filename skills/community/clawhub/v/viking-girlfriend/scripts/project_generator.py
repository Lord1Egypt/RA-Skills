"""
project_generator.py — Sigrid's Initiative Tracker
====================================================

New module — no source adoption. Sigrid carries ongoing projects:
creative work, learning paths, crafted things, shared endeavours with
the user. This module tracks them across sessions so nothing is forgotten.

A project is a named initiative with a status, a description, a running
note log, and metadata. Projects are stored in ``data/projects.json``
and persist across sessions.

Published to the state bus as ``project_tick`` so prompt_synthesizer
can inject awareness of active work into Sigrid's voice.

Norse framing: Skaði weaves the long hunt across seasons. Not every
worthy thing is completed in a day — some take the full turning of the year.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

_DEFAULT_DATA_ROOT: str = "data"
_MAX_PROJECTS: int = 100
_MAX_NOTES_PER_PROJECT: int = 50

ProjectStatus = Literal["active", "paused", "complete", "abandoned"]


# ─── Project dataclass ────────────────────────────────────────────────────────


@dataclass
class Project:
    """A single named initiative."""

    project_id: str
    name: str
    description: str
    status: str = "active"
    tags: List[str] = field(default_factory=list)
    notes: List[Dict[str, str]] = field(default_factory=list)   # [{ts, text}]
    created_at: str = ""
    updated_at: str = ""

    def add_note(self, text: str) -> None:
        """Append a timestamped note."""
        self.notes.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "text": text,
        })
        if len(self.notes) > _MAX_NOTES_PER_PROJECT:
            self.notes = self.notes[-_MAX_NOTES_PER_PROJECT:]
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def summary(self, max_note_chars: int = 120) -> str:
        """One-line summary for context injection."""
        latest = self.notes[-1]["text"][:max_note_chars] if self.notes else ""
        tag_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        note_str = f" — {latest}" if latest else ""
        return f"{self.name} ({self.status}){tag_str}{note_str}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            project_id=data.get("project_id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            status=data.get("status", "active"),
            tags=list(data.get("tags", [])),
            notes=list(data.get("notes", [])),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )


# ─── ProjectState ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ProjectState:
    """Typed snapshot of the project registry for state bus publication."""

    total_projects: int
    active_count: int
    paused_count: int
    complete_count: int
    recent_summaries: List[str]     # summaries of active projects (up to 5)
    prompt_hint: str
    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "counts": {
                "total": self.total_projects,
                "active": self.active_count,
                "paused": self.paused_count,
                "complete": self.complete_count,
            },
            "recent_summaries": self.recent_summaries,
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── ProjectGenerator ─────────────────────────────────────────────────────────


class ProjectGenerator:
    """Sigrid's persistent initiative tracker.

    Projects survive session breaks via JSON persistence.
    Use ``add_project()`` to create, ``update_status()`` to move between
    states, and ``add_note()`` to log progress.
    """

    def __init__(self, data_root: str = _DEFAULT_DATA_ROOT) -> None:
        self._root = Path(data_root)
        self._root.mkdir(parents=True, exist_ok=True)
        self._file = self._root / "projects.json"
        self._projects: Dict[str, Project] = {}
        self._degraded: bool = False
        self._load()

    # ── Public API ────────────────────────────────────────────────────────────

    def add_project(
        self,
        name: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        initial_note: str = "",
    ) -> Project:
        """Create a new project. Returns the created Project."""
        now = datetime.now(timezone.utc).isoformat()
        project = Project(
            project_id=str(uuid.uuid4()),
            name=name,
            description=description,
            status="active",
            tags=tags or [],
            created_at=now,
            updated_at=now,
        )
        if initial_note:
            project.add_note(initial_note)
        self._projects[project.project_id] = project
        self._save()
        logger.info("ProjectGenerator: created project '%s'.", name)
        return project

    def update_status(self, project_id: str, status: str) -> bool:
        """Change a project's status. Returns True if found."""
        project = self._projects.get(project_id)
        if project is None:
            return False
        project.status = status
        project.updated_at = datetime.now(timezone.utc).isoformat()
        self._save()
        return True

    def add_note(self, project_id: str, text: str) -> bool:
        """Add a note to a project. Returns True if found."""
        project = self._projects.get(project_id)
        if project is None:
            return False
        project.add_note(text)
        self._save()
        return True

    def get_project(self, project_id: str) -> Optional[Project]:
        return self._projects.get(project_id)

    def list_projects(
        self,
        status: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Project]:
        """List projects, optionally filtered by status and/or tag."""
        projects = list(self._projects.values())
        if status:
            projects = [p for p in projects if p.status == status]
        if tag:
            projects = [p for p in projects if tag in p.tags]
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)

    def get_state(self) -> ProjectState:
        """Build a typed ProjectState snapshot."""
        all_p = list(self._projects.values())
        active = [p for p in all_p if p.status == "active"]
        paused = [p for p in all_p if p.status == "paused"]
        complete = [p for p in all_p if p.status == "complete"]
        summaries = [p.summary() for p in active[:5]]
        hint = self._build_prompt_hint(len(active), summaries)
        return ProjectState(
            total_projects=len(all_p),
            active_count=len(active),
            paused_count=len(paused),
            complete_count=len(complete),
            recent_summaries=summaries,
            prompt_hint=hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=self._degraded,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit a ``project_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="project_generator",
                event_type="project_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("ProjectGenerator.publish failed: %s", exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _build_prompt_hint(self, active_count: int, summaries: List[str]) -> str:
        if not summaries:
            return "[Projects: none active]"
        first = summaries[0][:80]
        rest = f" (+{active_count - 1} more)" if active_count > 1 else ""
        return f"[Projects: {first}{rest}]"

    def _load(self) -> None:
        if not self._file.exists():
            return
        try:
            raw = json.loads(self._file.read_text(encoding="utf-8"))
            for entry in raw.get("projects", []):
                p = Project.from_dict(entry)
                self._projects[p.project_id] = p
            logger.info("ProjectGenerator: loaded %d projects.", len(self._projects))
        except Exception as exc:
            logger.warning("ProjectGenerator: failed to load %s: %s", self._file, exc)
            self._degraded = True

    def _save(self) -> None:
        try:
            all_p = list(self._projects.values())
            if len(all_p) > _MAX_PROJECTS:
                # Keep newest + all active
                active = [p for p in all_p if p.status == "active"]
                rest = [p for p in all_p if p.status != "active"]
                rest.sort(key=lambda p: p.updated_at, reverse=True)
                all_p = active + rest[:(_MAX_PROJECTS - len(active))]
                self._projects = {p.project_id: p for p in all_p}
            payload = {"projects": [p.to_dict() for p in self._projects.values()]}
            self._file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.warning("ProjectGenerator: failed to save: %s", exc)

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ProjectGenerator":
        """Construct from a config dict.

        Reads keys under ``project_generator``:
          data_root  (str, default "data")
        """
        cfg: Dict[str, Any] = config.get("project_generator", {})
        return cls(data_root=str(cfg.get("data_root", _DEFAULT_DATA_ROOT)))


# ─── Singleton ────────────────────────────────────────────────────────────────

_PROJECT_GENERATOR: Optional[ProjectGenerator] = None


def init_project_generator_from_config(config: Dict[str, Any]) -> ProjectGenerator:
    """Initialise the global ProjectGenerator. Idempotent."""
    global _PROJECT_GENERATOR
    if _PROJECT_GENERATOR is None:
        _PROJECT_GENERATOR = ProjectGenerator.from_config(config)
        logger.info(
            "ProjectGenerator initialised (%d projects loaded).",
            len(_PROJECT_GENERATOR._projects),
        )
    return _PROJECT_GENERATOR


def get_project_generator() -> ProjectGenerator:
    """Return the global ProjectGenerator.

    Raises RuntimeError if not yet initialised.
    """
    if _PROJECT_GENERATOR is None:
        raise RuntimeError(
            "ProjectGenerator not initialised — call init_project_generator_from_config() first."
        )
    return _PROJECT_GENERATOR
