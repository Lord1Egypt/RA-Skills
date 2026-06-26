#!/usr/bin/env python3
"""
小度设备控制技能初始化脚本
"""

import os
import sys
import json
from pathlib import Path

def create_skill_structure(skill_path):
    """创建技能目录结构"""
    skill_path = Path(skill_path)
    
    # 创建目录
    directories = [
        skill_path,
        skill_path / "scripts",
        skill_path / "references",
        skill_path / "assets"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    return skill_path

def create_skill_md(skill_path):
    """创建SKILL.md文件"""
    skill_md_content = """---
name: xiaodu-control
description: 小度智能设备控制技能。用于控制小度音箱、IoT设备、查看设备列表、语音播报等。当用户需要控制小度智能设备、查询设备状态、发送语音指令或管理智能家居时使用此技能。
---

# 小度智能设备控制技能

## 概述

此技能提供对小度智能设备的全面控制能力，包括：
- 小度音箱设备控制（语音指令、播报）
- IoT设备控制（灯光、窗帘、开关等）
- 设备列表查看和状态监控
- 语音播报和消息推送

## 快速开始

### 1. 查看设备列表
```bash
# 查看小度音箱设备
mcporter call xiaodu.list_user_devices

# 查看IoT设备
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS
```

### 2. 控制设备
```bash
# 发送语音指令
mcporter call xiaodu.control_xiaodu command="现在几点了？" cuid="YOUR_DEVICE_CUID" client_id="YOUR_CLIENT_ID"

# 控制灯光
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES action="turnOn" applianceName="书桌灯" roomName="客厅"
```

### 3. 使用脚本
```bash
# 更新设备列表
./scripts/update_devices.sh

# 语音播报
./scripts/speak_message.sh "你好，我是AI助手"

# 批量控制
./scripts/batch_control.sh turnOn "书桌灯 走廊灯"
```

## 详细文档

- [小度音箱MCP配置](references/xiaodu_mcp.md)
- [IoT设备控制API](references/iot_api.md)
- [设备管理最佳实践](references/device_management.md)
- [故障排除手册](references/troubleshooting.md)

## 脚本说明

### update_devices.sh
自动更新小度音箱和IoT设备列表，保存到工作空间文件。

### speak_message.sh
向指定的小度设备发送语音播报，支持预定义设备和自定义设备。

### batch_control.sh
批量控制多个IoT设备，支持灯光、窗帘、开关等设备。

## 配置要求

1. **MCP服务器配置**: 已配置小度音箱和IoT的MCP服务器
2. **Access Token**: 有效的百度DuerOS access_token
3. **设备发现**: 已运行设备发现脚本获取设备列表

## 支持的功能

### ✅ 已实现
- 小度音箱语音控制
- IoT设备开关控制
- 设备列表自动更新
- 语音播报功能
- 批量设备控制

### 🔄 计划中
- 设备状态监控
- 自动化场景
- 语音识别集成
- 多用户支持

## 故障排除

常见问题及解决方案请参考 [故障排除手册](references/troubleshooting.md)。

## 更新日志

- **v1.0.0** (2026-02-13): 初始版本发布
  - 基础设备控制功能
  - 实用脚本工具
  - 完整文档支持

## 贡献指南

欢迎提交问题和改进建议。请确保：
1. 代码符合现有风格
2. 包含适当的测试
3. 更新相关文档

## 许可证

MIT License
"""
    
    skill_md_path = skill_path / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding='utf-8')
    print(f"✅ 创建文件: {skill_md_path}")
    
    return skill_md_path

def create_example_files(skill_path):
    """创建示例文件"""
    
    # 创建示例设备列表
    example_devices = """书桌灯
走廊灯
面板灯
厨房灯
主卧布帘
次卧纱帘
"""
    
    devices_file = skill_path / "examples" / "devices.txt"
    devices_file.parent.mkdir(exist_ok=True)
    devices_file.write_text(example_devices, encoding='utf-8')
    print(f"✅ 创建示例文件: {devices_file}")
    
    # 创建配置示例
    config_example = {
        "mcpServers": {
            "xiaodu": {
                "url": "https://xiaodu.baidu.com/dueros_mcp_server/mcp/",
                "headers": {
                    "ACCESS_TOKEN": "your_access_token_here"
                }
            },
            "xiaodu-iot": {
                "command": "npx",
                "args": ["-y", "dueros-iot-mcp"],
                "env": {
                    "ACCESS_TOKEN": "your_access_token_here"
                }
            }
        }
    }
    
    config_file = skill_path / "examples" / "mcporter_config.json"
    config_file.write_text(json.dumps(config_example, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ 创建示例文件: {config_file}")
    
    return [devices_file, config_file]

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python init_skill.py <技能路径>")
        print("示例: python init_skill.py ./xiaodu-control")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    print(f"开始创建小度设备控制技能: {skill_path}")
    print("=" * 50)
    
    try:
        # 创建技能结构
        skill_dir = create_skill_structure(skill_path)
        
        # 创建SKILL.md
        create_skill_md(skill_dir)
        
        # 创建示例文件
        create_example_files(skill_dir)
        
        print("=" * 50)
        print("✅ 技能创建完成！")
        print(f"技能路径: {skill_dir.absolute()}")
        print("")
        print("下一步:")
        print("1. 配置MCP服务器访问令牌")
        print("2. 运行 update_devices.sh 获取设备列表")
        print("3. 测试设备控制功能")
        print("4. 根据实际需求调整脚本")
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()