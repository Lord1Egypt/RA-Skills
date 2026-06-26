#!/usr/bin/env python3
"""
树莓派摄像头 HTTP 服务
基于 FastAPI + Picamera2 + FFmpeg
"""
from __future__ import annotations

import os
import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

# 加载 .env 文件环境变量
from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator

from camera_manager import CameraManager
from converter import FFmpegConverter

# 从环境变量读取日志级别
LOG_LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
log_level_str: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL: int = LOG_LEVEL_MAP.get(log_level_str, logging.INFO)

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger: logging.Logger = logging.getLogger(__name__)

# 心跳机制配置常量
DEFAULT_HEARTBEAT_TIMEOUT = 30  # 默认心跳超时 30 秒
MAX_HEARTBEAT_TIMEOUT = 300     # 最大心跳超时 300 秒
HEARTBEAT_CHECK_INTERVAL = 5    # 心跳检查间隔 5 秒

# 会话管理类
class RecordingSession:
    """录制会话管理类"""
    def __init__(
        self,
        session_id: str,
        client_id: str,
        heartbeat_timeout: int = DEFAULT_HEARTBEAT_TIMEOUT,
        task_name: str = "",
        format: str = "h264"
    ) -> None:
        self.session_id: str = session_id
        self.client_id: str = client_id
        self.task_name: str = task_name
        self.format: str = format
        self.created_at: float = time.time()
        self.last_heartbeat: float = time.time()
        self.heartbeat_timeout: int = heartbeat_timeout
        self.is_active: bool = True
        self.recording_file: str | None = None

    def update_heartbeat(self, extend_timeout: int | None = None) -> None:
        """更新心跳时间，可选延长超时时间"""
        self.last_heartbeat = time.time()
        if extend_timeout and extend_timeout <= MAX_HEARTBEAT_TIMEOUT:
            self.heartbeat_timeout = extend_timeout

    def is_expired(self) -> bool:
        """检查会话是否过期（心跳超时）"""
        return (time.time() - self.last_heartbeat) > self.heartbeat_timeout

    def get_remaining_time(self) -> int:
        """获取剩余心跳时间（秒）"""
        elapsed = time.time() - self.last_heartbeat
        return max(0, int(self.heartbeat_timeout - elapsed))

    def get_last_heartbeat_iso(self) -> str:
        """获取最后心跳时间的 ISO 格式"""
        return datetime.fromtimestamp(self.last_heartbeat).isoformat()

    def get_expires_at_iso(self) -> str:
        """获取会话过期时间的 ISO 格式"""
        expires_timestamp = self.last_heartbeat + self.heartbeat_timeout
        return datetime.fromtimestamp(expires_timestamp).isoformat()

# Pydantic 模型定义
class GifParams(BaseModel):
    """GIF 转换参数（可选）"""
    fps: int = Field(default=10, ge=1, le=30, description="GIF 帧率")
    max_duration_sec: int = Field(default=5, ge=1, le=60, description="最大时长（秒）")
    width: int = Field(default=320, ge=100, le=1920, description="输出宽度（像素）")
    quality: int = Field(default=5, ge=1, le=10, description="调色板质量（1-10）")
    loop: bool = Field(default=True, description="是否循环播放")


class StartRequest(BaseModel):
    """开始录制请求"""
    client_id: str = Field(
        default_factory=lambda: f"client_{datetime.now().timestamp():.0f}",
        description="客户端标识"
    )
    task_name: str = Field(default="untitled", max_length=100, description="任务名称")
    output_format: Literal["h264", "mp4", "gif"] = Field(
        default="h264",
        description="输出格式：h264(原始), mp4(封装), gif(动图)"
    )
    keep_original: bool = Field(
        default=False,
        description="转换后是否保留原始 H264 文件"
    )
    heartbeat_timeout: int = Field(
        default=DEFAULT_HEARTBEAT_TIMEOUT,
        ge=5,
        le=MAX_HEARTBEAT_TIMEOUT,
        description="心跳超时时间（秒），超过此时间未收到心跳将自动停止录制"
    )
    gif_params: GifParams | None = Field(
        default=None,
        description="GIF 参数（仅当 format=gif 时有效，不传使用默认值）"
    )


class StopRequest(BaseModel):
    """停止录制请求"""
    keep_video: bool = Field(default=True, description="是否保留视频文件（false 则删除）")
    reason: str | None = Field(default=None, description="停止原因（用于日志）")


class HeartbeatRequest(BaseModel):
    """心跳请求（可选）"""
    extend_timeout: int | None = Field(
        default=None,
        ge=5,
        le=MAX_HEARTBEAT_TIMEOUT,
        description="可选：延长心跳超时时间（秒）"
    )


class CaptureRequest(BaseModel):
    """拍照请求"""
    task_name: str = Field(default="capture", max_length=100, description="任务名称")


class CaptureResponse(BaseModel):
    """拍照响应"""
    success: bool
    image_path: str
    filename: str
    file_size_bytes: int
    message: str


class JobInfo(BaseModel):
    """当前任务信息"""
    is_recording: bool
    current_job_id: str | None
    client_id: str | None
    format: Literal["h264", "mp4", "gif"] | None
    start_time: str | None
    output_path: str | None
    session_id: str | None = None  # 新增：会话ID
    last_heartbeat: str | None = None  # 新增：最后心跳时间
    expires_at: str | None = None  # 新增：过期时间
    remaining_time: int | None = None  # 新增：剩余时间（秒）


class StartResponse(BaseModel):
    """开始录制响应"""
    success: bool
    session_id: str  # 替换 execution_id，作为会话标识
    execution_id: str  # 保留兼容字段
    message: str
    confirmed_format: Literal["h264", "mp4", "gif"]
    h264_path: str
    heartbeat_timeout: int  # 新增：心跳超时时间


class StopResponse(BaseModel):
    """停止录制响应"""
    success: bool
    execution_id: str
    video_path: str
    h264_path: str | None  # 如果是 mp4/gif，返回原始 h264 路径（如果未删除）
    format: Literal["h264", "mp4", "gif", "deleted"]
    file_size_bytes: int
    message: str


# 服务状态管理（单例）
class ServiceState:
    """全局服务状态"""
    def __init__(self, output_dir: str = "/tmp/videos") -> None:
        self.lock: asyncio.Lock = asyncio.Lock()
        self.camera: CameraManager = CameraManager(output_dir)
        self.converter: FFmpegConverter = FFmpegConverter()
        self.output_dir: Path = Path(output_dir)
        self.current_job: dict[str, Any] | None = None
        self.active_session: RecordingSession | None = None  # 新增：活跃会话

    def set_session(self, session: RecordingSession) -> None:
        """设置活跃会话"""
        self.active_session = session

    def clear_session(self) -> None:
        """清除活跃会话"""
        self.active_session = None
        self.current_job = None

    def get_active_session(self) -> RecordingSession | None:
        """获取活跃会话"""
        return self.active_session

    def is_session_active(self) -> bool:
        """检查是否有活跃会话"""
        return self.active_session is not None and self.active_session.is_active

    def cleanup(self) -> None:
        """清理资源"""
        try:
            self.camera.release()
        except Exception as e:
            logger.error(f"清理摄像头失败: {e}")
        finally:
            self.clear_session()
            if self.lock.locked():
                self.lock.release()

# 全局状态实例
state: ServiceState = ServiceState(os.getenv('OUTPUT_DIR', '/tmp/videos'))


# Lifespan 管理（启动/关闭）
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("服务启动")
    # 启动心跳监控任务
    heartbeat_task = asyncio.create_task(_monitor_heartbeats())
    yield
    # 关闭时清理
    logger.info("服务关闭，清理资源")
    heartbeat_task.cancel()
    try:
        await heartbeat_task
    except asyncio.CancelledError:
        pass
    if state.current_job:
        logger.warning("关闭时检测到未完成的录制，强制停止")
        state.camera.stop_recording()
        state.camera.delete_recording()
        state.cleanup()


app: FastAPI = FastAPI(
    title="Pi Camera HTTP Service",
    description="树莓派摄像头 HTTP 控制服务（支持录像和拍照）",
    version="1.1.0",
    lifespan=lifespan
)


@app.get("/", response_model=dict[str, str])
async def root() -> dict[str, str]:
    """根路径"""
    return {
        "message": "Pi Camera Service",
        "docs": "/docs",
        "status": "/status"
    }


@app.get("/status", response_model=JobInfo)
async def get_status() -> JobInfo:
    """获取当前录制状态"""
    if state.current_job:
        session = state.get_active_session()
        return JobInfo(
            is_recording=True,
            current_job_id=state.current_job["id"],
            session_id=session.session_id if session else None,
            client_id=state.current_job["client_id"],
            format=state.current_job["format"],
            start_time=state.current_job["start_time"],
            output_path=str(state.camera.current_file) if state.camera.current_file else None,
            last_heartbeat=session.get_last_heartbeat_iso() if session else None,
            expires_at=session.get_expires_at_iso() if session else None,
            remaining_time=session.get_remaining_time() if session else None
        )
    return JobInfo(
        is_recording=False,
        current_job_id=None,
        session_id=None,
        client_id=None,
        format=None,
        start_time=None,
        output_path=None,
        last_heartbeat=None,
        expires_at=None,
        remaining_time=None
    )


@app.post("/start", response_model=StartResponse)
async def start_recording(request: StartRequest) -> StartResponse:
    """
    开始录制视频

    - **output_format**: h264(原始流), mp4(自动封装), gif(生成动图)
    - **gif_params**: 仅当 format=gif 时有效，不传则使用默认值
    - **heartbeat_timeout**: 心跳超时时间（秒），超过此时间未收到心跳将自动停止录制
    """
    if state.lock.locked():
        raise HTTPException(
            status_code=423,  # Locked
            detail="服务正忙，已有其他客户端正在录制"
        )

    await state.lock.acquire()
    session_id: str = str(uuid.uuid4())  # 使用完整 UUID 作为 session_id
    job_id: str = session_id[:8]  # 兼容现有的 execution_id

    try:
        # 初始化摄像头
        if not state.camera.init_camera(width=640, height=480, fps=30):
            state.cleanup()
            raise HTTPException(status_code=500, detail="摄像头初始化失败")

        # 开始录制（所有格式先录 H264）
        h264_path: str = state.camera.start_recording(job_id, request.task_name)

        # 创建会话
        session = RecordingSession(
            session_id=session_id,
            client_id=request.client_id,
            heartbeat_timeout=request.heartbeat_timeout,
            task_name=request.task_name,
            format=request.output_format
        )
        session.recording_file = h264_path
        state.set_session(session)

        # 存储任务信息
        state.current_job = {
            "id": job_id,
            "session_id": session_id,  # 新增
            "client_id": request.client_id,
            "format": request.output_format,
            "keep_original": request.keep_original,
            "gif_params": request.gif_params or GifParams(),  # 使用默认值
            "start_time": datetime.now().isoformat(),
            "h264_path": h264_path
        }

        logger.info(f"开始录制: {session_id}, 格式: {request.output_format}, 心跳超时: {request.heartbeat_timeout}s")

        return StartResponse(
            success=True,
            session_id=session_id,
            execution_id=job_id,
            message="开始录制",
            confirmed_format=request.output_format,
            h264_path=h264_path,
            heartbeat_timeout=request.heartbeat_timeout
        )

    except Exception as e:
        state.cleanup()
        logger.error(f"开始录制失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop/{session_id}", response_model=StopResponse)
async def stop_recording(
    session_id: str,
    request: StopRequest,
    background_tasks: BackgroundTasks
) -> StopResponse:
    """
    停止录制并转换格式

    - **session_id**: 会话ID或旧的 execution_id
    - **keep_video**: false 则直接删除视频文件
    - MP4/GIF 转换在后台执行，响应立即返回
    """
    # 支持 session_id 和旧的 execution_id
    if not state.current_job:
        raise HTTPException(status_code=404, detail="未找到正在进行的录制任务")

    # 检查 session_id 匹配（支持完整 session_id 或前8位的 execution_id）
    job_session_id = state.current_job.get("session_id")
    job_id = state.current_job.get("id")

    if session_id != job_session_id and session_id != job_id:
        raise HTTPException(status_code=404, detail="会话ID不匹配")

    job: dict[str, Any] = state.current_job

    try:
        # 停止录制（得到 H264）
        h264_path_str: str | None
        h264_size: int
        h264_path_str, h264_size = state.camera.stop_recording()

        if not h264_path_str:
            state.cleanup()
            raise HTTPException(status_code=500, detail="停止录制失败，未生成文件")

        h264_path: Path = Path(h264_path_str)

        # 如果要求删除，直接清理并返回
        if not request.keep_video:
            state.camera.delete_recording()
            state.cleanup()
            return StopResponse(
                success=True,
                execution_id=job_id,
                video_path="",
                h264_path=None,
                format="deleted",
                file_size_bytes=0,
                message=f"视频已删除" + (f": {request.reason}" if request.reason else "")
            )

        # 根据格式处理
        final_path: str = h264_path_str
        final_format: Literal["h264", "mp4", "gif"] = "h264"
        message: str = "录制完成（原始 H264）"
        h264_backup_path: str | None = h264_path_str

        if job["format"] == "mp4":
            final_path = str(h264_path.with_suffix(".mp4"))
            final_format = "mp4"
            message = "录制完成，MP4 转换中（后台处理）"

            # 后台转换
            background_tasks.add_task(
                _convert_to_mp4_task,
                h264_path_str,
                job["keep_original"]
            )
            if job["keep_original"]:
                h264_backup_path = h264_path_str
            else:
                h264_backup_path = None

        elif job["format"] == "gif":
            gif_params: GifParams = job["gif_params"]
            final_path = str(h264_path.with_suffix(".gif"))
            final_format = "gif"
            message = "录制完成，GIF 转换中（后台处理）"

            # 后台转换
            background_tasks.add_task(
                _convert_to_gif_task,
                h264_path_str,
                gif_params,
                job["keep_original"]
            )
            # GIF 转换后通常删除 H264（除非 keep_original）
            h264_backup_path = h264_path_str if job["keep_original"] else None

        # 清理状态（但文件保留）
        state.clear_session()
        state.camera.release()
        if state.lock.locked():
            state.lock.release()

        return StopResponse(
            success=True,
            execution_id=job_id,
            video_path=final_path,
            h264_path=h264_backup_path,
            format=final_format,
            file_size_bytes=h264_size,
            message=message
        )

    except Exception as e:
        logger.error(f"停止录制失败: {e}")
        state.cleanup()
        raise HTTPException(status_code=500, detail=str(e))


async def _convert_to_mp4_task(h264_path: str, keep_original: bool) -> None:
    """后台任务：转换为 MP4"""
    try:
        mp4_path, error = await state.converter.h264_to_mp4(
            h264_path, 
            framerate=30, 
            delete_original=not keep_original
        )
        if error:
            logger.error(f"MP4 转换失败: {error}")
        else:
            logger.info(f"MP4 转换完成: {mp4_path}")
    except Exception as e:
        logger.error(f"MP4 后台转换异常: {e}")


async def _convert_to_gif_task(
    h264_path: str,
    gif_params: GifParams,
    keep_original: bool
) -> None:
    """后台任务：转换为 GIF"""
    try:
        gif_path, error = await state.converter.h264_to_gif(
            h264_path,
            duration=gif_params.max_duration_sec,
            fps=gif_params.fps,
            width=gif_params.width
        )
        if error:
            logger.error(f"GIF 转换失败: {error}")
        else:
            logger.info(f"GIF 转换完成: {gif_path}")
            if not keep_original and Path(h264_path).exists():
                Path(h264_path).unlink()
                logger.info(f"已删除原始 H264: {h264_path}")
    except Exception as e:
        logger.error(f"GIF 后台转换异常: {e}")


async def _monitor_heartbeats() -> None:
    """后台任务：监控心跳超时并自动清理"""
    while True:
        try:
            session = state.get_active_session()
            if session and session.is_expired():
                logger.warning(
                    f"会话 {session.session_id} 心跳超时，自动停止录制。"
                    f"最后心跳: {session.get_last_heartbeat_iso()}, "
                    f"超时时间: {session.heartbeat_timeout}s"
                )
                await _auto_stop_session("心跳超时")
        except Exception as e:
            logger.error(f"心跳监控错误: {e}")
        await asyncio.sleep(HEARTBEAT_CHECK_INTERVAL)


async def _auto_stop_session(reason: str = "自动清理") -> None:
    """自动停止当前会话（用于心跳超时等场景）"""
    if not state.is_session_active():
        return

    try:
        # 复用现有的停止逻辑
        session = state.get_active_session()
        if not session:
            return

        job_id = state.current_job["id"] if state.current_job else session.session_id[:8]
        stop_request = StopRequest(keep_video=True, reason=reason)
        background_tasks = BackgroundTasks()

        # 停止录制
        h264_path_str, h264_size = state.camera.stop_recording()
        if h264_path_str:
            # 清理状态
            state.clear_session()
            state.camera.release()
            if state.lock.locked():
                state.lock.release()
            logger.info(f"自动停止会话成功: {h264_path_str}")
        else:
            state.cleanup()
            logger.warning("自动停止会话：未生成文件")

    except Exception as e:
        logger.error(f"自动停止会话失败: {e}")
        state.cleanup()


@app.put("/heartbeat/{session_id}")
async def heartbeat(session_id: str, request: HeartbeatRequest | None = None) -> JSONResponse:
    """
    客户端发送心跳，续期录制会话

    - **session_id**: 会话ID或旧的 execution_id
    - **extend_timeout**: 可选，延长心跳超时时间（秒）
    """
    session = state.get_active_session()
    if not session:
        raise HTTPException(status_code=404, detail="没有活跃的录制会话")

    # 支持 session_id 和旧的 execution_id
    job_session_id = state.current_job.get("session_id") if state.current_job else None
    job_id = state.current_job.get("id") if state.current_job else None

    if session_id != session.session_id and session_id != job_session_id and session_id != job_id:
        raise HTTPException(status_code=404, detail="会话ID不匹配")

    # 更新心跳
    extend_timeout = request.extend_timeout if request else None
    session.update_heartbeat(extend_timeout)

    logger.debug(f"收到心跳: {session.session_id}, 剩余时间: {session.get_remaining_time()}s")

    return JSONResponse({
        "success": True,
        "session_id": session.session_id,
        "last_heartbeat": session.get_last_heartbeat_iso(),
        "expires_at": session.get_expires_at_iso(),
        "remaining_time": session.get_remaining_time()
    })


@app.post("/capture", response_model=CaptureResponse)
async def capture_image(request: CaptureRequest) -> CaptureResponse:
    """
    拍照（JPEG 格式）

    - **task_name**: 任务名称，用于文件名
    - 与录像互斥，录像中返回 423 Locked
    """
    if state.lock.locked():
        raise HTTPException(
            status_code=423,
            detail="服务正忙，当前正在录制中，无法拍照"
        )

    await state.lock.acquire()

    try:
        # 初始化摄像头
        if not state.camera.init_camera(width=640, height=480, fps=30):
            raise HTTPException(status_code=500, detail="摄像头初始化失败")

        # 拍照
        image_path: str = state.camera.capture_image(request.task_name)

        # 获取文件大小
        file_size: int = Path(image_path).stat().st_size

        # 释放摄像头
        state.camera.release()

        filename: str = Path(image_path).name

        logger.info(f"拍照完成: {filename}, 大小: {file_size/1024:.1f}KB")

        return CaptureResponse(
            success=True,
            image_path=image_path,
            filename=filename,
            file_size_bytes=file_size,
            message="拍照成功"
        )

    except Exception as e:
        logger.error(f"拍照失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        state.lock.release()


@app.get("/output/{filename}")
async def get_video(filename: str) -> FileResponse:
    """
    下载视频文件
    
    - 支持范围请求（断点续传）
    """
    # 安全检查：防止目录遍历
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="非法文件名")
    
    file_path: Path = state.output_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    media_type: str = "video/H264"
    if filename.endswith(".mp4"):
        media_type = "video/mp4"
    elif filename.endswith(".gif"):
        media_type = "image/gif"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        media_type = "image/jpeg"
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


@app.delete("/output/{filename}")
async def delete_file(filename: str) -> JSONResponse:
    """删除文件（视频或图片）"""
    # 安全检查
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="非法文件名")
    
    file_path: Path = state.output_dir / filename
    if file_path.exists():
        try:
            file_path.unlink()
            return JSONResponse(
                content={"success": True, "message": "已删除", "filename": filename}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除失败: {e}")
    
    return JSONResponse(
        content={"success": False, "message": "文件不存在", "filename": filename},
        status_code=404
    )


@app.get("/outputs/")
async def list_outputs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
) -> JSONResponse:
    """列出所有输出文件（视频和图片，分页）"""
    try:
        # 支持视频和图片格式
        files: list[Path] = []
        for pattern in ["*.h264", "*.mp4", "*.gif", "*.jpg"]:
            files.extend(state.output_dir.glob(pattern))

        files = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)
        
        total: int = len(files)
        paginated_files: list[Path] = files[offset:offset + limit]
        
        items: list[dict[str, Any]] = []
        for f in paginated_files:
            stat = f.stat()
            items.append({
                "filename": f.name,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "format": f.suffix.lstrip(".")
            })
        
        return JSONResponse({
            "total": total,
            "offset": offset,
            "limit": limit,
            "items": items
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"列出文件失败: {e}")


if __name__ == "__main__":
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "27793"))
    uvicorn.run(
        "service:app",
        host=host,
        port=port,
        reload=False,
        workers=1  # 单进程，确保锁有效
    )