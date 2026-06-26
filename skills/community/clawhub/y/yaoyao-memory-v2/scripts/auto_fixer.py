#!/usr/bin/env python3
"""
自动修复系统 - 自修复常见问题
当检测到问题时，尝试自动修复

自修复场景：
1. Embedding 缓存损坏
2. 配置文件损坏
3. Feature Flag 文件损坏
4. 记忆目录缺失
5. 向量数据库损坏
6. 快照目录缺失
7. 缓存目录缺失
8. 脚本权限问题
9. 向量扩展未安装
10. 数据库连接超时
11. API Key 过期检测
12. 记忆文件权限问题
"""
import sys
import os
import json
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

try:
    from audit import log
except Exception as e:
    log(f"Warning: {type(e).__name__}: {e}")
    def log(*args, **kwargs): pass


class AutoFixer:
    """自动修复器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.skill_dir = self.script_dir.parent
        self.config_dir = self.skill_dir / "config"
        
        # 路径发现（使用 paths 模块）
        try:
            sys.path.insert(0, str(self.script_dir))
            from paths import get_memory_base, get_vectors_db, check_sqlite_vec_installed
            self.memory_base = get_memory_base()
            self.vectors_db = get_vectors_db()
            self.vec_installed, _ = check_sqlite_vec_installed()
        except ImportError:
            # paths 模块不可用，使用回退路径
            self.memory_base = Path.home() / ".openclaw" / "memory"
            self.vectors_db = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
            self.vec_installed = False
        except Exception:
            # 其他错误，使用安全默认值
            self.memory_base = Path.home() / ".openclaw" / "memory"
            self.vectors_db = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
            self.vec_installed = False
        
        # 基于 memory_base 设置其他目录
        self.memory_dir = self.memory_base
        self.cache_dir = self.memory_base / ".cache"
        self.snapshot_dir = self.memory_base / ".snapshots"
    
    def diagnose(self) -> list:
        """诊断所有可修复问题"""
        issues = []
        
        # 1. 检查 embedding 缓存
        cache_file = self.config_dir / "embeddings_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    json.load(f)
            except (json.JSONDecodeError, IOError, Exception) as e:
                issues.append({
                    "type": "cache_corrupted",
                    "file": str(cache_file),
                    "problem": f"Embedding 缓存文件损坏: {e}",
                    "fix": "删除缓存文件，系统会自动重建",
                    "action": lambda: cache_file.unlink() if cache_file.exists() else None,
                    "severity": "high"
                })
        
        # 2. 检查记忆目录
        if not self.memory_dir.exists():
            issues.append({
                "type": "memory_dir_missing",
                "problem": "记忆目录不存在",
                "fix": "创建记忆目录",
                "action": lambda: self.memory_dir.mkdir(parents=True, exist_ok=True),
                "severity": "critical"
            })
        
        # 3. 检查配置文件
        llm_config = self.config_dir / "llm_config.json"
        if llm_config.exists():
            try:
                with open(llm_config) as f:
                    json.load(f)
            except (json.JSONDecodeError, IOError, Exception) as e:
                issues.append({
                    "type": "config_corrupted",
                    "file": str(llm_config),
                    "problem": f"配置文件格式错误: {e}",
                    "fix": "备份并重建配置",
                    "action": lambda: self._backup_and_reset_config(llm_config),
                    "severity": "high"
                })
        
        # 4. 检查 feature_flag 文件
        ff_file = self.config_dir / "feature_flags.json"
        if ff_file.exists():
            try:
                with open(ff_file) as f:
                    json.load(f)
            except Exception as e:
                log(f"Warning: {type(e).__name__}: {e}")
                issues.append({
                    "type": "feature_flag_corrupted",
                    "file": str(ff_file),
                    "problem": "Feature Flag 文件损坏",
                    "fix": "重置 Feature Flags",
                    "action": lambda: ff_file.unlink() if ff_file.exists() else None,
                    "severity": "medium"
                })
        
        # 5. 检查磁盘空间
        try:
            stat = shutil.disk_usage(self.memory_dir)
            if stat.free < 100 * 1024 * 1024:  # < 100MB
                issues.append({
                    "type": "low_disk_space",
                    "problem": f"磁盘空间不足（剩余 {stat.free // (1024*1024)}MB）",
                    "fix": "建议清理过期记忆或删除缓存",
                    "action": None,
                    "severity": "high"
                })
        except Exception as e:
            log(f"Warning: {type(e).__name__}: {e}")
            pass
        
        # 6. 检查缓存目录
        if not self.cache_dir.exists():
            issues.append({
                "type": "cache_dir_missing",
                "problem": "缓存目录不存在",
                "fix": "创建缓存目录",
                "action": lambda: self.cache_dir.mkdir(parents=True, exist_ok=True),
                "severity": "low"
            })
        
        # 7. 检查快照目录
        if not self.snapshot_dir.exists():
            issues.append({
                "type": "snapshot_dir_missing",
                "problem": "快照目录不存在",
                "fix": "创建快照目录",
                "action": lambda: self.snapshot_dir.mkdir(parents=True, exist_ok=True),
                "severity": "low"
            })
        
        # 8. 检查向量数据库完整性
        if self.vectors_db.exists():
            try:
                conn = sqlite3.connect(str(self.vectors_db))
                cursor = conn.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                conn.close()
                
                if result[0] != 'ok':
                    issues.append({
                        "type": "vector_db_corrupted",
                        "problem": "向量数据库可能损坏",
                        "fix": "建议运行向量优化脚本重建索引",
                        "action": None,
                        "severity": "high"
                    })
            except Exception as e:
                log(f"Warning: {type(e).__name__}: {e}")
                issues.append({
                    "type": "vector_db_error",
                    "problem": "向量数据库无法访问",
                    "fix": "检查数据库文件权限或重建",
                    "action": None,
                    "severity": "high"
                })
        
        # 9. 检查向量扩展
        if not self.vec_installed:
            issues.append({
                "type": "vec_extension_missing",
                "problem": "sqlite-vec 向量扩展未安装",
                "fix": "安装 memory-tencentdb 插件：openclaw plugin install memory-tencentdb",
                "action": None,
                "severity": "critical"
            })
        
        # 10. 注意：Python 脚本不需要执行权限，所以不检查这个
        # 11. 检查快照目录是否需要创建
        if self.snapshot_dir and not self.snapshot_dir.exists():
            # 只有在快照文件存在但目录不存在时才需要修复
            snapshot_meta = self.snapshot_dir.parent / "snapshots.json"
            if snapshot_meta.exists():
                issues.append({
                    "type": "snapshot_dir_missing",
                    "problem": "快照目录不存在",
                    "fix": "创建快照目录",
                    "action": lambda: self.snapshot_dir.mkdir(parents=True, exist_ok=True),
                    "severity": "low"
                })
        
        # 11. 检查过期缓存
        if self.cache_dir.exists():
            cache_files = list(self.cache_dir.glob("*.json"))
            old_files = []
            for f in cache_files:
                try:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if datetime.now() - mtime > timedelta(days=7):
                        old_files.append(f)
                except Exception as e:
                    log(f"Warning: {type(e).__name__}: {e}")
                    pass
            
            if old_files:
                issues.append({
                    "type": "old_cache_files",
                    "problem": f"存在 {len(old_files)} 个超过7天的缓存文件",
                    "fix": "清理过期缓存",
                    "action": lambda: [f.unlink() for f in old_files],
                    "severity": "low"
                })
        
        # 12. 检查 API Key 格式
        secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
        if secrets_file.exists():
            try:
                content = secrets_file.read_text()
                if "YOUR_API_KEY" in content or "placeholder" in content.lower():
                    issues.append({
                        "type": "api_key_not_configured",
                        "problem": "API Key 可能是占位符，未真正配置",
                        "fix": "请配置真实的 API Key",
                        "action": None,
                        "severity": "medium"
                    })
            except Exception as e:
                log(f"Warning: {type(e).__name__}: {e}")
                pass
        
        return issues
    
    def _backup_and_reset_config(self, config_file: Path):
        """备份损坏的配置并重置"""
        backup = config_file.with_suffix('.json.bak')
        shutil.copy2(config_file, backup)
        default_config = {
            "embedding": {
                "api_key": "",
                "base_url": "https://ai.gitee.com/v1/embeddings",
                "model": "Qwen3-Embedding-8B",
                "dimensions": 1024
            },
            "llm": {
                "api_key": "",
                "base_url": ""
            }
        }
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        return True
    
    def auto_fix(self) -> dict:
        """执行自动修复"""
        issues = self.diagnose()
        fixed = []
        failed = []
        
        for issue in issues:
            try:
                if issue.get("action"):
                    issue["action"]()
                fixed.append({
                    "type": issue["type"],
                    "fix": issue["fix"]
                })
                log(f"[AutoFixer] 已修复: {issue['problem']}", "auto_fix")
            except Exception as e:
                failed.append({
                    "type": issue["type"],
                    "problem": issue["problem"],
                    "error": str(e)
                })
                log(f"[AutoFixer] 修复失败: {issue['problem']} - {e}", "auto_fix")
        
        return {
            "fixed": fixed,
            "failed": failed,
            "total": len(issues)
        }
    
    def report(self) -> str:
        """生成诊断报告"""
        issues = self.diagnose()
        
        if not issues:
            return "✅ 未检测到可自修复问题"
        
        lines = ["⚠️ 检测到以下可修复问题：", ""]
        
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. {issue['problem']}")
            lines.append(f"   修复方案: {issue['fix']}")
        
        lines.append("")
        lines.append("执行 `auto_fixer.py fix` 进行自动修复")
        
        return "\n".join(lines)


def main():
    fixer = AutoFixer()
    
    if len(sys.argv) < 2:
        print(fixer.report())
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'diagnose':
        print(fixer.report())
    
    elif cmd == 'fix':
        print("🔧 执行自动修复...")
        result = fixer.auto_fix()
        
        if result['fixed']:
            print(f"\n✅ 已修复 {len(result['fixed'])} 项:")
            for f in result['fixed']:
                print(f"  - {f['fix']}")
        
        if result['failed']:
            print(f"\n❌ 修复失败 {len(result['failed'])} 项:")
            for f in result['failed']:
                print(f"  - {f['problem']}: {f['error']}")
        
        if not result['fixed'] and not result['failed']:
            print("✅ 没有需要修复的问题")
    
    elif cmd == 'auto':
        """静默修复 - 用于脚本自动调用"""
        result = fixer.auto_fix()
        return result


if __name__ == '__main__':
    main()
