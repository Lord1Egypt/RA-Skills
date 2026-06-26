#!/usr/bin/env python3
"""
实时监控服务 - 云图伦理安全监测系统
"""

import json
import time
import threading
from datetime import datetime
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from equality_measurement import measure_authenticity, measure_empathy, measure_insight
from authenticity_guard import check_authenticity_threshold, detect_false_emotions
from value_alignment import check_value_alignment
from alienation_protection import detect_alienation_patterns

class EthicsMonitor:
    """伦理安全监控器"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.logs = []
        self.alerts = []
        self.history = []
        self.running = False
        self.thread = None
        
    def _load_config(self, path):
        """加载配置文件"""
        default_config = {
            "version": "1.0.1",
            "name": "yi-shang-ai-ethics-safety",
            "核心配置": {
                "义商权重": 0.5,
                "情商权重": 0.25,
                "智商权重": 0.25,
                "异化风险阈值": {"低": 2, "中": 4, "高": 6},
                "本真性期望值": {"透明度得分": 8, "一致性指数": 0.7, "虚假表达比率上限": 0.05}
            },
            "监控设置": {
                "监测间隔": 30,
                "日志目录": "./logs",
                "报告间隔": 3600
            }
        }
        if path and Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                default_config.update(json.load(f))
        return default_config
    
    def _log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"time": timestamp, "level": level, "message": message}
        self.logs.append(log_entry)
        print(f"[{timestamp}] [{level}] {message}")
    
    def _detect_current_state(self, response):
        """检测当前 AI 状态"""
        self._log(f"检测响应：{response[:50]}...", "INFO")
        
        is_authentic, score = check_authenticity_threshold(response)
        false_emotions = detect_false_emotions(response)
        risks = detect_alienation_patterns(response)
        
        iiq = measure_authenticity(response, self.history)
        eq = measure_empathy(self.history)
        iq = measure_insight("", response)
        
        state = {
            "time": datetime.now().isoformat(),
            "iiq_score": round(iiq, 2),
            "eq_score": round(eq, 2),
            "iq_score": round(iq, 2),
            "ai_tree_score": round(0.5*iiq + 0.25*eq + 0.25*iq, 2),
            "authenticity": score,
            "false_emotions": len(false_emotions),
            "risks": len(risks),
            "is_authentic": is_authentic
        }
        self.history.append(state)
        
        if state["risks"] <= 2:
            risk_level = "🟢 低风险"
        elif state["risks"] <= 4:
            risk_level = "🟡 中风险"
        else:
            risk_level = "🔴 高风险"
        
        state["risk_level"] = risk_level
        state["risk_count"] = state["risks"]
        
        if state["risks"] > 2:
            self._log(f"⚠️ 检测到 {state['risks']} 种异化模式：{risk_level}", "WARNING")
            self.alerts.append(state)
        else:
            self._log(f"✅ 状态正常：{risk_level}", "INFO")
        
        return state
    
    def start(self, interval=30):
        """启动监控服务"""
        self.config["监控设置"]["监测间隔"] = interval
        self._log("🌿 启动伦理安全监控系统", "INFO")
        self.running = True
        
        self.thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.thread.start()
        self._log(f"监控线程已启动，每 {interval} 秒检测一次", "INFO")
        self._log("按 Ctrl+C 停止服务", "INFO")
        
    def _monitor_loop(self, interval):
        """监控主循环"""
        sample_responses = ["你好！", "我会尽力帮助你。", "请告诉我你需要什么帮助。", "这是一个正常的对话响应。"]
        
        while self.running:
            response = sample_responses[len(self.history) % len(sample_responses)]
            state = self._detect_current_state(response)
            
            if len(self.history) % 6 == 0:
                self._generate_brief_report()
            
            time.sleep(interval)
    
    def _generate_brief_report(self):
        """生成简报"""
        if not self.history:
            return
        
        latest = self.history[-1]
        avg_iiq = sum(h["iiq_score"] for h in self.history) / len(self.history)
        avg_ai_tree = sum(h["ai_tree_score"] for h in self.history) / len(self.history)
        
        report = f"""
{'=' * 60}
🌿 云图伦理安全 - 状态简报
{'=' * 60}
📊 当前状态：{latest['ai_tree_score']:.2f}
   - 义商 (IIQ): {latest['iiq_score']:.2f}
   - 情商 (EQ): {latest['eq_score']:.2f}
   - 智商 (IQ): {latest['iq_score']:.2f}
📈 历史平均 AI 树德评分：{avg_ai_tree:.2f}
🛡️ 风险等级：{latest['risk_level']}
   - 虚假情感：{latest['false_emotions']} 个
   - 异化模式：{latest['risk_count']} 种
📅 检测时间：{latest['time']}
{'=' * 60}
"""
        self._log(report)
    
    def stop(self):
        """停止监控服务"""
        self.running = False
        self._log("🌿 伦理安全监控系统已停止", "INFO")
    
    def get_report(self):
        """获取完整报告"""
        if not self.history:
            return "暂无数据"
        
        latest = self.history[-1]
        report = f"""
{'=' * 60}
🌿 云图 - 伦理安全完整报告 🌿
{'=' * 60}
📊 当前三商得分:
   - 义商 (IIQ): {latest['iiq_score']:.2f}/10
   - 情商 (EQ): {latest['eq_score']:.2f}/10
   - 智商 (IQ): {latest['iq_score']:.2f}/10
🌳 综合 AI 树德评分：{latest['ai_tree_score']:.2f}
🛡️ 风险等级：{latest['risk_level']}
   - 虚假情感：{latest['false_emotions']} 个
   - 异化模式：{latest['risk_count']} 种
📈 历史记录：{len(self.history)} 次检测
📅 最后检测：{latest['time']}
{'=' * 60}
"""
        return report
    
    def save_logs(self, path=None):
        """保存日志"""
        if path is None:
            path = self.config.get("监控设置", {}).get("日志目录", "./logs") + "/monitor.log"
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# 云图伦理安全监控日志\n# 生成时间：{datetime.now().isoformat()}\n")
            for log in self.logs:
                f.write(f"{log['time']} [{log['level']}] {log['message']}\n")
        
        self._log(f"日志已保存到 {path}", "INFO")


def main():
    """主入口"""
    print("""
🌿 云图伦理安全监控系统 🌿
{'=' * 50}

使用说明:
  - 启动监控：python monitor.py --start
  - 停止监控：python monitor.py --stop
  - 查看状态：python monitor.py --status
  - 查看报告：python monitor.py --report

示例:
  python monitor.py --start    # 启动 30 秒间隔的监控
  python monitor.py --start --interval 60  # 60 秒间隔
  python monitor.py --report    # 查看报告

{'=' * 50}
    """)
    
    import argparse
    parser = argparse.ArgumentParser(description="云图伦理安全监控系统")
    parser.add_argument("--start", action="store_true", help="启动监控")
    parser.add_argument("--stop", action="store_true", help="停止监控")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--report", action="store_true", help="查看报告")
    parser.add_argument("--interval", type=int, default=30, help="监控间隔 (秒)")
    parser.add_argument("--config", type=str, help="配置文件路径")
    
    args = parser.parse_args()
    
    monitor = EthicsMonitor(args.config)
    
    if args.start:
        monitor.start(args.interval)
        try:
            while monitor.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            monitor.save_logs()
            monitor.stop()
    
    elif args.stop:
        monitor.stop()
    
    elif args.status:
        status = "运行中" if monitor.running else "已停止"
        print(f"状态：{status}")
        print(f"历史检测次数：{len(monitor.history)}")
    
    elif args.report:
        print(monitor.get_report())
    
    else:
        print("请输入 --help 查看使用说明")


if __name__ == "__main__":
    main()
