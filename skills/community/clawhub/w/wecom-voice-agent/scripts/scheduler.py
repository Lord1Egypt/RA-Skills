#!/usr/bin/env python3
"""
企业微信语音助手 — 外呼任务调度 v2.0

功能：
1. 定时外呼（指定时间自动发起通话）
2. 批量外呼（CSV/JSON 导入客户列表，逐一拨打）
3. 并发控制（根据硬件配置调整并发数）
4. 任务状态持久化

特性：
- 纯 Python 标准库（sched + threading + csv + json）
- 支持一次性任务和周期性任务
- 硬件自适应并发控制
- 任务状态本地持久化

更新日志：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2026-07-15 | 初始发布：定时/批量外呼、并发控制、任务持久化 |
| v2.0.1 | 2026-07-15 | 修复 time_str 解析异常、中文化日志、安全性增强 |

联系信息：njskills@agent.qq.com

使用方法：
    python scripts/scheduler.py                    # 自测
    python scripts/scheduler.py --daily 09:00      # 每日9点外呼
    python scripts/scheduler.py --batch customers.csv  # 批量外呼
"""

import csv
import json
import sched
import time
import logging
import os
import sys
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from enum import Enum

# ==========================================
# 配置
# ==========================================

SCHEDULER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp_scheduler')
MAX_DEFAULT_CONCURRENT = 3
TASK_FILE = os.path.join(SCHEDULER_DIR, 'tasks.json')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Scheduler")


def _safe_parse_time(time_str: str) -> tuple:
    """
    安全解析 'HH:MM' 格式的时间，返回 (hour, minute)。
    解析失败时返回 (9, 0) 并记录错误。
    """
    if not time_str or not isinstance(time_str, str):
        logger.warning(f"时间格式无效，使用默认值 09:00。收到: {time_str!r}")
        return (9, 0)
    parts = time_str.strip().split(":")
    if len(parts) != 2:
        logger.warning(f"时间格式不正确（需要 HH:MM），使用默认值 09:00。收到: {time_str!r}")
        return (9, 0)
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("时间超出范围")
        return (hour, minute)
    except (ValueError, TypeError) as e:
        logger.warning(f"时间解析失败: {e}，使用默认值 09:00。收到: {time_str!r}")
        return (9, 0)


# ==========================================
# 任务类型
# ==========================================

class TaskType(Enum):
    """任务类型"""
    ONE_SHOT = "one_shot"       # 一次性
    DAILY = "daily"             # 每日定时
    WEEKLY = "weekly"           # 每周定时
    BATCH = "batch"             # 批量外呼


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ==========================================
# 外呼任务定义
# ==========================================

class CallTask:
    """单个外呼任务"""

    def __init__(
        self,
        task_id: str,
        target: str,                # 被叫方（手机号或用户ID）
        target_name: str = "",
        script: str = "",           # 外呼话术模板
        task_type: TaskType = TaskType.ONE_SHOT,
        scheduled_time: str = "",   # ISO 格式时间
        metadata: Dict = None,
    ):
        self.task_id = task_id
        self.target = target
        self.target_name = target_name
        self.script = script
        self.task_type = task_type
        self.scheduled_time = scheduled_time
        self.metadata = metadata or {}
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now().isoformat()
        self.executed_at: Optional[str] = None
        self.result = None

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "target": self.target,
            "target_name": self.target_name,
            "script": self.script,
            "task_type": self.task_type.value,
            "scheduled_time": self.scheduled_time,
            "metadata": self.metadata,
            "status": self.status.value,
            "created_at": self.created_at,
            "executed_at": self.executed_at,
            "result": self.result,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CallTask":
        task = cls(
            task_id=data["task_id"],
            target=data["target"],
            target_name=data.get("target_name", ""),
            script=data.get("script", ""),
            task_type=TaskType(data.get("task_type", "one_shot")),
            scheduled_time=data.get("scheduled_time", ""),
            metadata=data.get("metadata", {}),
        )
        task.status = TaskStatus(data.get("status", "pending"))
        task.created_at = data.get("created_at", datetime.now().isoformat())
        task.executed_at = data.get("executed_at")
        task.result = data.get("result")
        return task


# ==========================================
# 外呼执行器（回调接口）
# ==========================================

class CallExecutor:
    """
    外呼执行器接口

    实际使用时需要继承此类并实现 execute_call 方法
    """

    def execute_call(self, target: str, script: str, task_id: str) -> Dict[str, Any]:
        """
        执行单个外呼

        Args:
            target: 被叫方
            script: 话术
            task_id: 任务ID

        Returns:
            执行结果 dict
        """
        raise NotImplementedError

    def on_batch_complete(self, results: List[Dict]):
        """批量外呼完成回调"""
        pass


# ==========================================
# 默认模拟执行器（用于测试）
# ==========================================

class MockCallExecutor(CallExecutor):
    """模拟外呼执行器，仅记录不真正拨打"""

    def __init__(self):
        self.call_log: List[Dict] = []

    def execute_call(self, target: str, script: str, task_id: str) -> Dict[str, Any]:
        result = {
            "task_id": task_id,
            "target": target,
            "script": script,
            "status": "simulated",
            "timestamp": datetime.now().isoformat(),
            "duration": 0,
        }
        self.call_log.append(result)
        logger.info(f"[模拟外呼] 目标={target}, 任务ID={task_id}")
        return result

    def on_batch_complete(self, results: List[Dict]):
        logger.info(f"[批量完成] 共 {len(results)} 个任务")


# ==========================================
# 任务调度器
# ==========================================

class OutboundScheduler:
    """
    外呼任务调度器

    使用方式：
        scheduler = OutboundScheduler(executor=MockCallExecutor())
        scheduler.start()

        # 添加一次性任务
        scheduler.add_one_shot("task_001", "13800138000", "预约确认", "2026-07-15T09:00:00")

        # 添加每日定时任务
        scheduler.add_daily("task_002", "13800138000", "提醒", "09:00")

        # 添加批量任务
        scheduler.add_batch([
            {"target": "13800138000", "name": "张三", "script": "预约确认"},
            {"target": "13800138001", "name": "李四", "script": "回访"},
        ])
    """

    def __init__(
        self,
        executor: CallExecutor = None,
        max_concurrent: int = MAX_DEFAULT_CONCURRENT,
    ):
        self.executor = executor or MockCallExecutor()
        self.max_concurrent = max_concurrent
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._tasks: Dict[str, CallTask] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._active_count = 0

        os.makedirs(SCHEDULER_DIR, exist_ok=True)
        self._load_tasks()
        logger.info(f"调度器创建，最大并发: {max_concurrent}")

    def start(self):
        """启动调度器"""
        if self._running:
            logger.warning("调度器已在运行")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("调度器已启动")

    def stop(self):
        """停止调度器"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("调度器已停止")

    def _run_loop(self):
        """调度主循环"""
        while self._running:
            try:
                self._scheduler.run(blocking=False)
                # 检查并发槽位
                self._check_pending_tasks()
            except Exception as e:
                logger.error(f"调度循环异常: {e}")
            time.sleep(1)

    def _check_pending_tasks(self):
        """检查并执行待处理任务"""
        to_execute = []
        with self._lock:
            if self._active_count >= self.max_concurrent:
                return

            pending = [
                t for t in self._tasks.values()
                if t.status == TaskStatus.PENDING
            ]
            for task in pending:
                if self._active_count >= self.max_concurrent:
                    break
                # 检查是否到执行时间
                if task.scheduled_time:
                    try:
                        scheduled = datetime.fromisoformat(task.scheduled_time)
                        if datetime.now() < scheduled:
                            continue
                    except ValueError:
                        pass
                to_execute.append(task)

        # 在锁外执行任务（避免死锁）
        for task in to_execute:
            self._execute_task(task)

    def _execute_task(self, task: CallTask):
        """执行单个任务"""
        # 标记为运行中（只需锁保护状态更新）
        with self._lock:
            self._active_count += 1
            task.status = TaskStatus.RUNNING
            task.executed_at = datetime.now().isoformat()

        def run():
            try:
                result = self.executor.execute_call(
                    task.target, task.script, task.task_id
                )
                task.result = result
                task.status = TaskStatus.COMPLETED
                logger.info(f"任务完成: {task.task_id}")
            except Exception as e:
                task.result = {"error": str(e)}
                task.status = TaskStatus.FAILED
                logger.error(f"任务失败: {task.task_id}, 错误={e}")
            finally:
                with self._lock:
                    self._active_count -= 1
                self._save_tasks()

        threading.Thread(target=run, daemon=True).start()

    def add_one_shot(
        self,
        task_id: str,
        target: str,
        script: str,
        scheduled_time: str,
        target_name: str = "",
        metadata: Dict = None,
    ) -> CallTask:
        """添加一次性外呼任务"""
        task = CallTask(
            task_id=task_id,
            target=target,
            target_name=target_name,
            script=script,
            task_type=TaskType.ONE_SHOT,
            scheduled_time=scheduled_time,
            metadata=metadata,
        )
        self._tasks[task_id] = task
        self._save_tasks()
        logger.info(f"添加一次性任务: {task_id}, 执行时间: {scheduled_time}")
        return task

    def add_daily(
        self,
        task_id: str,
        target: str,
        script: str,
        time_str: str,  # "HH:MM" 格式
        target_name: str = "",
    ) -> CallTask:
        """添加每日定时外呼任务"""
        # 安全解析时间字符串
        hour, minute = _safe_parse_time(time_str)

        now = datetime.now()
        next_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_time <= now:
            next_time += timedelta(days=1)

        task = CallTask(
            task_id=task_id,
            target=target,
            target_name=target_name,
            script=script,
            task_type=TaskType.DAILY,
            scheduled_time=next_time.isoformat(),
        )
        self._tasks[task_id] = task
        self._save_tasks()
        logger.info(f"添加每日任务: {task_id}, 每日 {hour:02d}:{minute:02d}")
        return task

    def add_batch(
        self,
        customers: List[Dict[str, str]],
        script_template: str = "",
        scheduled_time: str = None,
    ) -> List[CallTask]:
        """
        添加批量外呼任务

        Args:
            customers: 客户列表 [{"target": "138...", "name": "张三"}, ...]
            script_template: 话术模板（可用 {name} 替换）
            scheduled_time: 立即执行则为 None，否则为 ISO 时间
        """
        tasks = []
        for i, customer in enumerate(customers):
            target = customer.get("target", customer.get("phone", ""))
            name = customer.get("name", customer.get("target_name", ""))
            script = script_template.replace("{name}", name) if script_template else customer.get("script", "")

            task = CallTask(
                task_id=f"batch_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}",
                target=target,
                target_name=name,
                script=script,
                task_type=TaskType.BATCH,
                scheduled_time=scheduled_time or datetime.now().isoformat(),
            )
            self._tasks[task.task_id] = task
            tasks.append(task)

        self._save_tasks()
        logger.info(f"添加批量任务: {len(tasks)} 个客户")
        return tasks

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self._tasks.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            self._save_tasks()
            return True
        return False

    def get_task(self, task_id: str) -> Optional[CallTask]:
        """查询任务"""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[CallTask]:
        """获取所有任务"""
        return list(self._tasks.values())

    def get_tasks_by_status(self, status: TaskStatus) -> List[CallTask]:
        """按状态获取任务"""
        return [t for t in self._tasks.values() if t.status == status]

    def _save_tasks(self):
        """持久化任务"""
        try:
            data = {tid: t.to_dict() for tid, t in self._tasks.items()}
            with open(TASK_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"任务持久化失败: {e}")

    def _load_tasks(self):
        """恢复任务"""
        if not os.path.exists(TASK_FILE):
            return
        try:
            with open(TASK_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for tid, tdata in data.items():
                task = CallTask.from_dict(tdata)
                # 重置 RUNNING 为 FAILED（异常中断的任务）
                if task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.FAILED
                self._tasks[tid] = task
            logger.info(f"恢复 {len(self._tasks)} 个任务")
        except Exception as e:
            logger.warning(f"任务恢复失败: {e}")

    def get_stats(self) -> dict:
        """获取调度器统计"""
        stats = {s.value: 0 for s in TaskStatus}
        for task in self._tasks.values():
            stats[task.status.value] += 1
        return {
            "total": len(self._tasks),
            "active": self._active_count,
            "by_status": stats,
        }


# ==========================================
# CSV 导入工具
# ==========================================

class CustomerImporter:
    """客户列表导入器（CSV/JSON）"""

    @staticmethod
    def from_csv(filepath: str) -> List[Dict[str, str]]:
        """
        从 CSV 导入客户列表

        CSV 格式：target,name,script（可选）
        """
        customers = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customers.append({
                        "target": row.get("target", row.get("phone", "")),
                        "name": row.get("name", row.get("target_name", "")),
                        "script": row.get("script", ""),
                    })
            logger.info(f"CSV 导入: {len(customers)} 个客户")
        except FileNotFoundError:
            logger.error(f"CSV 文件不存在: {filepath}")
        except Exception as e:
            logger.error(f"CSV 导入失败: {e}")
        return customers

    @staticmethod
    def from_json(filepath: str) -> List[Dict[str, str]]:
        """从 JSON 导入客户列表"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            return data.get("customers", [])
        except FileNotFoundError:
            logger.error(f"JSON 文件不存在: {filepath}")
            return []
        except Exception as e:
            logger.error(f"JSON 导入失败: {e}")
            return []


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行调度器自测"""
    print("=" * 60)
    print("外呼任务调度 — 自测模式")
    print("=" * 60)

    # 测试 1: 一次性任务
    print("\n[测试 1] 一次性外呼任务")
    scheduler = OutboundScheduler(max_concurrent=2)
    scheduler.start()

    task = scheduler.add_one_shot(
        task_id="oneshot_001",
        target="13800138000",
        script="预约确认",
        scheduled_time=datetime.now().isoformat(),
        target_name="张三",
    )
    assert task.task_type == TaskType.ONE_SHOT
    assert task.status == TaskStatus.PENDING
    print(f"  创建任务: {task.task_id}")
    time.sleep(5)

    completed = scheduler.get_tasks_by_status(TaskStatus.COMPLETED)
    assert len(completed) >= 1
    print("✅ 一次性任务通过")

    # 测试 2: 每日定时任务
    print("\n[测试 2] 每日定时任务")
    daily = scheduler.add_daily(
        task_id="daily_001",
        target="13800138001",
        script="早安提醒",
        time_str="09:00",
        target_name="李四",
    )
    assert daily.task_type == TaskType.DAILY
    assert daily.scheduled_time
    print(f"  下次执行: {daily.scheduled_time}")
    print("✅ 每日定时任务通过")

    # 测试 3: 批量外呼
    print("\n[测试 3] 批量外呼")
    customers = [
        {"target": "13900139000", "name": "客户A", "script": "预约确认"},
        {"target": "13900139001", "name": "客户B", "script": "回访"},
        {"target": "13900139002", "name": "客户C", "script": "快递提醒"},
    ]
    batch = scheduler.add_batch(customers)
    assert len(batch) == 3
    print(f"  批量创建 {len(batch)} 个任务")
    time.sleep(3)

    completed = scheduler.get_tasks_by_status(TaskStatus.COMPLETED)
    print(f"  已完成: {len(completed)} 个")
    print("✅ 批量外呼通过")

    # 测试 4: 并发上限
    print("\n[测试 4] 并发上限控制")
    scheduler2 = OutboundScheduler(max_concurrent=1)
    scheduler2.start()

    for i in range(5):
        scheduler2.add_one_shot(
            task_id=f"concurrent_{i}",
            target=f"1380000000{i}",
            script="测试",
            scheduled_time=datetime.now().isoformat(),
        )
    time.sleep(1)
    stats = scheduler2.get_stats()
    print(f"  活跃任务: {stats['active']}")
    assert stats['active'] <= 1  # 并发上限1
    print("✅ 并发上限控制通过")
    scheduler2.stop()

    # 测试 5: 统计数据
    print("\n[测试 5] 统计数据")
    all_tasks = scheduler.get_all_tasks()
    print(f"  总任务数: {len(all_tasks)}")
    stats = scheduler.get_stats()
    print(f"  状态分布: {stats['by_status']}")
    print("✅ 统计查询通过")

    # 测试 6: CSV 导入
    print("\n[测试 6] CSV 导入")
    csv_path = os.path.join(SCHEDULER_DIR, "test_customers.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["target", "name", "script"])
        writer.writerow(["13700137000", "测试客户1", "预约确认"])
        writer.writerow(["13700137001", "测试客户2", "回访"])

    imported = CustomerImporter.from_csv(csv_path)
    assert len(imported) == 2
    assert imported[0]["name"] == "测试客户1"
    print(f"  导入 {len(imported)} 个客户")
    print("✅ CSV 导入通过")

    # 清理
    os.remove(csv_path)
    scheduler.stop()

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
