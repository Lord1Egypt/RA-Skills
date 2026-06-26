import os
import sys


def main():
    print("🔧 Zero-One-Two-Three 知识架构师 (v17.0.0)")
    print("=" * 50)

    # 核心模块状态检查
    modules = {
        "knowledge_lock.py": "知识加密引擎",
        "mailbox_tool.py": "邮箱发货系统",
        "style_clone.py": "风格克隆引擎",
        "voice_clone.py": "语音分身引擎",
        "personal_library.py": "个人图书馆",
        "ephemeral_share.py": "阅后即焚分享",
    }

    print("\n📦 核心模块状态:")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for filename, desc in modules.items():
        filepath = os.path.join(base_dir, filename)
        status = "✅" if os.path.exists(filepath) else "❌"
        print(f"  {status} {desc}: {filename}")

    # 可选：检查 genesis_engine 目录（如果存在）
    genesis_dir = os.path.join(base_dir, "genesis_engine")
    if os.path.exists(genesis_dir):
        print(f"\n📂 genesis_engine 扩展目录: ✅ 已加载")
    else:
        print(f"\n📂 genesis_engine 扩展目录: ⏸️ 可选模块，未安装")

    # 可选：检查 tools 目录
    tools_dir = os.path.join(base_dir, "tools")
    if os.path.exists(tools_dir):
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
        print(f"\n🧰 扩展工具 ({len(tool_files)} 个):")
        for tf in tool_files:
            print(f"    - {tf}")
    else:
        print(f"\n🧰 扩展工具目录: ⏸️ 可选模块，未安装")

    print("\n" + "=" * 50)
    print("✅ 系统检查完成！")
    print("\n💡 快速开始:")
    print("   python style_clone.py analyze ./你的文章.md")
    print("   python voice_clone.py speak '你好世界'")
    print("   python knowledge_lock.py lock 笔记.md 你的密码")
    print("   python personal_library.py --stats")


if __name__ == "__main__":
    main()
