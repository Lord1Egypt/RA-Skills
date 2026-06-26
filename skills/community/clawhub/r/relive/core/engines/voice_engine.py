import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class VoiceEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sample_rate = config.get("sample_rate", 16000)
        self.model_dir = config.get("model_dir", "models/voice/pretrained_models/Fun-CosyVoice3-0.5B")
        self._cosyvoice_model = None
        
    def synthesize(
        self,
        text: str,
        voice_profile_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        prompt_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        # prompt_text 必须由外部显式提供，以便与参考音频严格对齐
        if not prompt_text:
            return {
                "success": False,
                "error": "Missing prompt_text: please provide the transcript text that matches the reference audio."
            }
        if voice_profile_path is None or not Path(voice_profile_path).exists():
            return {
                "success": False,
                "error": "CosyVoice3 requires a voice profile (reference audio). Please provide reference audio file."
            }
            
        if output_path is None:
            output_path = voice_profile_path.parent / "cache" / f"{uuid.uuid4()}.wav"
            
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        return self._cosyvoice3_synthesize(text, voice_profile_path, output_path, prompt_text)
            
    def _cosyvoice3_synthesize(
        self,
        text: str,
        voice_profile_path: Path,
        output_path: Path,
        prompt_text: str,
    ) -> Dict[str, Any]:
        try:
            import sys
            import torchaudio
            
            model_dir = Path(self.model_dir)
            if not model_dir.exists():
                model_dir = Path(__file__).parent.parent.parent / self.model_dir
            
            cosyvoice_path = model_dir.parent.parent / "voice" / "CosyVoice"
            if cosyvoice_path.exists():
                sys.path.insert(0, str(cosyvoice_path))
            
            matche_tts_path = model_dir.parent.parent / "voice" / "CosyVoice" / "third_party" / "Matcha-TTS"
            if matche_tts_path.exists():
                sys.path.insert(0, str(matche_tts_path))
            
            from cosyvoice.cli.cosyvoice import AutoModel
            
            if self._cosyvoice_model is None:
                logger.info(f"Loading CosyVoice3 model from {model_dir}")
                self._cosyvoice_model = AutoModel(model_dir=str(model_dir))
                
            ref_wav = list(voice_profile_path.glob("*.wav")) + list(voice_profile_path.glob("*.mp3")) + list(voice_profile_path.glob("*.m4a"))
            if ref_wav:
                ref_wav_path = str(ref_wav[0])
            else:
                raise FileNotFoundError("No reference audio file found (.wav, .mp3 or .m4a)")
            
            # 这里假定上层已经保证 prompt_text 非空
            
            # 只取第一段输出即可，不需要 enumerate
            for out in self._cosyvoice_model.inference_zero_shot(
                text,
                f"You are a helpful assistant.<|endofprompt|>{prompt_text}",
                ref_wav_path,
                stream=False
            ):
                torchaudio.save(str(output_path), out['tts_speech'], self._cosyvoice_model.sample_rate)
                break
                
            return {
                "success": True,
                "audio_path": str(output_path)
            }
        except ImportError as e:
            logger.warning(f"CosyVoice3 not available: {e}")
            return {
                "success": False,
                "error": "CosyVoice3 not installed. Run download script to install."
            }
        except Exception as e:
            logger.error(f"CosyVoice3 synthesis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        
    def extract_voice_profile(self, audio_path: Path, output_path: Path) -> Dict[str, Any]:
        try:
            import librosa
            import soundfile as sf
            
            y, sr = librosa.load(str(audio_path), sr=16000)
            
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            profile_file = output_path / "reference.wav"
            sf.write(str(profile_file), y, sr)
            
            return {
                "success": True,
                "profile_path": str(profile_file),
                "sample_rate": sr,
                "duration": len(y) / sr
            }
        except Exception as e:
            logger.error(f"Voice profile extraction failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def download_model(self, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        if output_dir is None:
            output_dir = Path(self.model_dir).parent
            
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            from modelscope import snapshot_download
            
            logger.info("Downloading CosyVoice3-0.5B model...")
            model_path = snapshot_download(
                'FunAudioLLM/Fun-CosyVoice3-0.5B-2512',
                local_dir=str(output_dir / 'Fun-CosyVoice3-0.5B')
            )
            
            logger.info("Downloading CosyVoice-ttsfrd...")
            ttsfrd_path = snapshot_download(
                'iic/CosyVoice-ttsfrd',
                local_dir=str(output_dir / 'CosyVoice-ttsfrd')
            )
            
            return {
                "success": True,
                "model_dir": str(output_dir),
                "cosyvoice_path": model_path,
                "ttsfrd_path": ttsfrd_path
            }
        except ImportError:
            return {
                "success": False,
                "error": "modelscope not installed. Run: pip install modelscope"
            }
        except Exception as e:
            logger.error(f"Model download failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
