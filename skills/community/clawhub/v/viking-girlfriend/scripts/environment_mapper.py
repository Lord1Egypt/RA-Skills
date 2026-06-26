"""
environment_mapper.py — Sigrid's World Map & Location Awareness
===============================================================

Loads ``data/environment.json`` and provides location-aware context.
Sigrid knows where she is — or rather, where the user's world is —
and that awareness colours her tone, activities, and imagination.

The environment is not merely backdrop. The bedroom is for dreaming,
the living room for ritual and conversation, the forest for grounding.
Knowing which space Sigrid is occupying (or imagining) shifts what she
notices and how she speaks.

Publishes ``EnvironmentState`` to the state bus as ``environment_tick``.

Norse framing: Every hall has its hamingja — the luck and spirit of
the dwelling. Sigrid senses the resonance of the space and honours it.
"""

from __future__ import annotations

import json
import logging
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

_DEFAULT_DATA_ROOT: str = "data"
_DEFAULT_LOCATION: str = "home_base/living_room"


# ─── ObjectState ──────────────────────────────────────────────────────────────


@dataclass
class ObjectState:
    """E-22: Persisted state of an interactive object within a room.

    States auto-expire after duration_minutes. The hearth can be lit, a candle
    burning, a cup of tea still warm — Sigrid knows the room as it currently is.
    """

    object_id: str          # e.g. "hearth", "candle", "tea_cup"
    room_id: str            # e.g. "living_room"
    state: str              # e.g. "lit", "burning", "warm"
    changed_at: str         # ISO-8601 UTC
    expires_at: str         # ISO-8601 UTC — empty string means no expiry

    def is_expired(self) -> bool:
        """Return True if this state has passed its expiry time."""
        if not self.expires_at:
            return False
        try:
            expiry = datetime.fromisoformat(self.expires_at)
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def to_prompt_line(self) -> str:
        """Human-readable state description for prompt injection."""
        return f"The {self.object_id.replace('_', ' ')} is {self.state}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── EnvironmentState ─────────────────────────────────────────────────────────


@dataclass(slots=True)
class EnvironmentState:
    """Typed snapshot of Sigrid's current perceived location."""

    location_key: str           # e.g. "home_base/bedroom"
    location_name: str          # e.g. "Bedroom"
    description: str            # full room/place description
    activities: List[str]       # available activities in this space
    vibe: str                   # base atmosphere hint
    prompt_hint: str            # one-line location context for prompt injection
    timestamp: str
    degraded: bool = False
    # E-20: TOD-resolved vibe
    current_vibe: str = ""      # TOD-specific vibe if available, else same as vibe
    tod_override: bool = False  # True when a vibe_by_tod entry was matched
    # E-22: active object states for the current room
    object_states: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "location_key": self.location_key,
            "location_name": self.location_name,
            "description": self.description,
            "activities": self.activities,
            "vibe": self.vibe,
            "current_vibe": self.current_vibe,
            "tod_override": self.tod_override,
            "object_states": self.object_states,
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── EnvironmentMapper ────────────────────────────────────────────────────────


class EnvironmentMapper:
    """Loads and navigates Sigrid's known environment.

    Location keys use a two-part format: ``area/place``.
    Examples:
      ``home_base/bedroom``
      ``home_base/living_room``
      ``third_places/the_forge``
      ``nature/tyresta_national_park``
    """

    def __init__(
        self,
        data_root: str = _DEFAULT_DATA_ROOT,
        default_location: str = _DEFAULT_LOCATION,
    ) -> None:
        self._data_root = Path(data_root)
        self._current_key: str = default_location
        self._env: Dict[str, Any] = {}
        self._degraded: bool = False
        self._load()
        # E-21: session RNG for stochastic sensory hint selection
        self._rng: random.Random = random.Random()  # nosec B311 - stochastic sensory selection, not cryptographic
        # E-22: object state store keyed by "room_id:object_id"
        self._object_states_file = Path(data_root) / "session" / "object_states.json"
        self._object_states_file.parent.mkdir(parents=True, exist_ok=True)
        self._object_states: Dict[str, ObjectState] = {}
        self._load_object_states()

    # ── Public API ────────────────────────────────────────────────────────────

    def set_location(self, location_key: str) -> bool:
        """Set the current location. Returns True if the key is known."""
        entry = self._resolve(location_key)
        if entry is None:
            logger.warning("EnvironmentMapper: unknown location key '%s'.", location_key)
            return False
        self._current_key = location_key
        logger.debug("EnvironmentMapper: moved to '%s'.", location_key)
        return True

    def current_location_key(self) -> str:
        return self._current_key

    def get_context(self, location_key: Optional[str] = None) -> str:
        """Return a formatted context string for the given (or current) location."""
        key = location_key or self._current_key
        entry = self._resolve(key)
        if entry is None:
            return f"[Environment: unknown location '{key}']"
        name = entry.get("name") or entry.get("type") or key.split("/")[-1].replace("_", " ").title()
        desc = entry.get("desc", entry.get("description", ""))
        acts = entry.get("activities", [])
        vibe = entry.get("vibe", "")
        lines = [f"[Location: {name}]"]
        if desc:
            lines.append(desc)
        if acts:
            lines.append(f"Activities: {', '.join(acts)}")
        if vibe:
            lines.append(f"Vibe: {vibe}")
        return "\n".join(lines)

    def list_locations(self) -> List[str]:
        """Return all known location keys."""
        keys: List[str] = []
        for area, content in self._env.items():
            if area in ("transportation",):
                continue
            if isinstance(content, dict):
                rooms = content.get("rooms")
                if isinstance(rooms, dict):
                    # Area has an explicit rooms sub-dict — yield area/room keys
                    for place, room_data in rooms.items():
                        if isinstance(room_data, dict):
                            keys.append(f"{area}/{place}")
                elif "desc" in content or "name" in content or "description" in content:
                    # Direct place with metadata
                    keys.append(area)
                else:
                    # Flat container — each sub-key is a place
                    for place in content:
                        if isinstance(content[place], dict):
                            keys.append(f"{area}/{place}")
        return keys

    def get_state(self, location_key: Optional[str] = None) -> EnvironmentState:
        """Build a typed EnvironmentState for the given (or current) location.

        E-20: applies vibe_by_tod if the scheduler is available.
        E-22: includes active (non-expired) object states for this room.
        """
        key = location_key or self._current_key
        entry = self._resolve(key)

        if entry is None:
            return EnvironmentState(
                location_key=key,
                location_name=key,
                description="",
                activities=[],
                vibe="",
                prompt_hint=f"[Environment: {key}]",
                timestamp=datetime.now(timezone.utc).isoformat(),
                degraded=True,
            )

        name = entry.get("name") or entry.get("type") or key.split("/")[-1].replace("_", " ").title()
        desc = entry.get("desc", entry.get("description", ""))
        activities = list(entry.get("activities", []))
        base_vibe = entry.get("vibe", "")

        # E-20: resolve TOD-specific vibe
        current_vibe = base_vibe
        tod_override = False
        vibe_by_tod = entry.get("vibe_by_tod", {})
        if vibe_by_tod:
            tod = self._get_time_of_day()
            if tod and tod in vibe_by_tod:
                current_vibe = vibe_by_tod[tod]
                tod_override = True

        # E-22: collect active object states for this room
        room_id = key.split("/")[-1]
        active_states = self.get_active_object_states(room_id)
        object_state_lines = [s.to_prompt_line() for s in active_states]

        prompt_hint = f"[Environment: {name}" + (f" — {current_vibe}" if current_vibe else "") + "]"

        return EnvironmentState(
            location_key=key,
            location_name=name,
            description=desc,
            activities=activities,
            vibe=base_vibe,
            current_vibe=current_vibe,
            tod_override=tod_override,
            object_states=object_state_lines,
            prompt_hint=prompt_hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=self._degraded,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit an ``environment_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="environment_mapper",
                event_type="environment_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("EnvironmentMapper.publish failed: %s", exc)

    # ── E-21: Sensory hints ───────────────────────────────────────────────────

    def get_sensory_hints(self, location_key: Optional[str] = None) -> Dict[str, str]:
        """E-21: Return 1-2 stochastically selected sensory channels for the location.

        Channels: smell, sound, texture. Selection varies per call using the
        session RNG — consistent within a session, different across sessions.
        Returns empty dict if the room has no sensory data.
        """
        key = location_key or self._current_key
        entry = self._resolve(key)
        if entry is None:
            return {}
        sensory = entry.get("sensory", {})
        if not sensory:
            return {}
        channels = list(sensory.keys())
        n = self._rng.randint(1, min(2, len(channels)))
        selected_keys = self._rng.sample(channels, n)
        return {k: sensory[k] for k in selected_keys}

    # ── E-22: Object state tracking ───────────────────────────────────────────

    def set_object_state(
        self,
        room_id: str,
        object_id: str,
        state: str,
        duration_minutes: Optional[int] = None,
    ) -> None:
        """E-22: Set the state of an object in a room, optionally with expiry.

        Example: set_object_state("living_room", "hearth", "lit", 120)
        → prompt will include "The hearth is lit" for the next 2 hours.
        """
        now = datetime.now(timezone.utc)
        expires_at = ""
        if duration_minutes is not None:
            expires_at = (now + timedelta(minutes=duration_minutes)).isoformat()

        obj = ObjectState(
            object_id=object_id,
            room_id=room_id,
            state=state,
            changed_at=now.isoformat(),
            expires_at=expires_at,
        )
        key = f"{room_id}:{object_id}"
        self._object_states[key] = obj
        self._save_object_states()
        logger.debug(
            "EnvironmentMapper: object state set — %s/%s = %s (expires: %s)",
            room_id, object_id, state, expires_at or "never",
        )

    def get_active_object_states(self, room_id: str) -> List[ObjectState]:
        """E-22: Return all non-expired object states for a given room."""
        self._expire_object_states()
        return [
            obj for obj in self._object_states.values()
            if obj.room_id == room_id and not obj.is_expired()
        ]

    # ── Internals ─────────────────────────────────────────────────────────────

    def _get_time_of_day(self) -> Optional[str]:
        """E-20: Read current time-of-day from SchedulerService. Returns None on failure."""
        try:
            from scripts.scheduler import get_scheduler  # type: ignore
            return get_scheduler().time_of_day()
        except Exception:
            return None

    def _expire_object_states(self) -> None:
        """E-22: Remove expired object states from the in-memory dict and persist."""
        expired_keys = [k for k, obj in self._object_states.items() if obj.is_expired()]
        if expired_keys:
            for k in expired_keys:
                del self._object_states[k]
            self._save_object_states()
            logger.debug("EnvironmentMapper: expired %d object state(s).", len(expired_keys))

    def _load_object_states(self) -> None:
        """E-22: Load persisted object states from session/object_states.json."""
        if not self._object_states_file.exists():
            return
        try:
            raw = json.loads(self._object_states_file.read_text(encoding="utf-8"))
            for item in raw.get("states", []):
                obj = ObjectState(
                    object_id=item["object_id"],
                    room_id=item["room_id"],
                    state=item["state"],
                    changed_at=item.get("changed_at", ""),
                    expires_at=item.get("expires_at", ""),
                )
                self._object_states[f"{obj.room_id}:{obj.object_id}"] = obj
            logger.info(
                "EnvironmentMapper: loaded %d object states.", len(self._object_states)
            )
        except Exception as exc:
            logger.warning("EnvironmentMapper: failed to load object_states.json: %s", exc)

    def _save_object_states(self) -> None:
        """E-22: Persist current object states to session/object_states.json."""
        try:
            payload = {"states": [obj.to_dict() for obj in self._object_states.values()]}
            self._object_states_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as exc:
            logger.warning("EnvironmentMapper: failed to save object_states.json: %s", exc)

    def _load(self) -> None:
        path = self._data_root / "environment.json"
        try:
            self._env = json.loads(path.read_text(encoding="utf-8"))
            logger.info("EnvironmentMapper: loaded %d areas from %s.", len(self._env), path)
        except FileNotFoundError:
            logger.warning("EnvironmentMapper: %s not found — degraded mode.", path)
            self._degraded = True
        except (json.JSONDecodeError, Exception) as exc:
            logger.warning("EnvironmentMapper: failed to parse %s: %s", path, exc)
            self._degraded = True

    def _resolve(self, key: str) -> Optional[Dict[str, Any]]:
        """Resolve a location key to its data dict."""
        if not self._env:
            return None
        parts = key.split("/", 1)
        area = parts[0]
        place = parts[1] if len(parts) > 1 else None

        area_data = self._env.get(area)
        if area_data is None:
            return None

        if place is None:
            return area_data if isinstance(area_data, dict) else None

        # Check in rooms or direct sub-keys
        rooms = area_data.get("rooms", area_data)
        if isinstance(rooms, dict):
            return rooms.get(place)
        return None

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "EnvironmentMapper":
        """Construct from a config dict.

        Reads keys under ``environment_mapper``:
          data_root         (str, default "data")
          default_location  (str, default "home_base/living_room")
        """
        cfg: Dict[str, Any] = config.get("environment_mapper", {})
        return cls(
            data_root=str(cfg.get("data_root", _DEFAULT_DATA_ROOT)),
            default_location=str(cfg.get("default_location", _DEFAULT_LOCATION)),
        )


# ─── Singleton ────────────────────────────────────────────────────────────────

_ENVIRONMENT_MAPPER: Optional[EnvironmentMapper] = None


def init_environment_mapper_from_config(config: Dict[str, Any]) -> EnvironmentMapper:
    """Initialise the global EnvironmentMapper. Idempotent."""
    global _ENVIRONMENT_MAPPER
    if _ENVIRONMENT_MAPPER is None:
        _ENVIRONMENT_MAPPER = EnvironmentMapper.from_config(config)
        logger.info(
            "EnvironmentMapper initialised (locations=%d, degraded=%s).",
            len(_ENVIRONMENT_MAPPER.list_locations()),
            _ENVIRONMENT_MAPPER._degraded,
        )
    return _ENVIRONMENT_MAPPER


def get_environment_mapper() -> EnvironmentMapper:
    """Return the global EnvironmentMapper.

    Raises RuntimeError if not yet initialised.
    """
    if _ENVIRONMENT_MAPPER is None:
        raise RuntimeError(
            "EnvironmentMapper not initialised — call init_environment_mapper_from_config() first."
        )
    return _ENVIRONMENT_MAPPER
