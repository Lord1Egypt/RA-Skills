from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor
from src.core.time_anchor import TimeAnchorInjector

app = FastAPI(title="Temporal Agent Plugin API", description="智能体时序感知插件API")

# 初始化核心组件
temporal_analyzer = TemporalAnalyzer()
progress_estimator = ProgressEstimator()
anomaly_detector = AnomalyDetector()
social_temporal = SocialTemporal()
causal_predictor = CausalPredictor()
time_anchor = TimeAnchorInjector()

# 请求模型
class StartTimerRequest(BaseModel):
    task_id: Optional[str] = None

class StopTimerRequest(BaseModel):
    task_id: str

class PredictDurationRequest(BaseModel):
    task_type: str
    complexity: Optional[float] = 1.0

class StartTaskRequest(BaseModel):
    task_id: Optional[str] = None
    task_type: str
    total_steps: Optional[int] = 100

class UpdateProgressRequest(BaseModel):
    task_id: str
    current_step: int

class DetectAnomalyRequest(BaseModel):
    event_type: str
    duration: float

class RecordUtteranceRequest(BaseModel):
    speaker: str
    content: str

class PredictLatencyRequest(BaseModel):
    action: str

class GetTimeContextRequest(BaseModel):
    timezone: Optional[str] = None

class InjectTimeAnchorRequest(BaseModel):
    prompt: str
    timezone: Optional[str] = None

# 响应模型
class TimerResponse(BaseModel):
    task_id: str
    start_time: float

class DurationResponse(BaseModel):
    task_id: str
    duration: float

class PredictDurationResponse(BaseModel):
    task_type: str
    predicted_duration: float

class TaskResponse(BaseModel):
    task_id: str
    status: str

class ProgressResponse(BaseModel):
    task_type: str
    total_steps: int
    current_step: int
    progress: float
    elapsed_time: float
    remaining_time: float

class AnomalyResponse(BaseModel):
    event_type: str
    duration: float
    is_abnormal: bool

class UtteranceResponse(BaseModel):
    speaker: str
    content: str

class RespondResponse(BaseModel):
    should_respond: bool

class LatencyResponse(BaseModel):
    action: str
    predicted_latency: float

class TimeContextResponse(BaseModel):
    current_time: str
    current_date: str
    current_time_only: str
    day_of_week: str
    day_of_week_chinese: str
    month: str
    month_chinese: str
    year: int
    timestamp: float
    timezone: str
    is_weekend: bool
    is_morning: bool
    is_afternoon: bool
    is_evening: bool
    is_night: bool

class InjectTimeAnchorResponse(BaseModel):
    injected_prompt: str

# API端点
@app.post("/api/timer/start", response_model=TimerResponse)
async def start_timer(request: StartTimerRequest):
    task_id = request.task_id or f"task_{id(temporal_analyzer)}"
    start_time = temporal_analyzer.start_timer(task_id)
    return TimerResponse(task_id=task_id, start_time=start_time)

@app.post("/api/timer/stop", response_model=DurationResponse)
async def stop_timer(request: StopTimerRequest):
    duration = temporal_analyzer.stop_timer(request.task_id)
    return DurationResponse(task_id=request.task_id, duration=duration)

@app.post("/api/duration/predict", response_model=PredictDurationResponse)
async def predict_duration(request: PredictDurationRequest):
    predicted_duration = temporal_analyzer.predict_duration(request.task_type, request.complexity)
    return PredictDurationResponse(task_type=request.task_type, predicted_duration=predicted_duration)

@app.post("/api/task/start", response_model=TaskResponse)
async def start_task(request: StartTaskRequest):
    task_id = request.task_id or f"task_{id(progress_estimator)}"
    progress_estimator.start_task(task_id, request.task_type, request.total_steps)
    return TaskResponse(task_id=task_id, status="started")

@app.post("/api/task/progress", response_model=ProgressResponse)
async def update_progress(request: UpdateProgressRequest):
    progress_estimator.update_progress(request.task_id, request.current_step)
    progress = progress_estimator.get_progress(request.task_id)
    return ProgressResponse(**progress)

@app.get("/api/task/progress/{task_id}", response_model=ProgressResponse)
async def get_progress(task_id: str):
    progress = progress_estimator.get_progress(task_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Task not found")
    return ProgressResponse(**progress)

@app.post("/api/anomaly/detect", response_model=AnomalyResponse)
async def detect_anomaly(request: DetectAnomalyRequest):
    is_abnormal = anomaly_detector.is_response_time_abnormal(request.event_type, request.duration)
    return AnomalyResponse(event_type=request.event_type, duration=request.duration, is_abnormal=is_abnormal)

@app.post("/api/social/utterance", response_model=UtteranceResponse)
async def record_utterance(request: RecordUtteranceRequest):
    social_temporal.record_utterance(request.speaker, request.content)
    return UtteranceResponse(speaker=request.speaker, content=request.content)

@app.get("/api/social/should_respond", response_model=RespondResponse)
async def should_respond():
    should_respond_flag = social_temporal.should_respond()
    return RespondResponse(should_respond=should_respond_flag)

@app.post("/api/causal/predict_latency", response_model=LatencyResponse)
async def predict_latency(request: PredictLatencyRequest):
    predicted_latency = causal_predictor.predict_latency(request.action)
    return LatencyResponse(action=request.action, predicted_latency=predicted_latency)

@app.post("/api/time/context", response_model=TimeContextResponse)
async def get_time_context(request: GetTimeContextRequest):
    time_context = time_anchor.get_time_context(request.timezone)
    return TimeContextResponse(**time_context)

@app.post("/api/time/inject", response_model=InjectTimeAnchorResponse)
async def inject_time_anchor(request: InjectTimeAnchorRequest):
    injected_prompt = time_anchor.inject_time_anchor(request.prompt, request.timezone)
    return InjectTimeAnchorResponse(injected_prompt=injected_prompt)

@app.get("/api/time/current")
async def get_current_time(timezone: Optional[str] = None):
    current_time = time_anchor.get_time_string(timezone)
    return {"current_time": current_time}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)