"""VoiceTrust package for the self-contained Skill-VoiceTrust runtime."""

from .inference.pipeline import VoiceTrustPipeline, TrustScore

__version__ = "0.1.0"

__all__ = ["VoiceTrustPipeline", "TrustScore"]
