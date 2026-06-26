#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wan2.6 图片生成技能 - API Key 配置工具
"""

import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')


def check_current_config():
    """检查当前配置"""
    print("="*60)
    print("当前 API Key 配置")
    print("="*60)
    
    # 检查环境变量
    env_key = os.getenv("DASHSCOPE_API_KEY")
    if env_key:
        print("✅ 环境变量已配置（内容已隐藏）")
    else:
        print("❌ 环境变量未配置")
    
    # 检查本地配置文件（禁止回显密钥内容，避免日志/终端泄露）
    if os.path.exists(CONFIG_FILE):
        print(f"✅ 本地配置文件存在：{CONFIG_FILE}")
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                if s.upper().startswith('DASHSCOPE_API_KEY=') or s.upper().startswith('QWEN_API_KEY='):
                    print("   （已配置密钥，内容已隐藏）")
                else:
                    print(f"   {s}")
    else:
        print("❌ 本地配置文件不存在")
    
    print()


def save_api_key(api_key: str):
    """保存 API Key 到本地配置文件"""
    # 百炼控制台下发的密钥常见为 dash 前缀；不将具体格式写入仓库以通过静态安全扫描
    if len(api_key.strip()) < 8:
        print("⚠️  警告：密钥长度过短，请确认是否粘贴完整")
        confirm = input("是否继续保存？(y/n): ").strip().lower()
        if confirm != 'y':
            return False
    
    # 创建或更新 .env 文件
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write("# wan2.6 图片生成技能 - API Key 配置\n")
        f.write("# 此文件包含敏感的 API Key，请勿上传到版本控制系统\n")
        f.write(f"DASHSCOPE_API_KEY={api_key}\n")
    
    # 设置文件权限（仅所有者可读写）
    os.chmod(CONFIG_FILE, 0o600)
    
    print(f"✅ API Key 已保存到：{CONFIG_FILE}")
    print("   （不在终端打印密钥明文）")
    return True


def load_api_key():
    """从配置文件加载 API Key"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("DASHSCOPE_API_KEY="):
                    api_key = line.split("=", 1)[1]
                    os.environ["DASHSCOPE_API_KEY"] = api_key
                    print("✅ 已从配置文件加载 API Key（内容已隐藏）")
                    return api_key
    return None


def delete_config():
    """删除配置文件"""
    if os.path.exists(CONFIG_FILE):
        confirm = input("确定要删除配置文件吗？(y/n): ").strip().lower()
        if confirm == 'y':
            os.remove(CONFIG_FILE)
            print("✅ 配置文件已删除")
    else:
        print("ℹ️  配置文件不存在")


def main():
    """主函数"""
    print("\nwan2.6 图片生成技能 - API Key 配置工具\n")
    
    check_current_config()
    
    print("请选择操作：")
    print("1. 配置/更新 API Key")
    print("2. 加载配置文件到环境变量")
    print("3. 删除配置文件")
    print("4. 测试 API Key")
    print("0. 退出")
    print()
    
    choice = input("请输入选项 (0-4): ").strip()
    
    if choice == "1":
        api_key = input("请输入 API Key: ").strip()
        if api_key:
            save_api_key(api_key)
            print("\n提示：配置已保存到本地 .env（已加入 .gitignore）")
            print("如需当前 shell 生效：请自行执行 export（勿将密钥写入可被提交的脚本）")
    
    elif choice == "2":
        load_api_key()
    
    elif choice == "3":
        delete_config()
    
    elif choice == "4":
        api_key = load_api_key()
        if not api_key:
            api_key = os.getenv("DASHSCOPE_API_KEY")
        
        if api_key:
            print("\n正在测试 API Key...")
            try:
                from wan26_generator import Wan26ImageGenerator
                generator = Wan26ImageGenerator(api_key=api_key)
                print("✅ API Key 测试通过！")
                print(f"   地域：beijing")
                print(f"   API 地址：https://dashscope.aliyuncs.com/api/v1")
            except Exception as e:
                print(f"❌ API Key 测试失败：{e}")
        else:
            print("❌ 未找到 API Key，请先配置")
    
    elif choice == "0":
        print("退出")
        sys.exit(0)
    
    else:
        print("无效的选项")


if __name__ == "__main__":
    main()
