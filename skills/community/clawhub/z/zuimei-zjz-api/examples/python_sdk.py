"""
最美证件照 API Python SDK

安装依赖：pip install requests

环境变量：
export ZUIMEI_API_KEY="your_api_key"
export ZUIMEI_SECRET_KEY="your_secret_key"
"""

import hashlib
import hmac
import os
import secrets
import time
from decimal import Decimal
from typing import Any

import requests


class ZuimeiApiError(Exception):
    """最美证件照 API 错误"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class ZuimeiZjzClient:
    """最美证件照 API 客户端"""

    BASE_URL = "https://idphoto.huipai.vip"

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("ZUIMEI_API_KEY")
        self.secret_key = secret_key or os.environ.get("ZUIMEI_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError("请设置 ZUIMEI_API_KEY 和 ZUIMEI_SECRET_KEY")

    def _build_content_sha256(self, fields: dict[str, Any]) -> str:
        canonical_lines = []
        for key in sorted(fields.keys()):
            value = fields[key]
            if value is None:
                continue
            if isinstance(value, bool):
                value = "true" if value else "false"
            elif isinstance(value, float):
                decimal_value = Decimal(str(value)).normalize()
                value = format(decimal_value, "f").rstrip("0").rstrip(".") if decimal_value != 0 else "0"
            canonical_lines.append(f"{key}={value}")
        return hashlib.sha256("\n".join(canonical_lines).encode()).hexdigest()

    def _generate_signature(self, url: str, timestamp: str, nonce: str, content_sha256: str) -> str:
        sign_str = f"POST\n{url}\n{timestamp}\n{nonce}\n{content_sha256}"
        secret = self.secret_key
        if not secret:
            raise ValueError("secret_key 未设置")
        return hmac.new(secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()

    def _call_api(self, endpoint: str, files: dict | None = None, data: dict | None = None) -> dict:
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)

        fields = {}
        if files:
            for name, file_info in files.items():
                if isinstance(file_info, tuple) and len(file_info) >= 2:
                    fields[name] = hashlib.sha256(file_info[1]).hexdigest()
        if data:
            fields.update(data)

        content_sha256 = self._build_content_sha256(fields)
        signature = self._generate_signature(endpoint, timestamp, nonce, content_sha256)

        headers = {
            "X-API-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Signature": signature,
            "X-Content-SHA256": content_sha256,
            "X-Sign-Version": "v2",
        }

        response = requests.post(f"{self.BASE_URL}{endpoint}", files=files, data=data, headers=headers)
        result = response.json()

        if result.get("code") != 0:
            raise ZuimeiApiError(result.get("code", -1), result.get("message", "未知错误"))

        return result

    def id_photo(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
        width: int = 295,
        height: int = 413,
        background_color: str = "#FFFFFF",
        beautify: bool = False,
        return_hd_transparent: bool = False,
    ) -> dict:
        """一键证件照"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        return self._call_api(
            "/api/v1/photo/id-photo",
            files={"image": (filename, image_bytes, "image/jpeg")},
            data={
                "width": width,
                "height": height,
                "background_color": background_color,
                "beautify_flag": beautify,
                "return_hd_transparent": return_hd_transparent,
            },
        )

    def segment_portrait(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
    ) -> dict:
        """智能抠图"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        return self._call_api(
            "/api/v1/segment/portrait",
            files={"image": (filename, image_bytes, "image/jpeg")},
        )

    def segment_background(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
        background_color: str = "#FFFFFF",
        quality: str | None = None,
    ) -> dict:
        """换背景色"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        data = {"background_color": background_color}
        if quality:
            data["quality"] = quality

        return self._call_api(
            "/api/v1/segment/background",
            files={"image": (filename, image_bytes, "image/jpeg")},
            data=data,
        )

    def enhance(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
        fidelity: float = 0.3,
        use_sr: bool = False,
    ) -> dict:
        """人脸增强"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        return self._call_api(
            "/api/v1/photo/enhance",
            files={"image": (filename, image_bytes, "image/jpeg")},
            data={"fidelity": fidelity, "use_sr": use_sr},
        )

    def layout(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
        layout_type: str = "6inch",
        crop_line: bool = False,
    ) -> dict:
        """排版照"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        return self._call_api(
            "/api/v1/photo/layout",
            files={"image": (filename, image_bytes, "image/jpeg")},
            data={"layout_type": layout_type, "crop_line": crop_line},
        )

    def edit(
        self,
        image_path: str | None = None,
        image_bytes: bytes | None = None,
        width: int | None = None,
        height: int | None = None,
        dpi: int = 300,
        output_format: str = "jpeg",
    ) -> dict:
        """图片编辑"""
        if image_path:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(image_path)
        elif image_bytes:
            filename = "image.jpg"
        else:
            raise ValueError("请提供 image_path 或 image_bytes")

        data = {"dpi": dpi, "output_format": output_format}
        if width:
            data["width"] = width
        if height:
            data["height"] = height

        return self._call_api(
            "/api/v1/photo/edit",
            files={"image": (filename, image_bytes, "image/jpeg")},
            data=data,
        )


if __name__ == "__main__":
    client = ZuimeiZjzClient()

    # 一键证件照（默认不开启美颜）
    result = client.id_photo("photo.jpg", width=295, height=413, background_color="#438EDB")
    print("证件照:", result)

    # 智能抠图
    result = client.segment_portrait("photo.jpg")
    print("抠图:", result)

    # 换背景色
    result = client.segment_background("photo.jpg", background_color="#FFFFFF;#438EDB", quality="hd-pro")
    print("换底色:", result)

    # 人脸增强
    result = client.enhance("blurry.jpg", fidelity=0.3, use_sr=True)
    print("增强:", result)

    # 排版照
    result = client.layout("id_photo.jpg", layout_type="6inch")
    print("排版:", result)

    # 图片编辑
    result = client.edit("photo.jpg", width=800, height=600)
    print("编辑:", result)
