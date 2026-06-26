#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo v2.0 CLI - 命令行接口
"""
import os
import sys
import argparse
import json

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import get_engine


def cmd_save(args):
    """保存记忆"""
    engine = get_engine()
    
    if args.cause and args.change:
        # 结构化保存
        engine.save(args.cause, args.change, args.todo, args.topic)
        print(f"✅ 已保存记忆")
        print(f"主题: {args.topic or '日常记录'}")
        print(f"因: {args.cause}")
        print(f"改: {args.change}")
        if args.todo:
            print(f"待: {args.todo}")
    elif args.text:
        # 文本保存（自动提取结构）
        engine.save_text(args.text)
        print(f"✅ 已保存记忆")
        print(f"原文: {args.text[:100]}...")
    else:
        # 从 stdin 读取
        text = sys.stdin.read().strip()
        if text:
            engine.save_text(text)
            print(f"✅ 已保存记忆")
        else:
            print("❌ 未提供内容")
            return 1
    
    return 0


def cmd_search(args):
    """搜索记忆"""
    engine = get_engine()
    result = engine.search(args.keyword)
    
    found = False
    
    if result["daily"]:
        found = True
        print("📅 相关记忆:")
        for item in result["daily"]:
            print(f"  [{item['file']}]")
            print(f"  {item['content'][:150]}...\n")
    
    if result["knowledge"]:
        found = True
        print("📚 相关知识:")
        for item in result["knowledge"]:
            print(f"  - {item['title']}")
            print(f"    {item['content'][:100]}...\n")
    
    if not found:
        print(f"❌ 未找到相关内容: {args.keyword}")
    
    return 0


def cmd_show(args):
    """显示记忆"""
    engine = get_engine()
    
    if args.knowledge:
        # 显示知识库
        files = engine.storage.list_files()
        for f in files.get("knowledge", []):
            path = engine.storage.knowledge_dir / f["name"]
            content = path.read_text(encoding="utf-8")
            print(f"\n{'='*50}")
            print(content[:500])
            print("...")
    else:
        # 显示今日记忆
        content = engine.get_today()
        print(content)
    
    return 0


def cmd_list(args):
    """列出文件"""
    engine = get_engine()
    status = engine.get_status()
    
    print("📂 记忆文件:")
    print(f"\n📅 每日记忆 ({len(status['files']['daily'])} 个):")
    for f in status["files"]["daily"]:
        print(f"  {f['name']} ({f['size']} bytes)")
    
    print(f"\n📚 知识库 ({len(status['files']['knowledge'])} 个):")
    for f in status["files"]["knowledge"]:
        print(f"  {f['name']} ({f['size']} bytes)")
    
    if status["files"]["archive"]:
        print(f"\n📦 归档 ({len(status['files']['archive'])} 个):")
        for f in status["files"]["archive"][:5]:
            print(f"  {f['name']} ({f['size']} bytes)")
    
    return 0


def cmd_config(args):
    """配置管理"""
    engine = get_engine()
    
    if args.show or not any([args.llm, args.key, args.ai, args.web, args.persist]):
        # 显示配置
        status = engine.get_status()
        config = status["config"]
        print("⚙️ starmemo 配置:")
        print(f"  模型: {config['model']}")
        print(f"  AI优化: {'✅ 开启' if config['enable_ai'] else '❌ 关闭'}")
        print(f"  持久化: {'✅ 开启' if config['persist_key'] else '❌ 关闭'}")
        print(f"  联网: {'✅ 开启' if config['allow_web_fetch'] else '❌ 关闭'}")
        return 0
    
    # 更新配置
    config_text = "记忆配置"
    if args.llm:
        config_text += f" llm={args.llm}"
    if args.key:
        config_text += f" key={args.key}"
    if args.ai:
        config_text += f" ai={args.ai}"
    if args.web:
        config_text += f" web={args.web}"
    if args.persist:
        config_text += f" persist={args.persist}"
    
    engine._handle_config(config_text)
    print("✅ 配置已更新")
    
    return 0


def cmd_knowledge(args):
    """知识库管理"""
    engine = get_engine()
    
    if args.add:
        # 添加知识
        parts = args.add.split("|", 1)
        if len(parts) == 2:
            key, content = parts
            engine.save_knowledge(key.strip(), content.strip(), "手动添加")
            print(f"✅ 已添加知识: {key.strip()}")
        else:
            print("❌ 格式: --add '标题|内容'")
            return 1
    else:
        # 列出知识
        files = engine.storage.list_files()
        for f in files.get("knowledge", []):
            print(f"  {f['name']}")
    
    return 0


def cmd_process(args):
    """处理文本（完整流程）"""
    engine = get_engine()
    
    text = args.text
    if not text:
        text = sys.stdin.read().strip()
    
    if not text:
        print("❌ 未提供内容")
        return 1
    
    result = engine.process(text, auto_save=args.save)
    
    print(f"动作: {result['action']}")
    if result['memory']:
        print(f"\n找到记忆:\n{result['memory'][:300]}...")
    if result['response']:
        print(f"\n响应: {result['response']}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="starmemo v2.0 - 智能记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 保存结构化记忆
  python3 cli.py save --cause "用户喜欢TypeScript" --change "记录开发偏好"

  # 保存文本（自动提取结构）
  python3 cli.py save --text "今天学习了Python装饰器"

  # 搜索记忆
  python3 cli.py search Python

  # 查看今日记忆
  python3 cli.py show

  # 配置
  python3 cli.py config --show
  python3 cli.py config --llm huoshan --key YOUR_KEY
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # save
    save_p = subparsers.add_parser("save", help="保存记忆")
    save_p.add_argument("--cause", help="原因/背景")
    save_p.add_argument("--change", help="做了什么")
    save_p.add_argument("--todo", help="待办事项")
    save_p.add_argument("--topic", help="主题")
    save_p.add_argument("--text", help="文本内容（自动提取结构）")
    save_p.set_defaults(func=cmd_save)
    
    # search
    search_p = subparsers.add_parser("search", help="搜索记忆")
    search_p.add_argument("keyword", help="搜索关键词")
    search_p.set_defaults(func=cmd_search)
    
    # show
    show_p = subparsers.add_parser("show", help="显示记忆")
    show_p.add_argument("--knowledge", action="store_true", help="显示知识库")
    show_p.set_defaults(func=cmd_show)
    
    # list
    list_p = subparsers.add_parser("list", help="列出文件")
    list_p.set_defaults(func=cmd_list)
    
    # config
    config_p = subparsers.add_parser("config", help="配置管理")
    config_p.add_argument("--show", action="store_true", help="显示配置")
    config_p.add_argument("--llm", help="设置模型")
    config_p.add_argument("--key", help="设置 API Key")
    config_p.add_argument("--ai", help="开启/关闭 AI (true/false)")
    config_p.add_argument("--web", help="开启/关闭联网 (true/false)")
    config_p.add_argument("--persist", help="开启/关闭持久化 (true/false)")
    config_p.set_defaults(func=cmd_config)
    
    # knowledge
    knowledge_p = subparsers.add_parser("knowledge", help="知识库管理")
    knowledge_p.add_argument("--add", help="添加知识 (格式: 标题|内容)")
    knowledge_p.set_defaults(func=cmd_knowledge)
    
    # process
    process_p = subparsers.add_parser("process", help="处理文本（完整流程）")
    process_p.add_argument("text", nargs="?", help="文本内容")
    process_p.add_argument("--save", action="store_true", default=True, help="自动保存")
    process_p.set_defaults(func=cmd_process)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
