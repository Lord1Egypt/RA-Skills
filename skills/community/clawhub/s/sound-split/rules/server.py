"""
音频分离 Web 服务 - AI 智能分轨
输入视频/音频 → 分离人声和伴奏 → 在线预览 + 下载
"""

import os
import shutil
import subprocess
import asyncio
import tempfile
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="🎵 音频分离工具 - AI 智能分轨", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 配置 =====
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
HISTORY_FILE = Path("history.json")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 任务状态存储: {task_id: {"status", "progress", "result"}}
tasks = {}


def load_history():
    """从 history.json 加载已完成任务记录"""
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text("utf-8"))
        except Exception:
            pass
    return []


def save_history(record):
    """追加一条历史记录到 history.json"""
    records = load_history()
    # 避免重复（同 task_id 只保留最新）
    records = [r for r in records if r.get("task_id") != record["task_id"]]
    records.insert(0, record)  # 最新的排前面
    # 最多保留 50 条
    records = records[:50]
    HISTORY_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), "utf-8")


def rebuild_tasks_from_history():
    """启动时从 outputs 目录 + history.json 恢复任务状态到内存"""
    global tasks
    history = load_history()
    for rec in history:
        tid = rec.get("task_id")
        out_dir = OUTPUT_DIR / tid
        if out_dir.exists() and tid not in tasks:
            # 从磁盘重建 task 状态（标记为 completed）
            tracks = {}
            for mp3 in out_dir.glob("*.mp3"):
                tracks[mp3.stem] = mp3.name
            tasks[tid] = {
                "status": "completed",
                "progress": 100,
                "message": "Done!",
                "model": rec.get("model", "htdemucs"),
                "stems": rec.get("stems", "2stems"),
                "filename": rec.get("filename", "unknown"),
                "result": {"tracks": tracks, "output_dir": str(out_dir)},
            }
    # 同时扫描 outputs 目录中存在但不在 history 中的目录（兜底）
    if OUTPUT_DIR.exists():
        for d in OUTPUT_DIR.iterdir():
            if d.is_dir() and d.name not in tasks:
                tracks = {}
                for mp3 in d.glob("*.mp3"):
                    tracks[mp3.stem] = mp3.name
                if tracks:
                    tasks[d.name] = {
                        "status": "completed",
                        "progress": 100,
                        "message": "Done!",
                        "model": "unknown",
                        "stems": "unknown",
                        "filename": d.name,
                        "result": {"tracks": tracks, "output_dir": str(d)},
                    }

# 支持的模型
MODELS = {
    "htdemucs": "推荐模式（均衡质量与速度）",
    "htdemucs_ft": "高品质模式（更精细分离）",
    "demucs": "经典模式",
    "mdx": "人声增强模式",
    "mdx_extra": "增强模式",
}

# 支持的分离模式（输出轨道）
STEMS_CONFIG = {
    "2stems": {"description": "2轨：人声 + 伴奏", "tracks": ["vocals", "accompaniment"]},
    "4stems": {"description": "4轨：人声 + 鼓 + 贝斯 + 其他", "tracks": ["vocals", "drums", "bass", "other"]},
    "5stems": {"description": "5轨：人声 + 鼓 + 贝斯 + 钢琴 + 其他", "tracks": ["vocals", "drums", "bass", "piano", "other"]},
}


@app.get("/")
async def index():
    """返回着陆页（首页）"""
    return FileResponse("static/landing.html")


@app.get("/app.html")
async def app_page():
    """返回音频分离工具主页面"""
    return FileResponse("static/index.html")


@app.get("/editor")
async def editor_page():
    """返回音频剪辑编辑器页面"""
    return FileResponse("static/editor.html")


@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """查询任务状态"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    return tasks[task_id]


@app.get("/api/history")
async def get_history():
    """获取历史任务列表（已完成的，最新的在前）"""
    history = load_history()
    # 标记每个任务在磁盘上是否仍然存在
    result = []
    for rec in history:
        tid = rec.get("task_id", "")
        out_dir = OUTPUT_DIR / tid
        rec["exists"] = out_dir.exists()
        result.append(rec)
    return result


@app.get("/api/download/{task_id}/{track_name}")
async def download_track(task_id: str, track_name: str):
    """下载分离后的音轨文件"""
    task_dir = OUTPUT_DIR / task_id
    if not task_dir.exists():
        raise HTTPException(status_code=404, detail="任务目录不存在")

    # 查找匹配的文件（支持 mp3/wav）
    for ext in [".mp3", ".wav"]:
        file_path = task_dir / f"{track_name}{ext}"
        if file_path.exists():
            return FileResponse(
                path=str(file_path),
                media_type="audio/mpeg" if ext == ".mp3" else "audio/wav",
                filename=f"{track_name}{ext}",
            )

    raise HTTPException(status_code=404, detail=f"音轨 {track_name} 不存在")


# 裁剪输出目录
TRIM_DIR = Path("trims")
TRIM_DIR.mkdir(exist_ok=True)


from fastapi.responses import Response
import uuid


@app.post("/api/trim")
async def trim_audio(
    task_id: str = None,
    track_name: str = None,
    start_time: float = 0.0,
    end_time: float = 0.0,
):
    """
    裁剪指定音轨的音频片段
    参数: task_id, track_name, start_time(秒), end_time(秒)
    返回: 裁剪后的 MP3 文件下载
    """
    if not task_id or not track_name:
        raise HTTPException(status_code=400, detail="缺少 task_id 或 track_name")
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="结束时间必须大于开始时间")

    # 查找源文件
    task_dir = OUTPUT_DIR / task_id
    src_path = None
    for ext in [".mp3", ".wav"]:
        p = task_dir / f"{track_name}{ext}"
        if p.exists():
            src_path = p
            break

    if not src_path:
        raise HTTPException(status_code=404, detail=f"音轨 {track_name} 文件不存在")

    # 用 ffmpeg 裁剪
    trim_id = uuid.uuid4().hex[:12]
    output_path = TRIM_DIR / f"{trim_id}_{track_name}_trim.mp3"

    duration = end_time - start_time

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(src_path),
            "-ss", str(start_time),
            "-t", str(duration),
            "-acodec", "libmp3lame", "-ab", "320k",
            str(output_path),
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="ffmpeg 裁剪失败: " + str(e))

    if not output_path.exists():
        raise HTTPException(status_code=500, detail="裁剪输出文件未生成")

    return FileResponse(
        path=str(output_path),
        media_type="audio/mpeg",
        filename=f"{track_name}_{format_duration(start_time)}_{format_duration(end_time)}.mp3",
    )


def format_duration(seconds: float) -> str:
    """将秒数格式化为 mm:ss"""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}{s:02d}"


@app.post("/api/separate")
async def separate_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model: str = "htdemucs",
    stems: str = "2stems",
):
    """
    上传视频/音频文件，启动后台分离任务
    返回 task_id 用于轮询状态
    """
    # 校验参数
    if model not in MODELS:
        raise HTTPException(status_code=400, detail=f"不支持的模式: {model}，可选: {list(MODELS.keys())}")
    if stems not in STEMS_CONFIG:
        raise HTTPException(status_code=400, detail=f"不支持的轨道数: {stems}")

    # 生成任务 ID
    import uuid
    task_id = uuid.uuid4().hex[:12]

    # 保存上传文件
    suffix = Path(file.filename).suffix if file.filename else ".mp4"
    input_path = UPLOAD_DIR / f"{task_id}{suffix}"
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 初始化任务状态
    tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "message": "排队中...",
        "model": model,
        "stems": stems,
        "filename": file.filename or "unknown",
        "result": None,
    }

    # 后台执行分离
    background_tasks.add_task(run_demucs, task_id, str(input_path), model, stems)

    return JSONResponse({
        "task_id": task_id,
        "status": "pending",
        "message": "任务已提交，请用 task_id 轮询进度",
    })


def run_demucs(task_id: str, input_path: str, model: str, stems: str):
    """Run demucs separation in background"""
    output_base = OUTPUT_DIR / task_id

    try:
        tasks[task_id].update({"status": "processing", "progress": 5, "message": "Extracting audio..."})

        # If video, extract audio first with ffmpeg
        is_video = input_path.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".flv"))
        audio_for_demucs = input_path

        if is_video:
            wav_path = str(OUTPUT_DIR / task_id / "source.wav")
            output_base.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path,
                "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
                wav_path,
            ], check=True, capture_output=True)
            audio_for_demucs = wav_path
            tasks[task_id].update({"progress": 15, "message": "Audio extracted, loading model..."})
        else:
            output_base.mkdir(parents=True, exist_ok=True)

        # Run demucs
        tasks[task_id].update({"progress": 20, "message": "Running " + model + " separation..."})

        cmd = [
            "python3", "-m", "demucs",
            "-n", model,
            "--mp3", "--mp3-bitrate", "320",
            "-o", str(output_base),
            audio_for_demucs,
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Read progress in real-time
        # Demucs output may not contain "Processing"/"segment" keywords exactly,
        # so we track: any stdout activity = model is working, slowly advance progress
        line_count = 0
        for line in process.stdout:
            line_count += 1
            stripped = line.strip()
            print("[demucs] " + stripped)
            
            # Advance progress on any output (20 -> 85 range during separation)
            if stripped:
                # Slow ramp: first 30 lines = 20->40%, then gradual to 80%
                new_prog = min(20 + int(line_count * 1.5), 85)
                if new_prog > tasks[task_id]["progress"]:
                    tasks[task_id].update({
                        "progress": new_prog,
                        "message": "Separating... " + str(new_prog) + "% (" + str(line_count) + " lines processed)",
                    })

        process.wait()

        if process.returncode != 0:
            raise Exception("demucs failed with code " + str(process.returncode))

        # Find output files and copy to friendly names
        stem_info = STEMS_CONFIG[stems]
        result_tracks = {}

        # demucs outputs to: {output_base}/{model}/{original_filename}/
        # search recursively for the actual mp3 files
        demucs_out_dir = None
        model_dir = output_base / model

        if model_dir.exists():
            # Strategy 1: find folder containing vocals.mp3
            for candidate in model_dir.rglob("vocals.mp3"):
                demucs_out_dir = candidate.parent
                break
            # Strategy 2: find any mp3 under model dir
            if not demucs_out_dir:
                for candidate in model_dir.rglob("*.mp3"):
                    demucs_out_dir = candidate.parent
                    break

        # Fallback: search entire output dir
        if not demucs_out_dir:
            for mp3_file in output_base.rglob("*.mp3"):
                demucs_out_dir = mp3_file.parent
                break

        if demucs_out_dir:
            print("[demucs] Found outputs in: " + str(demucs_out_dir))
            # List all actual mp3 files demucs produced
            actual_files = {mp3_file.stem: mp3_file for mp3_file in demucs_out_dir.glob("*.mp3")}
            print("[demucs] Actual output tracks: " + str(list(actual_files.keys())))

            # Mapping for when demucs output doesn't match stems config exactly
            # e.g. htdemucs outputs [vocals, drums, bass, other] but user wants 2stems [vocals, accompaniment]
            FALLBACK_MAP = {
                "accompaniment": ["other", "no_vocals", "instrumental"],
                "no_vocals": ["other", "accompaniment", "instrumental"],
                "instrumental": ["other", "accompaniment", "no_vocals"],
            }

            expected_tracks = stem_info["tracks"]
            for track_name in expected_tracks:
                src = None
                # Try direct name first
                direct = demucs_out_dir / (track_name + ".mp3")
                if direct.exists():
                    src = direct
                else:
                    # Try fallback mapping
                    fallback_names = FALLBACK_MAP.get(track_name, [])
                    for fb_name in fallback_names:
                        fb_path = demucs_out_dir / (fb_name + ".mp3")
                        if fb_path.exists():
                            print("[demuc    s] Mapped '" + track_name + "' -> actual file '" + fb_name + ".mp3'")
                            src = fb_path
                            break

                if src:
                    dst = output_base / (track_name + ".mp3")
                    shutil.copy2(str(src), str(dst))
                    result_tracks[track_name] = track_name + ".mp3"
                    print("[demucs] Copied: " + track_name + ".mp3")
                else:
                    print("[demucs] Track not found (and no fallback): " + track_name)

        # Done
        tasks[task_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Done!",
            "result": {
                "tracks": result_tracks,
                "output_dir": str(output_base),
            },
        })

        # 持久化到历史记录
        save_history({
            "task_id": task_id,
            "filename": tasks[task_id].get("filename", "unknown"),
            "model": model,
            "stems": stems,
            "status": "completed",
            "track_count": len(result_tracks),
            "created_at": __import__("datetime").datetime.now().isoformat(),
        })

    except Exception as e:
        tasks[task_id].update({
            "status": "error",
            "progress": -1,
            "message": "Error: " + str(e),
        })


@app.delete("/api/cleanup/{task_id}")
async def cleanup_task(task_id: str):
    """清理任务文件"""
    task_dir = OUTPUT_DIR / task_id
    upload_file = list(UPLOAD_DIR.glob(f"{task_id}.*"))

    count = 0
    if task_dir.exists():
        shutil.rmtree(task_dir)
        count += 1
    for f in upload_file:
        f.unlink()
        count += 1

    if task_id in tasks:
        del tasks[task_id]

    return JSONResponse({"message": f"已清理 {count} 个文件"})


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    # 确保静态文件目录存在
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)

    # 启动时从磁盘恢复历史任务到内存
    rebuild_tasks_from_history()
    print(f"[init] 已从历史记录恢复 {len(tasks)} 个任务")

    print("""
╔══════════════════════════════════════════════╗
║   🎵 音频分离工具 - AI 智能分轨              ║
║   http://127.0.0.1:8765                       ║
╚══════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="127.0.0.1", port=8765)
