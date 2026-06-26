"""Persona & roles: persona, persona-get, roles, role-get, role-apply, role-create, role-delete, role-from-media, personality."""

from __future__ import annotations

import json
import os
from argparse import Namespace

from agent_memory.cli._utils import (
    get_memory,
    _HAS_PERSONALITY,
)

try:
    from agent_memory.cli._utils import ChatParser, PersonalityAnalyzer, PersonalityMemory
except ImportError:
    ChatParser = PersonalityAnalyzer = PersonalityMemory = None


# ── 数字孪生命令 ──────────────────────────────────────────


def cmd_persona(args):
    """构建数字孪生人格画像"""
    mem = get_memory()
    print("⚠️  人格画像是基于记忆数据生成的统计摘要，不是对真实性格的权威描述。", file=__import__('sys').stderr)
    profile = mem.build_persona()
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    mem.close()


def cmd_persona_get(args):
    """获取最新的数字孪生人格画像"""
    mem = get_memory()
    print("⚠️ 以上内容基于记忆数据自动生成，仅供参考，不代表对事实或人格的权威判断。", file=__import__('sys').stderr)
    profile = mem.get_persona()
    if profile:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print("📭 尚未构建人格画像 — 使用 persona 命令构建")
    mem.close()


# ── 个人风格 Agent 命令 ──────────────────────────────────


def cmd_roles(args):
    """列出所有可用的角色模板"""
    mem = get_memory()
    roles = mem.list_roles()
    if not roles:
        print("📭 暂无角色模板 — 使用 role-create 创建")
    else:
        print(json.dumps(roles, ensure_ascii=False, indent=2))
    mem.close()


def cmd_role_get(args):
    """获取特定角色模板"""
    mem = get_memory()
    role = mem.get_role(args.role_id)
    if role:
        print(json.dumps(role, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 角色模板不存在: {args.role_id} — 使用 roles 查看所有模板")
    mem.close()


def cmd_role_apply(args):
    """应用角色风格到个人人格"""
    mem = get_memory()
    result = mem.apply_role(args.role_id, args.weight)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 角色模板不存在: {args.role_id} — 使用 roles 查看所有模板")
    mem.close()


def cmd_role_create(args):
    """创建新角色模板"""
    mem = get_memory()
    try:
        traits = json.loads(args.traits)
        topics = args.topics.split(",") if args.topics else None
        result = mem.create_role(
            role_id=args.role_id,
            name=args.name,
            prompt_template=args.prompt,
            personality_traits=traits,
            speaking_style=args.speaking_style,
            topic_preferences=topics,
            emotional_tone=args.emotional_tone
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "人格特质 JSON 格式错误，示例: [\"开放性\", \"严谨性\"]"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    mem.close()


def cmd_role_delete(args):
    """删除角色模板"""
    # 确认提示（--yes/-y 跳过）
    if not args.yes:
        confirm = input(f"确认删除角色模板 {args.role_id}？此操作不可撤销 [y/N] ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return

    mem = get_memory()
    result = mem.delete_role(args.role_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


def cmd_role_from_media(args):
    """从媒体文件创建角色模板"""
    mem = get_memory()
    result = mem.create_role_from_media(args.file_path, args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


# ── 人格分析命令 ──────────────────────────────────────────


def cmd_personality(args):
    """人格分析命令"""
    subcmd = args.personality_subcmd

    if subcmd == "analyze":
        _cmd_personality_analyze(args)
    elif subcmd == "show":
        _cmd_personality_show(args)
    elif subcmd == "versions":
        _cmd_personality_versions(args)
    elif subcmd == "evidence":
        _cmd_personality_evidence(args)
    elif subcmd == "delete":
        _cmd_personality_delete(args)
    else:
        print("用法: agent-memory personality <analyze|show|versions|evidence|delete> [参数]")


def _cmd_personality_analyze(args):
    """分析聊天记录生成人格画像"""
    if not _HAS_PERSONALITY:
        print(json.dumps({"error": "人格分析模块未安装 (chat_parser / personality_analyzer / personality_memory)"}, ensure_ascii=False))
        return

    chat_text = args.text
    if args.file:
        if not os.path.exists(args.file):
            print(json.dumps({"error": f"文件不存在: {args.file}"}, ensure_ascii=False))
            return
        with open(args.file, "r", encoding="utf-8") as f:
            chat_text = f.read()

    if not chat_text:
        print(json.dumps({"error": "请提供 --text 或 --file 参数，例如: personality analyze --text \"你好世界\""}, ensure_ascii=False))
        return

    try:
        parser = ChatParser()
        analyzer = PersonalityAnalyzer()
        pmem = PersonalityMemory()

        parsed = parser.parse(
            chat_text,
            source_type=args.source_type,
            self_name=args.self_name or None,
        )

        profile = analyzer.analyze(
            parsed,
            privacy_level=args.privacy_level,
        )

        pmem.save(profile)

        print(json.dumps(profile, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def _cmd_personality_show(args):
    """获取人格画像"""
    if not _HAS_PERSONALITY:
        print(json.dumps({"error": "人格分析模块未安装 (chat_parser / personality_analyzer / personality_memory)"}, ensure_ascii=False))
        return

    try:
        pmem = PersonalityMemory()
        profile = pmem.get(
            args.person_id,
            access_level=args.access_level,
        )

        if profile:
            print(json.dumps(profile, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 人格画像不存在: {args.person_id} — 使用 persona 构建人格画像")

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def _cmd_personality_versions(args):
    """获取人格画像版本历史"""
    if not _HAS_PERSONALITY:
        print(json.dumps({"error": "人格分析模块未安装 (chat_parser / personality_analyzer / personality_memory)"}, ensure_ascii=False))
        return

    try:
        pmem = PersonalityMemory()
        versions = pmem.get_versions(args.person_id)

        print(json.dumps({
            "person_id": args.person_id,
            "versions": versions,
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def _cmd_personality_evidence(args):
    """获取人格特质推断的证据来源"""
    if not _HAS_PERSONALITY:
        print(json.dumps({"error": "人格分析模块未安装 (chat_parser / personality_analyzer / personality_memory)"}, ensure_ascii=False))
        return

    try:
        pmem = PersonalityMemory()
        evidence = pmem.get_evidence(
            args.person_id,
            trait=args.trait,
        )

        print(json.dumps({
            "person_id": args.person_id,
            "trait_filter": args.trait,
            "evidence": evidence,
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


def _cmd_personality_delete(args):
    """删除人格画像"""
    if not _HAS_PERSONALITY:
        print(json.dumps({"error": "人格分析模块未安装 (chat_parser / personality_analyzer / personality_memory)"}, ensure_ascii=False))
        return

    try:
        pmem = PersonalityMemory()
        deleted = pmem.delete(args.person_id)

        if deleted:
            print(f"🗑️  人格画像已删除: {args.person_id}")
        else:
            print(f"❌ 人格画像不存在: {args.person_id} — 使用 persona 构建人格画像")

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
