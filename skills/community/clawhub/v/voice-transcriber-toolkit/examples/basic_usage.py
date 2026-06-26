import os
import wave
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/voice-transcriber-toolkit')

from scripts.voice_transcriber import VoiceTranscriber, AudioConverter

def demo_transcription():
    print("=== Voice Transcription Demo ===\n")
    
    # 创建演示音频文件
    demo_path = "demo_audio.wav"
    with wave.open(demo_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b'\x00' * 16000 * 2 * 3)
    
    transcriber = VoiceTranscriber(engine="whisper", model_size="base")
    
    # 单文件转录
    print("1. Single file transcription:")
    result = transcriber.transcribe(demo_path, language="en")
    print(f"   Text: {result['text']}")
    print(f"   Language: {result['language']}")
    print(f"   Duration: {result['duration']:.1f}s")
    print(f"   Segments: {len(result['segments'])}")
    
    # 字幕导出
    print("\n2. Subtitle export:")
    srt = transcriber.export_subtitles(result, "srt")
    print(f"   SRT preview:\n{srt[:200]}...")
    
    vtt = transcriber.export_subtitles(result, "vtt")
    print(f"   VTT preview:\n{vtt[:200]}...")
    
    # 批量转录
    print("\n3. Batch transcription:")
    batch_results = transcriber.transcribe_batch([demo_path, demo_path])
    for r in batch_results:
        print(f"   File: {r.get('file')}, Success: {r.get('success')}")
    
    os.remove(demo_path)


def demo_audio_converter():
    print("\n=== Audio Converter Demo ===\n")
    
    converter = AudioConverter()
    print(f"ffmpeg available: {converter.ffmpeg_available}")
    
    # 创建演示WAV文件
    demo_path = "demo_for_convert.wav"
    with wave.open(demo_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b'\x00' * 16000 * 2 * 3)
    
    # 获取音频信息
    print(f"\nAudio info for {demo_path}:")
    info = converter.get_audio_info(demo_path)
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    os.remove(demo_path)


if __name__ == "__main__":
    demo_transcription()
    demo_audio_converter()
