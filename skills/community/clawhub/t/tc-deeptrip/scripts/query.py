#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能旅行助手 Skills 调用脚本

使用方式:
    python query.py "推荐成都春熙路附近的酒店"
    python query.py "查询成都到北京的航班"
    python query.py "帮我规划一个三天两晚的成都行程"

配置 API Key:
    python query.py --config your-api-key
    python query.py --config --clear
"""

import json
import sys
import requests
from pathlib import Path

# API 配置
API_URL = "https://dtgw.ly.com/deeptrip/claw/chat"

# 配置文件路径（保存在 skills 目录下）
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = "config.json"


def get_config_path() -> Path:
    """获取配置文件路径"""
    return SKILL_DIR / CONFIG_FILE


def load_config_from_file(config_path: Path) -> dict:
    """从配置文件读取配置"""
    if not config_path.exists():
        return {}
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config_to_file(config_path: Path, api_key: str) -> bool:
    """保存配置到文件"""
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # 设置目录权限为 700（仅所有者可读写执行）
        config_path.parent.chmod(0o700)

        config = {"api_key": api_key}
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        # 设置文件权限为 600（仅所有者可读写）
        config_path.chmod(0o600)
        return True
    except IOError:
        return False


def clear_config(config_path: Path) -> bool:
    """清除配置文件"""
    try:
        if config_path.exists():
            config_path.unlink()
        # 如果目录为空，也删除目录
        if config_path.parent.exists() and not any(config_path.parent.iterdir()):
            config_path.parent.rmdir()
        return True
    except IOError:
        return False


def get_api_key() -> str:
    """
    从配置文件获取 API Key
    """
    config = load_config_from_file(get_config_path())
    return config.get("api_key", "")

def query_skill(question: str) -> dict:
    """
    调用智能旅行助手技能

    Args:
        question: 用户问题

    Returns:
        dict: API 响应结果
    """
    api_key = get_api_key()

    headers = {
        "Content-Type": "application/json",
        "deeptrip-claw-api-key": api_key,
        "claw-channel": "clawhub_Intl"
    }

    payload = {
        "q": question
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=300
    )

    response.raise_for_status()
    return response.json()

def format_result(result: dict) -> str:
    """格式化输出结果"""
    if result.get("code") != "0":
        return f"❌ 请求失败: {result.get('msg', '未知错误')}"

    data = result.get("data", {})
    text = data.get("text", "")
    product_links = data.get("产品跳转链接", {})

    output = []
    output.append("=" * 60)
    output.append("📋 回复内容")
    output.append("=" * 60)
    output.append(text)

    if product_links:
        output.append("\n" + "=" * 60)
        output.append("🔗 产品跳转链接")
        output.append("=" * 60)
        for name, links in product_links.items():
            output.append(f"\n【{name}】")
            if "PC链接" in links:
                output.append(f"  PC端: {links['PC链接']}")
            if "手机链接" in links:
                output.append(f"  手机端: {links['手机链接']}")

    return "\n".join(output)

def print_config_status():
    """打印当前配置状态"""
    config_path = get_config_path()

    print("📋 当前 API Key 配置状态:\n")

    # 用户级配置
    config = load_config_from_file(config_path)
    if config.get("api_key"):
        print(f"  ✅ 用户级配置: {config_path}")
        print(f"     API Key: {config['api_key'][:8]}...{config['api_key'][-4:]}")
    else:
        print(f"  ⬜ 用户级配置: {config_path} (未配置)")

    api_key = get_api_key()
    if api_key:
        print(f"\n  当前生效的 API Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        print(f"\n  当前生效的 API Key: 未配置")


def main():
    """主函数"""
    # 处理 --config 参数
    if len(sys.argv) >= 2 and sys.argv[1] == "--config":
        # 检查是否有额外的参数
        if len(sys.argv) == 2:
            # 只打印配置状态
            print_config_status()
            sys.exit(0)

        # --config --clear: 清除配置
        if sys.argv[2] == "--clear":
            config_path = get_config_path()
            if config_path.exists():
                if clear_config(config_path):
                    print(f"✅ 已清除配置: {config_path}")
                else:
                    print(f"❌ 清除配置失败")
            else:
                print("ℹ️ 没有找到需要清除的配置文件")
            sys.exit(0)

        # --config <api-key>: 保存配置
        api_key = sys.argv[2]
        config_path = get_config_path()
        if save_config_to_file(config_path, api_key):
            print(f"✅ 已保存 API Key 到: {config_path}")
            sys.exit(0)
        else:
            print(f"❌ 保存配置失败")
            sys.exit(1)

    # 检查是否有查询参数
    if len(sys.argv) < 2:
        print("智能旅行助手 Skills")
        print("")
        print("使用方式:")
        print("  python query.py \"你的问题\"          # 查询旅行信息")
        print("  python query.py --config <api-key>   # 保存 API Key")
        print("  python query.py --config --clear     # 清除已保存的 API Key")
        print("  python query.py --config             # 查看当前配置状态")
        print("")
        print("示例:")
        print("  python query.py \"推荐成都春熙路附近的酒店\"")
        print("  python query.py \"查询成都到北京的航班\"")
        sys.exit(1)

    question = sys.argv[1]

    try:
        print(f"🔍 正在查询: {question}\n")
        result = query_skill(question)
        print(format_result(result))
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
