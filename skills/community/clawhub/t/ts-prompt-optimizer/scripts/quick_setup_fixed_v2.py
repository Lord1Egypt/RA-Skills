#!/usr/bin/env python3
"""
快速安装脚本 - 为冬冬主人创建TS-Prompt-Optimizer配置文件
"""

import os
import yaml
import json
from pathlib import Path


def create_config_for_dongdong():
    """为冬冬主人创建配置文件"""
    
    # 配置文件目录
    user_config_dir = Path.home() / ".openclaw"
    user_config_dir.mkdir(exist_ok=True)
    
    config_file = user_config_dir / "ts-optimizer-config.yaml"
    
    # 从环境变量获取API密钥
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
    bailian_key = os.getenv("BAILIAN_API_KEY", "")
    
    # 创建配置
    config = {
        "version": "1.0",
        "created_for": "陈冬冬",
        "created_at": "2026-04-04",
        
        "models": {
            "deepseek": {
                "provider": "deepseek",
                "model": "deepseek-chat",
                "api_key": deepseek_key,
                "enabled": True,
                "priority": 1,
                "cost_per_1k_tokens": 0.42,
                "capabilities": [
                    "日常对话",
                    "简单优化",
                    "代码审查",
                    "基础分析"
                ]
            },
            "qwen35": {
                "provider": "bailian",
                "model": "qwen3.5-plus",
                "api_key": bailian_key,
                "enabled": True,
                "priority": 2,
                "cost_per_1k_tokens": 0.00,
                "capabilities": [
                    "复杂任务",
                    "图像识别",
                    "中文写作",
                    "深度分析"
                ]
            },
            "qwen_coder": {
                "provider": "bailian",
                "model": "qwen3-coder-next",
                "api_key": bailian_key,
                "enabled": True,
                "priority": 3,
                "cost_per_1k_tokens": 0.00,
                "capabilities": [
                    "技术开发",
                    "代码生成",
                    "系统设计",
                    "算法实现"
                ]
            }
        },
        
        "routing": {
            "strategy": "cost_effective",
            "fallback_model": "deepseek",
            "cost_threshold": 1.00
        },
        
        "user_preferences": {
            "default_optimization_level": "standard",
            "show_config_summary": True,
            "auto_test_connections": True,
            "preferred_output_formats": {
                "code": "完整代码 + 注释 + 测试",
                "report": "Markdown + 数据可视化",
                "email": "正式商务邮件格式"
            }
        },
        
        "integration": {
            "with_smart_router": True,
            "auto_detect_prefix": True,
            "prefixes": ["ts:", "ts-opt:", "优化:"],
            "learning_enabled": True,
            "feedback_mechanism": True
        }
    }
    
    # 写入配置文件
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"配置文件已创建: {config_file}")
    
    # 检查API密钥配置状态
    configured_models = 0
    total_models = 0
    
    for model_id, model_info in config["models"].items():
        total_models += 1
        if model_info.get("api_key"):
            configured_models += 1
    
    print(f"模型配置状态: {configured_models}/{total_models} 个模型已配置API密钥")
    
    if configured_models < total_models:
        print("提示: 请设置以下环境变量:")
        if not deepseek_key:
            print("  export DEEPSEEK_API_KEY=您的DeepSeek密钥")
        if not bailian_key:
            print("  export BAILIAN_API_KEY=您的千问密钥")
        print("或运行: ts-config setup 进行交互式配置")
    
    return config_file


def main():
    print("=" * 60)
    print("TS-Prompt-Optimizer 快速安装")
    print("=" * 60)
    
    try:
        config_file = create_config_for_dongdong()
        
        print()
        print("安装完成！")
        print("下一步操作:")
        print("1. 设置API密钥环境变量")
        print("2. 运行: ts-config status 检查配置状态")
        print("3. 运行: ts-config test 测试模型连接")
        print("4. 在对话中使用 'ts:' 前缀触发优化")
        
    except Exception as e:
        print(f"安装失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())