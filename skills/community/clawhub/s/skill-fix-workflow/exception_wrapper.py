# -*- coding: utf-8 -*-
"""
统一异常装饰器 - V3.0

三级异常机制：
- Level 1: 临时错误（网络/超时）→ 自动重试
- Level 2: 资源失效但可替换 → 自动搜索替换 → 汇报用户
- Level 3: 无法修复/无资源 → 停止执行 → 强告警
"""

import logging
import time
from functools import wraps
from typing import Callable, Any, Dict, Optional
from datetime import datetime

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("OpenClaw.ExceptionWrapper")

# 异常配置
MAX_RETRY = 3
RETRY_INTERVAL = 10


class Level1Error(Exception):
    """Level 1: 临时错误，可重试"""
    pass


class Level2Error(Exception):
    """Level 2: 资源失效，可替换"""
    def __init__(self, message: str, original_resource: str = None):
        super().__init__(message)
        self.original_resource = original_resource


class Level3Error(Exception):
    """Level 3: 致命错误，无法修复"""
    pass


def level3_wrapper(task_name: str = "固化任务", log_dir: str = "./task_logs"):
    """
    统一异常装饰器 - 包裹所有拼接的业务代码
    
    用法:
        @level3_wrapper(task_name="新闻监控")
        def run():
            data = skill_search(keyword="AI")
            tool_file_save(data, path="result.csv")
            output(data)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return _execute_with_exception_handling(func, task_name, log_dir, *args, **kwargs)
        return wrapper
    return decorator


def _execute_with_exception_handling(func: Callable, task_name: str, 
                                      log_dir: str, *args, **kwargs) -> Any:
    """执行函数并处理三级异常"""
    
    # 确保日志目录存在
    import os
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}_{task_name}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)
    
    logger.info(f"[{task_name}] 任务开始执行")
    
    # Level 1: 自动重试
    retry_count = 0
    while retry_count < MAX_RETRY:
        try:
            result = func(*args, **kwargs)
            logger.info(f"[{task_name}] 任务执行成功")
            return result
            
        except Level1Error as e:
            retry_count += 1
            logger.warning(f"[{task_name}] [Level 1] 第{retry_count}次重试失败：{str(e)}")
            
            if retry_count == MAX_RETRY:
                logger.error(f"[{task_name}] [Level 1] 重试{MAX_RETRY}次失败，升级至 Level 2")
                return _handle_level2(task_name, str(e), None, log_file)
            
            time.sleep(RETRY_INTERVAL)
            
        except Level2Error as e:
            logger.warning(f"[{task_name}] [Level 2] 资源失效：{str(e)}")
            return _handle_level2(task_name, str(e), e.original_resource, log_file)
            
        except Level3Error as e:
            logger.critical(f"[{task_name}] [Level 3] 致命错误：{str(e)}")
            return _handle_level3(task_name, str(e), log_file)
            
        except Exception as e:
            # 未知错误，尝试判断等级
            error_type = _classify_error(e)
            if error_type == 1:
                retry_count += 1
                if retry_count == MAX_RETRY:
                    return _handle_level2(task_name, f"未知错误重试失败：{str(e)}", None, log_file)
                time.sleep(RETRY_INTERVAL)
            elif error_type == 2:
                return _handle_level2(task_name, str(e), None, log_file)
            else:
                return _handle_level3(task_name, str(e), log_file)
    
    return _handle_level3(task_name, "未知错误，重试耗尽", log_file)


def _classify_error(error: Exception) -> int:
    """
    分类错误等级
    Returns: 1=Level1, 2=Level2, 3=Level3
    """
    # Level 1: 临时错误
    level1_types = (TimeoutError, ConnectionError, ConnectionRefusedError)
    if isinstance(error, level1_types):
        return 1
    
    # Level 2: 资源错误
    level2_types = (FileNotFoundError, KeyError, ValueError, AttributeError)
    if isinstance(error, level2_types):
        return 2
    
    # Level 3: 其他
    return 3


def _handle_level2(task_name: str, error_msg: str, 
                   original_resource: Optional[str], log_file: str) -> Dict:
    """Level 2 处理：搜索替换资源 + 上报用户"""
    
    logger.info(f"[{task_name}] [Level 2] 开始自动搜索替换资源")
    
    # TODO: 对接真实资源搜索
    new_resource = _search_alternative_resource(original_resource)
    
    # 上报用户
    report_msg = f"""
【OpenClaw 任务上报】
任务：{task_name}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
原资源：{original_resource or 'N/A'}
替换资源：{new_resource}
异常：{error_msg}

请确认是否使用替换资源继续执行。
"""
    logger.info(report_msg)
    print(report_msg)
    
    # TODO: 通过 message 工具发送上报
    # message.send(to=user_id, message=report_msg)
    
    return {
        "status": "level2_replaced",
        "original_resource": original_resource,
        "new_resource": new_resource,
        "report": report_msg
    }


def _handle_level3(task_name: str, error_msg: str, log_file: str) -> Dict:
    """Level 3 处理：致命告警，停止执行"""
    
    alarm_msg = f"""
{'='*60}
【OpenClaw 严重告警】
任务：{task_name}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
异常：{error_msg}
结果：无可用替换资源，任务停止
日志：{log_file}
{'='*60}
"""
    logger.critical(alarm_msg)
    print(alarm_msg)
    
    # TODO: 通过 message 工具发送严重告警
    # message.send(to=user_id, message=alarm_msg, priority="high")
    
    return {
        "status": "level3_fatal",
        "error": error_msg,
        "alarm": alarm_msg
    }


def _search_alternative_resource(original: Optional[str]) -> str:
    """搜索替代资源（占位实现）"""
    if not original:
        return "【待实现：自动搜索的替换资源】"
    
    # 简单匹配
    if "kickstarter" in original.lower():
        return "https://www.indiegogo.com"
    elif "api" in original.lower():
        return "https://api.alternative.com"
    else:
        return "【待实现：自动搜索的替换资源】"


# 便捷函数
def raise_level1(msg: str):
    """抛出 Level 1 异常"""
    raise Level1Error(msg)


def raise_level2(msg: str, resource: str = None):
    """抛出 Level 2 异常"""
    raise Level2Error(msg, resource)


def raise_level3(msg: str):
    """抛出 Level 3 异常"""
    raise Level3Error(msg)
