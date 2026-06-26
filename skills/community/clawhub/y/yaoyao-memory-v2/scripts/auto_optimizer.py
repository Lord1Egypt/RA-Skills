#!/usr/bin/env python3
"""
auto_optimizer.py - 自动性能优化器
根据硬件配置自动应用最优设置
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONFIG_FILE = MEMORY_DIR / "config" / "optimization.json"


def load_hardware_profile():
    """加载硬件配置"""
    from scripts.hardware_detector import detect_cpu_features, get_optimization_level
    
    features = detect_cpu_features()
    opt = get_optimization_level(features)
    
    return {
        "features": features,
        "optimization": opt,
        "timestamp": datetime.now().isoformat()
    }


def get_optimized_settings(profile):
    """根据硬件配置生成最优设置"""
    opt_level = profile["optimization"]["level"]
    features = profile["features"]
    
    settings = {
        "fts_cache_size": 1000,
        "batch_size": 100,
        "vector_enabled": False,
        "compression": "none",
        "async_mode": False
    }
    
    if opt_level in ["MAX", "HIGH"]:
        settings.update({
            "fts_cache_size": 5000,
            "batch_size": 500,
            "vector_enabled": True,
            "compression": "lz4",
            "async_mode": True
        })
    elif opt_level == "MEDIUM":
        settings.update({
            "fts_cache_size": 2000,
            "batch_size": 200,
            "vector_enabled": True,
            "compression": "lz4",
            "async_mode": True
        })
    elif opt_level == "MOBILE":
        settings.update({
            "fts_cache_size": 500,
            "batch_size": 50,
            "vector_enabled": False,
            "compression": "none",
            "async_mode": False
        })
    
    return settings


def apply_optimization(profile):
    """应用优化设置"""
    settings = get_optimized_settings(profile)
    
    # 确保配置目录存在
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存配置
    config = {
        "profile": profile,
        "settings": settings,
        "applied_at": datetime.now().isoformat()
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    
    return settings


def get_current_settings():
    """获取当前设置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return None


def main():
    print("🚀 yaoyao-memory 自动优化器")
    print("=" * 40)
    
    # 加载硬件配置
    print("\n📊 检测硬件配置...")
    profile = load_hardware_profile()
    opt = profile["optimization"]
    
    print(f"  平台: {profile['features'].get('machine', 'Unknown')}")
    print(f"  优化级别: {opt['level']}")
    print(f"  向量方法: {opt['vector_method']}")
    
    # 应用优化
    print("\n⚙️ 应用优化设置...")
    settings = apply_optimization(profile)
    
    print(f"  FTS缓存: {settings['fts_cache_size']}")
    print(f"  批处理大小: {settings['batch_size']}")
    print(f"  向量搜索: {'开启' if settings['vector_enabled'] else '关闭'}")
    print(f"  压缩: {settings['compression']}")
    print(f"  异步模式: {'开启' if settings['async_mode'] else '关闭'}")
    
    print("\n✅ 优化完成!")
    print(f"  配置已保存到: {CONFIG_FILE}")
    
    return settings


if __name__ == "__main__":
    main()
