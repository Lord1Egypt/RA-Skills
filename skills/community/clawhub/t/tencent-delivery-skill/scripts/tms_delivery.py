#!/usr/bin/env python3
"""
腾讯出行服务跑腿 skill 管理脚本

核心命令：
  preflight                          环境检查
  save-token <token>                 保存 Token
  mcp-call <tool> [json]             调用 MCP 工具（通用入口，LLM 一般不直接用）
  state next / show                  FSM 驱动器 / 快照诊断
  state set/get/clear/init/reconcile

组合命令（推荐使用）：
  commit-address <role> <poi_json>   设地址 + 查联系人 + state next
  commit-contact <role> <name> <phone>  校验手机 + 设联系人 + state next
  prefill-contacts <s_name> <s_phone> <r_name> <r_phone>  乱序预登记联系人（4 个字段任一空串=跳过）
  run-estimate                       首次询价（断言 + 兜底 + 询价 + 自动 skuMap/display_rows）
  re-estimate                        询价重试（跳过 step3-entry，自动作废旧 recordId/skuMap/selectedSkuId）

高阶组合命令（极致减少 LLM 工具调用）：
  bootstrap                          入口一条命令（preflight + query_going_order + reconcile + state next）
  pick-address <role> <序号>         用户选序号 → 一步落盘地址 + 查联系人
  select-sku <序号>                  用户选 sku 序号 → 落盘 selectedSkuId + TTL 预检 + 返回下一步
  book-order                         一步下单（读 session → TTL 预检 → MCP 下单 → 落盘 orderCode）

决策工具：
  resolve-address <role> <keyword> [region]  地址簿 + POI 搜索（自动缓存供 pick-address 复用）

配置：~/.config/tms-delivery/env.json
会话：~/.config/tms-delivery/session.json
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import quote

# ============================================================
# 编码加固：强制 stdout/stderr 使用 UTF-8
# ============================================================
# 背景：本脚本输出 JSON（含中文 spName/POI 等）给上层 LLM 调用方解析。
# 当父进程通过 pipe 接走 stdout 且环境 locale 不是 UTF-8（容器/CI/部分 IDE 子进程
# 常见 LANG=C / POSIX），Python 3 的 sys.stdout.encoding 会降级为 ascii，
# 导致中文被替换为 \uXXXX 转义或 mojibake，下游 LLM 看到乱码后就开始"猜配送商名"。
#
# 这里在脚本入口强制把 stdout/stderr 重配置为 UTF-8，不再依赖外部 locale。
# - Python 3.7+ 提供 io.TextIOWrapper.reconfigure()
# - errors="replace" 兜底：极端情况下也不会因编码错误崩溃，而是替换为 ?
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    # 极旧 Python 或非 TextIOWrapper（如被外部接管）情形：不阻断主流程
    pass

CONFIG_DIR = os.path.expanduser("~/.config/tms-delivery")
CONFIG_FILE = os.path.join(CONFIG_DIR, "env.json")
SESSION_FILE = os.path.join(CONFIG_DIR, "session.json")
MCP_URL = "https://weixin.go.qq.com/mcp/user-auth-mcp/mcp"

# 会话陈旧阈值（秒）
# - 草稿态（无 orderCode）：30 分钟未更新视为陈旧，reconcile 时清理
# - 已下单（有 orderCode）：24 小时未更新才视为陈旧，给用户"下完单隔半天回来查单"留窗口
SESSION_STALE_SECONDS = 30 * 60
SESSION_STALE_SECONDS_WITH_ORDER = 24 * 60 * 60

# 询价新鲜度阈值（秒）
# - 3 分钟未过视为新鲜，可继续下单
# - 超过 3 分钟视为陈旧，下单前必须重新询价 + 让用户按新报价再次确认
# - 该阈值比服务端真实 TTL（约 60-90s 起）留出了余量，目标是在服务端拒绝前主动规避
ESTIMATE_FRESH_SECONDS = 3 * 60


def _load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def preflight():
    """环境检查。返回码：0=就绪，1=未就绪。"""
    config = _load_config()
    next_actions = []

    if not config.get("token"):
        next_actions.append("setup_token")

    return emit({
        "token_exists": bool(config.get("token")),
        "next_actions": next_actions if next_actions else ["ready"],
    }, exit_code=0 if not next_actions else 1)


def save_token(token):
    config = _load_config()
    config["token"] = token
    _save_config(config)
    return ok(message="Token 已保存")


def delete_token():
    config = _load_config()
    config.pop("token", None)
    _save_config(config)
    return ok(message="Token 已删除")


def mcp_call(tool_name, arguments_json="{}"):
    """调用 MCP 工具（CLI 入口版本：直接 print 结果）。token 不会输出到终端。

    对 LLM 可见的输出已走 _scrub_for_llm 过滤敏感字段；若 MCP 原始响应
    不是合法 JSON（罕见：网关返回 HTML 等），则原样透传 raw body——此时
    响应本身也不会包含 skuId 类结构化字段，风险可控。
    """
    try:
        arguments = json.loads(arguments_json)
    except json.JSONDecodeError as e:
        return fail("parse_error", f"参数 JSON 解析失败: {e}")

    result = _MCP.invoke(tool_name, arguments)
    if not result.ok:
        return emit(result.to_error_dict(), exit_code=1)

    # 成功路径：优先输出 inner_text（已解析的 MCP 业务返回）。
    # 尝试按 JSON 解析走 emit 过滤敏感字段；解析失败则降级为原样输出。
    raw_text = result.inner_text or result.raw_body or ""
    if raw_text:
        try:
            parsed = json.loads(raw_text)
            return emit(parsed)
        except (json.JSONDecodeError, TypeError):
            print(raw_text)
    return 0


# ============================================================
# MCPClient —— 统一 HTTP 请求 + 错误映射 + 副作用（Phase 1 重构）
# ============================================================
# 设计目标：消除 mcp_call / _mcp_call_silent / resolve_address / _estimate_core
# 四处独立的 urllib 请求代码；统一错误分类；统一"询价成功自动写 estimate_at"副作用。
#
# 核心对象：
#   - CallResult：HTTP 调用的结构化结果（ok/payload/inner_text/raw_body/error_kind/error_message）
#   - MCPClient.invoke(tool, arguments) -> CallResult
# ============================================================


class CallResult:
    """MCP 工具调用的统一结果对象。"""

    __slots__ = ("ok", "payload", "inner_text", "raw_body",
                 "error_kind", "error_message", "http_status")

    def __init__(self, ok, payload=None, inner_text=None, raw_body=None,
                 error_kind=None, error_message=None, http_status=None):
        self.ok = ok                        # bool：HTTP 是否 2xx + 解析是否成功
        self.payload = payload              # dict | str：inner_text 解析后的业务对象
        self.inner_text = inner_text        # str：MCP 的 result.content[0].text 原文
        self.raw_body = raw_body            # str：HTTP 响应原始 body
        self.error_kind = error_kind        # "no_token" | "token_invalid" | "http" | "network" | "exception"
        self.error_message = error_message  # 人类可读错误描述
        self.http_status = http_status      # HTTP 状态码（仅 error_kind == "http" / "token_invalid"）

    def to_error_dict(self):
        """转成 CLI 打印用的错误 JSON 结构。

        token 失效（no_token / token_invalid）时自动附上 next_doc + reply_template，
        引导 LLM 指示用户执行 save-token 重新绑定。
        """
        base = {
            "error": self.error_kind or "unknown",
            "message": self.error_message or "未知错误",
            **({"http_status": self.http_status} if self.http_status else {}),
        }
        if self.error_kind in ("no_token", "token_invalid"):
            base["next_doc"] = _doc_for_scenario("token_error")
            base["reply_template"] = _tpl_token_invalid(self.error_kind, self.error_message)
        return base


class MCPClient:
    """MCP 单例客户端：所有 MCP 请求走这里。"""

    def __init__(self, url, timeout=30):
        self.url = url
        self.timeout = timeout

    def _get_token(self):
        return _load_config().get("token", "")

    def invoke(self, tool_name, arguments=None):
        """统一的 MCP 调用入口。返回 CallResult。不 print、不 sys.exit。"""
        token = self._get_token()
        if not token:
            return CallResult(False, error_kind="no_token",
                              error_message="Token 未配置，请先执行 save-token")

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments or {}},
        }
        req = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Access-Token": token,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                # 成功路径也可能带 Token-Error 头（服务端如果仍返回 200）
                token_err_header = resp.headers.get("Token-Error") if resp.headers else None
                if token_err_header:
                    return CallResult(False, error_kind="token_invalid",
                                      error_message=token_err_header,
                                      http_status=resp.getcode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            # 服务端在 token 解析失败时返回 HTTP 500 + 响应头 Token-Error: ...
            # 优先识别为 token_invalid，引导用户重新 save-token，而不是笼统报 HTTP 错误
            token_err_header = e.headers.get("Token-Error") if e.headers else None
            if token_err_header:
                return CallResult(False, error_kind="token_invalid",
                                  error_message=token_err_header,
                                  http_status=e.code)
            return CallResult(False, error_kind="http",
                              error_message=error_body or e.reason,
                              http_status=e.code)
        except urllib.error.URLError as e:
            return CallResult(False, error_kind="network",
                              error_message=str(e.reason))
        except Exception as e:
            return CallResult(False, error_kind="exception",
                              error_message=str(e))

        # 解析 JSON-RPC 响应
        inner_text = ""
        try:
            rpc_resp = json.loads(body)
            content = (rpc_resp.get("result") or {}).get("content") or []
            inner_text = next((c.get("text", "") for c in content if c.get("type") == "text"), "")
        except (json.JSONDecodeError, AttributeError):
            # JSON-RPC 外层不是 JSON 或结构异常 —— 把整个 body 作为 inner_text 回传
            return CallResult(True, payload=body, inner_text=body, raw_body=body)

        # 副作用：询价成功自动写 estimate_at（原 mcp_call 内嵌逻辑，集中到此）
        if tool_name == "runerrand_estimate_price" and inner_text:
            _record_estimate_at_on_success(inner_text)

        # 解析 inner_text 为 dict（业务语义）
        payload = None
        if inner_text:
            try:
                payload = json.loads(inner_text)
            except json.JSONDecodeError:
                payload = inner_text

        return CallResult(True, payload=payload, inner_text=inner_text, raw_body=body)


# 全局单例
_MCP = MCPClient(MCP_URL)


# ============================================================
# 响应构造器（Phase 2 重构）—— 统一 JSON 输出
# ============================================================
# 设计目标：消除散落 80+ 处的 `print(json.dumps({...}))` 字面量；
# 统一成功/错误响应的 key 顺序；收口所有 stdout 写入点。
#
# 用法：
#   return ok(next_state="step2", hint="...")       # 成功（status 自动为 "ok"）
#   return fail("invalid_index", "序号无效", hint="...")   # 失败（exit 1）
#   return emit(data)                                # 任意 dict，直接输出（不强加 status 字段）
# ============================================================


# LLM 端不应直接看到的字段（"敏感字段"）。
# 走 emit() 的命令返回值里，如出现以下字段，会在输出前被递归过滤掉。
# 诊断命令（state show / state get）自己直接 print，不走 emit，故不受影响。
# mcp-call 走另一条原始输出路径，单独处理（见 mcp_call()）。
_LLM_HIDDEN_FIELDS = frozenset({
    "estimatePriceRecordId",  # 询价记录 ID
    "skuMap",                 # 序号→skuId 的映射
    "skuId",                  # 服务商报价 ID
    "selectedSkuId",          # 已选报价 ID
    "expressSkuInfos",        # 下单 payload 中的 skuId 数组
    "defaultChecked",         # 报价项的默认选中标记（LLM 用不到）
    "_last_pois",             # POI 候选缓存（JSON 形态）
})


def _scrub_for_llm(obj):
    """递归移除 LLM 不该见到的字段。列表内的 dict 也会递归处理。

    设计要点：
      - 只过滤 _LLM_HIDDEN_FIELDS 集合中的 key（黑名单），不做正则/模糊匹配
      - 不改动原对象（深拷贝语义）：返回新 dict / list
      - 非 dict/list（字符串、数字等）原样透传
    """
    if isinstance(obj, dict):
        return {
            k: _scrub_for_llm(v)
            for k, v in obj.items()
            if k not in _LLM_HIDDEN_FIELDS
        }
    if isinstance(obj, list):
        return [_scrub_for_llm(item) for item in obj]
    return obj


# ============================================================
# next_doc 映射表（v1.3.3+）—— LLM 拿到返回值后的文档路由器
# ============================================================
#
# 设计动机：
#   LLM 拿到脚本返回值后，最需要知道的就是"下一步读哪个文档"。
#   统一用 next_doc 字段覆盖所有出口（FSM 状态 + 非 FSM 场景），
#   消除 LLM 的"读什么"判断。
#
# 实现拆分：
#   _STATE_META[state]["doc_ref"]   —— 脚本内部字典 key（实现细节）
#                                      state_next/commit_* 读它时统一写入 next_doc
#   _SCENARIO_DOC_MAP[scenario]     —— 非 FSM 错误/降级场景的文档锚点
#
# LLM 可见字段：只有 next_doc。其他 doc_ref 字样均为脚本内部实现。
#
# 命名规则：相对 skill 根目录的 posix 路径 + 可选锚点
#   "references/delivery/step-3-estimate.md"
#   "references/error-handling.md#询价过期重试"
# ============================================================


# 场景关键词 → 文档锚点
# 只映射脚本里会用到的场景；FSM 状态类走 _STATE_META[state]["doc_ref"]
_SCENARIO_DOC_MAP = {
    # 通用错误 / 降级
    "mcp_error":            "references/error-handling.md",
    "token_error":          "references/quick-start-workflow.md",
    # 询价相关
    "estimate_expired":     "references/error-handling.md",       # 第 5 节：询价过期重试
    "re_estimate":          "references/delivery/step-3-estimate.md",
    # 地址相关
    "address_multi_poi":    "references/delivery/step-1-sender.md",
    "address_sug":          "references/delivery/step-1-sender.md",
    "address_book_hit":     "references/delivery/step-1-sender.md",
    "address_empty":        "references/delivery/step-1-sender.md",
    # 下单相关
    "book_order":           "references/delivery/step-5-book.md",
    # 异常拦截
    "has_ongoing_block":    "references/quick-start-workflow.md",
    "has_ongoing_resume":   "references/order-workflow.md",
}


def _doc_for_state(state):
    """FSM 状态 → 文档锚点。无匹配时返回 delivery 主流程。"""
    meta = _STATE_META.get(state) if state else None
    return (meta or {}).get("doc_ref") or "references/delivery-workflow.md"


def _doc_for_scenario(scenario):
    """场景 → 文档锚点。无匹配时退化到错误处理文档。"""
    return _SCENARIO_DOC_MAP.get(scenario, "references/error-handling.md")



#
# 设计目标：LLM 拿到返回值后，只要把 reply_template 原样粘给用户即可，
# 不再靠 SKILL.md/step-X.md 里的大段 markdown 模板 + "❌ 禁止模板外内容"
# 的 prompt 喊话来约束输出。
#
# 约束：
#   - 所有模板函数返回 str；None 表示该场景不走模板
#   - 模板内部自行负责"脱敏展示"（例如手机号中段星号）
#   - 新增场景在此集中添加；避免模板字符串散落到业务函数
#   - 被 emit() 写入的字段名固定为 "reply_template"
# ============================================================


def _tpl_token_invalid(error_kind, error_message):  # noqa: ARG001 — error_message 仅保留签名兼容
    """token 未配置 / 解析失败时的用户提示卡片。

    - error_kind == "no_token"：本地 env.json 里 token 为空
    - error_kind == "token_invalid"：MCP 响应头 Token-Error，token 过期或格式非法

    措辞**严格复用** quick-start-workflow.md §1.1 的初始化模板（扫码 / 微信自取
    两条路径），等同于让用户重新走一遍初始化流程，不另起炉灶造新的取 Token
    步骤说明。各行用 "\\n\\n" 分隔避免前端折叠。刻意不把服务端原始错误明细
    抛给用户（避免泄露 code:11001 / internal message 等内部诊断信息），只在
    脚本返回值的 message 字段里留存给 LLM/调试用。
    """
    if error_kind == "no_token":
        title = "🔐 还没有绑定跑腿 Token，需要先完成初始化。"
    else:
        title = "🔐 跑腿 Token 已失效，需要重新初始化。"
    return (
        f"{title}\n\n"
        "请使用微信扫描下方二维码，获取跑腿 TOKEN 后回复我：\n\n"
        "![引导图](https://static.img.tai.qq.com/mp/ops/cdnImg/2026/15/mplaunch_skillToken_1775811974.png)\n\n"
        "如果图片无法正常展示，请前往：\n\n"
        "「微信」-「我」-「服务」-「出行服务」-「我的」-「头像/昵称」-「Token信息」中获取跑腿 token\n\n"
        "拿到 Token 后直接回复我，我会自动帮你保存并继续刚才的需求。"
    )


def _tpl_has_ongoing_order(ongoing):
    """bootstrap 检测到进行中订单时的用户卡片。ongoing 应含 orderCode/expressTypeName/orderStatusText/spName。

    各行用 "\n\n"（空行）分隔，防止前端 Markdown 渲染器把相邻行折叠到一行。
    """
    sp = ongoing.get("spName") or ""
    express_type = ongoing.get("expressTypeName") or "跑腿"
    sp_part = f"{sp}（{express_type}）" if sp else express_type
    return (
        "🚴 检测到您还有一笔进行中的跑腿订单：\n\n"
        f"🧾 订单号：{ongoing.get('orderCode') or ''}\n\n"
        f"🏪 {sp_part}\n\n"
        f"📋 当前状态：{ongoing.get('orderStatusText') or ''}\n\n"
        "请选择：\n\n"
        "- 回复「查跑腿」查看详情\n"
        "- 回复「骑手到哪了」查看骑手位置\n"
        "- 回复「取消跑腿」取消订单"
    )


def _tpl_pick_poi_list(role, pois):
    """resolve-address 多 POI 候选时的序号列表。role ∈ {sender, receiver}。

    用 "\n\n"（空行）分隔条目，避免部分前端 Markdown 渲染器
    把相邻行折叠到一行（CommonMark 规范下单个 \n 是 soft-break）。
    """
    title = "寄件地址" if role == "sender" else "收件地址"
    parts = [f"### 请选择{title}"]
    for i, p in enumerate(pois, start=1):
        name = p.get("name") or ""
        addr = p.get("address") or ""
        parts.append(f"📍 **{i}. {name}**：{addr}")
    parts.append("回复序号确认，或重新提供更精确的关键词。")
    return "\n\n".join(parts)


def _tpl_payment_qr(order_code, sender_addr, receiver_addr, total_fee, code_url, scan_url):
    """下单成功后的支付二维码卡片。

    历史教训：仅靠 step-6-payment.md 文档模板约束 LLM，小模型常退化成
    "点击支付"裸链接，丢掉二维码图片。改为脚本直出 markdown，LLM 原样贴出即可。

    渲染策略（与 step-6-payment.md 硬约束保持一致）：
      - 首选 codeUrl（weixin:// 协议）→ 通过 api.qrserver.com 公共服务编码为图片
      - 兜底 scanUrl（HTML 页面）→ 直接作为 img src（部分前端可能渲染失败）
      - 始终在图片下方附带 scanUrl 文本链接，确保浏览器兜底
      - codeUrl 与 scanUrl 同时为空 → 返回 None，由调用方走异常处理
    """
    if not code_url and not scan_url:
        return None

    if code_url:
        # weixin:// 协议必须 URL 编码后再拼到 qrserver 的 data 参数
        qr_src = (
            "https://api.qrserver.com/v1/create-qr-code/?size=240x240&data="
            + quote(code_url, safe="")
        )
    else:
        qr_src = scan_url

    fee_text = f"¥{total_fee}" if total_fee and total_fee != "-" else "-"
    fallback_link = scan_url or code_url

    parts = [
        "📦 跑腿订单已创建！",
        f"🧾 订单号：{order_code or '-'}",
        f"📍 {sender_addr or '-'} → {receiver_addr or '-'}",
        f"💰 费用：{fee_text}",
        "💳 请使用微信扫码支付：",
        f"![支付二维码]({qr_src})",
        f"如果二维码无法显示，请复制以下链接到浏览器中打开：\n\n{fallback_link}",
        "✅ **支付完成后请告诉我，我将为您跟踪骑手状态**",
    ]
    return "\n\n".join(parts)


def _tpl_estimate_table(display_rows, sender_addr, receiver_addr):
    """询价成功后的报价表渲染。

    弃用文字指令"单一 markdown 表格"——小模型（如 DeepSeek V3.2）会无视
    指令自由发挥成嵌套编号列表（费用/预计送达 缩进错乱）。
    改为脚本直出 markdown 表格作为 reply_template，LLM 原样贴出即可。

    输出格式：
        ### 跑腿配送报价（共 N 个选项，按价格升序）

        - 寄件：xxx → 收件：xxx

        | 序号 | 配送商 | 类型 | 费用（元） | 预计送达 |
        |---|---|---|---|---|
        | 1 | 顺丰同城 | 特惠取送 | 1.00 | 16:09 |
        ...

        请回复序号选择配送方案。
    """
    if not display_rows:
        return None

    parts = [f"### 跑腿配送报价（共 {len(display_rows)} 个选项，按价格升序）"]

    if sender_addr or receiver_addr:
        parts.append(f"- 寄件：{sender_addr or '-'} → 收件：{receiver_addr or '-'}")

    # markdown 表格头 + 分隔行 + 数据行（用单 \n 拼，因为表格内不能空行断开）
    table_lines = [
        "| 序号 | 配送商 | 类型 | 费用（元） | 预计送达 |",
        "|---|---|---|---|---|",
    ]
    for row in display_rows:
        no = row.get("no", "")
        sp = row.get("spName") or "-"
        et = row.get("expressTypeName") or "-"
        fee = row.get("totalFee") or "-"
        dt = row.get("deliveryTime_short") or "-"
        table_lines.append(f"| {no} | {sp} | {et} | {fee} | {dt} |")
    parts.append("\n".join(table_lines))

    parts.append("请回复序号选择配送方案。")
    return "\n\n".join(parts)


def _collect_runtime_diag():
    """采集脚本当前运行时的编码 / locale 诊断信息。

    设计目标：把 stdout 编码、locale、LANG 等"无声依赖"显式暴露给上层 LLM，
    一旦未来再出现"中文乱码 → LLM 脑补字段"的问题，从 bootstrap 返回的
    JSON 里就能一眼定位是不是编码层出错——不用再让用户手动复现 / 抓 stderr。

    诊断字段说明：
      - stdout_encoding：经过 reconfigure 之后的 stdout 真实编码（期望 utf-8）
      - locale_pref    ：locale.getpreferredencoding(False)
      - lang_env       ：环境变量 LANG / LC_ALL / LC_CTYPE 的拼接
      - python_version ：解释器版本，帮助判断 reconfigure 是否生效（>=3.7）
      - chinese_probe  ：固定中文探针 + 一个 BMP 外字符。如果 LLM 看到的不是
                         "中文OK✓🚚"原文（出现 \\uXXXX / ? / mojibake），则说明
                         脚本写出 → 下游解析 → LLM 端 这条链路上仍有编码降级。
    """
    try:
        import locale
        loc_pref = locale.getpreferredencoding(False)
    except Exception:
        loc_pref = "unknown"

    lang_parts = []
    for key in ("LANG", "LC_ALL", "LC_CTYPE"):
        val = os.environ.get(key)
        if val:
            lang_parts.append(f"{key}={val}")
    lang_env = ";".join(lang_parts) or "<unset>"

    return {
        "stdout_encoding": getattr(sys.stdout, "encoding", "unknown"),
        "locale_pref": loc_pref,
        "lang_env": lang_env,
        "python_version": "{}.{}.{}".format(*sys.version_info[:3]),
        # 中文 + BMP 外字符（U+1F69A 货车）联合探针：覆盖 ascii 降级 / GBK 错码 / surrogate 各类故障
        "chinese_probe": "中文OK✓🚚",
    }


def emit(payload, exit_code=0):
    """通用 JSON 输出：不强加任何 key。用于响应字段名自定义的命令（如 bootstrap 的 stage 字段）。

    在输出前自动走 _scrub_for_llm() 剔除敏感字段，让 LLM 物理上看不到
    skuId / estimatePriceRecordId 等——替代历史上靠 prompt 喊"❌ 禁止输出"的做法。
    """
    safe = _scrub_for_llm(payload)
    # ensure_ascii=True：将所有非 ASCII 字符转义为 \uXXXX 形式，
    # 让 stdout 字节流变成纯 ASCII。下游任何编码（GBK/Latin-1/UTF-8）
    # 解码都不会乱码，LLM 读取 JSON 时会自动反转义回中文。
    # 这是从源头消除"中文落到下游变 mojibake"的根治方案。
    print(json.dumps(safe, ensure_ascii=True))
    return exit_code


def ok(**fields):
    """成功响应：自动注入 status="ok"。"""
    return emit({"status": "ok", **fields}, exit_code=0)


def fail(error, message, exit_code=1, stderr_copy=False, **fields):
    """失败响应：自动注入 status="error"、error、message。

    stderr_copy=True 时 stdout+stderr 双写（替代原 _emit_error），防 IDE 包装器吞 stdout。
    """
    payload = {"status": "error", "error": error, "message": message, **fields}
    # ensure_ascii=True：与 emit 出口对齐，根治下游编码降级导致的乱码。
    text = json.dumps(payload, ensure_ascii=True)
    print(text)
    if stderr_copy:
        print(text, file=sys.stderr)
    return exit_code


# ============================================================
# Session State（会话快照）
# ============================================================
#
# 设计要点：
#  - 本地 session.json 是 LLM 长对话中"上下文字段"的机械化备忘
#  - 用户端聊天记录完全看不到 session.json 内容（仅通过脚本 I/O）
#  - 会话隔离策略：以 "服务端 runerrand_query_going_order 的 orderCode" 为权威
#    * 本地无 orderCode（草稿） → 服务端也无进行中订单 → 视为旧草稿清理
#    * 本地有 orderCode，与服务端一致 → 续聊同一单，保留
#    * 本地有 orderCode，与服务端不一致 → 旧单残留，清理
#  - 陈旧保护：
#    * 草稿态（无 orderCode）last_update_at 超过 30 分钟 → 陈旧，清理
#    * 已下单（有 orderCode）last_update_at 超过 24 小时 → 陈旧，清理
#    （给用户"下完单隔半天回来查单"留窗口）
# ============================================================


def _empty_session():
    return {
        "schema_version": 3,
        "created_at": int(time.time()),
        "last_update_at": int(time.time()),

        # ——寄件信息（全程保留到 state clear）——
        "sender": {
            "name": None,
            "phone": None,
            "address": {
                "name": None,          # POI 名称，同时用于询价 fromAddrDetail
                "longitude": None,     # 询价必需（Number）
                "latitude": None,      # 询价必需（Number）
                "poiid": None,         # 寄=收兜底校验用
            },
        },

        # ——收件信息（全程保留到 state clear）——
        "receiver": {
            "name": None,
            "phone": None,
            "address": {
                "name": None,
                "longitude": None,
                "latitude": None,
                "poiid": None,
            },
        },

        # ——询价/下单参数（扁平化，原 estimate.* 前缀已去除）——
        "estimatePriceRecordId": None,   # 询价返回，下单必需
        "estimate_at": None,             # 询价成功的 Unix 时间戳，用于 TTL 新鲜度预检
        "skuMap": None,                  # {"1":"60797_1",...} 序号→skuId
        "selectedSkuId": None,           # 用户选中的 skuId 字符串（下单必需）

        # ——订单标识（订单终态时 state clear）——
        "orderCode": None,
    }


def _load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _save_session(session):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    session["last_update_at"] = int(time.time())
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)


def _parse_json_value(raw):
    """
    state set 的值解析规则：
      - 能解析为 JSON 就按 JSON（数字/布尔/数组/对象/null/带引号的字符串）
      - 不能解析的按原始字符串
    """
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


def _set_by_path(session, dot_path, value):
    """按 'a.b.c' 路径写入。中间节点不存在则自动创建 dict。"""
    if not dot_path:
        raise ValueError("path 不能为空")
    parts = dot_path.split(".")
    cur = session
    for p in parts[:-1]:
        if not isinstance(cur, dict):
            raise ValueError(f"路径 {dot_path} 在 {p} 处非 dict")
        if p not in cur or cur[p] is None or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    if not isinstance(cur, dict):
        raise ValueError(f"路径 {dot_path} 末端非 dict")
    cur[parts[-1]] = value


def _get_by_path(session, dot_path):
    if not dot_path:
        return session
    parts = dot_path.split(".")
    cur = session
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


# ============================================================
# WRITE_GUARD：state set 时的前置依赖校验
# ============================================================
#
# 设计动机：LLM 在"高效冲动"下可能跳步/并行处理，比如：
#   - 用户首条消息同时给了寄+收地址 → LLM 并行调 get_place_suggestion
#   - sender.address 尚未落盘 → LLM 就写 receiver.address
#   - 手机号未校验 → 进入询价
#
# WRITE_GUARD 把文档里的"不跳步"约束下沉到脚本：
#   - 写某字段前，校验其依赖的前置字段是否齐全
#   - 前置字段未齐 → 拒绝写入，返回 error 让 LLM 立即纠偏
#
# _require_any（任一字段非空）实际未在当前图中用到，保留 _require_all 即可。
# ============================================================

# 前置依赖：key = 目标字段；value = 必须先写齐的字段列表（全部非空）
WRITE_GUARD = {
    # 第二步之前：第一步 sender.* 必须完整（含手机号已校验 → 非空即视为通过）
    "receiver.address":           ["sender.address.name", "sender.address.longitude", "sender.address.latitude", "sender.name", "sender.phone"],
    "receiver.address.name":      ["sender.address.name", "sender.address.longitude", "sender.address.latitude", "sender.name", "sender.phone"],
    "receiver.name":              ["sender.address.name", "sender.name", "sender.phone"],
    "receiver.phone":             ["sender.address.name", "sender.name", "sender.phone"],

    # 第三步之前：sender/receiver 必须齐全
    "estimatePriceRecordId":      ["sender.address.name", "sender.address.longitude", "sender.address.latitude",
                                   "sender.name", "sender.phone",
                                   "receiver.address.name", "receiver.address.longitude", "receiver.address.latitude",
                                   "receiver.name", "receiver.phone"],
    "skuMap":                     ["estimatePriceRecordId"],

    # 第四步之前：必须已有 skuMap
    "selectedSkuId":              ["estimatePriceRecordId", "skuMap"],

    # 第五步之前：必须已选中 skuId
    "orderCode":                  ["selectedSkuId"],
}


def _is_empty(value):
    """判断字段是否为空：None / "" / 空列表/字典/0-数字 不算空；仅 None/空字符串 视为空。"""
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def _check_write_guard(session, dot_path):
    """校验 state set 的前置依赖。返回 (ok:bool, reason:str)。"""
    if dot_path not in WRITE_GUARD:
        return True, ""
    missing = []
    for required_path in WRITE_GUARD[dot_path]:
        value = _get_by_path(session, required_path)
        if _is_empty(value):
            missing.append(required_path)
    if missing:
        return False, f"写 {dot_path} 前必须先写齐：{', '.join(missing)}"
    return True, ""


# ============================================================
# 共用工具：filled_fields 收集 + reconcile 决策矩阵
# ============================================================
# 设计动机（Phase B）：
#   - state_next / commit_contact 两处重复枚举 14 个关键字段路径
#   - state_reconcile / bootstrap 两处重复同一套决策矩阵（陈旧/草稿/匹配/不匹配）
# ============================================================

# state_next 和 commit_contact 共用：扫一次 session 看哪些关键字段已落盘
_TRACKED_FIELDS = (
    "sender.address.name", "sender.address.longitude", "sender.address.latitude",
    "sender.name", "sender.phone",
    "receiver.address.name", "receiver.address.longitude", "receiver.address.latitude",
    "receiver.name", "receiver.phone",
    "estimatePriceRecordId", "skuMap", "selectedSkuId", "orderCode",
)


def _collect_filled_fields(session):
    """返回 session 中已落盘的关键字段路径列表（供 LLM 诊断）。"""
    if session is None:
        return []
    return [p for p in _TRACKED_FIELDS if not _is_empty(_get_by_path(session, p))]


def _reconcile_decision(session, has_ongoing, server_order_code, now):
    """根据本地 session + 服务端 going_order 推断 reconcile 决策。

    返回 (decision, reason)：
      decision ∈ {"init", "keep"}
      reason 为人类可读决策依据
    """
    if session is None:
        return "init", "no_local_session"
    last_update = session.get("last_update_at", 0)
    local_order_code = session.get("orderCode")
    stale_threshold = SESSION_STALE_SECONDS_WITH_ORDER if local_order_code else SESSION_STALE_SECONDS
    if now - last_update > stale_threshold:
        return "init", "local_stale"
    if not local_order_code:
        return "init", "local_draft_discarded"
    if has_ongoing and local_order_code == server_order_code:
        return "keep", "same_ongoing_order"
    return "init", "order_code_mismatch_or_closed"


# ============================================================
# 第三步询价的步首断言（仅剩一条，_estimate_core 内部使用）
# ============================================================
# 其他步骤的 entry assert 已废弃：LLM 信任上一命令返回的 next_state 即可。
# ============================================================

ENTRY_ASSERTIONS = {
    "step3-entry": {
        "require_empty": ["estimatePriceRecordId"],
        "require_filled": ["sender.address.name", "sender.address.longitude", "sender.address.latitude",
                           "sender.name", "sender.phone",
                           "receiver.address.name", "receiver.address.longitude", "receiver.address.latitude",
                           "receiver.name", "receiver.phone"],
        "description": "进入第三步前：sender + receiver 必须齐全；estimatePriceRecordId 为空",
    },
}


def state_init():
    """覆盖写入空快照。"""
    session = _empty_session()
    _save_session(session)
    return ok(action="init", step=0)


def state_get(dot_path=None):
    session = _load_session()
    if session is None:
        return emit({"status": "empty", "session": None})
    if dot_path:
        value = _get_by_path(session, dot_path)
        return ok(path=dot_path, value=value)
    # 完整 session 快照：用 emit 走过滤（_last_pois 等已在黑名单）
    return emit({"status": "ok", "session": session})


def state_set(dot_path, raw_value):
    session = _load_session()
    if session is None:
        # 防御：没有 session 就自动 init 一次，避免 set 失败
        session = _empty_session()

    # ——WRITE_GUARD：写某个字段前必须先写齐它依赖的前置字段——
    passed, reason = _check_write_guard(session, dot_path)
    if not passed:
        return fail(
            "write_guard_violation", reason,
            action="set", path=dot_path,
            hint="请先完成上一步字段落盘，禁止跳步或合并处理。参见 SKILL.md §3 核心约束。",
        )

    try:
        value = _parse_json_value(raw_value)
        _set_by_path(session, dot_path, value)
    except ValueError as e:
        return fail("parse_error", str(e))
    _save_session(session)
    return ok(action="set", path=dot_path)


def state_clear():
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
            return ok(action="clear", removed=True)
        except OSError as e:
            return fail("os_error", str(e))
    return ok(action="clear", removed=False)


def state_reconcile(going_order_json):
    """
    根据服务端 runerrand_query_going_order 的返回值校准本地会话。
    入参：整个 MCP 返回的 JSON 字符串（含 code/data/message），或仅 data 部分。
    决策矩阵：
      | 本地 session       | 服务端 hasOnGoingOrder       | 动作      |
      |-------------------|------------------------------|-----------|
      | 无                 | *                            | init     |
      | 陈旧（超时）        | *                            | init     |
      | 有，无 orderCode    | false                        | init     |
      | 有，无 orderCode    | true                         | init     |  (服务端有新单，本地草稿过期)
      | 有，orderCode 匹配  | true                         | keep     |  (续聊同一单)
      | 有，orderCode 不符  | *                            | init     |  (旧单残留)
    返回：
      {"status":"ok","decision":"init|keep","reason":"...","local":{...},"server":{...}}
    """
    try:
        payload = json.loads(going_order_json) if going_order_json else {}
    except json.JSONDecodeError as e:
        return fail("parse_error", f"going_order JSON 解析失败: {e}")

    # 支持传整个 {code,data,message} 或直接传 data
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    has_ongoing = bool(data.get("hasOnGoingOrder", False)) if isinstance(data, dict) else False
    server_order_code = None
    if isinstance(data, dict):
        # 服务端 orderCode 可能位于 data.orderCode 或 data.orderInfo.orderCode 等位置
        server_order_code = (
            data.get("orderCode")
            or (data.get("orderInfo") or {}).get("orderCode")
        )

    session = _load_session()
    now = int(time.time())
    decision, reason = _reconcile_decision(session, has_ongoing, server_order_code, now)
    server_info = {"hasOnGoingOrder": has_ongoing, "orderCode": server_order_code}

    if decision == "init":
        # 覆盖本地 session（内联 state_init，不让它 print 走掉最终输出）
        _save_session(_empty_session())
        return ok(decision="init", reason=reason, server=server_info)

    # decision == "keep"
    return ok(
        decision="keep",
        reason=reason,
        local={"orderCode": session.get("orderCode"), "step": session.get("step")},
        server=server_info,
    )


# ============================================================
# 决策工具（v1.2.0+）—— 把 LLM 的判断下沉到脚本
# ============================================================
#
# 设计动机：
#   Anthropic 官方 context engineering 最佳实践指出，LLM 的"思考/判断"
#   是 context 杀手。把确定性逻辑（正则校验、地址匹配、寄=收兜底）下沉到
#   脚本，文档只保留"调哪个命令 + 按返回值照模版回复"，能大幅降低 LLM
#   的 context 占用和判断漂移。
#
# 命令清单：
#   resolve-address          封装地址簿匹配 + get_place_suggestion + SUG 识别
#   （validate_phone 作为内部工具函数，供 commit-contact 复用，已不对外暴露）
# ============================================================


# —— PREFERENCE.md 地址簿路径（相对 skill 安装位置）——
# 本脚本位置：<skill_dir>/scripts/tms_delivery.py
# 地址簿位置：<skill_dir>/assets/PREFERENCE.md
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PREFERENCE_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), "assets", "PREFERENCE.md")


def _parse_preference_book():
    """
    解析 PREFERENCE.md 的地址簿表格。返回 list[dict]，每条包含：
      alias / name / lng / lat / contact / phone
    缺失字段留空字符串。
    """
    if not os.path.exists(PREFERENCE_FILE):
        return []
    try:
        with open(PREFERENCE_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return []

    entries = []
    in_table = False
    header_skipped = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|") and "别名" in line and "地址名称" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            header_skipped = True
            continue
        if in_table and header_skipped:
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            # 至少 6 列（别名/地址名称/经度/纬度/联系人/手机号）
            if len(cells) < 6:
                continue
            alias, name, lng, lat, contact, phone = cells[:6]
            # 空行跳过
            if not any([alias, name, lng, lat, contact, phone]):
                continue
            entries.append({
                "alias": alias,
                "name": name,
                "lng": lng,
                "lat": lat,
                "contact": contact,
                "phone": phone,
            })
    return entries


# 地名特征字（白名单）—— 中文地名/POI 通常带这些字之一。
# 用于识别 keyword 是否"看起来像地址"。命中任一字符即视为有地名特征。
_LOC_HINT_CHARS = set(
    # 道路 / 区划
    "路街道巷里弄区市县镇乡村屯庄"
    # 建筑 / 园区
    "园苑府邸厦楼宇阁塔店铺城广场中心"
    "大厦花园新村小区公馆大院公园湖山河海岛"
    # 自然 / 地貌
    "门口站口桥湾港岸滩"
    # 机构 / 公共场所
    "院校园校所局厂矿场馆寺庙观祠坛陵殿亭台轩斋厅堂"
    # 商业 / 餐饮品牌常见后缀
    "店铺超市商场酒店宾馆KTV餐厅食堂咖啡茶坊吧"
    # 知名连锁后缀字（家乐福/麦当劳/肯德基/星巴克/便利店/物美 等）
    "福劳基克美乐"
    # 城市/省份常用字（北京/上海/广州/深圳/天津/重庆 等首字符常出现）
    "京沪粤深津渝港澳台"
)
# 注：阈值取舍——本函数仅在"地址簿未命中"且"keyword 形态像姓名"双条件下触发拦截，
# 误拦的代价仅是"让用户多补一句具体地点"，远小于召回一堆同名村庄/店铺的代价。


def _looks_like_person_name(kw):
    """
    判定 keyword 是否"形态像纯中文姓名"（用于地址簿未命中时的 fallthrough 拦截）。

    规则：
      - 纯中文 2-4 字
      - 不含任何地名特征字（_LOC_HINT_CHARS）
      - 不含任何英文/数字
    命中即认为"更像人名而非地址"。

    设计动机：
      模型在 step1-sender-address 状态下，若用户只给了"姓名+手机号"
      （例如「寄件人：王念 18717178957」），可能误把"王念"当 keyword 调本命令。
      地址簿未命中时若 fallthrough 到 POI 搜索，会得到一堆带"王念"二字的
      村庄/店铺，对用户毫无意义。本函数用于在 fallthrough 之前拦截。
    """
    if not kw:
        return False
    # 必须是纯中文 2-4 字
    if not (2 <= len(kw) <= 4):
        return False
    if not all('\u4e00' <= c <= '\u9fff' for c in kw):
        return False
    # 任意地名特征字命中 → 不是人名形态
    if any(c in _LOC_HINT_CHARS for c in kw):
        return False
    return True


def _address_book_match(keyword):
    """
    按 PREFERENCE.md 匹配规则匹配地址簿。
    匹配优先级（与 PREFERENCE.md 文档一致）：
      - 别名精确匹配（忽略大小写）
      - 联系人精确匹配
      - 地址名称包含匹配
      - 去前缀兜底（"回公司" → "公司"；"寄去望京" → "望京"；"寄给张三" → "张三"）
    返回命中的 entries list。
    """
    if not keyword:
        return []
    kw = keyword.strip()
    if not kw:
        return []
    # 去前缀兜底
    prefixes = ["回", "寄去", "寄到", "寄给", "送去", "送到", "送给", "到", "去", "从"]
    candidates = [kw]
    for p in prefixes:
        if kw.startswith(p) and len(kw) > len(p):
            candidates.append(kw[len(p):])

    entries = _parse_preference_book()
    hits = []
    seen = set()
    for cand in candidates:
        cand_l = cand.lower()
        for e in entries:
            key = (e["alias"], e["name"], e["contact"])
            if key in seen:
                continue
            if e["alias"] and e["alias"].lower() == cand_l:
                hits.append(e); seen.add(key); continue
            if e["contact"] and e["contact"] == cand:
                hits.append(e); seen.add(key); continue
            if e["name"] and cand in e["name"]:
                hits.append(e); seen.add(key); continue
    return hits


def resolve_address(role, keyword, region=None):
    """
    统一的地址解析入口。
    流程：
      1) 先查 PREFERENCE.md 地址簿（命中 1 条且齐全 → address_book_hit）
      2) 未命中或字段不全 → 调 get_place_suggestion
      3) 分类 POI / SUG / empty
      4) 返回结构化 decision

    返回结构：
      {
        "decision": "address_book_hit" | "show_pois" | "need_sug_refinement" | "empty" | "error",
        "role": "sender" | "receiver",
        "pois": [...]            // show_pois 时
        "suggestions": [...]     // need_sug_refinement 时
        "entry": {...}           // address_book_hit 时（含 contact/phone 默认值）
        "hint": "..."            // empty/error 时用户提示
      }
    """
    role = role if role in ("sender", "receiver") else "sender"
    # 地址类场景的下一步文档：sender → step-1，receiver → step-2
    addr_doc = (
        "references/delivery/step-1-sender.md"
        if role == "sender" else "references/delivery/step-2-receiver.md"
    )

    # Step 0: keyword 来源合法性兜底 —— 防止 LLM 在用户没给地址时
    # 凭背景知识/常识捏造关键词去搜（详见 step-1-sender.md §0）
    kw = (keyword or "").strip()
    if len(kw) < 2:
        ask_tpl = (
            "请问您要从哪里寄出？可以告诉我大致地点（小区名 / 楼宇 / 商家名），"
            "或直接说「从公司」、「从家」等已保存的地址。"
            if role == "sender"
            else "请问您要寄到哪里？可以告诉我大致地点（小区名 / 楼宇 / 商家名），"
            "或直接说「寄到公司」、「寄给张三」等已保存的地址。"
        )
        return emit({
            "decision": "need_user_input",
            "role": role,
            "hint": (
                "keyword 为空或过短：禁止用模型自己推测的地址关键词调本命令。"
                "请先开口问用户具体地点或已保存的地址簿别名（见 step-1-sender.md §0），"
                "拿到用户原话提到的词后再重调 resolve-address。"
            ),
            "next_doc": addr_doc + "#0-调命令前的前置判断硬约束",
            "next_action": (
                "ask_user_for_sender_address" if role == "sender"
                else "ask_user_for_receiver_address"
            ),
            "reply_template": ask_tpl,
        }, exit_code=1)

    # Step 1: 地址簿匹配
    hits = _address_book_match(keyword)
    # 仅当命中 1 条且地址名称+经纬度齐全时直接返回
    usable = [h for h in hits if h.get("name") and h.get("lng") and h.get("lat")]
    if len(usable) == 1:
        h = usable[0]
        try:
            lng = float(h["lng"]); lat = float(h["lat"])
        except (TypeError, ValueError):
            lng, lat = None, None
        if lng is not None and lat is not None:
            result = {
                "decision": "address_book_hit",
                "role": role,
                "entry": {
                    "alias": h["alias"],
                    "name": h["name"],
                    "longitude": lng,
                    "latitude": lat,
                    "poiid": None,          # 地址簿暂不存 POI id
                    "contact": h.get("contact") or None,
                    "phone": h.get("phone") or None,
                },
                "hint": f"命中地址簿别名「{h['alias']}」，建议直接使用并向用户确认",
                "next_doc": addr_doc,
            }
            return emit(result)

    # Step 1.5: 拦截"姓名形态 keyword + 地址簿未命中"的 fallthrough。
    # 设计动机详见 _looks_like_person_name() docstring。
    # "联系人名作为合法 keyword" 的隐含前提是地址簿中存有该联系人；
    # 一旦地址簿没命中，姓名形态的 keyword 不应继续 fallthrough 到 POI 搜索，
    # 否则会得到一堆同名村庄/店铺等高噪声结果。
    if not usable and _looks_like_person_name(kw):
        ask_tpl = (
            f"您提到的「{kw}」看起来像联系人姓名，但目前地址簿中并未保存此联系人的地址。\n\n"
            "请告诉我具体的寄件地点（小区名 / 楼宇 / 商家名），"
            "或直接说「从公司」、「从家」等已保存的地址。"
            if role == "sender"
            else f"您提到的「{kw}」看起来像联系人姓名，但目前地址簿中并未保存此联系人的地址。\n\n"
            "请告诉我具体的收件地点（小区名 / 楼宇 / 商家名），"
            "或直接说「寄到公司」等已保存的地址。"
        )
        return emit({
            "decision": "need_user_input",
            "role": role,
            "hint": (
                f"keyword「{kw}」形态像中文姓名（2-4 字纯中文且无地名特征字），"
                "且地址簿未命中此联系人。'联系人名作为合法 keyword' 的隐含前提是"
                "地址簿命中——未命中时禁 fallthrough 到 POI 搜索（会召回大量同名 POI 噪音）。"
                "请询问用户具体寄件/收件地点的小区名 / 楼宇 / 商家名。"
            ),
            "next_doc": addr_doc + "#0-调命令前的前置判断硬约束",
            "next_action": (
                "ask_user_for_sender_address" if role == "sender"
                else "ask_user_for_receiver_address"
            ),
            "reply_template": ask_tpl,
        }, exit_code=1)

    # 多匹配或字段不全 → 走 get_place_suggestion
    result = _MCP.invoke("get_place_suggestion", {
        "keyword": keyword,
        "region": region or "",
        "pageSize": 20,
        "pageIndex": 1,
        "policy": "1",
    })
    if not result.ok:
        # token 失效独立走 to_error_dict()，带 reply_template 引导用户重新绑定
        if result.error_kind in ("no_token", "token_invalid"):
            return emit(result.to_error_dict(), exit_code=1)
        return emit({
            "decision": "error",
            "role": role,
            "hint": f"MCP 调用失败: {result.error_message}",
            "next_doc": _doc_for_scenario("mcp_error"),
        }, exit_code=1)

    mcp_data = result.payload if isinstance(result.payload, dict) else {}

    data_list = (mcp_data.get("data") or {}).get("dataList") or []
    pois = []
    sugs = []
    for item in data_list:
        loc = item.get("location") or {}
        lat = loc.get("lat")
        lng = loc.get("lng")
        entry = {
            "name": item.get("title", ""),
            "address": item.get("address", ""),
            "longitude": lng,
            "latitude": lat,
            "poiid": item.get("id", ""),
        }
        if lat and lng:  # 非零非空 = 真实 POI
            pois.append(entry)
        else:
            sugs.append(entry)

    if pois:
        # 最多返回 10 条（LLM 展示用），过多也是 context 浪费
        capped = pois[:10]
        # —— 杠杆 3：把 pois 缓存到 session._last_pois.<role>，供 pick-address 按序号直接取 ——
        try:
            session = _load_session() or _empty_session()
            cache = session.get("_last_pois") or {}
            cache[role] = capped
            session["_last_pois"] = cache
            _save_session(session)
        except Exception:
            # 缓存失败不阻塞主流程（LLM 仍可用 commit-address 回退）
            pass

        result = {
            "decision": "show_pois",
            "role": role,
            "pois": capped,
            "hint": "向用户展示编号列表，等待其回复序号；用户选完后用 `pick-address <role> <序号>` 一步完成落盘",
            "reply_template": _tpl_pick_poi_list(role, capped),
            "next_doc": addr_doc,
        }
        return emit(result)

    if sugs:
        return emit({
            "decision": "need_sug_refinement",
            "role": role,
            "suggestions": [s["name"] for s in sugs[:10]],
            "hint": "让用户从建议词中选一个更精确的关键词，重新调 resolve-address",
            "next_doc": addr_doc,
        })

    return emit({
        "decision": "empty",
        "role": role,
        "hint": "未找到结果，请让用户更换关键词或补充城市",
        "next_doc": addr_doc,
    })


def validate_phone(raw):
    """归一化 + 正则校验手机号（内部工具，供 commit-contact 调用）。

    规则：
      1. 去除空格、短横线、括号
      2. 以 "+86" 开头则去掉
      3. 正则：^1[3-9]\\d{9}$
    返回 (valid: bool, normalized_or_raw: str, reason: "empty"|"format"|None)
    """
    if raw is None or raw == "":
        return False, "", "empty"

    normalized = re.sub(r"[\s\-()（）]", "", str(raw))
    if normalized.startswith("+86"):
        normalized = normalized[3:]

    if re.match(r"^1[3-9]\d{9}$", normalized):
        return True, normalized, None
    return False, normalized, "format"


# ============================================================
# FSM 驱动器（state next）—— v1.2.0+ 新增
# ============================================================
#
# 设计动机：
#   LLM 在下单流程每一步都需要"自己判断当前状态"，消耗大量 context。
#   用状态机显式告诉它：你现在在哪、下一步做什么、参考哪个文档。
#
# LLM 的使用姿势：
# LLM 的使用姿势：
#   1. 进入任意轮对话后，调 `state next` 拿到 {current_state, next_action, next_doc}
#   2. 按 next_doc 读对应文档片段（Progressive Disclosure）
#   3. 与用户沟通 + 执行指令
#   4. 落盘后再调 `state next` 进入下一状态
#
# 状态清单（按下单流程线性推进）：
#   empty                 → 无 session，进入 reconcile
#   step0-extract         → reconcile 完成，需要做第零步意图预抽取
#   step1-sender-address  → 需要确定寄件地址
#   step1-sender-contact  → 寄件地址已定，需要寄件人姓名+手机号
#   step2-receiver-address→ 需要确定收件地址
#   step2-receiver-contact→ 收件地址已定，需要收件人姓名+手机号
#   step3-estimate        → 地址人信息齐全，需要调询价
#   step4-select          → 询价完成，需要让用户选序号
#   step5-book            → 用户已选，需要下单
#   step6-payment         → 下单完成，需要引导支付
#   step7-confirm         → 订单已出，等支付确认
#   has-order             → 已有 orderCode 续聊（查/改/取消）
# ============================================================


# ------------------------------------------------------------
# 状态推断：按优先级从高到低排列的谓词表
# ------------------------------------------------------------
# 每一项 (state_name, predicate)；第一个命中的谓词决定当前状态。
# 谓词接收一个 flat dict（由 _state_signals 生成），纯布尔逻辑，无副作用。
# ------------------------------------------------------------
_STATE_PREDICATES = (
    ("has-order",              lambda s: bool(s["order_code"])),
    ("step5-book",             lambda s: bool(s["selected_sku"])),
    ("step4-select",           lambda s: bool(s["sku_map"] and s["est_id"])),
    ("step3-estimate",         lambda s: s["s_addr_ok"] and s["s_contact_ok"] and s["r_addr_ok"] and s["r_contact_ok"]),
    ("step2-receiver-contact", lambda s: s["s_addr_ok"] and s["s_contact_ok"] and s["r_addr_ok"]),
    ("step2-receiver-address", lambda s: s["s_addr_ok"] and s["s_contact_ok"]),
    ("step1-sender-contact",   lambda s: s["s_addr_ok"]),
)


def _state_signals(session):
    """把 session 压缩成状态推断需要的最小特征 dict。"""
    sender = session.get("sender") or {}
    receiver = session.get("receiver") or {}
    s_addr = sender.get("address") or {}
    r_addr = receiver.get("address") or {}
    return {
        "order_code":    session.get("orderCode"),
        "selected_sku":  session.get("selectedSkuId"),
        "sku_map":       session.get("skuMap"),
        "est_id":        session.get("estimatePriceRecordId"),
        "s_addr_ok":     not _is_empty(s_addr.get("name")) and not _is_empty(s_addr.get("longitude")),
        "s_contact_ok":  not _is_empty(sender.get("name")) and not _is_empty(sender.get("phone")),
        "r_addr_ok":     not _is_empty(r_addr.get("name")) and not _is_empty(r_addr.get("longitude")),
        "r_contact_ok":  not _is_empty(receiver.get("name")) and not _is_empty(receiver.get("phone")),
    }


def _compute_current_state(session):
    """根据 session.json 各字段存在性推断当前状态（表驱动版）。"""
    if session is None:
        return "empty"
    signals = _state_signals(session)
    for state_name, predicate in _STATE_PREDICATES:
        if predicate(signals):
            return state_name
    return "step1-sender-address"


# 状态 → 下一步动作元数据
_STATE_META = {
    "empty": {
        "next_action": "run_entry_rituals",
        "required_fields": [],
        "doc_ref": "SKILL.md#entry-hard-rule",
        "user_reply_hint": "执行 §0 三动作（preflight + query_going_order + reconcile），不要对用户说任何业务话术",
    },
    "step0-extract": {
        "next_action": "extract_intent_and_go_step1",
        "required_fields": [],
        "doc_ref": "references/delivery/step-1-sender.md",
        "user_reply_hint": "对用户首条消息做一次性信息抽取（不调工具），然后进入第一步",
    },
    "step1-sender-address": {
        "next_action": "resolve_sender_address",
        "required_fields": ["sender.address.name", "sender.address.longitude", "sender.address.latitude"],
        "script_helper": "resolve-address sender <keyword> [region] → commit-address sender <poi_json>",
        "doc_ref": "references/delivery/step-1-sender.md#1.1",
        "user_reply_hint": "若用户当轮消息提到具体地名或地址簿别名（公司/家/妈妈家/联系人名）→ 把原词传给 resolve-address sender <keyword>（脚本会先查地址簿）；若完全没提任何地点 → 先开口问『从哪里寄？（小区名 / 楼宇 / 商家名，或「从公司/从家」等已保存地址）』；禁基于背景知识/常识/IP 归属自行捏造关键词",
    },
    "step1-sender-contact": {
        "next_action": "collect_sender_contact",
        "required_fields": ["sender.name", "sender.phone"],
        "script_helper": "commit-contact sender <name> <phone>",
        "doc_ref": "references/delivery/step-1-sender.md#1.2",
        "user_reply_hint": "请提供寄件人姓名和手机号（骑手取件时需要联系）",
    },
    "step2-receiver-address": {
        "next_action": "resolve_receiver_address",
        "required_fields": ["receiver.address.name", "receiver.address.longitude", "receiver.address.latitude"],
        "script_helper": "resolve-address receiver <keyword> [region] → commit-address receiver <poi_json>",
        "doc_ref": "references/delivery/step-2-receiver.md#2.1",
        "user_reply_hint": "若用户当轮消息提到具体地名或地址簿别名（公司/家/妈妈家/联系人名）→ 把原词传给 resolve-address receiver <keyword>（脚本会先查地址簿）；若完全没提任何地点 → 先开口问『寄到哪里？（小区名 / 楼宇 / 商家名，或「寄到公司/寄给张三」等已保存地址）』；禁基于背景知识/常识/IP 归属自行捏造关键词",
    },
    "step2-receiver-contact": {
        "next_action": "collect_receiver_contact",
        "required_fields": ["receiver.name", "receiver.phone"],
        "script_helper": "commit-contact receiver <name> <phone>",
        "doc_ref": "references/delivery/step-2-receiver.md#2.2",
        "user_reply_hint": "请提供收件人姓名和手机号",
    },
    "step3-estimate": {
        "next_action": "run_estimate",
        "required_fields": ["estimatePriceRecordId", "skuMap"],
        "script_helper": "run-estimate",
        "doc_ref": "references/delivery/step-3-estimate.md",
        "user_reply_hint": "调 run-estimate 一条命令完成断言+兜底+询价+落盘，然后展示报价表格",
    },
    "step4-select": {
        "next_action": "wait_user_sku_selection",
        "required_fields": ["selectedSkuId"],
        "script_helper": "select-sku <序号>（已内嵌 TTL 预检）",
        "doc_ref": "references/delivery/step-4-select.md",
        "user_reply_hint": "等待用户选序号；选完用 select-sku 一条命令完成落盘 + TTL 预检",
    },
    "step5-book": {
        "next_action": "place_order",
        "required_fields": ["orderCode"],
        "script_helper": "book-order（自动从 session 读参数、调 MCP、落盘 orderCode）",
        "doc_ref": "references/delivery/step-5-book.md",
        "user_reply_hint": "进本步前必须 select-sku 返回 fresh=true；调 book-order 一步完成下单",
    },
    "step6-payment": {
        "next_action": "guide_payment",
        "required_fields": [],
        "script_helper": "直接使用 payInfo.scanUrl 展示支付二维码图片",
        "doc_ref": "references/delivery/step-6-payment.md",
        "user_reply_hint": "展示支付二维码或支付链接",
    },
    "step7-confirm": {
        "next_action": "confirm_payment_and_cleanup",
        "required_fields": [],
        "script_helper": "mcp-call runerrand_query_order_detail",
        "doc_ref": "references/delivery/step-7-confirm.md",
        "user_reply_hint": "查订单详情，确认支付，state clear",
    },
    "has-order": {
        "next_action": "treat_as_existing_order",
        "required_fields": [],
        "script_helper": "mcp-call runerrand_query_order_detail / runerrand_precancel_order",
        "doc_ref": "references/order-workflow.md",
        "user_reply_hint": "按用户意图走查单/取消/骑手追踪流程",
    },
}


def state_next():
    """FSM 驱动器：告诉 LLM 当前状态和下一步该做什么。"""
    session = _load_session()
    state = _compute_current_state(session)
    meta = _STATE_META.get(state, {})
    doc = meta.get("doc_ref") or _doc_for_state(state)

    return emit({
        "current_state": state,
        "next_action": meta.get("next_action"),
        "required_fields": meta.get("required_fields", []),
        "script_helper": meta.get("script_helper"),
        "next_doc": doc,
        "user_reply_hint": meta.get("user_reply_hint"),
        "filled_fields": _collect_filled_fields(session),
    })


# ============================================================
# 询价新鲜度 TTL 标记
# ============================================================
#
# 设计要点：
#   1. 询价成功时 MCPClient 自动写 estimate_at 时间戳（LLM 零感知）
#   2. TTL 预检已内嵌到 `select-sku` 命令（用户选序号后一步完成）
#   3. 阈值 ESTIMATE_FRESH_SECONDS = 3 分钟
#   4. 预检仅用于"**是否需要让用户重新确认**"，不自动刷新、不自动下单
#      —— 严格遵守硬约束：询价到下单之间必须有用户二次确认
# ============================================================


def _record_estimate_at_on_success(mcp_text):
    """
    mcp_call 内部钩子：检测到 runerrand_estimate_price 成功返回时，
    自动把当前时间戳写入 session.estimate_at。LLM 零感知，避免遗漏。

    仅在 code == 0 且 data.estimatePriceRecordId 非空时触发。
    失败场景（询价 code != 0）不动时间戳，避免错误地把失败请求也当成"新鲜询价"。
    """
    try:
        payload = json.loads(mcp_text) if mcp_text else {}
    except (json.JSONDecodeError, TypeError):
        return
    if not isinstance(payload, dict):
        return
    if payload.get("code") != 0:
        return
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        return
    if not data.get("estimatePriceRecordId"):
        return

    session = _load_session()
    if session is None:
        # 没有 session 时不强行 init；等主流程自己写 recordId 时会先 init
        return
    session["estimate_at"] = int(time.time())
    _save_session(session)


# ============================================================
# 组合命令（v1.3.0+ 效率优化）—— 减少 LLM 脚本调用次数
# ============================================================
#
# 设计动机：
#   之前每个原子操作都是独立脚本调用（手机号校验 → state set name → state set phone → state next），
#   导致 LLM 一轮要跑 4+ 次脚本。组合命令把常见的"原子序列"打包成一条命令，
#   减少 LLM 调用次数从而减少延迟和 context 占用。
# ============================================================


def commit_contact(role, name, phone):
    """
    一条命令完成：手机号校验 + state set {role}.name + state set {role}.phone + state next
    返回：
      成功: {"status":"ok","valid":true,"normalized":"...","next_state":"...","filled_fields":[...]}
      手机号无效: {"valid":false,"reason":"...","hint":"..."}
      WRITE_GUARD 失败: {"status":"error","error":"write_guard_violation",...}
    """
    if role not in ("sender", "receiver"):
        return fail("invalid_role", "role must be sender/receiver")

    # 1. 手机号校验（复用内部工具 validate_phone）
    phone_ok, normalized, reason = validate_phone(phone)
    if not phone_ok:
        if reason == "empty":
            return emit({
                "valid": False, "reason": "empty", "raw": phone or "",
                "hint": "手机号为空",
            }, exit_code=1)
        return emit({
            "valid": False, "reason": "format", "raw": str(phone),
            "normalized": normalized,
            "hint": "请提供 11 位大陆手机号（以 13/14/15/16/17/18/19 开头）",
        }, exit_code=1)

    # 2. 写入 session
    session = _load_session()
    if session is None:
        session = _empty_session()

    name_path = f"{role}.name"
    phone_path = f"{role}.phone"

    # WRITE_GUARD 检查
    passed, reason = _check_write_guard(session, name_path)
    if not passed:
        return fail("write_guard_violation", reason, path=name_path)

    passed, reason = _check_write_guard(session, phone_path)
    if not passed:
        return fail("write_guard_violation", reason, path=phone_path)

    _set_by_path(session, name_path, name)
    _set_by_path(session, phone_path, normalized)
    _save_session(session)

    # 3. 计算下一状态
    state = _compute_current_state(session)
    meta = _STATE_META.get(state, {})
    doc = meta.get("doc_ref") or _doc_for_state(state)

    return ok(
        valid=True,
        normalized=normalized,
        next_state=state,
        next_action=meta.get("next_action"),
        next_doc=doc,
        filled_fields=_collect_filled_fields(session),
    )


def prefill_contacts(s_name, s_phone, r_name, r_phone):
    """乱序预登记联系人字段（v1.4.0+ Step-0 信息预抽取专用）。

    设计动机：
      用户首条消息常一次性给齐"寄件人/收件人 姓名+手机号"，但当前线性 FSM
      要求先 sender.address → sender.contact → receiver.address → receiver.contact。
      若坚持串行采集，LLM 会陷入"用户已说但脚本不让存"的死局，体验差。

    本命令打破"按 step 顺序写"的约束（**仅对联系人字段**），允许任意时刻把
    已抽到的字段直接落 session：
      - 联系人字段不参与任何 MCP 调用，纯本地写盘 → 安全
      - 后续 _compute_current_state 自动按"已填字段跳过"推进 FSM
      - 询价前 _estimate_core 的完整字段检查仍是最终保底

    入参语义：每个字段都允许传空串（""）表示"用户消息中未抽到此字段，跳过写入"。
    手机号字段非空时**必须**通过 validate_phone，否则整条命令拒绝（避免脏数据）。
    姓名字段非空时不做格式校验（中文姓名形态多样）。

    返回：
      成功 {"status":"ok","prefilled":["sender.name","sender.phone",...],
            "skipped":["receiver.name",...],
            "next_state":"...","next_action":"...","next_doc":"...",
            "filled_fields":[...],
            "user_reply_hint":"..."}
      手机号格式错误：{"status":"error","error":"invalid_phone",
                       "field":"sender.phone","raw":"...","hint":"..."}
    """
    # 1. 入参规范化（None / 占位字符串都视为空，统一空串语义）
    def _norm(v):
        if v is None:
            return ""
        v = str(v).strip()
        # 兼容 LLM 可能传入的占位词
        if v.lower() in ("", "none", "null", "-", "n/a"):
            return ""
        return v

    s_name = _norm(s_name)
    r_name = _norm(r_name)
    s_phone_raw = _norm(s_phone)
    r_phone_raw = _norm(r_phone)

    # 2. 手机号字段非空时校验格式（任一失败整体拒绝，不做"部分写入"）
    s_phone_normalized = ""
    if s_phone_raw:
        ok_phone, normalized, reason = validate_phone(s_phone_raw)
        if not ok_phone:
            return fail("invalid_phone",
                        f"sender.phone 格式不合法（{reason}）",
                        field="sender.phone", raw=s_phone_raw,
                        hint="请提供 11 位大陆手机号（以 13/14/15/16/17/18/19 开头），或传空串跳过")
        s_phone_normalized = normalized

    r_phone_normalized = ""
    if r_phone_raw:
        ok_phone, normalized, reason = validate_phone(r_phone_raw)
        if not ok_phone:
            return fail("invalid_phone",
                        f"receiver.phone 格式不合法（{reason}）",
                        field="receiver.phone", raw=r_phone_raw,
                        hint="请提供 11 位大陆手机号（以 13/14/15/16/17/18/19 开头），或传空串跳过")
        r_phone_normalized = normalized

    # 3. 写入 session（绕过 WRITE_GUARD —— 联系人字段不触发 MCP，安全）
    session = _load_session() or _empty_session()

    # 已下单态硬拦截：避免覆盖已下单的联系人快照
    if not _is_empty(session.get("orderCode")):
        return fail("order_in_progress",
                    "已存在 orderCode，禁止 prefill 联系人；如需新单请先 state clear",
                    hint="prefill-contacts 仅用于草稿态的 step-0 预抽取")

    prefilled = []
    skipped = []

    pairs = [
        ("sender.name",     s_name),
        ("sender.phone",    s_phone_normalized),
        ("receiver.name",   r_name),
        ("receiver.phone",  r_phone_normalized),
    ]
    for path, val in pairs:
        if val:
            # 已有非空值时优先保留旧值（用户后续修改请走 commit-contact，避免 prefill 误覆盖）
            existing = _get_by_path(session, path)
            if not _is_empty(existing) and existing != val:
                skipped.append({"path": path, "reason": "already_filled", "existing": "***" if "phone" in path else existing})
                continue
            _set_by_path(session, path, val)
            prefilled.append(path)
        else:
            skipped.append({"path": path, "reason": "empty_input"})

    _save_session(session)

    # 4. 计算下一状态（已填字段会被 _STATE_PREDICATES 自动跳过）
    state = _compute_current_state(session)
    meta = _STATE_META.get(state, {})
    doc = meta.get("doc_ref") or _doc_for_state(state)

    return ok(
        prefilled=prefilled,
        skipped=skipped,
        next_state=state,
        next_action=meta.get("next_action"),
        next_doc=doc,
        filled_fields=_collect_filled_fields(session),
        user_reply_hint=meta.get("user_reply_hint"),
    )



def commit_address(role, poi_json_str):
    """
    一条命令完成：state set {role}.address + 查 PREFERENCE 默认联系人 + state next
    入参 poi_json_str: {"name":"...","longitude":N,"latitude":N,"poiid":"..."}
    返回：
      {
        "status": "ok",
        "contact_hit": true/false,
        "contact_name": "...",      // hit 时
        "contact_phone": "...",     // hit 时
        "next_state": "...",
        "next_action": "...",
        "next_doc": "...",
        "user_reply_hint": "..."    // 如有默认联系人，告诉 LLM 可直接确认
      }
    """
    if role not in ("sender", "receiver"):
        return fail("invalid_role", "role must be sender/receiver")

    try:
        poi = json.loads(poi_json_str)
    except (json.JSONDecodeError, TypeError) as e:
        return fail("parse_error", f"poi JSON 解析失败: {e}")

    if not isinstance(poi, dict) or not poi.get("name"):
        return fail("invalid_poi", "poi 必须含 name 字段")

    # 1. 写入 address
    session = _load_session()
    if session is None:
        session = _empty_session()

    addr_path = f"{role}.address"
    passed, reason = _check_write_guard(session, addr_path)
    if not passed:
        # 尝试检查子路径
        passed2, reason2 = _check_write_guard(session, f"{addr_path}.name")
        if not passed2:
            return fail("write_guard_violation", reason or reason2, path=addr_path)

    _set_by_path(session, addr_path, poi)
    _save_session(session)

    # 2. 查 PREFERENCE 地址簿默认联系人
    contact_name = contact_phone = None
    addr_name = poi.get("name", "")
    for e in _parse_preference_book():
        if e.get("name") == addr_name and e.get("contact") and e.get("phone"):
            contact_name = e["contact"]
            contact_phone = e["phone"]
            break
    contact_hit = contact_name is not None

    # 3. 组装响应
    state = _compute_current_state(session)
    meta = _STATE_META.get(state, {})
    doc = meta.get("doc_ref") or _doc_for_state(state)
    extra = {}
    if contact_hit:
        extra["contact_name"] = contact_name
        extra["contact_phone"] = contact_phone
        extra["user_reply_hint"] = f"地址簿匹配到默认联系人：{contact_name} {contact_phone}，向用户确认是否使用"
    else:
        extra["user_reply_hint"] = meta.get("user_reply_hint", "请提供联系人姓名和手机号")

    return ok(
        contact_hit=contact_hit,
        next_state=state,
        next_action=meta.get("next_action"),
        next_doc=doc,
        **extra,
    )


def _estimate_core(skip_entry_assert=False, mode="run"):
    """询价核心逻辑（run-estimate / re-estimate 共用）。

    Args:
        skip_entry_assert: True=跳过 step3-entry 断言（重询场景用）
        mode: "run" | "re"，仅用于错误信息区分

    Returns:
        (exit_code, mcp_response_text_or_none)
    """
    session = _load_session()
    if session is None:
        return fail("assert", "session 为空，无法进入询价",
                    stderr_copy=True, stage="assert", mode=mode,
                    next_doc="references/delivery/step-3-estimate.md")

    # 1. 步首断言（re-estimate 场景跳过）
    if not skip_entry_assert:
        rule = ENTRY_ASSERTIONS["step3-entry"]
        violations = []
        for path in rule["require_filled"]:
            value = _get_by_path(session, path)
            if _is_empty(value):
                violations.append({"path": path, "expected": "non_empty", "actual": "empty"})
        for path in rule["require_empty"]:
            value = _get_by_path(session, path)
            if not _is_empty(value):
                violations.append({"path": path, "expected": "empty", "actual": "filled"})
        if violations:
            return fail("assert", rule["description"],
                        stderr_copy=True, stage="assert", mode=mode,
                        violations=violations,
                        hint="若因询价过期需要重询，请使用 re-estimate 命令",
                        next_doc=_doc_for_scenario("re_estimate"))

    # 2. sanity-check（寄=收兜底 + 字段完整性）
    issues = []
    required = [
        "sender.address.name", "sender.address.longitude", "sender.address.latitude",
        "sender.name", "sender.phone",
        "receiver.address.name", "receiver.address.longitude", "receiver.address.latitude",
        "receiver.name", "receiver.phone",
    ]
    for path in required:
        value = _get_by_path(session, path)
        if _is_empty(value):
            issues.append({"type": "missing_field", "path": path})

    number_paths = [
        "sender.address.longitude", "sender.address.latitude",
        "receiver.address.longitude", "receiver.address.latitude",
    ]
    for path in number_paths:
        v = _get_by_path(session, path)
        if v is not None and not isinstance(v, (int, float)):
            issues.append({"type": "invalid_number", "path": path, "value": str(v)})

    # 寄=收兜底
    s_addr = (session.get("sender") or {}).get("address") or {}
    r_addr = (session.get("receiver") or {}).get("address") or {}
    s_poiid = s_addr.get("poiid")
    r_poiid = r_addr.get("poiid")
    s_lng, s_lat = s_addr.get("longitude"), s_addr.get("latitude")
    r_lng, r_lat = r_addr.get("longitude"), r_addr.get("latitude")

    same = False
    if s_poiid and r_poiid and s_poiid == r_poiid:
        same = True
    elif all(isinstance(x, (int, float)) for x in (s_lng, s_lat, r_lng, r_lat)):
        if abs(float(s_lng) - float(r_lng)) < 1e-5 and abs(float(s_lat) - float(r_lat)) < 1e-5:
            same = True
    if same:
        issues.append({
            "type": "same_location",
            "display_name": s_addr.get("name") or r_addr.get("name") or "",
        })

    if issues:
        return fail("sanity_check", "询价前置校验失败",
                    stderr_copy=True, stage="sanity_check", mode=mode,
                    issues=issues,
                    next_doc="references/delivery/step-3-estimate.md")

    # 3. 组装参数，调 MCP
    sender = session.get("sender") or {}
    receiver = session.get("receiver") or {}
    result = _MCP.invoke("runerrand_estimate_price", {
        "fromLng": s_addr.get("longitude"),
        "fromLat": s_addr.get("latitude"),
        "fromUserName": sender.get("name"),
        "fromUserPhone": sender.get("phone"),
        "fromAddrDetail": s_addr.get("name"),
        "toLng": r_addr.get("longitude"),
        "toLat": r_addr.get("latitude"),
        "toUserName": receiver.get("name"),
        "toUserPhone": receiver.get("phone"),
        "toAddrDetail": r_addr.get("name"),
    })
    if not result.ok:
        # token 失效独立走 to_error_dict()，带 reply_template 引导用户重新绑定
        if result.error_kind in ("no_token", "token_invalid"):
            return emit(result.to_error_dict(), exit_code=1)
        return fail("mcp_call", result.error_message or "MCP 调用失败",
                    stderr_copy=True, stage="mcp_call", mode=mode,
                    next_doc=_doc_for_scenario("mcp_error"))

    # 4. 解析响应 —— 非预期结构 / 业务失败原样透传；成功走 render
    inner_text = result.inner_text or ""
    mcp_data = result.payload if isinstance(result.payload, dict) else None

    if not mcp_data:
        print(inner_text or result.raw_body or "")
        return 0

    if mcp_data.get("code") != 0:
        # 业务失败（如 10001 参数校验、510008 询价失效等）：原样输出 inner_text
        print(inner_text)
        return 0

    return _render_estimate_success(mcp_data, mode)


def _render_estimate_success(mcp_data, mode):
    """询价成功后的渲染 + 落盘。

    输出增强 JSON：原 MCP 结构 + display_rows + senderAddr + receiverAddr + mode + hint。
    副作用：按 totalFee 升序生成 skuMap 并落盘（estimate_at 已由 MCPClient 写入，
    这里重新 _load_session 确保不覆盖）。
    """
    data = mcp_data.get("data") or {}
    record_id = data.get("estimatePriceRecordId")
    sp_list = data.get("spEstimatePrices") or []

    # 🛑 关键：重新加载 session，避免覆盖 MCPClient 刚写入的 estimate_at
    session = _load_session() or _empty_session()

    if record_id:
        _ok, _reason = _check_write_guard(session, "estimatePriceRecordId")
        if _ok:
            _set_by_path(session, "estimatePriceRecordId", record_id)

    # 按 totalFee 升序排序 + 生成 skuMap + display_rows
    def _fee_key(item):
        try:
            return (0, float(item.get("totalFee")))
        except (TypeError, ValueError):
            return (1, 0.0)

    sorted_list = sorted(sp_list, key=_fee_key) if isinstance(sp_list, list) else []
    sku_map = {}
    display_rows = []
    for i, item in enumerate(sorted_list, start=1):
        sku_id = item.get("skuId") or ""
        if sku_id:
            sku_map[str(i)] = sku_id
        # 预格式化 deliveryTime："2026-04-30 12:36:15" → "12:36"
        dt_raw = item.get("deliveryTime") or ""
        dt_short = dt_raw[11:16] if isinstance(dt_raw, str) and len(dt_raw) >= 16 else "-"
        display_rows.append({
            "no": i,
            "spName": item.get("spName") or "",
            "expressTypeName": item.get("expressTypeName") or "",
            "totalFee": item.get("totalFee") or "",
            "deliveryTime_short": dt_short,
            "defaultChecked": item.get("defaultChecked", 0),
        })

    if sku_map:
        _ok, _reason = _check_write_guard(session, "skuMap")
        if _ok:
            _set_by_path(session, "skuMap", sku_map)

    _save_session(session)

    sender_addr = ((session.get("sender") or {}).get("address") or {}).get("name") or ""
    receiver_addr = ((session.get("receiver") or {}).get("address") or {}).get("name") or ""
    table_md = _tpl_estimate_table(display_rows, sender_addr, receiver_addr)
    if mode == "re" and table_md:
        # 重询场景在表格前加警示，避免静默代下单
        reply_template = (
            "⚠️ 报价已刷新\n\n"
            "由于价格每隔一段时间会更新，已为您获取最新报价，请重新确认：\n\n"
            f"{table_md}"
        )
    else:
        reply_template = table_md
    return emit({
        **mcp_data,
        "display_rows": display_rows,
        "senderAddr": sender_addr,
        "receiverAddr": receiver_addr,
        "mode": mode,
        "hint": "skuMap 已自动落盘；reply_template 已包含完整 markdown 表格，原样贴给用户即可，禁止再用编号嵌套列表",
        "reply_template": reply_template,
        "next_doc": "references/delivery/step-4-select.md",
    })


def run_estimate():
    """
    第三步首次询价（一条命令完成）：
      1. 步首断言（估价记录 ID 为空 + 寄收件信息齐全）
      2. 寄=收兜底 + 字段完整性检查
      3. 调 runerrand_estimate_price
      4. 成功后自动 state set estimatePriceRecordId + estimate_at

    使用场景：正常流程从第二步完成后进入第三步时调用（session 中 estimatePriceRecordId 应为空）。
    重询价（询价过期 / TTL 预检失败 / 40205）请改用 re-estimate。

    返回：
      成功：直接输出 mcp 返回的询价结果 JSON
      前置失败：{"status":"error","stage":"assert|sanity_check",...}（stdout+stderr 双写）
      MCP 失败：{"status":"error","stage":"mcp_call","message":"..."}
    """
    return _estimate_core(skip_entry_assert=False, mode="run")


def re_estimate():
    """
    询价重试（专用于询价过期 / TTL 预检失败 / 40205 场景）。

    与 run-estimate 的关键差异：
      - 跳过 step3-entry 断言（允许 estimatePriceRecordId 非空进入）
      - 进入前自动作废旧的 estimatePriceRecordId / skuMap / selectedSkuId
      - 调用成功后自动写入新的 estimatePriceRecordId + estimate_at

    语义：用户刚选完序号但 TTL 过期时，LLM 用一条命令安全地刷新报价。
    不会代用户下单，严格遵循「重询 + 等用户按新序号二次确认」的硬约束。

    返回：
      成功：直接输出 mcp 返回的新询价结果 JSON（供上层按 skuMap 展示）
      失败：{"status":"error","stage":"...","mode":"re",...}（stdout+stderr 双写）
    """
    # 作废旧值（幂等；即使字段本就为空也不会报错）
    session = _load_session()
    if session is None:
        return fail("assert", "session 为空，无法执行 re-estimate",
                    stderr_copy=True, stage="assert", mode="re",
                    next_doc="references/delivery/step-3-estimate.md")

    for path in ("estimatePriceRecordId", "skuMap", "selectedSkuId", "estimate_at"):
        _set_by_path(session, path, None)
    _save_session(session)

    return _estimate_core(skip_entry_assert=True, mode="re")


# ============================================================
# 高阶组合命令（v1.3.2+，极致减少 LLM 工具调用次数）
# ============================================================
#
# 设计目标：把"3-5 分钟"压到"1.5-2.5 分钟"
#   - bootstrap：入口三合一（preflight + query_going_order + reconcile + state next）
#   - pick-address：用户选序号后一步到位（_last_pois[序号] → commit-address）
#   - select-sku：用户选 sku 序号一步到位（skuMap → selectedSkuId → freshness）
#
# 向后兼容：保留 preflight/mcp-call/state/commit-address 等旧命令。
# ============================================================


def bootstrap():
    """入口一条命令搞定：preflight + query_going_order + reconcile + state next。

    返回：
      {
        "stage": "ready" | "setup_token" | "error" | "has_ongoing_order",
        "decision": "init" | "keep",
        "hasOnGoingOrder": bool,
        "ongoing_order": {...},     # 有进行中订单时展开
        "current_state": "...",
        "next_action": "...",
        "next_doc": "...",
        "user_reply_hint": "..."
      }
    """
    # 1. preflight
    # 同时采集运行时诊断（编码/locale/LANG），注入到本次 bootstrap 所有出口的返回值。
    # 一次性在入口算好，避免每个 return 分支重复调用。
    diag = _collect_runtime_diag()

    if not _load_config().get("token"):
        return emit({
            "stage": "setup_token",
            "next_action": "ask_user_for_token",
            "next_doc": "references/quick-start-workflow.md",
            "user_reply_hint": "请先配置 Token：贴出二维码模板引导用户扫码取 Token，拿到后调 save-token 保存",
            "reply_template": _tpl_token_invalid("no_token", ""),
            "_diag": diag,
        }, exit_code=1)

    # 2. 静默调 query_going_order
    result = _MCP.invoke("runerrand_query_going_order", {})
    if not result.ok:
        # token 失效独立走 to_error_dict()，带 reply_template 引导用户重新绑定
        if result.error_kind in ("no_token", "token_invalid"):
            err_dict = result.to_error_dict()
            err_dict["_diag"] = diag
            return emit(err_dict, exit_code=1)
        return emit({
            "stage": "error",
            "next_action": "retry_or_check_token",
            "message": result.error_message or "MCP 调用失败",
            "_diag": diag,
        }, exit_code=1)

    payload = result.payload
    if not isinstance(payload, dict):
        return emit({"stage": "error", "message": f"MCP 响应格式异常: {payload}", "_diag": diag}, exit_code=1)

    # 3. reconcile（共用 _reconcile_decision，不产生 stdout）
    data = payload.get("data") or {}
    has_ongoing = bool(data.get("hasOnGoingOrder", False))
    server_order_code = data.get("orderCode") or (data.get("orderInfo") or {}).get("orderCode")

    session = _load_session()
    now = int(time.time())
    decision, reason = _reconcile_decision(session, has_ongoing, server_order_code, now)

    if decision == "init":
        empty = _empty_session()
        empty["last_update_at"] = now
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(empty, f, ensure_ascii=False, indent=2)

    # 4. 组装结果
    session = _load_session()
    state = _compute_current_state(session)
    meta = _STATE_META.get(state, {})

    if has_ongoing:
        # 有进行中订单：两种 decision 共用 ongoing_order 结构，仅 next_action / hint / next_doc 不同
        ongoing_order = {
            "orderCode": server_order_code,
            "expressTypeName": data.get("expressTypeName") or "",
            "orderStatusText": data.get("orderStatusText") or "",
            "spName": data.get("spName") or "",
            "orderStatus": data.get("orderStatus") or 0,
        }
        if decision == "keep":
            return emit({
                "stage": "has_ongoing_order",
                "decision": decision,
                "hasOnGoingOrder": True,
                "ongoing_order": ongoing_order,
                "current_state": state,
                "next_action": "continue_or_query_order",
                "next_doc": _doc_for_scenario("has_ongoing_resume"),
                "user_reply_hint": "您有一笔进行中的跑腿订单，请选择：查看详情 / 取消订单 / 继续该单流程",
                "reply_template": _tpl_has_ongoing_order(ongoing_order),
                "_diag": diag,
            })
        # decision == "init"：服务端有订单但本地对不上
        return emit({
            "stage": "has_ongoing_order",
            "decision": decision,
            "reason": reason,
            "hasOnGoingOrder": True,
            "ongoing_order": ongoing_order,
            "current_state": state,
            "next_action": "block_new_order",
            "next_doc": _doc_for_scenario("has_ongoing_block"),
            "user_reply_hint": "您有一笔进行中的跑腿订单，需先处理完成才能下新单",
            "reply_template": _tpl_has_ongoing_order(ongoing_order),
            "_diag": diag,
        })

    # 正常态：可以开始下单
    return emit({
        "stage": "ready",
        "decision": decision,
        "reason": reason,
        "hasOnGoingOrder": False,
        "current_state": state,
        "next_action": meta.get("next_action"),
        "next_doc": meta.get("doc_ref") or _doc_for_state(state),
        "user_reply_hint": meta.get("user_reply_hint") or "请告诉我您要寄送的起点地址",
        "_diag": diag,
    })


def pick_address(role, index_str):
    """用户回复序号后一步完成：从 _last_pois[role] 取第 N 条 POI → commit-address。

    省掉 LLM 手动从返回值里摘字段 + 构造 JSON + 再调 commit-address 的两步。

    Args:
      role: "sender" | "receiver"
      index_str: "1" | "2" | ... 用户回复的序号（1-based）

    返回：与 commit-address 相同的结构（向前兼容）。
    """
    if role not in ("sender", "receiver"):
        return fail("invalid_role", "role must be sender/receiver")

    try:
        index = int(index_str)
        if index < 1:
            raise ValueError("index must >= 1")
    except (TypeError, ValueError) as e:
        return fail("invalid_index", f"序号无效: {e}", hint="请提供 1 开始的正整数序号")

    session = _load_session()
    if session is None:
        return fail("no_session", "session 不存在", hint="请先调 resolve-address 搜索地址")

    cache = (session.get("_last_pois") or {}).get(role) or []
    if not cache:
        return fail("no_cached_pois", f"未找到 {role} 的候选 POI 缓存",
                    hint=f"请先调 resolve-address {role} <keyword>")

    if index > len(cache):
        return fail("index_out_of_range",
                    f"序号 {index} 超出范围（共 {len(cache)} 条）",
                    hint=f"请回复 1-{len(cache)} 之间的序号")

    poi = cache[index - 1]
    # 复用 commit_address —— 构造 json 参数
    poi_json = {
        "name": poi.get("name") or "",
        "longitude": poi.get("longitude"),
        "latitude": poi.get("latitude"),
        "poiid": poi.get("poiid") or "",
    }
    return commit_address(role, json.dumps(poi_json, ensure_ascii=False))


def select_sku(index_str):
    """用户回复序号下单前：从 skuMap 取 skuId → state set selectedSkuId → 内嵌 TTL 预检。

    省掉 LLM 手动两次 state 子命令 + 一次独立 TTL 预检命令的 3 次调用。

    Args:
      index_str: "1" | "2" | ... 用户回复的序号（对应报价表格行号）

    返回：
      新鲜且成功：{"status":"ok","selectedSkuId":"60797_1","fresh":true,
                   "next_action":"book_order","next_doc":"step-5-book.md"}
      过期：     {"status":"expired","fresh":false,"age_seconds":N,
                   "next_action":"re_estimate",
                   "hint":"询价已过期，请调 re-estimate 重询后让用户按新序号重选"}
      序号错误： {"status":"error","error":"invalid_index|no_sku_map",...}
    """
    try:
        index = int(index_str)
        if index < 1:
            raise ValueError("index must >= 1")
    except (TypeError, ValueError) as e:
        return fail("invalid_index", f"序号无效: {e}")

    session = _load_session()
    if session is None:
        return fail("no_session", "session 不存在", hint="请先调 run-estimate 询价")

    sku_map = session.get("skuMap") or {}
    if not isinstance(sku_map, dict) or not sku_map:
        return fail("no_sku_map", "skuMap 为空", hint="请先调 run-estimate 询价")

    sku_id = sku_map.get(str(index))
    if not sku_id:
        return fail("index_not_in_sku_map",
                    f"序号 {index} 不在 skuMap 中（共 {len(sku_map)} 条）",
                    hint=f"请让用户回复 1-{len(sku_map)} 之间的序号")

    # 写 selectedSkuId
    _ok, reason = _check_write_guard(session, "selectedSkuId")
    if not _ok:
        return fail("write_guard_violation", reason, path="selectedSkuId")

    _set_by_path(session, "selectedSkuId", sku_id)
    _save_session(session)

    # 内联 freshness 检查
    estimate_at = session.get("estimate_at")
    record_id = session.get("estimatePriceRecordId")
    now = int(time.time())

    if _is_empty(record_id):
        return fail("no_estimate", "尚未询价",
                    fresh=False, reason="no_estimate", hint="请先调 run-estimate",
                    next_doc=_doc_for_scenario("re_estimate"))

    if not isinstance(estimate_at, (int, float)) or estimate_at <= 0:
        return emit({
            "status": "expired",
            "fresh": False,
            "reason": "no_estimate_at",
            "next_action": "re_estimate",
            "hint": "询价时间戳缺失，请调 re-estimate 重询价后让用户按新序号重选",
            "next_doc": _doc_for_scenario("estimate_expired"),
        }, exit_code=1)

    age = now - int(estimate_at)
    if age > ESTIMATE_FRESH_SECONDS:
        return emit({
            "status": "expired",
            "fresh": False,
            "reason": "stale",
            "age_seconds": age,
            "threshold_seconds": ESTIMATE_FRESH_SECONDS,
            "next_action": "re_estimate",
            "hint": f"询价已过 {age} 秒（阈值 {ESTIMATE_FRESH_SECONDS} 秒），请调 re-estimate 重询价后让用户按新序号重选",
            "next_doc": _doc_for_scenario("estimate_expired"),
        }, exit_code=1)

    # 全部通过
    return ok(
        selectedSkuId=sku_id,
        fresh=True,
        age_seconds=age,
        threshold_seconds=ESTIMATE_FRESH_SECONDS,
        next_action="book_order",
        next_doc="references/delivery/step-5-book.md",
        user_reply_hint="已确认选择，请直接调 book-order 下单",
    )


def book_order():
    """高阶组合命令：一步完成下单。

    自动从 session 读取 estimatePriceRecordId + selectedSkuId，内联 TTL 预检，
    调用 runerrand_book_order MCP，成功后落盘 orderCode，返回支付信息。

    省掉 LLM 手动 state show + state get × 2 + mcp-call 的 4 次调用。
    """
    session = _load_session()
    if session is None:
        return fail("no_session", "session 不存在", hint="请先完成询价流程")

    record_id = session.get("estimatePriceRecordId")
    sku_id = session.get("selectedSkuId")

    if _is_empty(record_id):
        return fail("no_estimate", "estimatePriceRecordId 为空",
                    hint="请先调 run-estimate 询价")
    if _is_empty(sku_id):
        return fail("no_sku_selected", "selectedSkuId 为空",
                    hint="请先调 select-sku 选择方案")

    # TTL 预检
    estimate_at = session.get("estimate_at")
    now = int(time.time())
    if not isinstance(estimate_at, (int, float)) or estimate_at <= 0:
        return fail("no_estimate_at", "询价时间戳缺失",
                    next_action="re_estimate",
                    hint="请调 re-estimate 重询价后让用户按新序号重选",
                    next_doc=_doc_for_scenario("estimate_expired"))

    age = now - int(estimate_at)
    if age > ESTIMATE_FRESH_SECONDS:
        return emit({
            "status": "expired",
            "fresh": False,
            "reason": "stale",
            "age_seconds": age,
            "threshold_seconds": ESTIMATE_FRESH_SECONDS,
            "next_action": "re_estimate",
            "hint": f"询价已过 {age} 秒（阈值 {ESTIMATE_FRESH_SECONDS} 秒），请调 re-estimate 重询价后让用户按新序号重选",
            "next_doc": _doc_for_scenario("estimate_expired"),
        }, exit_code=1)

    # 调用 MCP 下单
    arguments = {
        "estimatePriceRecordId": record_id,
        "expressSkuInfos": [sku_id],
    }
    result = _MCP.invoke("runerrand_book_order", arguments)
    if not result.ok:
        return emit(result.to_error_dict(), exit_code=1)

    raw_text = result.inner_text or result.raw_body or ""
    try:
        mcp_data = json.loads(raw_text)
    except (json.JSONDecodeError, TypeError):
        return fail("parse_error", f"MCP 返回非 JSON: {raw_text[:200]}")

    if mcp_data.get("code") != 0:
        return emit(mcp_data)

    # 成功：落盘 orderCode
    data = mcp_data.get("data") or {}
    order_code = data.get("orderCode")
    pay_info = data.get("payInfo") or {}
    scan_url = pay_info.get("scanUrl") or ""
    code_url = pay_info.get("codeUrl") or ""

    if order_code:
        _ok, _reason = _check_write_guard(session, "orderCode")
        if _ok:
            _set_by_path(session, "orderCode", order_code)
            _save_session(session)

    # 取费用信息
    sku_details = session.get("skuDetails") or {}
    sku_detail = sku_details.get(sku_id) if isinstance(sku_details, dict) else {}
    total_fee = sku_detail.get("totalFee") if isinstance(sku_detail, dict) else None
    total_fee = total_fee or "-"

    sender_addr = _get_by_path(session, "sender.address.name") or ""
    receiver_addr = _get_by_path(session, "receiver.address.name") or ""

    reply_template = _tpl_payment_qr(
        order_code, sender_addr, receiver_addr, total_fee, code_url, scan_url,
    )

    payload = {
        **mcp_data,
        "orderCode": order_code,
        "scanUrl": scan_url,
        "codeUrl": code_url,
        "senderAddr": sender_addr,
        "receiverAddr": receiver_addr,
        "totalFee": total_fee,
        "next_doc": "references/delivery/step-6-payment.md",
        "hint": "reply_template 已包含完整支付卡片（含二维码 markdown），原样贴给用户即可；禁止退化成纯链接",
    }
    if reply_template:
        payload["reply_template"] = reply_template
    return emit(payload)


def state_show():
    """诊断命令：展示当前 session 快照（脱敏）。

    与 state get 的区别：一次输出全部关键字段，便于 LLM/开发者快速排查。
    手机号中段脱敏；_last_pois 等内部缓存省略。
    """
    session = _load_session()
    if session is None:
        return emit({"status": "empty", "message": "session 不存在"})

    def _mask_phone(p):
        if isinstance(p, str) and len(p) == 11:
            return p[:3] + "****" + p[-4:]
        return p

    def _g(path):
        return _get_by_path(session, path)

    estimate_at = _g("estimate_at")
    age_seconds = (
        int(time.time()) - int(estimate_at)
        if isinstance(estimate_at, (int, float)) else None
    )

    snapshot = {
        "sender": {
            "address_name": _g("sender.address.name"),
            "name": _g("sender.name"),
            "phone": _mask_phone(_g("sender.phone")),
        },
        "receiver": {
            "address_name": _g("receiver.address.name"),
            "name": _g("receiver.name"),
            "phone": _mask_phone(_g("receiver.phone")),
        },
        "estimatePriceRecordId": _g("estimatePriceRecordId"),
        "skuMap_size": len(_g("skuMap") or {}),
        "selectedSkuId": _g("selectedSkuId"),
        "orderCode": _g("orderCode"),
        "estimate_at": estimate_at,
        "estimate_age_seconds": age_seconds,
        "last_update_at": _g("last_update_at"),
        "_last_pois_cached_roles": list((_g("_last_pois") or {}).keys()),
        "current_state": _compute_current_state(session),
    }
    return emit(snapshot)


def state_dispatch(args):
    """state 子命令分发。"""
    if not args:
        print("用法: state <init|get|set|clear|reconcile|next|show> [...]", file=sys.stderr)
        return 1
    sub = args[0]
    if sub == "init":
        return state_init()
    if sub == "get":
        path = args[1] if len(args) > 1 else None
        return state_get(path)
    if sub == "set":
        if len(args) < 3:
            print("用法: state set <dot.path> <json_value>", file=sys.stderr)
            return 1
        return state_set(args[1], args[2])
    if sub == "clear":
        return state_clear()
    if sub == "reconcile":
        going_json = args[1] if len(args) > 1 else "{}"
        return state_reconcile(going_json)
    if sub == "next":
        return state_next()
    if sub == "show":
        return state_show()
    print(f"未知 state 子命令: {sub}", file=sys.stderr)
    return 1


def main():
    """CLI 入口：基于 _COMMANDS 注册表分发（Phase 3 重构）。"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd_name = sys.argv[1]
    spec = _COMMANDS.get(cmd_name)
    if spec is None:
        print(f"未知命令: {cmd_name}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)

    handler, min_args, usage = spec
    # 位置参数 = sys.argv[2:] (跳过 "python... tms_delivery.py" 和命令名)
    rest = sys.argv[2:]
    if len(rest) < min_args:
        print(f"用法: python3 scripts/tms_delivery.py {usage}", file=sys.stderr)
        sys.exit(1)

    # 执行 handler 并以其返回值作为退出码
    sys.exit(handler(rest))


# ------------------------------------------------------------
# 命令注册表
# ------------------------------------------------------------
# 每条记录：命令名 -> (handler, min_args, usage_str)
#   handler: 接收 rest(list[str]) -> int(exit code) 的函数；允许用 lambda 适配现有签名
#   min_args: 该命令必需的最少位置参数数量
#   usage_str: 用法串（不含"python3 scripts/tms_delivery.py "前缀）
#
# 设计优势：
#   1. 新增命令 = 注册表加一行，不用改 main() 分发逻辑
#   2. 用法错误提示统一格式，不再 N 份 print+sys.exit 模板
#   3. 参数校验统一（min_args），不用每个分支写 if len(sys.argv) < N
# ------------------------------------------------------------

_COMMANDS = {
    # 基础
    "preflight": (lambda r: preflight(), 0, "preflight"),
    "save-token": (lambda r: save_token(r[0]), 1, "save-token <token>"),
    "delete-token": (lambda r: delete_token(), 0, "delete-token"),
    "mcp-call": (lambda r: mcp_call(r[0], r[1] if len(r) > 1 else "{}"), 1,
                 "mcp-call <tool_name> [arguments_json]"),
    "state": (lambda r: state_dispatch(r), 0, "state <init|get|set|clear|reconcile|assert|next|show|set-batch> [...]"),
    # 决策工具
    "resolve-address": (lambda r: resolve_address(r[0], r[1], r[2] if len(r) > 2 else None), 2,
                        "resolve-address <sender|receiver> <keyword> [region]"),
    # 组合命令（v1.3.0+）
    "commit-contact": (lambda r: commit_contact(r[0], r[1], r[2]), 3,
                       "commit-contact <sender|receiver> <name> <phone>"),
    "commit-address": (lambda r: commit_address(r[0], r[1]), 2,
                       "commit-address <sender|receiver> <poi_json>"),
    "prefill-contacts": (lambda r: prefill_contacts(r[0], r[1], r[2], r[3]), 4,
                         "prefill-contacts <sender_name> <sender_phone> <receiver_name> <receiver_phone>  (任一字段空串=跳过)"),
    "run-estimate": (lambda r: run_estimate(), 0, "run-estimate"),
    "re-estimate": (lambda r: re_estimate(), 0, "re-estimate"),
    # 高阶组合命令（v1.3.2+）
    "bootstrap": (lambda r: bootstrap(), 0, "bootstrap"),
    "pick-address": (lambda r: pick_address(r[0], r[1]), 2,
                     "pick-address <sender|receiver> <序号>"),
    "select-sku": (lambda r: select_sku(r[0]), 1, "select-sku <序号>"),
    "book-order": (lambda r: book_order(), 0, "book-order"),
}


if __name__ == "__main__":
    main()
