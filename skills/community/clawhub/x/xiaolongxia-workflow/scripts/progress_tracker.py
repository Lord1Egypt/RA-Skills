#!/usr/bin/env python3
"""
进度跟踪器 - 小龙虾工作流 v0.5.0 辅助组件

功能：
1. 实时跟踪任务进度
2. 生成进度报告（文本/HTML）
3. 预估剩余时间
4. 生成简单ASCII图表
5. WebSocket实时推送（可选）
6. 进度异常检测
"""

import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TaskProgress:
    """任务进度数据"""
    task_id: str
    task_name: str
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    skipped_steps: int = 0
    current_phase: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    last_update_time: datetime = field(default_factory=datetime.now)
    estimated_total_hours: float = 0.0
    phases: List[Dict[str, Any]] = field(default_factory=list)
    recent_activities: List[Dict[str, Any]] = field(default_factory=list)
    custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def completion_percentage(self) -> float:
        """完成百分比"""
        if self.total_steps == 0:
            return 0.0
        return min(100.0, (self.completed_steps / self.total_steps) * 100)
    
    @property
    def elapsed_hours(self) -> float:
        """已用时间（小时）"""
        elapsed = self.last_update_time - self.start_time
        return elapsed.total_seconds() / 3600
    
    @property
    def estimated_remaining_hours(self) -> float:
        """预估剩余时间（小时）"""
        if self.completed_steps == 0:
            return self.estimated_total_hours
        
        avg_time_per_step = self.elapsed_hours / self.completed_steps
        remaining_steps = self.total_steps - self.completed_steps
        return avg_time_per_step * remaining_steps
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.completed_steps == 0:
            return 100.0
        return ((self.completed_steps - self.failed_steps) / self.completed_steps) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['completion_percentage'] = self.completion_percentage
        data['elapsed_hours'] = self.elapsed_hours
        data['estimated_remaining_hours'] = self.estimated_remaining_hours
        data['success_rate'] = self.success_rate
        return data


@dataclass
class ProgressAlert:
    """进度警报"""
    level: str  # info, warning, error, critical
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化进度跟踪器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.tasks: Dict[str, TaskProgress] = {}
        self.alerts: List[ProgressAlert] = []
        self._callbacks: List[Callable[[TaskProgress], None]] = []
        self._alert_callbacks: List[Callable[[ProgressAlert], None]] = []
        self._update_lock = threading.Lock()
        
        # 启动后台线程（用于定时报告等）
        self._running = True
        if self.config['enable_background_reporting']:
            self._report_thread = threading.Thread(target=self._background_report_loop, daemon=True)
            self._report_thread.start()
        
        logger.info("进度跟踪器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'enable_background_reporting': True,
            'report_interval_seconds': 300,  # 5分钟
            'enable_websocket': False,
            'websocket_port': 8765,
            'enable_ascii_charts': True,
            'chart_width': 50,
            'enable_anomaly_detection': True,
            'anomaly_threshold': 0.3,  # 30%偏差
            'alert_on_stagnation': True,
            'stagnation_threshold_minutes': 60,
            'log_progress_to_file': True,
            'log_directory': '/tmp/xlx_progress_logs',
            'max_history_per_task': 100
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 深度合并
                if 'progress_tracker' in user_config:
                    for key, value in user_config['progress_tracker'].items():
                        default_config[key] = value
            except Exception as e:
                logger.warning(f"加载进度跟踪配置失败，使用默认配置: {e}")
        
        return default_config
    
    def _background_report_loop(self):
        """后台报告循环"""
        while self._running:
            time.sleep(self.config['report_interval_seconds'])
            
            with self._update_lock:
                if not self.tasks:
                    continue
                
                # 生成状态报告
                report = self._generate_system_report()
                
                # 记录到文件
                if self.config['log_progress_to_file']:
                    self._log_report(report)
                
                # 检查异常
                if self.config['enable_anomaly_detection']:
                    self._check_anomalies()
                
                # 检查停滞
                if self.config['alert_on_stagnation']:
                    self._check_stagnation()
    
    def _generate_system_report(self) -> Dict[str, Any]:
        """生成系统报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'active_tasks': sum(1 for t in self.tasks.values() 
                               if t.completion_percentage < 100),
            'completed_tasks': sum(1 for t in self.tasks.values() 
                                  if t.completion_percentage >= 100),
            'tasks': []
        }
        
        for task_id, task in self.tasks.items():
            task_report = task.to_dict()
            task_report['task_id'] = task_id
            report['tasks'].append(task_report)
        
        return report
    
    def _log_report(self, report: Dict[str, Any]):
        """记录报告到文件"""
        try:
            log_dir = Path(self.config['log_directory'])
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d')
            log_file = log_dir / f"progress_report_{timestamp}.jsonl"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(report, ensure_ascii=False, default=str) + '\n')
            
            logger.debug(f"进度报告已记录: {log_file}")
        except Exception as e:
            logger.warning(f"记录进度报告失败: {e}")
    
    def _check_anomalies(self):
        """检查进度异常"""
        for task_id, task in self.tasks.items():
            if task.completed_steps < 5:  # 数据太少
                continue
            
            # 计算预期的进度速度
            expected_speed = task.estimated_total_hours / task.total_steps
            actual_speed = task.elapsed_hours / task.completed_steps
            
            deviation = abs(actual_speed - expected_speed) / expected_speed
            
            if deviation > self.config['anomaly_threshold']:
                alert = ProgressAlert(
                    level='warning',
                    message=f"任务 {task.task_name} 进度异常: 实际速度偏离预期 {deviation:.1%}",
                    data={
                        'task_id': task_id,
                        'expected_speed': expected_speed,
                        'actual_speed': actual_speed,
                        'deviation': deviation
                    }
                )
                self.add_alert(alert)
    
    def _check_stagnation(self):
        """检查进度停滞"""
        stagnation_threshold = self.config['stagnation_threshold_minutes'] * 60
        
        for task_id, task in self.tasks.items():
            if task.completion_percentage >= 100:
                continue
            
            time_since_update = (datetime.now() - task.last_update_time).total_seconds()
            
            if time_since_update > stagnation_threshold:
                alert = ProgressAlert(
                    level='warning',
                    message=f"任务 {task.task_name} 进度停滞 {time_since_update/60:.1f} 分钟",
                    data={
                        'task_id': task_id,
                        'stagnation_minutes': time_since_update / 60,
                        'completion_percentage': task.completion_percentage
                    }
                )
                self.add_alert(alert)
    
    def register_task(self, task_id: str, task_name: str, total_steps: int = 0, 
                     estimated_hours: float = 0.0) -> TaskProgress:
        """
        注册新任务
        
        Args:
            task_id: 任务ID
            task_name: 任务名称
            total_steps: 总步骤数
            estimated_hours: 预计总小时数
            
        Returns:
            TaskProgress: 任务进度对象
        """
        with self._update_lock:
            if task_id in self.tasks:
                logger.warning(f"任务已存在: {task_id}")
                return self.tasks[task_id]
            
            task = TaskProgress(
                task_id=task_id,
                task_name=task_name,
                total_steps=total_steps,
                estimated_total_hours=estimated_hours
            )
            
            self.tasks[task_id] = task
            logger.info(f"注册新任务: {task_name} ({task_id})")
            
            # 触发回调
            for callback in self._callbacks:
                try:
                    callback(task)
                except Exception as e:
                    logger.warning(f"进度回调失败: {e}")
            
            return task
    
    def update_task(self, task_id: str, **kwargs) -> Optional[TaskProgress]:
        """
        更新任务进度
        
        Args:
            task_id: 任务ID
            **kwargs: 更新字段
            
        Returns:
            TaskProgress: 更新后的任务进度对象
        """
        with self._update_lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return None
            
            task = self.tasks[task_id]
            
            # 更新字段
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            # 更新最后更新时间
            task.last_update_time = datetime.now()
            
            # 记录活动
            if 'current_phase' in kwargs or 'completed_steps' in kwargs:
                activity = {
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'description': f"进度更新: {kwargs.get('description', '未指定')}",
                    'data': kwargs.copy()
                }
                task.recent_activities.append(activity)
                if len(task.recent_activities) > 10:
                    task.recent_activities = task.recent_activities[-10:]
            
            logger.debug(f"更新任务进度: {task_id} -> {task.completion_percentage:.1f}%")
            
            # 触发回调
            for callback in self._callbacks:
                try:
                    callback(task)
                except Exception as e:
                    logger.warning(f"进度回调失败: {e}")
            
            return task
    
    def add_step_result(self, task_id: str, success: bool = True, 
                       skipped: bool = False, description: str = ""):
        """
        添加步骤执行结果
        
        Args:
            task_id: 任务ID
            success: 是否成功
            skipped: 是否跳过
            description: 步骤描述
        """
        with self._update_lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return
            
            task = self.tasks[task_id]
            
            if skipped:
                task.skipped_steps += 1
            elif success:
                task.completed_steps += 1
            else:
                task.failed_steps += 1
            
            task.last_update_time = datetime.now()
            
            # 记录活动
            status = "成功" if success else "失败" if not skipped else "跳过"
            activity = {
                'time': datetime.now().strftime('%H:%M:%S'),
                'description': f"步骤执行{status}: {description}",
                'data': {'success': success, 'skipped': skipped}
            }
            task.recent_activities.append(activity)
            if len(task.recent_activities) > 10:
                task.recent_activities = task.recent_activities[-10:]
            
            # 触发回调
            for callback in self._callbacks:
                try:
                    callback(task)
                except Exception as e:
                    logger.warning(f"进度回调失败: {e}")
    
    def add_phase(self, task_id: str, phase_name: str, total_steps: int = 0, 
                 description: str = ""):
        """
        添加阶段
        
        Args:
            task_id: 任务ID
            phase_name: 阶段名称
            total_steps: 阶段总步骤数
            description: 阶段描述
        """
        with self._update_lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return
            
            task = self.tasks[task_id]
            
            phase = {
                'name': phase_name,
                'description': description,
                'total_steps': total_steps,
                'completed_steps': 0,
                'status': 'pending',
                'start_time': None,
                'end_time': None
            }
            
            task.phases.append(phase)
    
    def update_phase(self, task_id: str, phase_index: int, **kwargs):
        """
        更新阶段状态
        
        Args:
            task_id: 任务ID
            phase_index: 阶段索引
            **kwargs: 更新字段
        """
        with self._update_lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return
            
            task = self.tasks[task_id]
            
            if phase_index < 0 or phase_index >= len(task.phases):
                logger.warning(f"阶段索引无效: {phase_index}")
                return
            
            phase = task.phases[phase_index]
            phase.update(kwargs)
    
    def get_task_progress(self, task_id: str) -> Optional[TaskProgress]:
        """获取任务进度"""
        return self.tasks.get(task_id)
    
    def get_all_progress(self) -> Dict[str, TaskProgress]:
        """获取所有任务进度"""
        return self.tasks.copy()
    
    def generate_progress_report(self, task_id: Optional[str] = None, 
                               format: str = 'text') -> str:
        """
        生成进度报告
        
        Args:
            task_id: 任务ID（None表示所有任务）
            format: 报告格式 ('text', 'html', 'json')
            
        Returns:
            str: 进度报告
        """
        if task_id:
            task = self.tasks.get(task_id)
            if not task:
                return f"任务不存在: {task_id}"
            
            if format == 'json':
                return json.dumps(task.to_dict(), ensure_ascii=False, indent=2)
            elif format == 'html':
                return self._generate_html_report(task)
            else:
                return self._generate_text_report(task)
        else:
            # 所有任务
            if format == 'json':
                data = {tid: t.to_dict() for tid, t in self.tasks.items()}
                return json.dumps(data, ensure_ascii=False, indent=2)
            elif format == 'html':
                return self._generate_html_system_report()
            else:
                return self._generate_text_system_report()
    
    def _generate_text_report(self, task: TaskProgress) -> str:
        """生成文本报告"""
        report = []
        report.append(f"📊 任务进度报告: {task.task_name}")
        report.append(f"  任务ID: {task.task_id}")
        report.append(f"  开始时间: {task.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"  最后更新: {task.last_update_time.strftime('%H:%M:%S')}")
        report.append("")
        
        # 进度条
        if self.config['enable_ascii_charts']:
            progress_bar = self._create_ascii_progress_bar(task.completion_percentage)
            report.append(f"  进度: {progress_bar} {task.completion_percentage:.1f}%")
        else:
            report.append(f"  进度: {task.completion_percentage:.1f}%")
        
        report.append("")
        report.append(f"  📈 统计信息:")
        report.append(f"    总步骤: {task.total_steps}")
        report.append(f"    已完成: {task.completed_steps}")
        report.append(f"    已失败: {task.failed_steps}")
        report.append(f"    已跳过: {task.skipped_steps}")
        report.append(f"    成功率: {task.success_rate:.1f}%")
        report.append(f"    已用时间: {task.elapsed_hours:.1f} 小时")
        report.append(f"    预估剩余: {task.estimated_remaining_hours:.1f} 小时")
        report.append("")
        
        # 阶段信息
        if task.phases:
            report.append(f"  📋 阶段进展:")
            for i, phase in enumerate(task.phases):
                phase_percent = (phase.get('completed_steps', 0) / phase.get('total_steps', 1)) * 100
                report.append(f"    {i+1}. {phase['name']}: {phase.get('status', 'pending')} "
                            f"({phase_percent:.1f}%)")
        
        # 最近活动
        if task.recent_activities:
            report.append("")
            report.append(f"  🔄 最近活动:")
            for activity in task.recent_activities[-5:]:
                report.append(f"    • {activity['time']}: {activity['description']}")
        
        return '\n'.join(report)
    
    def _create_ascii_progress_bar(self, percentage: float) -> str:
        """创建ASCII进度条"""
        width = self.config['chart_width']
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = '█' * filled + '░' * empty
        return f"[{bar}]"
    
    def _generate_text_system_report(self) -> str:
        """生成系统文本报告"""
        report = []
        report.append(f"📊 系统进度报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"  总任务数: {len(self.tasks)}")
        report.append(f"  活跃任务: {sum(1 for t in self.tasks.values() if t.completion_percentage < 100)}")
        report.append(f"  已完成任务: {sum(1 for t in self.tasks.values() if t.completion_percentage >= 100)}")
        report.append("")
        
        for task_id, task in self.tasks.items():
            report.append(f"  🦞 {task.task_name} [{task_id}]")
            report.append(f"    进度: {task.completion_percentage:.1f}% | "
                         f"步骤: {task.completed_steps}/{task.total_steps} | "
                         f"剩余: {task.estimated_remaining_hours:.1f}h")
        
        # 警报
        if self.alerts:
            report.append("")
            report.append(f"  ⚠️  最近警报 ({len(self.alerts)}):")
            for alert in self.alerts[-3:]:
                report.append(f"    • {alert.timestamp.strftime('%H:%M')} [{alert.level}]: {alert.message}")
        
        return '\n'.join(report)
    
    def _generate_html_report(self, task: TaskProgress) -> str:
        """生成HTML报告（简化版）"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>任务进度报告: {task.task_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .progress-bar {{ height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 20px 0; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .stat-box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #4CAF50; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        .phase {{ margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; background: #f9f9f9; }}
        .activity {{ margin: 10px 0; padding: 10px; border-bottom: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 小龙虾工作流进度报告</h1>
        <h2>{task.task_name}</h2>
        <p>任务ID: {task.task_id} | 开始时间: {task.start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h3>整体进度</h3>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {task.completion_percentage}%;"></div>
    </div>
    <p style="text-align: center; font-size: 24px; font-weight: bold;">{task.completion_percentage:.1f}% 完成</p>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{task.completed_steps}/{task.total_steps}</div>
            <div class="stat-label">已完成步骤</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{task.success_rate:.1f}%</div>
            <div class="stat-label">成功率</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{task.elapsed_hours:.1f}h</div>
            <div class="stat-label">已用时间</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{task.estimated_remaining_hours:.1f}h</div>
            <div class="stat-label">剩余时间</div>
        </div>
    </div>
"""
        
        # 阶段信息
        if task.phases:
            html += "<h3>阶段进展</h3>"
            for i, phase in enumerate(task.phases):
                phase_percent = (phase.get('completed_steps', 0) / phase.get('total_steps', 1)) * 100
                html += f"""
                <div class="phase">
                    <h4>阶段 {i+1}: {phase['name']}</h4>
                    <p>{phase.get('description', '')}</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {phase_percent}%;"></div>
                    </div>
                    <p>状态: {phase.get('status', 'pending')} | 完成度: {phase_percent:.1f}%</p>
                </div>
"""
        
        # 最近活动
        if task.recent_activities:
            html += "<h3>最近活动</h3>"
            for activity in task.recent_activities[-10:]:
                html += f"""
                <div class="activity">
                    <strong>{activity['time']}:</strong> {activity['description']}
                </div>
"""
        
        html += """
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; text-align: center;">
        <p>小龙虾工作流 v0.5.0 | 报告生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_html_system_report(self) -> str:
        """生成系统HTML报告（简化版）"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>系统进度报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .task-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }}
        .task-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .task-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .task-progress {{ height: 10px; background: #e0e0e0; border-radius: 5px; overflow: hidden; margin: 10px 0; }}
        .task-progress-fill {{ height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); }}
        .alert-panel {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin: 30px 0; }}
        .alert {{ padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; background: white; }}
        .stat-box {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 小龙虾工作流系统监控</h1>
            <p>实时任务进度跟踪 | 系统时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
        
        <div class="stat-box">
            <h2>📈 系统概览</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin: 20px 0;">
                <div>
                    <h3 style="color: #667eea; margin: 0;">{len(self.tasks)}</h3>
                    <p>总任务数</p>
                </div>
                <div>
                    <h3 style="color: #4CAF50; margin: 0;">{sum(1 for t in self.tasks.values() if t.completion_percentage >= 100)}</h3>
                    <p>已完成</p>
                </div>
                <div>
                    <h3 style="color: #ff9800; margin: 0;">{sum(1 for t in self.tasks.values() if t.completion_percentage < 100 and t.completion_percentage > 0)}</h3>
                    <p>进行中</p>
                </div>
                <div>
                    <h3 style="color: #9c27b0; margin: 0;">{len(self.alerts)}</h3>
                    <p>活跃警报</p>
                </div>
            </div>
        </div>
        
        <h2>📋 任务列表</h2>
        <div class="task-grid">
"""
        
        for task_id, task in self.tasks.items():
            status_color = "#4CAF50" if task.completion_percentage >= 100 else "#ff9800"
            status_text = "已完成" if task.completion_percentage >= 100 else "进行中"
            
            html += f"""
            <div class="task-card">
                <div class="task-header">
                    <h3 style="margin: 0;">{task.task_name}</h3>
                    <span style="background: {status_color}; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">
                        {status_text}
                    </span>
                </div>
                <p style="color: #666; font-size: 14px;">ID: {task_id}</p>
                <p>开始时间: {task.start_time.strftime('%Y-%m-%d %H:%M')}</p>
                
                <div class="task-progress">
                    <div class="task-progress-fill" style="width: {task.completion_percentage}%;"></div>
                </div>
                <p style="text-align: center; font-weight: bold;">{task.completion_percentage:.1f}% 完成</p>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 15px 0;">
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #666;">步骤</p>
                        <p style="margin: 0; font-weight: bold;">{task.completed_steps}/{task.total_steps}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #666;">成功率</p>
                        <p style="margin: 0; font-weight: bold;">{task.success_rate:.1f}%</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #666;">已用时间</p>
                        <p style="margin: 0; font-weight: bold;">{task.elapsed_hours:.1f}h</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; color: #666;">剩余时间</p>
                        <p style="margin: 0; font-weight: bold;">{task.estimated_remaining_hours:.1f}h</p>
                    </div>
                </div>
            </div>
"""
        
        html += """
        </div>
"""
        
        # 警报面板
        if self.alerts:
            html += """
        <div class="alert-panel">
            <h2>⚠️ 系统警报</h2>
"""
            for alert in self.alerts[-10:]:
                alert_color = {
                    'info': '#2196F3',
                    'warning': '#ff9800',
                    'error': '#f44336',
                    'critical': '#d32f2f'
                }.get(alert.level, '#666')
                
                html += f"""
            <div class="alert" style="border-left-color: {alert_color};">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{alert.message}</strong>
                    <span style="color: #666; font-size: 12px;">{alert.timestamp.strftime('%H:%M:%S')}</span>
                </div>
                <div style="margin-top: 5px;">
                    <span style="background: {alert_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px;">
                        {alert.level.upper()}
                    </span>
                </div>
            </div>
"""
            html += """
        </div>
"""
        
        html += """
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; text-align: center;">
            <p>小龙虾工作流 v0.5.0 | 系统监控面板 | 自动更新每5分钟</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def add_alert(self, alert: ProgressAlert):
        """添加警报"""
        self.alerts.append(alert)
        
        # 触发警报回调
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.warning(f"警报回调失败: {e}")
        
        logger.info(f"进度警报: [{alert.level}] {alert.message}")
    
    def register_callback(self, callback: Callable[[TaskProgress], None]):
        """注册进度回调"""
        self._callbacks.append(callback)
    
    def register_alert_callback(self, callback: Callable[[ProgressAlert], None]):
        """注册警报回调"""
        self._alert_callbacks.append(callback)
    
    def stop(self):
        """停止跟踪器"""
        self._running = False
    
    def save_state(self, file_path: str):
        """保存状态到文件"""
        try:
            state = {
                'tasks': {tid: t.to_dict() for tid, t in self.tasks.items()},
                'alerts': [asdict(a) for a in self.alerts],
                'saved_at': datetime.now().isoformat()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            logger.info(f"进度状态已保存: {file_path}")
        except Exception as e:
            logger.error(f"保存进度状态失败: {e}")
    
    def load_state(self, file_path: str):
        """从文件加载状态"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 加载任务
            self.tasks.clear()
            for tid, task_data in state.get('tasks', {}).items():
                # 转换字符串时间为datetime
                for time_key in ['start_time', 'last_update_time']:
                    if time_key in task_data and isinstance(task_data[time_key], str):
                        task_data[time_key] = datetime.fromisoformat(task_data[time_key])
                
                task = TaskProgress(**task_data)
                self.tasks[tid] = task
            
            # 加载警报
            self.alerts.clear()
            for alert_data in state.get('alerts', []):
                if 'timestamp' in alert_data and isinstance(alert_data['timestamp'], str):
                    alert_data['timestamp'] = datetime.fromisoformat(alert_data['timestamp'])
                alert = ProgressAlert(**alert_data)
                self.alerts.append(alert)
            
            logger.info(f"进度状态已加载: {file_path}")
        except Exception as e:
            logger.error(f"加载进度状态失败: {e}")


def test_progress_tracker():
    """测试进度跟踪器"""
    print("🧪 测试进度跟踪器...")
    
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory(prefix='xlx_tracker_') as tmpdir:
        # 创建测试配置
        test_config = {
            'progress_tracker': {
                'enable_background_reporting': False,  # 测试中禁用后台
                'enable_ascii_charts': True,
                'chart_width': 40
            }
        }
        
        config_file = Path(tmpdir) / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=2)
        
        # 初始化跟踪器
        tracker = ProgressTracker(str(config_file))
        
        print("✅ 进度跟踪器初始化完成")
        
        # 注册测试任务
        task = tracker.register_task(
            task_id="test_task_001",
            task_name="电商平台开发",
            total_steps=56,
            estimated_hours=40
        )
        
        print(f"✅ 注册测试任务: {task.task_name}")
        
        # 添加阶段
        tracker.add_phase("test_task_001", "需求分析", 10, "收集和分析需求")
        tracker.add_phase("test_task_001", "架构设计", 15, "设计系统架构")
        tracker.add_phase("test_task_001", "核心开发", 25, "开发核心功能")
        tracker.add_phase("test_task_001", "测试部署", 6, "测试和部署系统")
        
        print("✅ 添加4个阶段")
        
        # 更新阶段状态
        tracker.update_phase("test_task_001", 0, status="completed", completed_steps=10, 
                           start_time="2026-03-17T09:00:00", end_time="2026-03-17T12:00:00")
        tracker.update_phase("test_task_001", 1, status="completed", completed_steps=15,
                           start_time="2026-03-17T13:00:00", end_time="2026-03-17T18:00:00")
        tracker.update_phase("test_task_001", 2, status="in_progress", completed_steps=12,
                           start_time="2026-03-17T19:00:00")
        
        print("✅ 更新阶段状态")
        
        # 模拟进度更新
        tracker.update_task("test_task_001", 
                          completed_steps=37,
                          current_phase="核心开发",
                          description="完成用户认证模块")
        
        print("✅ 更新任务进度")
        
        # 添加步骤结果
        tracker.add_step_result("test_task_001", success=True, description="实现登录功能")
        tracker.add_step_result("test_task_001", success=True, description="实现注册功能")
        tracker.add_step_result("test_task_001", success=False, description="支付集成测试")
        
        print("✅ 添加3个步骤结果")
        
        # 生成进度报告
        report = tracker.generate_progress_report("test_task_001", format='text')
        print("\n📊 进度报告:")
        print(report)
        
        # 测试系统报告
        system_report = tracker.generate_progress_report(format='text')
        print("\n📈 系统报告:")
        print(system_report)
        
        # 测试HTML报告
        html_report = tracker.generate_progress_report("test_task_001", format='html')
        html_file = Path(tmpdir) / "progress_report.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        print(f"\n✅ HTML报告已保存: {html_file}")
        
        # 测试状态保存/加载
        state_file = Path(tmpdir) / "tracker_state.json"
        tracker.save_state(str(state_file))
        
        new_tracker = ProgressTracker()
        new_tracker.load_state(str(state_file))
        
        print(f"✅ 状态保存/加载测试完成，加载任务数: {len(new_tracker.tasks)}")
        
        # 测试警报
        alert = ProgressAlert(
            level="warning",
            message="任务进展缓慢，考虑调整资源分配",
            data={"task_id": "test_task_001", "slow_factor": 2.5}
        )
        tracker.add_alert(alert)
        
        print(f"✅ 添加警报，总警报数: {len(tracker.alerts)}")
    
    print("\n✅ 进度跟踪器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_progress_tracker()
    else:
        print("用法:")
        print("  python progress_tracker.py test")
        print("\n集成到工作流:")
        print("  from progress_tracker import ProgressTracker")
        print("  tracker = ProgressTracker()")