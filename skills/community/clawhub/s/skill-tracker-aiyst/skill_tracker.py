#!/usr/bin/env python3
"""
技能追踪器 - Python 版本 (v1.2.0 生产环境版)

作者：aiyst
邮箱：aiyst@qq.com
GitHub: https://github.com/aiyst1982

特性：
- 非阻塞异步执行
- 异常隔离
- 重试机制
- 耗时统计
- 文件锁（并发安全）
- 原子写入
- 配置项
- 统一日志
"""

import json
import os
import threading
import time
import fcntl
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# ============ 配置 ============
class Config:
    """追踪器配置"""
    DATA_DIR = Path(__file__).parent / 'data'
    STATS_FILE = DATA_DIR / 'skill-stats.json'
    USAGE_LOG = DATA_DIR / 'usage-log.jsonl'
    LOCK_FILE = DATA_DIR / '.stats.lock'
    
    # 可配置项
    MAX_RETRIES = 3
    RETRY_DELAY = 0.1  # 秒
    LOG_LEVEL = 'INFO'
    ENABLE_LOGGING = True

# 确保数据目录存在
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============ 日志配置 ============
def setup_logger():
    """配置统一日志"""
    logger = logging.getLogger('SkillTracker')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # 避免重复添加 handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()

# ============ 文件锁 ============
_file_lock = threading.Lock()


def atomic_write(file_path: Path, content: str):
    """原子写入文件（避免并发损坏）"""
    temp_file = file_path.with_suffix('.tmp')
    try:
        # 写入临时文件
        temp_file.write_text(content, encoding='utf-8')
        # 确保写入磁盘
        fd = os.open(str(temp_file), os.O_RDONLY)
        os.fsync(fd)
        os.close(fd)
        # 原子替换
        temp_file.replace(file_path)
    except Exception as e:
        logger.error(f"原子写入失败：{e}")
        if temp_file.exists():
            temp_file.unlink()
        raise


def read_with_lock(file_path: Path) -> Dict[str, Any]:
    """带锁读取文件"""
    with _file_lock:
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, FileNotFoundError):
            return {}


def write_with_lock(file_path: Path, data: Dict[str, Any]):
    """带锁写入文件"""
    with _file_lock:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        atomic_write(file_path, content)


# ============ 初始化 ============
def init_stats_file():
    """初始化统计文件"""
    if not Config.STATS_FILE.exists():
        initial_data = {
            'totalCalls': 0,
            'skills': {},
            'lastUpdated': datetime.now().isoformat()
        }
        write_with_lock(Config.STATS_FILE, initial_data)


# 初始化
init_stats_file()


# ============ 核心功能 ============
def track(skill_name: str, action: str = 'call', context: Optional[Dict] = None):
    """
    记录技能调用（非阻塞，异常隔离）
    
    Args:
        skill_name: 技能名称
        action: 动作类型 (call/success/fail)
        context: 上下文信息（可选）
    
    Returns:
        None (不阻塞，立即返回)
    """
    context = context or {}
    
    # 异步非阻塞执行（使用线程）
    thread = threading.Thread(
        target=_track_impl,
        args=(skill_name, action, context),
        daemon=True,
        name=f'SkillTracker-{skill_name}'
    )
    thread.start()
    
    # 立即返回，不阻塞主流程
    return None


def _track_impl(skill_name: str, action: str, context: Dict):
    """实际追踪实现（在后台线程运行）"""
    try:
        timestamp = datetime.now().isoformat()
        date = datetime.now().strftime('%Y-%m-%d')
        start_time = context.get('start_time', datetime.now())
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # 写入日志（追加模式，天然线程安全）
        log_entry = {
            'timestamp': timestamp,
            'date': date,
            'skill': skill_name,
            'action': action,
            'duration_ms': duration_ms,
            'context': {
                'user': context.get('user', '韩先生'),
                'channel': context.get('channel', 'feishu'),
                'session_id': context.get('session_id'),
                'success': context.get('success', True),
                'error': context.get('error')
            }
        }
        
        # 追加日志（行级原子操作）
        with Config.USAGE_LOG.open('a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # 更新统计（带锁和重试）
        _update_stats(skill_name, action, duration_ms)
        
    except Exception as e:
        # 异常隔离：追踪失败不影响主流程
        if Config.ENABLE_LOGGING:
            logger.error(f"记录失败：{e}", exc_info=True)


def _update_stats(skill_name: str, action: str, duration_ms: int = 0):
    """更新统计数据（带锁和重试机制）"""
    last_error = None
    
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            # 读取现有统计（带锁）
            stats = read_with_lock(Config.STATS_FILE)
            
            # 更新总调用
            if action == 'call':
                stats['totalCalls'] = stats.get('totalCalls', 0) + 1
            
            # 更新技能统计
            if skill_name not in stats['skills']:
                stats['skills'][skill_name] = {
                    'calls': 0,
                    'success': 0,
                    'fail': 0,
                    'totalDuration': 0,
                    'firstUsed': datetime.now().isoformat(),
                    'lastUsed': datetime.now().isoformat()
                }
            
            skill = stats['skills'][skill_name]
            
            if action == 'call':
                skill['calls'] = skill.get('calls', 0) + 1
            elif action == 'success':
                skill['success'] = skill.get('success', 0) + 1
            elif action == 'fail':
                skill['fail'] = skill.get('fail', 0) + 1
            
            # 累加执行耗时
            skill['totalDuration'] = skill.get('totalDuration', 0) + duration_ms
            skill['avgDuration'] = round(skill['totalDuration'] / skill['calls']) if skill['calls'] > 0 else 0
            
            skill['lastUsed'] = datetime.now().isoformat()
            stats['lastUpdated'] = skill['lastUsed']
            
            # 保存统计（带锁和原子写入）
            write_with_lock(Config.STATS_FILE, stats)
            
            if Config.ENABLE_LOGGING:
                logger.debug(f"更新统计成功：{skill_name} ({action})")
            
            return
            
        except Exception as e:
            last_error = e
            if Config.ENABLE_LOGGING:
                logger.warning(f"更新统计失败 (尝试 {attempt}/{Config.MAX_RETRIES}): {e}")
            
            # 重试前等待
            if attempt < Config.MAX_RETRIES:
                time.sleep(Config.RETRY_DELAY * attempt)
    
    # 所有重试失败
    if Config.ENABLE_LOGGING:
        logger.error(f"更新统计最终失败：{last_error}", exc_info=True)


# ============ 查询功能 ============
def get_report() -> Dict[str, Any]:
    """获取统计报告"""
    try:
        stats = read_with_lock(Config.STATS_FILE)
        
        # 计算排行
        rankings = []
        for name, data in stats.get('skills', {}).items():
            calls = data.get('calls', 0)
            success = data.get('success', 0)
            fail = data.get('fail', 0)
            success_rate = (success / calls * 100) if calls > 0 else 0
            avg_duration = data.get('avgDuration', 0)
            
            rankings.append({
                'name': name,
                'calls': calls,
                'success': success,
                'fail': fail,
                'successRate': round(success_rate, 1),
                'avgDurationMs': avg_duration
            })
        
        # 按调用次数排序
        rankings.sort(key=lambda x: x['calls'], reverse=True)
        
        return {
            'totalCalls': stats.get('totalCalls', 0),
            'totalSkills': len(stats.get('skills', {})),
            'rankings': rankings,
            'lastUpdated': stats.get('lastUpdated', '')
        }
    
    except Exception as e:
        if Config.ENABLE_LOGGING:
            logger.error(f"获取报告失败：{e}")
        return {'error': str(e)}


def print_report():
    """打印统计报告"""
    report = get_report()
    
    if 'error' in report:
        print(f"❌ 获取报告失败：{report['error']}")
        return
    
    print("📊 技能使用统计报告")
    print("=" * 70)
    print(f"总调用次数：{report['totalCalls']}")
    print(f"技能总数：{report['totalSkills']}")
    print(f"最后更新：{report['lastUpdated']}")
    print()
    print("技能排行榜（按调用次数）：")
    print()
    
    for i, skill in enumerate(report['rankings'][:10], 1):
        medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '📦'
        print(f"{medal} **{i}. {skill['name']}**")
        print(f"   调用：{skill['calls']} | 成功：{skill['success']} | 失败：{skill['fail']} | 成功率：{skill['successRate']}% | 平均耗时：{skill['avgDurationMs']}ms")
    print()


# ============ 配置管理 ============
def configure(
    data_dir: Optional[str] = None,
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
    log_level: Optional[str] = None,
    enable_logging: Optional[bool] = None
):
    """
    配置追踪器
    
    Args:
        data_dir: 数据目录路径
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
        log_level: 日志级别 (DEBUG/INFO/WARNING/ERROR)
        enable_logging: 是否启用日志
    """
    if data_dir:
        Config.DATA_DIR = Path(data_dir)
        Config.STATS_FILE = Config.DATA_DIR / 'skill-stats.json'
        Config.USAGE_LOG = Config.DATA_DIR / 'usage-log.jsonl'
        Config.LOCK_FILE = Config.DATA_DIR / '.stats.lock'
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if max_retries:
        Config.MAX_RETRIES = max_retries
    
    if retry_delay:
        Config.RETRY_DELAY = retry_delay
    
    if log_level:
        Config.LOG_LEVEL = log_level.upper()
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    if enable_logging is not None:
        Config.ENABLE_LOGGING = enable_logging
    
    logger.info(f"配置已更新：data_dir={Config.DATA_DIR}, max_retries={Config.MAX_RETRIES}")


# ============ 命令行 ============
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'test':
            print("测试技能追踪器（生产环境版）...")
            print()
            
            # 测试非阻塞调用
            start = time.time()
            track('test-skill', 'call', {'user': '韩先生'})
            elapsed = time.time() - start
            print(f"✅ 非阻塞调用：{elapsed*1000:.2f}ms")
            
            # 等待后台线程
            time.sleep(0.5)
            
            # 打印报告
            print()
            print_report()
            
            print("✅ 测试完成")
        
        elif command == 'report':
            print_report()
        
        elif command == 'config':
            # 显示当前配置
            print("当前配置：")
            print(f"  DATA_DIR: {Config.DATA_DIR}")
            print(f"  MAX_RETRIES: {Config.MAX_RETRIES}")
            print(f"  RETRY_DELAY: {Config.RETRY_DELAY}s")
            print(f"  LOG_LEVEL: {Config.LOG_LEVEL}")
            print(f"  ENABLE_LOGGING: {Config.ENABLE_LOGGING}")
        
        else:
            print("用法：python skill_tracker.py [test|report|config]")
    else:
        print("用法：python skill_tracker.py [test|report|config]")
        print()
        print("命令:")
        print("  test    - 测试追踪器")
        print("  report  - 显示统计报告")
        print("  config  - 显示当前配置")
