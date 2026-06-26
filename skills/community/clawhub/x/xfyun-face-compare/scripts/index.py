"""
Face Compare Skill
Based on iFlytek Face Compare API - using native Python methods
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


class FaceCompareSkill:
    """
    Face Compare Agent Skill

    Features:
    1. Accept two face image paths
    2. Call iFlytek Face Compare API
    3. Return similarity score and comparison result
    """

    def __init__(self, app_id: str, api_key: str, api_secret: str):
        """
        Initialize face comparator

        Args:
            app_id: iFlytek Open Platform App ID
            api_key: iFlytek Open Platform API Key
            api_secret: iFlytek Open Platform API Secret
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.host_url = "https://api.xf-yun.com/v1/private/s67c9c78c"
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

    def build_request_body(self, image1_base64: str, format1: str,
                          image2_base64: str, format2: str) -> Dict[str, Any]:
        """
        Build API request body

        Args:
            image1_base64: Base64 encoded first image
            format1: First image format
            image2_base64: Base64 encoded second image
            format2: Second image format

        Returns:
            Request body dictionary
        """
        return {
            "header": {
                "app_id": self.app_id,
                "status": 3,
            },
            "parameter": {
                "s67c9c78c": {
                    "service_kind": "face_compare",
                    "face_compare_result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "plain"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": format1,
                    "image": image1_base64,
                },
                "input2": {
                    "encoding": format2,
                    "image": image2_base64,
                }
            }
        }

    def validate_image_path(self, image_path: str) -> bool:
        """
        Validate image path

        Args:
            image_path: Image file path

        Returns:
            True if valid, False otherwise
        """
        if not image_path or not os.path.exists(image_path):
            print(f"Invalid image path or file not found: {image_path}")
            return False

        if not os.path.isfile(image_path):
            print(f"Path is not a file: {image_path}")
            return False

        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        _, ext = os.path.splitext(image_path.lower())
        if ext not in valid_extensions:
            print(f"Unsupported image format: {ext}, supported formats: {valid_extensions}")
            return False

        return True

    def encode_image(self, image_path: str) -> Optional[str]:
        """
        Encode image to Base64 string

        Args:
            image_path: Image file path

        Returns:
            Base64 encoded string
        """
        try:
            with open(image_path, "rb") as file:
                encoded_string = base64.b64encode(file.read())
                return encoded_string.decode("utf-8")
        except Exception as e:
            print(f"Image encoding failed: {str(e)}")
            return None

    def get_image_format(self, image_path: str) -> str:
        """
        Get image format from file path

        Args:
            image_path: Image file path

        Returns:
            Image format (jpg/png/bmp)
        """
        _, ext = os.path.splitext(image_path.lower())
        format_map = {
            '.jpg': 'jpg',
            '.jpeg': 'jpg',
            '.png': 'png',
            '.bmp': 'bmp'
        }
        return format_map.get(ext, 'jpg')

    def compare_faces(self, image1_path: str, image2_path: str) -> Optional[Dict[str, Any]]:
        """
        Compare two face images

        Args:
            image1_path: First image path
            image2_path: Second image path

        Returns:
            Comparison result dictionary
        """
        try:
            if not self.validate_image_path(image1_path):
                return {"error": f"Invalid first image path: {image1_path}"}

            if not self.validate_image_path(image2_path):
                return {"error": f"Invalid second image path: {image2_path}"}

            print(f"Starting face comparison:")
            print(f"  Image 1: {image1_path}")
            print(f"  Image 2: {image2_path}")

            encoded_image1 = self.encode_image(image1_path)
            if not encoded_image1:
                return {"error": "Failed to encode first image"}

            encoded_image2 = self.encode_image(image2_path)
            if not encoded_image2:
                return {"error": "Failed to encode second image"}

            format1 = self.get_image_format(image1_path)
            format2 = self.get_image_format(image2_path)

            request_body = self.build_request_body(
                encoded_image1, format1,
                encoded_image2, format2
            )

            signed_url = self.create_signed_url(self.host_url, "POST")

            print("Calling face compare API...")
            response = requests.post(
                signed_url,
                json=request_body,
                timeout=self.timeout
            )
            response.raise_for_status()

            json_resp = response.json()
            print(f"API response: {json_resp}")

            if json_resp["header"]['code'] == 0:
                text = json_resp['payload']['face_compare_result']['text']
                result = base64.b64decode(text).decode("utf-8")
                result_data = json.loads(result)

                print(f"Face comparison successful")
                print(f"Similarity score: {result_data.get('score', 'N/A')}")

                return {
                    "success": True,
                    "result": result_data,
                    "raw_response": json_resp
                }
            else:
                error_msg = json_resp.get('header', {}).get('message', 'Unknown error')
                print(f"Face comparison failed: {error_msg}")
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
            print(f"Face comparison error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


def main():
    """
    Main function - supports dynamic parameter input
    """
    app_id = os.getenv('XF_FACE_APP_ID')
    api_key = os.getenv('XF_FACE_API_KEY')
    api_secret = os.getenv('XF_FACE_API_SECRET')

    if not app_id or not api_key or not api_secret:
        print("Missing required environment variables")
        print("Please configure the following environment variables:")
        print("set XF_FACE_APP_ID='your_app_id'")
        print("set XF_FACE_API_KEY='your_api_key'")
        print("set XF_FACE_API_SECRET='your_api_secret'")
        sys.exit(1)

    face_compare_skill = FaceCompareSkill(app_id, api_key, api_secret)

    image1_path = None
    image2_path = None

    if len(sys.argv) > 1:
        image1_path = sys.argv[1]

    if len(sys.argv) > 2:
        image2_path = sys.argv[2]

    if not image1_path or not image2_path:
        print("Please provide two image paths")
        print("Usage: python index.py <image1_path> <image2_path>")
        print("Example: python index.py face1.jpg face2.jpg")
        sys.exit(1)

    print(f"\n=== Face Comparison ===")
    result = face_compare_skill.compare_faces(image1_path, image2_path)

    if result:
        print("\nComparison result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("success"):
            print("\n✓ Face comparison successful")
        else:
            print("\n✗ Face comparison failed")
    else:
        print("\n✗ Face comparison failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
