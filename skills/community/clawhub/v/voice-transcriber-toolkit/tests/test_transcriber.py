import pytest
import os
import sys
import wave
sys.path.insert(0, '/root/.openclaw/workspace/skills/voice-transcriber-toolkit')

from scripts.voice_transcriber import VoiceTranscriber, AudioConverter

class TestVoiceTranscriber:
    def setup_method(self):
        self.transcriber = VoiceTranscriber()
    
    def create_demo_wav(self, path="test.wav"):
        with wave.open(path, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(b'\x00' * 16000 * 2 * 2)
        return path
    
    def teardown_method(self):
        for f in ["test.wav", "test2.wav", "output.wav"]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_transcribe_mock_mode(self):
        path = self.create_demo_wav()
        result = self.transcriber.transcribe(path)
        assert isinstance(result, dict)
        assert "text" in result
        assert "language" in result
        assert "segments" in result
    
    def test_transcribe_returns_text(self):
        path = self.create_demo_wav()
        result = self.transcriber.transcribe(path)
        assert isinstance(result["text"], str)
        assert len(result["text"]) > 0
    
    def test_transcribe_with_language(self):
        path = self.create_demo_wav()
        result = self.transcriber.transcribe(path, language="zh")
        assert result["language"] == "zh"
    
    def test_transcribe_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            self.transcriber.transcribe("nonexistent.mp3")
    
    def test_transcribe_unsupported_format(self):
        with pytest.raises(ValueError):
            self.transcriber.transcribe("file.xyz")
    
    def test_transcribe_batch(self):
        p1 = self.create_demo_wav("test.wav")
        p2 = self.create_demo_wav("test2.wav")
        results = self.transcriber.transcribe_batch([p1, p2])
        assert len(results) == 2
        assert all(r.get("success") for r in results)
    
    def test_export_srt(self):
        path = self.create_demo_wav()
        result = self.transcriber.transcribe(path)
        srt = self.transcriber.export_subtitles(result, "srt")
        assert isinstance(srt, str)
        assert "-->" in srt
    
    def test_export_vtt(self):
        path = self.create_demo_wav()
        result = self.transcriber.transcribe(path)
        vtt = self.transcriber.export_subtitles(result, "vtt")
        assert isinstance(vtt, str)
        assert "WEBVTT" in vtt
    
    def test_export_invalid_format(self):
        with pytest.raises(ValueError):
            self.transcriber.export_subtitles({"segments": []}, "abc")


class TestAudioConverter:
    def setup_method(self):
        self.converter = AudioConverter()
    
    def create_demo_wav(self, path="test.wav"):
        with wave.open(path, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(b'\x00' * 16000 * 2 * 2)
        return path
    
    def teardown_method(self):
        for f in ["test.wav", "converted.wav"]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_ffmpeg_check(self):
        assert isinstance(self.converter.ffmpeg_available, bool)
    
    def test_get_audio_info(self):
        path = self.create_demo_wav()
        info = self.converter.get_audio_info(path)
        assert isinstance(info, dict)
        assert "duration" in info or "error" in info
    
    def test_convert_to_wav_without_ffmpeg(self):
        if not self.converter.ffmpeg_available:
            with pytest.raises(RuntimeError):
                self.converter.convert_to_wav("dummy.mp3")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
