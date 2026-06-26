"""Models module for the current VoiceTrust mainline."""

from .speechbrain_wrapper import (
    SpeechBrainSpeakerVerifier,
    AntiSpoofingDetector,
    AudioPreprocessor,
)

SPEECHBRAIN_AVAILABLE = True

__all__ = [
    "SpeechBrainSpeakerVerifier",
    "AntiSpoofingDetector",
    "AudioPreprocessor",
    "SPEECHBRAIN_AVAILABLE",
]
