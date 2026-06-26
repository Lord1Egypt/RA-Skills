#!/usr/bin/env python3
"""
yaoyao-memory 健康检测脚本 v2
- 智能区分"未启用"vs"有问题"
- 只在功能启用时才检查
"""

import json
import os
import sys
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

from paths import get_memory_base, get_openclaw_home, get_vectors_db, CONFIG_DIR

# 状态文件
STATE_FILE = get_memory_base() / "heartbeat-state.json"
MEMORY_DIR = get_memory_base()
CHROMA_DB = get_memory_base() / "chroma_db"
EMBEDDING_CACHE = CONFIG_DIR / "embeddings_cache.json"
VECTORS_DB = get_vectors_db()


class HealthChecker:
    """健康检测器 v2"""
    
    def __init__(self):
        self.checks = []
        self.load_state()
    
    def load_state(self):
        """加载上次状态"""
        if STATE_FILE.exists():
            try:
                self.state = json.loads(STATE_FILE.read_text())
            except Exception as e:
                self.log(f"Warning: {type(e).__name__}: {e}")
                self.state = {}
        else:
            self.state = {}
    
    def save_state(self):
        """保存状态"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))
    
    def is_feature_enabled(self, feature: str) -> bool:
        """检查功能是否启用"""
        # 优先检查 unified_config.json
        config_file = CONFIG_DIR / "unified_config.json"
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text())
                # vector_search 在配置中
                if feature == "vector_search":
                    return config.get("vector_search", {}).get("enabled", True)
                # embedding 检查 unified_config 中的相关配置
                if feature == "embedding":
                    return config.get("embedding", {}).get("enabled", False)
            except Exception as e:
                self.log(f"Warning: {type(e).__name__}: {e}")
                pass
        # 回退检查 feature_flag.json
        flag_file = CONFIG_DIR / "feature_flag.json"
        if flag_file.exists():
            try:
                flags = json.loads(flag_file.read_text())
                return flags.get(feature, True)  # 默认 True
            except Exception as e:
                self.log(f"Warning: {type(e).__name__}: {e}")
                pass
        return True  # 默认启用
    
    # ========== 一、系统健康检测 ==========
    def check_system_health(self):
        """系统整体健康度"""
        score = 100
        
        # 检查关键目录
        if not MEMORY_DIR.exists():
            score -= 30
        if not VECTORS_DB.exists():
            score -= 20
        
        # 检查配置文件
        if not (CONFIG_DIR / "feature_flag.json").exists():
            score -= 10
        
        status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        
        self.checks.append({
            "name": "系统健康度",
            "score": score,
            "status": status
        })
        return score >= 80
    
    # ========== 二、模块完整性 ==========
    def check_module_integrity(self):
        """模块完整性检查"""
        scripts_dir = Path(__file__).parent
        
        core_modules = [
            "memory.py",
            "search.py",
            "health_check.py",
            "auto_fixer.py",
            "feature_flag.py",
            "paths.py"
        ]
        
        missing = [m for m in core_modules if not (scripts_dir / m).exists()]
        total_scripts = len(list(scripts_dir.glob("*.py")))
        
        if missing:
            score = max(0, 100 - len(missing) * 15)
            status = "⚠️" if len(missing) <= 2 else "❌"
            message = f"缺少: {', '.join(missing)}"
        else:
            score = 100
            status = "✅"
            message = f"核心模块完整 ({total_scripts}个脚本)"
        
        self.checks.append({
            "name": "模块完整性",
            "score": score,
            "status": status,
            "message": message,
            "total_scripts": total_scripts
        })
        return len(missing) == 0
    
    # ========== 三、错误日志 ==========
    def check_error_logs(self):
        """错误日志监控"""
        error_file = Path.home() / ".openclaw" / "workspace" / ".learnings" / "ERRORS.md"
        
        if not error_file.exists():
            error_count = 0
        else:
            content = error_file.read_text()
            error_count = content.count("\n## ")
        
        status = "✅" if error_count < 10 else "⚠️" if error_count < 20 else "❌"
        
        self.checks.append({
            "name": "错误日志监控",
            "count": error_count,
            "status": status
        })
        return error_count < 10
    
    # ========== 四、性能检测 ==========
    def check_performance(self):
        """性能检测 - 只在缓存启用时检查"""
        # 检查 embedding 功能是否启用
        emb_config = CONFIG_DIR / "embedding_config.json"
        emb_enabled = emb_config.exists()
        
        if not emb_enabled:
            # 功能未启用，不检查
            self.checks.append({
                "name": "性能检测",
                "status": "ℹ️",
                "message": "Embedding 未配置（N/A）"
            })
            return True
        
        # 功能启用，检查缓存（缓存为空是正常的，刚配置）
        cache_exists = EMBEDDING_CACHE.exists()
        cache_size = EMBEDDING_CACHE.stat().st_size if cache_exists else 0
        cache_has_data = cache_size > 100  # 至少有一些数据
        
        self.checks.append({
            "name": "性能检测",
            "cache_exists": cache_exists,
            "cache_size": cache_size,
            "status": "✅",
            "message": f"缓存正常 ({cache_size}字节)" if cache_has_data else "缓存为空（正常，首次使用会填充）"
        })
        return True  # 缓存为空不扣分
    
    # ========== 五、数据保留 ==========
    def check_data_retention(self):
        """数据保留检测"""
        cutoff = datetime.now() - timedelta(days=30)
        old_files = []
        
        if MEMORY_DIR.exists():
            for f in MEMORY_DIR.glob("*.md"):
                if f.stat().st_mtime < cutoff.timestamp():
                    old_files.append(f.name)
        
        self.checks.append({
            "name": "数据保留检测",
            "old_files_count": len(old_files),
            "status": "✅" if len(old_files) == 0 else "📋",
            "message": f"30天+文件: {len(old_files)}个"
        })
        return True
    
    # ========== 六、向量系统 ==========
    def check_vector_system(self):
        """向量系统检测 - 只在向量功能启用时检查"""
        # 检查向量功能是否启用
        vec_enabled = self.is_feature_enabled("vector_search")
        
        if not vec_enabled:
            self.checks.append({
                "name": "向量系统检测",
                "status": "ℹ️",
                "message": "向量搜索未启用（N/A）"
            })
            return True
        
        checks = {
            "embedding_cache": EMBEDDING_CACHE.exists(),
            "chroma_db": CHROMA_DB.exists(),
        }
        
        cache_size = EMBEDDING_CACHE.stat().st_size if EMBEDDING_CACHE.exists() else 0
        
        # 向量系统需要 embedding cache
        all_ok = checks["embedding_cache"]
        status = "✅" if all_ok else "⚠️"
        
        self.checks.append({
            "name": "向量系统检测",
            "status": status,
            "message": "向量功能正常" if all_ok else "Embedding缓存未建立",
            "checks": checks,
            "cache_size": cache_size
        })
        return all_ok
    
    # ========== 七、检索延迟 ==========
    def check_search_performance(self):
        """检索延迟检测"""
        from memory import Memory
        
        try:
            m = Memory()
            start = time.time()
            results = m.search("测试", limit=3, method="fts")
            elapsed = (time.time() - start) * 1000
            
            ok = elapsed < 100
            
            self.checks.append({
                "name": "检索延迟检测",
                "latency_ms": round(elapsed, 1),
                "status": "✅" if ok else "⚠️",
                "message": f"{elapsed:.1f}ms"
            })
            return ok
        except Exception as e:
            self.checks.append({
                "name": "检索延迟检测",
                "status": "❌",
                "message": str(e)[:50]
            })
            return False
    
    # ========== 八、缓存命中率 ==========
    def check_cache_hit_rate(self):
        """缓存命中率检测 - 只在缓存启用时检查"""
        emb_config = CONFIG_DIR / "embedding_config.json"
        
        if not emb_config.exists():
            self.checks.append({
                "name": "缓存命中率检测",
                "status": "ℹ️",
                "message": "Embedding 未配置（N/A）"
            })
            return True
        
        # 检查缓存统计
        cache_stats = self.state.get("cache_stats", {})
        hit_rate = cache_stats.get("hit_rate", 0)
        
        status = "✅" if hit_rate > 60 else "⚠️" if hit_rate > 0 else "ℹ️"
        
        self.checks.append({
            "name": "缓存命中率检测",
            "hit_rate": hit_rate,
            "status": status,
            "message": f"{hit_rate:.0f}%" if hit_rate > 0 else "无统计数据"
        })
        return hit_rate > 60
    
    # ========== 九、记忆统计 ==========
    def check_memory_stats(self):
        """记忆统计"""
        try:
            conn = sqlite3.connect(str(VECTORS_DB))
            cursor = conn.execute("SELECT COUNT(*) FROM l1_records")
            count = cursor.fetchone()[0]
            conn.close()
            
            self.checks.append({
                "name": "记忆统计",
                "count": count,
                "status": "✅",
                "message": f"{count}条记忆"
            })
            return True
        except Exception as e:
            self.log(f"Warning: {type(e).__name__}: {e}")
            self.checks.append({
                "name": "记忆统计",
                "status": "❌",
                "message": "数据库查询失败"
            })
            return False
    
    # ========== 十、MCP管线 ==========
    def check_mcp_pipeline(self):
        """MCP记忆管线检测"""
        mcp_dir = get_openclaw_home() / "memory-tdai" / "mcp_pipeline"
        
        if not mcp_dir.exists():
            self.checks.append({
                "name": "MCP记忆管线",
                "status": "ℹ️",
                "message": "MCP 未启用（N/A）"
            })
            return True
        
        l0_count = len(list(mcp_dir.glob("l0_*.json"))) if mcp_dir.exists() else 0
        l1_count = len(list(mcp_dir.glob("l1_*.json"))) if mcp_dir.exists() else 0
        
        self.checks.append({
            "name": "MCP记忆管线",
            "l0_capture": l0_count,
            "l1_extract": l1_count,
            "status": "✅",
            "message": f"L0:{l0_count} L1:{l1_count}"
        })
        return True
    
    # ========== 十一、云同步检测 ==========
    def check_cloud_sync(self):
        """云同步检测 - 推荐用户启用云备份"""
        # 检测 IMA 配置
        ima_configured = False
        ima_client_id = os.environ.get("IMA_OPENAPI_CLIENTID")
        ima_api_key = os.environ.get("IMA_OPENAPI_APIKEY")
        
        # 检查配置文件
        if not ima_client_id or not ima_api_key:
            config_dir = Path.home() / ".config" / "ima"
            if config_dir.exists():
                client_file = config_dir / "client_id"
                api_file = config_dir / "api_key"
                if client_file.exists() and api_file.exists():
                    ima_configured = True
        else:
            ima_configured = True
        
        # 检测 Samba/NAS 配置
        samba_configured = False
        samba_host = os.environ.get("SAMBA_HOST")
        if samba_host:
            samba_configured = True
        
        # 检测云备份 Skill 是否安装
        cloud_backup_installed = False
        skills_dir = get_openclaw_home() / "workspace" / "skills"
        if skills_dir.exists():
            if (skills_dir / "yaoyao-cloud-backup").exists() or \
               (skills_dir / "yaoyao-cloud-backup-homo").exists():
                cloud_backup_installed = True
        
        if cloud_backup_installed:
            # 云备份已安装
            if ima_configured or samba_configured:
                self.checks.append({
                    "name": "云同步",
                    "status": "✅",
                    "message": "云备份已配置"
                })
            else:
                self.checks.append({
                    "name": "云同步",
                    "status": "ℹ️",
                    "message": "云备份已安装，建议配置 IMA 或 Samba"
                })
            return True
        else:
            # 云备份未安装，检测是否有可能配置
            if ima_configured or samba_configured:
                self.checks.append({
                    "name": "云同步",
                    "status": "💡",
                    "message": "检测到云凭证，建议安装 yaoyao-cloud-backup",
                    "recommend": "install_cloud_backup",
                    "has_credentials": True
                })
                return True
            else:
                self.checks.append({
                    "name": "云同步",
                    "status": "ℹ️",
                    "message": "可选功能，需时再装"
                })
                return True
    
    # ========== 主流程 ==========
    def run_all_checks(self):
        """运行所有检测"""
        print("=" * 50)
        print("🩺 yaoyao-memory 健康检测 v2")
        print("=" * 50)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        checks = [
            ("【一】系统健康检测", self.check_system_health),
            ("【二】模块完整性", self.check_module_integrity),
            ("【三】错误日志监控", self.check_error_logs),
            ("【四】性能检测", self.check_performance),
            ("【五】数据保留检测", self.check_data_retention),
            ("【六】向量系统检测", self.check_vector_system),
            ("【七】检索延迟检测", self.check_search_performance),
            ("【八】缓存命中率检测", self.check_cache_hit_rate),
            ("【九】记忆统计", self.check_memory_stats),
            ("【十】MCP管线检测", self.check_mcp_pipeline),
            ("【十一】云同步检测", self.check_cloud_sync),
        ]
        
        for title, check_fn in checks:
            print(title)
            try:
                check_fn()
            except Exception as e:
                print(f"  检测出错: {e}")
            print()
        
        # 打印汇总
        self.print_summary()
    
    def print_summary(self):
        """打印汇总"""
        print("=" * 50)
        print("📊 检测结果汇总")
        print("=" * 50)
        
        # 分类统计
        passed = sum(1 for c in self.checks if c["status"] == "✅")
        warning = sum(1 for c in self.checks if c["status"] == "⚠️")
        na = sum(1 for c in self.checks if c["status"] in ["ℹ️", "📋"])
        failed = sum(1 for c in self.checks if c["status"] == "❌")
        
        for check in self.checks:
            status = check.get("status", "?")
            name = check.get("name", "?")
            msg = check.get("message", "")
            print(f"{status} {name}: {msg}")
        
        # 检查是否有云同步推荐
        cloud_recommend = next((c for c in self.checks if c.get("recommend") == "install_cloud_backup"), None)
        if cloud_recommend:
            print()
            print("💡 云端备份推荐")
            print("-" * 50)
            print("检测到您可能需要云端备份功能！")
            print()
            print("🔐 安全优势：")
            print("   - 本地数据完全自主控制")
            print("   - 云端凭证与本地完全隔离")
            print("   - 独立安装，互不影响")
            print()
            print("📦 安装方式：")
            print("   clawhub install yaoyao-cloud-backup")
            print()
            print("☁️ 云同步功能：")
            print("   - IMA 知识库同步（腾讯）")
            print("   - Samba/NAS 局域网同步")
            print("   - 数据导出（JSON/MD/CSV/HTML）")
        
        print()
        
        # 健康度计算（只统计实际检查项，排除N/A）
        actual_checks = [c for c in self.checks if c["status"] not in ["ℹ️"]]
        if actual_checks:
            actual_passed = sum(1 for c in actual_checks if c["status"] == "✅")
            health_score = int(actual_passed / len(actual_checks) * 100)
        else:
            health_score = 100
        
        print(f"✅ 通过: {passed}  ⚠️ 警告: {warning}  ℹ️ N/A: {na}  ❌ 失败: {failed}")
        print(f"📊 整体健康度: {health_score}%")
        
        # 保存状态
        self.state["last_health_check"] = datetime.now().isoformat()
        self.state["health_score"] = health_score
        self.save_state()


if __name__ == "__main__":
    h = HealthChecker()
    h.run_all_checks()


# ========== 云备份状态查询 ==========
def get_cloud_backup_status():
    """查询云备份安装状态（供外部调用）"""
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    
    status = {
        "installed": False,
        "configured": False,
        "path": None
    }
    
    if (skills_dir / "yaoyao-cloud-backup").exists():
        status["installed"] = True
        status["path"] = str(skills_dir / "yaoyao-cloud-backup")
    elif (skills_dir / "yaoyao-cloud-backup-homo").exists():
        status["installed"] = True
        status["path"] = str(skills_dir / "yaoyao-cloud-backup-homo")
    
    # 检查是否配置
    if status["installed"]:
        ima_client = os.environ.get("IMA_OPENAPI_CLIENTID")
        ima_api = os.environ.get("IMA_OPENAPI_APIKEY")
        samba_host = os.environ.get("SAMBA_HOST")
        
        if (ima_client and ima_api) or samba_host:
            status["configured"] = True
    
    return status
