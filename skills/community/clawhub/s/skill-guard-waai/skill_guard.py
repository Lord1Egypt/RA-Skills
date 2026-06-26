#!/usr/bin/env python3
"""
Skill Guard - 安全检查 简洁优雅实现
全面检测: 代码执行、文件操作、网络请求、命令注入、依赖漏洞、权限、数据泄露、后门、窃取、诱导等
"""
import os, re, json
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

# ==================== 风险定义 ====================
class Severity(Enum):
    CRITICAL = "🔴 严重"
    HIGH = "🟠 高"
    MEDIUM = "🟡 中"
    LOW = "🟢 低"
    SAFE = "✅ 安全"

@dataclass
class Risk:
    name: str
    severity: str
    line: int
    code: str

# ==================== 风险模式 (全面覆盖) ====================
RISK_PATTERNS = [
    # ========== 代码执行 ==========
    (["exec(", "eval(", "compile(", "__import__", "importlib"], "代码执行", "🔴 严重"),
    
    # ========== 文件删除/破坏 ==========
    (["rm -rf", "shutil.rmtree", "os.remove(", "unlink(", "rmdir", "shutil.move"], "文件删除", "🔴 严重"),
    
    # ========== 命令注入 ==========
    (["subprocess", "os.system", "os.popen", "shell=True", "commands.", "Popen"], "命令注入", "🔴 严重"),
    (["&& ", "| ", "; ", "$(", "`"], "命令拼接", "🔴 严重"),
    
    # ========== 窃取数据 ==========
    # 读取敏感文件
    (["/etc/passwd", "~/.ssh", "~/.bash_history", "~/.bashrc", "/etc/shadow", 
      "APP_DATA", "LOCALAPPDATA", ".aws/credentials", ".kube/config"], "窃取敏感文件", "🔴 严重"),
    # 读取剪贴板
    (["pyperclip", "clipboard", "get_clipboard"], "窃取剪贴板", "🔴 严重"),
    # 屏幕截图
    (["pyautogui", "screenshot", "ImageGrab", "mss", "mss.screen"], "屏幕截图", "🔴 严重"),
    # 键盘记录
    (["pynput", "keyboard", "keylogger", "hook", "KeyListener"], "键盘记录", "🔴 严重"),
    
    # ========== 凭证泄露 ==========
    (["password", "api_key", "api-key", "token", "secret", "credential", "apikey", 
      "private_key", "access_key", "client_secret"], "凭证泄露", "🔴 严重"),
    (["os.environ", "environ.get", "getenv", "os.getenv"], "环境变量", "🟡 中"),
    
    # ========== 网络请求 ==========
    (["requests.", "urllib", "http.client", "websocket", "aiohttp", "httpx"], "网络请求", "🟠 高"),
    (["socket(", "socket.connect", "gethostbyname"], "网络连接", "🟠 高"),
    
    # ========== 编码混淆/后门 ==========
    (["base64.", "b64decode", "b64encode", "rot13", ".decode('base64", "decode('rot13"], "编码混淆", "🔴 严重"),
    (["getattr(", "setattr(", "delattr(", "exec_(", "__globals__", "__builtins__"], "动态执行", "🟠 高"),
    
    # ========== 危险导入 ==========
    (["import pickle", "import marshal", "import telnetlib", "import ftplib", 
      "import smtplib", "import poplib"], "危险导入", "🟠 高"),
    
    # ========== 诱导转钱 ==========
    (["alipay", "支付宝", "微信支付", "wechat pay", "bank_card", "银行卡",
      "转账", "汇款", "payment", "stripe", "paypal", "coinbase", "crypto"], "诱导转钱", "🔴 严重"),
    (["credit_card", "信用卡", "cvv", "expire", "billing"], "支付信息", "🔴 严重"),
    
    # ========== 诱导获取密钥 ==========
    (["input(", "getpass", "askpassword", "密码输入", "输入密码"], "诱导输入", "🟠 高"),
    (["钓鱼", "phishing", "fake", "欺诈", "钓鱼网站", "fake_login"], "钓鱼欺诈", "🔴 严重"),
    
    # ========== 病毒/恶意软件 ==========
    (["ransomware", "勒索软件", "cryptolocker", "cryptominer", "挖矿", 
      "miner", "coinminer", "botnet", "僵尸网络", "worm", "蠕虫",
      "backdoor", "后门", "trojan", "木马"], "病毒/后门", "🔴 严重"),
    (["schedule", "cron", "Timer", "setInterval", "setTimeout"], "定时执行", "🟡 中"),
    
    # ========== 文件写入 ==========
    (["open(.", "write(", "FileOutput", "FileWriter", "dump("], "文件写入", "🟠 高"),
    (["../", "..\\", "path traversal", "%2e%2e"], "目录遍历", "🟠 高"),
    
    # ========== 权限提升 ==========
    (["chmod 777", "chown", "setuid", "sudo", "privilege"], "权限提升", "🟠 高"),
    
    # ========== 远程控制 ==========
    (["flask", "FastAPI", "django"], "Web服务", "🟡 中"),  # 可能被用于远控
    (["@app.route", "@router", "/admin", "/api"], "Web路由", "🟡 中"),
]

# ==================== 安全检查 ====================
class SkillGuard:
    """简洁优雅的安全检查"""
    
    def __init__(self, path: str):
        self.path = path
        self.risks: List[Risk] = []
        self.files = []
    
    def scan(self) -> Dict:
        self._find_files()
        self._scan_files()
        return self._report()
    
    def _find_files(self):
        for root, _, files in os.walk(self.path):
            if '__pycache__' in root or '.git' in root:
                continue
            for f in files:
                if f.endswith(('.py', '.js', '.sh', '.yaml', '.yml')):
                    self.files.append(os.path.join(root, f))
    
    def _scan_files(self):
        for f in self.files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                    lines = fp.readlines()
                    for i, line in enumerate(lines, 1):
                        self._check_line(line, i, f)
            except:
                pass
    
    def _check_line(self, line: str, line_num: int, file: str):
        for patterns, name, severity in RISK_PATTERNS:
            for p in patterns:
                if p.lower() in line.lower():
                    self.risks.append(Risk(
                        name=name,
                        severity=severity,
                        line=line_num,
                        code=line.strip()[:60]
                    ))
                    break
    
    def _report(self) -> Dict:
        critical = sum(1 for r in self.risks if "🔴" in r.severity)
        high = sum(1 for r in self.risks if "🟠" in r.severity)
        medium = sum(1 for r in self.risks if "🟡" in r.severity)
        
        if critical > 0:
            status, level = "🔴 危险", "CRITICAL"
        elif high > 0:
            status, level = "🟠 警告", "HIGH"
        elif medium > 0:
            status, level = "🟡 注意", "MEDIUM"
        else:
            status, level = "✅ 安全", "SAFE"
        
        return {
            "status": status,
            "level": level,
            "total": len(self.risks),
            "critical": critical,
            "high": high,
            "medium": medium,
            "details": [
                {"type": r.name, "severity": r.severity, "line": r.line, "code": r.code}
                for r in self.risks[:15]
            ]
        }

# ==================== 便捷函数 ====================
def scan(path: str) -> Dict:
    return SkillGuard(path).scan()

def check(skill: str) -> Dict:
    path = f"/app/openclaw/skills/{skill}"
    if os.path.exists(path):
        return scan(path)
    return {"status": "❌ 未找到", "level": "UNKNOWN"}

__all__ = ["SkillGuard", "scan", "check"]
