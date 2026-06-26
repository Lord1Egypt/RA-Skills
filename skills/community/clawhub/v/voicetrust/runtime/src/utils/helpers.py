"""Utility functions for voice trust."""
import io
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import torch
import yaml
import soundfile as sf


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("voicetrust")


def load_config(config_path: str) -> Dict[str, Any]:
    """Load YAML configuration."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def save_results(results: Dict[str, Any], output_path: str):
    """Save results to JSON."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)


def compute_eer(
    scores: np.ndarray, labels: np.ndarray
) -> tuple:
    """Compute Equal Error Rate."""
    sorted_indices = np.argsort(scores)
    sorted_scores = scores[sorted_indices]
    sorted_labels = labels[sorted_indices]

    n_positive = np.sum(labels == 1)
    n_negative = np.sum(labels == 0)

    fnrs = np.cumsum(sorted_labels) / n_positive
    fprs = 1 - np.cumsum(1 - sorted_labels) / n_negative

    eer_idx = np.argmin(np.abs(fnrs - fprs))
    eer = (fnrs[eer_idx] + fprs[eer_idx]) / 2
    threshold = sorted_scores[eer_idx]

    return eer, threshold


def compute_tDCF(
    scores: np.ndarray,
    labels: np.ndarray,
    p_target: float = 0.01,
    c_miss: float = 1.0,
    c_fa: float = 1.0,
) -> float:
    """Compute normalized tandem detection cost function."""
    thresholds = np.linspace(scores.min(), scores.max(), 1000)
    min_tdcf = float("inf")

    for threshold in thresholds:
        fa = np.sum((scores >= threshold) & (labels == 0)) / np.sum(labels == 0)
        miss = np.sum((scores < threshold) & (labels == 1)) / np.sum(labels == 1)

        tdcf = c_miss * p_target * miss + c_fa * (1 - p_target) * fa
        tdcf /= min(c_miss * p_target, c_fa * (1 - p_target))

        if tdcf < min_tdcf:
            min_tdcf = tdcf

    return min_tdcf


def get_device(prefer_cuda: bool = True) -> str:
    """Get best available device."""
    if prefer_cuda and torch.cuda.is_available():
        return "cuda"
    return "cpu"


def count_parameters(model: torch.nn.Module) -> int:
    """Count trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


class AverageMeter:
    """Computes and stores the average and current value."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def ensure_dir(path: str) -> Path:
    """Ensure directory exists."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _load_audio_with_soundfile(audio_path: str) -> Tuple[np.ndarray, int]:
    data, sample_rate = sf.read(audio_path, always_2d=False)
    if isinstance(data, tuple):
        raise RuntimeError("Unexpected soundfile output tuple")
    data = np.asarray(data, dtype=np.float32)
    return data, sample_rate


def _load_audio_with_ffmpeg(audio_path: str, sample_rate: int) -> np.ndarray:
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-v",
        "error",
        "-i",
        audio_path,
        "-f",
        "wav",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "pipe:1",
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    with sf.SoundFile(io.BytesIO(proc.stdout)) as f:
        data = f.read(dtype="float32", always_2d=False)
        return np.asarray(data, dtype=np.float32)


def load_audio_waveform(audio_path: str, target_sample_rate: int = 16000) -> Tuple[torch.Tensor, int]:
    """Stable audio loader that avoids torchaudio/torchcodec runtime fragility.

    Strategy:
    1. Try soundfile directly.
    2. If unsupported or decode fails, fall back to ffmpeg -> wav pipe.
    3. Convert to mono and resample with librosa when needed.
    """
    try:
        waveform_np, sample_rate = _load_audio_with_soundfile(audio_path)
    except Exception:
        waveform_np = _load_audio_with_ffmpeg(audio_path, target_sample_rate)
        sample_rate = target_sample_rate

    if waveform_np.ndim == 2:
        waveform_np = waveform_np.mean(axis=1)

    if sample_rate != target_sample_rate:
        import librosa
        waveform_np = librosa.resample(
            waveform_np,
            orig_sr=sample_rate,
            target_sr=target_sample_rate,
        )
        sample_rate = target_sample_rate

    waveform_np = np.asarray(waveform_np, dtype=np.float32)
    if waveform_np.ndim != 1:
        waveform_np = waveform_np.reshape(-1)

    waveform = torch.from_numpy(waveform_np).unsqueeze(0)
    return waveform, sample_rate
