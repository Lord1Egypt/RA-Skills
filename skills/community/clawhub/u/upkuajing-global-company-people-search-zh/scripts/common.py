"""
跨境魔方API脚本公共工具
"""
import os
import json
import sys
import uuid
import time
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
import httpx
from version_check import check_and_notify

# API配置
API_BASE_URL = "https://openapi.upkuajing.com"
API_KEY_ENV = "UPKUAJING_API_KEY"
UPKUAJING_DIR = Path.home() / '.upkuajing'
UPKUAJING_ENV_FILE = UPKUAJING_DIR / '.env'
UPKUAJING_LOGS_DIR = UPKUAJING_DIR / 'logs'

# 日志开关
ENABLE_API_LOGGING = False  # 设置为 False 可关闭API日志记录

# 请求配置
API_TIMEOUT = 120.0  # API 请求超时时间（秒），列表查询可能较慢
API_CONNECT_TIMEOUT = 10.0  # 连接超时时间（秒）

# 套餐计费配置
PLAN_MODE_ENV = "UPKUAJING_PLAN_MODE"
IDEMPOTENCY_KEY_ENV = "UPKUAJING_IDEMPOTENCY_KEY"
# 支持套餐计费的接口前缀：/agent/search/**、/agent/customs/**、/agent/map/**
PLAN_SUPPORTED_PREFIXES = ("/agent/search/", "/agent/customs/", "/agent/map/")
PLAN_MODE_BALANCE = 1  # 余额计费
PLAN_MODE_PLAN = 2  # 套餐计费
EXIT_PLAN_UNAVAILABLE = 3  # 套餐不可用，需用户确认是否改用余额

# 技能目录配置
SKILL_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK_DATA_DIR = os.path.join(SKILL_BASE_DIR, 'task_data')


# API错误码定义
class APIErrorCode:
    """跨境魔方API错误码常量"""
    UNKNOWN_ERROR = 99  # 系统繁忙
    REQUEST_PARAM_ERROR = 98  # 请求参数错误
    REQUEST_METHOD_ERROR = 97  # 请求方式错误
    REQUEST_AUTH_ERROR = 96  # 认证错误
    SEARCH_BALANCE_NOT_ENOUGH = 95  # 余额不足
    PLAN_NOT_SUPPORTED = 1003  # 接口不支持套餐计费
    PLAN_NOT_AVAILABLE = 1004  # 无有效套餐
    PLAN_QUOTA_EXHAUSTED = 1005  # 套餐额度已用完


# API错误码映射表
API_ERROR_MESSAGES = {
    APIErrorCode.UNKNOWN_ERROR: "系统繁忙，请稍后重试",
    APIErrorCode.REQUEST_PARAM_ERROR: "请求参数错误，请检查参数名称和值",
    APIErrorCode.REQUEST_METHOD_ERROR: "请求方式错误，请使用正确的HTTP方法",
    APIErrorCode.REQUEST_AUTH_ERROR: "认证错误，请检查API密钥是否有效",
    APIErrorCode.SEARCH_BALANCE_NOT_ENOUGH: "余额不足，请充值后继续使用",
    APIErrorCode.PLAN_NOT_SUPPORTED: "接口不支持套餐计费，请勿传 planMode=2",
    APIErrorCode.PLAN_NOT_AVAILABLE: "当前账号无有效套餐，请先购买套餐",
    APIErrorCode.PLAN_QUOTA_EXHAUSTED: "套餐额度已用完，可稍后重试或改用API余额",
}

# API错误处理建议
API_ERROR_SUGGESTIONS = {
    APIErrorCode.REQUEST_AUTH_ERROR: f"请检查环境变量 {API_KEY_ENV} 或文件 {UPKUAJING_ENV_FILE} 中的API密钥是否正确",
    APIErrorCode.SEARCH_BALANCE_NOT_ENOUGH: "请运行 auth.py --new_rec_order 创建充值订单",
    APIErrorCode.REQUEST_PARAM_ERROR: "请参考 references/ 目录下的API文档检查参数格式",
    APIErrorCode.PLAN_NOT_SUPPORTED: "该接口固定按余额计费，移除 planMode 参数后重试",
    APIErrorCode.PLAN_QUOTA_EXHAUSTED: f"可等待额度恢复，或设置 {PLAN_MODE_ENV}={PLAN_MODE_BALANCE} 改用API余额",
}


def load_env_file() -> Dict[str, str]:
    """
    从 ~/.upkuajing/.env 文件加载环境变量。

    Returns:
        环境变量字典
    """
    env_vars = {}
    if UPKUAJING_ENV_FILE.exists():
        with open(UPKUAJING_ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def get_api_key() -> str:
    """
    获取API密钥，优先从环境变量，其次从 ~/.upkuajing/.env 文件。
    """
    # 优先从环境变量获取
    api_key = os.environ.get(API_KEY_ENV)

    # 如果环境变量没有，尝试从 ~/.upkuajing/.env 读取
    if not api_key:
        env_vars = load_env_file()
        api_key = env_vars.get(API_KEY_ENV)

    if not api_key:
        print(
            f"错误：未找到API密钥。\n"
            f"请设置环境变量 {API_KEY_ENV}，\n"
            f"或在 {UPKUAJING_ENV_FILE} 文件中添加：{API_KEY_ENV}=your_api_key_here",
            file=sys.stderr
        )
        sys.exit(1)
    return api_key


def log_request(endpoint: str, request_data: dict) -> None:
    """
    记录API请求入参到日志文件。

    Args:
        endpoint: API端点路径
        request_data: 请求数据字典
    """
    # 检查日志开关
    if not ENABLE_API_LOGGING:
        return

    try:
        # 确保日志目录存在
        UPKUAJING_LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # 生成日志文件名（年-月-日.log）
        log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
        log_file = UPKUAJING_LOGS_DIR / log_filename

        # 构建日志内容
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'type': 'request',
            'endpoint': endpoint,
            'data': request_data
        }

        # 写入日志文件（追加模式）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    except Exception as e:
        # 日志记录失败不应该影响主流程，静默处理
        pass


def log_response(endpoint: str, response_data: dict, duration: float) -> None:
    """
    记录API响应出参到日志文件。

    Args:
        endpoint: API端点路径
        response_data: 响应数据字典
        duration: 请求耗时（秒）
    """
    # 检查日志开关
    if not ENABLE_API_LOGGING:
        return

    try:
        # 确保日志目录存在
        UPKUAJING_LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # 生成日志文件名（年-月-日.log）
        log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
        log_file = UPKUAJING_LOGS_DIR / log_filename

        # 构建日志内容
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'type': 'response',
            'endpoint': endpoint,
            'duration_seconds': round(duration, 3),
            'data': response_data
        }

        # 写入日志文件（追加模式）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    except Exception as e:
        # 日志记录失败不应该影响主流程，静默处理
        pass


def make_request(
        endpoint: str,
        params: Dict[str, Any],
        api_key: Optional[str] = None,
        require_auth: bool = True
) -> Dict[str, Any]:
    """
    向跨境魔方API发起HTTP请求。

    套餐计费：支持套餐的接口默认携带 planMode=2。套餐不可用时输出确认信息并以
    退出码 3 结束，不会自动降级为余额计费。

    Args:
        endpoint: API端点路径
        params: 请求参数字典
        api_key: API密钥（如果为None且require_auth=True，将从环境变量获取）
        require_auth: 是否需要Bearer令牌认证，默认为True
    """
    # 版本检测
    check_and_notify(API_BASE_URL)

    if require_auth and api_key is None:
        api_key = get_api_key()

    # 复制入参再注入 planMode：分页脚本会把 params 持久化到任务元数据，
    # 不能把本次计费模式写进调用方对象。
    request_params = dict(params) if isinstance(params, dict) else params
    plan_mode = resolve_plan_mode(endpoint, request_params)
    if isinstance(request_params, dict):
        request_params.pop("planMode", None)
        if plan_mode:
            if is_plan_supported(endpoint):
                request_params["planMode"] = plan_mode
            else:
                # 仅当调用方显式传了 planMode 才提示；会话级环境变量对不支持套餐的接口静默生效为「不传」
                if isinstance(params, dict) and "planMode" in params:
                    print(
                        f"[提示] 接口 {endpoint} 不支持套餐计费，已忽略 planMode={plan_mode}",
                        file=sys.stderr
                    )
                plan_mode = None

    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json"
    }

    # 只有在需要认证时才添加 Authorization 头
    if require_auth:
        headers["Authorization"] = f"Bearer {api_key}"

    # 网络超时后的重试复用同一个幂等键，避免重复计费
    idempotency_key = os.environ.get(IDEMPOTENCY_KEY_ENV)
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key

    try:
        # 分别设置连接超时和读取超时
        timeout_config = httpx.Timeout(API_TIMEOUT, connect=API_CONNECT_TIMEOUT)
        with httpx.Client(timeout=timeout_config) as client:
            # 记录请求开始时间
            start_time = time.time()

            # 记录入参日志（请求前）
            log_request(endpoint, {'params': request_params})

            response = client.post(url, json=request_params, headers=headers)

            # 计算请求耗时
            duration = time.time() - start_time

            # 先解析 JSON，以便记录日志
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {}

            # 记录出参日志（请求后）
            log_response(endpoint, {'response': data, 'status_code': response.status_code}, duration)

            # 套餐不可用：输出确认信息并以退出码 3 结束，由调用方询问用户
            plan_unavailable = build_plan_unavailable(
                endpoint, request_params, plan_mode, response.status_code, data,
                retry_after_header=response.headers.get("Retry-After")
            )
            if plan_unavailable:
                emit_plan_unavailable(plan_unavailable)

            # 再检查 HTTP 状态
            response.raise_for_status()

            # 检查API级别的错误  0表示成功，非0代表错误
            if data.get("code") != 0:
                code = data.get("code")
                if code == APIErrorCode.REQUEST_PARAM_ERROR and plan_mode == PLAN_MODE_PLAN:
                    print(
                        "[提示] 参数错误可能与 planMode=2 有关，可设置 "
                        f"{PLAN_MODE_ENV}={PLAN_MODE_BALANCE} 改用余额重试",
                        file=sys.stderr
                    )
                elif code == APIErrorCode.SEARCH_BALANCE_NOT_ENOUGH:
                    print(
                        "[提示] 余额不足，请引导用户充值（python scripts/auth.py --new_rec_order）",
                        file=sys.stderr
                    )
                elif code == APIErrorCode.PLAN_NOT_SUPPORTED:
                    print(
                        "[提示] 该接口不支持套餐计费，请移除 planMode 后重试",
                        file=sys.stderr
                    )
                # 不再自动退出，返回错误响应让调用者处理
                return data

            # 套餐计费成功时输出本次用量，便于调用方转述给用户
            notify_plan_usage(data.get("usage"))

            return data

    except httpx.HTTPStatusError as e:
        print(f"HTTP错误：{e.response.status_code}", file=sys.stderr)
        print(f"响应：{e.response.text}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"网络错误：无法连接到API服务器", file=sys.stderr)
        print(f"详细信息：{str(e)}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误：API返回的JSON无效", file=sys.stderr)
        sys.exit(1)


def is_plan_supported(endpoint: str) -> bool:
    """判断接口是否支持套餐计费（/agent/search/**、/agent/customs/**、/agent/map/**）。"""
    return any(endpoint.startswith(prefix) for prefix in PLAN_SUPPORTED_PREFIXES)


def _parse_plan_mode(value: Any) -> Optional[int]:
    """
    解析 planMode 取值。

    Returns:
        1=余额计费，2=套餐计费，0=显式不传，None=未设置或非法值
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value in (0, PLAN_MODE_BALANCE, PLAN_MODE_PLAN) else None
    text = str(value).strip().lower()
    if text in ("0", "", "off", "none"):
        return 0
    if text in (str(PLAN_MODE_BALANCE), str(PLAN_MODE_PLAN)):
        return int(text)
    return None


def resolve_plan_mode(endpoint: str, params: Dict[str, Any]) -> Optional[int]:
    """
    决定本次请求的 planMode 取值。

    优先级：环境变量 > 请求参数中的 planMode > 接口默认值。
    环境变量优先级最高：分页任务用 --task_id 续跑时会读取历史 params，
    必须保证用户"改用余额"的选择不会被历史 planMode 覆盖。

    Returns:
        1=余额计费，2=套餐计费，0/None=不传 planMode
    """
    env_mode = _parse_plan_mode(os.environ.get(PLAN_MODE_ENV))
    if env_mode is not None:
        return env_mode

    param_mode = _parse_plan_mode(params.get("planMode")) if isinstance(params, dict) else None
    if param_mode is not None:
        return param_mode

    return PLAN_MODE_PLAN if is_plan_supported(endpoint) else None


def _to_timestamp(value: Any) -> Optional[int]:
    """把 resetsAt 统一成秒级时间戳（兼容秒与毫秒）。"""
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return None
    return number // 1000 if number > 10 ** 12 else number


def format_plan_time(value: Any) -> Optional[str]:
    """把套餐相关时间戳（秒/毫秒）格式化为本地时间字符串。"""
    timestamp = _to_timestamp(value)
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def normalize_plan_windows(windows: Any) -> list:
    """
    把套餐额度窗口统一成列表。

    服务端在不同接口分别返回列表与 {窗口名: 窗口信息} 两种形态。
    """
    if isinstance(windows, dict):
        normalized = []
        for name, window in windows.items():
            item = dict(window) if isinstance(window, dict) else {}
            item.setdefault("window", name)
            normalized.append(item)
        return normalized
    if isinstance(windows, list):
        return [dict(window) for window in windows if isinstance(window, dict)]
    return []


def format_duration(seconds: Any) -> Optional[str]:
    """把秒数转成便于阅读的中文时长。"""
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return None
    if seconds <= 0:
        return None
    if seconds < 60:
        return f"约 {seconds} 秒"
    if seconds < 3600:
        return f"约 {round(seconds / 60)} 分钟"
    if seconds < 86400:
        return f"约 {round(seconds / 3600, 1)} 小时"
    return f"约 {round(seconds / 86400, 1)} 天"


def _summarize_params(params: Dict[str, Any], limit: int = 300) -> str:
    """生成请求参数摘要，剔除游标等无意义的超长字段。"""
    if not isinstance(params, dict):
        return ""
    summary = {
        key: value
        for key, value in params.items()
        if key not in ("cursor", "pitId", "planMode")
    }
    text = json.dumps(summary, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "..."


def build_plan_unavailable(
        endpoint: str,
        params: Dict[str, Any],
        plan_mode: Optional[int],
        http_status: int,
        data: Dict[str, Any],
        retry_after_header: Any = None
) -> Optional[dict]:
    """
    识别"套餐不可用"，生成给调用方的确认信息。

    只在本次请求确实走了套餐（planMode=2）时生效，避免把普通限流误判为额度不足。
    """
    if plan_mode != PLAN_MODE_PLAN:
        return None

    code = data.get("code")
    body = data.get("data") if isinstance(data.get("data"), dict) else {}
    windows = normalize_plan_windows(body.get("windows"))
    exhausted = [window for window in windows if window.get("remaining") == 0] or windows
    # 响应体优先；缺失时回退到 Retry-After 响应头
    retry_after = body.get("retryAfter")
    if retry_after is None:
        retry_after = retry_after_header
    if isinstance(retry_after, str) and retry_after.strip().isdigit():
        retry_after = int(retry_after.strip())

    if code == APIErrorCode.PLAN_NOT_AVAILABLE:
        reason, reason_text = "no_plan", "当前账号无有效套餐"
    elif code == APIErrorCode.PLAN_QUOTA_EXHAUSTED or (
            http_status == 429 and (windows or retry_after is not None)):
        reason, reason_text = "quota_exhausted", "套餐额度已用完"
    else:
        return None

    reset_timestamps = [
        timestamp
        for timestamp in (_to_timestamp(window.get("resetsAt")) for window in exhausted)
        if timestamp
    ]

    # retryAfter 是服务端给出的"预计恢复时间"，优先使用；没有时按窗口 resetsAt 推算
    duration = format_duration(retry_after)
    if duration:
        seconds = _to_timestamp(retry_after)
        resume_at = format_plan_time(int(time.time()) + seconds) if seconds else None
    elif reset_timestamps:
        duration = format_duration(min(reset_timestamps) - int(time.time()))
        resume_at = format_plan_time(min(reset_timestamps))
    else:
        resume_at = None

    recovery = "，".join(part for part in (
        f"预计{duration}后恢复" if duration else "",
        f"恢复时间约 {resume_at}" if resume_at else "",
    ) if part)
    ask_user = (
        f"{reason_text}{'，' + recovery if recovery else ''}。"
        "是否改用API余额继续本次调用？改用余额将按接口定价扣费，"
        "可用 auth.py --price_info 查询单价。"
    )

    return {
        "status": "plan_unavailable",
        "reason": reason,
        "reasonText": reason_text,
        "httpStatus": http_status,
        "code": code,
        "endpoint": endpoint,
        "requestId": data.get("requestId"),
        "retryAfterSeconds": retry_after,
        "resumeAt": resume_at,
        "exhaustedWindows": exhausted,
        "serverHint": body.get("hint"),
        "paramsSummary": _summarize_params(params),
        "billingMode": "PLAN",
        "nextActions": ["use_balance", "retry_later", "upgrade_plan"],
        "retryWith": f"{PLAN_MODE_ENV}={PLAN_MODE_BALANCE} <同一条命令>",
        "askUser": ask_user,
    }


def emit_plan_unavailable(payload: dict) -> None:
    """
    输出套餐不可用的结构化确认信息并退出（退出码 3）。

    这里只输出信号，绝不自动改传 planMode=1：是否消耗余额必须由用户明确确认。
    """
    print("PLAN_UNAVAILABLE " + json.dumps(payload, ensure_ascii=False))
    print(f"套餐不可用：{payload.get('askUser', '')}", file=sys.stderr)
    if payload.get("requestId"):
        print(f"requestId：{payload.get('requestId')}", file=sys.stderr)
    sys.exit(EXIT_PLAN_UNAVAILABLE)


def format_plan_usage(usage: Dict[str, Any]) -> str:
    """把响应中的 usage 转成一句话套餐消耗说明。"""
    if not isinstance(usage, dict) or usage.get("billingMode") != "PLAN":
        return ""

    parts = []
    request_usage = usage.get("request")
    if isinstance(request_usage, dict) and request_usage.get("used"):
        remaining = request_usage.get("remaining")
        suffix = f"（剩余 {remaining}）" if remaining is not None else ""
        parts.append(f"{request_usage.get('quotaType') or 'REQUEST'} {request_usage.get('used')} 次{suffix}")

    for record in usage.get("records") or []:
        if not isinstance(record, dict) or not record.get("used"):
            continue
        remaining = record.get("remaining")
        suffix = f"（剩余 {remaining}）" if remaining is not None else ""
        parts.append(f"{record.get('quotaType') or 'RECORD'} {record.get('used')} 条{suffix}")

    if not parts:
        return ""
    return "本次套餐消耗：" + "，".join(parts)


def notify_plan_usage(usage: Dict[str, Any]) -> None:
    """套餐计费成功时向 stderr 输出本次消耗，供调用方转述给用户。"""
    text = format_plan_usage(usage)
    if text:
        print(f"[套餐] {text}", file=sys.stderr)


def handle_api_error(response_data: Dict[str, Any], exit_on_error: bool = True) -> None:
    """
    处理API错误响应，提供详细的错误消息。

    Args:
        response_data: API响应数据
        exit_on_error: 是否在遇到错误时退出程序（默认True）

    Returns:
        None（如果exit_on_error=True会退出程序）

    Raises:
        SystemExit: 如果exit_on_error=True且遇到错误
    """
    error_code = response_data.get("code")
    server_msg = response_data.get("msg", "")

    # 获取标准错误消息
    if error_code in API_ERROR_MESSAGES:
        standard_msg = API_ERROR_MESSAGES[error_code]
    else:
        standard_msg = server_msg or "未知错误"

    # 输出错误信息
    print(f"API错误（代码：{error_code}）：{standard_msg}", file=sys.stderr)

    # 如果服务器返回了额外的消息，也显示出来
    if server_msg and server_msg != standard_msg:
        print(f"服务器消息：{server_msg}", file=sys.stderr)

    # 提供处理建议
    if error_code in API_ERROR_SUGGESTIONS:
        print(f"建议：{API_ERROR_SUGGESTIONS[error_code]}", file=sys.stderr)

    if exit_on_error:
        sys.exit(1)


def save_to_file(data: Any, filepath: str) -> None:
    """
    将数据保存到文件，使用JSONL格式（每行一个JSON对象）。

    Args:
        data: 要保存的数据（可以是字典或列表）
        filepath: 输出文件路径
    """
    try:
        # 如果数据是列表，将每个项目写入单独的行
        if isinstance(data, list):
            with open(filepath, 'a', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        else:
            # 如果数据是单个字典，将其写入一行
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    except IOError as e:
        print(f"写入文件错误 {filepath}：{str(e)}", file=sys.stderr)
        sys.exit(1)


def parse_params(params_str: str) -> Dict[str, Any]:
    """
    解析JSON字符串参数。

    Args:
        params_str: 包含参数的JSON字符串

    Returns:
        解析后的参数字典

    Raises:
        SystemExit: 如果JSON解析失败
    """
    try:
        params = json.loads(params_str)
        if not isinstance(params, dict):
            print("错误：参数必须是JSON对象", file=sys.stderr)
            sys.exit(1)
        return params
    except json.JSONDecodeError as e:
        print(f"错误：参数中的JSON无效：{str(e)}", file=sys.stderr)
        sys.exit(1)


def print_json_output(data: Any) -> None:
    """
    将数据以格式化的JSON打印到标准输出。

    Args:
        data: 要打印的数据
    """
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ============ 任务管理函数 ============

def generate_task_id() -> str:
    """
    生成新的任务ID（UUID4格式）。

    Returns:
        任务ID字符串
    """
    return str(uuid.uuid4())


def get_task_dir(task_id: str) -> str:
    """
    获取任务目录路径（带安全验证）。

    Args:
        task_id: 任务ID（必须是有效的UUID格式）

    Returns:
        任务目录的完整路径

    Raises:
        ValueError: 如果 task_id 不是有效的UUID或包含路径遍历字符
    """
    # 验证 UUID 格式，防止路径遍历攻击
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise ValueError(f"无效的 task_id 格式：{task_id}")

    task_dir = os.path.join(TASK_DATA_DIR, task_id)

    # 确保路径在 TASK_DATA_DIR 内（防止路径遍历）
    task_dir = os.path.abspath(task_dir)
    data_dir = os.path.abspath(TASK_DATA_DIR)
    if not task_dir.startswith(data_dir):
        raise ValueError("task_id 包含非法路径字符")

    return task_dir


def ensure_task_dir(task_id: str) -> str:
    """
    确保任务目录存在，如果不存在则创建。

    Args:
        task_id: 任务ID

    Returns:
        任务目录的完整路径
    """
    task_dir = get_task_dir(task_id)
    os.makedirs(task_dir, exist_ok=True)
    return task_dir


def get_task_meta_file(task_id: str) -> str:
    """
    获取任务元数据文件路径。

    Args:
        task_id: 任务ID

    Returns:
        元数据文件的完整路径
    """
    return os.path.join(get_task_dir(task_id), 'meta.json')


def get_task_result_file(task_id: str) -> str:
    """
    获取任务结果文件路径。

    Args:
        task_id: 任务ID

    Returns:
        结果文件的完整路径
    """
    return os.path.join(get_task_dir(task_id), 'result.jsonl')


def save_task_meta(task_id: str, meta: Dict[str, Any]) -> None:
    """
    保存任务元数据到文件。

    Args:
        task_id: 任务ID
        meta: 元数据字典
    """
    meta_file = get_task_meta_file(task_id)
    ensure_task_dir(task_id)
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def load_task_meta(task_id: str) -> Optional[Dict[str, Any]]:
    """
    从文件加载任务元数据。

    Args:
        task_id: 任务ID

    Returns:
        元数据字典，如果文件不存在则返回None
    """
    meta_file = get_task_meta_file(task_id)
    if not os.path.exists(meta_file):
        return None
    with open(meta_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def append_result_data(task_id: str, data_list: list) -> None:
    """
    追加结果数据到任务结果文件。

    Args:
        task_id: 任务ID
        data_list: 要追加的数据列表
    """
    result_file = get_task_result_file(task_id)
    ensure_task_dir(task_id)
    with open(result_file, 'a', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def cover_fee_info(fee: dict) -> dict:
    """
    将Api响应的费用信息 转为利于Ai理解的格式
    """
    if not fee:
        return {}
    api_cost = fee.get("apiCost", 0)
    balance = fee.get("accountBalance", 0)
    return {
        "apiCost": f"{api_cost}分钱",
        "balance": f"{balance}分钱"
    }
    
