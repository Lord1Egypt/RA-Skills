"""
WPS Office 全家桶 - 智能错误处理模块 v2.2

错误ID系统（E001-E015）：
  E001-E010: 用户可自助解决（有明确操作步骤）
  E011-E015: 需要进一步排查或联系支持

每个错误ID包含：
  - 错误描述（中文）
  - 可能原因
  - 解决步骤（分步骤）
  - 是否可自动修复（auto/manual）
"""
from typing import Dict, Optional

# ==================== 错误ID映射表 ====================

ERROR_MAP: Dict[str, Dict] = {
    # ---- 用户可自助解决 ----
    "E001": {
        "code": "E001",
        "title": "WPS 未安装或 COM 注册失败",
        "description": "系统没有安装 WPS Office，或安装后未重启电脑",
        "cause": "WPS COM 组件未注册到系统",
        "solution": [
            "1. 安装 WPS Office 2019+ 或 WPS 365",
            "2. 安装后必须重启电脑（重要！）",
            "3. 重启后验证：python scripts/wps_test.py",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E002": {
        "code": "E002",
        "title": "python-docx 未安装",
        "description": "纯Python模式需要 python-docx 库",
        "cause": "未安装依赖包",
        "solution": [
            "pip install python-docx",
            "pip install openpyxl     # Excel 也需要",
            "pip install python-pptx  # PPT 也需要",
        ],
        "auto_fixable": True,
        "auto_command": "pip install python-docx openpyxl python-pptx",
        "severity": "warning",
    },
    "E003": {
        "code": "E003",
        "title": "文件路径不存在或无法访问",
        "description": "指定的文件路径不存在，或没有访问权限",
        "cause": "中文路径编码错误、路径拼写错误、权限不足",
        "solution": [
            "1. 检查路径是否正确",
            "2. 中文路径建议改用英文路径，如 D:\\docs\\report.docx",
            "3. 或以管理员身份运行命令行",
            "4. 使用纯Python模式：python scripts/wps_word.py create",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E004": {
        "code": "E004",
        "title": "格式转换失败（纯Python模式不支持）",
        "description": "当前引擎不支持格式转换（如 Word → PDF）",
        "cause": "纯Python模式不提供格式转换能力",
        "solution": [
            "1. 安装 WPS Office 自动获得转换能力",
            "2. 或安装 LibreOffice：https://www.libreoffice.org/",
            "3. 纯Python模式仅支持创建和编辑",
        ],
        "auto_fixable": False,
        "severity": "warning",
    },
    "E005": {
        "code": "E005",
        "title": "排序/筛选/图表需要 WPS 模式",
        "description": "该功能仅在 WPS 模式下可用，当前引擎不支持",
        "cause": f"当前引擎不支持高级功能",
        "solution": [
            "1. 安装 WPS Office 2019+",
            "2. 安装后重启电脑",
            "3. 验证：python scripts/wps_test.py",
        ],
        "auto_fixable": False,
        "severity": "warning",
    },
    "E006": {
        "code": "E006",
        "title": "WPS/LibreOffice 卡住无响应",
        "description": "WPS 或 LibreOffice 进程长时间无响应（超过 60 秒）",
        "cause": "WPS 偶尔会因插件冲突或内存不足卡住",
        "solution": [
            "1. 等待 60 秒（子进程超时保护会自动终止）",
            "2. 如仍卡住，打开任务管理器 → 结束 WPS 进程",
            "3. 更新 WPS 到最新版",
            "4. 关闭 WPS 中不用的插件",
        ],
        "auto_fixable": True,
        "auto_action": "kill_process",
        "severity": "warning",
    },
    "E007": {
        "code": "E007",
        "title": "权限不足",
        "description": "没有写入或修改文件的权限",
        "cause": "文件只读、被其他程序占用、或用户权限不足",
        "solution": [
            "Windows：右键命令行 → 以管理员身份运行",
            "macOS/Linux：命令前加 sudo",
            "2. 检查文件是否被其他程序占用",
            "3. 检查文件属性是否为只读",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E008": {
        "code": "E008",
        "title": "pywin32 导入失败",
        "description": "pywin32 库安装错误或架构不匹配",
        "cause": "32位Python安装了64位pywin32，或反之",
        "solution": [
            "1. 卸载重装：pip uninstall pywin32 && pip install pywin32",
            "2. 确保 Python 和 pywin32 位数一致（都用64位）",
            "3. 如仍失败，使用纯Python模式：pip install python-docx",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E009": {
        "code": "E009",
        "title": "Python 版本过低",
        "description": "需要 Python 3.8 或更高版本",
        "cause": "当前 Python 版本低于 3.8",
        "solution": [
            "python --version  # 检查当前版本",
            "从 https://www.python.org/downloads/ 下载 3.8+",
            "或使用 conda/venv 创建新环境",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E010": {
        "code": "E010",
        "title": "当前引擎不支持此功能",
        "description": f"该功能需要更高版本的引擎（WPS/MS Office）",
        "cause": f"当前引擎为纯 Python 或 LibreOffice，功能受限",
        "solution": [
            "1. 安装 WPS Office 获得完整功能",
            "2. 或安装 LibreOffice 增加转换能力",
            "3. 使用 info 命令查看当前引擎能力",
        ],
        "auto_fixable": False,
        "severity": "warning",
    },
    # ---- 需要进一步排查 ----
    "E011": {
        "code": "E011",
        "title": "LibreOffice 未安装",
        "description": "系统未安装 LibreOffice，无法使用 Headless 转换",
        "cause": "LibreOffice 不在系统 PATH 中",
        "solution": [
            "1. 下载 LibreOffice：https://www.libreoffice.org/",
            "2. 安装时勾选 '添加到 PATH'",
            "3. 安装后重启命令行",
        ],
        "auto_fixable": False,
        "severity": "warning",
    },
    "E012": {
        "code": "E012",
        "title": "LibreOffice 转换失败",
        "description": "LibreOffice Headless 执行出错",
        "cause": "文件损坏、格式不支持、路径问题",
        "solution": [
            "1. 检查源文件是否能用 WPS/LibreOffice 手动打开",
            "2. 文件路径避免中文和特殊字符",
            "3. 查看详细错误信息：soffice --headless 命令手动运行",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E013": {
        "code": "E013",
        "title": "文件不存在",
        "description": "指定的文件或路径不存在",
        "cause": "路径拼写错误、文件被删除、权限不足",
        "solution": [
            "1. 检查路径是否正确：{path}",
            "2. 确认文件未被删除或移动",
            "3. 确认有访问权限",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E014": {
        "code": "E014",
        "title": "未知运行时错误",
        "description": "执行过程中出现意外错误",
        "cause": "详见 detail 字段",
        "solution": [
            "1. 查看详细错误信息",
            "2. 运行环境自检：python scripts/wps_test.py",
            "3. 如仍无法解决，请提交反馈：python scripts/wps_feedback.py email",
        ],
        "auto_fixable": False,
        "severity": "error",
    },
    "E015": {
        "code": "E015",
        "title": "不支持的操作或格式",
        "description": "请求的操作或输出格式在当前环境下不受支持",
        "cause": "引擎能力限制或文件格式问题",
        "solution": [
            "1. 检查输出格式是否正确（如 pdf、txt、html）",
            "2. 使用 info 命令查看文件信息",
            "3. 安装 WPS 获得完整能力",
        ],
        "auto_fixable": False,
        "severity": "warning",
    },
}


def get_error(error_id: str) -> Dict:
    """获取错误详情"""
    return ERROR_MAP.get(error_id, ERROR_MAP["E014"])


def wps_error(error_id: str, **kwargs) -> str:
    """
    根据错误ID返回格式化的中文错误信息。
    
    用法:
      wps_error("E005")  # 基础错误
      wps_error("E013", path="D:\\docs\\report.docx")  # 带参数
      wps_error("E014", detail="COM timeout after 30s")  # 带详细描述
    """
    err = get_error(error_id)
    msg_parts = [
        f"【{err['code']}】{err['title']}",
        f"描述: {err['description']}",
    ]

    # 动态参数替换
    if "path" in kwargs:
        for key, val in kwargs.items():
            msg_parts.append(f"{key}: {val}")

    if "engine" in kwargs:
        msg_parts.append(f"当前引擎: {kwargs['engine']}")

    if "feature" in kwargs:
        msg_parts.append(f"涉及功能: {kwargs['feature']}")

    if "detail" in kwargs:
        msg_parts.append(f"详情: {kwargs['detail']}")

    # 解决步骤
    if err.get("solution"):
        msg_parts.append("解决步骤:")
        for step in err["solution"]:
            msg_parts.append(f"  {step}")

    return "\n".join(msg_parts)


def is_auto_fixable(error_id: str) -> bool:
    """判断错误是否可自动修复"""
    return ERROR_MAP.get(error_id, {}).get("auto_fixable", False)


def get_auto_command(error_id: str) -> Optional[str]:
    """获取自动修复命令"""
    err = ERROR_MAP.get(error_id, {})
    return err.get("auto_command")


def list_all_errors() -> list:
    """返回所有错误ID列表（供文档生成用）"""
    return [
        {
            "code": v["code"],
            "title": v["title"],
            "severity": v["severity"],
            "auto_fixable": v["auto_fixable"],
        }
        for v in ERROR_MAP.values()
    ]


if __name__ == "__main__":
    import sys
    eid = sys.argv[1] if len(sys.argv) > 1 else "E001"
    print(wps_error(eid))
