#!/usr/bin/env python3
"""
上下文压缩集成服务
集成监控、压缩和报告功能
"""

import json
import time
import threading
import subprocess
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

class ContextCompactorIntegration:
    """上下文压缩集成服务"""
    
    def __init__(self):
        """初始化"""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.running = True
        
        # 组件路径
        self.components = {
            "monitor": os.path.join(self.script_dir, "monitor.py"),
            "compactor": os.path.join(self.script_dir, "compactor.py"),
            "hierarchical_compactor": os.path.join(self.script_dir, "hierarchical_compactor.py"),
            "config": os.path.join(self.script_dir, "config.json")
        }
        
        # 状态
        self.status = {
            "start_time": datetime.now().isoformat(),
            "components": {},
            "last_compaction": None,
            "total_compactions": 0,
            "total_tokens_saved": 0
        }
        
        # 确保日志目录存在
        self.log_dir = os.path.join(self.script_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 加载配置
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """加载配置"""
        config_path = self.components["config"]
        default_config = {
            "integration": {
                "auto_start_monitor": True,
                "auto_start_compactor": False,
                "check_interval": 60,
                "enable_reporting": True
            },
            "compaction": {
                "auto_trigger_threshold": 0.7,
                "max_compactions_per_hour": 4,
                "enable_smart_compaction": True
            }
        }
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                # 深度合并
                self.deep_merge(default_config, user_config)
        except Exception as e:
            print(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def deep_merge(self, base: Dict, update: Dict):
        """深度合并字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.deep_merge(base[key], value)
            else:
                base[key] = value
    
    def check_component_status(self, component: str) -> Dict:
        """检查组件状态"""
        component_path = self.components.get(component)
        
        if not component_path or not os.path.exists(component_path):
            return {
                "exists": False,
                "runnable": False,
                "error": f"文件不存在: {component_path}"
            }
        
        # 检查是否可执行
        runnable = False
        try:
            if component_path.endswith(".py"):
                # 检查Python文件
                with open(component_path, "r", encoding="utf-8") as f:
                    content = f.read(100)
                    if "python" in content.lower() or "#!/usr/bin/env" in content:
                        runnable = True
            elif component_path.endswith(".sh"):
                # 检查Shell脚本
                runnable = os.access(component_path, os.X_OK)
        except Exception:
            runnable = False
        
        return {
            "exists": True,
            "runnable": runnable,
            "path": component_path,
            "size": os.path.getsize(component_path),
            "modified": datetime.fromtimestamp(os.path.getmtime(component_path)).isoformat()
        }
    
    def start_monitor(self) -> bool:
        """启动监控服务"""
        try:
            monitor_script = os.path.join(self.script_dir, "start_monitor.sh")
            
            if os.path.exists(monitor_script) and os.access(monitor_script, os.X_OK):
                # 使用启动脚本
                result = subprocess.run(
                    [monitor_script],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    cwd=self.script_dir
                )
                
                if result.returncode == 0:
                    print("监控服务启动成功")
                    return True
                else:
                    print(f"监控服务启动失败: {result.stderr}")
                    return False
            else:
                # 直接运行Python脚本
                result = subprocess.run(
                    [sys.executable, self.components["monitor"]],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    cwd=self.script_dir
                )
                
                if result.returncode == 0:
                    print("监控服务启动成功")
                    return True
                else:
                    print(f"监控服务启动失败: {result.stderr}")
                    return False
                    
        except Exception as e:
            print(f"启动监控服务时出错: {e}")
            return False
    
    def trigger_compaction(self, reason: str = "scheduled") -> Optional[Dict]:
        """触发压缩"""
        try:
            print(f"触发压缩，原因: {reason}")
            
            # 使用分层压缩器
            compactor_args = [
                sys.executable, self.components["hierarchical_compactor"],
                "--trigger", reason,
                "--auto"
            ]
            
            result = subprocess.run(
                compactor_args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=self.script_dir
            )
            
            if result.returncode == 0:
                # 解析结果
                try:
                    output_lines = result.stdout.strip().split("\n")
                    for line in output_lines:
                        if line.startswith("{"):
                            compaction_result = json.loads(line)
                            
                            # 更新状态
                            self.status["last_compaction"] = {
                                "timestamp": datetime.now().isoformat(),
                                "reason": reason,
                                "result": compaction_result
                            }
                            self.status["total_compactions"] += 1
                            
                            if "stats" in compaction_result:
                                stats = compaction_result["stats"]
                                self.status["total_tokens_saved"] += stats.get("tokens_saved", 0)
                            
                            print(f"压缩成功: {compaction_result.get('stats', {})}")
                            return compaction_result
                except json.JSONDecodeError:
                    print(f"压缩成功，但无法解析结果: {result.stdout[:100]}...")
                    return {"success": True, "output": result.stdout[:200]}
            else:
                print(f"压缩失败: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"触发压缩时出错: {e}")
            return None
    
    def collect_session_data(self) -> List[Dict]:
        """收集会话数据"""
        try:
            # 尝试从OpenClaw工作区获取数据
            workspace_dir = os.path.expanduser("~/.openclaw/workspace")
            
            data = []
            
            # 检查内存文件
            memory_dir = os.path.join(workspace_dir, "memory")
            if os.path.exists(memory_dir):
                # 获取今天的内存文件
                today = datetime.now().strftime("%Y-%m-%d")
                memory_file = os.path.join(memory_dir, f"{today}.md")
                
                if os.path.exists(memory_file):
                    with open(memory_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 解析为消息
                    lines = content.strip().split("\n")
                    for i, line in enumerate(lines):
                        if line.strip():
                            data.append({
                                "content": line.strip(),
                                "timestamp": datetime.now().isoformat(),
                                "source": "memory_file",
                                "line_number": i + 1
                            })
            
            # 检查AGENTS.md
            agents_file = os.path.join(workspace_dir, "AGENTS.md")
            if os.path.exists(agents_file):
                with open(agents_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 提取最近修改的部分
                lines = content.strip().split("\n")
                recent_lines = lines[-20:]  # 最近20行
                
                for line in recent_lines:
                    if line.strip() and not line.startswith("#"):
                        data.append({
                            "content": line.strip(),
                            "timestamp": datetime.now().isoformat(),
                            "source": "AGENTS.md"
                        })
            
            # 如果没有数据，返回模拟数据
            if not data:
                data = [
                    {
                        "content": "上下文压缩集成服务已启动",
                        "timestamp": datetime.now().isoformat(),
                        "source": "integration"
                    },
                    {
                        "content": "正在收集会话数据进行压缩优化",
                        "timestamp": datetime.now().isoformat(),
                        "source": "integration"
                    }
                ]
            
            return data
            
        except Exception as e:
            print(f"收集会话数据失败: {e}")
            return []
    
    def analyze_context_usage(self) -> Dict:
        """分析上下文使用情况"""
        data = self.collect_session_data()
        
        # 计算基本统计
        total_items = len(data)
        total_chars = sum(len(item["content"]) for item in data)
        
        # 估算token使用（简单估算）
        # 中文字符约1.5 tokens，英文字符约0.25 tokens
        total_tokens = 0
        for item in data:
            content = item["content"]
            chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            english_chars = len(content) - chinese_chars
            total_tokens += chinese_chars * 1.5 + english_chars * 0.25
        
        # 假设最大上下文为8000 tokens
        max_context_tokens = 8000
        token_usage = total_tokens / max_context_tokens
        
        # 分析数据来源
        sources = {}
        for item in data:
            source = item.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_items": total_items,
            "total_chars": total_chars,
            "total_tokens": total_tokens,
            "token_usage": token_usage,
            "max_context_tokens": max_context_tokens,
            "sources": sources,
            "needs_compaction": token_usage > self.config["compaction"]["auto_trigger_threshold"],
            "last_analysis": datetime.now().isoformat()
        }
    
    def generate_report(self) -> Dict:
        """生成报告"""
        # 检查组件状态
        component_status = {}
        for component in self.components:
            component_status[component] = self.check_component_status(component)
        
        # 分析上下文使用
        usage_analysis = self.analyze_context_usage()
        
        # 检查压缩历史
        compaction_db = os.path.join(self.script_dir, "context_compactor.db")
        compaction_history = {}
        
        if os.path.exists(compaction_db):
            try:
                import sqlite3
                conn = sqlite3.connect(compaction_db)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*), 
                           SUM(tokens_before - tokens_after) as total_saved,
                           MAX(timestamp) as last_compaction
                    FROM compaction_history
                ''')
                
                row = cursor.fetchone()
                compaction_history = {
                    "total_compactions": row[0] or 0,
                    "total_tokens_saved": row[1] or 0,
                    "last_compaction": row[2]
                }
                
                conn.close()
            except Exception as e:
                compaction_history = {"error": str(e)}
        
        # 构建报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "integration": {
                "status": "running" if self.running else "stopped",
                "start_time": self.status["start_time"],
                "config": self.config["integration"]
            },
            "components": component_status,
            "context_analysis": usage_analysis,
            "compaction": {
                "history": compaction_history,
                "status": self.status,
                "config": self.config["compaction"]
            },
            "recommendations": []
        }
        
        # 生成建议
        if usage_analysis["needs_compaction"]:
            report["recommendations"].append({
                "type": "compaction",
                "priority": "high",
                "message": f"上下文使用率过高 ({usage_analysis['token_usage']:.2%})，建议立即压缩"
            })
        
        if not component_status["monitor"]["runnable"]:
            report["recommendations"].append({
                "type": "component",
                "priority": "medium",
                "message": "监控服务不可运行，请检查文件权限"
            })
        
        return report
    
    def save_report(self, report: Dict):
        """保存报告"""
        try:
            report_file = os.path.join(self.log_dir, "integration_report.json")
            
            # 读取历史报告
            history = []
            if os.path.exists(report_file):
                with open(report_file, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                        if not isinstance(history, list):
                            history = []
                    except json.JSONDecodeError:
                        history = []
            
            # 添加新报告
            history.append(report)
            
            # 保持最近100个报告
            if len(history) > 100:
                history = history[-100:]
            
            # 保存
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            print(f"报告已保存: {report_file}")
            
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    def integration_loop(self):
        """集成服务主循环"""
        print("=" * 60)
        print("上下文压缩集成服务启动")
        print("=" * 60)
        
        # 检查组件
        print("检查组件状态...")
        for component, path in self.components.items():
            status = self.check_component_status(component)
            status_symbol = "✅" if status["exists"] and status["runnable"] else "❌"
            print(f"  {status_symbol} {component}: {status.get('error', '正常')}")
        
        print()
        
        # 自动启动监控
        if self.config["integration"]["auto_start_monitor"]:
            print("自动启动监控服务...")
            if self.start_monitor():
                print("✅ 监控服务启动成功")
            else:
                print("❌ 监控服务启动失败")
        
        print()
        print("开始集成循环...")
        print(f"检查间隔: {self.config['integration']['check_interval']}秒")
        print("=" * 60)
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 集成循环 #{cycle_count}")
                
                # 分析上下文使用
                print("分析上下文使用情况...")
                usage = self.analyze_context_usage()
                
                print(f"  项目数: {usage['total_items']}")
                print(f"  Token使用率: {usage['token_usage']:.2%}")
                print(f"  需要压缩: {'是' if usage['needs_compaction'] else '否'}")
                
                # 检查是否需要压缩
                if usage["needs_compaction"]:
                    # 检查压缩频率限制
                    last_compaction_time = None
                    if self.status["last_compaction"]:
                        last_compaction_time = datetime.fromisoformat(
                            self.status["last_compaction"]["timestamp"]
                        )
                    
                    should_compact = True
                    if last_compaction_time:
                        time_since_last = (datetime.now() - last_compaction_time).total_seconds()
                        max_per_hour = self.config["compaction"]["max_compactions_per_hour"]
                        min_interval = 3600 / max_per_hour if max_per_hour > 0 else 900
                        
                        if time_since_last < min_interval:
                            print(f"  距离上次压缩仅{time_since_last:.0f}秒，跳过（最小间隔{min_interval:.0f}秒）")
                            should_compact = False
                    
                    if should_compact:
                        print("  触发压缩...")
                        result = self.trigger_compaction("auto_threshold")
                        if result:
                            print(f"  压缩完成，节省Token: {result.get('stats', {}).get('tokens_saved', 0)}")
                
                # 定期生成报告
                if cycle_count % 5 == 0:  # 每5个循环生成一次报告
                    print("生成集成报告...")
                    report = self.generate_report()
                    
                    if self.config["integration"]["enable_reporting"]:
                        self.save_report(report)
                        print("  报告已保存")
                    
                    # 显示摘要
                    print(f"  总压缩次数: {report['compaction']['history'].get('total_compactions', 0)}")
                    print(f"  总节省Token: {report['compaction']['history'].get('total_tokens_saved', 0)}")
                
                # 等待下一次检查
                print(f"等待{self.config['integration']['check_interval']}秒...")
                time.sleep(self.config["integration"]["check_interval"])
                
            except KeyboardInterrupt:
                print("\n收到中断信号")
                self.running = False
                break
                
            except Exception as e:
                print(f"集成循环出错: {e}")
                time.sleep(10)  # 出错后等待10秒
        
        # 服务停止
        print("\n" + "=" * 60)
        print("上下文压缩集成服务停止")
        
        # 生成最终报告
        final_report = self.generate