"""Inference pipeline for VoiceTrust.

Current mainline focuses on:
- SpeechBrain ECAPA-TDNN for speaker verification
- audio quality and speech-activity metadata
- STT-independent trust scoring
"""
import torch
import numpy as np
from typing import Dict, Optional, Tuple, Any, List
from dataclasses import dataclass, field
from pathlib import Path
import warnings

try:
    from models.speechbrain_wrapper import (
        SpeechBrainSpeakerVerifier,
        AudioPreprocessor,
    )
    from data.owner_profiles import OwnerProfileStore
    SPEECHBRAIN_AVAILABLE = True
except ImportError:
    SPEECHBRAIN_AVAILABLE = False
    warnings.warn("SpeechBrain wrapper not available. Pipeline will not function.")


@dataclass
class TrustScore:
    """Trust analysis results."""

    speaker_match: float
    audio_quality: float
    overall_trust: float
    confidence: float
    identity_score: float = -1.0
    trust_label: str = "low"
    decision: str = "reject_command"
    decision_reasons: List[str] = field(default_factory=list)
    speaker_id: Optional[str] = None
    speech_duration: float = 0.0
    speech_ratio: float = 0.0
    vad_status: str = "unavailable"
    failure_reason: Optional[str] = None
    raw_speaker_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker_match": self.speaker_match,
            "audio_quality": self.audio_quality,
            "overall_trust": self.overall_trust,
            "confidence": self.confidence,
            "identity_score": self.identity_score,
            "trust_label": self.trust_label,
            "decision": self.decision,
            "decision_reasons": self.decision_reasons,
            "speaker_id": self.speaker_id,
            "speech_duration": self.speech_duration,
            "speech_ratio": self.speech_ratio,
            "vad_status": self.vad_status,
            "failure_reason": self.failure_reason,
            "raw_scores": {
                "speaker_similarity": self.raw_speaker_score,
            },
        }


class VoiceTrustPipeline:
    """Main pipeline for voice trust verification using pre-trained models."""

    def __init__(
        self,
        device: str = "cpu",
        sample_rate: int = 16000,
        verification_threshold: float = 0.25,
        weights: Optional[Dict[str, float]] = None,
        speaker_model: str = "ecapa_voxceleb",
    ):
        if not SPEECHBRAIN_AVAILABLE:
            raise RuntimeError(
                "SpeechBrain is required. Install with: pip install speechbrain"
            )

        self.device = device
        self.sample_rate = sample_rate
        self.weights = weights or {
            "speaker": 0.85,
            "confidence": 0.15,
        }
        self.verification_threshold = verification_threshold
        self.preprocessor = AudioPreprocessor(target_sample_rate=sample_rate)
        self.min_speech_duration = 1.5
        self.min_speech_ratio = 0.25
        self.owner_profile_store = OwnerProfileStore(
            Path(__file__).resolve().parent.parent.parent / "data" / "owners"
        )

        print("Initializing VoiceTrust pipeline...")
        print(f"Device: {device}")

        try:
            self.speaker_verifier = SpeechBrainSpeakerVerifier(
                model_name=speaker_model,
                device=device,
                verification_threshold=verification_threshold,
            )
        except Exception as e:
            print(f"Warning: Could not load speaker verification model: {e}")
            self.speaker_verifier = None

        print("Pipeline initialized successfully")

    def analyze_audio(
        self,
        audio_path: str,
        speaker_id: Optional[str] = None,
        expected_language: Optional[str] = None,
    ) -> TrustScore:
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        speech_duration, speech_ratio, vad_status, failure_reason = self._analyze_speech(audio_path)
        speaker_match, raw_speaker_score = self._verify_speaker(audio_path, speaker_id)
        audio_quality = self._analyze_quality(audio_path)

        if failure_reason in {"too_short", "insufficient_speech"}:
            speaker_match = -1.0
            raw_speaker_score = 0.0

        overall_trust, confidence, identity_score, trust_label, decision, decision_reasons = self._compute_trust_decision(
            speaker_match=speaker_match,
            audio_quality=audio_quality,
            speech_duration=speech_duration,
            speech_ratio=speech_ratio,
            vad_status=vad_status,
            failure_reason=failure_reason,
        )

        return TrustScore(
            speaker_match=speaker_match,
            audio_quality=audio_quality,
            overall_trust=overall_trust,
            confidence=confidence,
            identity_score=identity_score,
            trust_label=trust_label,
            decision=decision,
            decision_reasons=decision_reasons,
            speaker_id=speaker_id,
            speech_duration=speech_duration,
            speech_ratio=speech_ratio,
            vad_status=vad_status,
            failure_reason=failure_reason,
            raw_speaker_score=raw_speaker_score,
        )

    def _analyze_deepfake(self, audio_path: str) -> Tuple[float, float]:
        if self.spoofing_detector is None:
            warnings.warn("No spoofing detector available")
            return 50.0, 0.5
        try:
            result = self.spoofing_detector.analyze(audio_path)
            spoof_prob = result["spoof_probability"]
            bonafide_prob = result["bonafide_probability"]
            return bonafide_prob * 100, spoof_prob
        except Exception as e:
            warnings.warn(f"Deepfake analysis failed: {e}")
            return 50.0, 0.5

    def _analyze_speech(self, audio_path: str) -> Tuple[float, float, str, Optional[str]]:
        """Lightweight speech activity estimation for VoiceTrust."""
        try:
            waveform, sr = self.preprocessor.preprocess(audio_path)
            mono = waveform.squeeze(0)
            if mono.numel() == 0:
                return 0.0, 0.0, "empty", "insufficient_speech"

            total_duration = mono.shape[-1] / sr
            frame_size = max(1, int(0.03 * sr))
            hop_size = max(1, int(0.015 * sr))

            energies = []
            for start in range(0, max(1, mono.shape[-1] - frame_size + 1), hop_size):
                frame = mono[start:start + frame_size]
                if frame.numel() == 0:
                    continue
                energies.append(torch.sqrt(torch.mean(frame ** 2)).item())

            if not energies:
                return 0.0, 0.0, "no_frames", "insufficient_speech"

            energies_np = np.asarray(energies)
            max_energy = float(np.max(energies_np))
            if max_energy <= 1e-6:
                return 0.0, 0.0, "silence", "insufficient_speech"

            energy_threshold = max(0.01, max_energy * 0.2)
            speech_frames = energies_np > energy_threshold
            speech_ratio = float(np.mean(speech_frames))
            speech_duration = float(speech_ratio * total_duration)

            failure_reason = None
            if total_duration < 1.0:
                failure_reason = "too_short"
            elif speech_duration < self.min_speech_duration or speech_ratio < self.min_speech_ratio:
                failure_reason = "insufficient_speech"

            return speech_duration, speech_ratio, "ok", failure_reason
        except Exception as e:
            warnings.warn(f"Speech activity analysis failed: {e}")
            return 0.0, 0.0, "unavailable", None

    def _verify_speaker(self, audio_path: str, speaker_id: Optional[str]) -> Tuple[float, float]:
        if self.speaker_verifier is None or speaker_id is None:
            return -1.0, 0.0
        if speaker_id not in self.speaker_verifier.get_enrolled_speakers():
            return -1.0, 0.0
        try:
            score, _is_match = self.speaker_verifier.verify(audio_path, speaker_id)
            return score * 100, score
        except Exception as e:
            warnings.warn(f"Speaker verification failed: {e}")
            return -1.0, 0.0

    def _analyze_quality(self, audio_path: str) -> float:
        try:
            waveform, sr = self.preprocessor.preprocess(audio_path)
            duration = waveform.shape[-1] / sr
            rms = torch.sqrt(torch.mean(waveform ** 2)).item()
            peak = torch.max(torch.abs(waveform)).item()
            dynamic_range_db = 20 * np.log10(peak / (rms + 1e-10)) if peak > 0 else 0

            score = 100.0
            if duration < 1.0:
                score -= 20 * (1.0 - duration)
            if rms < 0.01:
                score -= 20
            if peak > 0.95:
                score -= 10
            if dynamic_range_db < 10:
                score -= 15
            return max(0.0, min(100.0, score))
        except Exception as e:
            warnings.warn(f"Quality analysis failed: {e}")
            return 70.0

    def _analyze_language(
        self, audio_path: str, expected_language: Optional[str]
    ) -> Tuple[float, Optional[str], float]:
        """Metadata-first placeholder until a real LID backend is integrated."""
        if expected_language is None:
            return 50.0, None, 0.0
        return 50.0, expected_language, 0.25

    def _compute_trust_decision(
        self,
        speaker_match: float,
        audio_quality: float,
        speech_duration: float,
        speech_ratio: float,
        vad_status: str,
        failure_reason: Optional[str],
    ) -> Tuple[float, float, float, str, str, List[str]]:
        decision_reasons: List[str] = []

        if speaker_match < 0:
            identity_score = 0.0
            confidence = 0.0
            if failure_reason is not None:
                decision_reasons.append(failure_reason)
            else:
                decision_reasons.append("speaker_match_unavailable")
        else:
            confidence = max(0.0, min(100.0, 0.7 * speaker_match + 0.2 * audio_quality + 10.0))
            identity_score = (
                self.weights["speaker"] * speaker_match
                + self.weights["confidence"] * confidence
            )

        overall_trust = identity_score

        if failure_reason is not None:
            decision_reasons.append(f"failure:{failure_reason}")
            overall_trust -= 35.0

        if vad_status != "ok":
            decision_reasons.append("vad_not_ok")
            overall_trust -= 25.0

        if speech_duration < 2.5:
            decision_reasons.append("short_speech")
            overall_trust -= 15.0
        elif speech_duration < 3.0:
            decision_reasons.append("borderline_short_speech")
            overall_trust -= 8.0

        if speech_ratio < 0.35:
            decision_reasons.append("low_speech_ratio")
            overall_trust -= 10.0
        elif speech_ratio < 0.45:
            decision_reasons.append("borderline_speech_ratio")
            overall_trust -= 5.0

        if speaker_match >= 0 and speaker_match < 70.0:
            decision_reasons.append("speaker_match_below_owner_threshold")
            overall_trust -= 18.0
        if confidence < 75.0:
            decision_reasons.append("confidence_below_execution_threshold")
            overall_trust -= 12.0

        overall_trust = max(0.0, min(100.0, overall_trust))

        short_high_confidence_override = (
            speech_duration >= 1.2
            and speaker_match >= 85.0
            and confidence >= 85.0
        )

        if (
            failure_reason is None
            and vad_status == "ok"
            and (speech_duration >= 3.0 or short_high_confidence_override)
            and speaker_match >= 78.0
            and confidence >= 80.0
            and identity_score >= 82.0
        ):
            decision = "allow_command"
        else:
            decision = "reject_command"

        if speaker_match >= 0 and identity_score >= 85.0 and confidence >= 80.0 and failure_reason is None:
            trust_label = "high"
        elif speaker_match >= 0 and identity_score >= 72.0 and confidence >= 68.0 and failure_reason is None:
            trust_label = "medium"
        else:
            trust_label = "low"

        if not decision_reasons and decision == "allow_command":
            decision_reasons.append("meets_execution_threshold")

        return overall_trust, confidence, identity_score, trust_label, decision, decision_reasons

    def enroll_speaker(self, speaker_id: str, audio_path: str) -> np.ndarray:
        if self.speaker_verifier is None:
            raise RuntimeError("Speaker verifier not initialized")
        return self.speaker_verifier.enroll(speaker_id, audio_path)

    def enroll_owner_sample(self, speaker_id: str, audio_path: str) -> dict:
        if self.speaker_verifier is None:
            raise RuntimeError("Speaker verifier not initialized")

        embedding = self.speaker_verifier.enroll(speaker_id, audio_path)
        profile = self.owner_profile_store.append_sample(speaker_id, audio_path, embedding)
        aggregate_path = self.owner_profile_store.speaker_dir(speaker_id) / profile.aggregate_embedding_file
        self.speaker_verifier.load_voiceprint(speaker_id, str(aggregate_path))

        return {
            "speaker_id": speaker_id,
            "sample_count": len(profile.samples),
            "aggregate_embedding_file": str(aggregate_path),
        }

    def get_enrolled_speakers(self) -> list:
        if self.speaker_verifier is None:
            return []
        return self.speaker_verifier.get_enrolled_speakers()

    def save_voiceprint(self, speaker_id: str, path: str) -> None:
        if self.speaker_verifier is None:
            raise RuntimeError("Speaker verifier not initialized")
        self.speaker_verifier.save_voiceprint(speaker_id, path)

    def load_voiceprint(self, speaker_id: str, path: str) -> None:
        if self.speaker_verifier is None:
            raise RuntimeError("Speaker verifier not initialized")
        self.speaker_verifier.load_voiceprint(speaker_id, path)

    def load_owner_profile(self, speaker_id: str) -> bool:
        if self.speaker_verifier is None:
            raise RuntimeError("Speaker verifier not initialized")
        profile = self.owner_profile_store.load_profile(speaker_id)
        if profile is None:
            return False
        aggregate_path = self.owner_profile_store.speaker_dir(speaker_id) / profile.aggregate_embedding_file
        if not aggregate_path.exists():
            return False
        self.speaker_verifier.load_voiceprint(speaker_id, str(aggregate_path))
        return True

    def set_verification_threshold(self, threshold: float) -> None:
        self.verification_threshold = threshold
        if self.speaker_verifier is not None:
            self.speaker_verifier.verification_threshold = threshold
