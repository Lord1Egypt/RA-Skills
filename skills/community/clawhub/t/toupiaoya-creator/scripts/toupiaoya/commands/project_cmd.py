from __future__ import annotations

import argparse
import datetime
import json
import sys

import requests

from toupiaoya.auth import resolve_token
from toupiaoya.config import load_config, token_from_config
from toupiaoya.create import ToupiaoyaCreator, parse_group_list
from toupiaoya.project_api import (
    add_project_group,
    add_project_choice,
    fetch_project_groups,
    fetch_project_choices,
    fetch_project_view_data,
    fetch_project_vote_data,
    fetch_scene_data_list,
    update_project_group,
    update_project_choice,
)


def register(subparsers: argparse._SubParsersAction) -> None:
    project_parser = subparsers.add_parser("project", help="作品（投票项目）相关命令")
    proj_sub = project_parser.add_subparsers(dest="project_command")

    p = proj_sub.add_parser("create", help="创建投票作品")
    p.add_argument("--briefTitle", type=str, required=True, help="封面标题")
    p.add_argument("--briefDesc", type=str, required=True, help="封面简介")
    p.add_argument("--detailTitle", type=str, required=False, default=None, help="详细标题")
    p.add_argument("--detailDesc", type=str, required=False, default=None, help="详细说明")
    p.add_argument("--sponsor", type=str, required=False, default=None, help="主办方")
    p.add_argument(
        "--voteType",
        type=str,
        required=False,
        default="textVote",
        help="投票类型：imageVote/textVote/videoVote",
    )
    p.add_argument("--timeStart", type=str, required=False, default=None, help="开始时间，格式 yyyy-MM-dd HH:mm")
    p.add_argument("--timeEnd", type=str, required=False, default=None, help="结束时间，格式 yyyy-MM-dd HH:mm")
    p.add_argument("--templateId", type=int, required=False, default=None, help="模板ID，不传则走后端默认")
    p.add_argument(
        "--groupList",
        type=str,
        required=False,
        default=None,
        help='分组JSON数组字符串，例如: \'[{"groupName":"第一组","choices":[{"name":"A"}]}]\'',
    )
    p.add_argument(
        "--multi",
        action="store_true",
        help="多选开关；默认不传即单选。",
    )
    p.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取（推荐先执行 login）",
    )

    lp = proj_sub.add_parser("list", help="分页查询作品/场景列表（lwork scene/data/list）")
    lp.add_argument("--type", dest="list_type", type=int, default=3, help="接口 type，默认 3")
    lp.add_argument("--sort", type=str, default="update_time", help="排序字段，默认 update_time")
    lp.add_argument("--orderType", type=str, default="desc", help="排序方向，默认 desc")
    lp.add_argument("--pageNum", type=int, default=1, help="页码，默认 1")
    lp.add_argument("--pageSize", type=int, default=30, help="每页条数，默认 30")
    lp.add_argument(
        "--bizTypes",
        type=str,
        default="",
        help="业务类型筛选，默认空字符串（与接口一致）",
    )
    lp.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    vp = proj_sub.add_parser("vote-data", help="获取作品投票数据（m/lp/data/list）")
    vp.add_argument("--id", type=int, required=True, help="作品 id")
    vp.add_argument("--startTime", type=str, default="", help="筛选开始时间，默认空")
    vp.add_argument("--endTime", type=str, default="", help="筛选结束时间，默认空")
    vp.add_argument("--pageNo", type=int, default=1, help="页码，默认 1")
    vp.add_argument("--pageSize", type=int, default=10, help="每页条数，默认 10")
    vp.add_argument("--showTrash", type=int, default=1, help="是否展示回收站数据，默认 1")
    vp.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    vwp = proj_sub.add_parser("view-data", help="获取作品访问趋势数据（m/single/getWorkViewData）")
    vwp.add_argument("--id", type=int, required=True, help="作品 id")
    vwp.add_argument("--startDay", type=str, default="", help="统计开始日期，格式 yyyy-MM-dd，不传默认最近15天")
    vwp.add_argument("--endDay", type=str, default="", help="统计结束日期，格式 yyyy-MM-dd，不传默认今天")
    vwp.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    cp = proj_sub.add_parser("choice", help="投票选项管理（get/update/add）")
    choice_sub = cp.add_subparsers(dest="choice_command")

    cg = choice_sub.add_parser("get", help="获取作品全部投票选项")
    cg.add_argument("--id", type=int, required=True, help="作品 id")
    cg.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    cu = choice_sub.add_parser("update", help="更新作品某个投票选项")
    cu.add_argument("--id", type=int, required=True, help="作品 id")
    cu.add_argument("--choiceId", type=int, required=True, help="选项 id")
    cu.add_argument("--groupId", type=int, required=False, default=None, help="可选，目标分组 id（用于移动选项分组）")
    cu.add_argument(
        "--choice",
        type=str,
        required=True,
        help='选项补丁 JSON 对象，例如: \'{"content":"新名称","cover":"material/xxx.png"}\'',
    )
    cu.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    ca = choice_sub.add_parser("add", help="给指定分组新增一个投票选项")
    ca.add_argument("--id", type=int, required=True, help="作品 id")
    ca.add_argument("--groupId", type=int, required=True, help="目标分组 id")
    ca.add_argument(
        "--choice",
        type=str,
        required=True,
        help='新增选项 JSON 对象，例如: \'{"content":"新选项","cover":"material/xxx.png"}\'',
    )
    ca.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    gp = proj_sub.add_parser("group", help="投票分组管理（get/add/update）")
    group_sub = gp.add_subparsers(dest="group_command")

    gg = group_sub.add_parser("get", help="获取作品分组列表")
    gg.add_argument("--id", type=int, required=True, help="作品 id")
    gg.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    ga = group_sub.add_parser("add", help="新增分组")
    ga.add_argument("--id", type=int, required=True, help="作品 id")
    ga.add_argument("--groupName", type=str, required=True, help="分组名称")
    ga.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )

    gu = group_sub.add_parser("update", help="更新分组名称")
    gu.add_argument("--id", type=int, required=True, help="作品 id")
    gu.add_argument("--groupId", type=int, required=True, help="分组 id")
    gu.add_argument("--groupName", type=str, required=True, help="新的分组名称")
    gu.add_argument(
        "--access-token",
        type=str,
        required=False,
        default=None,
        help="X-Openclaw-Token；默认从 ~/.toupiaoya/config.json 读取",
    )


def run_project(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    sub = getattr(args, "project_command", None)
    if sub == "create":
        _run_create(args, parser)
    elif sub == "list":
        _run_list(args, parser)
    elif sub == "vote-data":
        _run_vote_data(args, parser)
    elif sub == "view-data":
        _run_view_data(args, parser)
    elif sub == "choice":
        _run_choice(args, parser)
    elif sub == "group":
        _run_group(args, parser)
    else:
        parser.print_help()
        raise SystemExit(1)


def _run_create(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    cfg = load_config()
    token_cli = getattr(args, "access_token", None)
    token = (token_cli or "").strip() or token_from_config(cfg)
    if not token:
        print(
            "提示: 未设置 X-Openclaw-Token；请先执行 `login` 或传 --access-token。",
            file=sys.stderr,
        )
    creator = ToupiaoyaCreator(base_url=args.base_url)
    group_list = parse_group_list(args.groupList)
    single_vote = not getattr(args, "multi", False)
    result = creator.execute(
        brief_title=args.briefTitle,
        brief_desc=args.briefDesc,
        detail_title=args.detailTitle,
        detail_desc=args.detailDesc,
        vote_type=args.voteType,
        time_start=args.timeStart,
        time_end=args.timeEnd,
        group_list=group_list,
        template_id=args.templateId,
        single_vote=single_vote,
        sponsor=args.sponsor,
        access_token=token or None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _run_list(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    token = resolve_token(getattr(args, "access_token", None))
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    try:
        data = fetch_scene_data_list(
            token,
            list_type=getattr(args, "list_type", 3),
            sort=getattr(args, "sort", "update_time"),
            order_type=getattr(args, "orderType", "desc"),
            page_num=getattr(args, "pageNum", 1),
            page_size=getattr(args, "pageSize", 27),
            biz_types=getattr(args, "bizTypes", "") or "",
        )
    except RuntimeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"作品列表 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_choice(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    token = resolve_token(getattr(args, "access_token", None))
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    choice_command = getattr(args, "choice_command", None)
    if choice_command == "get":
        _run_choice_get(args, token)
        return
    if choice_command == "update":
        _run_choice_update(args, token)
        return
    if choice_command == "add":
        _run_choice_add(args, token)
        return

    print(
        json.dumps(
            {"success": False, "code": 400, "msg": "缺少子命令: choice get|update|add"},
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(1)


def _run_choice_get(args: argparse.Namespace, token: str) -> None:
    try:
        data = fetch_project_choices(token, project_id=getattr(args, "id"), base_url=args.base_url)
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"获取选项 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_choice_update(args: argparse.Namespace, token: str) -> None:
    try:
        choice_patch = json.loads(getattr(args, "choice") or "{}")
    except json.JSONDecodeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": f"--choice 不是合法 JSON 对象: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    if not isinstance(choice_patch, dict):
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": "--choice 必须是 JSON 对象"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)
    group_id = getattr(args, "groupId", None)
    if group_id is not None:
        choice_patch["groupId"] = group_id

    try:
        data = update_project_choice(
            token,
            project_id=getattr(args, "id"),
            choice_id=getattr(args, "choiceId"),
            choice_patch=choice_patch,
            base_url=args.base_url,
        )
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"更新选项 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_choice_add(args: argparse.Namespace, token: str) -> None:
    try:
        choice_payload = json.loads(getattr(args, "choice") or "{}")
    except json.JSONDecodeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": f"--choice 不是合法 JSON 对象: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    if not isinstance(choice_payload, dict):
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": "--choice 必须是 JSON 对象"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    try:
        data = add_project_choice(
            token,
            project_id=getattr(args, "id"),
            group_id=getattr(args, "groupId"),
            choice_payload=choice_payload,
            base_url=args.base_url,
        )
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"添加选项 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_vote_data(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    token = resolve_token(getattr(args, "access_token", None))
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    try:
        data = fetch_project_vote_data(
            token,
            project_id=getattr(args, "id"),
            start_time=getattr(args, "startTime", "") or "",
            end_time=getattr(args, "endTime", "") or "",
            page_no=getattr(args, "pageNo", 1),
            page_size=getattr(args, "pageSize", 10),
            show_trash=getattr(args, "showTrash", 1),
        )
    except RuntimeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"获取投票数据 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_view_data(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    token = resolve_token(getattr(args, "access_token", None))
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    try:
        end_day = (getattr(args, "endDay", "") or "").strip()
        start_day = (getattr(args, "startDay", "") or "").strip()
        if not end_day:
            end_date = datetime.date.today()
            end_day = end_date.strftime("%Y-%m-%d")
        else:
            end_date = datetime.datetime.strptime(end_day, "%Y-%m-%d").date()
        if not start_day:
            start_day = (end_date - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
        else:
            datetime.datetime.strptime(start_day, "%Y-%m-%d")

        data = fetch_project_view_data(
            token,
            project_id=getattr(args, "id"),
            start_day=start_day,
            end_day=end_day,
        )
    except ValueError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": f"日期格式错误，需 yyyy-MM-dd: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except RuntimeError as e:
        print(
            json.dumps(
                {"success": False, "code": 400, "msg": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"获取访问趋势 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e

    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_group(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    _ = parser
    token = resolve_token(getattr(args, "access_token", None))
    if not token:
        print(
            json.dumps(
                {
                    "success": False,
                    "code": 401,
                    "msg": "缺少 X-Openclaw-Token：请先执行 `login` 或传 --access-token。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)

    group_command = getattr(args, "group_command", None)
    if group_command == "get":
        _run_group_get(args, token)
        return
    if group_command == "add":
        _run_group_add(args, token)
        return
    if group_command == "update":
        _run_group_update(args, token)
        return

    print(
        json.dumps(
            {"success": False, "code": 400, "msg": "缺少子命令: group get|add|update"},
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(1)


def _run_group_get(args: argparse.Namespace, token: str) -> None:
    try:
        data = fetch_project_groups(token, project_id=getattr(args, "id"), base_url=args.base_url)
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"获取分组 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_group_add(args: argparse.Namespace, token: str) -> None:
    group_name = (getattr(args, "groupName", "") or "").strip()
    if not group_name:
        print(json.dumps({"success": False, "code": 400, "msg": "--groupName 不能为空"}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    try:
        data = add_project_group(
            token,
            project_id=getattr(args, "id"),
            group_name=group_name,
            base_url=args.base_url,
        )
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"新增分组 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _run_group_update(args: argparse.Namespace, token: str) -> None:
    group_name = (getattr(args, "groupName", "") or "").strip()
    if not group_name:
        print(json.dumps({"success": False, "code": 400, "msg": "--groupName 不能为空"}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    try:
        data = update_project_group(
            token,
            project_id=getattr(args, "id"),
            group_id=getattr(args, "groupId"),
            group_name=group_name,
            base_url=args.base_url,
        )
    except RuntimeError as e:
        print(json.dumps({"success": False, "code": 400, "msg": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(
            json.dumps(
                {"success": False, "code": 502, "msg": f"更新分组 HTTP 失败: {e}"},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from e
    print(json.dumps(data, ensure_ascii=False, indent=2))
