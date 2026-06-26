#!/usr/bin/env python3
"""
VoiceTrust Demo Script - Integration with SpeechBrain pre-trained models.

Analyze audio files for deepfake detection and trust scoring.
Optimized for Chinese/English voice messages.

Usage:
    # Check local model assets first
    uv run --python .venv/bin/python ../scripts/ensure_models.py

    # Analyze without speaker verification
    uv run --python .venv/bin/python ../scripts/demo.py --audio sample.wav

    # Enroll a speaker
    uv run --python .venv/bin/python ../scripts/demo.py --audio enrollment.wav --speaker owner --enroll

    # Verify a speaker
    uv run --python .venv/bin/python ../scripts/demo.py --audio message.wav --speaker owner

    # Create test audio
    uv run --python .venv/bin/python ../scripts/demo.py --create-demo test.wav
"""
import argparse
import sys
import os
import json
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_ROOT = PACKAGE_ROOT / "runtime"

# Add runtime src to path
sys.path.insert(0, str(RUNTIME_ROOT / "src"))

import torch
import numpy as np

try:
    from inference.pipeline import VoiceTrustPipeline, TrustScore
    SPEECHBRAIN_AVAILABLE = True
except ImportError as e:
    print(f"Error importing VoiceTrust: {e}")
    print("\nPlease install dependencies:")
    print("  uv pip install --python .venv/bin/python -r requirements.txt")
    SPEECHBRAIN_AVAILABLE = False


# Default storage
VOICEPRINT_DIR = RUNTIME_ROOT / "data" / "voiceprints"
OWNER_PROFILE_DIR = RUNTIME_ROOT / "data" / "owners"
MODEL_DIR = RUNTIME_ROOT / "assets" / "models" / "ecapa_voxceleb"
REQUIRED_MODEL_FILES = [
    "hyperparams.yaml",
    "classifier.ckpt",
    "embedding_model.ckpt",
    "label_encoder.ckpt",
    "mean_var_norm_emb.ckpt",
]


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  VoiceTrust for OpenClaw")
    print("  Voice Message Trust Verification System")
    print("  Powered by SpeechBrain Pre-trained Models")
    print("=" * 60)
    print()


def ensure_model_assets() -> bool:
    missing = [name for name in REQUIRED_MODEL_FILES if not (MODEL_DIR / name).exists()]
    if not missing:
        return True

    print("VoiceTrust model assets are missing.")
    print(f"Expected directory: {MODEL_DIR}")
    print("Missing files:")
    for name in missing:
        print(f"  - {name}")
    print()
    print("This lightweight skill bundle does not include large checkpoint files.")
    print("Prepare the model assets first, then re-run this command:")
    print("  cd runtime")
    print("  uv run --python .venv/bin/python ../scripts/ensure_models.py")
    print()
    return False


def print_result(result: TrustScore):
    """Pretty print analysis result."""
    print("-" * 60)
    print("ANALYSIS RESULTS")
    print("-" * 60)
    print()

    print("Component Scores (0-100, higher = more trustworthy):")
    if result.speaker_match >= 0:
        print(f"  Speaker Verification:  {result.speaker_match:6.2f}")
    else:
        print(f"  Speaker Verification:  Not checked")
    print(f"  Audio Quality:         {result.audio_quality:6.2f}")
    print(f"  Identity Score:        {result.identity_score:6.2f}")
    print()

    print(f"Overall Trust Score: {result.overall_trust:.2f} ({result.trust_label.upper()})")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Decision: {result.decision}")
    print(f"Speech Duration: {result.speech_duration:.2f}s")
    print(f"Speech Ratio: {result.speech_ratio:.3f}")
    print(f"VAD Status: {result.vad_status}")
    if result.failure_reason is not None:
        print(f"Failure Reason: {result.failure_reason}")
    if result.decision_reasons:
        print("Decision Reasons:")
        for reason in result.decision_reasons:
            print(f"  - {reason}")
    print()

    print("-" * 60)
    if result.speaker_id and result.speaker_match >= 0:
        match_status = "MATCH" if result.speaker_match >= 78 else "NO MATCH"
        print(f"Speaker Verification ({result.speaker_id}): {match_status}")
        print(f"  Similarity Score: {result.raw_speaker_score:.3f}")
    print("-" * 60)
    print()


def create_demo_audio(output_path: str, duration: float = 3.0):
    """Create a demo audio file for testing."""
    try:
        import soundfile as sf
        import numpy as np

        sample_rate = 16000
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Generate a simple synthetic voice-like signal
        f0 = 150
        waveform = np.sin(2 * np.pi * f0 * t)
        for i in range(2, 6):
            waveform += 0.3 ** i * np.sin(2 * np.pi * f0 * i * t)
        waveform = waveform / np.abs(waveform).max()

        sf.write(output_path, waveform, sample_rate)
        print(f"Created demo audio: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creating demo audio: {e}")
        return None


def save_voiceprint(speaker_id: str, embedding: np.ndarray, voiceprint_dir: Path = VOICEPRINT_DIR):
    """Save voiceprint to disk."""
    voiceprint_dir.mkdir(parents=True, exist_ok=True)
    voiceprint_path = voiceprint_dir / f"{speaker_id}.npy"
    np.save(voiceprint_path, embedding)
    print(f"  Saved voiceprint to: {voiceprint_path}")


def load_voiceprint(speaker_id: str, voiceprint_dir: Path = VOICEPRINT_DIR) -> np.ndarray:
    """Load voiceprint from disk."""
    voiceprint_path = voiceprint_dir / f"{speaker_id}.npy"
    if voiceprint_path.exists():
        return np.load(voiceprint_path)
    return None


def list_enrolled_speakers(voiceprint_dir: Path = VOICEPRINT_DIR, owner_profile_dir: Path = OWNER_PROFILE_DIR) -> dict:
    """List legacy voiceprints and owner profiles."""
    legacy = []
    if voiceprint_dir.exists():
        legacy = [f.stem for f in voiceprint_dir.glob("*.npy")]

    owners = []
    if owner_profile_dir.exists():
        for d in owner_profile_dir.iterdir():
            if not d.is_dir():
                continue
            profile = d / "profile.json"
            if profile.exists():
                owners.append(d.name)

    return {
        "owner_profiles": sorted(owners),
        "legacy_voiceprints": sorted(legacy),
    }


def main():
    parser = argparse.ArgumentParser(
        description="VoiceTrust Demo - Analyze voice messages for authenticity"
    )
    parser.add_argument(
        "--audio",
        type=str,
        help="Path to audio file to analyze",
    )
    parser.add_argument(
        "--speaker",
        type=str,
        help="Speaker ID for verification",
    )
    parser.add_argument(
        "--enroll",
        action="store_true",
        help="Enroll speaker instead of verifying",
    )
    parser.add_argument(
        "--enroll-sample",
        action="store_true",
        help="Append an enrollment sample to a multi-sample owner profile",
    )
    parser.add_argument(
        "--create-demo",
        type=str,
        metavar="PATH",
        help="Create a demo audio file at the specified path",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to use for inference",
    )
    parser.add_argument(
        "--expected-lang",
        type=str,
        choices=["chinese", "english"],
        help="Expected language in the audio",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.25,
        help="Speaker verification threshold (default: 0.25)",
    )
    parser.add_argument(
        "--spoof-threshold",
        type=float,
        default=0.5,
        help="Spoof detection threshold (default: 0.5)",
    )
    parser.add_argument(
        "--list-speakers",
        action="store_true",
        help="List enrolled speakers",
    )
    parser.add_argument(
        "--clear-speaker",
        type=str,
        metavar="SPEAKER_ID",
        help="Clear a specific speaker's enrollment",
    )

    args = parser.parse_args()

    # Check SpeechBrain availability
    if not SPEECHBRAIN_AVAILABLE:
        print("Error: SpeechBrain not available. Please install dependencies.")
        sys.exit(1)

    # Create demo audio if requested
    if args.create_demo:
        create_demo_audio(args.create_demo)
        return

    # Handle list speakers without requiring model checkpoints
    if args.list_speakers:
        listing = list_enrolled_speakers()
        owner_profiles = listing["owner_profiles"]
        legacy_voiceprints = listing["legacy_voiceprints"]

        if owner_profiles:
            print("Owner profiles:")
            for s in owner_profiles:
                print(f"  - {s}")
        if legacy_voiceprints:
            print("Legacy voiceprints:")
            for s in legacy_voiceprints:
                print(f"  - {s}")
        if not owner_profiles and not legacy_voiceprints:
            print("No enrolled speakers found.")
        return

    # Handle clear speaker without requiring model checkpoints
    if args.clear_speaker:
        voiceprint_path = VOICEPRINT_DIR / f"{args.clear_speaker}.npy"
        if voiceprint_path.exists():
            voiceprint_path.unlink()
            print(f"Cleared enrollment for speaker: {args.clear_speaker}")
        else:
            print(f"Speaker '{args.clear_speaker}' not found.")
        return

    # Any real VoiceTrust runtime action below this point needs local model assets
    if not ensure_model_assets():
        sys.exit(2)

    # Check audio file
    if not args.audio:
        print("Error: --audio is required (or use --create-demo)")
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.audio):
        print(f"Error: Audio file not found: {args.audio}")
        sys.exit(1)

    # Print banner
    if not args.json:
        print_banner()

    # Set device
    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("CUDA not available, using CPU")
        device = "cpu"

    # Initialize pipeline
    try:
        if not args.json:
            print(f"Initializing pipeline on {device}...")
            print("Note: local model assets must already be prepared before first use")
            print()

        pipeline = VoiceTrustPipeline(
            device=device,
            verification_threshold=args.threshold,
        )
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Enroll speaker if requested
    if args.enroll and args.speaker:
        try:
            if not args.json:
                print(f"Enrolling speaker: {args.speaker}")
                print(f"Audio file: {args.audio}")
                print()

            embedding = pipeline.enroll_speaker(args.speaker, args.audio)

            # Save voiceprint to disk for persistence
            save_voiceprint(args.speaker, embedding)

            if not args.json:
                print(f"Speaker '{args.speaker}' enrolled successfully.")
                print(f"Embedding shape: {embedding.shape}")
            else:
                print(json.dumps({
                    "status": "success",
                    "speaker_id": args.speaker,
                    "embedding_shape": list(embedding.shape),
                }))
        except Exception as e:
            print(f"Enrollment failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        return

    if args.enroll_sample and args.speaker:
        try:
            result = pipeline.enroll_owner_sample(args.speaker, args.audio)
            if not args.json:
                print(f"Appended owner sample for '{args.speaker}'.")
                print(f"Sample count: {result['sample_count']}")
                print(f"Aggregate embedding: {result['aggregate_embedding_file']}")
            else:
                print(json.dumps({"status": "success", **result}, indent=2))
        except Exception as e:
            print(f"Owner sample enrollment failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        return

    # Analyze audio
    try:
        # Load existing voiceprints
        if args.speaker:
            owner_profile_loaded = False
            try:
                owner_profile_loaded = pipeline.load_owner_profile(args.speaker)
            except Exception:
                owner_profile_loaded = False

            if owner_profile_loaded:
                if not args.json:
                    print(f"Loaded owner profile for speaker: {args.speaker}")
            else:
                voiceprint = load_voiceprint(args.speaker)
                if voiceprint is not None:
                    pipeline.load_voiceprint(args.speaker, str(VOICEPRINT_DIR / f"{args.speaker}.npy"))
                    if not args.json:
                        print(f"Loaded voiceprint for speaker: {args.speaker}")
                elif not args.json:
                    print(f"Warning: Speaker '{args.speaker}' not enrolled. Run with --enroll first.")

        if not args.json:
            print(f"Analyzing: {args.audio}")
            if args.speaker:
                if args.speaker in pipeline.get_enrolled_speakers():
                    print(f"Verifying against speaker: {args.speaker}")
                else:
                    print(f"Warning: Speaker '{args.speaker}' not enrolled!")
            if args.expected_lang:
                print(f"Expected language: {args.expected_lang}")
            print()

        result = pipeline.analyze_audio(
            audio_path=args.audio,
            speaker_id=args.speaker,
            expected_language=args.expected_lang,
        )

        # Output results
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_result(result)

            # Recommendations
            print("RECOMMENDATIONS:")
            if result.decision == "allow_command":
                print("  - Owner verification passed at executable level")
                print("  - Command-capable trust threshold met")
                print("  - Safe to use for voice command execution")
            elif result.trust_label == "medium":
                print("  - Partial owner similarity detected")
                print("  - Keep transcript, but require secondary confirmation for commands")
                print("  - Not safe for automatic command execution")
            else:
                print("  - Owner verification insufficient")
                print("  - Do not execute voice commands from this sample")
                print("  - Ask for text confirmation or a longer clearer voice sample")
            print()

    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
