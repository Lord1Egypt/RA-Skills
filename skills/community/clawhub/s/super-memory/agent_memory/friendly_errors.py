"""Human-friendly error messages for Agent Memory."""

# Map internal error patterns to user-friendly messages
ERROR_MESSAGES = {
    "content_too_short": {
        "message": "内容太短，无法形成有意义的记忆。",
        "tip": "尝试写几个词来描述你想记住的内容。",
    },
    "empty_content": {
        "message": "无法记住空内容。",
        "tip": "确保内容至少包含1个非空白字符。",
    },
    "duplicate_skipped": {
        "message": "这条记忆已经存在了。",
        "tip": "如果想修改已有记忆，请使用 update() 方法。",
    },
    "circuit_open": {
        "message": "记忆系统暂时不可用（熔断器已开启）。",
        "tip": "请稍后重试，系统会自动恢复。",
    },
    "quota_exceeded": {
        "message": "记忆容量已满。",
        "tip": "删除一些旧记忆，或升级套餐获取更多存储空间。",
    },
    "cooldown_active": {
        "message": "写入太快了，请慢一点。",
        "tip": "在同一主题下写入记忆时，请间隔几秒。",
    },
    "filtered": {
        "message": "记忆被过滤，未存储。",
        "tip": "内容可能与已有记忆太相似，或未通过质量检查。",
    },
    "tenant_not_found": {
        "message": "租户不存在。",
        "tip": "请确保租户已注册后再使用。",
    },
    "permission_denied": {
        "message": "权限不足。",
        "tip": "请确认你有执行此操作所需的权限级别。",
    },
    "backup_failed": {
        "message": "备份创建失败。",
        "tip": "请检查磁盘空间和备份目录的文件权限。",
    },
    "restore_failed": {
        "message": "从备份恢复失败。",
        "tip": "请确保备份文件存在且未损坏。",
    },
}


def get_friendly_error(error_key: str, details: str = "") -> dict:
    """Get a human-friendly error message.

    Args:
        error_key: Internal error identifier
        details: Additional error details

    Returns:
        {"message": str, "tip": str, "details": str}
    """
    template = ERROR_MESSAGES.get(error_key, {
        "message": f"发生错误：{error_key}",
        "tip": "请查看日志获取更多详情。",
    })
    return {
        "message": template["message"],
        "tip": template["tip"],
        "details": details,
    }
