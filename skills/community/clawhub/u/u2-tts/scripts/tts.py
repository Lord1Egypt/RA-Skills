# coding:utf-8
"""
UniSound TTS WebSocket Demo

Text-to-speech conversion using UniSound's TTS WebSocket API.
"""
import websocket
import hashlib
import json
import time
from functools import partial
try:
    import thread
except ImportError:
    import _thread as thread
import os
import argparse
from typing import Optional

class Ws_parms(object):
    """
    WebSocket TTS parameter class.

    Manages configuration and state for TTS WebSocket connections.
    """
    
    def __init__(self, url, appkey, secret, pid, vcn, text, user_id, tts_format, tts_sample):
        self.url = url
        self.appkey = appkey
        self.secret = secret
        self.user_id = user_id

        self.tts_format = tts_format
        self.tts_sample = tts_sample
        self.tts_text = text
        self.tts_vcn = vcn
        self.tts_speed = 50
        self.tts_volume = 50
        self.tts_pitch = 50
        self.tts_bright = 50
        self.tts_stream = b''
        self.punc = ''
        self.status = False
        self.message = ''
        self.code = 0
        self._pid = pid

    def get_sha256(self, timestamp):
        """
        Generate SHA256 signature for authentication.

        Args:
            timestamp: Current timestamp in milliseconds

        Returns:
            Uppercase hex string signature
        """
        hs = hashlib.sha256()
        hs.update((self.appkey + timestamp + self.secret).encode('utf-8'))
        signature = hs.hexdigest().upper()
        return signature

    def get_url(self):
        """
        Build complete WebSocket URL with authentication parameters.

        Returns:
            Complete WebSocket URL with query parameters
        """
        timestamp = str(int(time.time() * 1000))
        self.url = self.url + '?' + 'time=' + timestamp + '&appkey=' + \
                   self.appkey + '&sign=' + self.get_sha256(timestamp)
        return self.url

def on_message(ws, data, ws_parms):
    """
    WebSocket message handler.

    Args:
        ws: WebSocket instance
        data: Received data (str for JSON, bytes for audio)
        ws_parms: Ws_parms instance for storing state
    """
    if isinstance(data, str):
        print('Received text message:', data)
        try:
            json_object = json.loads(data)
            if 'end' in json_object and json_object['end'] and ws.sock.connected:
                print("Closing WebSocket as 'end' flag is True.")
                ws.close()
        except json.JSONDecodeError:
            print("String data is not a valid JSON format")

    if isinstance(data, bytes):
        ws_parms.tts_stream += data
        print(f'Received audio chunk: {len(data)} bytes')


def on_error(ws, error):
    """
    WebSocket error handler.

    Args:
        ws: WebSocket instance
        error: Exception or error message
    """
    print(f"WebSocket error: {error}")


def on_close(ws, close_status_code=None, close_msg=None):
    """
    WebSocket close handler.

    Args:
        ws: WebSocket instance
        close_status_code: Status code for closing
        close_msg: Close message
    """
    print(f"### WebSocket closed ###")
    if close_status_code:
        print(f"Status code: {close_status_code}")
    if close_msg:
        print(f"Close message: {close_msg}")

def on_open(ws, ws_parms):
    """
    WebSocket open handler - sends TTS request.

    Args:
        ws: WebSocket instance
        ws_parms: Ws_parms instance with TTS configuration
    """
    print('WebSocket connected!')

    def run(*args):
        """Send TTS request in a separate thread."""
        request_data = {
            "format": ws_parms.tts_format,
            "sample": ws_parms.tts_sample,
            "text": ws_parms.tts_text,
            "vcn": ws_parms.tts_vcn,
            "user_id": ws_parms.user_id,
            "speed": ws_parms.tts_speed,
            "volume": ws_parms.tts_volume,
            "pitch": ws_parms.tts_pitch,
            "bright": ws_parms.tts_bright,
        }
        print("Sending request:", request_data)
        ws.send(json.dumps(request_data))
        print(f"Voice: {ws_parms.tts_vcn}, Format: {ws_parms.tts_format}, Text: {ws_parms.tts_text[:50]}...")

    thread.start_new_thread(run, ())


def ensure_dir(dir_path):
    """
    Create directory if it doesn't exist.

    Args:
        dir_path: Directory path to create
    """
    os.makedirs(dir_path, exist_ok=True)


def do_ws(ws_parms):
    """
    Execute WebSocket TTS connection.

    Args:
        ws_parms: Ws_parms instance with TTS configuration

    Returns:
        Updated ws_parms instance with audio stream data
    """
    ws_url = ws_parms.get_url()
    websocket.enableTrace(False)
    print(f"Connecting to: {ws_url}")

    ws = websocket.WebSocketApp(
        url=ws_url,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = partial(on_open, ws_parms=ws_parms)
    ws.on_message = partial(on_message, ws_parms=ws_parms)

    ws.run_forever()

    # Check if audio data was received
    if len(ws_parms.tts_stream) == 0:
        print("No audio data received")
    else:
        print(f"Received {len(ws_parms.tts_stream)} bytes of audio data")

    return ws_parms
    

def write_results(ws_parms):
    """
    Write audio stream to file.

    Args:
        ws_parms: Ws_parms instance containing audio stream data

    Returns:
        Path to the created audio file
    """
    ensure_dir('results')
    timestamp = str(int(time.time()))
    filename = f"{timestamp}.{ws_parms.tts_format}"
    file_path = os.path.join('results', filename)

    with open(file_path, 'wb') as f:
        f.write(ws_parms.tts_stream)

    print(f"Audio saved to: {file_path} ({len(ws_parms.tts_stream)} bytes)")
    return file_path

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='UniSound TTS WebSocket Demo - Text to Speech conversion'
    )

    # Authentication
    parser.add_argument(
        '--appkey',
        type=str,
        default=os.getenv('UNISOUND_APPKEY', ''),
        help='UniSound AppKey (default: UNISOUND_APPKEY env var)'
    )
    parser.add_argument(
        '--secret',
        type=str,
        default=os.getenv('UNISOUND_SECRET', ''),
        help='UniSound Secret (default: UNISOUND_SECRET env var)'
    )

    # TTS parameters
    parser.add_argument(
        '--text',
        type=str,
        default='今天天气怎么样？',
        help='Text to convert to speech'
    )
    parser.add_argument(
        '--voice', '-v',
        type=str,
        default='xiaofeng-base',
        help='Voice name (default: xiaofeng-base)'
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        default='mp3',
        choices=['mp3', 'wav', 'pcm'],
        help='Output format (default: mp3)'
    )
    parser.add_argument(
        '--sample', '-s',
        type=str,
        default='24k',
        choices=['8k', '16k', '24k'],
        help='Sample rate (default: 24k)'
    )

    # Speech parameters
    parser.add_argument(
        '--speed',
        type=int,
        default=50,
        help='Speech speed 0-100 (default: 50)'
    )
    parser.add_argument(
        '--volume',
        type=int,
        default=50,
        help='Volume 0-100 (default: 50)'
    )
    parser.add_argument(
        '--pitch',
        type=int,
        default=50,
        help='Pitch 0-100 (default: 50)'
    )
    parser.add_argument(
        '--bright',
        type=int,
        default=50,
        help='Brightness 0-100 (default: 50)'
    )

    # Connection
    parser.add_argument(
        '--url',
        type=str,
        default='wss://ws-stts.hivoice.cn/v1/tts',
        help='WebSocket URL'
    )
    parser.add_argument(
        '--user-id',
        type=str,
        default='unisound-python-demo',
        help='User identifier'
    )

    # Other
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Do not clean up old log files'
    )

    return parser.parse_args()


def main():
    """Main entry point for the TTS demo."""
    args = parse_arguments()

    # Validate credentials
    if not args.appkey or not args.secret:
        print("Error: AppKey and Secret are required!")
        print("Set them via --appkey/--secret arguments or UNISOUND_APPKEY/UNISOUND_SECRET environment variables.")
        return 1

    # Validate speech parameters
    for param, name in [(args.speed, 'speed'), (args.volume, 'volume'),
                         (args.pitch, 'pitch'), (args.bright, 'bright')]:
        if not 0 <= param <= 100:
            print(f"Error: {name} must be between 0 and 100, got {param}")
            return 1

    # Create TTS parameters
    ws_parms = Ws_parms(
        url=args.url,
        appkey=args.appkey,
        secret=args.secret,
        pid=1,
        vcn=args.voice,
        text=args.text,
        tts_format=args.format,
        tts_sample=args.sample,
        user_id=args.user_id,
    )

    # Apply custom speech parameters
    ws_parms.tts_speed = args.speed
    ws_parms.tts_volume = args.volume
    ws_parms.tts_pitch = args.pitch
    ws_parms.tts_bright = args.bright

    # Execute TTS conversion
    print(f"\n{'='*60}")
    print(f"UniSound TTS - Text to Speech Conversion")
    print(f"{'='*60}")
    print(f"Text: {args.text}")
    print(f"Voice: {args.voice}")
    print(f"Format: {args.format}, Sample Rate: {args.sample}")
    print(f"Parameters - Speed: {args.speed}, Volume: {args.volume}, Pitch: {args.pitch}, Bright: {args.bright}")
    print(f"{'='*60}\n")

    try:
        do_ws(ws_parms)
        print('\nTTS conversion completed successfully!')

        # Save results
        if len(ws_parms.tts_stream) > 0:
            write_results(ws_parms)
            return 0
        else:
            print("Error: No audio data received")
            return 1

    except Exception as e:
        print(f"Error during TTS conversion: {e}")
        return 1


if __name__ == '__main__':
    exit(main())   
