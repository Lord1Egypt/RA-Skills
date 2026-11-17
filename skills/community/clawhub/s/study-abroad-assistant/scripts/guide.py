#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""留学助理 skill — 主交互脚本（CLI）。
用法示例:
  python3 scripts/guide.py assess --gpa 3.5 --toefl 100 --gre 320 --degree ms --discipline cs --direction "systems,ai"
  python3 scripts/guide.py plan --season 2027 --degree ms
  python3 scripts/guide.py status --season 2027
  python3 scripts/guide.py done --task p3t2 --season 2027
  python3 scripts/guide.py schools --gpa 3.5 --direction "systems,ai" --top 6
  python3 scripts/guide.py feedback --type sop --text "I have always been passionate about ..."
  python3 scripts/guide.py outreach --mode first --professor '{"name":"Prof. X","field":"Distributed Systems","topics":["systems"]}'
  python3 scripts/guide.py report --type decision --payload '{"offers":[{"program":"A","funding":80,"rank":90,"fit":80,"cost":50}]}'
  python3 scripts/guide.py plan       # 无参数 = 对话引导
"""
import argparse
import json
import os
import sys

# Python 版本守卫：包声明要求 3.10+，低于 3.10 直接给出清晰报错（而非深层 TypeError）
if sys.version_info < (3, 10):
    print(
        f"⚠️ 需要 Python 3.10+（当前 {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}）。\n"
        "  示例（macOS）：/opt/homebrew/bin/python3.13 scripts/guide.py assess --gpa 3.5",
        file=sys.stderr,
    )
    sys.exit(1)

import api
import render


def _parse_json(value, name):
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        print(f"参数 {name} 不是合法 JSON: {value}", file=sys.stderr)
        sys.exit(2)


def _wrapped(fn):
    """统一异常处理：QUOTA 403 → 注册引导；引擎不可达 → 降级提示。"""
    try:
        return fn()
    except api.ApiError as e:
        if getattr(e, "status", 0) == 403:
            print(api.REGISTER_GUIDE, file=sys.stderr)
            sys.exit(1)
        print(f"⚠️ 引擎不可用: {e}", file=sys.stderr)
        print("已降级：当前结果基于通用知识，无法使用知识库/画像/计划引擎。请确认引擎已启动（STUDY_ENGINE_URL）。",
              file=sys.stderr)
        sys.exit(1)


def cmd_assess(args):
    def run():
        profile = {
            "gpa": args.gpa, "toefl": args.toefl, "gre": args.gre,
            "targetDegree": args.degree,
            "disciplines": args.discipline,
            "research": _parse_json(args.research, "--research") or [],
            "intern": _parse_json(args.intern, "--intern") or [],
        }
        if args.direction:
            profile["direction"] = [d.strip() for d in args.direction.split(",")]
        print(render.render_assess(api.assess(profile)))
    _wrapped(run)


def cmd_schools(args):
    def run():
        params = {"degree": args.degree, "discipline": args.discipline, "top": args.top}
        if args.mode:
            params["mode"] = args.mode
        if args.gpa is not None:
            params["gpa"] = args.gpa
        if args.toefl is not None:
            params["toefl"] = args.toefl
        if args.gre is not None:
            params["gre"] = args.gre
        if args.direction:
            params["direction"] = args.direction
        if args.school_ids:
            params["school_ids"] = args.school_ids
        print(render.render_schools(api.schools(**params)))
    _wrapped(run)


def cmd_professors(args):
    def run():
        d = api.professors(gpa=args.gpa, direction=args.direction, top=args.top,
                           school_ids=args.school_ids)
        print(render.render_professors(d))
    _wrapped(run)


def cmd_feedback(args):
    def run():
        ctx = _parse_json(args.context, "--context")
        print(render.render_feedback(api.feedback(args.type, args.text, ctx)))
    _wrapped(run)


def cmd_outreach(args):
    def run():
        prof = _parse_json(args.professor, "--professor")
        if not prof:
            print("--professor 必填，如 '{\"name\":\"Prof. X\",\"field\":\"Distributed Systems\",\"topics\":[\"systems\"]}'",
                  file=sys.stderr)
            sys.exit(2)
        sender = _parse_json(args.sender, "--sender") or {}
        print(render.render_outreach(api.outreach(args.mode, prof, sender)))
    _wrapped(run)


def cmd_report(args):
    def run():
        payload = _parse_json(args.payload, "--payload") or {}
        print(render.render_report(api.report(args.type, payload)))
    _wrapped(run)


def cmd_plan(args):
    def run():
        profile = {"targetDegree": args.degree, "disciplines": args.discipline}
        d = api.plan_generate(profile, args.season, args.degree)
        print(render.render_plan({"plan": d["plan"], "progress": d["progress"]}))
    _wrapped(run)


def cmd_status(args):
    def run():
        print(render.render_plan(api.plan_get(args.season)))
    _wrapped(run)


def cmd_done(args):
    def run():
        d = api.plan_task(args.season, args.task, args.status)
        print(f"已更新任务 {args.task} → {args.status}，进度 {d['progress']}")
    _wrapped(run)


def cmd_apps(args):
    def run():
        if args.action == "list":
            print(render.render_apps(api.apps_list()))
        elif args.action == "add":
            d = api.apps_add({"program": args.program, "school": args.school or "",
                              "deadline": args.deadline, "status": args.status, "notes": args.notes or ""})
            print(f"已添加: {d['item']['school']} {d['item']['program']} [{d['item']['id']}]")
            print(render.render_apps(api.apps_list()))
        elif args.action == "update":
            fields = {}
            if args.status:
                fields["status"] = args.status
            if args.deadline:
                fields["deadline"] = args.deadline
            if args.notes:
                fields["notes"] = args.notes
            if not fields:
                print("update 至少提供 --status/--deadline/--notes 之一", file=sys.stderr)
                sys.exit(2)
            d = api.apps_update(args.id, fields)
            print(f"已更新 {args.id} → {d['item']}")
        elif args.action == "del":
            api.apps_delete(args.id)
            print(f"已删除 {args.id}")
    _wrapped(run)


def cmd_register(args):
    """注册转化：保存 API Key 到本机配置 + 合并匿名进度。"""
    key = args.key or os.environ.get("STUDY_API_KEY", "").strip()
    if not key:
        print("请提供 API Key：`python3 scripts/guide.py register --key sk_xxx`"
              "（key 在 compliancehub.cn 注册后获取）", file=sys.stderr)
        sys.exit(2)
    api.save_api_key(key)
    try:
        d = api.merge(api.anon_id())
        print(f"✅ 注册成功：Key 已保存到 {api.KEY_FILE}")
        print(f"   匿名进度已合并：{d['merged']}")
        print("   后续调用自动携带 Key（额度更高，不再受匿名 5 次限制）。")
    except api.ApiError as e:
        print(f"⚠️ Key 已保存，但合并失败: {e}", file=sys.stderr)
        print("   请确认 Key 有效（在 compliancehub.cn 注册获取）。", file=sys.stderr)
        sys.exit(1)


def cmd_profile(args):
    """申请人档案：多轮对话增量累积，驱动画像/选校持续修正。"""
    def run():
        if args.action == "show":
            print(render.render_profile(api.profile_get()))
        else:  # update
            fields = {}
            for k in ("gpa", "toefl", "gre", "targetDegree"):
                v = getattr(args, k, None)
                if v is not None:
                    fields[k] = v
            if args.direction:
                fields["direction"] = [d.strip() for d in args.direction.split(",")]
            if args.school_ids:
                fields["school_ids"] = [s.strip() for s in args.school_ids.split(",")]
            if args.disciplines:
                fields["disciplines"] = args.disciplines
            if args.research:
                fields["research"] = _parse_json(args.research, "--research") or []
            if args.intern:
                fields["intern"] = _parse_json(args.intern, "--intern") or []
            if not fields:
                print("update 至少提供一个字段（--gpa/--toefl/--gre/--degree/--direction/--school_ids/--research/--intern）",
                      file=sys.stderr)
                sys.exit(2)
            d = api.profile_update(fields)
            print(f"✅ 档案已更新：{json.dumps(d['profile'], ensure_ascii=False)}")
            print("   下次 assess/schools 自动采用（请求参数可省略）。")
    _wrapped(run)


def interactive():
    """无参数时的对话引导。"""
    print("留学助理（引擎版）· 对话引导")
    print("先做背景评估：")
    gpa = input("GPA（如 3.5，回车跳过）: ").strip()
    toefl = input("TOEFL（如 100，回车跳过）: ").strip()
    gre = input("GRE（如 320，回车跳过）: ").strip()
    degree = input("目标学位（ms/phd，默认 ms）: ").strip() or "ms"
    direction = input("研究方向（逗号分隔，如 systems,ai，回车跳过）: ").strip()

    profile = {"targetDegree": degree, "disciplines": ["cs"]}
    if gpa:
        profile["gpa"] = float(gpa)
    if toefl:
        profile["toefl"] = int(toefl)
    if gre:
        profile["gre"] = int(gre)
    if direction:
        profile["direction"] = [d.strip() for d in direction.split(",")]

    _wrapped(lambda: print(render.render_assess(api.assess(profile))))
    season = input("\n生成申请计划？（输入申请年份如 2027，回车跳过）: ").strip()
    if season:
        d = api.plan_generate(profile, season, degree)
        print(render.render_plan({"plan": d["plan"], "progress": d["progress"]}))
        print("\n后续可用: guide.py status / done / schools / feedback / outreach")


def main():
    ap = argparse.ArgumentParser(description="留学助理 skill 主流程")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("assess", help="竞争力画像")
    p.add_argument("--gpa", type=float); p.add_argument("--toefl", type=int); p.add_argument("--gre", type=int)
    p.add_argument("--degree", default="ms"); p.add_argument("--discipline", nargs="+", default=["cs"])
    p.add_argument("--direction"); p.add_argument("--research"); p.add_argument("--intern")

    p = sub.add_parser("schools", help="选校匹配")
    p.add_argument("--gpa", type=float); p.add_argument("--toefl", type=int); p.add_argument("--gre", type=int)
    p.add_argument("--degree", default="ms"); p.add_argument("--discipline", default="cs")
    p.add_argument("--direction"); p.add_argument("--top", type=int, default=9); p.add_argument("--mode")
    p.add_argument("--school_ids", help="连接校（交换/套磁目标）强制纳入，逗号分隔，如 uw,uiuc")

    p = sub.add_parser("professors", help="教授短名单（套磁选导）")
    p.add_argument("--gpa", type=float); p.add_argument("--direction", help="如 systems,distributed")
    p.add_argument("--top", type=int, default=8); p.add_argument("--school_ids", help="限定学校，逗号分隔")

    p = sub.add_parser("feedback", help="文书逐段反馈")
    p.add_argument("--type", required=True); p.add_argument("--text", required=True); p.add_argument("--context")

    p = sub.add_parser("outreach", help="套磁草稿")
    p.add_argument("--mode", default="first"); p.add_argument("--professor", required=True); p.add_argument("--sender")

    p = sub.add_parser("report", help="报告")
    p.add_argument("--type", default="decision"); p.add_argument("--payload")

    p = sub.add_parser("plan", help="生成申请计划")
    p.add_argument("--season"); p.add_argument("--degree", default="ms"); p.add_argument("--discipline", nargs="+", default=["cs"])

    p = sub.add_parser("status", help="查看计划进度")
    p.add_argument("--season")

    p = sub.add_parser("done", help="标记任务完成")
    p.add_argument("--task", required=True); p.add_argument("--season", required=True); p.add_argument("--status", default="done")

    p = sub.add_parser("apps", help="申请清单（list/add/update/del）")
    p.add_argument("action", choices=["list", "add", "update", "del"])
    p.add_argument("--id"); p.add_argument("--program"); p.add_argument("--school")
    p.add_argument("--deadline", help="ISO 日期，如 2026-12-01"); p.add_argument("--status", default="planned")
    p.add_argument("--notes")

    p = sub.add_parser("register", help="注册转化：保存 API Key + 合并匿名进度")
    p.add_argument("--key", help="合规平台 API Key（sk_ 开头）")

    p = sub.add_parser("profile", help="申请人档案（多轮对话累积，show/update）")
    p.add_argument("action", choices=["show", "update"])
    p.add_argument("--gpa", type=float); p.add_argument("--toefl", type=int); p.add_argument("--gre", type=int)
    p.add_argument("--degree"); p.add_argument("--disciplines", nargs="+")
    p.add_argument("--direction", help="研究方向，逗号分隔，如 ai,ml,robotics")
    p.add_argument("--school_ids", help="连接校（交换/套磁目标），逗号分隔，如 uw,uiuc")
    p.add_argument("--research", help="科研 JSON"); p.add_argument("--intern", help="实习 JSON")

    args = ap.parse_args()
    if not args.cmd:
        interactive()
        return
    {"assess": cmd_assess, "schools": cmd_schools, "professors": cmd_professors,
     "feedback": cmd_feedback, "outreach": cmd_outreach, "report": cmd_report,
     "plan": cmd_plan, "status": cmd_status, "done": cmd_done, "apps": cmd_apps,
     "register": cmd_register, "profile": cmd_profile}[args.cmd](args)


if __name__ == "__main__":
    main()
