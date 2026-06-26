#!/usr/bin/env python3
"""
hardware_detector.py - 硬件能力检测
自动检测CPU特性，选择最优执行路径
"""
import platform
import os


def detect_cpu_features():
    """检测CPU特性"""
    features = {
        "platform": platform.system(),
        "processor": platform.processor(),
        "machine": platform.machine(),
    }
    
    # Linux CPU特性检测
    if features["platform"] == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                cpuinfo = f.read()
                
            # 特性检测
            features["avx512"] = "avx512" in cpuinfo.lower()
            features["avx2"] = "avx" in cpuinfo.lower()
            features["vnni"] = "vnni" in cpuinfo.lower()
            features["amx"] = "amx" in cpuinfo.lower() or "intel_amx" in cpuinfo.lower()
            features["neon"] = "neon" in cpuinfo.lower()
            features["sve"] = "sve" in cpuinfo.lower()
            
            # 核心数
            cores = cpuinfo.count("processor")
            features["cores"] = cores
        except:
            pass
    
    # macOS检测
    elif features["platform"] == "Darwin":
        import subprocess
        try:
            result = subprocess.run(
                ["sysctl", "-a"],
                capture_output=True,
                text=True,
                timeout=10  # 超时保护
            )
            sysctl = result.stdout.lower()
            features["avx512"] = "avx512" in sysctl
            features["neon"] = "neon" in sysctl
        except:
            pass
    
    # Windows/WSL检测
    else:
        features["avx512"] = False
        features["avx2"] = False
        features["vnni"] = False
        features["amx"] = False
        features["neon"] = False
    
    return features


def get_optimization_level(features):
    """根据硬件特性返回优化级别"""
    if features.get("amx"):
        return {
            "level": "MAX",
            "vector_method": "AMX",
            "description": "Intel AMX - 最强性能"
        }
    elif features.get("avx512"):
        return {
            "level": "HIGH",
            "vector_method": "AVX512",
            "description": "AVX512 - 高性能"
        }
    elif features.get("vnni"):
        return {
            "level": "MEDIUM",
            "vector_method": "VNNI",
            "description": "VNNI - 中等性能"
        }
    elif features.get("avx2"):
        return {
            "level": "BASIC",
            "vector_method": "AVX2",
            "description": "AVX2 - 基础优化"
        }
    elif features.get("neon"):
        return {
            "level": "MOBILE",
            "vector_method": "NEON",
            "description": "NEON - 移动端优化"
        }
    else:
        return {
            "level": "FALLBACK",
            "vector_method": "PURE_PYTHON",
            "description": "纯Python - 兼容性优先"
        }


def main():
    print("🔍 硬件能力检测")
    print("=" * 40)
    
    features = detect_cpu_features()
    
    print(f"\n📋 平台信息:")
    print(f"  系统: {features.get('platform', 'Unknown')}")
    print(f"  架构: {features.get('machine', 'Unknown')}")
    print(f"  处理器: {features.get('processor', 'Unknown')}")
    print(f"  核心数: {features.get('cores', 'Unknown')}")
    
    print(f"\n⚡ 硬件加速特性:")
    print(f"  AVX512: {'✅ 支持' if features.get('avx512') else '❌ 不支持'}")
    print(f"  AVX2: {'✅ 支持' if features.get('avx2') else '❌ 不支持'}")
    print(f"  VNNI: {'✅ 支持' if features.get('vnni') else '❌ 不支持'}")
    print(f"  AMX: {'✅ 支持' if features.get('amx') else '❌ 不支持'}")
    print(f"  NEON: {'✅ 支持' if features.get('neon') else '❌ 不支持'}")
    
    opt = get_optimization_level(features)
    print(f"\n🎯 推荐优化级别: {opt['level']}")
    print(f"  向量方法: {opt['vector_method']}")
    print(f"  说明: {opt['description']}")
    
    return features


if __name__ == "__main__":
    main()
