# -*- coding: utf-8 -*-
"""
UniSound ASR Transcribe Script
语音文件转写脚本 - 支持命令行调用
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ==================== 配置类 ====================
@dataclass
class ASRConfig:
    """ASR配置类"""

    # 默认配置 - 直接填入你的凭据
    base_url: str = "http://af-asr.uat.hivoice.cn"
    appkey: str = ""
    secret: str = ""
    userid: str = "unisound-python-demo"

    domain: str = "finance"
    audiotype: str = "wav"
    use_hot_data: bool = True

    punction: str = "beauty"
    callbackurl: str = ""

    timeout: int = 30
    max_retries: int = 3
    poll_interval: int = 5
    max_poll_attempts: int = 120

    @classmethod
    def from_env(cls) -> "ASRConfig":
        """从环境变量加载配置（环境变量会覆盖默认值）"""
        return cls(
            base_url=os.getenv("UNISOUND_BASE_URL", cls.base_url),
            appkey=os.getenv("UNISOUND_APPKEY", cls.appkey),
            secret=os.getenv("UNISOUND_SECRET", cls.secret),
            userid=os.getenv("UNISOUND_USERID", cls.userid),
            audiotype=os.getenv("UNISOUND_AUDIOTYPE", cls.audiotype),
            use_hot_data=os.getenv("UNISOUND_USE_HOT_DATA", str(cls.use_hot_data)).lower() == "true",
        )

    @property
    def urls(self) -> dict[str, str]:
        """获取所有API端点"""
        base = self.base_url
        return {
            "upload_init": f"{base}/utservice/v2/trans/append_upload/init",
            "upload": f"{base}/utservice/v2/trans/append_upload/upload",
            "upload_status": f"{base}/utservice/v2/trans/append_upload/status",
            "transcribe": f"{base}/utservice/v4/trans/transcribe",
            "text": f"{base}/utservice/v2/trans/text",
        }


# ==================== 异常类 ====================
class ASRError(Exception):
    """ASR基础异常类"""
    pass


class ASRAPIError(ASRError):
    """API调用错误"""

    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(f"[{error_code}] {message}")


# ==================== 工具函数 ====================
def calculate_file_md5(filepath: str) -> str:
    """计算文件的MD5值"""
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def get_timestamp() -> int:
    """获取当前时间戳"""
    return int(time.time())


# ==================== ASR客户端类 ====================
class ASRClient:
    """ASR语音识别客户端"""

    def __init__(self, config: ASRConfig):
        self.config = config
        self.session = requests.Session()

        retry_strategy = Retry(
            total=config.max_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _generate_signature(self, params: dict[str, Any]) -> str:
        """生成签名"""
        sorted_params = sorted(params.items())
        sign_str = self.config.secret + "".join(v for _, v in sorted_params) + self.config.secret
        return hashlib.sha1(sign_str.encode("utf-8")).hexdigest().upper()

    def _build_params(self, **kwargs) -> dict[str, str]:
        """构建带签名的请求参数"""
        params = {
            "appkey": self.config.appkey,
            "timestamp": str(get_timestamp()),
            **kwargs,
        }
        params["signature"] = self._generate_signature(params)
        return params

    def _request(self, method: str, url: str, **kwargs) -> bytes:
        """发送HTTP请求"""
        response = self.session.request(
            method=method,
            url=url,
            timeout=self.config.timeout,
            **kwargs,
        )
        response.raise_for_status()
        return response.content

    def _parse_response(self, data: bytes) -> dict[str, Any]:
        """解析响应数据"""
        return json.loads(data.decode("utf-8"))

    def _check_error(self, response: dict[str, Any]) -> None:
        """检查响应错误"""
        error_code = response.get("error_code", -1)
        if error_code != 0:
            message = response.get("message", "Unknown error")
            raise ASRAPIError(error_code, message)

    def init_upload(self) -> str:
        """初始化上传"""
        url = self.config.urls["upload_init"]
        params = self._build_params(userid=self.config.userid)
        response_data = self._request("GET", url, params=params)
        response = self._parse_response(response_data)
        self._check_error(response)
        return response.get("task_id")

    def upload_file(self, task_id: str, filepath: str) -> str:
        """上传音频文件"""
        url = self.config.urls["upload"]
        file_md5 = calculate_file_md5(filepath)
        params = self._build_params(
            userid=self.config.userid,
            task_id=task_id,
            md5=file_md5,
            audiotype=self.config.audiotype,
        )

        with open(filepath, "rb") as f:
            response_data = self._request("POST", url, params=params, data=f)

        response = self._parse_response(response_data)
        self._check_error(response)
        return task_id

    def start_transcribe(self, task_id: str, filepath: str) -> str:
        """开始转写"""
        file_md5 = calculate_file_md5(filepath)
        url = self.config.urls["transcribe"]

        params = self._build_params(
            userid=self.config.userid,
            task_id=task_id,
            audiotype=self.config.audiotype,
            domain=self.config.domain,
            md5=file_md5,
            use_hot_data=str(self.config.use_hot_data).lower(),
            callbackurl=self.config.callbackurl,
            num_convert="true",
            vocab_id="a7ea15d097184eb0814d1e588f45f118"
        )

        response_data = self._request("GET", url, params=params)
        response = self._parse_response(response_data)
        self._check_error(response)
        return response.get("task_id")

    def get_transcribe_result(self, task_id: str) -> dict[str, Any]:
        """获取转写结果"""
        url = self.config.urls["text"]
        params = self._build_params(task_id=task_id)
        response_data = self._request("GET", url, params=params)
        return self._parse_response(response_data)

    def poll_transcribe_result(self, task_id: str) -> dict[str, Any]:
        """轮询获取转写结果"""
        for attempt in range(self.config.max_poll_attempts):
            result = self.get_transcribe_result(task_id)
            self._check_error(result)

            status = result.get("status")
            if status == "done":
                return result

            if attempt % 10 == 0:
                print(f"  转写中... ({status})", file=sys.stderr)

            time.sleep(self.config.poll_interval)

        raise ASRError(f"转写超时: {task_id}")

    def transcribe(self, filepath: str) -> dict[str, Any]:
        """完整的转写流程"""
        # 1. 初始化上传
        task_id = self.init_upload()
        print(f"  task_id: {task_id}", file=sys.stderr)

        # 2. 上传文件
        print(f"  上传文件...", file=sys.stderr)
        self.upload_file(task_id, filepath)

        # 3. 开始转写
        print(f"  开始转写...", file=sys.stderr)
        transcribe_task_id = self.start_transcribe(task_id, filepath)

        # 4. 轮询结果
        print(f"  等待转写完成...", file=sys.stderr)
        result = self.poll_transcribe_result(transcribe_task_id)

        return result

    def extract_text(self, result: dict[str, Any]) -> str:
        """从转写结果中提取文本"""
        texts = []
        if "results" in result:
            for item in result["results"]:
                if "text" in item:
                    texts.append(item["text"])
        return "".join(texts)

    def close(self):
        """关闭客户端"""
        self.session.close()


# ==================== 命令行接口 ====================
def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="UniSound ASR - 语音文件转写工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s audio.wav
  %(prog)s audio.wav --out result.txt
  %(prog)s audio.wav --json --out result.json
  %(prog)s audio.wav --domain finance
  %(prog)s audio.wav --format mp3
        """,
    )

    parser.add_argument("audio", help="音频文件路径")
    parser.add_argument("--out", "-o", help="输出文件路径（默认输出到stdout）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式（包含完整结果）")
    parser.add_argument("--format", help="音频格式（默认: wav）", default="wav")
    parser.add_argument("--domain", help="领域（默认: other）", default="other")

    args = parser.parse_args()

    # 检查文件是否存在
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"错误: 音频文件不存在: {args.audio}", file=sys.stderr)
        sys.exit(1)

    # 加载配置（优先使用环境变量，否则使用默认配置）
    config = ASRConfig.from_env()
    config.audiotype = args.format
    config.domain = args.domain

    # 执行转写
    print(f"开始转写: {args.audio}", file=sys.stderr)

    client = ASRClient(config)
    try:
        result = client.transcribe(str(audio_path))
        text = client.extract_text(result)

        # 输出结果
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            output = text

        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"结果已保存到: {args.out}", file=sys.stderr)
        else:
            print(output)

    except ASRError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    main()
