"""Audio data loading and augmentation for voice trust training."""
import torch
from torch.utils.data import Dataset, DataLoader
import torchaudio
import numpy as np
import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class AudioDataset(Dataset):
    """Dataset for audio files with labels."""

    def __init__(
        self,
        manifest_path: str,
        sample_rate: int = 16000,
        max_duration: float = 10.0,
        augment: bool = False,
        augment_config: Optional[Dict] = None,
    ):
        self.sample_rate = sample_rate
        self.max_duration = max_duration
        self.augment = augment
        self.augment_config = augment_config or {}

        # Load manifest
        with open(manifest_path, "r") as f:
            self.samples = [json.loads(line) for line in f]

        # Filter invalid samples
        self.samples = [
            s for s in self.samples
            if Path(s["audio_path"]).exists()
        ]

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        sample = self.samples[idx]

        # Load audio
        waveform, sr = torchaudio.load(sample["audio_path"])

        # Convert to mono
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        # Resample if needed
        if sr != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
            waveform = resampler(waveform)

        # Truncate or pad to max_duration
        max_samples = int(self.sample_rate * self.max_duration)
        if waveform.shape[1] > max_samples:
            # Random crop
            start = random.randint(0, waveform.shape[1] - max_samples)
            waveform = waveform[:, start:start + max_samples]
        else:
            # Pad
            padding = max_samples - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding))

        # Apply augmentations
        if self.augment:
            waveform = self._augment(waveform)

        # Get label
        label = sample.get("label", 0)  # 0 = bonafide, 1 = spoof

        return waveform.squeeze(0), label

    def _augment(self, waveform: torch.Tensor) -> torch.Tensor:
        """Apply augmentations."""
        config = self.augment_config

        # Add noise
        if random.random() < config.get("noise", {}).get("prob", 0.0):
            snr_range = config.get("noise", {}).get("snr_range", [5, 20])
            snr = random.uniform(*snr_range)
            noise = torch.randn_like(waveform)
            signal_power = waveform.pow(2).mean()
            noise_power = noise.pow(2).mean()
            snr_linear = 10 ** (snr / 10)
            noise_scale = (signal_power / noise_power / snr_linear).sqrt()
            waveform = waveform + noise_scale * noise

        return waveform


class SpeakerDataset(Dataset):
    """Dataset for speaker verification training."""

    def __init__(
        self,
        manifest_path: str,
        sample_rate: int = 16000,
        max_duration: float = 4.0,
    ):
        self.sample_rate = sample_rate
        self.max_duration = max_duration

        # Load manifest
        with open(manifest_path, "r") as f:
            self.samples = [json.loads(line) for line in f]

        # Group by speaker
        self.speaker_to_samples = {}
        for s in self.samples:
            spk = s.get("speaker_id", "unknown")
            if spk not in self.speaker_to_samples:
                self.speaker_to_samples[spk] = []
            self.speaker_to_samples[spk].append(s)

        self.speakers = list(self.speaker_to_samples.keys())

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        sample = self.samples[idx]

        # Load audio
        waveform, sr = torchaudio.load(sample["audio_path"])

        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        if sr != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
            waveform = resampler(waveform)

        # Truncate or pad
        max_samples = int(self.sample_rate * self.max_duration)
        if waveform.shape[1] > max_samples:
            start = random.randint(0, waveform.shape[1] - max_samples)
            waveform = waveform[:, start:start + max_samples]
        else:
            padding = max_samples - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding))

        speaker_id = sample.get("speaker_id", "unknown")
        speaker_idx = self.speakers.index(speaker_id)

        return waveform.squeeze(0), speaker_idx

    def get_triplet(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Get a triplet (anchor, positive, negative) for training."""
        # Select anchor speaker
        anchor_spk = random.choice(self.speakers)

        # Get anchor and positive from same speaker
        anchor_sample, pos_sample = random.sample(
            self.speaker_to_samples[anchor_spk], 2
        )

        # Get negative from different speaker
        neg_spk = random.choice([s for s in self.speakers if s != anchor_spk])
        neg_sample = random.choice(self.speaker_to_samples[neg_spk])

        anchor, _ = self[self.samples.index(anchor_sample)]
        positive, _ = self[self.samples.index(pos_sample)]
        negative, _ = self[self.samples.index(neg_sample)]

        return anchor, positive, negative


def collate_fn(batch: List[Tuple]) -> Tuple[torch.Tensor, torch.Tensor]:
    """Collate function for DataLoader."""
    waveforms, labels = zip(*batch)
    waveforms = torch.stack(waveforms)
    labels = torch.tensor(labels)
    return waveforms, labels


def create_dataloader(
    manifest_path: str,
    batch_size: int = 32,
    shuffle: bool = True,
    num_workers: int = 4,
    augment: bool = False,
    **kwargs
) -> DataLoader:
    """Create a DataLoader."""
    dataset = AudioDataset(
        manifest_path=manifest_path,
        augment=augment,
        **kwargs
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=collate_fn,
        pin_memory=True,
    )
