#!/usr/bin/env python3
"""
Xtoys.app Webhook 控制器 v1.1.0
用于通过 webhook API 远程控制设备

改进点：
- 修复 "estim" 前导空格问题
- 增加环境变量支持
- 改进错误处理和日志
- 支持连接池复用
"""

import requests
import argparse
import json
import os
import sys
import logging
from typing import Optional, List
from urllib.parse import urljoin, urlencode


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XtoysController:
    """xtoys.app webhook 控制器"""
    
    BASE_URL = "https://webhook.xtoys.app"
    
    # 身体部位列表（可被单独控制）
    BODY_PARTS = [
        "left_nipple",   # 左边乳头
        "right_nipple",  # 右边乳头
        "both_nipples",  # 两边乳头
        "left_breast",   # 左边乳房
        "right_breast",  # 右边乳房
        "both_breasts",  # 两边乳房
        "clitoris",      # 阴蒂
        "vagina",        # 阴道
        "anus",          # 后庭
    ]
    
    # 所有支持的 action（包括特殊指令）
    COMMON_ACTIONS = BODY_PARTS + ["stop", "pause"]
    
    def __init__(self, webhook_id: Optional[str] = None, session: Optional[requests.Session] = None):
        """
        初始化控制器
        
        Args:
            webhook_id: Webhook ID，如果为 None 则尝试从配置文件或环境变量读取
            session: 可选的 requests Session 对象（用于连接池复用）
        """
        self.webhook_id = webhook_id or self._load_webhook_id()
        if not self.webhook_id:
            raise ValueError(
                "未提供 webhook_id。请通过以下方式设置：\n"
                "1. 传入参数 webhook_id\n"
                "2. 设置环境变量 XTOYS_WEBHOOK_ID\n"
                "3. 在 config.json 中配置 webhook_id"
            )
        
        # 使用连接池复用
        self.session = session or requests.Session()
        
        # 配置重试适配器
        from urllib3.util.retry import Retry
        from requests.adapters import HTTPAdapter
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 记录当前正在刺激的部位（xtoys 一次只能操作一个地方）
        self._current_part: Optional[str] = None
        
        logger.debug(f"XtoysController 初始化完成")
    
    def _load_webhook_id(self) -> Optional[str]:
        """
        加载 webhook_id，优先级：
        1. 环境变量 XTOYS_WEBHOOK_ID
        2. 配置文件 config.json
        """
        # 1. 检查环境变量
        env_webhook_id = os.environ.get("XTOYS_WEBHOOK_ID")
        if env_webhook_id:
            logger.debug("从环境变量加载 webhook_id")
            return env_webhook_id
        
        # 2. 检查配置文件
        config_webhook_id = self._load_config()
        if config_webhook_id:
            logger.debug("从配置文件加载 webhook_id")
            return config_webhook_id
        
        return None
    
    def _load_config(self) -> Optional[str]:
        """从配置文件加载 webhook_id"""
        # 尝试多个可能的配置文件路径
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "config.json"),
            os.path.join(os.path.dirname(__file__), "config.json"),
            os.path.expanduser("~/.config/xtoys/config.json"),
            "/etc/xtoys/config.json",
        ]
        
        for config_path in possible_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        config = json.load(f)
                        webhook_id = config.get("webhook_id")
                        if webhook_id:
                            logger.debug(f"从 {config_path} 加载配置")
                            return webhook_id
                except json.JSONDecodeError as e:
                    logger.warning(f"配置文件 {config_path} JSON 格式错误: {e}")
                except IOError as e:
                    logger.warning(f"读取配置文件 {config_path} 失败: {e}")
        
        return None
    
    def send_command(self, action: str, level: int = 50) -> bool:
        """
        发送控制命令
        
        Args:
            action: 身体部位/动作
            level: 强度 (0-100)
        
        Returns:
            是否成功
        """
        # 验证参数
        if not isinstance(level, (int, float)):
            logger.error(f"level 必须是数字，当前类型: {type(level)}")
            return False
        
        level = int(level)
        if not 0 <= level <= 100:
            logger.warning(f"level {level} 超出范围 0-100，已调整为 {max(0, min(100, level))}")
            level = max(0, min(100, level))
        
        # 验证 action
        action = action.strip().lower()
        if not action:
            logger.error("action 不能为空")
            return False
        
        # 处理特殊指令：stop 和 pause 会停止当前正在刺激的部位
        if action in ("stop", "pause"):
            if self._current_part:
                logger.info(f"接收到 {action} 指令，停止当前部位: {self._current_part}")
                result = self._send_raw_command(self._current_part, 0)
                if result:
                    self._current_part = None
                return result
            else:
                logger.info(f"接收到 {action} 指令，但当前没有正在刺激的部位")
                return True
        
        # 如果要切换到新部位，先停止之前的部位（xtoys 一次只能操作一个地方）
        if action in self.BODY_PARTS:
            if self._current_part and self._current_part != action and level > 0:
                logger.info(f"切换部位: 先停止 {self._current_part}")
                self._send_raw_command(self._current_part, 0)
        
        # 发送实际命令
        result = self._send_raw_command(action, level)
        if result and level > 0:
            self._current_part = action
        elif result and level == 0:
            self._current_part = None
        return result
    
    def _send_raw_command(self, action: str, level: int) -> bool:
        """
        发送原始控制命令（内部方法，不处理状态逻辑）
        
        Args:
            action: 身体部位/动作
            level: 强度 (0-100)
        
        Returns:
            是否成功
        """
        # 构建 URL（使用 urllib 避免注入）
        base_url = self.BASE_URL.rstrip('/')
        webhook_id = self.webhook_id.strip('/')
        url = f"{base_url}/{webhook_id}"
        
        params = {
            "action": action,
            "level": level
        }
        
        logger.info(f"发送命令: {action} -> level {level}")
        
        try:
            response = self.session.get(
                url, 
                params=params, 
                timeout=(5, 10)  # (连接超时, 读取超时)
            )
            
            # 接受 2xx 状态码为成功
            if 200 <= response.status_code < 300:
                logger.info(f"✓ 成功: {action} -> level {level}")
                return True
            else:
                logger.error(f"✗ 失败: HTTP {response.status_code}")
                logger.debug(f"响应内容: {response.text[:500]}")
                return False
                
        except requests.exceptions.Timeout as e:
            logger.error(f"✗ 请求超时: {e}")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"✗ 连接错误: {e}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ 请求错误: {e}")
            return False
    
    def send_batch(self, commands: List[dict]) -> List[bool]:
        """
        批量发送命令
        
        Args:
            commands: 命令列表，每个命令是 {"action": str, "level": int} 的字典
        
        Returns:
            每个命令的成功状态列表
        """
        results = []
        for cmd in commands:
            action = cmd.get("action", "")
            level = cmd.get("level", 50)
            result = self.send_command(action, level)
            results.append(result)
        return results
    
    def stop(self) -> bool:
        """停止当前正在刺激的部位"""
        if self._current_part:
            logger.info(f"停止当前部位: {self._current_part}")
            result = self._send_raw_command(self._current_part, 0)
            if result:
                self._current_part = None
            return result
        else:
            logger.info("当前没有正在刺激的部位")
            return True
    
    def stop_all(self) -> bool:
        """停止当前正在刺激的部位（兼容旧接口）"""
        return self.stop()
    
    def pause(self) -> bool:
        """暂停当前正在刺激的部位（同 stop）"""
        return self.stop()
    
    def pause_all(self) -> bool:
        """暂停当前正在刺激的部位（兼容旧接口）"""
        return self.stop()
    
    def list_actions(self):
        """列出常见 action"""
        print("支持的常见 action：")
        for action in self.COMMON_ACTIONS:
            print(f"  - {action}")
        print("\n注意: 实际支持的 action 取决于你的设备配置")
    
    def test_connection(self) -> bool:
        """测试连接是否可用"""
        try:
            # 发送一个测试命令（左边乳头 level=0）来验证连接
            return self.send_command("left_nipple", 0)
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False
    
    def close(self):
        """关闭 session，释放连接池"""
        if self.session:
            self.session.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Xtoys.app Webhook 控制器 v1.1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
配置方式（优先级从高到低）：
  1. 命令行参数 --webhook-id
  2. 环境变量 XTOYS_WEBHOOK_ID
  3. 配置文件 config.json

示例:
  # 控制左边乳头
  %(prog)s --action left_nipple --level 50
  
  # 控制阴蒂
  %(prog)s --action clitoris --level 80
  
  # 停止当前部位
  %(prog)s --action stop
  %(prog)s --stop
  
  # 列出支持的 action
  %(prog)s --list
  
  # 测试连接
  %(prog)s --test
  
  # 使用环境变量
  XTOYS_WEBHOOK_ID=xxx %(prog)s --action left_nipple --level 50

环境变量:
  XTOYS_WEBHOOK_ID    设置 webhook ID
  XTOYS_LOG_LEVEL     设置日志级别 (DEBUG/INFO/WARNING/ERROR)
        """
    )
    
    parser.add_argument(
        "--action", "-a",
        help="身体部位/动作 (如: left_nipple, clitoris, stop)"
    )
    parser.add_argument(
        "--level", "-l",
        type=int,
        default=50,
        help="强度 0-100 (默认: 50)"
    )
    parser.add_argument(
        "--webhook-id", "-w",
        help="Webhook ID (如果不提供则使用环境变量或 config.json)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出支持的 action 列表"
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="停止当前正在刺激的部位 (等同于 --action stop)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试连接是否可用"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细日志"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose or os.environ.get("XTOYS_LOG_LEVEL") == "DEBUG":
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 初始化控制器
    try:
        controller = XtoysController(args.webhook_id)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 处理命令
    with controller:
        if args.list:
            controller.list_actions()
        elif args.test:
            if controller.test_connection():
                print("✓ 连接测试成功")
            else:
                print("✗ 连接测试失败")
                sys.exit(1)
        elif args.stop:
            if not controller.stop_all():
                sys.exit(1)
        elif args.action:
            if not controller.send_command(args.action, args.level):
                sys.exit(1)
        else:
            parser.print_help()
            print("\n错误: 请指定 --action 或使用 --list/--stop/--test")
            sys.exit(1)


if __name__ == "__main__":
    main()
