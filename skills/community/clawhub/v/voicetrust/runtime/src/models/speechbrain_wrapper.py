"""SpeechBrain model wrapper for speaker verification and anti-spoofing.

Uses pre-trained models from SpeechBrain hub:
- ECAPA-TDNN for speaker verification (trained on VoxCeleb)
- Anti-spoofing model for deepfake detection
"""
import torch
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple, Dict, List
from pathlib import Path
import warnings

from utils.helpers import load_audio_waveform

# Compatibility shim: some newer torchaudio builds removed list_audio_backends(),
# while current SpeechBrain versions still expect it during import/runtime checks.
if not hasattr(torch, "__dict__"):
    pass
else:
    try:
        import torchaudio  # type: ignore
        if not hasattr(torchaudio, "list_audio_backends"):
            def _list_audio_backends() -> list[str]:
                try:
                    import soundfile  # noqa: F401
                    return ["soundfile"]
                except Exception:
                    return []
            torchaudio.list_audio_backends = _list_audio_backends  # type: ignore[attr-defined]
    except Exception:
        torchaudio = None  # noqa: F841

try:
    try:
        from speechbrain.inference import EncoderClassifier, SpeakerRecognition
    except ImportError:
        from speechbrain.pretrained import EncoderClassifier, SpeakerRecognition
    from speechbrain.utils.metric_stats import EER
    SPEECHBRAIN_AVAILABLE = True
except ImportError:
    SPEECHBRAIN_AVAILABLE = False
    warnings.warn("SpeechBrain not installed. Speaker verification will not work.")


class SpeechBrainSpeakerVerifier:
    """Speaker verification using local SpeechBrain ECAPA-TDNN assets."""

    LOCAL_MODEL_DIRS = {
        "ecapa_voxceleb": Path(__file__).resolve().parent.parent.parent / "assets" / "models" / "ecapa_voxceleb",
    }
    REQUIRED_MODEL_FILES = [
        "hyperparams.yaml",
        "classifier.ckpt",
        "embedding_model.ckpt",
        "label_encoder.ckpt",
        "mean_var_norm_emb.ckpt",
    ]

    def __init__(
        self,
        model_name: str = "ecapa_voxceleb",
        device: str = "cpu",
        verification_threshold: float = 0.25,
        savedir: Optional[str] = None,
    ):
        if not SPEECHBRAIN_AVAILABLE:
            raise RuntimeError("SpeechBrain is required. Install with: pip install speechbrain")

        self.device = device
        self.verification_threshold = verification_threshold
        self.model_name = model_name
        self.savedir = Path(savedir) if savedir else self.LOCAL_MODEL_DIRS.get(model_name)

        if self.savedir is None:
            raise ValueError(f"Unsupported local speaker model: {model_name}")
        if not self.savedir.exists():
            raise FileNotFoundError(
                f"Local SpeechBrain model asset directory not found: {self.savedir}\n"
                f"Prepare the local assets first with: python ../scripts/ensure_models.py"
            )

        missing = [name for name in self.REQUIRED_MODEL_FILES if not (self.savedir / name).exists()]
        if missing:
            raise FileNotFoundError(
                "Local SpeechBrain model assets are incomplete.\n"
                f"Missing: {', '.join(missing)}\n"
                f"Model dir: {self.savedir}\n"
                f"Run: python ../scripts/ensure_models.py"
            )

        print(f"Loading local speaker verification model: {self.savedir}")

        try:
            self.classifier = SpeakerRecognition.from_hparams(
                source=str(self.savedir),
                savedir=str(self.savedir),
                run_opts={"device": device},
            )
            print("Speaker verification model loaded successfully")
        except Exception as e:
            print(f"Error loading local model: {e}")
            raise

        self.enrolled_embeddings: Dict[str, torch.Tensor] = {}

    def _load_signal(self, audio_path: str) -> torch.Tensor:
        waveform, _sample_rate = load_audio_waveform(audio_path, target_sample_rate=16000)
        return waveform.to(self.device)

    def enroll(self, speaker_id: str, audio_path: str) -> np.ndarray:
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        signal = self._load_signal(audio_path)
        embedding = self.classifier.encode_batch(signal)
        self.enrolled_embeddings[speaker_id] = embedding.cpu()
        return embedding.squeeze().cpu().numpy()

    def enroll_embedding(self, speaker_id: str, embedding: np.ndarray) -> None:
        self.enrolled_embeddings[speaker_id] = torch.from_numpy(embedding).unsqueeze(0)

    def verify(self, audio_path: str, speaker_id: str) -> Tuple[float, bool]:
        if speaker_id not in self.enrolled_embeddings:
            raise ValueError(f"Speaker '{speaker_id}' not enrolled. Enroll first.")
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        signal = self._load_signal(audio_path)
        test_embedding = self.classifier.encode_batch(signal)
        enrolled_embedding = self.enrolled_embeddings[speaker_id].to(self.device)

        similarity = self.classifier.similarity(
            test_embedding.squeeze(1),
            enrolled_embedding.squeeze(1)
        )
        score = (similarity.item() + 1) / 2
        is_match = score > self.verification_threshold
        return score, is_match

    def verify_embeddings(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        emb1 = torch.from_numpy(embedding1).unsqueeze(0).to(self.device)
        emb2 = torch.from_numpy(embedding2).unsqueeze(0).to(self.device)
        similarity = self.classifier.similarity(emb1, emb2)
        return (similarity.item() + 1) / 2

    def get_enrolled_speakers(self) -> List[str]:
        return list(self.enrolled_embeddings.keys())

    def clear_enrollment(self, speaker_id: Optional[str] = None) -> None:
        if speaker_id is None:
            self.enrolled_embeddings.clear()
        else:
            self.enrolled_embeddings.pop(speaker_id, None)

    def save_voiceprint(self, speaker_id: str, path: str) -> None:
        if speaker_id not in self.enrolled_embeddings:
            raise ValueError(f"Speaker '{speaker_id}' not enrolled")
        embedding = self.enrolled_embeddings[speaker_id].squeeze().numpy()
        np.save(path, embedding)

    def load_voiceprint(self, speaker_id: str, path: str) -> None:
        embedding = np.load(path)
        self.enroll_embedding(speaker_id, embedding)


class AntiSpoofingDetector:
    """Anti-spoofing placeholder."""

    def __init__(
        self,
        model_name: str = "rawnet2_asvspoof",
        device: str = "cpu",
        savedir: Optional[str] = None,
    ):
        self.device = device
        self.savedir = Path(savedir) if savedir else None
        self.classifier = None
        print("Anti-spoofing backend disabled: no local model assets configured")

    def analyze(self, audio_path: str) -> Dict[str, float]:
        if self.classifier is None:
            return {
                "spoof_probability": 0.5,
                "bonafide_probability": 0.5,
                "is_synthetic": False,
                "error": "Model not loaded",
            }

        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        signal, _sample_rate = load_audio_waveform(audio_path, target_sample_rate=16000)
        signal = signal.to(self.device)
        prediction = self.classifier.classify_batch(signal)

        if hasattr(prediction, 'shape'):
            if prediction.dim() > 1:
                probs = F.softmax(prediction, dim=-1)
                bonafide_prob = probs[0, 0].item()
                spoof_prob = probs[0, 1].item() if probs.shape[1] > 1 else 1 - bonafide_prob
            else:
                bonafide_prob = torch.sigmoid(prediction).item()
                spoof_prob = 1 - bonafide_prob
        else:
            bonafide_prob = 0.5
            spoof_prob = 0.5

        return {
            "spoof_probability": spoof_prob,
            "bonafide_probability": bonafide_prob,
            "is_synthetic": spoof_prob > 0.5,
        }


class AudioPreprocessor:
    """Audio preprocessing utilities."""

    def __init__(self, target_sample_rate: int = 16000):
        self.target_sample_rate = target_sample_rate

    def preprocess(self, audio_path: str) -> Tuple[torch.Tensor, int]:
        try:
            waveform, sample_rate = load_audio_waveform(
                audio_path,
                target_sample_rate=self.target_sample_rate,
            )
            return waveform, sample_rate
        except Exception as e:
            raise RuntimeError(f"Failed to load audio: {e}")


def compute_trust_score(
    spoof_probability: float,
    speaker_match_score: Optional[float] = None,
    quality_score: float = 70.0,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, float, str]:
    if weights is None:
        weights = {"deepfake": 0.4, "speaker": 0.3, "quality": 0.3}

    deepfake_score = (1 - spoof_probability) * 100

    if speaker_match_score is not None:
        overall = (
            weights["deepfake"] * deepfake_score +
            weights["speaker"] * speaker_match_score * 100 +
            weights["quality"] * quality_score
        )
    else:
        w_df = weights["deepfake"] + weights["speaker"] / 2
        w_q = weights["quality"] + weights["speaker"] / 2
        overall = w_df * deepfake_score + w_q * quality_score

    scores = [deepfake_score, quality_score]
    if speaker_match_score is not None:
        scores.append(speaker_match_score * 100)

    variance = np.var(scores)
    confidence = max(0, min(100, 100 - variance / 10))

    if overall >= 70:
        trust_level = "high"
    elif overall >= 40:
        trust_level = "medium"
    else:
        trust_level = "low"

    return overall, confidence, trust_level
