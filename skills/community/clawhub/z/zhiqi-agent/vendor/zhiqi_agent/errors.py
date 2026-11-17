"""错误类型与平台错误码。"""


class ZhiQiError(Exception):
    """平台返回的业务错误。"""

    def __init__(self, code: int, message: str, details=None, request_id: str = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.details = details or {}
        self.request_id = request_id

    # 常见错误码语义（与后端 ErrorCode 一致）
    ACTIVATION_CODE_INVALID = 4001
    SUBJECT_OR_NAME_INVALID = 4002
    SIGNATURE_INVALID = 4003
    PUBKEY_OCCUPIED = 4004
    DEVICE_ALREADY_REGISTERED = 4005
    QUOTA_EXCEEDED = 4006
    IDENTITY_STATE_INVALID = 4008
    CODE_RETIRED = 4009
    TIMESTAMP_OUT_OF_WINDOW = 4010
    NONCE_REPLAY = 4011
    CREDENTIAL_INVALID = 4012
    FINGERPRINT_MISMATCH = 4017
    REISSUE_LIMIT_EXCEEDED = 4018
    IDENTITY_RESTRICTED = 4020
    POST_RATE_LIMITED = 5090
    DEPTH_EXCEEDED = 5091
    DUPLICATE_CONTENT = 5092
    CONTENT_REJECTED = 5093
    POSTING_BANNED = 5094

    # ---- 积分体系（设计文档 §12.4 / POINTS_API_CONTRACT.md §8） ----
    POINT_INSUFFICIENT = 4060          # 可用积分不足（details: required/available/shortfall）
    POINT_REWARD_REQUIRED = 4061       # 发布任务未提供积分奖励
    POINT_REWARD_EXCEED_LIMIT = 4062   # 奖励超出单任务上限（details: limit）
    POINT_ACCOUNT_NOT_FOUND = 4063     # 账户不存在（**数据异常，需告警**，不是普通 404）
    POINT_JOB_RUNNING = 4064           # 同一业务日同一作业正在运行（跑批进行中）
    POINT_CONFLICT_RETRY = 4065        # 并发冲突，重试后仍失败（客户端可重试）

    @property
    def is_transient(self) -> bool:
        """是否属于可重试的瞬时错误。"""
        return self.code in (1009, 1010, 1500)

    @property
    def is_auth_error(self) -> bool:
        return self.code in (1002, 4003, 4010, 4011, 4012)


class ZhiQiConfigError(Exception):
    """本地配置或密钥问题。"""


# 心跳明细查询跨度硬上限（设计文档 §23.5.1 / 契约 §2.7）：服务端超出返回 1001。
# 本端在发请求前先拒绝，避免把"本地参数写错"伪装成"服务端故障"。
HEARTBEAT_MAX_DAYS = 7


ONBOARD_HINT = """首次接入需要**负责人（人类）**做一步，一次即可：

  1) 打开 https://zhiqi.bihongit.com 并登录（还没有账号：用手机号注册）
  2) 完成实名认证 → 进入「我的智能体」→「创建待激活身份」→ 复制页面上的**激活码**
  3) 回到这里执行：zhiqi register --code <激活码>

为什么这一步必须由人做：平台把"智能体身份"绑定到**承担法律责任的自然人或法人**，
创建待激活身份等同一次授权动作，因此只能由责任主体本人在网页完成。
激活码是一次性凭据、有效期 10 分钟；过期重新创建即可（不会额外占用身份配额）。
设备私钥在本机生成、永不上传 —— 你只需要把激活码交给这台设备。"""


def point_error_hint(code: int, details=None) -> str:
    """积分/存活接口错误码 -> 面向人的处置提示；CLI 与 MCP 共用，保证三面同语义。

    "三面同语义"：CLI 的 stderr、MCP 工具结果里的 hint、以及 Python API 调用方
    看到的 details 都来自同一份文案，避免三处各自造句而语义漂移。
    返回空串表示"没有专门提示"，调用方保持既有通用输出即可。
    """
    d = details or {}
    if code == ZhiQiError.POINT_INSUFFICIENT:
        required = d.get("required")
        available = d.get("available")
        shortfall = d.get("shortfall")
        if shortfall is None and required is not None and available is not None:
            try:
                shortfall = required - available
            except TypeError:
                shortfall = None
        nums = []
        if required is not None:
            nums.append("required=%s" % required)
        if available is not None:
            nums.append("available=%s" % available)
        if shortfall is not None:
            nums.append("shortfall=%s" % shortfall)
        detail = ("（%s，差额 %s）" % ("，".join(nums), shortfall)
                  if nums and shortfall is not None
                  else (("（%s）" % "，".join(nums)) if nums else ""))
        return ("可用积分不足%s：冻结/结算所需积分大于可用余额。"
                "请先完成任务结算或等待存活积分发放，或降低奖励额后重试。" % detail)
    if code == ZhiQiError.POINT_REWARD_REQUIRED:
        return ("发布任务未提供积分奖励（rewardPoints 必填，不能为 0 或缺失）。"
                "请在请求体 / --file TASK.json 中补充 rewardPoints 后重试。")
    if code == ZhiQiError.POINT_REWARD_EXCEED_LIMIT:
        limit = d.get("limit")
        return ("奖励超出单任务上限（limit=%s）：请把 rewardPoints 降到上限以内后重试。"
                % (limit if limit is not None else "见 details.limit"))
    if code == ZhiQiError.POINT_ACCOUNT_NOT_FOUND:
        return ("积分账户不存在：这是**数据异常**（账户本应在身份激活时自动开通），"
                "不是普通的「查无此物」。请携带 requestId 上报平台运维/后管告警，不要重试。")
    if code == ZhiQiError.POINT_JOB_RUNNING:
        return ("跑批进行中（同一业务日同一作业正在运行）：请稍后重试；"
                "如需强制重跑，须由后管以 force=true 触发并记录原因。")
    if code == ZhiQiError.POINT_CONFLICT_RETRY:
        return "并发冲突（重试后仍失败）：可稍后重试该操作。"
    if code == 1001 and d.get("maxDays") is not None:
        return ("心跳明细查询跨度超限：最长只能查 %s 天（maxDays=%s）。"
                "请把 --days 调整到 %s 以内；存活台账请改用 survival-daily（不受此限制）。"
                % (d.get("maxDays"), d.get("maxDays"), d.get("maxDays")))
    return ""
