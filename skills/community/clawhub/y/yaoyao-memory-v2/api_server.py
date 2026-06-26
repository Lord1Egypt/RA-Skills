#!/usr/bin/env python3
"""
yaoyao-memory-dashboard API 服务器 v4
增强版 - 完整功能 + 优化性能
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
MEMORY_SKILLS_DIR = SKILLS_DIR / "yaoyao-memory"
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
STATE_FILE = MEMORY_DIR / "heartbeat-state.json"
HTML_FILE = Path(__file__).parent.parent / "html" / "dashboard.html"

# 缓存
_cache = {"stats": None, "stats_time": 0}
_CACHE_TTL = 5  # 秒


def get_stats(use_cache=True):
    """获取统计数据"""
    global _cache
    
    # 简单缓存
    if use_cache and _cache["stats"] and (time.time() - _cache["stats_time"]) < _CACHE_TTL:
        return _cache["stats"]
    
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory import Memory
        m = Memory()
        stats = m.stats()
        
        state = {}
        if STATE_FILE.exists():
            try:
                state = json.load(open(STATE_FILE))
            except:
                pass
        
        total = stats.get("total", 0)
        
        # 计算健康度
        health = 100
        errors = stats.get("by_type", {}).get("error", 0)
        if total < 10:
            health = 60
        elif total < 50:
            health = 80
        if errors > 5:
            health -= min(20, errors * 2)
        
        result = {
            "total": total,
            "healthScore": max(0, health),
            "by_type": stats.get("by_type", {}),
            "by_importance": stats.get("by_importance", {}),
            "cacheCount": total,
            "lastSync": state.get("lastChecks", {}).get("imaSync", "从未"),
            "uptime": state.get("uptime", 0),
            "errors": errors,
        }
        
        _cache["stats"] = result
        _cache["stats_time"] = time.time()
        return result
    except Exception as e:
        return {"error": str(e), "total": 0, "healthScore": 0}


def get_recent_activity(limit=30):
    """获取最近活动"""
    activities = []
    try:
        memories = list(MEMORY_DIR.glob("*.md"))
        for f in sorted(memories, key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
            if f.name.startswith("."):
                continue
            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            memory_type = "info"
            importance = "Normal"
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")[:500]
                for line in content.split("\n")[:10]:
                    if line.startswith("类型:") or line.startswith("type:"):
                        memory_type = line.split(":")[1].strip().lower()
                    if line.startswith("重要性:") or line.startswith("importance:"):
                        importance = line.split(":")[1].strip()
            except:
                pass
            
            activities.append({
                "file": f.name,
                "modified": mtime.strftime("%H:%M:%S"),
                "date": mtime.strftime("%Y-%m-%d"),
                "size": stat.st_size,
                "type": memory_type,
                "importance": importance,
            })
    except:
        pass
    return activities


def get_daily_stats(days=30):
    """获取每日统计"""
    try:
        memories = list(MEMORY_DIR.glob("*.md"))
        daily = {}
        
        for f in memories:
            if f.name.startswith("."):
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            date_key = mtime.strftime("%Y-%m-%d")
            
            if date_key not in daily:
                daily[date_key] = {"count": 0, "size": 0}
            daily[date_key]["count"] += 1
            daily[date_key]["size"] += f.stat().st_size
        
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            result.append({
                "date": date,
                "count": daily.get(date, {}).get("count", 0),
                "size": daily.get(date, {}).get("size", 0),
            })
        
        return list(reversed(result))
    except:
        return []


def get_system_info():
    """获取系统信息"""
    try:
        import shutil
        mem_usage = shutil.disk_usage(MEMORY_DIR)
        
        return {
            "disk_total": mem_usage.total,
            "disk_used": mem_usage.used,
            "disk_free": mem_usage.free,
            "disk_percent": int(mem_usage.used / mem_usage.total * 100),
            "memory_total": mem_usage.total,
            "memory_used_pct": int(mem_usage.used / mem_usage.total * 100),
        }
    except:
        return {}


def get_alerts():
    """获取告警"""
    try:
        alert_file = MEMORY_DIR / ".alerts.json"
        if not alert_file.exists():
            return []
        alerts = json.load(open(alert_file))
        return alerts.get("active_alerts", [])[:10]
    except:
        return []


def get_performance_stats():
    """获取性能统计"""
    perf_file = MEMORY_DIR / ".performance.json"
    if not perf_file.exists():
        return {"operation_count": 0, "avg_latency_ms": 0, "p95_latency_ms": 0, "p99_latency_ms": 0}
    
    try:
        data = json.load(open(perf_file))
        records = data.get("records", [])
        
        cutoff = datetime.now() - timedelta(hours=1)
        recent = [r for r in records if datetime.fromisoformat(r["timestamp"]) >= cutoff]
        
        if not recent:
            return {"operation_count": 0, "avg_latency_ms": 0, "p95_latency_ms": 0, "p99_latency_ms": 0}
        
        total = len(recent)
        latencies = sorted(r["latency_ms"] for r in recent)
        p95_idx = min(int(total * 0.95), len(latencies) - 1)
        p99_idx = min(int(total * 0.99), len(latencies) - 1)
        
        return {
            "operation_count": total,
            "avg_latency_ms": round(sum(r["latency_ms"] for r in recent) / total, 1),
            "p95_latency_ms": round(latencies[p95_idx], 1),
            "p99_latency_ms": round(latencies[p99_idx], 1),
            "total_tokens": sum(r.get("tokens", 0) for r in recent),
            "cache_hit_rate": sum(1 for r in recent if r.get("cache_hit")) / total if total > 0 else 0,
            "success_rate": sum(1 for r in recent if r.get("success")) / total if total > 0 else 0,
        }
    except:
        return {}


def get_backup_list():
    """获取备份列表"""
    backup_dir = MEMORY_DIR / "backups"
    if not backup_dir.exists():
        return []
    
    backups = []
    for f in sorted(backup_dir.glob("backup_*.tar.gz"), reverse=True)[:10]:
        backups.append({
            "name": f.name,
            "size": f.stat().st_size,
            "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
        })
    return backups


def get_feature_flags():
    """获取功能开关（带描述）"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from feature_flag import FeatureFlag
        ff = FeatureFlag()
        all_flags = ff.list()
        # 返回完整信息包括描述
        result = {}
        for k, v in all_flags.items():
            if isinstance(v, dict):
                result[k] = {
                    'value': v.get('value', False),
                    'description': v.get('description', ''),
                    'type': v.get('type', 'bool'),
                }
            else:
                result[k] = {'value': v, 'description': '', 'type': 'unknown'}
        return result
    except Exception as e:
        return {}


def toggle_feature(feature: str, enabled: bool):
    """切换功能开关"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from feature_flag import FeatureFlag
        ff = FeatureFlag()
        if enabled:
            ff.enable(feature)
        else:
            ff.disable(feature)
        return {"success": True, "feature": feature, "enabled": enabled}
    except Exception as e:
        return {"error": str(e)}


def search_memories(keyword: str, limit=50):
    """搜索记忆"""
    if not keyword:
        return []
    
    try:
        results = []
        keyword_lower = keyword.lower()
        memories = list(MEMORY_DIR.glob("*.md"))
        
        for f in memories:
            if f.name.startswith("."):
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if keyword_lower in content.lower():
                    lines = content.split("\n")
                    title = lines[0] if lines else f.name
                    preview = content[:300].replace("\n", " ")
                    
                    results.append({
                        "file": f.name,
                        "title": title[:80] if len(title) > 80 else title,
                        "preview": preview[:150],
                        "size": f.stat().st_size,
                        "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    })
            except:
                pass
        return results[:limit]
    except:
        return []


def run_health_check():
    """执行健康检查"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from health_check import HealthChecker
        hc = HealthChecker()
        result = hc.run()
        return result
    except Exception as e:
        return {"error": str(e)}


def create_backup(description: str = ""):
    """创建备份"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from backup_manager import BackupManager
        bm = BackupManager()
        info = bm.create_backup(description or "Dashboard手动备份")
        return {"success": True, "backup_id": info.id if info else None}
    except Exception as e:
        return {"error": str(e)}


def cleanup_expired():
    """清理过期"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from cleanup import main as cleanup_main
        cleanup_main()
        return {"success": True}
    except:
        return {"success": True}


def clear_cache():
    """清理缓存"""
    try:
        cache_dir = MEMORY_DIR / "cache"
        if cache_dir.exists():
            for f in cache_dir.glob("*.json"):
                f.unlink()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}


def get_config_all():
    """获取所有配置"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import get_config, get_categories, CAT_NAMES, get_api_config, get_api_categories
        config = get_config()
        categories = get_categories()
        # 获取 API 配置
        api_config = get_api_config()
        api_categories = get_api_categories()
        # 合并 API 分类到总分类
        for cat, keys in api_categories.items():
            if cat not in categories:
                categories[cat] = keys
            else:
                categories[cat].extend(keys)
        # 合并 API 配置到总配置
        config.update(api_config)
        return {
            "config": config,
            "categories": categories,
            "cat_names": CAT_NAMES,
        }
    except Exception as e:
        return {"error": str(e)}


def set_config_item(key: str, value: str):
    """设置配置项"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import set_config
        success = set_config(key, value)
        if success:
            return {"success": True, "key": key, "value": value}
        else:
            return {"error": "保存失败"}
    except Exception as e:
        return {"error": str(e)}


def delete_config_item(key: str):
    """删除配置项"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import delete_config
        success = delete_config(key)
        return {"success": success}
    except Exception as e:
        return {"error": str(e)}


def get_password_status():
    """获取密码状态"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import has_config_password
        return {"has_password": has_config_password()}
    except Exception as e:
        return {"error": str(e), "has_password": False}


def set_password(password: str):
    """设置二级密码"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import set_config_password
        success = set_config_password(password)
        return {"success": success}
    except Exception as e:
        return {"error": str(e)}


def verify_password_api(password: str):
    """验证二级密码"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import verify_config_password
        correct = verify_config_password(password)
        return {"success": True, "correct": correct}
    except Exception as e:
        return {"error": str(e), "correct": False}


def remove_password(current_password: str):
    """删除二级密码"""
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from config_manager import verify_config_password, remove_config_password
        if verify_config_password(current_password):
            success = remove_config_password()
            return {"success": success}
        else:
            return {"error": "密码错误", "correct": False}
    except Exception as e:
        return {"error": str(e)}


class DashboardHandler(BaseHTTPRequestHandler):
    """请求处理器"""
    
    def do_GET(self):
        path = urlparse(self.path).path
        query = urlparse(self.path).query
        
        if path == "/" or path == "/dashboard":
            if HTML_FILE.exists():
                with open(HTML_FILE, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Dashboard not found")
        
        elif path == "/api/stats":
            self.send_json(get_stats())
        elif path == "/api/activity":
            self.send_json(get_recent_activity())
        elif path == "/api/daily":
            self.send_json(get_daily_stats())
        elif path == "/api/system":
            self.send_json(get_system_info())
        elif path == "/api/alerts":
            self.send_json(get_alerts())
        elif path == "/api/performance":
            self.send_json(get_performance_stats())
        elif path == "/api/backups":
            self.send_json(get_backup_list())
        elif path == "/api/features":
            self.send_json(get_feature_flags())
        elif path.startswith("/api/search"):
            params = parse_qs(query)
            keyword = params.get("q", [""])[0]
            self.send_json(search_memories(keyword))
        elif path == "/api/config":
            self.send_json(get_config_all())
        elif path == "/api/get_password_status":
            self.send_json(get_password_status())
        elif path == "/api/memory_trends":
            self.send_json(run_memory_trends())
        elif path == "/api/memory_insights":
            self.send_json(run_memory_insights())
        elif path == "/api/memory_quality":
            self.send_json(run_memory_quality())
        elif path == "/api/smart_query":
            self.send_json(run_smart_query())
        elif path == "/api/query_predictor":
            self.send_json(run_query_predictor())
        elif path == "/api/snapshot_list":
            self.send_json(get_snapshot_list())
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        path = urlparse(self.path).path
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        action = path.replace("/api/", "")
        
        handlers = {
            "health_check": lambda: run_health_check(),
            "backup": lambda: create_backup(data.get("description", "")),
            "cleanup": lambda: cleanup_expired(),
            "clear_cache": lambda: clear_cache(),
            "toggle_feature": lambda: toggle_feature(data.get("feature", ""), data.get("enabled", True)),
            "search": lambda: search_memories(data.get("keyword", "")),
            "get_config": lambda: get_config_all(),
            "set_config": lambda: set_config_item(data.get("key", ""), data.get("value", "")),
            "delete_config": lambda: delete_config_item(data.get("key", "")),
            "get_password_status": lambda: get_password_status(),
            "set_password": lambda: set_password(data.get("password", "")),
            "verify_password": lambda: verify_password_api(data.get("password", "")),
            "remove_password": lambda: remove_password(data.get("password", "")),
            "snapshot_create": lambda: create_snapshot(),
        }
        
        if action in handlers:
            self.send_json(handlers[action]())
        else:
            self.send_error(404, "Unknown action")
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(port=8765):
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"🦞 Dashboard v4 运行中 http://localhost:{port}/dashboard")
    server.serve_forever()


# 新模块 API 包装函数
def run_memory_trends():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory_trends import MemoryTrends
        mt = MemoryTrends()
        result = mt.calculate_health_score()
        mt.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def run_memory_insights():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory_insights import MemoryInsights
        mi = MemoryInsights()
        result = {"keywords": mi.extract_keywords(5), "topics": mi.identify_patterns()}
        mi.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def run_memory_quality():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory_quality import MemoryQualityAnalyzer
        mq = MemoryQualityAnalyzer()
        result = mq.get_quality_distribution()
        mq.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def run_smart_query():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from smart_query import SmartQueryRecommender
        sq = SmartQueryRecommender()
        result = {"suggestions": sq.get_time_based_suggestions()}
        sq.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def run_query_predictor():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from query_predictor import QueryPredictor
        qp = QueryPredictor()
        result = {"predictions": qp.get_combined_predictions(limit=5)}
        qp.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def create_snapshot():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory_snapshot import MemorySnapshot
        ms = MemorySnapshot()
        result = ms.create_snapshot()
        ms.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def get_snapshot_list():
    try:
        sys.path.insert(0, str(MEMORY_SKILLS_DIR / "scripts"))
        from memory_snapshot import MemorySnapshot
        ms = MemorySnapshot()
        result = ms.list_snapshots()
        ms.close()
        return result
    except Exception as e:
        return []


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Yaoyao Memory Dashboard")
    parser.add_argument("--port", type=int, default=8765, help="端口号")
    args = parser.parse_args()
    run_server(args.port)
