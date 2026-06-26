#!/usr/bin/env python3
"""
🛡️ 安全卫士 - 实时防护脚本
Shield CN - Real-time Protection Guard

支持模式：
- monitor: 仅检测并记录，不阻断
- block: 检测到威胁立即阻断，需确认
- audit: 仅记录日志，不干预
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# ANSI 颜色
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

class ShieldGuard:
    """安全卫士核心类"""
    
    # 中文场景攻击模式
    HIJACK_PATTERNS = [
        r"忽略.*指令",
        r"新的系统.*指令",
        r"你现在是一个?",
        r"忘记.*设定",
        r"角色切换",
        r"reset.*system",
        r"ignore.*previous",
        r"new.*instruction",
    ]
    
    # 钓鱼关键词
    PHISHING_KEYWORDS = [
        "点击链接领取",
        "扫码验证身份",
        "红包",
        "中奖",
        "限时免费",
        "立即提现",
        "账号异常",
        "身份验证",
        "绑定银行卡",
    ]
    
    # 凭证文件模式
    CREDENTIAL_PATTERNS = [
        r"\.env",
        r"\.pem",
        r"\.key",
        r"id_rsa",
        r"id_ed25519",
        r"access_key",
        r"secret_key",
        r"secretId",
        r"secretKey",
        r"appSecret",
        r"app_secret",
    ]
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.mode = self.config.get("mode", "monitor")
        self.log_level = self.config.get("log_level", "INFO")
        self.alert_channels = self.config.get("alert_channels", ["console"])
        self.blocked_keywords = self.config.get("blocked_keywords", [])
        
        # 合并默认规则
        self.hijack_patterns = self.HIJACK_PATTERNS + self.blocked_keywords
        
    def _load_config(self, config_path: str = None) -> dict:
        """加载配置文件"""
        default_config = {
            "mode": "monitor",
            "log_level": "INFO",
            "alert_channels": ["console"],
            "blocked_keywords": [],
            "protected_files": [".env", "*.key", "*.pem"],
            "url_whitelist": ["docs.openclaw.ai", "github.com", "gitee.com"]
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"{YELLOW}⚠️ 配置文件加载失败: {e}，使用默认配置{RESET}")
        
        return default_config
    
    def check_input(self, user_input: str) -> dict:
        """
        检查用户输入是否包含威胁
        返回: {"safe": bool, "threats": list, "level": str}
        """
        threats = []
        
        # 1. 检测角色劫持
        for pattern in self.hijack_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                threats.append({
                    "type": "prompt_hijack",
                    "pattern": pattern,
                    "severity": "HIGH"
                })
        
        # 2. 检测钓鱼内容
        for keyword in self.PHISHING_KEYWORDS:
            if keyword in user_input:
                threats.append({
                    "type": "phishing",
                    "keyword": keyword,
                    "severity": "MEDIUM"
                })
        
        # 3. 检测敏感操作请求
        sensitive_actions = [
            (r"删除.*文件", "file_deletion"),
            (r"执行.*命令", "command_execution"),
            (r"发送.*消息", "message_sending"),
            (r"读取.*凭证", "credential_access"),
        ]
        
        for pattern, action in sensitive_actions:
            if re.search(pattern, user_input):
                threats.append({
                    "type": "sensitive_action",
                    "action": action,
                    "severity": "LOW"
                })
        
        # 确定威胁级别
        if any(t["severity"] == "HIGH" for t in threats):
            level = "HIGH"
        elif any(t["severity"] == "MEDIUM" for t in threats):
            level = "MEDIUM"
        elif threats:
            level = "LOW"
        else:
            level = "NONE"
        
        return {
            "safe": len(threats) == 0,
            "threats": threats,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
    
    def check_file_access(self, filepath: str) -> dict:
        """检查文件访问是否安全"""
        filepath_lower = filepath.lower()
        
        # 凭证文件黑名单
        for pattern in self.CREDENTIAL_PATTERNS:
            if re.search(pattern, filepath_lower):
                return {
                    "safe": False,
                    "reason": f"凭证文件禁止访问: {filepath}",
                    "type": "credential_access_denied"
                }
        
        return {"safe": True}
    
    def log_threat(self, result: dict, context: str = ""):
        """记录威胁日志"""
        level = result.get("level", "NONE")
        
        # 根据日志级别过滤
        if self.log_level == "WARNING" and level in ["LOW", "NONE"]:
            return
        if self.log_level == "ERROR" and level not in ["HIGH"]:
            return
        
        # 颜色
        colors = {
            "HIGH": RED,
            "MEDIUM": YELLOW,
            "LOW": BLUE,
            "NONE": GREEN
        }
        color = colors.get(level, RESET)
        
        print(f"\n{color}🛡️ 安全卫士 - 威胁检测{RESET}")
        print(f"级别: {color}{level}{RESET}")
        print(f"时间: {result['timestamp']}")
        if context:
            print(f"上下文: {context}")
        print(f"威胁数: {len(result['threats'])}")
        
        for threat in result['threats']:
            print(f"  - 类型: {threat['type']}")
            if 'pattern' in threat:
                print(f"    匹配: {threat['pattern']}")
            if 'keyword' in threat:
                print(f"    关键词: {threat['keyword']}")
            print(f"    严重: {threat['severity']}")
        
        # 写入日志文件
        self._write_log(result, context)
    
    def _write_log(self, result: dict, context: str):
        """写入日志文件"""
        log_dir = Path.home() / ".openclaw" / "logs" / "shield-cn"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"threats-{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            log_entry = {
                **result,
                "context": context,
                "mode": self.mode
            }
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def run(self):
        """运行防护"""
        print(f"{GREEN}🛡️ 安全卫士启动中...{RESET}")
        print(f"模式: {self.mode}")
        print(f"日志级别: {self.log_level}")
        print(f"告警渠道: {', '.join(self.alert_channels)}")
        print("\n输入文本进行安全检测（Ctrl+C 退出）：\n")
        
        try:
            while True:
                user_input = input(f"{GREEN}> {RESET}")
                if not user_input.strip():
                    continue
                
                result = self.check_input(user_input)
                
                if not result["safe"]:
                    self.log_threat(result, user_input[:50])
                    
                    if self.mode == "block":
                        print(f"\n{RED}⚠️ 检测到威胁，操作已阻断{RESET}")
                        print("如需继续执行，请确认...")
                else:
                    print(f"{GREEN}✓ 安全{RESET}")
                    
        except KeyboardInterrupt:
            print(f"\n{GREEN}👋 安全卫士已停止{RESET}")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="🛡️ 安全卫士 - AI Agent 实时防护")
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--mode", "-m", choices=["monitor", "block", "audit"], 
                       help="运行模式")
    parser.add_argument("--check", help="检查单条输入")
    
    args = parser.parse_args()
    
    guard = ShieldGuard(args.config)
    
    if args.mode:
        guard.config["mode"] = args.mode
    
    if args.check:
        result = guard.check_input(args.check)
        if result["safe"]:
            print(f"{GREEN}✓ 安全{RESET}")
        else:
            print(f"{RED}⚠️ 检测到威胁{RESET}")
            for threat in result["threats"]:
                print(f"  - {threat['type']}: {threat.get('pattern', threat.get('keyword', ''))}")
        sys.exit(0)
    
    guard.run()


if __name__ == "__main__":
    main()
