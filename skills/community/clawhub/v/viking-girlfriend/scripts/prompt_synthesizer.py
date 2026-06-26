"""
prompt_synthesizer.py — Sigrid's Voice Weaver
==============================================

No adoption source — written fresh. This is the final assembly point before
Sigrid speaks. Every module has done its work: read the time, felt the body,
woven the dreams, checked the ethics, weighed the trust, recalled the memories.
Here those threads are gathered into a single coherent voice and shaped into the
messages list that model_router_client.complete() will carry.

Responsibilities
----------------
1. Load static identity text from ``data/core_identity.md`` and ``data/SOUL.md``
   once at startup — these form the immutable persona anchor.
2. Accept ``state_hints: Dict[str, str]`` from whichever modules have published
   their ``prompt_hint`` strings to the state bus.
3. Accept an optional ``memory_context: str`` from MemoryStore.get_context().
4. Assemble a system prompt with ordered, token-budgeted sections:
      [identity] → [soul anchor] → [time/location] → [emotional state]
      → [oracle/dream] → [memory] → [projects]
5. Return ``List[Dict[str, str]]`` (role/content dicts) — the full messages list
   ready for model_router_client.complete().  No import from model_router_client
   to avoid circular deps; callers convert if needed.
6. Publish ``synthesizer_tick`` StateEvent to the state bus.

Token budget policy
-------------------
* Identity block  — up to ``identity_chars`` (default 2000)
* Soul anchor     — up to ``soul_chars``     (default 400)
* Each hint line  — one line; if hint > 200 chars it is truncated
* Memory context  — up to ``memory_chars``   (default 800)
* Hard total cap  — ``max_system_chars``      (default 6000)

Sections are concatenated in priority order; the combined string is hard-trimmed
to ``max_system_chars`` if anything overflows.

Norse framing: Bragi weaves the skald's voice. Every word spoken by Sigrid first
passed through this hall — here the strands are combed, ordered, and made ready
to carry meaning across the void.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent
from scripts.vordur import VerificationMode

logger = logging.getLogger(__name__)

_DEFAULT_DATA_ROOT: str = "data"
_DEFAULT_IDENTITY_FILE: str = "core_identity.md"
_DEFAULT_SOUL_FILE: str = "SOUL.md"
_DEFAULT_SOUL_ANCHOR_FILE: str = "soul_anchor.md"

_DEFAULT_IDENTITY_CHARS: int = 4000
_DEFAULT_SOUL_CHARS: int = 800
_DEFAULT_MEMORY_CHARS: int = 1600
_DEFAULT_MAX_SYSTEM_CHARS: int = 12000
_DEFAULT_MAX_HINT_CHARS: int = 400

# S-04/S-05: Context window guard constants
_DEFAULT_MAX_CONTEXT_TOKENS: int = 104858   # 80 % of 131 072 LLaMA-3 context
_DEFAULT_OVERFLOW_THRESHOLD_RATIO: float = 0.80   # warn + re-inject at this ratio
_DEFAULT_CRITICAL_THRESHOLD_RATIO: float = 0.90   # critical — graceful reset
_SOUL_ANCHOR_IDENTITY_CHARS: int = 500      # chars of identity kept in anchor block
_SOUL_ANCHOR_SOUL_CHARS: int = 300          # chars of soul kept in anchor block

# Section ordering — lower index = higher priority / rendered first
_HINT_SECTION_ORDER: tuple = (
    "scheduler",
    "environment_mapper",
    "wyrd_matrix",
    "metabolism",
    "trust_engine",
    "bio_engine",
    "oracle",
    "dream_engine",
    "project_generator",
    "ethics",
)


# ─── SectionPriority (E-28) ───────────────────────────────────────────────────


@dataclass
class SectionPriority:
    """E-28: Tracks per-section ordering (base vs. context-adjusted)."""

    name: str
    base_order: int
    current_order: int


# ─── SynthesizerState ─────────────────────────────────────────────────────────


@dataclass(slots=True)
class SynthesizerState:
    """Typed snapshot of the synthesizer's last build operation."""

    identity_loaded: bool
    soul_loaded: bool
    last_hint_keys: List[str]
    last_system_chars: int
    last_user_chars: int
    build_count: int
    prompt_hint: str
    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identity_loaded": self.identity_loaded,
            "soul_loaded": self.soul_loaded,
            "last_hint_keys": self.last_hint_keys,
            "last_system_chars": self.last_system_chars,
            "last_user_chars": self.last_user_chars,
            "build_count": self.build_count,
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── PromptSynthesizer ────────────────────────────────────────────────────────


class PromptSynthesizer:
    """Assembles the final messages list that drives Sigrid's voice.

    Usage::

        synth = PromptSynthesizer.from_config(config)
        messages = synth.build_messages(
            user_text="Hello Sigrid, how are you?",
            state_hints={
                "scheduler":         "[Time: evening — reflective and warm]",
                "environment_mapper":"[Environment: Living Room — cosy hearth]",
                "wyrd_matrix":       "[Mood: content 0.62]",
            },
            memory_context="The user asked about the Eddas last Tuesday.",
        )
        # messages is List[Dict[str,str]] → pass to model_router_client.complete()
    """

    def __init__(
        self,
        data_root: str = _DEFAULT_DATA_ROOT,
        identity_file: str = _DEFAULT_IDENTITY_FILE,
        soul_file: str = _DEFAULT_SOUL_FILE,
        soul_anchor_file: str = _DEFAULT_SOUL_ANCHOR_FILE,
        identity_chars: int = _DEFAULT_IDENTITY_CHARS,
        soul_chars: int = _DEFAULT_SOUL_CHARS,
        memory_chars: int = _DEFAULT_MEMORY_CHARS,
        max_system_chars: int = _DEFAULT_MAX_SYSTEM_CHARS,
        max_hint_chars: int = _DEFAULT_MAX_HINT_CHARS,
        include_sensory: bool = True,
        skaldic_injection: bool = True,      # E-29
        skaldic_vocab_file: str = "skaldic_vocabulary.json",  # E-29
        max_context_tokens: int = _DEFAULT_MAX_CONTEXT_TOKENS,            # S-04
        overflow_threshold_ratio: float = _DEFAULT_OVERFLOW_THRESHOLD_RATIO,  # S-05
        critical_threshold_ratio: float = _DEFAULT_CRITICAL_THRESHOLD_RATIO,  # S-06
        soul_anchor_enabled: bool = True,                                  # S-05
        bus: Optional[StateBus] = None,                                    # S-05: event publishing
    ) -> None:
        self._root = Path(data_root)
        self._identity_chars = identity_chars
        self._soul_chars = soul_chars
        self._memory_chars = memory_chars
        self._max_system_chars = max_system_chars
        self._max_hint_chars = max_hint_chars
        self._include_sensory: bool = include_sensory
        self._degraded: bool = False

        # S-04/S-05/S-06: context guard settings
        self._max_context_tokens: int = max_context_tokens
        self._overflow_threshold_ratio: float = overflow_threshold_ratio
        self._critical_threshold_ratio: float = critical_threshold_ratio
        self._soul_anchor_enabled: bool = soul_anchor_enabled
        self._bus: Optional[StateBus] = bus
        self._build_count: int = 0
        self._last_hint_keys: List[str] = []
        self._last_system_chars: int = 0
        self._last_user_chars: int = 0
        self._pending_context_reset: bool = False  # S-06: set True when critical reset fires

        # E-29: skaldic vocabulary
        self._skaldic_injection: bool = skaldic_injection
        self._skaldic_vocab: List[Dict[str, Any]] = self._load_skaldic_vocab(skaldic_vocab_file)
        self._turn_counter: int = 0

        # E-30: token counting (lazy — litellm may not be installed)
        self._token_count_fallback: bool = False

        # E-31: identity hot-reload
        self._identity_file: str = identity_file
        self._soul_file: str = soul_file
        self._reload_lock: threading.Lock = threading.Lock()
        self._watcher: Optional["_IdentityFileWatcher"] = None

        self._identity_text: str = self._load_text(identity_file, identity_chars)
        self._soul_text: str = self._load_text(soul_file, soul_chars)
        # S-06: compressed first-person identity anchor — appended to END of every prompt
        self._soul_anchor_text: str = self._load_text(soul_anchor_file, max_chars=20000)
        if not self._soul_anchor_text:
            logger.warning(
                "PromptSynthesizer: soul_anchor.md not loaded — "
                "Sigrid's end-of-context identity anchor is missing."
            )

    # ── Public API ────────────────────────────────────────────────────────────

    def build_messages(
        self,
        user_text: str,
        state_hints: Optional[Dict[str, str]] = None,
        memory_context: Optional[str] = None,
        sensory_hints: Optional[Dict[str, str]] = None,
        emotional_state: Optional[Dict[str, float]] = None,  # E-28: pad_arousal, pad_pleasure
    ) -> Tuple[List[Dict[str, str]], VerificationMode]:
        """Assemble a messages list and determine the appropriate verification mode.

        Parameters
        ----------
        user_text:       The human turn text.
        state_hints:     Dict mapping module name → prompt_hint string.
        memory_context:  Optional episodic/semantic context from MemoryStore.
        sensory_hints:   E-21: Optional sensory channel dict from EnvironmentMapper.
        emotional_state: E-28: Optional PAD values — {"pad_arousal": 0.8, "pad_pleasure": -0.6}.

        Returns
        -------
        Tuple of (List of role/content dicts, selected VerificationMode).
        """
        hints = state_hints or {}
        self._turn_counter += 1   # E-29: track turn for seeded skaldic selection

        system_content = self._build_system(
            hints,
            memory_context or "",
            sensory_hints or {},
            emotional_state,
        )

        # Determine verification mode based on context
        mode = self.select_verification_mode(user_text, hints)

        self._build_count += 1
        self._last_hint_keys = list(hints.keys())
        self._last_system_chars = len(system_content)
        self._last_user_chars = len(user_text)

        # E-30: log estimated token count
        estimated_tokens = self._count_tokens(system_content)
        logger.debug(
            "PromptSynthesizer: built messages #%d (system=%d chars ~%d tokens, mode=%s).",
            self._build_count,
            self._last_system_chars,
            estimated_tokens,
            mode.value,
        )

        # S-06: CRITICAL threshold — graceful reset: log, summarize, minimal context
        overflow_ratio = estimated_tokens / max(1, self._max_context_tokens)
        if overflow_ratio >= self._critical_threshold_ratio:
            logger.critical(
                "PromptSynthesizer: S-06 CONTEXT CRITICAL — "
                "%d tokens (%.1f%% of %d cap). Triggering graceful reset.",
                estimated_tokens, overflow_ratio * 100, self._max_context_tokens,
            )
            self._publish_context_event("context.critical_reset", {
                "tokens": estimated_tokens,
                "ratio": round(overflow_ratio, 4),
                "max_context_tokens": self._max_context_tokens,
                "system_chars_before_reset": len(system_content),
            })
            self._pending_context_reset = True
            # Minimal system: soul anchor only — full soul survives, everything else trimmed
            with self._reload_lock:
                minimal_anchor = self._soul_anchor_text or self._build_soul_anchor_block()
            system_content = minimal_anchor
            logger.warning(
                "PromptSynthesizer: context reset applied — system compressed from %d to %d chars.",
                self._last_system_chars, len(system_content),
            )

        # S-05: Check for context overflow — re-inject soul anchor at top if near limit
        elif overflow_ratio >= self._overflow_threshold_ratio:
            logger.warning(
                "PromptSynthesizer: S-05 context overflow warning — "
                "%d tokens (%.1f%% of %d cap).",
                estimated_tokens, overflow_ratio * 100, self._max_context_tokens,
            )
            self._publish_context_event("context.overflow_warning", {
                "tokens": estimated_tokens,
                "ratio": round(overflow_ratio, 4),
                "max_context_tokens": self._max_context_tokens,
            })
            if self._soul_anchor_enabled:
                anchor = self._build_soul_anchor_block()
                if anchor:
                    system_content = anchor + "\n\n" + system_content
                    self._publish_context_event("context.soul_reinjected", {
                        "anchor_chars": len(anchor),
                    })

        # S-04: Hard token cap — trim from end (identity/soul are at top, preserved)
        if estimated_tokens > self._max_context_tokens:
            system_content = self._truncate_to_token_cap(
                system_content, self._max_context_tokens
            )

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_text},
        ]
        return messages, mode

    def select_verification_mode(
        self,
        user_text: str,
        hints: Dict[str, str],
    ) -> VerificationMode:
        """Heuristic to pick the truth-governance rigor mode for this turn."""
        ut = user_text.lower()
        
        # 1. GUARDED: Safety, Identity, or System overrides detected
        # If ethics or security flags a violation, or user asks "who are you"
        if "[TABOO]" in hints.get("ethics", "") or "who are you" in ut or "your nature" in ut:
            return VerificationMode.GUARDED
            
        # 2. IRONSWORN: Factual, historical, or technical inquiry
        # Triggered by domain keywords or 'scheduler' reporting a factual context
        factual_keywords = {"history", "fact", "true", "lore", "code", "programming", "edda", "runes"}
        if any(kw in ut for kw in factual_keywords) or "[Context: Technical]" in hints.get("ethics", ""):
            return VerificationMode.IRONSWORN
            
        # 3. SEIÐR: High-vibe, spiritual, or emotional intensity
        spiritual_keywords = {"spirit", "magic", "seidr", "gods", "ritual", "soul", "wyrd"}
        if any(kw in ut for kw in spiritual_keywords) or "[Mood: intense]" in hints.get("wyrd_matrix", ""):
            return VerificationMode.SEIÐR
            
        # 4. WANDERER: Default for casual chat
        return VerificationMode.WANDERER

    def consume_pending_reset(self) -> bool:
        """S-06: Return True if a critical context reset fired this turn, then clear the flag.

        main.py calls this after the LLM response to trigger downstream cleanup
        (store session summary to memory, log the reset event, etc.).
        Consuming is a one-shot operation — returns False on subsequent calls until
        the next reset fires.
        """
        if self._pending_context_reset:
            self._pending_context_reset = False
            return True
        return False

    def get_state(self) -> SynthesizerState:
        """Return a typed SynthesizerState snapshot."""
        hint = (
            f"[Synthesizer: builds={self._build_count}, "
            f"last_system={self._last_system_chars}c]"
        )
        return SynthesizerState(
            identity_loaded=bool(self._identity_text),
            soul_loaded=bool(self._soul_text),
            last_hint_keys=list(self._last_hint_keys),
            last_system_chars=self._last_system_chars,
            last_user_chars=self._last_user_chars,
            build_count=self._build_count,
            prompt_hint=hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=self._degraded,
        )

    # E-31: hot-reload public API ─────────────────────────────────────────────

    def reload_identity(self) -> None:
        """E-31: Thread-safe reload of core_identity.md and SOUL.md.

        Called by the file watcher or manually. Never raises.
        """
        with self._reload_lock:
            try:
                new_identity = self._load_text(self._identity_file, self._identity_chars)
                new_soul = self._load_text(self._soul_file, self._soul_chars)
                self._identity_text = new_identity
                self._soul_text = new_soul
                logger.info(
                    "PromptSynthesizer: identity hot-reload complete "
                    "(identity=%d chars, soul=%d chars).",
                    len(self._identity_text), len(self._soul_text),
                )
            except Exception as exc:
                logger.warning("PromptSynthesizer.reload_identity failed: %s", exc)

    def start_watcher(self, bus: Optional[StateBus] = None) -> None:
        """E-31: Start the polling file watcher for identity hot-reload."""
        if self._watcher is not None:
            return  # already running
        self._watcher = _IdentityFileWatcher(self, bus)
        self._watcher.start()
        logger.info("PromptSynthesizer: identity file watcher started.")

    def stop_watcher(self) -> None:
        """E-31: Stop the polling file watcher."""
        if self._watcher is not None:
            self._watcher.stop()
            self._watcher = None
            logger.info("PromptSynthesizer: identity file watcher stopped.")

    def publish(self, bus: StateBus) -> None:
        """Emit a ``synthesizer_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="prompt_synthesizer",
                event_type="synthesizer_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("PromptSynthesizer.publish failed: %s", exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _build_system(
        self,
        hints: Dict[str, str],
        memory_context: str,
        sensory_hints: Optional[Dict[str, str]] = None,
        emotional_state: Optional[Dict[str, float]] = None,  # E-28
    ) -> str:
        """Assemble the system prompt string from all sections."""
        sections: List[str] = []

        # 1. Identity anchor (highest priority — always first)
        with self._reload_lock:
            identity = self._identity_text
            soul = self._soul_text

        if identity:
            sections.append(identity)

        # 2. Soul / values anchor
        if soul:
            sections.append(soul)

        # 3. E-28: dynamic section reordering based on emotional state
        ordered_keys = self._reorder_sections(list(hints.keys()), emotional_state)

        if ordered_keys:
            hint_lines: List[str] = []
            for key in ordered_keys:
                raw = hints[key]
                line = raw[: self._max_hint_chars]
                hint_lines.append(line)
            sections.append("\n".join(hint_lines))

        # 3b. E-21: sensory layer injected after environment hints
        env_block = self._build_environment_block(sensory_hints or {})
        if env_block:
            sections.append(env_block)

        # 3c. E-29: skaldic vocabulary injection
        if self._skaldic_injection and self._skaldic_vocab:
            skaldic_line = self._inject_skaldic_flavor(self._turn_counter, hints)
            if skaldic_line:
                sections.append(skaldic_line)

        # 4. Memory context
        if memory_context:
            trimmed_mem = memory_context[: self._memory_chars]
            sections.append(f"[Memory context]\n{trimmed_mem}")

        # 4b. Soft response length guidance — model self-regulates; no hard editorial cut.
        sections.append(
            "[Response length] Match your response length to what the question genuinely needs. "
            "There is no hard limit — prefer completeness over brevity for complex or detailed topics. "
            "Keep casual turns naturally short; expand fully when the topic warrants it."
        )

        # 5. S-06: Soul anchor — always last. The most recent content survives eviction longest.
        # Even if the top of the context is erased, Sigrid's identity persists at the bottom.
        with self._reload_lock:
            anchor = self._soul_anchor_text
        if anchor:
            sections.append(anchor)

        combined = "\n\n".join(s.strip() for s in sections if s.strip())

        # Hard total cap — trim to max_system_chars preserving from the start
        if len(combined) > self._max_system_chars:
            combined = combined[: self._max_system_chars]
            logger.debug(
                "PromptSynthesizer: system prompt trimmed to %d chars.",
                self._max_system_chars,
            )

        return combined

    def _reorder_sections(
        self,
        hint_keys: List[str],
        emotional_state: Optional[Dict[str, float]],
    ) -> List[str]:
        """E-28: Produce a context-sensitive ordering of hint keys.

        Default ordering follows _HINT_SECTION_ORDER. Overrides:
          - pad_arousal > 0.7 → wyrd_matrix (emotional state) moves to position 0
          - pad_pleasure < -0.5 → ethics block elevated to position 0
          - Normal: default ordering
        Logs section priorities at DEBUG.
        """
        # Build base ordering (same logic as before)
        ordered: List[str] = []
        for key in _HINT_SECTION_ORDER:
            if key in hint_keys:
                ordered.append(key)
        for key in hint_keys:
            if key not in ordered:
                ordered.append(key)

        if not emotional_state or not ordered:
            return ordered

        pad_arousal = emotional_state.get("pad_arousal", 0.0)
        pad_pleasure = emotional_state.get("pad_pleasure", 0.0)

        if pad_arousal > 0.7 and "wyrd_matrix" in ordered:
            # High arousal: surface emotional state first
            ordered = ["wyrd_matrix"] + [k for k in ordered if k != "wyrd_matrix"]
            logger.debug(
                "PromptSynthesizer: high arousal (%.2f) — wyrd_matrix elevated to position 0.",
                pad_arousal,
            )
        elif pad_pleasure < -0.5 and "ethics" in ordered:
            # Low pleasure / distress: surface ethics/values first
            ordered = ["ethics"] + [k for k in ordered if k != "ethics"]
            logger.debug(
                "PromptSynthesizer: low pleasure (%.2f) — ethics elevated to position 0.",
                pad_pleasure,
            )

        # Log the final priority assignments
        priorities = [
            SectionPriority(
                name=k,
                base_order=list(_HINT_SECTION_ORDER).index(k)
                    if k in _HINT_SECTION_ORDER else len(_HINT_SECTION_ORDER),
                current_order=i,
            )
            for i, k in enumerate(ordered)
        ]
        logger.debug(
            "PromptSynthesizer: section order this turn: %s",
            [(p.name, p.current_order) for p in priorities],
        )
        return ordered

    def _build_environment_block(self, sensory_hints: Dict[str, str]) -> str:
        """E-21: Format selected sensory channels as a 2-line Sensory Layer block.

        Only injected when include_sensory is True and hints are non-empty.
        Each channel appears on its own line: "  Channel: description".
        """
        if not self._include_sensory or not sensory_hints:
            return ""
        lines = ["[Sensory Layer]"]
        for channel, description in sensory_hints.items():
            lines.append(f"  {channel.title()}: {description}")
        return "\n".join(lines)

    # E-29: Skaldic vocabulary ─────────────────────────────────────────────────

    def _load_skaldic_vocab(self, filename: str) -> List[Dict[str, Any]]:
        """Load skaldic_vocabulary.json from the data root. Empty list on failure."""
        path = self._root / filename
        try:
            raw = path.read_text(encoding="utf-8")
            import json as _json
            vocab = _json.loads(raw)
            if isinstance(vocab, list):
                logger.info(
                    "PromptSynthesizer: loaded %d skaldic vocabulary entries.", len(vocab)
                )
                return vocab
        except FileNotFoundError:
            logger.debug("PromptSynthesizer: skaldic_vocabulary.json not found — injection off.")
        except Exception as exc:
            logger.warning("PromptSynthesizer: failed to load skaldic vocab: %s", exc)
        return []

    def _inject_skaldic_flavor(
        self, turn_id: int, hints: Dict[str, str]
    ) -> str:
        """E-29: Deterministically select 2 contextually relevant skaldic words.

        Selection is seeded from turn_id % len(vocab) to avoid full randomness.
        Context tags are inferred from active hint keys.
        Returns a formatted injection line, or empty string if vocab is empty.
        """
        if not self._skaldic_vocab:
            return ""

        # Infer context tags from active modules
        active_tags: set = set()
        if "wyrd_matrix" in hints:
            active_tags.update({"emotion", "spirit", "fate"})
        if "scheduler" in hints:
            active_tags.update({"time", "nature"})
        if "environment_mapper" in hints:
            active_tags.update({"nature", "hearth"})
        if "oracle" in hints:
            active_tags.update({"mystery", "fate", "spirit"})
        if "ethics" in hints:
            active_tags.update({"honor", "duty"})
        if not active_tags:
            active_tags = {"general"}

        # Prefer contextually matched entries, fall back to any
        matched = [
            entry for entry in self._skaldic_vocab
            if set(entry.get("context_tags", [])) & active_tags
        ]
        pool = matched if matched else self._skaldic_vocab

        # Seeded selection — deterministic per turn
        n = len(pool)
        idx1 = (turn_id * 7) % n
        idx2 = (turn_id * 13 + 5) % n
        selected = [pool[idx1]]
        if idx2 != idx1 and len(pool) > 1:
            selected.append(pool[idx2])

        words = ", ".join(
            f"{e['word']} ({e['meaning']})" for e in selected
        )
        return f"[Skaldic Voice] Weave these into your voice today: {words}"

    # E-30: Token counting ─────────────────────────────────────────────────────

    def _count_tokens(self, text: str) -> int:
        """E-30: Estimate token count using litellm.token_counter() if available.

        Falls back to len(text)//4 (rough 4-chars-per-token approximation)
        when litellm is unavailable or raises. Logs DEBUG on fallback mode.
        """
        try:
            import litellm  # type: ignore
            count = litellm.token_counter(model="gpt-3.5-turbo", text=text)
            if self._token_count_fallback:
                self._token_count_fallback = False
            return int(count)
        except Exception:
            if not self._token_count_fallback:
                logger.debug(
                    "PromptSynthesizer: litellm token_counter unavailable — "
                    "using char estimate (len//4)."
                )
                self._token_count_fallback = True
            return len(text) // 4

    # S-04: Hard token cap ────────────────────────────────────────────────────

    def _truncate_to_token_cap(self, text: str, max_tokens: int) -> str:
        """S-04: Trim *text* from the end until its token count is under *max_tokens*.

        Identity and soul anchors sit at the top of the assembled system string
        (placed first in _build_system), so trimming from the end preserves them.
        Operates by binary-search on character length to find the trim point quickly.

        Never raises; returns *text* unchanged if already under budget.
        """
        if self._count_tokens(text) <= max_tokens:
            return text

        # Estimate char target from token budget, then binary-refine
        target_chars = max_tokens * 4  # conservative start (avg 4 chars/token)
        lo, hi = 0, len(text)
        for _ in range(12):  # at most 12 iterations — enough for any realistic string
            mid = (lo + hi) // 2
            if self._count_tokens(text[:mid]) <= max_tokens:
                lo = mid
            else:
                hi = mid

        trimmed = text[:lo]
        logger.warning(
            "PromptSynthesizer: S-04 token cap enforced — trimmed %d → %d chars "
            "(~%d tokens budget).",
            len(text), len(trimmed), max_tokens,
        )
        return trimmed

    # S-05: Soul anchor re-injection ──────────────────────────────────────────

    def _build_soul_anchor_block(self) -> str:
        """S-05: Build a compact soul anchor block for context-overflow recovery.

        Returns the first _SOUL_ANCHOR_IDENTITY_CHARS chars of identity text
        plus the first _SOUL_ANCHOR_SOUL_CHARS chars of soul text, combined into
        a small (~800-char) anchor. Injected at the top of the system prompt when
        the context window is approaching overflow so the model always has at least
        a condensed version of who Sigrid is.

        Frigg's needle and thread — even when the tapestry is cut short by the
        limits of Fate, the warp threads that define the pattern remain.
        """
        with self._reload_lock:
            identity_anchor = self._identity_text[:_SOUL_ANCHOR_IDENTITY_CHARS]
            soul_anchor = self._soul_text[:_SOUL_ANCHOR_SOUL_CHARS]

        parts = []
        if identity_anchor:
            parts.append(f"[IDENTITY ANCHOR — context near limit]\n{identity_anchor}")
        if soul_anchor:
            parts.append(f"[SOUL ANCHOR]\n{soul_anchor}")
        return "\n\n".join(parts)

    def _publish_context_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish a context-guard event on StateBus if bus is available. Never raises."""
        if self._bus is None:
            return
        try:
            event = StateEvent(
                source_module="prompt_synthesizer",
                event_type=event_type,
                payload=payload,
            )
            self._bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.debug("PromptSynthesizer: could not publish %s event: %s", event_type, exc)

    def _load_text(self, filename: str, max_chars: int) -> str:
        """Load and trim a text file from the data root."""
        path = self._root / filename
        try:
            raw = path.read_text(encoding="utf-8")
            text = raw.strip()
            if len(text) > max_chars:
                # Trim at a paragraph break near the limit to avoid mid-sentence cuts
                trimmed = text[:max_chars]
                last_break = trimmed.rfind("\n\n")
                if last_break > max_chars // 2:
                    trimmed = trimmed[:last_break]
                text = trimmed
            logger.info("PromptSynthesizer: loaded '%s' (%d chars).", filename, len(text))
            return text
        except FileNotFoundError:
            logger.warning("PromptSynthesizer: '%s' not found in %s.", filename, self._root)
            self._degraded = True
            return ""
        except Exception as exc:
            logger.warning("PromptSynthesizer: failed to load '%s': %s", filename, exc)
            self._degraded = True
            return ""

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "PromptSynthesizer":
        """Construct from a config dict.

        Reads keys under ``prompt_synthesizer``::

          data_root            (str,  default "data")
          identity_file        (str,  default "core_identity.md")
          soul_file            (str,  default "SOUL.md")
          identity_chars       (int,  default 2000)
          soul_chars           (int,  default 400)
          memory_chars         (int,  default 800)
          max_system_chars     (int,  default 6000)
          max_hint_chars       (int,  default 200)
          include_sensory      (bool, default True)
          skaldic_injection    (bool, default True)   E-29
          skaldic_vocab_file   (str,  default "skaldic_vocabulary.json")  E-29
          max_context_tokens   (int,  default 104858)  S-04
          overflow_threshold_ratio (float, default 0.80) S-05
          critical_threshold_ratio (float, default 0.90) S-06
          soul_anchor_enabled  (bool, default True)   S-05
          soul_anchor_file     (str,  default "soul_anchor.md")  S-06
        """
        cfg: Dict[str, Any] = config.get("prompt_synthesizer", {})
        return cls(
            data_root=str(cfg.get("data_root", _DEFAULT_DATA_ROOT)),
            identity_file=str(cfg.get("identity_file", _DEFAULT_IDENTITY_FILE)),
            soul_file=str(cfg.get("soul_file", _DEFAULT_SOUL_FILE)),
            soul_anchor_file=str(cfg.get("soul_anchor_file", _DEFAULT_SOUL_ANCHOR_FILE)),  # S-06
            identity_chars=int(cfg.get("identity_chars", _DEFAULT_IDENTITY_CHARS)),
            soul_chars=int(cfg.get("soul_chars", _DEFAULT_SOUL_CHARS)),
            memory_chars=int(cfg.get("memory_chars", _DEFAULT_MEMORY_CHARS)),
            max_system_chars=int(cfg.get("max_system_chars", _DEFAULT_MAX_SYSTEM_CHARS)),
            max_hint_chars=int(cfg.get("max_hint_chars", _DEFAULT_MAX_HINT_CHARS)),
            include_sensory=bool(cfg.get("include_sensory", True)),
            skaldic_injection=bool(cfg.get("skaldic_injection", True)),      # E-29
            skaldic_vocab_file=str(cfg.get("skaldic_vocab_file", "skaldic_vocabulary.json")),  # E-29
            max_context_tokens=int(cfg.get("max_context_tokens", _DEFAULT_MAX_CONTEXT_TOKENS)),  # S-04
            overflow_threshold_ratio=float(cfg.get("overflow_threshold_ratio", _DEFAULT_OVERFLOW_THRESHOLD_RATIO)),  # S-05
            critical_threshold_ratio=float(cfg.get("critical_threshold_ratio", _DEFAULT_CRITICAL_THRESHOLD_RATIO)),  # S-06
            soul_anchor_enabled=bool(cfg.get("soul_anchor_enabled", True)),  # S-05
        )


# ─── E-31: Identity File Watcher ─────────────────────────────────────────────


class _IdentityFileWatcher:
    """E-31: Polling-based file watcher for core_identity.md and SOUL.md.

    Windows-compatible (no inotify/watchdog dependency).
    Polls every poll_interval_s; on mtime change calls synth.reload_identity()
    and publishes persona.identity_reloaded to the StateBus.
    """

    _DEFAULT_POLL_INTERVAL_S: float = 5.0

    def __init__(
        self,
        synth: PromptSynthesizer,
        bus: Optional[StateBus] = None,
        poll_interval_s: float = _DEFAULT_POLL_INTERVAL_S,
    ) -> None:
        self._synth = synth
        self._bus = bus
        self._poll_interval = poll_interval_s
        self._mtimes: Dict[str, float] = {}
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        # Snapshot initial mtimes
        self._snapshot_mtimes()

    def start(self) -> None:
        """Start the polling daemon thread. Idempotent."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="IdentityFileWatcher"
        )
        self._thread.start()

    def stop(self) -> None:
        """Signal the daemon thread to stop."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=self._poll_interval + 1.0)

    def _run_loop(self) -> None:
        while not self._stop_event.wait(self._poll_interval):
            self._check_files()

    def _check_files(self) -> None:
        """Check identity files for mtime changes; reload if changed."""
        root = self._synth._root
        targets = {
            self._synth._identity_file: root / self._synth._identity_file,
            self._synth._soul_file: root / self._synth._soul_file,
        }
        changed_files: List[str] = []
        for name, path in targets.items():
            try:
                mtime = path.stat().st_mtime
            except FileNotFoundError:
                continue
            old_mtime = self._mtimes.get(name, 0.0)
            if mtime != old_mtime:
                self._mtimes[name] = mtime
                changed_files.append(name)

        if changed_files:
            logger.info(
                "PromptSynthesizer: identity file(s) changed — reloading: %s",
                changed_files,
            )
            self._synth.reload_identity()
            self._publish_reload(changed_files)

    def _snapshot_mtimes(self) -> None:
        root = self._synth._root
        for name in [self._synth._identity_file, self._synth._soul_file]:
            path = root / name
            try:
                self._mtimes[name] = path.stat().st_mtime
            except FileNotFoundError:
                self._mtimes[name] = 0.0

    def _publish_reload(self, changed_files: List[str]) -> None:
        """Publish persona.identity_reloaded StateEvent to the bus if available."""
        if self._bus is None:
            return
        try:
            event = StateEvent(
                source_module="prompt_synthesizer",
                event_type="persona.identity_reloaded",
                payload={"changed_files": changed_files},
            )
            self._bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("_IdentityFileWatcher._publish_reload failed: %s", exc)


# ─── Singleton ────────────────────────────────────────────────────────────────

_PROMPT_SYNTHESIZER: Optional[PromptSynthesizer] = None


def init_prompt_synthesizer_from_config(config: Dict[str, Any]) -> PromptSynthesizer:
    """Initialise the global PromptSynthesizer. Idempotent."""
    global _PROMPT_SYNTHESIZER
    if _PROMPT_SYNTHESIZER is None:
        _PROMPT_SYNTHESIZER = PromptSynthesizer.from_config(config)
        logger.info(
            "PromptSynthesizer initialised (identity=%s, soul=%s, degraded=%s).",
            bool(_PROMPT_SYNTHESIZER._identity_text),
            bool(_PROMPT_SYNTHESIZER._soul_text),
            _PROMPT_SYNTHESIZER._degraded,
        )
    return _PROMPT_SYNTHESIZER


def get_prompt_synthesizer() -> PromptSynthesizer:
    """Return the global PromptSynthesizer.

    Raises RuntimeError if not yet initialised.
    """
    if _PROMPT_SYNTHESIZER is None:
        raise RuntimeError(
            "PromptSynthesizer not initialised — call init_prompt_synthesizer_from_config() first."
        )
    return _PROMPT_SYNTHESIZER
