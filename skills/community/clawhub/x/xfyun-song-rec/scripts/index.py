"""
Song Recognition Skill
Based on iFlytek Song Recognition API - using native Python methods
"""
import json
import os
import sys
import base64
import hashlib
import hmac
import requests
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time
from typing import Optional, Dict, Any


class SongRecognitionSkill:
    """
    Song Recognition Agent Skill

    Features:
    1. Recognize songs from audio files
    2. Return song name, artist and other information
    """

    def __init__(self, app_id: str, api_key: str, api_secret: str):
        """
        Initialize song recognizer

        Args:
            app_id: iFlytek Open Platform App ID
            api_key: iFlytek Open Platform API Key
            api_secret: iFlytek Open Platform API Secret
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.host_url = "https://cn-east-1.api.xf-yun.com/v1/private/s29ebee0d"
        self.timeout = 120

    def create_signed_url(self, api_url: str, method: str = "POST") -> str:
        """
        Generate signed URL for API authentication

        Args:
            api_url: API endpoint URL
            method: HTTP method

        Returns:
            Signed URL
        """
        try:
            parsed_url = urlparse(api_url)
            host = parsed_url.netloc
            path = parsed_url.path
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))

            signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(
                host, date, method, path
            )

            signature_sha = hmac.new(
                self.api_secret.encode('utf-8'),
                signature_origin.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()

            signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

            authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
                self.api_key, "hmac-sha256", "host date request-line", signature_sha
            )

            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

            values = {
                "authorization": authorization,
                "host": host,
                "date": date
            }

            return api_url + "?" + urlencode(values)
        except Exception as e:
            print(f"Failed to create signed URL: {str(e)}")
            raise

    def encode_file(self, file_path: str) -> Optional[str]:
        """
        Encode file to Base64 string

        Args:
            file_path: file path

        Returns:
            Base64 encoded string
        """
        try:
            with open(file_path, "rb") as file:
                encoded_string = base64.b64encode(file.read())
                return encoded_string.decode("utf-8")
        except Exception as e:
            print(f"File encoding failed: {str(e)}")
            return None

    def build_request_body(self, encoded_file: str, encoding: str = "lame", sample_rate: int = 16000) -> Dict[
        str, Any]:
        """
        Build API request body

        Args:
            encoded_file: Audio file to base64 string
            encoding: Audio encoding format
            sample_rate: Sample rate

        Returns:
            Request body dictionary
        """
        return {
            "header": {
                "app_id": self.app_id,
                "status": 3
            },
            "parameter": {
                "acr_music": {
                    "mode": "music",
                    "output_text": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "data": {
                    "encoding": encoding,
                    "sample_rate": sample_rate,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": 3,
                    "audio": encoded_file,
                    "frame_size": 0
                }
            }
        }

    def recognize_file(self, file_path: str, encoding: str = "lame", sample_rate: int = 16000) -> Optional[
        Dict[str, Any]]:
        """
        Recognize song from audio file

        Args:
            file_path: Audio file path
            encoding: Audio encoding format
            sample_rate: Sample rate

        Returns:
            Recognition result dictionary
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"Audio file not found: {file_path}"}

            print(f"Starting song recognition:")
            print(f"  Audio file: {file_path}")
            print(f"  Audio encoding: {encoding}")
            print(f"  Sample rate: {sample_rate}")

            encoded_file = self.encode_file(file_path)
            if not encoded_file:
                return {"error": "Failed to encode song file"}

            request_body = self.build_request_body(encoded_file, encoding, sample_rate)
            signed_url = self.create_signed_url(self.host_url, "POST")

            print("Calling song recognition API...")
            response = requests.post(
                signed_url,
                json=request_body,
                timeout=self.timeout
            )

            json_resp = response.json()

            # Parse result
            if json_resp["header"]['code'] == 0:
                text = json_resp['payload']['output_text']['text']
                result = base64.b64decode(text).decode("utf-8")
                result_data = json.loads(result)

                print(f"Song recognition successful")
                return {
                    "success": True,
                    "result": result_data.get("metadata"),
                    "raw_response": None
                }
            else:
                error_msg = json_resp.get('header', {}).get('message', 'Unknown error')
                print(f"Song recognition failed: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_code": json_resp["header"]['code'],
                    "raw_response": json_resp
                }

        except requests.exceptions.RequestException as e:
            print(f"Network request error: {str(e)}")
            return {
                "success": False,
                "error": f"Network request error: {str(e)}"
            }
        except Exception as e:
            print(f"Song recognition error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


def main():
    """
    Main function - supports dynamic parameter input
    """
    app_id = os.getenv('XF_SONG_APP_ID')
    api_key = os.getenv('XF_SONG_API_KEY')
    api_secret = os.getenv('XF_SONG_API_SECRET')

    if not app_id or not api_key or not api_secret:
        print("Missing required environment variables")
        print("Please configure the following environment variables:")
        print("export XF_SONG_APP_ID='your_app_id'")
        print("export XF_SONG_API_KEY='your_api_key'")
        print("export XF_SONG_API_SECRET='your_api_secret'")
        sys.exit(1)

    skill = SongRecognitionSkill(app_id, api_key, api_secret)

    if len(sys.argv) < 2:
        print("Please provide audio file path")
        print("Usage: python index.py <audio_path>")
        print("Example: python index.py humming.wav")
        sys.exit(1)

    audio_path = sys.argv[1]

    print(f"\n=== Song Recognition ===")
    result = skill.recognize_file(audio_path)

    if result:
        print("\nRecognition result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("success"):
            print("\n✓ Song recognition successful")
        else:
            print("\n✗ Song recognition failed")
    else:
        print("\n✗ Song recognition failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
