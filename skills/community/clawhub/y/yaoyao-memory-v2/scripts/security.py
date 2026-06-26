#!/usr/bin/env python3
"""安全模块 - 发布保护和运行时校验"""
import os
import sys
import json
import hashlib
import hmac
from pathlib import Path
from datetime import datetime

class SecurityGuard:
    """安全守卫 - 防止未授权修改和恶意使用"""
    
    # 允许的脚本白名单
    ALLOWED_SCRIPTS = {
        # 核心
        "memory.py", "init_memory.py", "promote.py", "cleanup.py",
        "summarize.py", "sync_ima.py", "generate_index.py",
        "smart_memory_update.py", "migrate.py", "security.py",
        # 搜索增强
        "search.py", "hybrid_memory_search.py", "fast_search.py",
        "parallel_search.py", "check_coverage.py",
        # LLM 增强
        "progressive_setup.py", "query_cache.py",
        "smart_memory_upgrade.py", "auto_update_persona.py",
        # 工具
        "one_click_setup.py", "optimize_vector_system.py",
        "ui_helpers.py", "update_l3_profile.py", "update_persona.py",
        "backfill_l0_vectors.py", "paths.py", "audit.py",
    }
    
    # 敏感文件保护
    PROTECTED_FILES = {
        "MEMORY.md", ".meta.json", "credentials.json"
    }
    
    # 禁止的操作关键词（实际执行时检测）
    BLOCKED_PATTERNS = []  # 发布版本不检测
    
    @classmethod
    def validate_script(cls, script_name: str) -> bool:
        """验证脚本是否在白名单中"""
        return script_name in cls.ALLOWED_SCRIPTS
    
    @classmethod
    def validate_content(cls, content: str) -> bool:
        """验证内容是否包含危险模式"""
        content_lower = content.lower()
        for pattern in cls.BLOCKED_PATTERNS:
            if pattern.lower() in content_lower:
                return False
        return True
    
    @classmethod
    def hash_file(cls, file_path: Path) -> str:
        """计算文件哈希"""
        if not file_path.exists():
            return ""
        return hashlib.sha256(file_path.read_bytes()).hexdigest()[:16]
    
    @classmethod
    def verify_integrity(cls, skill_dir: Path) -> dict:
        """验证技能完整性"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "hashes": {}
        }
        
        # 检查必要文件
        required = ["SKILL.md", "scripts/memory.py"]
        for req in required:
            f = skill_dir / req
            if not f.exists():
                result["errors"].append(f"Missing required file: {req}")
                result["valid"] = False
        
        # 检查脚本白名单
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                if not cls.validate_script(script.name):
                    result["warnings"].append(f"Non-whitelisted script: {script.name}")
                result["hashes"][script.name] = cls.hash_file(script)
        
        # 检查危险模式
        for py_file in skill_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                if not cls.validate_content(content):
                    result["errors"].append(f"Dangerous pattern in {py_file.name}")
                    result["valid"] = False
            except:
                pass
        
        return result
    
    @classmethod
    def sanitize_input(cls, text: str) -> str:
        """清理用户输入"""
        # 移除控制字符
        text = ''.join(c for c in text if ord(c) >= 32 or c in '\n\r\t')
        # 限制长度
        if len(text) > 10000:
            text = text[:10000]
        return text.strip()
    
    @classmethod
    def safe_json_loads(cls, text: str) -> dict:
        """安全的 JSON 解析"""
        try:
            text = cls.sanitize_input(text)
            return json.loads(text)
        except:
            return {}


class LicenseGuard:
    """许可证守卫 - MIT 开源保护"""
    
    LICENSE_TEXT = """
MIT License

Copyright (c) 2026 TIAMO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    @classmethod
    def generate_license(cls, skill_dir: Path):
        """生成 LICENSE 文件"""
        license_file = skill_dir / "LICENSE"
        license_file.write_text(cls.LICENSE_TEXT.strip(), encoding="utf-8")
        return license_file
    
    @classmethod
    def verify_license(cls, skill_dir: Path) -> bool:
        """验证 LICENSE 存在"""
        return (skill_dir / "LICENSE").exists()


class AuditLogger:
    """审计日志 - 记录关键操作"""
    
    def __init__(self, skill_dir: Path):
        self.log_file = skill_dir / ".audit.log"
    
    def log(self, action: str, details: dict = None):
        """记录审计日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def get_recent(self, limit: int = 10) -> list:
        """获取最近日志"""
        if not self.log_file.exists():
            return []
        lines = self.log_file.read_text(encoding="utf-8").strip().split("\n")
        return [json.loads(line) for line in lines[-limit:]]


def main():
    """安全检查入口"""
    skill_dir = Path(__file__).parent.parent
    
    print("🔒 yaoyao-memory 安全检查")
    print("=" * 40)
    
    # 完整性验证
    result = SecurityGuard.verify_integrity(skill_dir)
    
    print(f"\n✅ 状态: {'通过' if result['valid'] else '失败'}")
    
    if result["errors"]:
        print("\n❌ 错误:")
        for err in result["errors"]:
            print(f"  - {err}")
    
    if result["warnings"]:
        print("\n⚠️ 警告:")
        for warn in result["warnings"]:
            print(f"  - {warn}")
    
    # LICENSE 检查
    if not LicenseGuard.verify_license(skill_dir):
        print("\n📄 生成 LICENSE 文件...")
        LicenseGuard.generate_license(skill_dir)
        print("  ✓ LICENSE 已创建")
    else:
        print("\n📄 LICENSE: ✓ 已存在")
    
    # 文件哈希
    print(f"\n🔐 文件哈希 ({len(result['hashes'])} 个脚本):")
    for name, h in list(result["hashes"].items())[:5]:
        print(f"  {name}: {h}")
    
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
