#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云语音合成配置模板
提供API密钥配置、环境设置和安全最佳实践指导
"""

import os
import sys
from typing import Dict, Optional


class ConfigManager:
    """配置管理器类"""
    
    # 必需的配置项
    REQUIRED_CONFIGS = [
        "TENCENTCLOUD_SECRET_ID",
        "TENCENTCLOUD_SECRET_KEY"
    ]
    
    # 可选的配置项
    OPTIONAL_CONFIGS = {
        "TENCENTCLOUD_REGION": "ap-guangzhou",  # 默认区域
        "TENCENTCLOUD_TOKEN": "",  # 临时令牌
        "TTS_DEFAULT_VOICE_TYPE": "101001",  # 默认语音类型
        "TTS_DEFAULT_CODEC": "mp3",  # 默认音频格式
        "TTS_DEFAULT_OUTPUT_DIR": "./output"  # 默认输出目录
    }
    
    @classmethod
    def validate_configuration(cls) -> Dict[str, bool]:
        """验证配置是否完整"""
        validation_results = {}
        
        for config_name in cls.REQUIRED_CONFIGS:
            value = os.getenv(config_name)
            validation_results[config_name] = bool(value and value.strip())
        
        return validation_results
    
    @classmethod
    def get_config_status(cls) -> Dict[str, any]:
        """获取配置状态报告"""
        validation = cls.validate_configuration()
        
        status = {
            "is_valid": all(validation.values()),
            "missing_configs": [k for k, v in validation.items() if not v],
            "available_configs": {},
            "recommendations": []
        }
        
        # 检查所有配置项
        for config_name in cls.REQUIRED_CONFIGS + list(cls.OPTIONAL_CONFIGS.keys()):
            value = os.getenv(config_name)
            if value:
                status["available_configs"][config_name] = value[:10] + "..." if len(value) > 10 else value
            else:
                status["available_configs"][config_name] = "未设置"
        
        # 生成建议
        if not status["is_valid"]:
            status["recommendations"].append("请设置缺失的必需配置项")
        
        if not os.getenv("TTS_DEFAULT_OUTPUT_DIR"):
            status["recommendations"].append("建议设置输出目录以避免文件混乱")
        
        return status
    
    @classmethod
    def generate_env_template(cls) -> str:
        """生成环境变量模板文件内容"""
        template = """# 腾讯云语音合成服务环境配置
# 请将本文件保存为 .env 文件，并根据实际情况修改配置值

# ===== 必需配置项 =====
# 腾讯云API密钥 - 请从腾讯云控制台获取
TENCENTCLOUD_SECRET_ID="your-secret-id-here"
TENCENTCLOUD_SECRET_KEY="your-secret-key-here"

# ===== 可选配置项 =====
# 服务区域（默认：ap-guangzhou）
TENCENTCLOUD_REGION="ap-guangzhou"

# 临时令牌（如使用临时密钥）
TENCENTCLOUD_TOKEN=""

# ===== 语音合成默认配置 =====
# 默认语音类型（101001-101015）
TTS_DEFAULT_VOICE_TYPE="101001"

# 默认音频格式（mp3/wav）
TTS_DEFAULT_CODEC="mp3"

# 默认输出目录
TTS_DEFAULT_OUTPUT_DIR="./audio_output"

# ===== 高级配置 =====
# 请求超时时间（秒）
TTS_REQUEST_TIMEOUT="30"

# 重试次数
TTS_MAX_RETRIES="3"

# 日志级别（DEBUG/INFO/WARNING/ERROR）
TTS_LOG_LEVEL="INFO"
"""
        return template


def setup_environment():
    """环境设置向导"""
    print("=== 腾讯云语音合成环境设置向导 ===\n")
    
    # 检查当前配置状态
    status = ConfigManager.get_config_status()
    
    print("📊 当前配置状态:")
    for config_name, value in status["available_configs"].items():
        icon = "✅" if value != "未设置" else "❌"
        print(f"   {icon} {config_name}: {value}")
    
    print(f"\n🔍 配置完整性: {'✅ 完整' if status['is_valid'] else '❌ 不完整'}")
    
    if not status["is_valid"]:
        print(f"\n⚠️  缺失的必需配置:")
        for missing in status["missing_configs"]:
            print(f"   • {missing}")
    
    if status["recommendations"]:
        print(f"\n💡 建议:")
        for rec in status["recommendations"]:
            print(f"   • {rec}")
    
    return status


def generate_config_files():
    """生成配置文件"""
    print("\n=== 生成配置文件 ===\n")
    
    # 生成.env文件模板
    env_content = ConfigManager.generate_env_template()
    
    env_file_path = ".env.template"
    with open(env_file_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print(f"✅ 已生成环境变量模板: {env_file_path}")
    print("💡 使用方法:")
    print("   1. 复制 .env.template 为 .env")
    print("   2. 编辑 .env 文件，填入实际的API密钥")
    print("   3. 运行: source .env")
    
    # 生成配置检查脚本
    check_script = """#!/usr/bin/env python3
# 配置检查脚本

import os
from config_template import ConfigManager

if __name__ == "__main__":
    status = ConfigManager.get_config_status()
    
    if status["is_valid"]:
        print("✅ 配置检查通过！可以正常使用语音合成服务。")
    else:
        print("❌ 配置检查失败！")
        print("缺失的配置项:")
        for missing in status["missing_configs"]:
            print(f"  - {missing}")
        print("\n请检查 .env 文件配置。")
"""
    
    check_script_path = "check_config.py"
    with open(check_script_path, "w", encoding="utf-8") as f:
        f.write(check_script)
    
    print(f"✅ 已生成配置检查脚本: {check_script_path}")
    print("💡 使用方法: python check_config.py")


def security_best_practices():
    """安全最佳实践指南"""
    print("\n=== 安全最佳实践 ===\n")
    
    practices = [
        {
            "title": "密钥管理",
            "description": "不要将API密钥硬编码在代码中",
            "good": "使用环境变量或密钥管理服务",
            "bad": "secret_key = 'your-key-here'"
        },
        {
            "title": "权限控制",
            "description": "使用最小权限原则",
            "good": "仅为语音合成服务授权",
            "bad": "使用拥有所有权限的根密钥"
        },
        {
            "title": "配置文件",
            "description": "保护配置文件安全",
            "good": ".env文件加入.gitignore",
            "bad": "将包含密钥的文件提交到版本控制"
        },
        {
            "title": "临时令牌",
            "description": "生产环境使用临时令牌",
            "good": "使用STS服务获取临时令牌",
            "bad": "长期使用固定密钥"
        },
        {
            "title": "监控审计",
            "description": "监控API使用情况",
            "good": "定期检查API调用日志",
            "bad": "不监控异常调用行为"
        }
    ]
    
    for practice in practices:
        print(f"🔒 {practice['title']}")
        print(f"   📝 {practice['description']}")
        print(f"   ✅ 推荐: {practice['good']}")
        print(f"   ❌ 避免: {practice['bad']}")
        print()


def api_key_guide():
    """API密钥获取指南"""
    print("\n=== API密钥获取指南 ===\n")
    
    steps = [
        "1. 登录腾讯云控制台: https://console.cloud.tencent.com",
        "2. 进入『访问管理』->『API密钥管理』",
        "3. 点击『新建密钥』创建新的SecretId和SecretKey",
        "4. 复制生成的密钥到.env文件中",
        "5. 确保已开通语音合成(TTS)服务",
        "6. 可选：为密钥添加描述和权限限制"
    ]
    
    print("📋 获取步骤:")
    for step in steps:
        print(f"   {step}")
    
    print("\n⚠️  注意事项:")
    print("   • 妥善保管SecretKey，一旦泄露请立即删除")
    print("   • 定期轮换密钥以提高安全性")
    print("   • 为不同环境使用不同的密钥")


if __name__ == "__main__":
    # 运行环境设置向导
    setup_environment()
    
    # 生成配置文件
    generate_config_files()
    
    # 显示安全最佳实践
    security_best_practices()
    
    # 显示API密钥获取指南
    api_key_guide()
    
    print("\n=== 配置向导完成 ===")
    print("💡 接下来请:")
    print("   1. 按照指南获取腾讯云API密钥")
    print("   2. 配置.env文件")
    print("   3. 运行配置检查脚本验证设置")
    print("   4. 开始使用语音合成服务！")