#!/usr/bin/env python3
"""
OpenClaw WhatsApp Monitor Skill 加载器
在 OpenClaw 启动时自动加载此技能
"""

import os
import sys
import json
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_skill_structure(skill_dir: Path) -> bool:
    """检查技能目录结构是否完整"""
    required_files = [
        "SKILL.md",
        "scripts/monitor.py",
        "scripts/config_manager.py",
        "scripts/whatsapp_client.py",
        "scripts/feishu_client.py",
        "scripts/message_processor.py",
        "config/whatsapp-targets.json",
        "config/feishu-settings.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = skill_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"缺少必要文件: {missing_files}")
        return False
    
    logger.info("技能目录结构完整")
    return True


def check_dependencies() -> bool:
    """检查 Python 依赖"""
    required_packages = [
        "aiohttp",
        "pydantic",
        "yaml",
        "requests",
        "python-dateutil"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少 Python 包: {missing_packages}")
        logger.info("请运行: pip install -r requirements.txt")
        return False
    
    logger.info("所有依赖包已安装")
    return True


def validate_configs(skill_dir: Path) -> bool:
    """验证配置文件"""
    configs_valid = True
    
    # 验证 WhatsApp 配置
    whatsapp_config_path = skill_dir / "config" / "whatsapp-targets.json"
    if whatsapp_config_path.exists():
        try:
            with open(whatsapp_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查必要字段
            if "targets" not in config:
                logger.error("whatsapp-targets.json 缺少 'targets' 字段")
                configs_valid = False
            else:
                logger.info(f"WhatsApp 配置有效: {len(config.get('targets', []))} 个目标")
        except json.JSONDecodeError as e:
            logger.error(f"whatsapp-targets.json JSON 格式错误: {e}")
            configs_valid = False
    else:
        logger.warning("whatsapp-targets.json 不存在，将使用默认配置")
    
    # 验证飞书配置
    feishu_config_path = skill_dir / "config" / "feishu-settings.json"
    if feishu_config_path.exists():
        try:
            with open(feishu_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查是否还是默认配置
            app_id = config.get("feishu", {}).get("app_id", "")
            if app_id == "YOUR_APP_ID" or not app_id:
                logger.warning("飞书配置仍为默认值，请更新 config/feishu-settings.json")
            else:
                logger.info("飞书配置有效")
        except json.JSONDecodeError as e:
            logger.error(f"feishu-settings.json JSON 格式错误: {e}")
            configs_valid = False
    else:
        logger.warning("feishu-settings.json 不存在，将使用默认配置")
    
    return configs_valid


def create_default_configs(skill_dir: Path) -> bool:
    """创建默认配置文件（如果不存在）"""
    config_dir = skill_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    # WhatsApp 默认配置
    whatsapp_config_path = config_dir / "whatsapp-targets.json"
    if not whatsapp_config_path.exists():
        default_whatsapp_config = {
            "version": "1.0",
            "targets": [
                {
                    "name": "示例工作群",
                    "type": "group",
                    "identifier": "请填写群聊ID",
                    "enabled": False,
                    "keywords": ["紧急", "截止", "会议", "问题", "帮忙"],
                    "keyword_patterns": [
                        "紧急.*",
                        ".*截止.*",
                        "会议.*[0-9]{1,2}:[0-9]{2}"
                    ],
                    "priority": "high"
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
        
        try:
            with open(whatsapp_config_path, 'w', encoding='utf-8') as f:
                json.dump(default_whatsapp_config, f, ensure_ascii=False, indent=2)
            logger.info(f"已创建默认 WhatsApp 配置: {whatsapp_config_path}")
        except Exception as e:
            logger.error(f"创建 WhatsApp 配置失败: {e}")
            return False
    
    # 飞书默认配置
    feishu_config_path = config_dir / "feishu-settings.json"
    if not feishu_config_path.exists():
        default_feishu_config = {
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
        
        try:
            with open(feishu_config_path, 'w', encoding='utf-8') as f:
                json.dump(default_feishu_config, f, ensure_ascii=False, indent=2)
            logger.info(f"已创建默认飞书配置: {feishu_config_path}")
        except Exception as e:
            logger.error(f"创建飞书配置失败: {e}")
            return False
    
    return True


def create_data_dirs(skill_dir: Path) -> bool:
    """创建数据目录"""
    data_dir = skill_dir / "data"
    logs_dir = skill_dir / "logs"
    
    try:
        data_dir.mkdir(exist_ok=True)
        logs_dir.mkdir(exist_ok=True)
        
        # 创建 .gitignore 文件防止提交数据
        gitignore_path = skill_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_content = """# 数据文件
data/
logs/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.env
*.log
"""
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
        
        logger.info("数据目录已创建")
        return True
    except Exception as e:
        logger.error(f"创建数据目录失败: {e}")
        return False


def register_with_openclaw(skill_dir: Path) -> bool:
    """
    注册技能到 OpenClaw
    注意：这需要根据 OpenClaw 的实际注册机制调整
    """
    try:
        # 这里应该是 OpenClaw 的技能注册逻辑
        # 由于 OpenClaw 的具体注册机制未知，这里只是示例
        
        # 检查是否在 OpenClaw 环境中
        openclaw_home = os.environ.get("OPENCLAW_HOME")
        if not openclaw_home:
            logger.info("未检测到 OpenClaw 环境，跳过注册")
            return True
        
        # 创建技能链接或注册文件
        # 实际实现需要根据 OpenClaw 的文档
        logger.info(f"技能目录: {skill_dir}")
        logger.info("技能已准备好，可在 OpenClaw 中使用")
        
        return True
    except Exception as e:
        logger.error(f"注册技能失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("WhatsApp Monitor Skill 加载器")
    print("=" * 60)
    
    # 获取技能目录
    script_dir = Path(__file__).parent
    skill_dir = script_dir
    
    logger.info(f"技能目录: {skill_dir}")
    
    # 步骤 1: 检查目录结构
    print("\n[1/5] 检查技能目录结构...")
    if not check_skill_structure(skill_dir):
        print("❌ 技能目录结构不完整")
        return False
    print("✅ 技能目录结构完整")
    
    # 步骤 2: 检查依赖
    print("\n[2/5] 检查 Python 依赖...")
    if not check_dependencies():
        print("❌ 依赖检查失败")
        return False
    print("✅ 所有依赖已安装")
    
    # 步骤 3: 创建默认配置（如果需要）
    print("\n[3/5] 检查配置文件...")
    if not create_default_configs(skill_dir):
        print("❌ 创建默认配置失败")
        return False
    
    if not validate_configs(skill_dir):
        print("⚠️ 配置验证有警告，但可以继续")
    else:
        print("✅ 配置文件有效")
    
    # 步骤 4: 创建数据目录
    print("\n[4/5] 创建数据目录...")
    if not create_data_dirs(skill_dir):
        print("❌ 创建数据目录失败")
        return False
    print("✅ 数据目录已创建")
    
    # 步骤 5: 注册到 OpenClaw
    print("\n[5/5] 注册到 OpenClaw...")
    if not register_with_openclaw(skill_dir):
        print("⚠️ 注册到 OpenClaw 有警告，但可以继续")
    else:
        print("✅ 技能已准备好")
    
    print("\n" + "=" * 60)
    print("WhatsApp Monitor Skill 加载完成！")
    print("\n下一步操作:")
    print("1. 编辑 config/whatsapp-targets.json 配置监控目标")
    print("2. 编辑 config/feishu-settings.json 配置飞书凭证")
    print("3. 运行 'python scripts/monitor.py --test-config' 测试配置")
    print("4. 运行 'python scripts/monitor.py --start' 启动监控")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"加载器运行失败: {e}", exc_info=True)
        sys.exit(1)