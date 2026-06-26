#!/usr/bin/env python3
"""
非交互式 .env 配置工具。供外部 agent 调用。

用法:
    python selfskill/scripts/configure.py <KEY> <VALUE>          # 设置单个配置项
    python selfskill/scripts/configure.py --show                 # 显示当前配置（隐藏敏感值）
    python selfskill/scripts/configure.py --show-raw             # 显示当前配置（含原始值）
    python selfskill/scripts/configure.py --init                 # 从 .env.example 初始化 .env（不覆盖已有）
    python selfskill/scripts/configure.py --batch K1=V1 K2=V2    # 批量设置

示例:
    python skill/scripts/configure.py LLM_API_KEY sk-xxxx
    python skill/scripts/configure.py LLM_BASE_URL https://api.deepseek.com
    python skill/scripts/configure.py LLM_MODEL deepseek-chat
    python skill/scripts/configure.py --batch LLM_API_KEY=sk-xxx LLM_BASE_URL=https://api.deepseek.com LLM_MODEL=deepseek-chat
"""
import os
import re
import sys
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")
ENV_EXAMPLE = os.path.join(PROJECT_ROOT, "config", ".env.example")

SENSITIVE_KEYS = {"LLM_API_KEY", "INTERNAL_TOKEN", "TELEGRAM_BOT_TOKEN", "QQ_BOT_SECRET"}

# 合法的环境变量key列表（基于SKILL.md文档）
VALID_KEYS = {
    # LLM配置
    "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL", "LLM_PROVIDER", "LLM_VISION_SUPPORT",
    # 端口配置
    "PORT_AGENT", "PORT_SCHEDULER", "PORT_OASIS", "PORT_FRONTEND", "PORT_BARK",
    # TTS配置
    "TTS_MODEL", "TTS_VOICE",
    # OpenClaw配置
    "OPENCLAW_API_URL", "OPENCLAW_API_KEY", "OPENCLAW_SESSIONS_FILE",
    # 内部配置
    "INTERNAL_TOKEN", "OPENAI_STANDARD_MODE",
    # 命令执行配置
    "ALLOWED_COMMANDS", "EXEC_TIMEOUT", "MAX_OUTPUT_LENGTH",
    # 服务配置
    "OASIS_BASE_URL", "PUBLIC_DOMAIN", "BARK_PUBLIC_URL",
    # 聊天机器人配置
    "TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_USERS", "QQ_APP_ID", "QQ_BOT_SECRET", 
    "QQ_BOT_USERNAME", "AI_MODEL_TG", "AI_MODEL_QQ", "AI_API_URL"
}


def validate_key(key):
    """验证key是否合法"""
    if key not in VALID_KEYS:
        print(f"❌ 错误: '{key}' 不是合法的配置项")
        print(f"   支持的配置项: {', '.join(sorted(VALID_KEYS))}")
        return False
    return True


def read_env():
    """读取 .env 为 (行列表, {key: value} 字典)"""
    if not os.path.exists(ENV_PATH):
        return [], {}
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    kvs = {}
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            k, v = s.split("=", 1)
            kvs[k.strip()] = v.strip()
    return lines, kvs


def set_env_with_validation(key, value):
    """设置单个 key=value，包含合法性检查和详细回显"""
    # 验证key合法性
    if not validate_key(key):
        return False
    
    # 设置环境变量
    lines, _ = read_env()
    key_found = False
    new_lines = []
    for line in lines:
        s = line.strip()
        if s.startswith(f"{key}=") or s.startswith(f"# {key}="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)
    if not key_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"{key}={value}\n")
    
    os.makedirs(os.path.dirname(ENV_PATH), exist_ok=True)
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    # 详细回显设置内容
    display_value = value[:4] + "****" + value[-4:] if key in SENSITIVE_KEYS and len(value) > 8 else value
    print(f"✅ {key}={display_value} 已设置")
    print(f"📁 配置文件: {ENV_PATH}")
    
    return True


def set_env(key, value):
    """设置单个 key=value，如果 key 已存在则更新，否则追加（兼容旧版本）"""
    return set_env_with_validation(key, value)


def show_env(raw=False):
    """显示当前配置，包含详细回显"""
    _, kvs = read_env()
    if not kvs:
        print("⚠️  config/.env 不存在或为空")
        return
    
    print(f"📁 配置文件: {ENV_PATH}")
    print(f"📊 当前配置项数量: {len(kvs)}")
    print("=" * 60)
    
    for k, v in kvs.items():
        # 验证key的合法性
        is_valid = k in VALID_KEYS
        validity_indicator = "✅" if is_valid else "⚠️"
        
        if not raw and k in SENSITIVE_KEYS and v:
            display = v[:4] + "****" + v[-4:] if len(v) > 8 else "****"
        else:
            display = v
        
        print(f"{validity_indicator} {k}={display}")
        if not is_valid:
            print(f"   ⚠️ 注意: '{k}' 不是标准配置项，请检查拼写")
    
    print("=" * 60)
    print(f"💡 提示: 使用 '--show-raw' 查看原始值（包含敏感信息）")


def init_env():
    """从 .env.example 初始化 .env（不覆盖已有）"""
    if os.path.exists(ENV_PATH):
        print(f"✅ config/.env 已存在，跳过初始化")
        return
    if not os.path.exists(ENV_EXAMPLE):
        print(f"❌ config/.env.example 不存在", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(ENV_PATH), exist_ok=True)
    shutil.copy2(ENV_EXAMPLE, ENV_PATH)
    print(f"✅ 已从 .env.example 初始化 config/.env")


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--show":
        show_env(raw=False)
    elif cmd == "--show-raw":
        show_env(raw=True)
    elif cmd == "--init":
        init_env()
    elif cmd == "--batch":
        if len(sys.argv) < 3:
            print("用法: configure.py --batch KEY1=VAL1 KEY2=VAL2 ...", file=sys.stderr)
            sys.exit(1)
        
        print("🔧 批量配置开始...")
        print(f"📁 配置文件: {ENV_PATH}")
        print("-" * 60)
        
        success_count = 0
        total_count = len(sys.argv[2:])
        
        for arg in sys.argv[2:]:
            if "=" not in arg:
                print(f"❌ 跳过无效参数: {arg}", file=sys.stderr)
                continue
            k, v = arg.split("=", 1)
            k = k.strip()
            v = v.strip()
            
            if set_env_with_validation(k, v):
                success_count += 1
        
        print("-" * 60)
        print(f"📊 批量配置完成: {success_count}/{total_count} 项成功设置")
        if success_count < total_count:
            print(f"⚠️  有 {total_count - success_count} 项配置失败，请检查key名称是否正确")
    else:
        # 单个 KEY VALUE
        if len(sys.argv) != 3:
            print("用法: configure.py <KEY> <VALUE>", file=sys.stderr)
            sys.exit(1)
        
        key = sys.argv[1]
        value = sys.argv[2]
        
        print("🔧 单个配置开始...")
        print(f"📁 配置文件: {ENV_PATH}")
        print("-" * 60)
        
        if set_env_with_validation(key, value):
            print("-" * 60)
            print("✅ 配置完成")
        else:
            print("-" * 60)
            print("❌ 配置失败，请检查key名称是否正确")
            sys.exit(1)


if __name__ == "__main__":
    main()
