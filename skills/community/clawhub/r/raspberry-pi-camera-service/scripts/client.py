#!/usr/bin/env python3
"""
树莓派摄像头 HTTP 客户端 SDK
"""
from __future__ import annotations

import logging
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Generator

import requests

logger = logging.getLogger(__name__)


class CameraClientError(Exception):
    """SDK 基础异常"""
    pass


class ServiceBusyError(CameraClientError):
    """服务被占用"""
    pass


class APIError(CameraClientError):
    """API 调用失败"""
    pass


class CameraClient:
    def __init__(
        self,
        base_url: str = "http://localhost:27793",
        timeout: int = 30,
        heartbeat_enabled: bool = True  # 新增：是否启用自动心跳
    ) -> None:
        self.base_url: str = base_url.rstrip("/")
        self.timeout: int = timeout
        self.session: requests.Session = requests.Session()
        self._current_job_id: str | None = None
        self._current_session_id: str | None = None  # 新增：会话ID
        self._heartbeat_thread: threading.Thread | None = None  # 心跳线程
        self._heartbeat_enabled: bool = heartbeat_enabled
        self._heartbeat_interval: int = 10  # 心跳间隔（秒）
        self._heartbeat_stop_event: threading.Event = threading.Event()
    
    def __enter__(self) -> CameraClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any
    ) -> None:
        # 停止心跳线程
        self._stop_heartbeat()
        if self._current_job_id or self._current_session_id:
            try:
                self.stop_recording(keep_video=False, reason="Client exception")
            except Exception:
                pass  # 忽略清理错误
        self.session.close()
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs: Any
    ) -> dict[str, Any]:
        url: str = f"{self.base_url}{endpoint}"
        try:
            response: requests.Response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            if response.status_code == 423:
                raise ServiceBusyError("服务正忙，摄像头被占用")
            raise APIError(f"HTTP {response.status_code}: {response.text}")
        except requests.RequestException as e:
            raise CameraClientError(f"请求失败: {e}")
    
    def get_status(self) -> dict[str, Any]:
        return self._request("GET", "/status")
    
    def start_recording(
        self,
        task_name: str = "",
        output_format: str = "h264",
        keep_original: bool = False,
        gif_params: dict[str, Any] | None = None,
        client_id: str | None = None,
        heartbeat_timeout: int = 30  # 新增：心跳超时时间
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "client_id": client_id or f"client_{int(time.time())}",
            "task_name": task_name,
            "output_format": output_format,
            "keep_original": keep_original,
            "heartbeat_timeout": heartbeat_timeout  # 新增
        }

        if gif_params and output_format == "gif":
            payload["gif_params"] = gif_params

        result: dict[str, Any] = self._request("POST", "/start", json=payload)
        if result.get("success"):
            self._current_job_id = result.get("execution_id")
            self._current_session_id = result.get("session_id")  # 新增
            # 启动自动心跳线程（如果启用）
            if self._heartbeat_enabled and self._current_session_id:
                self._start_heartbeat(self._current_session_id)
        else:
            raise APIError(f"开始录制失败: {result.get('message')}")

        return result

    def stop_recording(
        self,
        keep_video: bool = True,
        reason: str | None = None
    ) -> dict[str, Any]:
        if not self._current_job_id and not self._current_session_id:
            raise ValueError("未提供 execution_id 且没有正在进行的录制")

        payload: dict[str, Any] = {"keep_video": keep_video}
        if reason:
            payload["reason"] = reason

        session_id = self._current_session_id or self._current_job_id
        result: dict[str, Any] = self._request(
            "POST",
            f"/stop/{session_id}",
            json=payload
        )
        self._current_job_id = None
        self._current_session_id = None
        self._stop_heartbeat()
        return result
    
    def record_video(
        self,
        duration: int,
        task_name: str = "",
        output_format: str = "mp4",
    ) -> dict[str, Any]:
        self.start_recording(
            task_name=task_name,
            output_format=output_format
        )
        
        try:
            for i in range(duration):
                time.sleep(1)
            return self.stop_recording(keep_video=True)
            
        except Exception as e:
            # 异常时清理
            self.stop_recording(keep_video=False, reason=str(e))
            raise
    
    def record_gif(
        self,
        duration: int = 3,
        width: int = 320,
        fps: int = 10,
        **kwargs: Any
    ) -> dict[str, Any]:
        """
        便捷方法：录制 GIF
        
        Args:
            duration: 时长（秒）
            width: 宽度（像素）
            fps: 帧率
            **kwargs: 其他参数如 quality, loop
        """
        gif_params: dict[str, Any] = {
            "max_duration_sec": duration,
            "width": width,
            "fps": fps,
            **kwargs
        }
        
        self.start_recording(
            output_format="gif",
            gif_params=gif_params
        )
        
        try:
            for i in range(duration):
                time.sleep(1)
            return self.stop_recording(keep_video=True)
            
        except Exception as e:
            # 异常时清理
            self.stop_recording(keep_video=False, reason=str(e))
            raise
    
    def download(
        self,
        remote_filename: str,
        local_path: str | Path,
        chunk_size: int = 8192
    ) -> Path:
        """
        下载文件（视频或图片）

        Args:
            remote_filename: 服务端文件名（如 "xxx.mp4", "xxx.jpg"）
            local_path: 本地保存路径
        """
        url: str = f"{self.base_url}/output/{remote_filename}"
        local: Path = Path(local_path)
        
        try:
            with self.session.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(local, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            return local
        except requests.RequestException as e:
            raise CameraClientError(f"下载失败: {e}")
    
    def delete_remote(self, filename: str) -> bool:
        """删除服务端文件"""
        try:
            result: dict[str, Any] = self._request(
                "DELETE",
                f"/output/{filename}"
            )
            return result.get("success", False)
        except APIError:
            return False

    def list_outputs(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> dict[str, Any]:
        """列出服务端所有输出文件（视频和图片）"""
        return self._request(
            "GET",
            f"/outputs/?limit={limit}&offset={offset}"
        )

    def capture(
        self,
        task_name: str = "capture"
    ) -> dict[str, Any]:
        """
        拍照（JPEG 格式）

        Args:
            task_name: 任务名称，用于文件名

        Returns:
            {
                'success': True,
                'image_path': '/tmp/videos/xxx.jpg',
                'filename': 'xxx.jpg',
                'file_size_bytes': 12345,
                'message': '拍照成功'
            }
        """
        payload = {"task_name": task_name}
        return self._request("POST", "/capture", json=payload)

    def send_heartbeat(
        self,
        session_id: str | None = None,
        extend_timeout: int | None = None
    ) -> dict[str, Any]:
        """
        手动发送心跳

        Args:
            session_id: 会话ID，如果不提供则使用当前会话
            extend_timeout: 可选，延长心跳超时时间（秒）
        """
        if not session_id and not self._current_session_id:
            raise ValueError("未提供 session_id 且没有当前会话")

        use_session_id = session_id or self._current_session_id
        payload = {}
        if extend_timeout:
            payload["extend_timeout"] = extend_timeout

        return self._request("PUT", f"/heartbeat/{use_session_id}", json=payload)

    def _start_heartbeat(self, session_id: str) -> None:
        """启动自动心跳线程"""
        self._heartbeat_stop_event.clear()
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(session_id,),
            daemon=True
        )
        self._heartbeat_thread.start()
        logger.info(f"自动心跳线程已启动 (session_id: {session_id})")

    def _heartbeat_loop(self, session_id: str) -> None:
        """心跳循环（在线程中运行）"""
        while not self._heartbeat_stop_event.is_set():
            try:
                self.send_heartbeat(session_id)
                logger.debug(f"心跳发送成功 (session_id: {session_id})")
            except Exception as e:
                logger.error(f"心跳发送失败: {e}")
            # 等待下一次心跳（间隔 = 超时时间/3，保证至少3次心跳机会）
            for _ in range(self._heartbeat_interval):
                if self._heartbeat_stop_event.is_set():
                    break
                time.sleep(1)

    def _stop_heartbeat(self) -> None:
        """停止心跳线程"""
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_stop_event.set()
            self._heartbeat_thread.join(timeout=2)
            logger.info("心跳线程已停止")
        self._heartbeat_thread = None