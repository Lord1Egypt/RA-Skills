"""
TTS Voice Service - 文本转语音服务
封装与后端 API 的交互逻辑

核心 API：
1. /sys/openapi/tts/voices - 获取声音列表
2. /sys/openapi/tts/submit - 提交 TTS 任务（异步）
3. /sys/openapi/tts/status/{taskId} - 检查任务状态
4. /sys/openapi/tts/upload - 上传音频到 OSS（中转）
5. /sys/openapi/tts/style/add - 添加定制声音

所有接口均支持 X-Api-Key header 认证，后端自动从 header 中提取 username
"""

import requests
from typing import Optional, Dict, List, Any
import time


class TTSService:
    """TTS 服务类"""

    def __init__(self, base_url: str, api_key: str):
        """
        初始化 TTS 服务

        Args:
            base_url: API 基础地址，如 "https://www.datamass.cn/ai-back"
            api_key: API Key（从 ~/.openclaw/config.json 读取）
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.timeout = 30
        self._username = None  # 缓存 username

    def get_username(self) -> str:
        """获取当前 API Key 关联的用户名"""
        if self._username is not None:
            return self._username

        url = f"{self.base_url}/sys/openapi/user/info"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            if result.get('success'):
                user_info = result.get('result', {})
                self._username = user_info.get('username')
                return self._username
            else:
                raise Exception(f"获取用户信息失败：{result.get('message', '')}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取用户信息失败：{str(e)}")

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def _get(self, endpoint: str) -> Dict[str, Any]:
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def get_voice_list(self, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        获取可用声音列表（用户上传的音频记录）

        Args:
            filters: 过滤条件 {"style": "", "sex": "", "style_type": ""}

        Returns:
            声音列表（来自 speech_audio_upload_style 表）
        """
        # API Key 认证模式下，后端自动从 header 获取 username，无需在参数中传递
        url = f"{self.base_url}/sys/openapi/tts/voices"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()

            if result.get('success') and result.get('result'):
                return result.get('result', [])
            return []
        except requests.exceptions.RequestException as e:
            return []

    def generate_speech(
        self,
        text: str,
        media_path: str,
        workflow_id: str = '73',
        style_id: str = '',
        audio_text: str = ''
    ) -> Dict[str, Any]:
        """
        生成语音（异步任务）- 核心接口

        Args:
            text: 要转换的文本
            media_path: 声音模型路径
            workflow_id: 工作流 ID，默认 "73"
            style_id: 声音风格 ID
            audio_text: 音频文本

        Returns:
            {"success": True, "task_id": "taskId_xxx"}
            或 {"success": False, "error": "..."}
        """
        # API Key 认证模式下，后端自动从 header 获取 username
        data = {
            "style_id": style_id,
            "media_path": media_path,
            "workflow_id": workflow_id,
            "inputText": text,
            "audio_text": audio_text
        }
        result = self._post('/sys/openapi/tts/submit', data)

        if result.get('success'):
            return {"success": True, "task_id": result.get('result', '')}
        return {"success": False, "error": result.get('message', '请求失败')}

    def check_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        检查任务状态

        Args:
            task_id: 任务 ID

        Returns:
            {"status": "processing|completed|error", "audio_url": "..."}
        """
        # 后端接口是 GET 方法，不需要传 body
        result = self._get('/sys/openapi/tts/status/' + task_id)

        if result.get('success') and result.get('result'):
            result_data = result.get('result', {})
            status = result_data.get('status', 0)

            if status == 2:
                return {"status": "completed", "audio_url": result_data.get('audio_url', ''), "file_path": result_data.get('audio_url', '')}
            elif status == 3:
                return {"status": "error", "message": "任务失败"}
            else:
                return {"status": "processing", "message": "任务处理中"}
        return {"status": "processing", "message": "任务处理中"}

    def wait_for_task(self, task_id: str, max_attempts: int = 60, interval: int = 5) -> Dict[str, Any]:
        """
        等待任务完成（轮询模式）

        Args:
            task_id: 任务 ID
            max_attempts: 最大轮询次数
            interval: 轮询间隔（秒）

        Returns:
            {"success": True, "audio_url": "..."} 或 {"success": False, "error": "..."}
        """
        for _ in range(max_attempts):
            result = self.check_task_status(task_id)

            if result['status'] == 'completed':
                return result
            elif result['status'] == 'error':
                return {"success": False, "error": "任务执行失败"}

            time.sleep(interval)

        return {"success": False, "error": f"任务超时（{max_attempts * interval}秒）"}

    def add_custom_voice(
        self,
        audio_url: str,
        style_name: str,
        audio_text: str,
        style_type: int = 2
    ) -> Dict[str, Any]:
        """
        添加定制声音（参考音频）

        Args:
            audio_url: 音频文件 URL（OSS 路径）
            style_name: 声音风格名称（如 "温柔女声"）
            audio_text: 音频对应的文本内容
            style_type: 类型 1=克隆，2=定制，默认 2

        Returns:
            {"success": True} 或 {"success": False, "error": "..."}
        """
        # API Key 认证模式下，后端自动从 header 获取 username
        data = {
            "style_type": style_type,
            "audio_url": audio_url,
            "style_name": style_name,
            "audio_text": audio_text
        }
        result = self._post('/sys/openapi/tts/style/add', data)

        if result.get('success'):
            return {"success": True}
        return {"success": False, "error": result.get('message', '请求失败')}

    def upload_audio(
        self,
        file_path: str,
        style_name: str = ""
    ) -> Dict[str, Any]:
        """
        上传音频文件到后端（后端中转上传到 OSS）

        Args:
            file_path: 本地音频文件路径
            style_name: 声音风格名称（可选）

        Returns:
            {"success": True, "audio_url": "https://..."} 或 {"success": False, "error": "..."}
        """
        url = f"{self.base_url}/sys/openapi/tts/upload"

        try:
            # 构造 biz 参数 - 格式：style_name
            if style_name:
                biz = style_name
            else:
                biz = "default"

            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'biz': biz}

                # 复制 headers，让 requests 自动设置 Content-Type
                upload_headers = {k: v for k, v in self.headers.items() if k.lower() != 'content-type'}

                response = requests.post(url, files=files, data=data, headers=upload_headers, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()

            if result.get('success') and result.get('result'):
                audio_url = result.get('result', {}).get('audio_url', '')
                return {"success": True, "audio_url": audio_url}
            return {"success": False, "error": result.get('message', '上传失败')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
        except FileNotFoundError:
            return {"success": False, "error": f"文件不存在：{file_path}"}
