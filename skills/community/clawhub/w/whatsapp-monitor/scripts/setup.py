#!/usr/bin/env python3
"""
WhatsApp Monitor 安装和配置脚本
"""

import json
import os
import sys
import logging
from pathlib import Path


def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def create_directory_structure(base_dir: str = "."):
    """创建目录结构"""
    logger = setup_logging()
    
    directories = [
        "config",
        "data",
        "logs",
        "scripts"
    ]
    
    for directory in directories:
        dir_path = Path(base_dir) / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"创建目录: {dir_path}")
    
    return True


def create_default_configs(config_dir: str = "config"):
    """创建默认配置文件"""
    logger = setup_logging()
    
    config_dir_path = Path(config_dir)
    
    # WhatsApp 配置
    whatsapp_config = {
        "version": "1.0",
        "targets": [
            {
                "name": "示例工作群",
                "type": "group",
                "identifier": "工作群聊的ID或名称",
                "enabled": False,
                "keywords": ["紧急", "截止", "会议", "问题", "帮忙"],
                "keyword_patterns": [
                    r"紧急.*",
                    r".*截止.*",
                    r"会议.*[0-9]{1,2}:[0-9]{2}"
                ],
                "priority": "high"
            },
            {
                "name": "示例项目群",
                "type": "group",
                "identifier": "项目群聊的ID或名称",
                "enabled": False,
                "keywords": ["状态", "进度", "测试", "部署", "里程碑"],
                "keyword_patterns": [
                    r"进度.*%",
                    r"测试.*通过",
                    r"部署.*完成"
                ],
                "priority": "medium"
            }
        ],
        "monitoring": {
            "scan_interval_minutes": 5,
            "batch_size": 10,
            "max_age_hours": 24,
            "alert_on_high_priority": True,
            "include_context_messages": 2
        }
    }
    
    # 飞书配置
    feishu_config = {
        "feishu": {
            "app_id": "YOUR_APP_ID",
            "app_secret": "YOUR_APP_SECRET",
            "tenant_access_token": "",
            "table_app_token": "YOUR_TABLE_APP_TOKEN",
            "table_token": "YOUR_TABLE_TOKEN"
        },
        "table": {
            "name": "WhatsApp 消息监控日志",
            "fields": [
                {"field_name": "timestamp", "type": 5, "property": {"date_format": "yyyy-MM-dd HH:mm:ss"}},
                {"field_name": "source", "type": 1},
                {"field_name": "sender", "type": 1},
                {"field_name": "message_content", "type": 1},
                {"field_name": "keyword_matched", "type": 1},
                {"field_name": "priority", "type": 3},
                {"field_name": "message_type", "type": 1},
                {"field_name": "attachment", "type": 1},
                {"field_name": "chat_link", "type": 1}
            ]
        },
        "export": {
            "batch_threshold": 10,
            "schedule": "every 30 minutes",
            "retry_on_failure": True,
            "max_retries": 3,
            "timeout_seconds": 30
        }
    }
    
    # 保存配置文件
    try:
        whatsapp_config_path = config_dir_path / "whatsapp-targets.json"
        with open(whatsapp_config_path, 'w', encoding='utf-8') as f:
            json.dump(whatsapp_config, f, ensure_ascii=False, indent=2)
        logger.info(f"已创建 WhatsApp 配置: {whatsapp_config_path}")
        
        feishu_config_path = config_dir_path / "feishu-settings.json"
        with open(feishu_config_path, 'w', encoding='utf-8') as f:
            json.dump(feishu_config, f, ensure_ascii=False, indent=2)
        logger.info(f"已创建飞书配置: {feishu_config_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"创建配置文件失败: {str(e)}")
        return False


def create_requirements_file(base_dir: str = "."):
    """创建 requirements.txt 文件"""
    logger = setup_logging()
    
    requirements = """# WhatsApp Monitor 依赖包
aiohttp>=3.8.0
pydantic>=2.0.0
python-dateutil>=2.8.0
requests>=2.28.0
pyyaml>=6.0
"""
    
    try:
        req_path = Path(base_dir) / "requirements.txt"
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write(requirements)
        logger.info(f"已创建 requirements.txt: {req_path}")
        return True
    except Exception as e:
        logger.error(f"创建 requirements.txt 失败: {str(e)}")
        return False


def create_readme_file(base_dir: str = "."):
    """创建 README.md 文件"""
    logger = setup_logging()
    
    readme_content = """# WhatsApp Monitor Skill

## 概述

这是一个 OpenClaw Skill，用于实时监控 WhatsApp 消息，根据关键词过滤，并将匹配的消息批量导出到飞书多维表格。

## 功能特性

- ✅ 实时监控 WhatsApp 个人聊天和群聊
- ✅ 支持关键词和正则表达式匹配
- ✅ 消息批量处理，避免频繁 API 调用
- ✅ 飞书多维表格自动导出
- ✅ 可配置的监控目标和优先级
- ✅ 详细的日志记录和错误处理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 1. WhatsApp 配置

编辑 `config/whatsapp-targets.json`：

```json
{
  "targets": [
    {
      "name": "工作团队群",
      "type": "group",
      "identifier": "群聊ID或名称",
      "enabled": true,
      "keywords": ["紧急", "截止", "问题"],
      "keyword_patterns": ["紧急.*", ".*截止.*"],
      "priority": "high"
    }
  ],
  "monitoring": {
    "scan_interval_minutes": 5,
    "batch_size": 10
  }
}
```

### 2. 飞书配置

编辑 `config/feishu-settings.json`：

```json
{
  "feishu": {
    "app_id": "你的飞书应用ID",
    "app_secret": "你的飞书应用密钥",
    "table_app_token": "多维表格应用token",
    "table_token": "表格token"
  }
}
```

### 3. 获取飞书凭证

1. 登录飞书开放平台：https://open.feishu.cn/
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 开启「多维表格」权限
5. 创建多维表格并获取 Table Token

## 使用方法

### 启动监控

```bash
python scripts/monitor.py --start
```

### 查看状态

```bash
python scripts/monitor.py --status
```

### 测试配置

```bash
python scripts/monitor.py --test-config
```

### 强制导出

```bash
python scripts/monitor.py --export
```

## OpenClaw 集成

### 作为 Skill 使用

1. 将本目录复制到 OpenClaw skills 目录
2. 在 OpenClaw 中加载技能
3. 使用技能命令进行配置和监控

### 自动运行

可以通过 OpenClaw 的 cron 功能定时运行监控：

```yaml
schedule: "*/5 * * * *"  # 每5分钟运行一次
```

## 文件结构

```
whatsapp-monitor/
├── config/                    # 配置文件
│   ├── whatsapp-targets.json  # WhatsApp 监控配置
│   └── feishu-settings.json   # 飞书集成配置
├── scripts/                   # 脚本文件
│   ├── monitor.py            # 主监控脚本
│   ├── config_manager.py     # 配置管理
│   ├── whatsapp_client.py    # WhatsApp 客户端
│   ├── feishu_client.py      # 飞书客户端
│   └── message_processor.py  # 消息处理器
├── data/                     # 数据存储
│   └── matched_messages.json # 匹配的消息缓存
├── logs/                     # 日志文件
├── requirements.txt          # Python 依赖
└── README.md                # 说明文档
```

## 故障排除

### 常见问题

1. **WhatsApp 连接失败**
   - 确保 OpenClaw WhatsApp 渠道已配置
   - 检查设备是否已配对

2. **飞书 API 错误**
   - 验证 App ID 和 App Secret
   - 检查多维表格权限
   - 确认 Table Token 正确

3. **关键词不匹配**
   - 检查关键词拼写
   - 验证正则表达式语法
   - 查看消息内容格式

### 日志查看

```bash
tail -f logs/whatsapp-monitor.log
```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持 WhatsApp 消息监控
- 支持飞书多维表格导出
- 可配置关键词和正则匹配

## 许可证

MIT License
"""
    
    try:
        readme_path = Path(base_dir) / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        logger.info(f"已创建 README.md: {readme_path}")
        return True
    except Exception as e:
        logger.error(f"创建 README.md 失败: {str(e)}")
        return False


def setup_skill():
    """安装技能"""
    logger = setup_logging()
    
    logger.info("开始安装 WhatsApp Monitor Skill...")
    
    # 获取当前目录
    current_dir = Path(__file__).parent.parent
    
    # 创建目录结构
    if not create_directory_structure(current_dir):
        logger.error("创建目录结构失败")
        return False
    
    # 创建配置文件
    if not create_default_configs(current_dir / "config"):
        logger.error("创建配置文件失败")
        return False
    
    # 创建 requirements.txt
    if not create_requirements_file(current_dir):
        logger.error("创建 requirements.txt 失败")
        return False
    
    # 创建 README.md
    if not create_readme_file(current_dir):
        logger.error("创建 README.md 失败")
        return False
    
    logger.info("✅ WhatsApp Monitor Skill 安装完成！")
    logger.info("")
    logger.info("📋 下一步操作：")
    logger.info("1. 编辑 config/whatsapp-targets.json 配置监控目标")
    logger.info("2. 编辑 config/feishu-settings.json 配置飞书凭证")
    logger.info("3. 运行 'pip install -r requirements.txt' 安装依赖")
    logger.info("4. 运行 'python scripts/monitor.py --test-config' 测试配置")
    logger.info("5. 运行 'python scripts/monitor.py --start' 启动监控")
    logger.info("")
    logger.info("💡 提示：请确保 OpenClaw WhatsApp 渠道已正确配置并配对设备")
    
    return True


if __name__ == "__main__":
    setup_skill()