#!/usr/bin/env python3
"""Combined Whisper STT + Piper TTS HTTP server.

Endpoints:
  POST /transcribe  - Audio file → text (Whisper)
  POST /speak       - JSON {text} → audio/ogg (Piper TTS)

Requires: faster-whisper, piper-tts binary, ffmpeg
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from faster_whisper import WhisperModel
import tempfile, os, json, subprocess, argparse

def create_handler(model, piper_bin, piper_model, piper_speaker, speed):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args): pass

        def do_POST(self):
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)

            if self.path == '/transcribe':
                self._transcribe(data)
            elif self.path == '/speak':
                self._speak(data)
            else:
                self.send_response(404)
                self.end_headers()

        def _transcribe(self, data):
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as f:
                f.write(data)
                tmp_path = f.name
            try:
                segments, info = model.transcribe(tmp_path, beam_size=5)
                text = ' '.join(seg.text for seg in segments).strip()
                self._json_response(200, {'text': text, 'language': info.language})
            except Exception as e:
                self._json_response(500, {'error': str(e)})
            finally:
                os.unlink(tmp_path)

        def _speak(self, data):
            wav_file = ogg_file = None
            try:
                text = json.loads(data).get('text', '')
                speaker = json.loads(data).get('speaker', piper_speaker)
                wav_file = tempfile.mktemp(suffix='.wav')
                ogg_file = tempfile.mktemp(suffix='.ogg')
                subprocess.run(
                    [piper_bin, '--model', piper_model, '--speaker', str(speaker),
                     '--length_scale', str(speed), '--output_file', wav_file],
                    input=text.encode(), capture_output=True, timeout=30
                )
                subprocess.run(
                    ['ffmpeg', '-i', wav_file, '-c:a', 'libopus', '-b:a', '32k', ogg_file, '-y'],
                    capture_output=True, timeout=15
                )
                with open(ogg_file, 'rb') as f:
                    audio = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'audio/ogg')
                self.send_header('Content-Length', str(len(audio)))
                self.end_headers()
                self.wfile.write(audio)
            except Exception as e:
                self._json_response(500, {'error': str(e)})
            finally:
                for f in [wav_file, ogg_file]:
                    if f:
                        try: os.unlink(f)
                        except: pass

        def _json_response(self, code, data):
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

    return Handler

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Whisper STT + Piper TTS Server')
    p.add_argument('--port', type=int, default=9998)
    p.add_argument('--whisper-model', default='small', help='Whisper model size: tiny/base/small/medium/large')
    p.add_argument('--whisper-device', default='cpu', help='cpu or cuda')
    p.add_argument('--piper-bin', required=True, help='Path to piper binary')
    p.add_argument('--piper-model', required=True, help='Path to piper .onnx voice model')
    p.add_argument('--piper-speaker', default='4', help='Speaker ID for multi-speaker models')
    p.add_argument('--speed', type=float, default=0.9, help='TTS speed (lower=faster, 1.0=normal)')
    args = p.parse_args()

    print(f'Loading Whisper model ({args.whisper_model}, {args.whisper_device})...')
    model = WhisperModel(args.whisper_model, device=args.whisper_device, compute_type='int8')
    print('Model loaded!')

    handler = create_handler(model, args.piper_bin, args.piper_model, args.piper_speaker, args.speed)
    print(f'Voice Server on http://0.0.0.0:{args.port}')
    print(f'  POST /transcribe  (audio → text)')
    print(f'  POST /speak       (text → audio/ogg)')
    HTTPServer(('0.0.0.0', args.port), handler).serve_forever()
