"""Owner voiceprint set management for VoiceTrust.

This module keeps VoiceTrust independent from STT and focused on
curated owner verification. It supports multiple enrollment samples per owner
and a simple centroid-style aggregate embedding for the current mainline.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import numpy as np


@dataclass
class OwnerSample:
    path: str
    embedding_file: str


@dataclass
class OwnerProfile:
    speaker_id: str
    aggregate_embedding_file: str
    samples: List[OwnerSample]

    def to_dict(self) -> dict:
        return {
            "speaker_id": self.speaker_id,
            "aggregate_embedding_file": self.aggregate_embedding_file,
            "samples": [
                {"path": s.path, "embedding_file": s.embedding_file}
                for s in self.samples
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OwnerProfile":
        return cls(
            speaker_id=data["speaker_id"],
            aggregate_embedding_file=data["aggregate_embedding_file"],
            samples=[OwnerSample(**s) for s in data.get("samples", [])],
        )


class OwnerProfileStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def speaker_dir(self, speaker_id: str) -> Path:
        return self.root / speaker_id

    def profile_path(self, speaker_id: str) -> Path:
        return self.speaker_dir(speaker_id) / "profile.json"

    def aggregate_path(self, speaker_id: str) -> Path:
        return self.speaker_dir(speaker_id) / "aggregate.npy"

    def sample_embedding_path(self, speaker_id: str, sample_index: int) -> Path:
        return self.speaker_dir(speaker_id) / f"sample_{sample_index:03d}.npy"

    def load_profile(self, speaker_id: str) -> Optional[OwnerProfile]:
        path = self.profile_path(speaker_id)
        if not path.exists():
            return None
        return OwnerProfile.from_dict(json.loads(path.read_text()))

    def save_profile(self, profile: OwnerProfile) -> None:
        sdir = self.speaker_dir(profile.speaker_id)
        sdir.mkdir(parents=True, exist_ok=True)
        self.profile_path(profile.speaker_id).write_text(
            json.dumps(profile.to_dict(), indent=2, ensure_ascii=False)
        )

    def append_sample(self, speaker_id: str, audio_path: str, embedding: np.ndarray) -> OwnerProfile:
        existing = self.load_profile(speaker_id)
        sdir = self.speaker_dir(speaker_id)
        sdir.mkdir(parents=True, exist_ok=True)

        samples = list(existing.samples) if existing else []
        sample_index = len(samples) + 1
        emb_path = self.sample_embedding_path(speaker_id, sample_index)
        np.save(emb_path, embedding)
        samples.append(OwnerSample(path=str(audio_path), embedding_file=emb_path.name))

        vectors = []
        for sample in samples:
            vectors.append(np.load(sdir / sample.embedding_file))
        aggregate = np.mean(np.stack(vectors, axis=0), axis=0)
        agg_path = self.aggregate_path(speaker_id)
        np.save(agg_path, aggregate)

        profile = OwnerProfile(
            speaker_id=speaker_id,
            aggregate_embedding_file=agg_path.name,
            samples=samples,
        )
        self.save_profile(profile)
        return profile
