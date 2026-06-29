from __future__ import annotations

from typing import Any


CARD_VERSION = "paper-kb-card-v1"


def option(label: str, value: str, description: str = "", style: str = "default") -> dict[str, Any]:
    return {
        "label": label,
        "value": value,
        "description": description,
        "style": style,
    }


def card(
    card_id: str,
    title: str,
    summary: str,
    actions: list[dict[str, Any]] | None = None,
    hidden: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "type": "feishu_interactive_card",
        "version": CARD_VERSION,
        "card_id": card_id,
        "title": title,
        "summary": summary,
        "fallback_text": summary,
        "actions": actions or [],
        "hidden": hidden or {},
        "callback_contract": {
            "action_value_field": "CardActionValue",
            "form_values_field": "CardFormValues",
            "hidden_fields_included": True,
        },
    }


def incremental_confirm(task_id: str, source_label: str, change_count: int) -> dict[str, Any]:
    return card(
        "scan.incremental.confirm",
        "确认增量编译",
        f"资料源「{source_label}」发现 {change_count} 个变化，超过自动处理上限。请选择是否开始增量编译。",
        actions=[
            option("开始增量编译", f"confirm_incremental:{task_id}", "确认后会创建增量 job", "primary"),
            option("取消", f"cancel_incremental:{task_id}", "保留资料源，不执行本次更新", "danger"),
        ],
        hidden={"task_id": task_id},
    )


def no_updates(source_label: str) -> dict[str, Any]:
    return card(
        "scan.no_updates",
        "没有发现更新",
        f"资料源「{source_label}」目前没有新增、修改或删除文件。",
    )
