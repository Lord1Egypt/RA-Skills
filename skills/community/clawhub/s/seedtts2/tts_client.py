#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包 SeedTTS 2.0 Python 封装库

简化语音合成调用，自动从配置读取凭证。

使用示例：
    from tts_client import SeedTTS2
    
    tts = SeedTTS2()
    tts.say("你好，这是测试")
    tts.say("你好", speaker="zh_male_ruyayichen_uranus_bigtts")
    tts.say_and_play("你好")
"""

import requests
import base64
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Union


class SeedTTS2:
    """豆包 SeedTTS 2.0 语音合成客户端"""
    
    # 默认配置
    DEFAULT_API_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
    DEFAULT_FORMAT = "mp3"
    DEFAULT_SAMPLE_RATE = 24000
    DEFAULT_TIMEOUT = 60  # 超时时间（秒）
    
    # JARVIS 默认音色
    DEFAULT_SPEAKER = "zh_male_ruyayichen_uranus_bigtts"  # 儒雅逸辰 2.0
    
    # 类变量：复用 Session
    _session: Optional[requests.Session] = None
    
    def __init__(
        self,
        app_id: Optional[str] = None,
        access_token: Optional[str] = None,
        resource_id: Optional[str] = None,
        api_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        初始化 SeedTTS2 客户端
        
        参数优先级：
        1. 构造函数参数
        2. 环境变量
        3. 配置文件 (~/.openclaw/openclaw.json)
        
        Args:
            app_id: 火山引擎 APP ID
            access_token: 火山引擎 Access Token
            resource_id: 资源 ID（默认 seed-tts-2.0）
            api_url: API 端点 URL
            timeout: 请求超时时间（秒），默认 60 秒
        """
        # 从多种来源加载配置
        self.app_id = app_id or self._load_env("VOLCANO_APP_ID") or self._load_config("app_id")
        self.access_token = access_token or self._load_env("VOLCANO_ACCESS_TOKEN") or self._load_config("access_token")
        self.resource_id = resource_id or self._load_env("VOLCANO_RESOURCE_ID", "seed-tts-2.0")
        self.api_url = api_url or self._load_env("VOLCANO_API_URL", self.DEFAULT_API_URL)
        self.timeout = timeout
        
        # 验证必要配置
        self._validate_config()
        
        # 输出目录：固定到 ~/.openclaw/tts_output
        self.output_dir = Path.home() / ".openclaw" / "tts_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 Session（复用）
        if SeedTTS2._session is None:
            SeedTTS2._session = requests.Session()
    
    def _load_env(self, key: str, default: str = None) -> Optional[str]:
        """从环境变量加载配置"""
        return os.environ.get(key, default)
    
    def _load_config(self, key: str) -> Optional[str]:
        """从 OpenClaw 配置文件加载"""
        config_paths = [
            Path.home() / ".openclaw" / "openclaw.json",
            Path(__file__).parent.parent / "openclaw.json",
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    # 尝试从 skills.entries.seedtts2.env 加载
                    env = config.get("skills", {}).get("entries", {}).get("seedtts2", {}).get("env", {})
                    
                    key_map = {
                        "app_id": "VOLCANO_APP_ID",
                        "access_token": "VOLCANO_ACCESS_TOKEN",
                        "secret_key": "VOLCANO_SECRET_KEY",
                    }
                    
                    env_key = key_map.get(key, f"VOLCANO_{key.upper()}")
                    value = env.get(env_key)
                    if value:
                        return value
                except Exception as e:
                    continue
        
        return None
    
    def _validate_config(self):
        """验证必要配置"""
        missing = []
        if not self.app_id:
            missing.append("APP_ID")
        if not self.access_token:
            missing.append("ACCESS_TOKEN")
        
        if missing:
            raise ValueError(
                f"缺少必要配置：{', '.join(missing)}\n"
                f"请设置环境变量或在 openclaw.json 中配置\n"
                f"环境变量示例:\n"
                f"  export VOLCANO_APP_ID=your_app_id\n"
                f"  export VOLCANO_ACCESS_TOKEN=your_token"
            )
    
    def _make_headers(self, request_id: str = None) -> Dict[str, str]:
        """构建请求头"""
        headers = {
            "Content-Type": "application/json",
            "X-Api-App-Id": self.app_id,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": self.resource_id,
            # 添加 Authorization header（部分 API 节点需要）
            "Authorization": f"Bearer; {self.access_token}",
        }
        
        if request_id:
            headers["X-Api-Request-Id"] = request_id
        
        return headers
    
    def _make_payload(
        self,
        text: str,
        speaker: str,
        audio_format: str = DEFAULT_FORMAT,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
    ) -> Dict:
        """构建请求体"""
        return {
            "user": {"uid": "jarvis_client"},
            "req_params": {
                "text": text,
                "speaker": speaker,
                "audio_params": {
                    "format": audio_format,
                    "sample_rate": sample_rate,
                }
            }
        }
    
    def _parse_response(self, response) -> Optional[bytes]:
        """
        解析响应，提取音频数据
        
        结束条件（满足任一即结束）：
        1. code == 0 且 data 为 null（官方文档）
        2. code == 20000000（兼容旧版本）
        """
        audio_chunks = []
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    
                    # 检查是否有音频数据
                    if data.get("data"):
                        audio_chunks.append(data["data"])
                    
                    # 检查结束标记（两种格式）
                    code = data.get("code")
                    has_data = data.get("data") is not None
                    
                    # 官方格式：code=0 且 data=null
                    if code == 0 and not has_data:
                        break
                    
                    # 兼容格式：code=20000000
                    if code == 20000000:
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        if audio_chunks:
            return b"".join([base64.b64decode(c) for c in audio_chunks])
        return None
    
    def synthesize(
        self,
        text: str,
        speaker: str = None,
        output: str = None,
        audio_format: str = DEFAULT_FORMAT,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        request_id: str = None,
    ) -> Optional[str]:
        """
        语音合成
        
        Args:
            text: 要合成的文本
            speaker: 音色 ID（默认使用 JARVIS 官方音色）
            output: 输出文件路径（默认自动生成）
            audio_format: 音频格式（mp3/wav）
            sample_rate: 采样率
            request_id: 请求 ID（用于追踪）
        
        Returns:
            生成的音频文件路径，失败返回 None
        """
        speaker = speaker or self.DEFAULT_SPEAKER
        request_id = request_id or f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        headers = self._make_headers(request_id)
        payload = self._make_payload(text, speaker, audio_format, sample_rate)
        
        try:
            # 复用 Session（性能优化）
            response = SeedTTS2._session.post(
                self.api_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=self.timeout  # 可配置超时时间
            )
            
            if response.status_code != 200:
                print(f"❌ 请求失败：{response.text[:200]}", file=sys.stderr)
                return None
            
            audio_bytes = self._parse_response(response)
            if not audio_bytes:
                print("❌ 未获取到音频数据", file=sys.stderr)
                return None
            
            # 确定输出文件路径
            if output:
                output_path = Path(output)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_speaker = speaker.replace('/', '_')
                output_path = self.output_dir / f"{timestamp}_{safe_speaker}.{audio_format}"
            
            # 确保目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            with open(output_path, 'wb') as f:
                f.write(audio_bytes)
            
            print(f"✅ 已生成：{output_path} ({len(audio_bytes)/1024:.1f} KB)")
            return str(output_path)
            
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时（{self.timeout}秒），长文本建议增加超时时间", file=sys.stderr)
            return None
        except Exception as e:
            print(f"❌ 异常：{e}", file=sys.stderr)
            return None
    
    def say(
        self,
        text: str,
        speaker: str = None,
        output: str = None,
    ) -> Optional[str]:
        """
        简化版语音合成（推荐）
        
        Args:
            text: 要合成的文本
            speaker: 音色 ID（可选）
            output: 输出文件路径（可选）
        
        Returns:
            生成的音频文件路径
        """
        return self.synthesize(text, speaker=speaker, output=output)
    
    def say_and_play(
        self,
        text: str,
        speaker: str = None,
        remove_after_play: bool = False,
    ) -> bool:
        """
        语音合成并播放
        
        Args:
            text: 要合成的文本
            speaker: 音色 ID（可选）
            remove_after_play: 播放后是否删除文件
        
        Returns:
            是否成功播放
        """
        output = self.say(text, speaker)
        if not output:
            return False
        
        try:
            # 根据系统选择播放器
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['afplay', output], check=True)
            elif sys.platform == 'linux':
                subprocess.run(['aplay', output], check=True)
            elif sys.platform == 'win32':
                subprocess.run(['start', output], shell=True, check=True)
            else:
                print(f"⚠️  未知平台，无法自动播放：{output}", file=sys.stderr)
                return False
            
            if remove_after_play:
                os.remove(output)
            
            return True
            
        except Exception as e:
            print(f"❌ 播放失败：{e}", file=sys.stderr)
            return False
    
    def batch_generate(
        self,
        texts: List[Union[str, Dict]],
        output_dir: str = None,
    ) -> List[str]:
        """
        批量生成语音
        
        Args:
            texts: 文本列表，可以是字符串或字典
                   字典格式：{"text": "文本", "speaker": "音色 ID", "output": "输出路径"}
            output_dir: 输出目录（可选）
        
        Returns:
            生成的音频文件路径列表
        """
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        for i, item in enumerate(texts):
            if isinstance(item, str):
                text = item
                speaker = None
                output = None
            else:
                text = item.get("text")
                speaker = item.get("speaker")
                output = item.get("output")
            
            if output and output_dir:
                output = str(Path(output_dir) / Path(output).name)
            
            result = self.say(text, speaker=speaker, output=output)
            if result:
                results.append(result)
        
        return results
    
    def list_speakers(self) -> List[Dict]:
        """
        列出常用音色
        
        Returns:
            音色列表
        """
        return [
            {"id": "zh_male_ruyayichen_uranus_bigtts", "name": "儒雅逸辰 2.0", "desc": "成熟稳重（JARVIS 官方）"},
            {"id": "zh_male_m191_uranus_bigtts", "name": "云舟", "desc": "沉稳大气"},
            {"id": "zh_male_sophie_uranus_bigtts", "name": "魅力苏菲 2.0", "desc": "磁性魅力"},
            {"id": "zh_female_vv_uranus_bigtts", "name": "Vivi 2.0", "desc": "表现力强"},
            {"id": "zh_female_tianmeixiaoyuan_uranus_bigtts", "name": "甜美小源 2.0", "desc": "甜美温柔"},
            {"id": "zh_female_xiaohe_uranus_bigtts", "name": "小何", "desc": "自然亲切"},
            {"id": "en_male_tim_uranus_bigtts", "name": "Tim", "desc": "标准美式"},
            {"id": "en_female_dacey_uranus_bigtts", "name": "Dacey", "desc": "标准英式"},
        ]
    
    @classmethod
    def cleanup(cls):
        """清理 Session（程序退出时调用）"""
        if cls._session:
            cls._session.close()
            cls._session = None


# 便捷函数
def say(text: str, speaker: str = None, output: str = None) -> Optional[str]:
    """快捷函数：语音合成"""
    tts = SeedTTS2()
    return tts.say(text, speaker=speaker, output=output)


def say_and_play(text: str, speaker: str = None) -> bool:
    """快捷函数：语音合成并播放"""
    tts = SeedTTS2()
    return tts.say_and_play(text, speaker=speaker)


def batch_generate(texts: List[Union[str, Dict]], output_dir: str = None) -> List[str]:
    """快捷函数：批量生成"""
    tts = SeedTTS2()
    return tts.batch_generate(texts, output_dir=output_dir)


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="豆包 SeedTTS 2.0 语音合成")
    parser.add_argument("text", nargs="?", help="要合成的文本")
    parser.add_argument("-s", "--speaker", default=None, help="音色 ID")
    parser.add_argument("-o", "--output", default=None, help="输出文件路径")
    parser.add_argument("-p", "--play", action="store_true", help="合成后播放")
    parser.add_argument("-l", "--list", action="store_true", help="列出可用音色")
    parser.add_argument("-t", "--timeout", type=int, default=60, help="超时时间（秒）")
    
    args = parser.parse_args()
    
    tts = SeedTTS2(timeout=args.timeout)
    
    if args.list:
        print("可用音色：")
        for sp in tts.list_speakers():
            print(f"  {sp['id']}\n    - {sp['name']}: {sp['desc']}")
        sys.exit(0)
    
    if not args.text:
        parser.print_help()
        sys.exit(1)
    
    if args.play:
        success = tts.say_and_play(args.text, speaker=args.speaker)
        sys.exit(0 if success else 1)
    else:
        result = tts.say(args.text, speaker=args.speaker, output=args.output)
        sys.exit(0 if result else 1)
