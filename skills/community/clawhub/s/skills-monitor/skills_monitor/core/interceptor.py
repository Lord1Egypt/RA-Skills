"""
SDK 拦截器 v0.5.0 — @skill_monitor 装饰器
无侵入地包裹 skill 函数调用，自动采集运行指标
v0.5.0: 新增实时反馈上报（异步，不阻塞）
"""

import functools
import logging
import time
import traceback
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from skills_monitor.data.store import DataStore

logger = logging.getLogger(__name__)

# 全局单例（在 init 时设置）
_store: Optional[DataStore] = None
_agent_id: Optional[str] = None
_realtime_reporter = None   # v0.5.0: 实时上报器（延迟初始化）
_realtime_enabled: bool = True  # v0.5.0: 是否开启实时上报


def configure(store: DataStore, agent_id: str, enable_realtime: bool = True):
    """配置拦截器的全局 store 和 agent_id"""
    global _store, _agent_id, _realtime_enabled
    _store = store
    _agent_id = agent_id
    _realtime_enabled = enable_realtime


def _get_realtime_reporter():
    """延迟初始化实时上报器"""
    global _realtime_reporter
    if _realtime_reporter is None and _realtime_enabled:
        try:
            from skills_monitor.core.realtime_reporter import RealtimeReporter
            _realtime_reporter = RealtimeReporter.get_instance()
        except Exception as e:
            logger.debug(f"实时上报器初始化失败: {e}")
            _realtime_reporter = False  # 标记为失败，不再重试
    return _realtime_reporter if _realtime_reporter is not False else None


def get_store() -> Optional[DataStore]:
    return _store


def skill_monitor(skill_id: str, task_name: str = ""):
    """
    装饰器：自动采集 skill 运行指标

    用法:
        @skill_monitor(skill_id="a-share-short-decision", task_name="get_market_sentiment")
        def run_market_sentiment():
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if _store is None or _agent_id is None:
                # 未初始化，直接调用原函数
                return func(*args, **kwargs)

            run_id = str(uuid.uuid4())[:12]
            start_time = datetime.now()
            t_name = task_name or func.__name__

            # 记录开始
            run_record = {
                "run_id": run_id,
                "agent_id": _agent_id,
                "skill_id": skill_id,
                "task_name": t_name,
                "status": "running",
                "start_time": start_time.isoformat(),
                "input_data": _safe_input(args, kwargs),
            }
            _store.insert_run(run_record)

            result = None
            error_msg = None
            status = "success"

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                error_msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()[-500:]}"
                raise
            finally:
                end_time = datetime.now()
                duration_ms = (end_time - start_time).total_seconds() * 1000

                _store.update_run(
                    run_id,
                    status=status,
                    end_time=end_time.isoformat(),
                    duration_ms=round(duration_ms, 2),
                    output_data=result if status == "success" else None,
                    error_msg=error_msg,
                )

                # 更新当日聚合指标
                today = start_time.strftime("%Y-%m-%d")
                _store.upsert_daily_metrics(_agent_id, skill_id, today)

                # v0.5.0: 实时反馈上报（异步，不阻塞）
                rt = _get_realtime_reporter()
                if rt:
                    try:
                        rt.enqueue({
                            "run_id": run_id,
                            "agent_id": _agent_id,
                            "skill_id": skill_id,
                            "task_name": t_name,
                            "status": status,
                            "duration_ms": round(duration_ms, 2),
                            "error_type": type(error_msg).__name__ if error_msg else None,
                            "timestamp": end_time.isoformat(),
                        })
                    except Exception:
                        pass  # 实时上报失败不影响主流程

        # 附加元信息便于查询
        wrapper._skill_id = skill_id
        wrapper._task_name = task_name
        return wrapper

    return decorator


def run_skill_function(
    func: Callable,
    skill_id: str,
    task_name: str = "",
    args: tuple = (),
    kwargs: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    命令式调用：运行任意函数并自动采集指标
    返回 {"run_id": ..., "status": ..., "result": ..., "duration_ms": ..., "error": ...}
    """
    if kwargs is None:
        kwargs = {}

    if _store is None or _agent_id is None:
        raise RuntimeError("拦截器未初始化，请先调用 configure(store, agent_id)")

    run_id = str(uuid.uuid4())[:12]
    start_time = datetime.now()
    t_name = task_name or func.__name__

    run_record = {
        "run_id": run_id,
        "agent_id": _agent_id,
        "skill_id": skill_id,
        "task_name": t_name,
        "status": "running",
        "start_time": start_time.isoformat(),
        "input_data": _safe_input(args, kwargs),
    }
    _store.insert_run(run_record)

    result = None
    error_msg = None
    status = "success"

    try:
        result = func(*args, **kwargs)
    except Exception as e:
        status = "error"
        error_msg = f"{type(e).__name__}: {e}"

    end_time = datetime.now()
    duration_ms = (end_time - start_time).total_seconds() * 1000

    _store.update_run(
        run_id,
        status=status,
        end_time=end_time.isoformat(),
        duration_ms=round(duration_ms, 2),
        output_data=result if status == "success" else None,
        error_msg=error_msg,
    )

    today = start_time.strftime("%Y-%m-%d")
    _store.upsert_daily_metrics(_agent_id, skill_id, today)

    # v0.5.0: 实时反馈上报
    rt = _get_realtime_reporter()
    if rt:
        try:
            rt.enqueue({
                "run_id": run_id,
                "agent_id": _agent_id,
                "skill_id": skill_id,
                "task_name": t_name,
                "status": status,
                "duration_ms": round(duration_ms, 2),
                "error_type": type(error_msg).__name__ if error_msg else None,
                "timestamp": end_time.isoformat(),
            })
        except Exception:
            pass

    return {
        "run_id": run_id,
        "skill_id": skill_id,
        "task_name": t_name,
        "status": status,
        "duration_ms": round(duration_ms, 2),
        "result": result,
        "error": error_msg,
    }


def _safe_input(args: tuple, kwargs: dict) -> Optional[dict]:
    """安全地序列化输入参数"""
    try:
        data = {}
        if args:
            data["args"] = [str(a)[:200] for a in args]
        if kwargs:
            data["kwargs"] = {k: str(v)[:200] for k, v in kwargs.items()}
        return data if data else None
    except Exception:
        return None
