"""Bundled, pinned SAR key registry snapshot and lifecycle classification.

This module replaces the previous stale, unclassified flat key list in
``keys/sar-keys.json`` (``sar-prod-ed25519-01/-02/-03`` only, no lifecycle
data). It loads the bundled, refreshed copy of the canonical public registry
(``keys/sar-keys.json``, now the full 8-entry canonical document with
lifecycle fields) and derives a lifecycle classification per key, so
verification can distinguish:

NOTE: this module is intentionally near-identical to
``defaultsettle-cli``'s ``defaultsettle/registry_snapshot.py`` (same design,
copied rather than imported cross-repository to avoid runtime coupling
between independently-releasable artifacts). Keep changes to the
classification logic mirrored between the two if it evolves.

  1. Cryptographic signature validity (unaffected by any of this — a
     retired or duplicate key's signature still verifies if the bytes match).
  2. Whether the key is present in this bundled snapshot at all.
  3. The key's lifecycle status in that snapshot (``active`` / ``retired`` /
     ``reserved`` / statusless-legacy / ``documented_non_operational_duplicate``).
  4. Whether the key is scoped to the SAR settlement-witness signing profile
     (``use: sar_settlement_witness_signing``, or no ``use`` field at all —
     the three original legacy kids that predate the ``use`` field).
  5. Whether the key currently counts as the trusted *current production*
     signer, as opposed to a historically verifiable but no-longer-active one.

Doctrine citations (state/DECISIONS.md in the morpheus repo):
  - D4 (2026-07-11): registry statuses are facts only
    (generated/reserved/active/retired); retired -> active is illegal.
  - D4 clarification, shared-public-key identity governance (2026-07-12):
    a key sharing public-key bytes with another kid without independent
    operational evidence of its own is classified
    ``documented_non_operational_duplicate`` — internal-only, never
    represented as an independently active/operational signer.
  - D7 (2026-07-12): retirement never removes historical verifiability.

No policy is invented here: the ``documented_non_operational_duplicate``
classification for a given kid is read directly out of that kid's own
registry ``note`` field (``classification=...``), which is itself the
Keith-approved D4-clarification text already present in the canonical
registry — this module transcribes it, it does not decide it.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Any, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)
DEFAULT_SNAPSHOT_PATH = os.path.join(_SKILL_ROOT, "keys", "sar-keys.json")

# Provenance of the bundled snapshot. Recorded, not recomputed: this is what
# was fetched/copied and independently confirmed byte-identical across
# /home/ubuntu/settlement-witness/sar-keys.json, /var/www/html/.well-known/
# sar-keys.json, and https://defaultverifier.com/.well-known/sar-keys.json
# on 2026-07-19.
SNAPSHOT_SOURCE = "https://defaultverifier.com/.well-known/sar-keys.json"
SNAPSHOT_DATE = "2026-07-19"
SNAPSHOT_SHA256 = (
    "2da5285f458af9f3369e5baddd953164834d961161c87c9594b823ce251a4f6b"
)

# The only ``use`` value this verifier trusts for SAR v0.1 settlement-witness
# receipts. Keys registered for a different profile (SAR-402 recording
# attribution, continuity-evaluation receipts) are a different signing
# authority entirely and must never be accepted here, regardless of their
# lifecycle status.
SAR_SETTLEMENT_WITNESS_USE = "sar_settlement_witness_signing"

# The legacy kids that predate the registry's ``use`` field. Their scope was
# always SAR v0.1 settlement-witness signing; treated as in-profile only for
# this reason, not because a missing ``use`` field is assumed to mean
# "any profile".
_LEGACY_NO_USE_FIELD_KIDS = frozenset(
    {"sar-prod-ed25519-01", "sar-prod-ed25519-02", "sar-prod-ed25519-03"}
)

_DUPLICATE_CLASSIFICATION_RE = re.compile(r"classification=([a-zA-Z0-9_]+)")


class RegistrySnapshotError(RuntimeError):
    """Raised when the bundled registry snapshot is missing or tampered."""


def _b64url_decode_flexible(s: str) -> bytes:
    import base64

    s = (s or "").strip()
    pad = (-len(s)) % 4
    return base64.urlsafe_b64decode((s + ("=" * pad)).encode("utf-8"))


def load_snapshot_raw(path: str = DEFAULT_SNAPSHOT_PATH) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as exc:
        raise RegistrySnapshotError(f"cannot read bundled registry snapshot: {exc}") from exc


def snapshot_sha256(path: str = DEFAULT_SNAPSHOT_PATH) -> str:
    return hashlib.sha256(load_snapshot_raw(path)).hexdigest()


def _pubkey_hash(entry: dict) -> Optional[str]:
    """Normalized public-key byte hash, independent of encoding (x vs public_key_hex)."""
    x = entry.get("x")
    if isinstance(x, str) and x.strip():
        try:
            raw = _b64url_decode_flexible(x)
        except Exception:
            return None
        return hashlib.sha256(raw).hexdigest()
    hexkey = entry.get("public_key_hex")
    if isinstance(hexkey, str) and hexkey.strip():
        try:
            raw = bytes.fromhex(hexkey.strip())
        except ValueError:
            return None
        return hashlib.sha256(raw).hexdigest()
    return None


class KeyClassification:
    __slots__ = (
        "kid",
        "present",
        "status",
        "use",
        "profile_ok",
        "duplicate_classification",
        "pubkey_hash",
        "note",
    )

    def __init__(
        self,
        kid: str,
        present: bool,
        status: Optional[str],
        use: Optional[str],
        profile_ok: bool,
        duplicate_classification: Optional[str],
        pubkey_hash: Optional[str],
        note: Optional[str],
    ) -> None:
        self.kid = kid
        self.present = present
        self.status = status
        self.use = use
        self.profile_ok = profile_ok
        self.duplicate_classification = duplicate_classification
        self.pubkey_hash = pubkey_hash
        self.note = note

    @property
    def is_documented_non_operational_duplicate(self) -> bool:
        return self.duplicate_classification == "documented_non_operational_duplicate"

    @property
    def is_current_production_signer(self) -> bool:
        """Trusted as the CURRENT active production signer for new claims."""
        return bool(
            self.present
            and self.profile_ok
            and self.status == "active"
            and not self.is_documented_non_operational_duplicate
        )

    @property
    def is_historically_verifiable(self) -> bool:
        """Eligible for historical verification (signature check still runs
        regardless — this only governs how the result should be labeled)."""
        if not (self.present and self.profile_ok):
            return False
        if self.is_documented_non_operational_duplicate:
            # -02's bytes are historically explained via -03, not itself.
            return False
        # active, retired, or statusless-legacy (created pre-D4 governance)
        # all remain historically verifiable; only reserved keys have never
        # signed anything yet.
        return self.status in ("active", "retired", None)

    @property
    def lifecycle_label(self) -> str:
        if not self.present:
            return "unknown"
        if not self.profile_ok:
            return "wrong_profile"
        if self.is_documented_non_operational_duplicate:
            return "documented_non_operational_duplicate"
        if self.status is None:
            return "legacy_unclassified"
        return self.status  # active / retired / reserved


class RegistrySnapshot:
    def __init__(self, path: str = DEFAULT_SNAPSHOT_PATH) -> None:
        self.path = path
        raw = load_snapshot_raw(path)
        self.raw_sha256 = hashlib.sha256(raw).hexdigest()
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise RegistrySnapshotError(f"bundled registry snapshot is not valid JSON: {exc}") from exc
        if not isinstance(doc, dict) or not isinstance(doc.get("keys"), list):
            raise RegistrySnapshotError("bundled registry snapshot has unexpected shape")
        self._by_kid: dict[str, dict] = {}
        for entry in doc["keys"]:
            kid = entry.get("kid")
            if isinstance(kid, str) and kid:
                self._by_kid[kid] = entry

    def verify_pinned_hash(self, expected: str = SNAPSHOT_SHA256) -> None:
        if self.raw_sha256 != expected:
            raise RegistrySnapshotError(
                "bundled registry snapshot does not match its pinned SHA-256 "
                f"(expected {expected}, got {self.raw_sha256}); refusing to "
                "verify against a snapshot that may have been tampered with "
                "or is out of sync with its recorded provenance"
            )

    def get_public_key_bytes(self, kid: str) -> Optional[bytes]:
        entry = self._by_kid.get(kid)
        if entry is None:
            return None
        x = entry.get("x")
        if isinstance(x, str) and x.strip():
            return _b64url_decode_flexible(x)
        hexkey = entry.get("public_key_hex")
        if isinstance(hexkey, str) and hexkey.strip():
            return bytes.fromhex(hexkey.strip())
        return None

    def classify(self, kid: str) -> KeyClassification:
        entry = self._by_kid.get(kid)
        if entry is None:
            return KeyClassification(
                kid=kid,
                present=False,
                status=None,
                use=None,
                profile_ok=False,
                duplicate_classification=None,
                pubkey_hash=None,
                note=None,
            )
        status = entry.get("status")
        use = entry.get("use")
        note = entry.get("note")
        if use is None and kid in _LEGACY_NO_USE_FIELD_KIDS:
            profile_ok = True
        else:
            profile_ok = use == SAR_SETTLEMENT_WITNESS_USE
        dup_classification = None
        if isinstance(note, str):
            m = _DUPLICATE_CLASSIFICATION_RE.search(note)
            if m:
                dup_classification = m.group(1)
        return KeyClassification(
            kid=kid,
            present=True,
            status=status,
            use=use,
            profile_ok=profile_ok,
            duplicate_classification=dup_classification,
            pubkey_hash=_pubkey_hash(entry),
            note=note,
        )


def load_default_snapshot() -> RegistrySnapshot:
    """Load the registry snapshot, honoring ``SAR_KEYS_REGISTRY_PATH`` if set
    (matching the skill's pre-existing override variable). When overridden,
    the pinned-hash check is skipped, since an intentionally different
    registry file (e.g. a test fixture) will not match the bundled hash by
    design; the bundled default path always enforces the pinned hash."""
    override = os.environ.get("SAR_KEYS_REGISTRY_PATH")
    if override:
        return RegistrySnapshot(override)
    snap = RegistrySnapshot(DEFAULT_SNAPSHOT_PATH)
    snap.verify_pinned_hash()
    return snap
