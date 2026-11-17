"""任务编排、日志查询。

百度知道回答发布编排层：
- 参数校验（question_url / input_id 必填）
- 鉴权（check_entitlement）
- 幂等预检（answer_publish_records 按 idempotency_key 查重）
- 档位分流（mock / simulator_rpa / real_rpa）
- 调用 baidu_zhidao_rpa.run_publish_answer_async
- 写 answer_publish_records + task_logs
- 录屏包裹（RpaVideoSession）
- stdout 输出 JSON 结果
"""

from __future__ import annotations

import asyncio
import json
import os
import uuid
from typing import Any, Dict, Optional

from jiangchang_skill_core import collect_runtime_diagnostics, config, format_runtime_health_lines
from jiangchang_skill_core.rpa.video_session import RpaVideoSession

from db import answer_publish_records_repository as apr
from db import task_logs_repository as tlr
from service.account_client import AccountManagerError, pick_web_account_with_fallback, release_lease
from service.baidu_zhidao_rpa import (
    STATUS_FAILED,
    STATUS_PENDING_REVIEW,
    STATUS_SUCCESS,
    PublishRunResult,
    run_publish_answer_async,
)
from service.entitlement_service import check_entitlement
from service.task_run_support import (
    _print_video_summary,
    build_video_info,
    merge_video_into_result_summary,
)
from util.constants import (
    PLATFORM_KIT_MIN_VERSION,
    QUESTION_URL_PREFIXES,
    SKILL_SLUG,
    SKILL_VERSION,
    TARGET_PLATFORM,
)
from util.runtime_paths import get_skill_data_dir, get_skill_root
from util.timeutil import now_unix, unix_to_iso


def _is_mock_mode() -> bool:
    """判断是否走 mock 档位（不触网、不启动浏览器）。"""
    target = (os.getenv("OPENCLAW_TEST_TARGET") or "").strip().lower()
    return target in ("", "unit", "mock")


def _is_simulator_mode() -> bool:
    target = (os.getenv("OPENCLAW_TEST_TARGET") or "").strip().lower()
    return target == "simulator_rpa"


def _validate_run_params(
    question_url: Optional[str],
    input_id: Optional[str],
    optimize: bool = False,
) -> Optional[tuple[str, str]]:
    """校验必填参数。返回 (error_message, error_code) 或 None。

    Args:
        question_url: 问题 URL
        input_id: 回答文稿路径（optimize 模式下允许为空，由 AI 生成）
        optimize: 是否启用 AI 优化
    """
    if not question_url:
        return "缺少必填参数 --question-url（百度知道问题页 URL）", "QUESTION_URL_EMPTY"
    if not input_id and not optimize:
        return "缺少必填参数 --input-id（本地回答文稿路径；--optimize 模式下可省略）", "ANSWER_PATH_EMPTY"
    url = question_url.strip()
    if not url.startswith(QUESTION_URL_PREFIXES):
        return (
            f"问题 URL 必须形如 https://zhidao.baidu.com/question/XXXXXXX（当前：{url}）",
            "QUESTION_URL_INVALID",
        )
    if input_id and not os.path.isfile(input_id):
        return f"回答文稿不存在：{input_id}", "ANSWER_FILE_NOT_FOUND"
    return None


def _build_result_payload(
    run_result: PublishRunResult,
    publish_record_id: Optional[int],
    duplicate: bool,
) -> Dict[str, Any]:
    """按 SKILL.md 契约构造 stdout JSON。"""
    return {
        "ok": run_result.success,
        "account_id": run_result.account_id,
        "question_url": run_result.question_url,
        "answer_path": run_result.answer_path,
        "status": run_result.status,
        "platform_message": run_result.platform_message,
        "publish_record_id": publish_record_id,
        "duplicate": duplicate,
        "error": (
            {
                "code": run_result.error.code,
                "message": run_result.error.message,
                "stage": run_result.error.stage,
            }
            if run_result.error
            else None
        ),
    }


async def _run_mock(
    question_url: str,
    input_id: str,
    target: Optional[str],
    idempotency_key: str,
) -> tuple[int, Dict[str, Any], Optional[int], bool]:
    """mock 档位：不触网，模拟成功结果，用于 CI 与开发联调。"""
    batch_id = uuid.uuid4().hex[:12]
    data_dir = get_skill_data_dir()

    async with RpaVideoSession(
        skill_slug=SKILL_SLUG,
        skill_data_dir=data_dir,
        batch_id=batch_id,
        title=f"开始发布回答（mock）问题={question_url}",
        closing_title="mock 发布流程完成",
    ) as video:
        video.add_step("mock 模式：跳过浏览器与 account-manager")
        video.add_step(f"问题 URL：{question_url}")
        video.add_step(f"回答文稿：{input_id}")
        video.add_step("mock 模式：模拟发布成功")

    video_summary = video.summary()
    video_info = build_video_info(video_summary, {}, {})

    # mock：用虚拟账号 ID
    account_id = target or "mock-account"
    run_result = PublishRunResult(
        success=True,
        status=STATUS_SUCCESS,
        platform_message="[mock] 提交成功",
        account_id=str(account_id),
        question_url=question_url,
        answer_path=input_id,
    )

    # 写发布记录（mock 也写，便于幂等预检测试）
    record_id, duplicate = apr.save_publish_record(
        idempotency_key=idempotency_key or None,
        account_id=str(account_id),
        question_url=question_url,
        answer_path=input_id,
        status=run_result.status,
        platform_message=run_result.platform_message,
        published_at=now_unix(),
    )

    payload = _build_result_payload(run_result, record_id, duplicate)
    payload["video"] = video_info
    return 0, payload, record_id, duplicate


async def _run_real(
    question_url: str,
    input_id: str,
    target: Optional[str],
    idempotency_key: str,
    optimize: bool = False,
    auto_approve: bool = False,
) -> tuple[int, Dict[str, Any], Optional[int], bool]:
    """real_rpa / simulator_rpa 档位：走真实浏览器流程。"""
    batch_id = uuid.uuid4().hex[:12]
    data_dir = get_skill_data_dir()
    lease_token: Optional[str] = None
    account: Optional[Dict[str, Any]] = None

    try:
        # 步 1：账号租约（account-manager 失败时自动 fallback 到直接 profile 模式）
        account = pick_web_account_with_fallback(TARGET_PLATFORM, target)
        lease_token = account.get("lease_token")
        if account.get("fallback"):
            # fallback 时记录警告，便于运维识别
            print(
                "[警告] account-manager 不可用，已自动 fallback 到直接 profile 模式。"
                f"profile_dir={account.get('profile_dir')}",
                flush=True,
            )

        async with RpaVideoSession(
            skill_slug=SKILL_SLUG,
            skill_data_dir=data_dir,
            batch_id=batch_id,
            title=f"开始发布回答 问题={question_url}",
            closing_title="发布流程完成",
        ) as video:
            video.add_step(f"使用账号：{account.get('id') or account.get('account_id')}")
            video.add_step(f"问题 URL：{question_url}")
            video.add_step(f"回答文稿：{input_id}")

            run_result: PublishRunResult = await run_publish_answer_async(
                account,
                question_url,
                input_id,
                idempotency_key=idempotency_key,
                step_callback=lambda msg: video.add_step(msg),
                optimize=optimize,
                auto_approve=auto_approve,
            )

            video.add_step(f"发布状态：{run_result.status}")

        video_summary = video.summary()
        video_info = build_video_info(video_summary, {}, {})

        # 步 21：写 answer_publish_records
        record_id: Optional[int] = None
        duplicate = False
        if run_result.success or run_result.status in (STATUS_SUCCESS, STATUS_PENDING_REVIEW):
            record_id, duplicate = apr.save_publish_record(
                idempotency_key=idempotency_key or None,
                account_id=run_result.account_id,
                question_url=run_result.question_url,
                answer_path=run_result.answer_path,
                status=run_result.status,
                platform_message=run_result.platform_message,
                published_at=now_unix(),
            )
        else:
            # 失败也记录一条（便于排查），但不占用幂等键（用 NULL idempotency_key）
            record_id, duplicate = apr.save_publish_record(
                idempotency_key=None,
                account_id=run_result.account_id,
                question_url=run_result.question_url,
                answer_path=run_result.answer_path,
                status=run_result.status,
                platform_message=run_result.platform_message,
                published_at=None,
            )

        payload = _build_result_payload(run_result, record_id, duplicate)
        payload["video"] = video_info
        return (0 if run_result.success else 1), payload, record_id, duplicate

    except AccountManagerError as exc:
        # 账号准备失败
        run_result = PublishRunResult(
            success=False,
            status=STATUS_FAILED,
            platform_message=exc.message,
            account_id="",
            question_url=question_url,
            answer_path=input_id,
            error=None,
        )
        # 失败记录（不占幂等键）
        record_id, duplicate = apr.save_publish_record(
            idempotency_key=None,
            account_id="",
            question_url=question_url,
            answer_path=input_id,
            status=STATUS_FAILED,
            platform_message=f"{exc.code}: {exc.message}",
            published_at=None,
        )
        payload = _build_result_payload(run_result, record_id, duplicate)
        payload["error"] = {"code": exc.code, "message": exc.message, "stage": "account_prepare"}
        return 1, payload, record_id, duplicate
    finally:
        release_lease(lease_token)


def cmd_run(
    target: Optional[str] = None,
    input_id: Optional[str] = None,
    question_url: Optional[str] = None,
    idempotency_key: Optional[str] = None,
    optimize: bool = False,
    auto_approve: bool = False,
) -> int:
    """百度知道回答发布入口。"""
    # 鉴权
    ok, reason = check_entitlement(SKILL_SLUG)
    if not ok:
        print(f"❌ {reason}")
        return 1

    # 参数校验
    err = _validate_run_params(question_url, input_id, optimize=optimize)
    if err is not None:
        err_msg, err_code = err
        print(json.dumps({
            "ok": False,
            "error": {"code": err_code, "message": err_msg},
        }, ensure_ascii=False))
        return 1

    question_url = question_url.strip()
    input_id = (input_id or "").strip()
    idempotency_key = (idempotency_key or "").strip() or None

    # 幂等预检：若 idempotency_key 已存在，直接返回已有记录
    if idempotency_key:
        existing = apr.find_by_idempotency_key(idempotency_key)
        if existing is not None:
            existing_id, _, acct_id, q_url, a_path, status, msg, pub_at, cat, _ = existing
            payload = {
                "ok": status in (STATUS_SUCCESS, STATUS_PENDING_REVIEW),
                "account_id": acct_id,
                "question_url": q_url,
                "answer_path": a_path,
                "status": status,
                "platform_message": msg or "",
                "publish_record_id": int(existing_id),
                "duplicate": True,
            }
            print(json.dumps(payload, ensure_ascii=False))
            tlr.save_task_log(
                task_type="publish",
                target_id=acct_id,
                input_id=str(existing_id),
                input_title=f"幂等命中：{idempotency_key}",
                status="success" if status != STATUS_FAILED else "failed",
                error_msg=None,
                result_summary=json.dumps(payload, ensure_ascii=False),
            )
            return 0 if status != STATUS_FAILED else 1

    # 档位分流
    if _is_mock_mode():
        rc, payload, record_id, _ = asyncio.run(
            _run_mock(question_url, input_id, target, idempotency_key or "")
        )
    else:
        rc, payload, record_id, _ = asyncio.run(
            _run_real(
                question_url, input_id, target, idempotency_key or "",
                optimize=optimize, auto_approve=auto_approve,
            )
        )

    # 打印录屏信息
    video_info = payload.get("video") or {}
    _print_video_summary(video_info)

    # 写 task_logs
    summary_payload = merge_video_into_result_summary(
        {
            "question_url": question_url,
            "answer_path": input_id,
            "status": payload.get("status"),
            "publish_record_id": record_id,
        },
        video_info,
    )
    tlr.save_task_log(
        task_type="publish",
        target_id=payload.get("account_id") or "",
        input_id=str(record_id) if record_id else input_id,
        input_title=f"百度知道回答发布：{question_url}",
        status="success" if payload.get("ok") else "failed",
        error_msg=(payload.get("error") or {}).get("message") if not payload.get("ok") else None,
        result_summary=json.dumps(summary_payload, ensure_ascii=False),
    )

    # stdout 输出业务 JSON（不包含 video 字段，避免过长）
    output_payload = {k: v for k, v in payload.items() if k != "video"}
    print(json.dumps(output_payload, ensure_ascii=False))
    return rc


def cmd_logs(
    limit: int = 10,
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    target_id: Optional[str] = None,
) -> int:
    if limit <= 0:
        limit = 10
    rows = tlr.list_task_logs(limit, status, task_type, target_id)
    if not rows:
        print("暂无任务日志")
        return 0

    sep_line = "_" * 39
    for idx, r in enumerate(rows):
        rid, ttype, tid, iid, ititle, st, err, rsum, cat, uat = r
        print(f"id：{rid}")
        print(f"task_type：{ttype or ''}")
        print(f"target_id：{tid or ''}")
        print(f"input_id：{iid or ''}")
        print(f"input_title：{ititle or ''}")
        print(f"status：{st or ''}")
        print(f"error_msg：{err or ''}")
        print(f"result_summary：{rsum or ''}")
        print(f"created_at：{unix_to_iso(cat) or str(cat or '')}")
        print(f"updated_at：{unix_to_iso(uat) or str(uat or '')}")
        if idx != len(rows) - 1:
            print(sep_line)
            print()
    return 0


def cmd_log_get(log_id: str) -> int:
    if not str(log_id).isdigit():
        print("❌ log_id 必须是数字")
        return 1
    row = tlr.get_task_log_by_id(int(log_id))
    if not row:
        print("❌ 没有这条任务日志")
        return 1
    rid, ttype, tid, iid, ititle, st, err, rsum, cat, uat = row
    print(
        json.dumps(
            {
                "id": int(rid),
                "task_type": ttype,
                "target_id": tid,
                "input_id": iid,
                "input_title": ititle,
                "status": st,
                "error_msg": err,
                "result_summary": rsum,
                "created_at": unix_to_iso(cat),
                "updated_at": unix_to_iso(uat),
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_config_path() -> int:
    example_path = os.path.join(get_skill_root(), ".env.example")
    env_path = config.get_env_file_path() or ""
    print(
        json.dumps(
            {
                "skill": SKILL_SLUG,
                "env_path": env_path,
                "example_path": os.path.abspath(example_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_health() -> int:
    runtime = collect_runtime_diagnostics(
        skill_slug=SKILL_SLUG,
        platform_kit_min_version=PLATFORM_KIT_MIN_VERSION,
        skill_root=get_skill_root(),
    )
    example_path = os.path.join(get_skill_root(), ".env.example")
    env_path = config.get_env_file_path() or ""
    env_exists = bool(env_path and os.path.isfile(env_path))

    health_status = "failed" if runtime.has_fatal_issues else "ok"
    lines = [
        f"{SKILL_SLUG} health: {health_status}",
        *format_runtime_health_lines(runtime),
        f"env_path: {env_path}",
        f"env_exists: {env_exists}",
        f"example_path: {os.path.abspath(example_path)}",
    ]
    for line in lines:
        print(line)
    return 1 if runtime.has_fatal_issues else 0


def cmd_version() -> int:
    print(json.dumps({"version": SKILL_VERSION, "skill": SKILL_SLUG}, ensure_ascii=False))
    return 0
