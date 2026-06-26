#!/usr/bin/env python3
"""
上下文压缩监控服务
实时监控会话上下文使用情况，基于内存使用触发压缩
"""

import json
import time
import threading
import sqlite3
from datetime import datetime
import os
import sys
import signal

class ContextMonitor:
    """上下文监控服务"""
    
    def __init__(self, compactor_path: str = None):
        """初始化监控服务"""
        self.running = True
        self.compactor_path = compactor_path or os.path.join(
            os.path.dirname(__file__), "compactor.py"
        )
        
        # 监控配置
        self.config = {
            "check_interval": 30,  # 检查间隔（秒）
            "token_usage_threshold": 0.7,  # token使用阈值
            "message_count_threshold": 50,  # 消息数量阈值
            "max_history_size": 1000,  # 最大历史记录
            "enable_auto_compaction": True,  # 启用自动压缩
            "enable_logging": True,  # 启用日志
            "log_file": "logs/monitor.log"  # 日志文件
        }
        
        # 状态跟踪
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "total_checks": 0,
            "total_compactions_triggered": 0,
            "last_check_time": None,
            "last_compaction_time": None,
            "current_token_usage": 0,
            "current_message_count": 0
        }
        
        # 会话历史
        self.session_history = []
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.config["log_file"]), exist_ok=True)
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """信号处理"""
        self.log(f"收到信号 {signum}，正在关闭...")
        self.running = False
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        if not self.config["enable_logging"]:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        try:
            with open(self.config["log_file"], "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"日志写入失败: {e}")
        
        # 控制台输出
        if level in ["ERROR", "WARNING"]:
            print(log_entry)
    
    def estimate_token_usage(self, messages: list) -> float:
        """估算token使用率"""
        if not messages:
            return 0.0
        
        # 简单估算：每个中文字符约1.5个token，每个英文字符约0.25个token
        total_tokens = 0
        for msg in messages:
            content = str(msg.get("content", ""))
            chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            english_chars = len(content) - chinese_chars
            total_tokens += chinese_chars * 1.5 + english_chars * 0.25
        
        # 假设最大上下文为8000 tokens
        max_context_tokens = 8000
        usage = total_tokens / max_context_tokens
        
        return min(usage, 1.0)  # 限制在0-1之间
    
    def collect_session_data(self):
        """收集会话数据"""
        # 这里需要根据实际环境获取会话数据
        # 暂时使用模拟数据
        try:
            # 尝试从OpenClaw会话获取数据
            workspace_dir = os.path.expanduser("~/.openclaw/workspace")
            
            # 检查内存目录
            memory_dir = os.path.join(workspace_dir, "memory")
            if os.path.exists(memory_dir):
                # 获取最新的内存文件
                memory_files = sorted([f for f in os.listdir(memory_dir) if f.endswith(".md")])
                if memory_files:
                    latest_file = os.path.join(memory_dir, memory_files[-1])
                    with open(latest_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 解析内容为消息
                    lines = content.strip().split("\n")
                    messages = []
                    for line in lines:
                        if line.strip():
                            messages.append({
                                "content": line.strip(),
                                "timestamp": datetime.now().isoformat(),
                                "source": "memory_file"
                            })
                    
                    return messages
            
            # 如果没有找到内存文件，返回模拟数据
            return [
                {"content": "会话监控已启动", "timestamp": datetime.now().isoformat(), "source": "monitor"},
                {"content": "正在收集上下文使用数据", "timestamp": datetime.now().isoformat(), "source": "monitor"},
                {"content": "准备进行压缩优化", "timestamp": datetime.now().isoformat(), "source": "monitor"}
            ]
            
        except Exception as e:
            self.log(f"收集会话数据失败: {e}", "ERROR")
            return []
    
    def check_compaction_needed(self, token_usage: float, message_count: int) -> bool:
        """检查是否需要压缩"""
        # 检查token使用
        if token_usage >= self.config["token_usage_threshold"]:
            self.log(f"Token使用率过高: {token_usage:.2%} >= {self.config['token_usage_threshold']:.2%}")
            return True
        
        # 检查消息数量
        if message_count >= self.config["message_count_threshold"]:
            self.log(f"消息数量过多: {message_count} >= {self.config['message_count_threshold']}")
            return True
        
        # 检查时间间隔
        if self.stats["last_compaction_time"]:
            time_since_last = time.time() - self.stats["last_compaction_time"]
            if time_since_last > 3600:  # 1小时
                self.log(f"距离上次压缩已超过1小时: {time_since_last:.0f}秒")
                return True
        
        return False
    
    def trigger_compaction(self, token_usage: float, message_count: int):
        """触发压缩"""
        try:
            self.log(f"触发压缩: token_usage={token_usage:.2%}, messages={message_count}")
            
            # 调用压缩代理
            import subprocess
            import sys
            
            # 构建压缩参数
            compactor_args = [
                sys.executable, self.compactor_path,
                "--token-usage", str(token_usage),
                "--message-count", str(message_count),
                "--auto-trigger"
            ]
            
            # 执行压缩
            result = subprocess.run(
                compactor_args,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            if result.returncode == 0:
                self.log(f"压缩成功: {result.stdout[:100]}...")
                self.stats["total_compactions_triggered"] += 1
                self.stats["last_compaction_time"] = time.time()
            else:
                self.log(f"压缩失败: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log(f"触发压缩时出错: {e}", "ERROR")
    
    def monitor_loop(self):
        """监控循环"""
        self.log("上下文监控服务启动")
        self.log(f"配置: {json.dumps(self.config, indent=2, ensure_ascii=False)}")
        
        while self.running:
            try:
                # 收集数据
                messages = self.collect_session_data()
                message_count = len(messages)
                token_usage = self.estimate_token_usage(messages)
                
                # 更新状态
                self.stats["total_checks"] += 1
                self.stats["last_check_time"] = time.time()
                self.stats["current_token_usage"] = token_usage
                self.stats["current_message_count"] = message_count
                
                # 记录会话历史
                self.session_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "token_usage": token_usage,
                    "message_count": message_count
                })
                
                # 保持历史记录大小
                if len(self.session_history) > self.config["max_history_size"]:
                    self.session_history = self.session_history[-self.config["max_history_size"]:]
                
                # 检查是否需要压缩
                if self.config["enable_auto_compaction"]:
                    if self.check_compaction_needed(token_usage, message_count):
                        self.trigger_compaction(token_usage, message_count)
                
                # 定期报告状态
                if self.stats["total_checks"] % 10 == 0:  # 每10次检查报告一次
                    self.report_status()
                
                # 等待下一次检查
                time.sleep(self.config["check_interval"])
                
            except Exception as e:
                self.log(f"监控循环出错: {e}", "ERROR")
                time.sleep(5)  # 出错后等待5秒
    
    def report_status(self):
        """报告状态"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "current_usage": {
                "token_usage": self.stats["current_token_usage"],
                "message_count": self.stats["current_message_count"]
            },
            "config": self.config
        }
        
        self.log(f"状态报告: {json.dumps(status, ensure_ascii=False)}")
        
        # 保存状态到文件
        status_file = os.path.join(os.path.dirname(__file__), "status.json")
        try:
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"保存状态文件失败: {e}", "ERROR")
    
    def get_detailed_report(self) -> dict:
        """获取详细报告"""
        return {
            "monitor": {
                "config": self.config,
                "stats": self.stats,
                "session_history_size": len(self.session_history),
                "running": self.running
            },
            "current_session": {
                "token_usage": self.stats["current_token_usage"],
                "message_count": self.stats["current_message_count"],
                "estimated_tokens": self.stats["current_token_usage"] * 8000
            },
            "compaction_history": {
                "total_triggered": self.stats["total_compactions_triggered"],
                "last_compaction": self.stats["last_compaction_time"]
            }
        }

def main():
    """主函数"""
    print("=" * 60)
    print("上下文压缩监控服务")
    print("=" * 60)
    
    # 创建监控实例
    monitor = ContextMonitor()
    
    # 启动监控
    try:
        monitor_thread = threading.Thread(target=monitor.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("监控服务已启动，按 Ctrl+C 停止")
        print(f"检查间隔: {monitor.config['check_interval']}秒")
        print(f"Token阈值: {monitor.config['token_usage_threshold']:.2%}")
        print(f"消息阈值: {monitor.config['message_count_threshold']}")
        print("=" * 60)
        
        # 保持主线程运行
        while monitor.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n收到中断信号，正在关闭...")
        monitor.running = False
        monitor_thread.join(timeout=5)
        
        # 生成最终报告
        report = monitor.get_detailed_report()
        print(f"\n最终报告: {json.dumps(report, indent=2, ensure_ascii=False)}")
        
        print("监控服务已停止")

if __name__ == "__main__":
    main()