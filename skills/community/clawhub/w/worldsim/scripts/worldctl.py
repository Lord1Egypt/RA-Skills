#!/usr/bin/env python3
"""
worldctl.py — WorldSim 批量状态管理 V2

用法:
  worldctl.py <世界名> read                ← 读取所有 .yaml 状态文件 → stdout（合并 YAML）
  worldctl.py <世界名> read --files a,b,c  ← 限读指定文件
  worldctl.py <世界名> write              ← 从 stdin 读 YAML diff → 合并写入
  worldctl.py <世界名> write --full       ← 从 stdin 读完整 YAML → 覆写
  worldctl.py <世界名> write-raw <文件key> <YAML键> [内容]
                                         ← 原始文本直写（无YAML解析）
  worldctl.py <世界名> write-raw --batch  ← 批量原始文本直写，stdin 用 ###FILE/###KEY 记录格式
                                         ⚠ 非幂等：###APPEND: 重复执行会重复追加累积字段——同一批次只执行一次·验证用 read/validate/--dry-run·禁止重放 write 命令
  worldctl.py <世界名> append-raw <文件key> <YAML键> [内容]
                                         ← 追加模式原始文本直写（列表/累积字段追加·--batch 同 write-raw）
  worldctl.py <世界名> delete <文件key> <键路径>
                                         ← 删整条 CT / pending 条目（批量流支持 ###DELETE:）
  worldctl.py <世界名> convert            ← 将 .md 状态文件转为 .yaml（按章节存 block scalar）
  worldctl.py <世界名> validate           ← 验证 YAML 格式（键表/枚举/联动检查）；格式错误 exit 1，内容警告 exit 0（非阻断）
  worldctl.py <世界名> audit             ← 校验 stdin 的 change set 草案（###FILE/###KEY 格式），不落盘
                                         （语义不变量：代价行/载体/记忆上限/轮次单调/落点一致）
  worldctl.py <世界名> grep <关键词>      ← 全仓（含所有场景 scene_state）搜索元素注册原文
  worldctl.py <世界名> scan [--live]      ← 扫描世界状态摘要（默认含历史轮转/archive·--live 仅当前）
  worldctl.py <世界名> gate dramatist|storyliner|director|actor|keeper|writer [--check]
                                         ← 六阶段闸门（--check=从 stdin 读该阶段批次/叙事跑代码化核验·不合格 exit 1）
  worldctl.py <世界名> storyline <子命令> ← 事件线结构维护（show/add/rewrite/close/clear·写 states/storylines.yaml·②编剧唯一通道）
  worldctl.py <世界名> beat <子命令>     ← 演出指针维护（show/set/deepen/advance·写 states/direction.yaml·③导演唯一通道）
  worldctl.py <世界名> reset-cycle [--asset <角色>]
                                         ← 循环世界周期重置（全员机械重置+登记+重建倒计时）
  worldctl.py <世界名> round-check       ← 轮完整性检查（⑤场记收尾：direction/world_state 三件套/场景时间线/区域一致性/引用对账）
  worldctl.py <世界名> cast-baseline      ← 场景 cast 基线查询（只读·exit 0 恒过·切场景 init_scene 后运行·scene_card「出场角色/焦外/在场」两栏照此填）
  worldctl.py <世界名> ledger [轮次]      ← 批次账本查询（只读·各段 op 索引 + ④段 MUSE/ACTION/SCHEDULE/META 原文·落盘后自动写·跨场景回退·取证面）
  worldctl.py <世界名> init-states      ← 首次启动物化缺失动态文件（幂等·模板+SEED+CHAR_state 骨架·LF·有 regions/ 自动对账）
  worldctl.py <世界名> map-sync         ← world_map 镜像层对账（regions/ 目录树 → 补缺失节点）
  worldctl.py <世界名> lint              ← 规范化检查：报告 YAML 引号/类型问题（只读，不修改）
  worldctl.py <世界名> fix               ← 规范化重写：修复引号/类型问题（snap 自动备份 + validate）
  worldctl.py <世界名> tmp-clean         ← 清理该世界 tmp/ 下过程临时文件（跨会话恢复时自动执行）

文件格式约定:
  - 所有状态文件使用 .yaml 扩展名
  - 每个顶级章节用 YAML 映射键存储，内容为 block scalar (|)
  - 结构化的表（如 conflicts）用 mapping of mappings，键为项目ID
  - 角色状态用自由键值对 + 多行 prose 值

核心优化：read = 1 次 exec 获取所有状态；write = 1 次 exec 更新所有变更。
"""
import sys, os, yaml, re, shutil, argparse, difflib
from datetime import datetime, timezone
from pathlib import Path

# I/O 纪律（硬性）：本脚本读写一律 UTF-8——Windows 缺省 locale（GBK）读中文 yaml 必炸、
# emoji（🔴等）写 GBK stdout 必炸；所有 open/read_text/write_text 已显式 encoding，此处兜底 stdout/stderr
for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 路径推导单一事实源（skill 根 / worlds 根 / 世界目录解析 / 破坏性删除安全网）——见 _paths.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import SKILL_DIR, assert_no_links, require_world_marker, resolve_world, safe_rmtree, snapshot_or_abort
CHAR_STATE_PREFIX = "CHAR_"
CHAR_STATE_SUFFIX = "_state.yaml"

# 节拍表（v0.11 旧结构·conflicts.yaml 顶层·迁移后由 storylines.yaml 取代）
BEAT_TOP_KEY = "节拍表"
BEAT_ENUM = ("铺垫", "接触", "升级", "顶点", "余波")

# 三幕十五拍节拍清单（② 故事弧线.节点落位 的键域·权威=references/beat_structure.md §一）
# 键域随当前幕而变：节点落位的键必须落在当前幕的清单内（validate 软警·不拦截）。
ARC_BEATS = {
    "第一幕": ("开场画面", "主题陈述", "铺垫", "催化剂", "挣扎犹豫"),
    "第二幕": ("进入第二幕", "B故事", "游戏时间", "中点", "反派逼近", "失去一切", "灵魂暗夜"),
    "第三幕": ("进入第三幕", "高潮", "终场画面"),
}

# 六阶段单管道：结构蓝图（storylines·②编剧）与现场控制（direction·③导演）分权
STORYLINES_FILE = "storylines.yaml"
DIRECTION_FILE = "direction.yaml"
STORYLINE_TOP_KEY = "事件线"
STORYLINE_ID_PREFIX = "SL-"
STAGES = ("戏剧家", "编剧", "导演", "角色", "场记", "作家")
# 批次类五阶段（作家=叙事闸门·gate writer --check 于叙事输出前独立核验·不参与批次段级闸门）
BATCH_GATE_STAGES = ("戏剧家", "编剧", "导演", "角色", "场记")
# Single Writer per State（design-v2 §4 写入矩阵）：阶段 → 允许写入的文件 key（"CHAR_"=前缀匹配）
STAGE_WRITE_MAP = {
    "戏剧家": {"conflicts"},
    "编剧": {"storylines"},
    "导演": {"direction"},
    "角色": {"CHAR_"},
    "场记": {"scene_state", "world_state", "world_map", "pending_actions", "foreshadow"},
    "作家": set(),
}
# conflicts 已迁移字段：写入即拦截（防旧流程残留写回）
CT_LEGACY_KEYS = ("当前节拍", "下一个节拍(推荐)", "角色反应", "节拍表")
DIRECTION_KEYS = {"当前事件线", "当前拍", "当前戏剧问题", "当前张力", "演出状态", "阶段",
                  "承接判断", "节拍决策", "guidance", "转场", "escalation_flags", "时间窗口", "调度单"}
DECISION_SUBFIELDS = ("核心诉求", "当前计划", "当前行动", "行动驱动", "行动对象", "行动窗口", "失败后续", "未完成意图")
DECISION_RUNTIME_FIELDS = ("当前行动", "行动驱动", "行动对象", "行动窗口", "失败后续", "未完成意图")
# 有 ACTION 才查的行动前置物化字段（字符串型·空值/[占位]均视为未物化——位置无落点/核心状态不明/
# 妆扮服饰未建基线/压力防御缺档位时行动决策无依据·见 keys.md 骨架物化规则/phase_actor 先决状态转换）
ACTION_SKELETON_STR_FIELDS = ("位置", "核心状态", "妆扮", "压力水平", "防御有效性")
# 服饰为列表型（模板初始 []·物化后应按 CHAR_.md 外在特征填充基线）——空列表视为未物化·单独判定
STORYLINES_TOP_KEYS = {"故事弧线", STORYLINE_TOP_KEY}
PERF_STATES = ("上升", "持续", "转折", "收束", "停滞")
# ── 产物体量失忆探针阈值（内部常量·只存于本处）──
# 探针=以产物体量反推「是否走了完整流程」（体量不足≈流程未走）。阈值一律不得出现在面向 LLM 的
# 文本里（报错文案/reference/模板）——否则 LLM 会以凑字数替代走流程·探针失效。
_MUSE_MIN_CHARS = 200        # ④角色 MUSE 心声下限（三段结构＋权重判定）
_WRITER_MIN_TOKENS = 600     # ⑥作家叙事下限（失忆探针·最低产出）
_DIRECTOR_MIN_CHARS = 120    # ③导演 承接判断 下限（回判评估的最低留痕）
# 施压方向（CT 子字段 CT-{XX}.施压方向·①戏剧家每轮随推进池逐条标注——瞄准声明·非结算字段非行动脚本；旧版顶层键已废弃）
PRESSURE_KEY = "施压方向"
PRESSURE_ENUM = ("死局两难", "防御踩爆", "关系爆破", "不可逆代价", "维持")
PRESSURE_HOLD = "维持"
_PRESSURE_RE = re.compile(r"^\s*([^—]+?)\s*(?:—+\s*(.*))?\s*$")

# escalation_flags 旗标在场判定（读值·兼容历史写法）：键存在且值非空、非「无」类占位才算在场
# （历史数据常见 `停滞: 无` 表示无旗标——按键存在判定会把无旗标误判为在场·扭曲加压义务）
_FLAG_OFF_VALUES = {"", "无", "—", "-", "none", "false", "False", "0"}


def _flag_active(v) -> bool:
    s = str(v if v is not None else "").strip()
    return bool(s) and s not in _FLAG_OFF_VALUES


# 人际动态档位枚举（keys.md 唯一值域·validate 与 write-raw 写时软警共用）
RELATION_TIERS = {"稳固", "信任", "中立", "防备", "破裂", "待重建"}


def _split_pressure(value):
    """Split enum——explanation pressure values into (enum, explanation)."""
    match = _PRESSURE_RE.match(str(value or ""))
    if not match:
        return "", ""
    return (match.group(1) or "").strip(), (match.group(2) or "").strip()


# 连续行动轨迹增长告警线（窗口滚动裁剪后·兜底软告警）
ACTION_TRACK_LIMIT = 5000
# 自主性档位阶梯（loop_machinery §5.3：脚本→漂移→觉醒→变质·每次极端冲击只升一级·不跨级）
# 值=序级，用于升档/降档/跨级判定（替代逐对硬编码路径——原写法漏判 脚本→漂移、误放 脚本→觉醒）
AUTO_ORDER = {"脚本": 0, "漂移": 1, "觉醒": 2, "变质": 3}
# 变质判定门槛（升档唯一入口·loop_machinery §5.3 / keys.md §自主性）
AUTO_PROMOTE_PRESSURE = "临界"
AUTO_PROMOTE_DEFENSE = "已彻底崩解"


def _is_template_value(value) -> bool:
    """空值或状态模板占位（[字段定义]）都不是可供角色决策的真实值。"""
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return not stripped or bool(re.fullmatch(r"\s*\[[^\]]+\]\s*", value))


def _decision_template_fields(data) -> list[str]:
    """返回尚未实体化的 decision 子字段；缺映射也视为八项均缺。"""
    decision = data.get("decision") if isinstance(data, dict) else None
    if not isinstance(decision, dict):
        return list(DECISION_SUBFIELDS)
    return [field for field in DECISION_SUBFIELDS
            if field not in decision or _is_template_value(decision.get(field))]

# 顶点约束（Vertex Constraint——编剧声明的这一场关系必须被推至的临界验收结构）
# 结构：关系主体(≥2·不区分玩家/NPC·顶点单位=关系) / 核心张力(未决问题·点名赌注所在) /
#       变化维度(枚举·创作意图声明——指导张力走向与演出侧重·非验收映射) /
#       非玩家爆破(≥1 外部角色或事件·主体静止时的加压力量·防死锁) /
#       基准快照(脚本自动记录·仅关系主体·实质状态字段集·私有落档 states/.climax_baseline_{SL}.yaml——
#         不进 storylines/任何读取面·LLM 不填不读)
# 验收：关系主体的实质状态字段发生任何真实变化即出线（任一来源——主体/对手/外部爆破/世界事件）。
#   【核心设计】验收对比面 = 下面的字段集·但该字段集不写入任何规则文本/审计消息——
#   让 LLM 公开知道"验收哪些字段"= 给它做题靶子（信念演化/防御重构/自主性正是最高级改变·更须防泄露）；
#   字段集的唯一权威在本文件（脚本层）：LLM 只负责演出·脚本默默比对。
DIM_ENUM = ("关系", "认知", "决策", "资源")
SUBSTANTIVE_FIELDS = ("人际动态", "记忆锚点", "信念演化", "decision",
                      "防御有效性", "防御形态", "崩溃表现", "自主性", "核心状态")
CLIMAX_LIST_FIELDS = ("记忆锚点", "信念演化")   # 列表字段按条数比较（基准快照用）

def _climax_baseline_fp(world_dir: Path, sl_id: str) -> Path:
    """基准快照私有落档路径（下划线前缀=脚本私有·不进入 discover_files/read/storyline show 等任何读取面）。"""
    return world_dir / "states" / f".climax_baseline_{sl_id}.yaml"

def _load_climax_baseline(world_dir: Path, sl_id: str) -> dict:
    fp = _climax_baseline_fp(world_dir, sl_id)
    if not fp.exists():
        return {}
    try:
        d = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    return d if isinstance(d, dict) else {}
CLIMAX_BASELINE_KEY = "基准快照"
CLIMAX_CONSTRAINT_KEY = "顶点约束"

def _read_stdin_utf8() -> str:
    """stdin 原始字节显式 UTF-8（与 --batch 同款安全通道）——Windows cmd /c 重定向 UTF-8 临时文件时，
    sys.stdin 按 locale（GBK）解码会损坏中文；一律经系统 stdin 字节流显式 UTF-8 解码。"""
    return sys.stdin.buffer.read().decode("utf-8")


def _elems_equal(a, b) -> bool:
    """结构化累积元素的「重复」判据（通用兜底）：规范化后全元素相等。

    旧判据 = 轮次 + 内容。对没有「内容」键的字段（信念演化=轮次/时间/触发事件/旧→新；
    偏离登记=轮次/时间/动作/档位）两侧恒取空串、恒等 → 判据退化成「同一轮次只准 1 条」
    （实测：一轮写 2 条信念演化 / 2 条偏离登记，各只落 1 条，另一条被 [SKIP] 吞掉）。
    全元素相等既修掉误杀，也照样拦住真正的批次重放（重放产出完全相同的条目）。
    """
    if type(a) is not type(b):
        return False
    if not isinstance(a, dict):
        return str(a) == str(b)
    try:
        return (yaml.safe_dump(a, allow_unicode=True, sort_keys=True, default_flow_style=True)
                == yaml.safe_dump(b, allow_unicode=True, sort_keys=True, default_flow_style=True))
    except Exception:
        return str(a) == str(b)


def _coerce_str_list(content) -> list:
    """把「字符串列表」字段的输入统一规整为 list[str]（物理锚点/已知地点·类型统一 + 散文兼容）。

    接受两种输入：① YAML 列表文本（`- 条目` / `[a, b]` / `[]`）② 多行散文（逐行一条，
    行首 `-`/`·`/`*`/`•` 与包裹引号一律剥净）。散文按行切分，不做 YAML 折叠——
    多行纯文本经 yaml.safe_load 会被折成一个字符串（"a\\nb" → "a b"），旧路径正因此把列表写成字符串。
    """
    txt = _strip_wrapping_quotes(str(content or "")).strip()
    if not txt or txt in ("[]", "{}"):
        return []
    if txt.startswith("[") or re.search(r"^\s*[-•*]\s+", txt, re.M):
        try:
            parsed = yaml.safe_load(txt)
        except Exception:
            parsed = None
        if isinstance(parsed, list):
            return [str(it).strip() for it in parsed if str(it).strip()]
    out = []
    for ln in txt.split("\n"):
        ln = re.sub(r"^\s*[-•*·]\s*", "", ln).strip()
        ln = _strip_wrapping_quotes(ln).strip()
        if ln:
            out.append(ln)
    return out


# ── 结构化累积字段 append 形态校验（write_one 与 --dry-run 共用·预演与实跑同源）──
# 结构化累积字段（append 时追加为 yaml 列表元素——轮次/时间/线索 开头·或 已知地点「- 地点名」·或 道具「- ID:」）
STRUCTURED_APPEND_FIELDS = {"记忆锚点", "信念演化", "偏离登记", "已知地点", "伏笔", "连续行动轨迹", "场景时间线", "道具", "物理锚点"}
# 字符串列表字段（元素=纯字符串·非映射）：输入侧散文/列表两种形态一律由脚本归一为 list[str]
STR_LIST_COERCE_FIELDS = {"已知地点", "物理锚点"}


def _append_shape_check(file_key: str, key_path: list, content: str, append: bool):
    """结构化累积字段 append 的形态/类型纯校验（不落盘）。

    返回 (错误文案|None, is_structured_field, is_list_item_content)——后两者供 write_one 后续
    分支复用（覆盖路径 2935/2943 也依赖它们），故由本函数一并算出，保证与校验口径同源。
    抽出的动机：--dry-run 原先只跑 audit 层、不模拟 write_one 的 op 级拒绝，导致
    「预演 exit 0 · 实跑 exit 1」的假阳性（实测：场景时间线 自由文本 append）。
    """
    leaf = key_path[-1]
    is_structured_field = ((file_key.startswith(CHAR_STATE_PREFIX) or file_key in ("foreshadow", "scene_state"))
                           and leaf in STRUCTURED_APPEND_FIELDS)
    if leaf in STR_LIST_COERCE_FIELDS:
        is_list_item_content = bool(re.match(r"^\s*-\s+", content))
    else:
        is_list_item_content = bool(re.match(r"^\s*-\s*(?:轮次|时间|线索|ID)[:：]", content))
    if not (append and is_structured_field):
        return None, is_structured_field, is_list_item_content
    _path = f"{file_key}.{'.'.join(key_path)}"
    if not is_list_item_content:
        return (f"{_path} 结构化字段追加需列表元素格式（- 轮次:…/- 时间:…/- ID:…/地点名）"
                f"——旧字符串格式（· 连接/表格行）不再接受·拒绝写入（防把结构化列表替换成字符串）",
                is_structured_field, is_list_item_content)
    try:
        _new_items = yaml.safe_load(content)
    except Exception:
        return f"{_path} 结构化追加内容不是合法 YAML 列表，拒绝写入", is_structured_field, is_list_item_content
    if not isinstance(_new_items, list):
        return (f"{_path} 结构化追加内容必须是 YAML 列表（- 轮次: ... / - 地点名）",
                is_structured_field, is_list_item_content)
    return None, is_structured_field, is_list_item_content


def _parse_single_line_list(content) -> list | None:
    """单行列表文本 → list[str]；不是单行标量列表则返回 None（含空列表 `[]` 返回 []）。

    接受 `[SL-01]` / `[SL-01, SL-02]` / `- SL-01` 三种单行形态。元素限定为标量：
    含映射或嵌套列表（`- 轮次: 1` 这类结构化元素）一律返回 None——那是结构化通道的活，
    混进来会把 dict 字符串化。调用方须用 `is not None` 判定（空列表为合法结果）。
    """
    t = str(content or "").strip()
    if "\n" in t or not (re.match(r"^\[.*\]$", t) or re.match(r"^-\s+\S", t)):
        return None
    try:
        items = yaml.safe_load(t)
    except Exception:
        return None
    if not isinstance(items, list) or any(isinstance(it, (dict, list)) for it in items):
        return None
    return [str(it).strip() for it in items if str(it).strip()]


def _read_input_utf8(input_file: str | None) -> str:
    """批次文本读取统一入口：--file 给定时读 UTF-8 文件（utf-8-sig·兼容 BOM），否则走 stdin。
    PowerShell 等无 heredoc 环境的编码安全通道——中文批次先落 UTF-8 临时文件再 --file 引用，
    管道直传会经 locale 重编码损坏中文（实测 heredoc/parser 双失败后被迫绕通道）。"""
    if input_file:
        p = Path(input_file)
        if not p.is_file():
            print(f"[ERR] --file 不存在: {p}", file=sys.stderr)
            sys.exit(1)
        try:
            return p.read_bytes().decode("utf-8-sig")
        except UnicodeDecodeError as e:
            print(f"[ERR] --file 不是合法 UTF-8: {p} ({e})——批次文本必须显式 UTF-8 落盘", file=sys.stderr)
            sys.exit(1)
    return sys.stdin.buffer.read().decode("utf-8")


# ── 文件发现 ──────────────────────────────────────────────────────
def get_world_dir(world: str) -> Path:
    """世界目录解析统一走 _paths.resolve_world：
    名称校验（允许中文）→ 存在性 → 链接拦截 → realpath 越界校验。
    states/scenes 树内嵌套链接会让下游 glob/写 YAML/场景定位写穿到世界外——打开世界即整体校验。"""
    wd = resolve_world(world)
    assert_no_links(wd / "states")
    assert_no_links(wd / "scenes")
    return wd

def get_scene_dir(world_dir: Path) -> Path | None:
    """从 world_state.yaml 顶层「焦点场景」（唯一权威源）定位当前场景目录。

    兼容旧键：优先读顶层 焦点场景；找不到时回退 地点.焦点场景 / 地点.当前焦点场景。
    """
    ws_fp = world_dir / "states" / "world_state.yaml"
    if not ws_fp.exists():
        return None
    try:
        ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(ws, dict):
        return None
    scene_id = str(ws.get("焦点场景", "") or "").strip()
    if not scene_id:
        loc = ws.get("地点") or {}
        scene_id = str(loc.get("焦点场景", loc.get("当前焦点场景", "")) or "").strip()
    if not scene_id:
        # 旧格式兼容（ol 型：无 world_state.yaml / 无焦点场景）→ 回退 .active
        active_file = world_dir / ".active"
        if active_file.exists():
            scene_id = active_file.read_text(encoding="utf-8").strip()
    if not scene_id:
        return None
    scenes_dir = world_dir / "scenes"
    if not scenes_dir.is_dir():
        return None
    for d in scenes_dir.iterdir():
        if d.is_dir() and d.name.startswith(scene_id):
            return d
    return None

def discover_files(world_dir: Path, scene_dir: Path | None) -> dict[str, Path]:
    files = {}
    # 固定文件
    for fname in ["world_state.yaml", "conflicts.yaml", "world_map.yaml", STORYLINES_FILE, DIRECTION_FILE]:
        fp = world_dir / "states" / fname
        if fp.exists(): files[fp.stem] = fp
    # 角色状态
    for fp in world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}"):
        files[fp.stem] = fp
    # 场景状态
    if scene_dir:
        ssp = scene_dir / "scene_state.yaml"
        if ssp.exists(): files["scene_state"] = ssp
    # 焦外（场景级·与 scene_state 同处）
    if scene_dir:
        ofp = scene_dir / "pending_actions.yaml"
        if ofp.exists(): files["pending_actions"] = ofp
    # 伏笔登记（可选·触发式）
    ffp = world_dir / "states" / "foreshadow.yaml"
    if ffp.exists(): files["foreshadow"] = ffp
    return files

# ── CHAR key 命名归一化 ──────────────────────────────────────────
def _normalize_file_key(key: str) -> str:
    """文件 key 归一化（对齐 write_protocol「FILE key 注册表·兼容写法自动剥离」承诺）：
    剥 .yaml/.yml 后缀、剥 states/ 或任意路径前缀（含反斜杠）——使
    `world_state.yaml` / `scenes/S01-xx/pending_actions.yaml` / `scenes/S01-xx/scene_state.yaml` 等写法
    均归一到注册表 stem（world_state/pending_actions/scene_state…）。"""
    k = (key or "").strip().replace("\\", "/")
    if k.endswith(".yaml"):
        k = k[:-5]
    elif k.endswith(".yml"):
        k = k[:-4]
    k = k.split("/")[-1]
    return k


def _char_target_name(key: str) -> str:
    """从 CHAR_ 文件 key 提取角色名（去 CHAR_ 前缀与 _state 后缀）——简写容错的比较基准。"""
    k = _normalize_file_key(key)
    if k.startswith(CHAR_STATE_PREFIX):
        k = k[len(CHAR_STATE_PREFIX):]
    if k.endswith("_state"):
        k = k[:-len("_state")]
    return k.strip()


def _known_char_names(world_dir: Path, existing: dict) -> list[str]:
    """已存在的角色状态名（只取 discover_files 已注册的 CHAR_state 文件）。"""
    return list(dict.fromkeys(
        stem[len(CHAR_STATE_PREFIX):-len("_state")]
        for stem in existing
        if stem.startswith(CHAR_STATE_PREFIX) and stem.endswith("_state")
    ))


def _char_fuzzy_hits(target: str, known: list[str]) -> list[str]:
    """已知角色名中与 target 包含/分词匹配的候选（双向包含·或 ≥3 字符 token 相等）。"""
    nt = _norm_char_key(target)
    if not nt:
        return []
    out = []
    for name in known:
        nn = _norm_char_key(name)
        if nn and (nt == nn or nt in nn or nn in nt):
            out.append(name)
    return list(dict.fromkeys(out))


def _canonical_role_label(label: str, world_dir: Path, existing: dict) -> str:
    """把行动卡/META 中的角色标签归一到已存在的角色全名；多义或未知则保留原标签交给闸门报告。"""
    raw = str(label or "").strip().replace("_", " ")
    if not raw:
        return raw
    known = _known_char_names(world_dir, existing)
    exact = [name for name in known if _norm_char_key(name) == _norm_char_key(raw)]
    if len(exact) == 1:
        return exact[0]
    fuzzy = _char_fuzzy_hits(raw, known)
    return fuzzy[0] if len(fuzzy) == 1 else raw


def _char_refuse_message(key: str, target: str, known: list[str]) -> str:
    """未命中时的拒绝信息：给出已存在的可能匹配 CHAR_ key（多义/疑似拼写错误分别列候选）。"""
    hits = _char_fuzzy_hits(target, known)
    if len(hits) > 1:
        cands = " / ".join(f"CHAR_{h}_state" for h in hits[:6])
        reason = f"匹配到多个角色（{len(hits)} 个）·无法判定落点"
    else:
        near = hits or difflib.get_close_matches(target, known, n=3, cutoff=0.6)
        cands = " / ".join(f"CHAR_{h}_state" for h in near) if near else "无"
        reason = "无任何已知角色与之匹配" if not near else "存在可能匹配·但未按猜测自动落点"
    return (f"[ERR] 未知角色状态 key '{key}'——禁止新建（防同一角色产生两份状态文件·{reason}）\n"
            f"      可能匹配: {cands}\n"
            f"      确为新建角色时：先建档 characters/CHAR_<全名>.md，再用全名 `###FILE: CHAR_<全名>_state` 写入")


def resolve_char_file(existing: dict, key: str, world_dir: Path):
    """解析 CHAR_* 文件 key：真实文件或既有空格/下划线变体可映射，其余一律拒绝新建。
    未命中时返回 (None, 含候选 CHAR_* key 的错误信息)，由调用方阻止写入。"""
    key = _normalize_file_key(key)
    if key in existing:
        return existing[key], None
    if key.startswith(CHAR_STATE_PREFIX):
        variants = []
        if key.endswith("_state"):
            stem = key[len(CHAR_STATE_PREFIX):-len("_state")]  # 仅角色名部分做空格/下划线互换
            variants = [CHAR_STATE_PREFIX + stem.replace(" ", "_") + "_state",
                        CHAR_STATE_PREFIX + stem.replace("_", " ") + "_state"]
        else:
            variants.append(key + "_state")  # 缺失 _state 后缀
        for v in variants:
            if v in existing:
                return existing[v], f"[WARN] key '{key}' 与已有文件 '{existing[v].name}' 命名不一致(空格/下划线/_state)，已映射到已有文件，避免产生重复"
        # 未命中真实角色状态文件：只返回候选，不自动猜测落点；候选必须由调用方改成真实 key 后重提。
        target = _char_target_name(key)
        known = _known_char_names(world_dir, existing)
        return None, _char_refuse_message(key, target, known)
    return None, None

def pending_actions_path(scene_dir: Path | None, create: bool = True) -> Path | None:
    """场景级 pending_actions.yaml 路径——缺失时按模板建（对齐 init_scene）。create=False 用于 --dry-run（只解析不落盘）。"""
    if scene_dir is None:
        return None
    ofp = scene_dir / "pending_actions.yaml"
    if not ofp.exists():
        if not create:
            return ofp
        try:
            ofp.write_text("已完成: {}\n活跃中: {}\n", encoding="utf-8", newline="")
        except OSError as e:
            print(f"[ERR] 创建 pending_actions.yaml 失败（{e}）", file=sys.stderr)
            return None
    return ofp

# ── 深层合并 ──────────────────────────────────────────────────────
def deep_merge(base: dict, delta: dict) -> dict:
    for k, v in delta.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base

def write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)


# ── 批次账本（各段 op 索引 + ④段原文·私有取证面）──────────────────
# 定位：每段落盘后的取证面。④段承载批次级元数据行（###MUSE/###ACTION/###SCHEDULE/###META）原文——
#   这些行不产生状态写入 ops，只存在于当轮上下文（写盘后即随会话丢失），而行动卡原文是 ⑥作家
#   「事不得增减」的锚点、代价/强度是 W2/audit 的判定对象，丢失则事后不可核验。
#   非④段承载 op 索引（file.key + APPEND/DELETE/顶回标记）——回答「本批做了/没做哪些 op」。
# 落点：scenes/{段所属场景}/.ledger_r{轮次}.{阶段}.{时间戳}.yaml——点前缀=不进 discover_files/read/
#   任何 LLM 加载面（与 states/.climax_baseline_*.yaml 同约定）；同轮重驱按时间戳生成
#   第二份不覆盖（与 narrative.r{N}.{ts}.md 同约定）。取证入口=`ledger` 只读子命令。
def _split_role_line(line: str) -> tuple[str, str]:
    """拆 `{角色}: {原文}` 行为 (角色, 原文)；无冒号时角色空（键名由调用方补序号）。"""
    m = re.match(r"^\s*([^:：]+)[:：]\s*(.*)$", str(line or ""))
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", str(line or "").strip()


def _ledger_round(world_dir: Path, ctx: dict) -> str:
    """账本轮次 = 本轮实际轮次。取序（作者明写优先·不做时点推断）：
      ① 批次 ###SCHEDULE 声明的轮次（④必写项·格式「轮次N·…」·最可靠）
      ② 批次 CHAR_state `连续行动轨迹` 元素声明的 `轮次`（④·与记忆锚点/轨迹反查键同源）
      ③ 本批写 world_state.轮次 → 取所写新值（⑤场记批·落盘后盘上已是本轮值）
      ④ 以上皆无 → 按批次类型定：跨场景轮入场帧批（META「同轮续批」·轮次已由旧场景收尾批推进）
         与无 ###STAGE 维护/恢复批 → 盘上 world_state.轮次 原值；其余舞台批次（①③跑在⑤之前·
         盘上仍是上一轮值）→ +1。"""
    for line in ctx.get("schedule") or []:
        m = re.search(r"(?:轮次|第)\s*(\d+)\s*轮?", str(line))
        if m:
            return m.group(1)
    rounds = []
    for kind, file_key, key_path, content, _append in ctx.get("ops") or []:
        if kind != "write" or not str(key_path).endswith("连续行动轨迹"):
            continue
        _fk = _normalize_file_key(file_key)
        if not (_fk.startswith(CHAR_STATE_PREFIX) and _fk.endswith("_state")):
            continue
        try:
            blocks = yaml.safe_load(content) or []
        except Exception:
            continue
        for b in blocks if isinstance(blocks, list) else []:
            if isinstance(b, dict):
                v = str(b.get("轮次", "") or "").strip()
                if re.fullmatch(r"\d+", v):
                    rounds.append(int(v))
    if rounds:
        return str(max(rounds))
    for kind, file_key, key_path, content, _append in ctx.get("ops") or []:
        if kind == "write" and _normalize_file_key(file_key) == "world_state" \
                and str(key_path).strip() == "轮次":
            v = str(content).strip().strip("'\"")
            if re.fullmatch(r"\d+", v):
                return v
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
        cur = str(ws.get("轮次", "") if isinstance(ws, dict) else "").strip().strip("'\"")
    except Exception:
        cur = ""
    _meta_txt = " ".join(str(x) for x in (ctx.get("meta") or []))
    if str(ctx.get("stage", "") or "").strip() and "同轮续批" not in _meta_txt \
            and re.fullmatch(r"\d+", cur):
        return str(int(cur) + 1)
    return cur


def write_round_ledger(world_dir: Path, ctx: dict) -> Path | None:
    """段批次落盘成功后写账本（脚本自动·LLM 零动作·零新增标记）。
    ④段存 MUSE/ACTION/SCHEDULE/META 原文；各段均存 阶段/META/op 索引（file.key + APPEND/DELETE/顶回标记）。
    无任何内容 → 不建文件。返回落盘路径，未写返回 None。"""
    muse = ctx.get("muse") or []
    action = ctx.get("action") or []
    meta = [str(x) for x in (ctx.get("meta") or [])]
    schedule = [str(x) for x in (ctx.get("schedule") or [])]
    blocked = set(ctx.get("blocked") or ())
    op_index = []
    for _idx, (_kind, _fk, _kp, _content, _append) in enumerate(ctx.get("ops") or []):
        _mark = "（DELETE）" if _kind == "delete" else ("（APPEND）" if _append else "")
        if _idx in blocked:
            _mark += "（顶回）"
        op_index.append(f"{_fk}.{_kp}{_mark}")
    if not (muse or action or meta or schedule or op_index):
        return None
    scene_dir = get_scene_dir(world_dir)
    if scene_dir is None or not scene_dir.is_dir():
        return None
    stage = str(ctx.get("stage", "") or "").strip() or "维护"
    data: dict = {"轮次": _ledger_round(world_dir, ctx), "场景": scene_dir.name, "阶段": stage}
    for key, src in (("MUSE", muse), ("ACTION", action)):
        # 列表存储（保序＋允许同角色重复）——同角色同窗口多环＝各环原文全存·按序；
        # 曾用 {角色: 文本} 字典，同角色多环互相覆盖、只剩末环（实测 r9 丢失环1）。
        items = []
        for i, line in enumerate(src, 1):
            role, text = _split_role_line(line)
            items.append({role or f"（第{i}行）": text})
        if items:
            data[key] = items
    for key, src in (("SCHEDULE", schedule), ("META", meta)):
        if src:
            data[key] = src
    if op_index:
        data["op索引"] = op_index
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    fp = scene_dir / f".ledger_r{data['轮次'] or '未知'}.{stage}.{ts}.yaml"
    try:
        write_yaml(fp, data)
    except Exception as e:
        print(f"[WARN] 账本写入失败（不影响本段落盘结果）: {e}", file=sys.stderr)
        return None
    print(f"[LEDGER] 账本: {scene_dir.name}/{fp.name}（阶段 {stage} · op {len(op_index)} · MUSE {len(muse)} · ACTION {len(action)}）", file=sys.stderr)
    return fp

# ── CONVERT 核心 ──────────────────────────────────────────────────
def markdown_sections_to_yaml(text: str) -> dict:
    """
    将 markdown 文本按 ## 章节拆分，每个章节内容作为 block scalar。
    顶级 # 标题忽略或作为文件元。
    返回 {section_title: content_string} 的 dict。
    """
    lines = text.split("\n")
    sections = {}
    current_title = None
    current_lines = []

    def flush():
        if current_title:
            content = "\n".join(current_lines).strip()
            if content:
                # 清理标题序号（"1. ", "2. "）
                clean_title = re.sub(r"^\d+\.\s*", "", current_title).strip()
                # 清理多余的标记
                clean_title = clean_title.replace("**", "").strip()
                sections[clean_title] = content

    for line in lines:
        if line.startswith("## "):
            flush()
            current_title = line[3:].strip()
            current_lines = []
        elif line.startswith("# ") and not line.startswith("##"):
            continue  # 忽略一级标题
        else:
            current_lines.append(line)
    flush()
    return sections

def sections_to_yaml(text: str) -> dict:
    """按 ## 拆分并转为 YAML 友好结构"""
    sections = markdown_sections_to_yaml(text)
    result = {}
    for title, content in sections.items():
        # 尝试按二级子弹拆分
        result[title] = content
    return result

def convert_md_to_yaml(text: str, source_name: str) -> dict:
    """通用 .md → YAML 转换"""
    # 检查是否是表格格式
    if "|" in text and "---" in text:
        # 可能是冲突表或其他表格式 → 尝试结构化解
        return convert_table_format(text, source_name)
    # 默认：按章节 block scalar
    return sections_to_yaml(text)

def convert_table_format(text: str, source_name: str) -> dict:
    """
    处理表格格式 md（如 conflicts.md）。
    产出：{CT-ID: {field: value, ...}} 结构
    """
    result = {}
    # 按 ## CT- 拆分
    ct_blocks = re.split(r"^## (CT-\d+[^\n]*)", text, flags=re.MULTILINE)

    # 跳过标题行，从 CT 块开始
    i = 1 if ct_blocks and not ct_blocks[0].startswith("CT-") else 0
    while i + 1 < len(ct_blocks):
        ct_title = ct_blocks[i].strip().replace("：", ":").split("：")[0].split(" ")[0]  # "CT-01"
        ct_body = ct_blocks[i + 1]

        ct_data = {}
        # 在 block 内找表格行
        in_table = False
        current_field = None
        current_value = []

        for line in ct_body.split("\n"):
            if line.strip().startswith("|") and line.strip().endswith("|"):
                if "---" in line:
                    in_table = True
                    continue
                if in_table:
                    cells = [c.strip() for c in line.strip("|").split("|")]
                    if len(cells) >= 2:
                        field = cells[0].replace("**", "").strip()
                        value = cells[1].strip()
                        if field:
                            ct_data[field] = value
            else:
                in_table = False
                # 非表格行可能包含额外的内容
                if line.strip() and "**" in line and "：" in line:
                    parts = line.split("：", 1)
                    ct_data["_" + parts[0].replace("**", "").strip()[:20]] = parts[1].strip()

        if ct_data:
            result[ct_title] = ct_data
        else:
            # 退化为 block scalar
            result[ct_title] = ct_body.strip()

        i += 2

    # 如果没有解析出任何 CT
    if not result:
        return sections_to_yaml(text)
    return result

def convert_world_state(text: str) -> dict:
    """world_state.md 特殊处理"""
    sections = markdown_sections_to_yaml(text)
    result = {}
    for title, content in sections.items():
        # 尝试解析子弹列表
        items = {}
        for line in content.split("\n"):
            m = re.match(r"^- (\*\*)?(.+?)(\*\*)?:\s*(.*)", line)
            if m:
                key = m.group(2).strip()
                val = m.group(4).strip()
                items[key] = val
        if items:
            result[title] = items
        else:
            result[title] = content
    return result

def convert_char_state(text: str) -> dict:
    """CHAR_state.md — key=value 格式"""
    result = {}
    for line in text.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            result[k.strip()] = v.strip()
        elif line.strip() and not line.startswith("#"):
            # 可能是多行值的续行
            pass
    # 如果 key=value 解析失败，fallback 到 sections
    if not result:
        return sections_to_yaml(text)
    return result

def cmd_convert(world_dir: Path):
    """批量转换 .md → .yaml"""
    scene_dir = get_scene_dir(world_dir)

    # 定义转换映射：{md_path: yaml_path}
    md_to_yaml = {
        world_dir / "world_state.md":      world_dir / "states" / "world_state.yaml",
        world_dir / "conflicts.md":        world_dir / "states" / "conflicts.yaml",
    }
    # 角色状态
    for fp in world_dir.glob(f"{CHAR_STATE_PREFIX}*_state.md"):
        yaml_name = fp.stem + ".yaml"
        md_to_yaml[fp] = world_dir / "states" / yaml_name

    # 场景状态
    if scene_dir:
        ssmd = scene_dir / "scene_state.md"
        ssym = scene_dir / "scene_state.yaml"
        if ssmd.exists():
            md_to_yaml[ssmd] = ssym

    # 焦外（legacy convert：旧格式单一 off_focus/pending_actions.md → states/pending_actions.yaml）
    # 注：现行约定 pending_actions 为场景级（scenes/{焦点场景}/·由 init_scene/create 建）；此映射仅服务旧 .md 世界转换的过渡产物。
    ofmd = world_dir / "off_focus" / "pending_actions.md"
    ofym = world_dir / "states" / "pending_actions.yaml"
    if ofmd.exists():
        md_to_yaml[ofmd] = ofym

    # 处理函数映射：(函数, 额外参数)
    handlers = {
        "world_state": (convert_world_state, False),
    }

    for src, dst in md_to_yaml.items():
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        name = src.stem

        if name == "conflicts":
            data = convert_table_format(text, name)
        elif "CHAR_" in name and name.endswith("_state"):
            data = convert_char_state(text)
        elif name in handlers:
            data = handlers[name][0](text)
        else:
            data = sections_to_yaml(text)

        # 备份 .md
        bak = src.with_suffix(".md.bak")
        if not bak.exists():
            shutil.copy2(src, bak)

        write_yaml(dst, data)
        print(f"[OK] {src.name} → {dst.name}  ({len(text)}b → {len(str(data))} keys)")

# ── READ ──────────────────────────────────────────────────────────
def cmd_read(world_dir: Path, files_filter: list[str] | None = None):
    scene_dir = get_scene_dir(world_dir)
    files = discover_files(world_dir, scene_dir)
    results = {}
    for key, fp in sorted(files.items()):
        if files_filter and key not in files_filter:
            continue
        try:
            with open(fp, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            results[key] = data if data else {}
        except Exception as e:
            print(f"[WARN] 读取 {key} 失败: {e}", file=sys.stderr)
            results[key] = {"_error": str(e)}
    if scene_dir:
        results["_scene_dir"] = scene_dir.name
    yaml.dump(results, sys.stdout, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

# ── WRITE ─────────────────────────────────────────────────────────
def cmd_write(world_dir: Path, full_replace: bool = False):
    scene_dir = get_scene_dir(world_dir)
    existing = discover_files(world_dir, scene_dir)

    if full_replace:
        print("[WARN] --full 全量覆写：只保留 stdin 提供的键，未提及的键将被清除。确认无遗漏后再继续。", file=sys.stderr)

    delta = yaml.safe_load(_read_stdin_utf8())
    if delta is None:
        print("[ERR] stdin 为空", file=sys.stderr); sys.exit(1)

    written = []
    failures = []
    for key, new_data in delta.items():
        if key.startswith("_"):
            continue
        filepath, note = resolve_char_file(existing, key, world_dir)
        if filepath is None:
            if note:
                print(note, file=sys.stderr)
            else:
                print(f"[WARN] 未知 key: {key}, 跳过", file=sys.stderr)
            failures.append(key)
            continue
        if note:
            print(note, file=sys.stderr)

        if filepath.exists() and not full_replace:
            try:
                with open(filepath, encoding="utf-8") as f:
                    existing_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"[ERR] {key} 解析失败，拒绝写入（防止静默清空）: {e}", file=sys.stderr)
                failures.append(key)
                continue
            merged = deep_merge(existing_data, new_data)
        else:
            merged = new_data

        write_yaml(filepath, merged)
        written.append(key)

    if failures:
        print(f"[FAIL] {len(failures)} 个文件未写入: {', '.join(failures)}", file=sys.stderr)
        sys.exit(1)
    print(f"[OK] 已更新 {len(written)} 个文件: {', '.join(written)}")

# ── 语义不变量（audit）─────────────────────────────────────────
# 脚本校验线（与 keys.md 记忆锚点行 / write_protocol.md 写入表 一致）
ANCHOR_LIMIT_TOTAL = 3000
# 记忆锚点单条长度**不设限**（口径见 write_protocol.md 写入表 / keys.md「记录字段写法」）：
# 锚点质量由「须自足」定义（实体在事实段·定性可直接读出）——字数不是有效指标，
# 强压字数会牺牲自足性。
TRAJECTORY_WINDOW = 10              # 连续行动轨迹窗口（最近 N 轮·APPEND 后脚本自动删最旧·LLM 零操作·长期记忆由记忆锚点承载）

def _strip_wrapping_quotes(text: str) -> str:
    """循环剥离完整包裹引号：内容被一对匹配的单/双引号首尾完整包裹即剥一层，直到不再匹配。
    输入侧引号=批次文本通道的运输保护（防换行/特殊字符），落盘前剥净交 yaml.dump 重新封装；
    多层累积（'''x'''）一并归一。对白类内嵌引号不满足「首尾同字符成对包裹」判据，不受影响。"""
    t = text.strip()
    while len(t) >= 2 and t[0] == t[-1] and t[0] in ("'", '"'):
        t = t[1:-1].strip()
    return t

def _parse_world_time(text: str):
    """解析世界时间 '第N日 HH:MM' → (day:int, minutes:int)；无法解析返回 (None, None)。
    供重置点机械拦截（④b）与 reset-cycle 重建到期时刻使用。"""
    m = re.match(r"第\s*(\d+)\s*日\s*(\d{1,2}):(\d{2})", _strip_wrapping_quotes(str(text)))
    if not m:
        return None, None
    try:
        day = int(m.group(1))
        minutes = int(m.group(2)) * 60 + int(m.group(3))
        return day, minutes
    except ValueError:
        return None, None


def _cycle_reset_due(ws_data, day, minute):
    """重置类周期倒计时判定：返回 (到期时刻, 日标签) —— day/minute 越过到期时刻 且 维护名单无覆盖该日的非豁免条目；否则 None。

    供 ④b 重置点机械拦截（传入批次新写值）与 precheck 周期重置义务预曝光（传入当前值）共用——
    判据同源，故预检的「本批写具体时间会被顶回」预测与闸门的实际拦截完全一致。
    """
    if day is None or not isinstance(ws_data, dict):
        return None
    try:
        due_hit = None
        cds = ws_data.get("外部倒计时") or {}
        if isinstance(cds, dict):
            for cd in cds.values():
                # 仅重置类周期倒计时（威胁含 周期/重置/循环 关键字）参与；
                # 非周期倒计时即使误带「到期时刻」字段也不参与（2026-08-13 修复）
                if isinstance(cd, dict) and str(cd.get("到期时刻", "")).strip() and (
                        "周期" in str(cd.get("威胁", "")) or "重置" in str(cd.get("威胁", "")) or "循环" in str(cd.get("威胁", ""))):
                    dd, dm = _parse_world_time(str(cd.get("到期时刻", "")))
                    if dd is not None and (dd, dm) <= (day, minute):
                        due_hit = str(cd.get("到期时刻", "")).strip()
                        break
        if not due_hit:
            return None
        reset_rec = ws_data.get("维护名单") or {}
        day_label = f"第{day}日"
        if isinstance(reset_rec, dict):
            for rspec in reset_rec.values():
                # 豁免条目（触发=豁免）不算全员重置已执行——豁免仅跳过该角色·其他循环角色仍须重置
                #   （2026-08-17 加入·防豁免条目误放行全员重置）
                if isinstance(rspec, dict) and str(rspec.get("重置日期", "")) == day_label \
                        and str(rspec.get("触发", "")) != "豁免":
                    return None
        return due_hit, day_label
    except Exception:
        return None


def parse_batch_entries(lines):
    """解析 ###FILE/###KEY/###APPEND/###DELETE 与批次元数据行。
    返回 ctx（dict）：
      ops      : [(kind, file_key, key_path, content, append)]，kind ∈ {"write","delete"}；空值 KEY 覆盖在此阶段拒绝
      errors   : 解析错误列表
      meta     : ###META 行（静默自查锚点——不产生写入 ops·不落盘）
      stage    : ###STAGE 声明的阶段名（戏剧家/编剧/导演/角色/场记/作家·缺省 ""）
      storyline: [(动作行, payload行列表|None)]——add/rewrite/close 后跟 YAML 块（到下一个 ### 行·write-raw 自动执行）
      beat     : [动作行]——set/deepen/advance（③导演·无 payload）
      action   : [行动卡行]——④角色阶段产物（三件套+有条件代价·audit ①/①b/⑨ 检查对象）
      schedule : [行动链留痕行]——④角色·时间窗口收敛记录（不落盘·不裁决调度）"""
    ops = []
    errors = []
    meta_lines = []
    stage = ""
    storyline_lines = []
    beat_lines = []
    action_lines = []
    schedule_lines = []
    muse_lines = []
    current_file = None
    current_key = None
    current_append = False
    current_content = []
    sl_payload = None

    def flush():
        nonlocal current_file, current_key, current_append, current_content
        if current_file and current_key:
            content = "\n".join(current_content).rstrip("\n")
            if not current_append and content == "":
                errors.append(f"空值覆盖已拒绝: {current_file}.{current_key}（###KEY: 值不能为空；追加请用 ###APPEND:，覆盖需带完整值）")
            else:
                ops.append(("write", current_file, current_key, content, current_append))
        current_key = None
        current_append = False
        current_content = []

    for line in lines:
        line = line.lstrip("\ufeff")  # Windows 工具链（如 PS5.1 Set-Content -Encoding UTF8）可能在首行产生 BOM
        if line.startswith("###STAGE:"):
            sl_payload = None
            stage = line[len("###STAGE:"):].strip()
        elif line.startswith("###META:"):
            sl_payload = None
            meta_lines.append(line[8:].strip())
        elif line.startswith("###STORYLINE:"):
            sl_action = line[len("###STORYLINE:"):].strip()
            first = sl_action.split()[0] if sl_action else ""
            if first in ("add", "rewrite", "close"):
                sl_payload = []
                storyline_lines.append((sl_action, sl_payload))
            else:
                sl_payload = None
                storyline_lines.append((sl_action, None))
        elif line.startswith("###BEAT:"):
            sl_payload = None
            beat_lines.append(line[len("###BEAT:"):].strip())
        elif line.startswith("###ACTION:"):
            sl_payload = None
            action_lines.append(line[len("###ACTION:"):].strip())
        elif line.startswith("###SCHEDULE:"):
            sl_payload = None
            schedule_lines.append(line[len("###SCHEDULE:"):].strip())
        elif line.startswith("###MUSE:"):
            sl_payload = None
            muse_lines.append(line[len("###MUSE:"):].strip())
        elif line.startswith("###FILE:"):
            sl_payload = None
            flush()
            current_file = line[8:].strip()
        elif line.startswith("###KEY:"):
            sl_payload = None
            flush()
            current_key = line[7:].strip()
            current_append = False
        elif line.startswith("###APPEND:"):
            sl_payload = None
            flush()
            current_key = line[10:].strip()
            current_append = True
        elif line.startswith("###DELETE:"):
            sl_payload = None
            flush()
            rest = line[10:].strip()
            parts = rest.split(None, 1)
            if len(parts) == 2:
                ops.append(("delete", parts[0], parts[1], "", False))
            else:
                errors.append("###DELETE 格式: ###DELETE: <文件key> <YAML键路径>")
        elif sl_payload is not None:
            # ###STORYLINE: add/rewrite 的事件线 YAML 块（收集到下一个 ### 行）
            sl_payload.append(line)
        elif current_file and current_key:
            # 内容行内嵌标记检测（防拼接 bug）：行内出现批次标记但不在行首 = 上一字段内容被拼接
            for marker in ("###FILE:", "###KEY:", "###APPEND:", "###DELETE:", "###STORYLINE:", "###BEAT:", "###ACTION:", "###SCHEDULE:", "###STAGE:"):
                if marker in line and not line.lstrip().startswith(marker):
                    errors.append(
                        f"内容行内嵌标记 {marker.strip(':')}（行首无标记）：'{line[:60]}'——疑似上一字段内容与标记拼接（如缺少换行）。"
                        f"位置: {current_file}.{current_key}"
                    )
                    break
            current_content.append(line)
    flush()
    return {"ops": ops, "errors": errors, "meta": meta_lines, "stage": stage,
            "storyline": storyline_lines, "beat": beat_lines, "action": action_lines, "schedule": schedule_lines,
            "muse": muse_lines}


META_CLAIM_PREFIXES = ("角色覆盖", "记忆✓", "绑定")
# 需带冒号的前缀；`记忆✓` 后直接接 ` {角色}:{计数}·{状态}`，不带冒号（格式见 phase_actor.md META 记忆标记）
META_CLAIM_COLONED = frozenset({"角色覆盖", "绑定"})


def _meta_claim_segments(meta_lines, keyword):
    """提取 ###META 中某前缀声明（如「角色覆盖:」「绑定:」）的全部声明段。

    兼容三种写法：单独一行一条、一行内逗号分隔多人、一行内多个前缀空格衔接
    （如 `角色覆盖: A=更新 记忆✓ A:1·已触发 绑定: A=子agent`）。

    **段边界=下一个任意声明前缀的起点**，不只是同一关键字的下一次出现——
    旧实现只以同关键字的下一次命中为终点，会把同行后续前缀的内容一并吞进本段，
    再按逗号切分后生成伪条目覆盖真值（实测：`角色覆盖: A=更新 绑定: A=子agent`
    解析出 `A=子agent`，把真正的 `A=更新` 覆盖掉）。前缀全集见 META_CLAIM_PREFIXES。

    返回声明段文本列表（每段=一个前缀后的内容）。
    """
    segments = []
    pattern = re.compile(rf"(?:^|\s){re.escape(keyword)}\s*[:：]\s*")
    stop_alt = "|".join(re.escape(p) + (r"\s*[:：]" if p in META_CLAIM_COLONED else "")
                        for p in META_CLAIM_PREFIXES)
    stop = re.compile(rf"(?:^|\s)(?:{stop_alt})")
    for line in meta_lines or []:
        text = str(line or "")
        hits = list(pattern.finditer(text))
        for i, m in enumerate(hits):
            end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
            nxt = stop.search(text, m.end())
            if nxt:
                end = min(end, nxt.start())
            segments.append(text[m.end():end].strip())
    return segments


def _parse_role_coverage(meta_lines):
    """解析 ###META 中的结构化角色覆盖声明。

    格式：角色覆盖: Name=更新,Other=更新(在轨·轻量)
    返回 {规范化角色名: 状态}；角色名允许用下划线代替空格。
    """
    coverage = {}
    for seg in _meta_claim_segments(meta_lines, "角色覆盖"):
        for item in seg.split(","):
            item = item.strip()
            if "=" not in item:
                continue
            role, status = item.split("=", 1)
            role = role.strip().replace("_", " ")
            status = status.strip()
            if role:
                coverage[role] = status
    return coverage


def _parse_role_binding(meta_lines):
    """解析 ###META 中的执行绑定声明（phase_actor 执行绑定 Step 0）。

    格式：绑定: Name=子agent,Other=单窗口(豁免原因)
    返回 {规范化角色名: 状态}；角色名允许用下划线代替空格。
    """
    binding = {}
    for seg in _meta_claim_segments(meta_lines, "绑定"):
        for item in seg.split(","):
            item = item.strip()
            if "=" not in item:
                continue
            role, status = item.split("=", 1)
            role = role.strip().replace("_", " ")
            status = status.strip()
            if role:
                binding[role] = status
    return binding


def _action_roles(action_lines):
    """收集 ###ACTION 行动卡的角色名（'{角色}: {行为序列} | 驱动: …' 前缀）。"""
    roles = set()
    for line in action_lines or []:
        m = re.match(r"^\s*([^:|]+)[:：]", str(line))
        if m:
            role = m.group(1).strip()
            if role:
                roles.add(role)
    return roles


def _direction_schedule_text(world_dir: Path) -> str:
    """direction.yaml 的「调度单」字段文本（③导演主次分档·焦内活跃/背景角色/焦外）。"""
    fp = world_dir / "states" / DIRECTION_FILE
    if not fp.exists():
        return ""
    try:
        d = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return ""
    if not isinstance(d, dict):
        return ""
    return str(d.get("调度单", "") or "")


def _strip_wrapping_brackets(text: str) -> str:
    """若整串被一对括号包裹则剥掉（支持中英圆/方/花括号·可叠加）。

    `Clementine Pennyfeather(厅角钢琴·弹下半首中)` 的 `(…)` 是画面注记，
    剥掉后剩档案名本体——匹配在「名 + 注记」两段上都能成功。只在整串被
    完整包裹时剥（`A(B) C(D)` 不动），避免误切正文。"""
    s = (text or "").strip()
    pairs = {"(": ")", "（": "）", "[": "]", "【": "】", "{": "}", "｛": "｝"}
    changed = True
    while changed and len(s) >= 2 and s[0] in pairs and s[-1] == pairs[s[0]]:
        # 校验首括号与其配对尾括号确实闭合整串（防 `(A)·(B)` 误剥）
        depth = 0
        closes_at = -1
        for i, ch in enumerate(s):
            if ch == s[0]:
                depth += 1
            elif ch == pairs[s[0]]:
                depth -= 1
                if depth == 0:
                    closes_at = i
                    break
        if closes_at != len(s) - 1:
            break
        s = s[1:-1].strip()
    return s


def _split_schedule_segments(segment: str) -> list[str]:
    """调度单分档文本切独立人名段（全等点名用·与子串提醒共享切分口径）。

    分隔符：`·` `,` `，` `、` `;` `；`。**括号内的分隔符不切**——注记
    `Clementine Pennyfeather(厅角钢琴·弹下半首中)` 里的 `·` 属注记内容，
    切开会把档案名碎成 `…(厅角钢琴` / `弹下半首中)` 两段、导致全等匹配
    失败、整档解析为空（存量 bug·实测）。切分后额外产出去注记的形态
    （括号注记剥离版），使「名(注记)」与「名」两种写法都能命中。"""
    text = segment or ""
    parts, buf, depth = [], [], 0
    brackets = {"(": ")", "（": "）", "[": "]", "【": "】", "{": "}", "｛": "｝"}
    closing = set(brackets.values())
    for ch in text:
        if ch in brackets:
            depth += 1
            buf.append(ch)
        elif ch in closing and depth > 0:
            depth -= 1
            buf.append(ch)
        elif depth > 0:
            buf.append(ch)
        elif re.match(r"[·,，、;；]", ch):
            if buf:
                parts.append("".join(buf))
                buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    out: list[str] = []
    for p in (x.strip() for x in parts):
        if not p:
            continue
        out.append(p)
        # 同时产出去注记形态（供「名(注记)」命中档案名）
        stripped = _strip_wrapping_brackets(p)
        if stripped and stripped != p:
            out.append(stripped)
        # 末尾注记未闭合的残段（历史脏数据）：再剥一层尾随括号
        m = re.match(r"^(.*?)\s*[（(\[【].*$", p)
        if m and m.group(1).strip() and m.group(1).strip() != p:
            cand = m.group(1).strip()
            if cand not in out:
                out.append(cand)
    return out


# 调度单四档（v0.30 起「背景」桶更名「背景角色」——直指在场非行动主体角色）。
# 读取端兼容旧字面「背景」：仅当其后紧跟 =/: 才命中（「背景角色=」不会误命中「背景」），
# 供存量 direction.yaml / 快照在迁移前照常解析；写入端一律用新字面。
_SCHEDULE_BUCKETS = ("焦内活跃", "背景角色", "焦外→焦内", "焦外")
_SCHEDULE_BUCKET_TOKENS = (
    ("焦内活跃", "焦内活跃"),
    ("背景角色", "背景角色"),
    ("背景", "背景角色"),
    ("焦外→焦内", "焦外→焦内"),
    ("焦外", "焦外"),
)


def _schedule_body_text(schedule_text: str | None, bucket: str) -> str:
    """取调度单中某桶的正文文本（不含桶头与后续桶）。与 _schedule_roles_by_bucket
    使用同一「桶头位置切片」口径：桶头仅作分界，正文 = 桶头到下一桶头之间。
    尾部由 `·` 等分隔符引入的悬空残符会被清掉（下一桶头前的 ` · ` 属分界，
    不属本桶正文）。"""
    sched = str(schedule_text or "")
    if not sched:
        return ""
    heads = [(m.start(), m.end(), canon) for _token, canon in _SCHEDULE_BUCKET_TOKENS
             for m in re.finditer(rf"\b{re.escape(_token)}\s*[=:：]", sched)]
    heads.sort()
    for i, (_pos, seg_start, canon) in enumerate(heads):
        if canon != bucket:
            continue
        seg_end = heads[i + 1][0] if i + 1 < len(heads) else len(sched)
        return re.sub(r"[\s·,，、;；]+$", "", sched[seg_start:seg_end])
    return ""


def _schedule_roles_by_bucket(world_dir: Path, schedule_text: str | None = None) -> dict[str, set[str]]:
    """从调度单提取四档角色；复用档案名匹配，供导演与角色阶段共享。

    四层（与 phase_director D5 / phase_actor 调度单 同构）：焦内活跃 / 背景角色 / 焦外 / 焦外→焦内。
    口径（硬性）：独立人名段与档案全名全等才命中（归一化去空格/大小写后比）；
    子串/token 别名命中只记软提醒、不计入命中（防同姓/同 token 连带，如 Dolores
    Abernathy 段连带 Peter Abernathy）。提醒文本由调用方经
    _schedule_substring_hints 统一拼装。

    分桶采用「桶头位置切片」而非正则 lookahead：避免 `焦外` 段把 `焦外→焦内=Teddy`
    整段吞入（实测旧正则 `焦外` 命中到 `D（可揭示）· 焦外→焦内=Teddy`）。"""
    sched = str(schedule_text if schedule_text is not None else _direction_schedule_text(world_dir) or "")
    known = set()
    for fp in world_dir.glob("characters/CHAR_*.md"):
        name = fp.stem[len("CHAR_"):].strip()
        if name:
            known.add(name)
    buckets = _SCHEDULE_BUCKETS
    result = {b: set() for b in buckets}
    if not sched:
        return result
    # 按桶头出现位置从左到右切片（桶头仅作分界，不再吞后续桶）
    heads = [(m.start(), m.end(), canon) for _token, canon in _SCHEDULE_BUCKET_TOKENS
             for m in re.finditer(rf"\b{re.escape(_token)}\s*[=:：]", sched)]
    heads.sort()
    for i, (_pos, seg_start, bucket) in enumerate(heads):
        seg_end = heads[i + 1][0] if i + 1 < len(heads) else len(sched)
        body = sched[seg_start:seg_end]
        for seg in _split_schedule_segments(body):
            for name in known:
                if _norm_char_key(seg) == _norm_char_key(name):
                    result[bucket].add(name)
    return result


def _schedule_substring_hints(world_dir: Path, schedule_text: str | None = None) -> list[str]:
    """子串/别名连带命中提醒（软提醒·不拦截）：独立段未全等命中、但段内含档案
    全名子串或单 token 别名的角色逐条列出，供 LLM 确认是否为独立点名笔误。"""
    sched = str(schedule_text if schedule_text is not None else _direction_schedule_text(world_dir) or "")
    known = set()
    for fp in world_dir.glob("characters/CHAR_*.md"):
        name = fp.stem[len("CHAR_"):].strip()
        if name:
            known.add(name)
    exact = _schedule_roles_by_bucket(world_dir, sched)
    exact_all = set().union(*exact.values()) if any(exact.values()) else set()
    hints: list[str] = []
    for bucket in _SCHEDULE_BUCKETS:
        # 与 _schedule_roles_by_bucket/_schedule_body_text 共用同一「桶头位置切片」，
        # 取代旧 lookahead 正则（旧式要求桶间恰为 ` · `，注记含 `·` 或分隔符变体时漏配）。
        body = _schedule_body_text(sched, bucket)
        if not body:
            continue
        for seg in _split_schedule_segments(body):
            for name in sorted(known):
                if name in exact_all:
                    continue
                aliases = {" ".join(name.split())}
                aliases.update(word for word in name.split() if len(word) >= 3)
                if any(alias in seg for alias in aliases):
                    hints.append(f"{bucket}段‘{seg}’疑似连带命中‘{name}’（子串/别名·非独立点名·请确认）")
    return hints


def _schedule_cast_roles(world_dir: Path) -> set:
    """从 调度单 提取点名/提及的已知角色名（四档角色·用于角色覆盖对账）。

    口径与 _schedule_roles_by_bucket 一致（**同一匹配规则·两条路径不可分歧**）：
    只认独立人名段与档案全名全等命中（含「名(注记)」剥离版）；子串/别名命中走
    _schedule_substring_hints 软提醒、不计入覆盖名单。

    范围＝四档（焦内活跃/背景角色/焦外→焦内/焦外）——规格（phase_actor 闸门、
    keys.md「更新触发」）要求 调度单点名角色一律进角色覆盖：焦内活跃须有行动、
    背景角色/焦外经轻量自推演刷新；`焦外→焦内` 为过渡档（本轮须落最终桶）同须覆盖。"""
    buckets = _schedule_roles_by_bucket(world_dir)
    if any(buckets.values()):
        return set().union(*buckets.values())
    # 兜底：主路径全空（无档案可匹配/调度单格式异常）——仍按四档正文取候选，
    # 但**沿用主路径的全等口径**（旧实现退化为裸子串包含，会把 `A` 连带进
    # `Angela`、结果与主路径不一致·实测易致覆盖对账两套结论）。
    sched = _direction_schedule_text(world_dir)
    if not sched:
        return set()
    known = set()
    for fp in world_dir.glob("characters/CHAR_*.md"):
        stem = fp.stem[len("CHAR_"):].strip()
        if stem:
            known.add(stem)
    known_keys = {_norm_char_key(n): n for n in known}
    cast = set()
    for _b in _SCHEDULE_BUCKETS:
        for _seg in _split_schedule_segments(_schedule_body_text(sched, _b)):
            hit = known_keys.get(_norm_char_key(_seg))
            if hit:
                cast.add(hit)
    return cast


def _focus_region_markers(world_dir: Path) -> list[str]:
    """当前焦点场景区域的中文/名称标记（用于角色时间线位置与场景归属匹配）。

    焦点区域 REGION 路径为英文（如 `Westworld Park 1/Sweetwater/Main Street`），
    而 CHAR_.md 时间线位置为中文（如 `甜水镇·主街/酒馆外`、`甜水镇·Mariposa等`），
    两者无法直接字符串匹配。故取两类表面：
    - 焦点场景 REGION.md 标题中 ` / ` 后的中文名（如 `主街`）；
    - 焦点场景 scene_card 场景名（如 `甜水镇主街`）及区域行链上的中文片段。
    返回可参与 `in` 子串匹配的中文标记列表（含 '·' 切分的中文段）。"""
    markers: list[str] = []
    _focus = _focus_region_node(world_dir)
    if _focus:
        fp = world_dir / "regions" / _focus / "REGION.md"
        if fp.exists():
            try:
                in_sub = False
                for ln in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
                    s = ln.strip()
                    if s.startswith("## "):
                        in_sub = bool(re.match(r"^##\s*子区域", s))
                    elif in_sub and s.startswith("-"):
                        # 子区域行形如 `- Mariposa（主街中段北侧·…）`——取子区域名
                        _nm = re.sub(r"^-\s*", "", s).split("（")[0].split("(")[0].strip()
                        if _nm:
                            markers.append(_nm)
                    elif s.startswith("# ") and "/" in s:
                        # 标题形如 `# Main Street / 主街`——取中/英文两侧非空白段
                        for _part in s.lstrip("#").split("/"):
                            _p = _part.strip()
                            if _p:
                                markers.append(_p)
            except Exception:
                pass
    # 场景名（scene_card「场景名」中文）
    sc_fp = get_scene_dir(world_dir)
    if sc_fp is not None:
        card = sc_fp / "scene_card.md"
        if card.exists():
            try:
                m = re.search(r"^\|\s*场景名\s*\|\s*([^|]+?)\s*\|", card.read_text(encoding="utf-8", errors="ignore"), re.M)
                if m:
                    for _part in re.split(r"[·,，、]", m.group(1).strip()):
                        if _part.strip():
                            markers.append(_part.strip())
            except Exception:
                pass
    return [mk for mk in markers if mk]


def _scene_cast_baseline(world_dir: Path) -> set:
    """本场景应出现的角色基线（precheck 义务区 / gate keeper cast 覆盖 共用，单一来源）。

    基线 = POV ∪ 本场常驻NPC ∪ conflicts 关联角色 ∪ 调度单四层角色。

    「本场常驻NPC」判定（NPC 会动，非静态全员硬入）：仅取 REGION.常驻NPC 中
    —— 其 CHAR_.md「默认循环时间线」在当前时刻命中位置 ∈ 焦点场景区域（或该角色无时间线解析
    —— 此时按 REGION 静态归属保守纳入，本场景是它的注册地）；
    —— 时间线命中别处者（如 Dolores 12:00-14:00=牧场·不在主街）→ 本场景基线**不纳入**（他处仍
       在世界的角色不视为本场缺席），只入 precheck §3 待物化清单（④物化）。
    判据完全复用 _char_timeline_preset / _focus_region_node，不新增机制。"""
    baseline = set()
    # POV（用户角色·直接从 world_state 叙事约定解析，避免依赖 existing 上下文）
    try:
        _ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
        _pov = re.search(r"POV\s*=\s*([^；;\n]*)", str(_ws.get("叙事约定", "") or ""))
        if _pov:
            _pov_tok = _pov.group(1).strip()
            # 优先取括号内实际角色名（如 `游客(Guest)` → Guest；`游客` 是视角标签非角色名）
            _paren = re.search(r"[（(]([^（）()]+)[)）]", _pov_tok)
            _pov_name = (_paren.group(1).strip() if _paren else _pov_tok.split("(")[0].strip())
            if _pov_name:
                baseline.add(_pov_name.replace("_", " "))
        else:
            for _cfp in world_dir.glob("characters/CHAR_Guest*.md"):
                _n = _cfp.stem[len("CHAR_"):].strip().replace("_state", "").strip()
                if _n:
                    baseline.add(_n.replace("_", " "))
                    break
    except Exception:
        pass
    # 调度单四层角色（导演已声明的画面成员）
    baseline.update(_schedule_cast_roles(world_dir))
    # conflicts 关联角色：仅当「当前时刻物理在本场」才强制入 cast 义务——
    #   其 CHAR_state.位置（或时间线命中位置）在本场，或已被调度单点名。
    #   否则他处仍在世界的冲突角色不构成「本场 cast 缺失」，由④/⑤焦外管道跟踪。
    _focus = _focus_region_node(world_dir)
    _timelines = _parse_char_timeline(world_dir)
    _cur_min, _t = _parse_world_current_min(world_dir)
    _markers = _focus_region_markers(world_dir)
    _char_states = dict(_load_char_states(world_dir))
    try:
        _cd = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
        for _ct, _cv in _cd.items() if isinstance(_cd, dict) else []:
            if not isinstance(_cv, dict):
                continue
            for _r in (_cv.get("关联角色") or []):
                if not isinstance(_r, str) or not _r.strip():
                    continue
                _rn = _r.strip()
                if _in_region(_rn, _focus, _markers, _timelines, _cur_min, _char_states):
                    baseline.add(_rn)
    except Exception:
        pass
    # 本场常驻NPC（按当前时刻时间线命中本场）
    if _focus:
        for npc in _region_record_npcs(world_dir, _focus):
            _rows = _timelines.get(npc) or []
            if not _rows:
                # 无时间线解析 → 按 REGION 静态归属保守纳入（本场景是注册地）
                baseline.add(npc)
                continue
            _loc, _ac, _inwin = _char_timeline_preset(_rows, _cur_min)
            if _inwin and _loc and any(_mk in _loc for _mk in _markers):
                # 时间线命中且位置含焦点场景中文标记 → 纳入本场
                baseline.add(npc)
            # 时间线命中但位置在别的区域 → 不纳入（他在别处）
    return baseline


def _cast_overlap_missing(world_dir: Path, baseline: set) -> list[str]:
    """返回 baseline 中未被 scene_card cast 覆盖的角色（缺名·按规范名归一）。

    覆盖面 = scene_card「出场角色」(焦内) + 「焦外/在场」(焦外)。判定时不要求面面俱到：
    baseline 里的角色只要在任一栏以具名（或以可归一到的档案全名）出现即视为覆盖；
    仅无 CHAR_.md 的纯背景「群像」才允许占位——若 baseline 角色被「群像/外部者/游客/守卫」
    等虚词替代（未具名），视为缺名（虚词不可替代具名角色）。
    角色可能以简称（如 Dolores/Teddy）出现在 cast——用档案全名+token 别名归一到 baseline。
    """
    sc_fp = get_scene_dir(world_dir)
    if sc_fp is None:
        return sorted(baseline)
    card = sc_fp / "scene_card.md"
    if not card.exists():
        return sorted(baseline)
    try:
        txt = card.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return sorted(baseline)
    covered_raw: list[str] = []
    for col in ("出场角色", "焦外/在场"):
        m = re.search(rf"^\|\s*{re.escape(col)}\s*\|\s*([^|]+?)\s*\|", txt, re.M)
        if m:
            for _seg in re.split(r"[·,，、;；]", m.group(1)):
                _s = _seg.strip().lstrip("-")
                if _s and _s.lower() not in ("无", "none", "-"):
                    covered_raw.append(_s)
    # 虚词：以下 token 不能替代具名档案角色
    VAGUE = ("群像", "外部者", "游客", "守卫", "群众", "背景", "路人", "纯背景")
    known = set()
    for fp in world_dir.glob("characters/CHAR_*.md"):
        nm = fp.stem[len("CHAR_"):].strip().replace("_state", "").strip()
        if nm:
            known.add(nm)
    missing = []
    for role in sorted(baseline):
        rk = _norm_char_key(role)
        hit = False
        for cand in covered_raw:
            ck = _norm_char_key(cand.split("(")[0].strip())
            # 虚词不可替代具名角色——只判名字部分（ck）：`Dolores Abernathy(背景)` 是具名，档位括注不使其退化为虚词
            if any(v in ck for v in VAGUE):
                continue
            if rk == ck:
                hit = True
                break
            # token 别名：角色全名或 ≥3 字符 token 在候选段中出现
            toks = {_norm_char_key(w) for w in role.split() if len(w) >= 3}
            toks.add(rk)
            if any(t and t in ck for t in toks):
                hit = True
                break
        if not hit:
            # 虚词替代已建档角色 → 缺名
            missing.append(role)
    return sorted(missing)


def _in_region(role_name: str, focus_region: str | None, markers: list[str],
               timelines: dict, cur_min, char_states: dict) -> bool:
    """角色当前是否物理在本场（focus_region）。

    判据（按序取可靠）：① CHAR_state.位置 命中焦点区域标记；② 时间线命中位置命中标记；
    ③ 已被调度单点名（画面成员·无论位置）——由调用方并入 baseline（此处只判物理位置）。
    无任何定位线索 → 不视为本场（避免把全局冲突角色误判为在场）。"""
    if not focus_region or not markers:
        return False
    # ① CHAR_state.位置
    for _cn, _cd in char_states.items():
        if _norm_char_key(_cn) == _norm_char_key(role_name):
            _pos = str(_cd.get("位置", "") or "").strip()
            if _pos and any(_mk in _pos for _mk in markers):
                return True
            break
    # ② 时间线命中位置
    _rows = timelines.get(role_name) or []
    if _rows:
        _loc, _ac, _inwin = _char_timeline_preset(_rows, cur_min)
        if _inwin and _loc and any(_mk in _loc for _mk in markers):
            return True
    return False


def _loop_relevant_roles(world_dir: Path) -> set:
    """循环轨道逐角色结论的必须覆盖名单（与 precheck §1b / gate 轨道✓ 同源闭环）：
    三源并集——① 调度单点名循环角色（③已声明画面成员·必保）② 当前焦点场景区 REGION 常驻NPC
    ③ §1a 临近互锁涉及角色（即将入画·来自 LOOPS 跨角色互锁时刻表）。
    限定循环角色（自主性 ∈ 枚举）：调度单点名的非循环角色（如用户 Guest）不属轨道✓对象。
    「时段内活跃」不再单独展开（避免把 Pariah/Mesa 等跨区角色误捞——大区归属由 REGION 常驻NPC承载）。
    返回角色全名 set。"""
    loop_names = [n for n, d in _load_char_states(world_dir)
                  if str(d.get("自主性", "") or "").strip() in AUTO_ORDER]
    if not loop_names:
        return set()
    # 循环角色别名 → 档案全名：全名 + 各 token（≥3 字符）——互锁表/调度单常以名字引用（Hector/Maeve/Clementine）
    _alias = {}
    for n in loop_names:
        _alias[_norm_char_key(n)] = n
        for w in n.split():
            if len(w) >= 3:
                _alias.setdefault(_norm_char_key(w), n)

    def _canon(nm):
        k = _norm_char_key(nm)
        return _alias.get(k) or _alias.get(_norm_char_key(nm.split("·")[0])) or None

    # ① 调度单点名的循环角色（焦内活跃/背景角色/焦外 与循环角色取交集）
    relevant = {n for n in _schedule_cast_roles(world_dir) if _norm_char_key(n) in _alias}

    # ② 当前焦点场景区 REGION 常驻NPC
    _focus = _focus_region_node(world_dir)
    for n in _region_record_npcs(world_dir, _focus):
        c = _canon(n)
        if c:
            relevant.add(c)

    # ③ §1a 临近互锁涉及角色（LOOPS 跨角色互锁时刻表·窗口重叠·简称归一到档案全名）
    cur_min, _t = _parse_world_current_min(world_dir)
    _bm, *_ = _window_status(world_dir)
    _wmin = _bm if _bm is not None else 30
    if cur_min is not None:
        for _s0, _e0, _ev, roles in _loops_interlocks_near(_loops_interlocks(world_dir), cur_min, _wmin):
            for r in roles:
                c = _canon(r)
                if c:
                    relevant.add(c)
    return relevant


def _norm_char_key(key: str) -> str:
    """归一化角色字符键（去空格/下划线·小写）——兼容 ###FILE 空格 vs 下划线混用。"""
    return key.replace(" ", "").replace("_", "").lower()


def _load_char_states(world_dir: Path) -> list:
    """读全部 CHAR_state → [(角色名, 数据)]（角色名=文件名去 CHAR_ 前缀与 _state 后缀；读失败/非映射跳过）。"""
    out = []
    states = world_dir / "states"
    if not states.is_dir():
        return out
    for fp in sorted(states.glob(f"{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
        try:
            data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if isinstance(data, dict):
            out.append((fp.stem[len(CHAR_STATE_PREFIX):-len("_state")], data))
    return out


def _loop_char_keys(world_dir: Path) -> set:
    """循环角色集合（归一化键）：读状态文件 自主性 字段在枚举内即为循环角色。
    用于循环轨道硬拦（循环世界 ①戏剧家批须含逐角色 `轨道✓(...)` 结论·见 loop_machinery §1）。"""
    return {_norm_char_key(name) for name, data in _load_char_states(world_dir)
            if str(data.get("自主性", "") or "").strip() in AUTO_ORDER}


def _batch_preceding(ops, idx, file_key, key_path_str, current):
    """取批次内 idx 之前对 file_key.key_path_str 的最后写入值；无则回落磁盘当前值（current）。

    current 是 check_batch 起始构建的磁盘快照·不随 op 变更——两个来源都不可省：
      跨轮累积（压力前几轮已落盘·本批只升档）→ 走磁盘；
      同批级联（本批推到临界再升档，见 phase_actor 写入节「先完成本批压力/防御更新再判」）→ 走前置 op。
    """
    val = None
    for i, (_k, _fk, _kp, _c, _a) in enumerate(ops):
        if i >= idx:
            break
        if _k == "write" and _fk == file_key and _kp == key_path_str:
            val = _strip_wrapping_quotes(str(_c)).strip()
    if val is None:
        data = current.get(file_key) or {}
        val = str(data.get(key_path_str, "") or "").strip() if isinstance(data, dict) else ""
    return val


def _canonicalize_char_ops(ops, world_dir, existing):
    """把批次内可解析的 CHAR_ 别名统一为真实 state 文件 stem。

    check_batch 的 current/前置 op 对账必须使用同一个逻辑 key；否则同一角色用空格、
    下划线或缺后缀写法时，升档门槛与轨迹覆盖检查会读不到真实旧值。未知 key 保留原文，
    由后续 FILE/写入路径报告错误，不在此处猜测角色。
    """
    normalized = []
    for op in ops:
        if len(op) != 5:
            normalized.append(op)
            continue
        kind, file_key, key_path, content, append = op
        canonical = _normalize_file_key(file_key)
        if canonical.startswith(CHAR_STATE_PREFIX):
            fp, _ = resolve_char_file(existing, canonical, world_dir)
            if fp is not None and fp.stem in existing:
                canonical = fp.stem
        normalized.append((kind, canonical, key_path, content, append))
    return normalized


def _pov_role_names(world_dir: Path, existing: dict) -> set:
    """用户角色名集合（POV 定位·与 _region_consistency 同源）：world_state.叙事约定 POV=… 优先·
    括号内名/token 逐一归一到已知状态名·命中即收；读不到回退 CHAR_Guest* 首个。
    供角色段缺 ACTION 豁免与调度单覆盖豁免（第二人称无指令可无决策无行动·不代笔）。"""
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws = {}
    if not isinstance(ws, dict):
        ws = {}
    known = set(_known_char_names(world_dir, existing))
    names = set()
    mm = re.search(r"POV\s*=\s*([^；;\n]*)", str(ws.get("叙事约定", "") or ""))
    if mm:
        seg = mm.group(1)
        cands = re.findall(r"[（(]([^（）()]+)[)）]", seg) + [t for t in re.split(r"[·,，、\s]+", seg) if t]
        for c in cands:
            c = c.strip()
            if not c:
                continue
            canon = _canonical_role_label(c, world_dir, existing)
            if canon in known:
                names.add(canon)
                break
    if not names:
        guests = sorted((world_dir / "states").glob(f"{CHAR_STATE_PREFIX}Guest*{CHAR_STATE_SUFFIX}"))
        if guests:
            names.add(guests[0].stem[len(CHAR_STATE_PREFIX):-len("_state")])
    return names


def check_batch(ops, world_dir, ctx=None, enforce_scene_dir=True, force=False, via="write", resume_from=False, maintenance=False):
    """语义不变量检查（六阶段批次→硬性违规/软性警告分类）。
    ctx = parse_batch_entries 返回值（stage/storyline/beat/action/schedule/meta）——按阶段分化必含项。
    enforce_scene_dir=False（gate/audit 预检路径）：scene_state 落点检查降级为软提示——
    场景目录由场记阶段 init_scene 创建（先于批次写入），预检时目录可能尚不存在，不误拦。
    硬性违规（hard）：结构性/机械性错误——关键字段缺失、载体核验、轮次单调、落点错误、Single Writer 越权。写入时**单字段顶回**。
    软性警告（soft）：内容质量类——记忆锚点超限等。写入时**不拦截**，仅记录（validate 汇总）。
    返回 (hard, soft)，元素为 (op_index, message)；批次级消息 op_index=-1（gate 按阶段升级为硬拦）。"""

    hard = []
    soft = []
    scene_dir = get_scene_dir(world_dir)
    existing = discover_files(world_dir, scene_dir)
    ctx = ctx or {}
    stage = str(ctx.get("stage", "") or "")
    storyline_lines = ctx.get("storyline") or []
    beat_lines = ctx.get("beat") or []
    action_lines = ctx.get("action") or []
    meta_lines = ctx.get("meta") or []

    # 预读当前值（用于对比型检查：轮次单调、锚点总量）
    current = {}
    for key, fp in existing.items():
        try:
            current[key] = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        except Exception:
            current[key] = {}

    # 先统一可解析的 CHAR_ 别名，再做所有跨 op/current 对账（多角色批次共用此规范化结果）。
    # 原始 ops 只在本函数内替换；落盘仍使用原始批次，write_one 会再次解析并输出映射提示。
    ops = _canonicalize_char_ops(ops, world_dir, existing)

    # 重置豁免预扫描（2026-08-12 加入）：批次内登记了角色重置（world_state.维护名单.{角色} KEY 写入）→
    # 该角色按 loop_machinery §4 联动表清空/压缩 记忆锚点/轨迹（脚本档全清·漂移压缩·觉醒/变质保留）。
    # 轨迹覆盖写检查对此豁免——重置清空是机制执行（联动表），不是丢失历史
    reset_chars = set()
    for _i, (_k, _fk, _kp, _c, _a) in enumerate(ops):
        if _k == "write" and _fk == "world_state" and _kp.startswith("维护名单."):
            _name = _kp[len("维护名单."):]
            if _name:
                reset_chars.add(_name)

    # Single Writer per State（硬性·design-v2 §4 写入矩阵）：###STAGE 声明后按矩阵拦截越权写入
    if stage in STAGE_WRITE_MAP:
        allowed = STAGE_WRITE_MAP[stage]
        for idx, (kind, file_key, key_path_str, content, append) in enumerate(ops):
            if kind != "write":
                continue
            ok = (file_key in allowed
                  or ("CHAR_" in allowed and file_key.startswith(CHAR_STATE_PREFIX)))
            if not ok:
                hard.append((idx, f"Single Writer 违规：{stage}批不得写 {file_key}.{key_path_str}（写入矩阵: conflicts=①戏剧家 / storylines=②编剧 / direction=③导演 / CHAR_*=④角色 / scenes+world_state+world_map+pending_actions+foreshadow=⑤场记——design-v2 §4）"))
    elif stage and stage not in STAGES:
        soft.append((-1, f"###STAGE '{stage}' 非法（枚举: {'/'.join(STAGES)}）"))

    # 批次整体必含项标记（阶段分化·见批次级检查）
    has_ct_op = False
    has_ws_time = False
    has_ws_round = False
    has_ws_summary = False
    has_scene_timeline = False
    has_char_op = False

    for idx, (kind, file_key, key_path_str, content, append) in enumerate(ops):
        if kind != "write":
            continue
        # CHAR_ 未命中真实 state 文件属于硬性 FILE 错误：先在 check_batch 拦截，避免 write_one
        # 失败后仍打印批次成功，或在多角色批次中悄悄漏掉一个角色。
        if file_key.startswith(CHAR_STATE_PREFIX):
            _char_fp, _char_note = resolve_char_file(existing, file_key, world_dir)
            if _char_fp is None:
                hard.append((idx, _char_note or f"未知 CHAR_state 文件 key: {file_key}——禁止新建"))
        # 人际动态档位写时软警（keys.md 枚举）——子 agent 产出非法档位当场暴露·不再等到收尾 validate
        if (kind == "write" and not append and file_key.startswith(CHAR_STATE_PREFIX)
                and key_path_str.split(".")[-1] == "人际动态"):
            _rel_first = next((ln for ln in str(content).strip().splitlines() if ln.strip()), "")
            _rel_m = re.match(r"^\s*([^:：]+)[:：]\s*(.+)", _rel_first)
            _rel_tier = _rel_m.group(2).split("——")[0].strip() if _rel_m else ""
            if _rel_tier and _rel_tier not in RELATION_TIERS:
                soft.append((idx, f"{file_key}: 人际动态档位 '{_rel_tier}' 非法（枚举: 稳固/信任/中立/防备/破裂/待重建）——写时提醒·落盘前可改"))
        key_path = key_path_str.split(".")

        # 嵌套记录字段类型校验（2026-08-17 加入·方案B·防复发）：记录类字段（world_state.维护名单.{角色}/时间线.{ID}/外部倒计时.{CD}
        #   ·world_map.已探索区域.{区域}）内容必须为 YAML 映射——多行字符串会被当字符串写入=读取端（reset-cycle 豁免/④b 覆盖判定/validate 8b）读不到。
        #   判据与 write_one 实际写入对齐：多行且 safe_load 为 dict → 写入 dict（放行）；单行/列表/解析失败 → 写入字符串（顶回）
        if len(key_path) == 2 and (
                (file_key == "world_state" and key_path[0] in ("维护名单", "时间线", "外部倒计时"))
                or (file_key == "world_map" and key_path[0] == "已探索区域")):
            _will_be_dict = False
            if "\n" in content:
                try:
                    _parsed_map = yaml.safe_load(content)
                except Exception:
                    _parsed_map = None
                _will_be_dict = isinstance(_parsed_map, dict)
            if not _will_be_dict:
                hard.append((idx, f"{file_key}.{key_path_str}: 嵌套映射字段内容必须为 YAML 映射（{key_path[0]}.{key_path[1]} 应为多行键值块·当前单行/列表/字符串=写入后读取端读不到）"))

        # 批次整体必含项标记
        if file_key == "conflicts" and key_path and key_path[0].startswith("CT-"):
            has_ct_op = True
        if file_key == "world_state" and key_path == ["时间", "具体时间"]:
            has_ws_time = True
        if file_key == "world_state" and key_path == ["轮次"]:
            has_ws_round = True
        if file_key == "world_state" and key_path == ["时间", "前情描述"]:
            has_ws_summary = True
        if file_key == "scene_state" and key_path == ["场景时间线"]:
            has_scene_timeline = True
        if file_key.startswith(CHAR_STATE_PREFIX):
            has_char_op = True

        # conflicts.yaml 路径归一化：去掉多余的 `conflicts.` 根前缀
        if file_key == "conflicts" and key_path and key_path[0] == "conflicts":
            key_path = key_path[1:]

        # ⓪ CT 已迁移字段守卫（硬性）：节拍表/当前节拍/下一个节拍(推荐)/角色反应 已迁出 conflicts——
        #    结构归 storylines（###STORYLINE·②编剧）/指针归 direction（###BEAT·③导演）/角色行动归 ###ACTION+CHAR_state（④角色）
        if file_key == "conflicts" and key_path:
            if key_path[0] == BEAT_TOP_KEY or (key_path[0].startswith("CT-")
                    and any(k in key_path for k in ("当前节拍", "下一个节拍(推荐)", "角色反应"))):
                hard.append((idx, f"{file_key}.{key_path_str}: 已迁移字段（节拍表/当前节拍/下一个节拍(推荐)/角色反应）——结构走 ###STORYLINE（storylines）/指针走 ###BEAT（direction）/角色行动走 ###ACTION+CHAR_state"))

        # ② 被争夺资源必须写明载体/持有者（实体写持有者·抽象写载体）
        if (file_key == "conflicts" and key_path and key_path[0].startswith("CT-")
                and key_path[-1] == "被争夺资源"):
            if "当前载体=" not in content and "当前持有者=" not in content:
                hard.append((idx, f"{file_key}.{key_path_str}: 被争夺资源缺「当前载体=/当前持有者=」（抽象写载体·实体写持有者·写不出=不合格）"))

        # ③ 记忆锚点：仅校验写入后总量 ≤3000（软性警告·不拦截——内容质量类，validate 汇总）
        #    单条长度不设限（见文件头常量注释）。
        if file_key.startswith(CHAR_STATE_PREFIX) and key_path == ["记忆锚点"]:
            filepath, _ = resolve_char_file(existing, file_key, world_dir)
            if append:
                total = len(content)
                if filepath and filepath.exists():
                    try:
                        old = (yaml.safe_load(filepath.read_text(encoding="utf-8")) or {}).get("记忆锚点", "")
                        if isinstance(old, list):
                            total += sum(len(str(it.get("内容", ""))) for it in old if isinstance(it, dict))
                        elif isinstance(old, str) and old:
                            total += len(old)
                    except Exception:
                        pass
                if total > ANCHOR_LIMIT_TOTAL:
                    soft.append((idx, f"{file_key}.记忆锚点: 写入后总量 {total} 字 > {ANCHOR_LIMIT_TOTAL} 校验线——建议执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）"))
            else:
                if len(content) > ANCHOR_LIMIT_TOTAL:
                    soft.append((idx, f"{file_key}.记忆锚点: 覆盖写入总量 {len(content)} 字 > {ANCHOR_LIMIT_TOTAL} 校验线"))

        # ④ 轮次单调（时间只增不减）——显式回退（--force）豁免：轮次可回退，但必须仍为整数
        # via="gate" 为闸门终检：落盘在闸门之前（SKILL 顺序：产出→写→gate），磁盘轮次已=新值，
        #   故用防倒退语义（new<old 才拦·new==old 放行=已落盘正常）；via="write"（write-raw/audit）为落盘前校验，用推进语义（new>old）。
        # via="write" 且 resume_from=True（--resume-from 重提失败段）：部分成功落盘后重提——磁盘轮次可能已=新值
        #   （批次先前写过·写入失败却已落盘轮次），重提同一批属"继续完成"非回退→沿用防倒退语义（new<old 才拦）。
        #   区分三类语义：推进（新轮·new>old）｜防倒退（重提/gate·new>=old 放行·仅拦真回退 new<old）｜--force 回退（任意）。
        if file_key == "world_state" and key_path == ["轮次"]:
            try:
                new_val = int(_strip_wrapping_quotes(content))
                old_val = int(_strip_wrapping_quotes(str(current.get("world_state", {}).get("轮次") or 0)))
                if not force:
                    if via == "gate" or (via == "write" and resume_from):
                        if new_val < old_val:
                            hard.append((idx, f"world_state.轮次: {new_val} < 当前值 {old_val}（时间只增不减·防回退——{('重提完成' if via == 'write' else '闸门终检')}语义·仍禁止真回退）"))
                    else:
                        if new_val <= old_val:
                            hard.append((idx, f"world_state.轮次: {new_val} 必须 > 当前值 {old_val}（时间只增不减·重提同轮用 --resume-from <本段号>·显式回退用 write-raw --batch --force）"))
            except ValueError:
                hard.append((idx, f"world_state.轮次: 非整数 '{content.strip()}'"))

        # ④b 重置点机械拦截（循环世界·周期倒计时管道）：写 时间.具体时间 越过 重置类周期到期时刻
        #     且 维护名单 无覆盖新时间日期的非豁免条目 → 硬性顶回（防跨天漏重置/回退重放；执行=worldctl.py reset-cycle）
        if file_key == "world_state" and key_path == ["时间", "具体时间"]:
            ws_cur = current.get("world_state", {}) or {}
            new_day, new_min = _parse_world_time(content)
            _due = _cycle_reset_due(ws_cur, new_day, new_min)
            if _due:
                hard.append((idx, f"world_state.时间.具体时间: 越过周期重置到期时刻 {_due[0]}·但 维护名单 无覆盖 {_due[1]} 的非豁免条目——重置未执行（执行: worldctl.py {world_dir.name} reset-cycle 后重写）"))


        # ⑤ scene_state 落点：必须有真实存在的焦点场景目录（防止写错场景 / init_scene 未执行时静默 mkdir 残缺场景）——写入路径硬性拦截；
        #    gate/audit 预检路径（enforce_scene_dir=False）降为软提示（场景目录由场记阶段3 init_scene 创建·先于批次写入）
        if file_key == "scene_state" and (scene_dir is None or not scene_dir.is_dir()):
            if scene_dir is None:
                msg = "scene_state 落点错误: 无法定位当前焦点场景目录——先确认 world_state.焦点场景 后再写入"
            else:
                msg = f"scene_state 落点错误: 焦点场景目录不存在（{scene_dir}）——先执行 init_scene 创建场景（scene_card/start_snapshot/INDEX ACTIVE）后再写入"
            if enforce_scene_dir:
                hard.append((idx, msg))
            else:
                soft.append((idx, f"{msg}（预检软提示：场景目录将由场记阶段3 init_scene 创建·写入点仍硬性拦截）"))

        # ⑥ 时间线事件写语义提示（软性·不拦截）：world_state.时间线.*.事件 默认 APPEND 追加；
        #    ###KEY 覆盖仅用于 validate 告警后的压缩维护（读旧值+压缩合并+补新）
        if (file_key == "world_state" and len(key_path) >= 3
                and key_path[0] == "时间线" and key_path[-1] == "事件" and not append):
            soft.append((idx, f"{file_key}.{key_path_str}: 时间线事件默认 ###APPEND 追加；###KEY 覆盖仅在 validate 告警后的压缩维护时使用（读旧值+压缩合并+补新）"))

        # ⑦ world_state 键表外字段（软性警告——无语义定义的漂移字段）
        if file_key == "world_state" and key_path:
            WS_TOP_KEYS = {"焦点场景", "轮次", "时间", "外部倒计时", "全局标记", "时间线", "维护名单", "叙事约定"}
            WS_TIME_KEYS = {"基准时间", "具体时间", "时间流速比", "前情描述"}
            if key_path[0] not in WS_TOP_KEYS:
                soft.append((idx, f"world_state.{key_path_str}: 未知顶层键（键表: 焦点场景/轮次/时间/外部倒计时/全局标记/时间线/维护名单/叙事约定）"))
            elif len(key_path) >= 2 and key_path[0] == "时间" and key_path[1] not in WS_TIME_KEYS:
                soft.append((idx, f"world_state.{key_path_str}: 未知时间子键（键表: 基准时间/具体时间/时间流速比/前情描述）"))
            elif len(key_path) >= 2 and key_path[0] == "地点":
                soft.append((idx, f"world_state.{key_path_str}: 地点字段已废弃（当前区域→scene 区域关联·已探索区域→world_map 镜像·请勿再写）"))

        # ⑧ 自主性：枚举合法（硬）+ 升档门槛（硬·变质判定唯一入口）+ 跨级/降档路径（软）
        #    升档唯一入口=loop_machinery §5.3（压力=临界 且 防御=已彻底崩解）；§信念提炼 只产出信念演化·非升级入口
        if file_key.startswith(CHAR_STATE_PREFIX) and key_path == ["自主性"]:
            new_auto = _strip_wrapping_quotes(content)
            if new_auto not in AUTO_ORDER:
                hard.append((idx, f"{file_key}.自主性: 非法值 '{new_auto}'（枚举: 脚本/漂移/觉醒/变质）"))
            else:
                old_data = current.get(file_key, {})
                old_auto = _strip_wrapping_quotes(str(old_data.get("自主性", ""))) if isinstance(old_data, dict) else ""
                if old_auto in AUTO_ORDER and new_auto != old_auto:
                    delta = AUTO_ORDER[new_auto] - AUTO_ORDER[old_auto]
                    if delta > 0:
                        if not force:
                            _p = _batch_preceding(ops, idx, file_key, "压力水平", current)
                            _d = _batch_preceding(ops, idx, file_key, "防御有效性", current)
                            if _p != AUTO_PROMOTE_PRESSURE or _d != AUTO_PROMOTE_DEFENSE:
                                hard.append((idx, f"{file_key}.自主性: 升档 {old_auto}→{new_auto} 未达变质判定门槛（压力水平={_p or '空'}·防御有效性={_d or '空'}）——唯一入口=loop_machinery §5.3（压力={AUTO_PROMOTE_PRESSURE} 且 防御={AUTO_PROMOTE_DEFENSE}）·未达标则重写行为而非升档（低档位出现觉醒级行为=执行越界）；若本批已写压力/防御，须排在自主性之前"))
                        if delta > 1:
                            soft.append((idx, f"{file_key}.自主性: 升档 {old_auto}→{new_auto} 跨级——每次极端冲击只升一级（脚本→漂移→觉醒→变质）"))
                    else:
                        soft.append((idx, f"{file_key}.自主性: 降档 {old_auto}→{new_auto} 非标准（升档唯一入口=§变质判定）——确认是否为显式回退"))

        # ⑬ FILE 归属校验（硬性——防 FILE 标记错位导致字段写入错误文件）
        if key_path:
            if file_key == "conflicts":
                if not key_path[0].startswith("CT-"):
                    hard.append((idx, f"{file_key}.{key_path_str}: conflicts 顶层键必须是 CT-XX（当前 '{key_path[0]}'）——疑似 FILE 标记错位/字段写入错误文件/旧版顶层施压方向残留"))
                elif len(key_path) >= 2:
                    # ⑭ CT 子键白名单（硬性·防编码损坏静默入库）：CT-XX 下仅允许八字段+事件线引用+施压方向（+存量归档标记）
                    #   实测案例：PowerShell 管道把中文键损坏成 `????` → 被当新键静默创建；白名单使此类损坏当场爆炸
                    CT_SUB_KEYS = {"描述", "对抗双方", "被争夺资源", "关联角色", "相位", "紧迫度", "事件线引用", "状态", PRESSURE_KEY, "上轮结算"}
                    if key_path[1] == "上轮结算":
                        if len(key_path) != 3 or key_path[2] not in ("关系状态", "内部状态"):
                            hard.append((idx, f"{file_key}.{key_path_str}: 上轮结算子键仅允许 关系状态/内部状态（当前 '{'/'.join(key_path[2:])}'）"))
                    elif key_path[1] not in CT_SUB_KEYS:
                        hard.append((idx, f"{file_key}.{key_path_str}: CT 子键 '{key_path[1]}' 不在键表（描述/对抗双方/被争夺资源/关联角色/相位/紧迫度/事件线引用/状态/上轮结算）——疑似编码损坏或字段漂移"))
                    # ⑮ CT 列表字段类型守卫（硬性·A）：关联角色/事件线引用 是 YAML 列表——只接受多行列表文本（逐行 '- 名字' / '[]'）的 KEY 全量覆盖；
                    #   单行文本会被当字符串覆盖整个列表（类型损坏）；###APPEND 对这两字段无安全追加路径（禁用）
                    elif key_path[1] in ("关联角色", "事件线引用"):
                        if append:
                            hard.append((idx, f"{file_key}.{key_path_str}: 禁用 ###APPEND（通用追加通道会把列表写成字符串）——用 ###KEY 全量覆盖为完整 YAML 列表（含保留项+新增项）"))
                        else:
                            try:
                                _items = yaml.safe_load(content)
                            except Exception:
                                _items = None
                            if not isinstance(_items, list):
                                hard.append((idx, f"{file_key}.{key_path_str}: 内容必须为多行 YAML 列表（逐行 '- 名字'）——单行文本会把列表覆盖成字符串（类型损坏）"))
                            # 软性（B·档案对账）：名单与 characters/CHAR_*.md 无唯一匹配 → 警告核对拼写（不拦·防跨世界命名差异误伤）
                            elif key_path[1] == "关联角色":
                                _chars_dir = world_dir / "characters"
                                if _chars_dir.is_dir():
                                    _stems = [p.stem[len("CHAR_"):] for p in sorted(_chars_dir.glob("CHAR_*.md"))]
                                    for _nm in dict.fromkeys(str(it).strip() for it in _items if str(it).strip()):
                                        if _nm in _stems:
                                            continue
                                        _hits = [s for s in _stems if _nm in s or s in _nm]
                                        if len(_hits) != 1:
                                            soft.append((idx, f"{file_key}.{key_path_str}: '{_nm}' 与 characters/ 档案无唯一匹配（{'候选: ' + '/'.join(_hits[:3]) if _hits else '无候选'}）——核对角色名拼写"))
            elif file_key.startswith(CHAR_STATE_PREFIX):
                CHAR_STATE_KEYS = {"自主性", "位置", "已知地点", "核心状态", "情绪", "压力水平", "防御有效性", "防御形态", "崩溃表现", "偏离登记", "人际动态", "decision", "信念演化", "记忆锚点", "连续行动轨迹", "名字", "性别", "健康", "妆扮", "服饰", "随身物品"}
                if key_path[0] not in CHAR_STATE_KEYS:
                    hard.append((idx, f"{file_key}.{key_path_str}: CHAR_state 顶层键必须在键表内（当前 '{key_path[0]}'）——疑似 FILE 标记错位/字段写入错误文件"))
            elif file_key == "scene_state":
                SCENE_STATE_KEYS = {"核心状态", "场景时间线", "物理锚点", "道具", "关键场景信息", "出场角色摘要"}
                if key_path[0] not in SCENE_STATE_KEYS:
                    hard.append((idx, f"{file_key}.{key_path_str}: scene_state 顶层键必须在键表内（当前 '{key_path[0]}'）——疑似 FILE 标记错位/字段写入错误文件"))
            elif file_key == "direction":
                if key_path[0] not in DIRECTION_KEYS:
                    hard.append((idx, f"{file_key}.{key_path_str}: direction 顶层键必须在键表内（当前 '{key_path[0]}'·键表: {'/'.join(sorted(DIRECTION_KEYS))}）——疑似 FILE 标记错位/防镜像（焦点场景/CT紧迫度/拍序不得复制）"))
            elif file_key == "storylines":
                if key_path[0] not in STORYLINES_TOP_KEYS:
                    hard.append((idx, f"{file_key}.{key_path_str}: storylines 顶层键必须在键表内（当前 '{key_path[0]}'·键表: 故事弧线/事件线）——事件线读写走 ###STORYLINE（②编剧）"))

        # ⑬b 轨迹覆盖写检测（硬性——防覆盖写丢失历史：覆盖写必须保留旧值首末轮次标记·连续行动轨迹由脚本按窗口裁剪·禁手动删块）
        # 重置豁免：该角色已登记重置（world_state.维护名单.{角色}）→ 按 loop_machinery §4 联动表清空/压缩重建，不拦
        if (file_key.startswith(CHAR_STATE_PREFIX) and key_path and key_path[0] == "连续行动轨迹"
                and len(key_path) == 1 and not append and not force):
            _fp_r, _ = resolve_char_file(existing, file_key, world_dir)
            if _fp_r is not None:
                _stem = _fp_r.stem[len(CHAR_STATE_PREFIX):]
                if _stem.endswith("_state"):
                    _stem = _stem[:-len("_state")]
                if _stem in reset_chars:
                    continue
            old_val = (current.get(file_key, {}) or {}).get(key_path[0], "")
            if isinstance(old_val, str) and old_val.strip():
                old_marks = re.findall(r"第\s*\d+\s*轮\(", old_val)
                if old_marks:
                    first, last = old_marks[0], old_marks[-1]
                    if first not in content or last not in content:
                        hard.append((idx, f"{file_key}.{key_path[0]}: 覆盖写丢失历史——新内容必须保留旧值首末轮次标记（{first}…/{last}…）·窗口/压缩由机制执行·禁止手动删块"))

    # ① 行动卡三件套 + ①b 有条件代价可核验 + ⑨ 角色档案存在（硬性·###ACTION——④角色阶段产物）
    COST_BLACKLIST = ("幻想", "安全感", "预期", "确定性", "耐性", "错觉", "安宁", "掌控感", "主动权", "节奏", "局面", "从容")
    for a_line in action_lines:
        a_show = a_line[:60]
        for token in ("驱动:", "情绪:", "强度:"):
            if token not in a_line:
                hard.append((-1, f"###ACTION 缺「{token}」: {a_show}"))
                break
        # 有条件代价：过渡/寒暄轮可豁免（软警），推进轮必填（硬拦由 phase_actor 条件判定，此处仅软提示）
        if "代价:" not in a_line:
            soft.append((-1, f"###ACTION 未含「代价:」——推进性行动（关联CT∈推进池且施压方向∈四爆破或当前拍为资源/关系/控制权/认知类问题）应含代价，其余过渡豁免: {a_show}"))
        m = re.search(r"代价:\s*(\S+)", a_line)
        if m and not m.group(1).strip():
            hard.append((-1, f"###ACTION 代价: 后为空（任一方无变化=本轮无冲突）: {a_show}"))
        cost_m = re.search(r"代价:\s*(.+?)(?:\s*\|\s*耗时:|$)", a_line)
        if cost_m:
            braces = re.findall(r"\{([^}]*)\}", cost_m.group(1))
            hit = [w for w in COST_BLACKLIST if any(w in b for b in braces)]
            if hit:
                hard.append((-1, f"###ACTION 代价含不可核验抽象词 {hit}——内部认知/无载体抽象词不算可核验变化（可核验枚举: 资源易主/载体状态变化/新增伤害/控制权易手/被迫选择/被迫承认/关系档位变化）: {a_show}"))
        rm = re.match(r"^\s*([^:|]+)[:：]", a_line)
        if rm:
            char_name = rm.group(1).strip()
            md_fp = world_dir / "characters" / f"CHAR_{char_name}.md"
            state_fp = world_dir / "states" / f"CHAR_{char_name}_state.yaml"
            if char_name and not md_fp.exists() and not state_fp.exists():
                resolved = None
                try:
                    for fp in world_dir.glob("characters/CHAR_*.md"):
                        full = fp.stem[len("CHAR_"):]
                        if char_name in full or full in char_name or full.replace(" ", "") == char_name.replace(" ", ""):
                            resolved = full
                            break
                except Exception:
                    pass
                if resolved:
                    soft.append((-1, f"###ACTION 角色 '{char_name}' 是简称，档案全名为 '{resolved}'——请用全名"))
                else:
                    hard.append((-1, f"###ACTION 角色 '{char_name}' 无档案（缺 CHAR_{char_name}.md——档案缺失=禁止该角色行动；若为简称请用档案全名）"))

    # ⑩⑪⑫ 阶段必含项（软性·查询轮/轻量豁免；gate <阶段> --check 升级为硬拦）
    if not maintenance and ops and stage == "戏剧家":
        if not has_ct_op:
            soft.append((-1, "戏剧家批应含 ≥1 条 CT 推进/注册（conflicts.CT-XX）——查询轮豁免"))
        # 施压方向每轮核验（逐 CT·跟随推进池）：本批推进的每条 CT → 必写 CT-XX.施压方向
        #   余波已兑现批豁免（phase_dramatist D11 前置分支「余波只结算·不施压」）：该批只写结算字段
        #   （上轮结算/紧迫度/相位）而必写施压方向，故 当前拍==余波 时不要求此软警；
        #   「未兑现」余波由停滞旗标区分——停滞硬拦不依赖本豁免（见下）。
        _dr = _load_direction(world_dir)
        _dram_beat = str(_dr.get("当前拍", "") or "").strip()
        _press_writes = {}
        _touched_cts = set()
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or _file_key.strip().lower() != "conflicts":
                continue
            _kp = str(_key_path).strip().split(".")
            _top = _kp[0]
            if not _top.startswith("CT-"):
                continue
            _touched_cts.add(_top)
            if len(_kp) == 2 and _kp[1] == PRESSURE_KEY:
                _pv = str(_content).strip()
                _pe, _pd = _split_pressure(_pv)
                if _pe and _pe not in PRESSURE_ENUM:
                    hard.append((-1, f"conflicts.{_top}.{PRESSURE_KEY} '{_pv}' 非法（枚举: {'/'.join(PRESSURE_ENUM)}）"))
                else:
                    _press_writes[_top] = _pe
                    if _pe and _pe != PRESSURE_HOLD and not _pd:
                        soft.append((-1, f"conflicts.{_top}.{PRESSURE_KEY}: 四爆破方向'{_pe}'缺少压力说明——补写‘压力来源+受力点+转变方向’"))
        _missing_press = sorted(_touched_cts - set(_press_writes))
        if _dram_beat != "余波":
            if has_ct_op and not _press_writes:
                soft.append((-1, f"戏剧家批应含 CT-XX.{PRESSURE_KEY}（每轮·跟随推进池——四爆破方向四选一/维持）"))
            elif _missing_press:
                soft.append((-1, f"戏剧家批推进了 {'、'.join(_missing_press)} 但未标 {PRESSURE_KEY}——推进池每条 CT 须带 CT-XX.{PRESSURE_KEY}"))
        # 停滞旗标消费核验：旗标在场 → 本批必须写 CT 施压方向 且至少一条 ≠维持（加压兑现）
        _flags = _dr.get("escalation_flags")
        if isinstance(_flags, dict) and any("停滞" in str(k) and _flag_active(v) for k, v in _flags.items()):
            if not _press_writes:
                hard.append((-1, f"direction.escalation_flags.停滞 在场——本批必须写 CT-XX.{PRESSURE_KEY}（四爆破方向四选一·加压兑现·停滞旗标当轮消化）"))
            elif all(v == PRESSURE_HOLD for v in _press_writes.values()):
                hard.append((-1, f"direction.escalation_flags.停滞 在场而施压方向全为{PRESSURE_HOLD}——停滞轮禁全维持（四爆破方向四选一）"))
            else:
                # 加压载体核验（phase_dramatist D9/D11 载体登记）：施压方向说明是元层瞄准·④角色只感知已登记载体
                #   → 新变量同批登记认知层载体：CT.关联角色（①唯一可写通道·新主体与威胁/事件类皆由 CT 承载）。
                #     需 world_state.外部倒计时 时①只指定·落盘=⑤场记（写入矩阵 world_state 归⑤）——故本处不认 world_state op。
                _has_carrier = any(
                    _kind == "write"
                    and _file_key.strip().lower() == "conflicts"
                    and str(_key_path).strip().split(".")[0].startswith("CT-")
                    and str(_key_path).strip().split(".", 1)[-1] == "关联角色"
                    for _kind, _file_key, _key_path, _content, _append in ops
                )
                if not _has_carrier:
                    hard.append((-1, "direction.escalation_flags.停滞 在场——加压批须含新变量载体（###FILE: conflicts + ###KEY CT-XX.关联角色 登记新主体/威胁事件类·由③调度单入场承载）——施压方向说明仅是瞄准·④角色只感知已登记载体"))
        # v0.28 CT待结算旗标消费核验：旗标在场 → 本批必须含 conflicts CT op（结算/重估·推进池重估紧迫度）
        if isinstance(_flags, dict) and any("CT待结算" in str(k) and _flag_active(v) for k, v in _flags.items()):
            if not any(
                _kind == "write" and _file_key.strip().lower() == "conflicts"
                and str(_key_path).strip().split(".")[0].startswith("CT-")
                for _kind, _file_key, _key_path, _content, _append in ops
            ):
                hard.append((-1, "direction.escalation_flags.CT待结算 在场——①戏剧家本批必须含 conflicts CT op（结算/重估·推进池重估紧迫度）"))
        # 循环轨道硬拦（只限循环世界·loop_machinery §1 步骤1-2）：循环世界每个 ①戏剧家批
        #     → META 压力扫描必须含「轨道✓(角色=在轨/偏离·离岗/已回归)」逐角色结论。
        #     §1 明写「每轮必查·不依赖主路是否已有 CT 推进」——故此处不挂钩 has_ct_op。
        #     缺=本层未扫描→偏离检测可被静默合并进 CT 状态更新而无显式在轨/偏离/回归判定（审计 C2/C3/A2/A3）。
        _loop_keys = _loop_char_keys(world_dir)
        if _loop_keys and not force:      # --force 显式逃生口（与 ④/⑬b/A0 同款）
            # 逐角色覆盖率核验（scoped 版·名单与 precheck §1b / _loop_relevant_roles 同源闭环）：
            #   轨道✓(...) 必须逐一覆盖「调度单点名循环角色 ∪ 当前焦点区 REGION 常驻NPC ∪ §1a互锁涉及角色」——
            #   缺任一名 = 本层未扫描。（vs 旧版仅验格式存在——12 循环角色只写 1 个也能过·现为机检漏洞）
            _track_meta = " ".join(str(m) for m in meta_lines)
            _track_exprs = re.findall(r"轨道✓\s*\(([^)]*)\)", _track_meta)
            _tracked = set()
            for _expr in _track_exprs:
                for _tok in re.split(r"[/|,;；]", _expr):
                    _m = re.match(r"^\s*([^=]+)=", _tok)
                    if _m:
                        _ln = _canonical_role_label(_m.group(1).strip(), world_dir, existing)
                        if _ln:
                            _tracked.add(_ln)
            _required = _loop_relevant_roles(world_dir)
            _missing = sorted(_required - _tracked)
            if _missing:
                hard.append((-1, f"循环世界 ①戏剧家批——META 压力扫描「轨道✓(...)」逐角色结论未覆盖: {'/'.join(_missing)}（必须覆盖: {'/'.join(sorted(_required))}——范围=调度单点名循环角色 ∪ 当前焦点区 REGION 常驻NPC ∪ §1a互锁涉及角色·即本轮相关循环角色；缺名=本层未扫描→偏离检测可被静默合并进 CT 状态更新（phase_dramatist D7 轨道判定 + 写入节轨道✓；loop_machinery §1: 循环轨道每轮必查·不依赖主路是否已有 CT 推进）。裸勾/只写「无偏离」/只写部分角色=本层未扫描·--force 豁免。格式: 轨道✓(全名=在轨|偏离·离岗|已回归·以 / , ; ； 任一分隔·每项必须含 =)）"))
        # 压力扫描逐源覆盖核验（D8 逐源快判·十源＋爆破源）：META 压力扫描须逐源表态——
        #   把十源写成"任一命中即注册"的一条标准会让 LLM 只扫到最显眼的那个、其余静默跳过
        #   （与 轨道✓ 同款覆盖率问题）→ 每源必须在 META 里有 ✓/— 表态。--force 显式逃生口。
        if ops and not force:
            _scan_meta = " ".join(str(m) for m in meta_lines)
            _scan_sources = ("人际", "目标", "资源", "轨道", "跨叙事", "时间", "环境", "法则", "扩散", "兜底", "爆破源")
            _scan_missing = [s for s in _scan_sources
                             if not re.search(rf"{s}\s*[✓✔√×✗—\-－]", _scan_meta)]
            if _scan_missing:
                hard.append((-1, f"①戏剧家批——META 压力扫描未逐源表态，缺: {'/'.join(_scan_missing)}（十源＋爆破源：人际/目标/资源/轨道/跨叙事/时间/环境/法则/扩散/兜底/爆破源·每源写 `源名✓` 或 `源名—`）——缺源=本层未扫描→该压力源可被静默跳过（phase_dramatist D8 逐源快判；--force 豁免）"))
    elif not maintenance and ops and stage == "场记":
        # 轮次+1 豁免：跨场景轮入场帧批（META 标「同轮续批」且本批确写场景时间线）——轮次已由旧场景收尾批推进
        # 同轮续批（跨场景轮入场帧批）：世界三件套已由旧场景收尾批推进·入场帧不含场景时间线
        # （scene_management §跨场景轮落盘顺序/§场景切换流程第4步唯一定义）→ 四项必含全部豁免
        _continue_round = any("同轮续批" in str(m) for m in meta_lines)
        for flag, msg in ((has_ws_time or _continue_round, "场记批应含 world_state.时间.具体时间 推进"),
                          (has_ws_round or _continue_round, "场记批应含 world_state.轮次 +1"),
                          (has_ws_summary or _continue_round, "场记批应含 world_state.前情描述（≤100字状态短语）"),
                          (has_scene_timeline or _continue_round, "场记批应含 scene_state.场景时间线 追加")):
            if not flag:
                soft.append((-1, msg + "——查询轮豁免"))
        # 场景基线 cast 覆盖硬拦（转场/新场景入画·与 precheck 义务区同源 _scene_cast_baseline）
        #   触发（任一）：① direction.转场.目标场景 非空；② 本批写 scene_card；
        #   ③ 入场帧批——本批写 scene_state.场景时间线 且盘上该字段为空（场景创建后/重置后首条剧情
        #      落盘时刻）。scene_card 由场记在 init_scene 后批外手写（不在任何批次里），导演未写
        #      转场.目标场景而由场记自行检测切换（scene_management 流程第1步）时，①②均不命中——
        #      唯一可闸的时刻就是入场帧批：此时 init_scene 已切焦点，基线取盘上焦点场景即新场景。
        #   常驻NPC 只取按当前时刻时间线命中本场者（NPC 会动·别处不硬套）；时间线命中别处者不构成缺失。
        #   跨场景轮豁免（旧场景收尾批）：direction.转场.目标场景 已指向新场景（对账基线属新场景）且
        #   当前焦点场景 ID 不在目标中 → 本批是旧场景收尾，跳过 cast 硬拦——切场景后的入场帧批照常核。
        _keeper_trans = _map_field(_load_direction(world_dir).get("转场"))
        _keeper_target = _keeper_trans.get("目标场景") or None
        _writes_scene_card = any(
            _kind == "write" and "scene_card" in str(_file_key) for _kind, _file_key, _kp, _c, _a in ops
        )
        _ws_cur = current.get("world_state") or {}
        _focus_id = re.sub(r"\s+", "", str(_ws_cur.get("焦点场景", "") or "")) if isinstance(_ws_cur, dict) else ""
        _target_norm = re.sub(r"\s+", "", str(_keeper_target or ""))
        _old_scene_closing = bool(_keeper_target) and bool(_focus_id) and (_focus_id not in _target_norm)
        # 入场帧批：本批写 scene_state 且盘上场景时间线为空（场景创建/重置后首次落盘时刻——
        # 入场帧按 scene_management 只记锚点/道具/出场摘要·不记时间线，故不得以「本批写时间线」为触发）
        _writes_scene_state = any(
            _kind == "write" and str(_file_key).strip().lower() == "scene_state"
            for _kind, _file_key, _kp, _c, _a in ops
        )
        _entry_frame = _writes_scene_state and not (current.get("scene_state") or {}).get("场景时间线")
        if not _old_scene_closing and (_keeper_target or _writes_scene_card or _entry_frame):
            _bl = _scene_cast_baseline(world_dir)
            _miss = _cast_overlap_missing(world_dir, _bl)
            if _miss:
                hard.append((-1, f"场景基线 cast 覆盖：本场景应出现角色未入 cast（缺: {'/'.join(_miss)}）——常驻NPC 按当前时刻时间线命中本场者须入『出场角色』(焦内) 或『焦外/在场』(焦外)·时间线命中别处者按 REGION 静态归属复核（见 scene_management 场景切换流程第6步）"))
    elif not maintenance and stage == "编剧":
        _sl_map = (_load_storylines(world_dir).get(STORYLINE_TOP_KEY) or {})
        _dr_sl = _load_direction(world_dir)
        try:
            _cd = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
        except Exception:
            _cd = {}
        # 本层必含项判定：
        #   A. D4 建线决策·合并触发（机械标准·独立于语义评估）：未引用活跃线 CT 且无活跃线可接 → 必含 add
        #      （判据见 _storyliner_unref_and_must_add·与 precheck 同源）
        #   B. D2 不承接归位：不承接 flag 在场 → 必含 add/rewrite/clear（三问定原线去向）
        #   C. D1 弧线定位：本批必含 故事弧线 落盘
        _must_add, _unref_ct, _active_sl = _storyliner_unref_and_must_add(_sl_map, _dr_sl, _cd)
        _has_structure_action = bool(storyline_lines)
        _has_arc_write = any(
            _k == "write" and str(_fk).strip().lower() == "storylines"
            and str(_kp).strip().startswith("故事弧线")
            for _k, _fk, _kp, _c, _a in ops
        )
        if _must_add and not _has_structure_action:
            hard.append((-1, "编剧批——D4 合并触发（无活跃线可接当前叙事）：conflicts 存在未引用活跃线的 CT（"
                             f"{'/'.join(_unref_ct)}）而 {'无活跃线' if not _active_sl else '当前拍=余波已兑现且无其他非余波活跃线可接'}——"
                             "必含 ###STORYLINE: add（每轮至多取一条·未引用CT包括已收束线引用；空表由 round-check 兜底）"))
        # D5 取材核验（有add时）：META须回显取材=CT-XX（或场景兜底），且该CT未命中活跃线
        _has_add = any(str(a or "").strip().split()[:1] == ["add"] for a, _p in storyline_lines)
        if _has_add:
            _cited = []
            for _m in meta_lines:
                _cited += re.findall(r"取材\s*=\s*(CT-\d+)", str(_m))
            _cited_fallback = any("取材=场景兜底" in str(_m) for _m in meta_lines)
            if not _cited and not _cited_fallback:
                hard.append((-1, "编剧批——含###STORYLINE: add须META回显取材来源（缺=拦·D5 取材）：`取材=CT-XX`；扫描零合格者写 `取材=场景兜底`"))
            else:
                for _ct in _cited:
                    _cv = _cd.get(_ct) if isinstance(_cd, dict) else None
                    if isinstance(_cv, dict):
                        _refs = _cv.get("事件线引用") or []
                        if not isinstance(_refs, list):
                            _refs = [str(_refs)]
                        _hits = {re.sub(r"\s+", "", str(r).strip()) for r in _refs if str(r).strip()}
                        _norm_active = {re.sub(r"\s+", "", str(a).strip()) for a in _active_sl}
                        if _hits & _norm_active:
                            hard.append((-1, f"编剧批——取材{_ct}当前被活跃线承载（{','.join(sorted(_hits & _norm_active))}）·取即违规（D5 取材资格·取材须未引用）"))
        # D2 触发：不承接 flag 在场
        _flags_sl = _dr_sl.get("escalation_flags") or {}
        if isinstance(_flags_sl, dict) and any("不承接" in str(k) and _flag_active(v) for k, v in _flags_sl.items()):
            if not _has_structure_action:
                hard.append((-1, "编剧批——direction.escalation_flags.不承接 在场（上轮原计划失效）：必含 ###STORYLINE: add/rewrite/clear 三问定原线去向（phase_storyliner D2 不承接归位）"))
        # D1 弧线定位：本批必含落盘
        if not _has_arc_write:
            hard.append((-1, "编剧批——必含 D1 弧线定位落盘（###KEY: 故事弧线.当前幕 / .张力基调 / .节点落位.*）"))
    elif not maintenance and stage == "导演":
        _dr = _load_direction(world_dir)
        # v0.29 取消「复用」：③每轮必写 direction——guidance 与 调度单 逐轮落盘（内容未变也照写）
        _writes_guidance = any(
            _kind == "write" and _file_key.strip().lower() == "direction" and "guidance" in _key_path.lower()
            for _kind, _file_key, _key_path, _content, _append in ops
        )
        _writes_schedule = any(
            _kind == "write" and _file_key.strip().lower() == "direction" and "调度单" in _key_path.lower()
            for _kind, _file_key, _key_path, _content, _append in ops
        )
        if not str(_dr.get("guidance", "") or "").strip() and not _writes_guidance:
            hard.append((-1, "direction.guidance 为空且批次未写 guidance——③导演每轮必写 guidance/调度单（取消复用）"))
        if not str(_dr.get("调度单", "") or "").strip() and not _writes_schedule:
            hard.append((-1, "direction.调度单 为空且批次未写 调度单——③导演每轮必写 guidance/调度单（取消复用）"))
        if ops and not beat_lines and not any("回判" in m for m in meta_lines):
            soft.append((-1, "导演批应含 ###BEAT: 动作（set/deepen/advance）或 META 回判留痕"))
        # 连续同拍核验（窗口感知·v0.29）：上轮落盘 节拍决策=继续当前拍 且 本批仍写「继续当前拍」→ 同拍
        # 判据只读 节拍决策 字段（指针不动=同拍）·不挂 ###BEAT 动作行——避免以省略动作行绕开停滞加压
        # 窗口已耗尽 → 必须明确表态：advance（不再继续）/ 停滞旗标 / 续演（批内重设 时间窗口=追加拍级预算）
        # 窗口未耗尽 → 软警（窗口=拍发育期·默认 deepen·验收点=窗口耗尽）；窗口状态不可判定（缺起点/格式未解析）→ 按未耗尽处理·不拦（补起点归③本批·回判兜底归 phase_director D2/D4）
        # 豁免：本批 演出状态∈{上升,转折} 视为推进中同拍（替代兑现可写）不拦；措辞不匹配=静默放过·退化为 phase_director 规则兜底·不误拦
        _prev_same_beat = str(_dr.get("节拍决策", "") or "").strip().startswith("继续当前拍")
        _cur_decision = ""
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind == "write" and _file_key.strip().lower() == "direction" \
                    and _key_path.strip().lower() == "节拍决策":
                _cur_decision = str(_content).strip()
        if _prev_same_beat and _cur_decision.startswith("继续当前拍"):
            _is_progressing = any(
                _kind == "write" and _file_key.strip().lower() == "direction"
                and _key_path.strip().lower() == "演出状态"
                and str(_content).strip() in ("上升", "转折")
                for _kind, _file_key, _key_path, _content, _append in ops
            )
            _flag_stall = any(
                _kind == "write" and _file_key.strip().lower() == "direction"
                and "escalation_flags" in _key_path
                and ("停滞" in _key_path or "停滞" in _content)
                for _kind, _file_key, _key_path, _content, _append in ops
            )
            _rewrites_window = any(
                _kind == "write" and _file_key.strip().lower() == "direction"
                and ("时间窗口" in _key_path or "时间窗口" in str(_content))
                for _kind, _file_key, _key_path, _content, _append in ops
            )
            _bm, _el, _re, _exh = _window_status(world_dir)
            # 「已过半」=剩余≤预算一半（与 phase_director D2/D6 同口径·首次验收点）
            _half = (_re is not None and _bm is not None and _re <= (_bm / 2.0))
            if _exh is True:
                if not (_is_progressing or _flag_stall or _rewrites_window):
                    hard.append((-1, "窗口已耗尽仍连续同拍（上轮与本批 节拍决策 均=继续当前拍）——本批必须明确表态：advance（推进下一拍）/ escalation_flags.停滞=待加压 / 续演（批内重设 时间窗口·起点=当前世界时间·新拍级预算）"))
            elif _exh is False and _half:
                # 首个验收点（过半）：不硬拦——停滞判据含语义裁量（意图能否明显逼近问题·phase_director D2）·脚本不代判；
                # 但必须把验收点推到③面前，避免其滑到重设窗口把停滞判定从中间抹掉。
                _msg_half = (f"连续同拍·窗口已过半（剩余≈{_re}分钟／预算{_bm}分钟）——首个验收点·"
                             f"③须先判停滞标准（phase_director D2）：意图仍能明显逼近本拍问题→续演（过半不重设窗口）；"
                             f"不能明显逼近→escalation_flags.停滞（①加压·引入或推进非玩家爆破）")
                if not any(isinstance(s, tuple) and len(s) > 1 and str(s[1]).startswith("连续同拍·窗口已过半") for s in soft):
                    soft.append((-1, _msg_half))
            elif _exh is False:
                _msg_soft = f"连续同拍·窗口未过半（剩余≈{_re}分钟／预算{_bm}分钟）——窗口=拍发育期·默认 deepen"
                if not any(isinstance(s, tuple) and len(s) > 1 and str(s[1]).startswith("连续同拍·窗口未过半") for s in soft):
                    soft.append((-1, _msg_soft))
            else:
                _msg_soft = f"连续同拍·窗口状态不可判定（缺起点或时间格式未解析）——按未耗尽处理·③下批补设窗口{{起点,预算}}"
                if not any(isinstance(s, tuple) and len(s) > 1 and str(s[1]).startswith("连续同拍·窗口状态不可判定") for s in soft):
                    soft.append((-1, _msg_soft))
        # 调度单点名角色档案核验（软警告·防具名新角色无档案漂移到演员层才暴露）
        _sched_text = " ".join(
            str(_content) for _kind, _file_key, _key_path, _content, _append in ops
            if _kind == "write" and _file_key.strip().lower() == "direction" and "调度单" in _key_path
        )
        if not _sched_text:
            _sched_text = _direction_schedule_text(world_dir)
        _sched_buckets = _schedule_roles_by_bucket(world_dir, _sched_text)
        _active_cast = _sched_buckets["焦内活跃"]
        for _hint in _schedule_substring_hints(world_dir, _sched_text):
            soft.append((-1, f"调度单{_hint}"))
        if not _active_cast:
            hard.append((-1, "导演批调度单缺焦内活跃具名角色——焦内活跃是本拍行动主体，背景角色不得替代"))
        elif len(_active_cast) > 3:
            soft.append((-1, f"导演批焦内活跃超3个（当前 {len(_active_cast)}: {'/'.join(sorted(_active_cast))}）——请确认承接判断已显式主次排序·单轮链成本自负"))
        # 四层调度单具名核验（背景角色/焦外/焦外→焦内 段——虚词不得替代已建档角色）
        # 正向规则见 phase_director D5：调度单一律写具名条目；仅无 CHAR_.md 的纯背景可标群像。
        VAGUE = ("群像", "外部者", "游客", "守卫", "群众", "背景", "背景角色", "路人", "纯背景")
        _known_char = set()
        for _cfp in world_dir.glob("characters/CHAR_*.md"):
            _nm = _cfp.stem[len("CHAR_"):].strip().replace("_state", "").strip()
            if _nm:
                _known_char.add(_nm)
        for _bucket in ("背景角色", "焦外", "焦外→焦内"):
            _body = _schedule_body_text(_sched_text, _bucket)
            if _body and _body.lower() not in ("无", "none"):
                for _seg in _split_schedule_segments(_body):
                    _s = _seg.strip().lstrip("-")
                    if not _s:
                        continue
                    # 虚词段：仅当该段确实无对应档案角色才放行；含已建档角色名 → 视为替代违例
                    if any(v in _s for v in VAGUE):
                        # 检查虚词段内是否偷偷带着已建档角色（如「群像(Dolores)」）
                        _named_in_vague = any(
                            _norm_char_key(n) in _norm_char_key(_s) for n in _known_char
                        )
                        if _named_in_vague:
                            hard.append((-1, f"调度单 {_bucket} 段‘{_s}’用虚词（群像/外部者等）替代已建档角色——须写具名 CHAR_ 条目（仅无 CHAR_.md 的纯背景可标群像）"))
                        continue
                    # 具名段：可归一到已知档案才放行；不可解析（既非已知角色亦非纯背景名）→ 软警告
                    if _canonical_role_label(_s, world_dir, existing) is None:
                        soft.append((-1, f"调度单 {_bucket} 段‘{_s}’无法归一为已建档角色名——确认是具名条目（可解析）还是纯背景虚词"))
        # 焦外→焦内 过渡桶：角色必须在该轮落到「焦内活跃」或「背景角色」最终桶（完成状态更新）
        _transit = _sched_buckets.get("焦外→焦内") or set()
        if _transit:
            _final = (_sched_buckets.get("焦内活跃") or set()) | (_sched_buckets.get("背景角色") or set())
            _unlanded = _transit - _final
            if _unlanded:
                hard.append((-1, f"调度单 焦外→焦内 角色未落到最终桶（焦内活跃/背景角色）·状态更新无法完成: {'/'.join(sorted(_unlanded))}——过渡桶须本轮完成迁移"))
        if any(str(line).startswith("deepen") for line in beat_lines):
            _writes_handoff = any(
                _kind == "write" and _file_key.strip().lower() == "direction"
                and _key_path.strip().lower() == "承接判断"
                and "未完成意图" in str(_content)
                for _kind, _file_key, _key_path, _content, _append in ops
            )
            if not _writes_handoff:
                hard.append((-1, "导演批 deepen 必须在 direction.承接判断 点名调度单各角色的「未完成意图」及待改变状态——姿态/情绪/走位不是承接理由"))
            # 承接判断 体量失忆探针（与 MUSE/叙事 探针同构·阈值只存常量不对外）：
            #   本批确实写了承接判断、却体量不足 → 疑似未走回判评估（写了字但没做判断）。
            #   最小批（_daily_reuse）不重写该字段·天然豁免。
            _handoff_text = "".join(
                str(_content) for _kind, _file_key, _key_path, _content, _append in ops
                if _kind == "write" and _file_key.strip().lower() == "direction"
                and _key_path.strip().lower() == "承接判断"
            )
            _hcc = len(re.sub(r"\s+", "", _handoff_text))
            if _handoff_text.strip() and _hcc < _DIRECTOR_MIN_CHARS:
                hard.append((-1, f"导演批 承接判断 仅 ≈{_hcc} 字，低于 token 下限——疑似未走回判（失忆）：先重读 references/phase_director.md，再重做③。本段未落盘。"))
        for _name in _unarchived_named_roles(world_dir):
            if _name in _sched_text:
                soft.append((-1, f"调度单点名具名角色 '{_name}' 无档案（缺 CHAR_{_name}.md）——补注册建档（精简档即可）或降级为无名群像/纯外压（①戏剧家兜底新角色建档义务·见 phase_dramatist D8·源⑩兜底）"))
    elif not maintenance and stage == "角色":
        _char_writes = sum(
            1 for _kind, _file_key, _key_path, _content, _append in ops
            if _kind == "write" and _file_key.startswith(CHAR_STATE_PREFIX) and _file_key.endswith("_state")
        )
        if not action_lines and not _char_writes:
            hard.append((-1, "角色批既无 ###ACTION 行动卡也未更新任何 CHAR_state——④角色层零产出（焦内活跃角色即兴/焦外自推演至少落其一）"))
        elif ops and not action_lines and has_char_op:
            soft.append((-1, "角色批应含 ≥1 条 ###ACTION 行动卡（焦内活跃角色逐一即兴）"))
        _active_roles = _schedule_roles_by_bucket(world_dir)["焦内活跃"]
        _action_roles_canonical = {
            _canonical_role_label(role, world_dir, existing) for role in _action_roles(action_lines)
        }
        # 用户角色（POV）缺 ACTION 豁免：第二人称无指令可无决策无行动·不代笔（见 phase_actor POV 路径）；
        # A4 人工核授权（行动卡 vs 用户本轮输入逐条核对）不受影响·仍执行。
        _pov_roles = _pov_role_names(world_dir, existing)
        _pov_norm = {_norm_char_key(p) for p in _pov_roles}
        _missing_active_actions = {a for a in _active_roles - _action_roles_canonical
                                   if _norm_char_key(a) not in _pov_norm}
        if _missing_active_actions:
            hard.append((-1, f"焦内活跃角色必须各自产 ACTION 并进入行动链，缺: {sorted(_missing_active_actions)}"))

        # ⑬e 执行绑定声明（硬性·phase_actor 执行绑定 Step 0）：每个 ###ACTION 行动角色须在 META
        #     声明绑定路径——`绑定: Name=子agent,Other=单窗口(豁免原因)`。缺声明=拦截（执行绑定
        #     无锚点即静默兜底）；裸 `单窗口` 无豁免原因=拦截；非 POV 角色标 单窗口(原因) → 软警核豁免依据。
        _binding = {
            _canonical_role_label(role, world_dir, existing): status
            for role, status in _parse_role_binding(meta_lines).items()
        }
        for _role_b in sorted(_action_roles_canonical):
            _status_b = _binding.get(_role_b)
            if _status_b is None:
                hard.append((-1, f"###META 绑定声明缺行动角色: {_role_b}（格式 `绑定: Name=子agent,Other=单窗口(豁免原因)`·phase_actor 执行绑定 Step 0）"))
            elif _status_b.startswith("子agent") and "(组装✓)" not in _status_b:
                hard.append((-1, f"角色 {_role_b} 子agent 绑定缺组装自查标记（应为 `子agent(组装✓)`·派发前按 references/subagent_prompt.md「派发自查」逐项核对留痕·phase_actor 组装通道）"))
            elif _status_b == "单窗口" or (_status_b.startswith("单窗口") and not _status_b.startswith("单窗口(")):
                hard.append((-1, f"角色 {_role_b} 绑定声明为裸 `单窗口`——缺豁免原因；宿主具备子 agent 工具时非 POV 焦内活跃角色必须走子 agent 路径（phase_actor 执行绑定）"))
            elif _status_b.startswith("单窗口") and _norm_char_key(_role_b) not in _pov_norm:
                if re.search(r"子agent不可用|工具不存在|宿主不可续话", _status_b or ""):
                    soft.append((-1, f"角色 {_role_b} 非 POV 绑定单窗口({_status_b})——豁免字面通过·仍须按 A9 审计复核（`子agent不可用`/`工具不存在` 须有本会话派发报错为据；`宿主不可续话` 据＝绑定声明）"))
                else:
                    hard.append((-1, f"角色 {_role_b} 非 POV 却绑定单窗口({_status_b})——豁免字面不在白名单。执行绑定合法豁免仅三种字面：POV 用 `单窗口(第二人称POV·用户指令转写)`·非 POV 用 `单窗口(子agent不可用)`／`单窗口(工具不存在)`（须有本会话派发报错为据）／`单窗口(宿主不可续话)`（宿主不支持具名子 agent 续话·据＝绑定声明）。“在轨轻量/背景位/主agent直演”等不是执行绑定豁免（前两者豁免对象见 A7 意图循环/角色路由表·非执行绑定）——非 POV 角色须走子 agent 路径（phase_actor 执行绑定 Step 0）"))

        # ⑬e2 绑定声明自洽（phase_actor 执行绑定 O2）：「宿主不可续话」是宿主属性·同批内必须一致——
        #      同批若同时存在 `子agent(组装✓)` 与 `单窗口(宿主不可续话)`，至少一方错，而该字面据＝绑定声明
        #      本身（自报）·机械只验白名单字面 → 此处出软警，须 A9 复核。
        _host_unresumable = sorted(_r for _r, _st in _binding.items() if _st.startswith("单窗口") and "宿主不可续话" in _st)
        if _host_unresumable and any(_st.startswith("子agent") for _st in _binding.values()):
            soft.append((-1, f"绑定声明自相矛盾：{_host_unresumable} 判「宿主不可续话」，但同批另有角色走 `子agent` 路径——宿主能否续话是宿主属性，同批内必须一致；该豁免据＝绑定声明（自报），须 A9 复核（phase_actor 执行绑定 O2）"))

        _states_by_name = {name: data for name, data in _load_char_states(world_dir)}
        # ⑬f MUSE 存在性（心声先于 ACTION·机械只验有无+对应·内容是否倒补归审计复核）：
        #     每个 ###ACTION 行动角色须有同名 ###MUSE 行（行序以批次原文账本取证）。
        _muse_roles_canonical = {
            _canonical_role_label(role, world_dir, existing) for role in _action_roles(ctx.get("muse"))
        }
        _missing_muse = sorted({a for a in _action_roles_canonical if a not in _muse_roles_canonical})
        if _missing_muse:
            hard.append((-1, f"ACTION 行动角色缺 ###MUSE 心声行: {_missing_muse}（心声先于 ACTION·MUSE 须排在各自 ACTION 之前·见 actor_decision.md「思考过程 = 心声（MUSE）」）"))
        # ⑬f2 每环须有 MUSE（phase_actor 行动环·多环落盘）：MUSE 数 ≥ ACTION 数
        #      多环＝每环一组 MUSE——有 ACTION 的环＝MUSE+ACTION；无 ACTION 的零卡环＝仅 MUSE（D4 判 `无` 的自判留痕）。
        #      上界（MUSE 数 == 环条目数）在 ⑬g2 顺序段解析后核（需环条目数）。
        def _role_line_counts(lines):
            _counts = {}
            for _l in lines or []:
                _m = re.match(r"^\s*([^:|：]+)[:：]", str(_l))
                if not _m:
                    continue
                _r = _m.group(1).strip()
                if _r:
                    _c = _canonical_role_label(_r, world_dir, existing)
                    _counts[_c] = _counts.get(_c, 0) + 1
            return _counts
        _muse_count = _role_line_counts(ctx.get("muse"))
        _action_count = _role_line_counts(ctx.get("action"))
        _muse_short = sorted(_r for _r in set(_muse_count) | set(_action_count)
                             if _muse_count.get(_r, 0) < _action_count.get(_r, 0))
        if _muse_short:
            hard.append((-1, f"同角色 MUSE 少于 ACTION: {_muse_short}——每环须有 MUSE（有 ACTION 的环＝MUSE+ACTION·零卡环＝仅 MUSE·phase_actor 行动环·多环落盘）"))
        # ⑬g SCHEDULE 留痕（行动链收敛记录·角色批必含·见 phase_actor 行动链留痕）。
        if not ctx.get("schedule"):
            hard.append((-1, "角色批缺 ###SCHEDULE 行动链留痕（轮次/窗口/顺序/收敛·调度权威仍归③调度单·此处只验留痕存在）"))
        else:
            # ⑬g2 顺序与多环（phase_actor 职责2 行动环·顺序段逐环列出）：解析顺序段
            #     `名(环N[·受影响:渠道|·自环][·零卡])` 序列；`名(环1→环2)` 合并写法解析不出足数
            #     条目，撞下条条目数检查（报错指向展开格式）。零卡环（无 ACTION·留 MUSE）照列·标 `·零卡`，
            #     **可出现在任意位置**——零卡＝该环不落地·**不结束走环**（phase_actor 收敛核对）。
            _seq_text = " ".join(str(_s) for _s in ctx.get("schedule") or [])
            _seq_part = _seq_text.split("收敛", 1)[0]
            _rings_by_role = {}
            for _m in re.finditer(r"([^→/，,;；:：()（）]+)\(\s*环\s*(\d+)([^()（）]*)\)", _seq_part):
                _nm = _m.group(1).strip()
                if not _nm:
                    continue
                _c = _canonical_role_label(_nm, world_dir, existing)
                _suffix = (_m.group(3) or "").strip()
                _src_m = re.search(r"受影响\s*[:：]\s*([^·]*)", _suffix)
                _src = _src_m.group(1).strip() if _src_m else ""
                _is_zero = "零卡" in _suffix
                _is_self = "自环" in _suffix
                _rings_by_role.setdefault(_c, []).append(
                    (_m.start(), int(_m.group(2)), _src, _is_zero, _is_self))
            for _r in sorted(set(_muse_count) | set(_action_count)):
                _entries = sorted(_rings_by_role.get(_r, []))
                _ag = _action_count.get(_r, 0)
                _nonzero = [_e for _e in _entries if not _e[3]]
                if _ag >= 1 and len(_nonzero) != _ag:
                    hard.append((-1, f"角色 {_r} 本批 ACTION {_ag} 组，但 ###SCHEDULE 顺序段解析出 {len(_nonzero)} 条非零卡环条目（须按实际落地序逐环列出并标环号·禁 `名(环1→环2)` 合并写法·零卡环标 `(环N·零卡)`·格式见 phase_actor 行动链留痕）"))
                    continue
                _nums = [_n for _, _n, _, _, _ in _entries]
                if any(_b <= _a for _a, _b in zip(_nums, _nums[1:])):
                    hard.append((-1, f"角色 {_r} 的 ###SCHEDULE 顺序段环号未递增（须按实际落地序逐环列出）"))
                # ⑬f2b 每环须有 MUSE（phase_actor 闸门「顺序与多环」）：MUSE 数 == 环条目数
                #       零卡环无 ACTION 但须有 MUSE——无行动是角色的判定结果，须有角色自述可核
                if _entries and _muse_count.get(_r, 0) != len(_entries):
                    hard.append((-1, f"角色 {_r} 本批 MUSE {_muse_count.get(_r, 0)} 行，但 ###SCHEDULE 顺序段解析出 {len(_entries)} 条环条目——每环须有 MUSE（有 ACTION 的环＝MUSE+ACTION·零卡环＝仅 MUSE·见 phase_actor 行动环·多环落盘）"))
                    continue
                for _pos, _n, _src, _is_zero, _is_self in _entries:
                    if _n >= 2 and not _src and not _is_self:
                        hard.append((-1, f"角色 {_r} 的 ###SCHEDULE 顺序段环{_n}条目缺输入来源（续环须标 `·受影响:渠道` 或 `·自环`·见 phase_actor 行动链留痕）"))
                        break
            # ⑬g3 收敛可验（phase_actor 闸门·收敛可验）：收敛段逐角色**两项**表态（窗口否/是·待用户否/是）；
            #     范围＝调度单焦内活跃角色 ∪ 有 ACTION 角色（含 POV——第二人称的收敛理由固定为「待用户是」·
            #     视角约定使然：其行动只能来自用户输入，无 ACTION 锚点）。只验留痕格式与脚本可核项。
            _conv_tail = ""
            for _s in ctx.get("schedule") or []:
                _ss = str(_s)
                if "收敛" in _ss:
                    _conv_tail += _ss.split("收敛", 1)[1]
            _conv_segs = {}
            for _part in re.split(r"[／/]", _conv_tail):
                _cm = re.match(r"^\s*([^=／/]+?)\s*=\s*(.+)$", _part.strip(), re.DOTALL)
                if _cm and _cm.group(1).strip():
                    _conv_segs.setdefault(_canonical_role_label(_cm.group(1).strip(), world_dir, existing), _cm.group(2).strip())
            # ⑬g3a 窗口同口径导出（phase_actor 收敛核对·窗口耗尽）：与 _window_status/precheck 同源；
            #      本批已产耗时＝###ACTION 卡 `耗时:` 合计（④ 跑在 ⑤ 之前·世界时间未推进）。
            _bm_w, _el_w, _re_w, _exh_w = _window_status(world_dir)
            _batch_min = 0
            for _al in ctx.get("action") or []:
                _hm = re.search(r"耗时\s*[:：]\s*(\d+)", str(_al))
                if _hm:
                    try:
                        _batch_min += int(_hm.group(1))
                    except Exception:
                        pass
            _remain_after = (_re_w - _batch_min) if _re_w is not None else None
            _win_exhausted_now = (_remain_after <= 0) if _remain_after is not None else None
            try:
                _ws_narr_g = str((yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}).get("叙事约定", "") or "")
            except Exception:
                _ws_narr_g = ""
            _second_person_g = "第二人称" in _ws_narr_g
            _act_text_g, _muse_text_g = {}, {}
            for _ln_g in ctx.get("action") or []:
                _am_g = re.match(r"^\s*([^:|：]+)[:：]\s*(.*)$", str(_ln_g), re.DOTALL)
                if _am_g and _am_g.group(1).strip():
                    _c_g = _canonical_role_label(_am_g.group(1).strip(), world_dir, existing)
                    _act_text_g[_c_g] = (_act_text_g.get(_c_g, "") + _am_g.group(2)).strip()
            for _ln_g in ctx.get("muse") or []:
                _mm_g = re.match(r"^\s*([^:|：]+)[:：]\s*(.*)$", str(_ln_g), re.DOTALL)
                if _mm_g and _mm_g.group(1).strip():
                    _c_g = _canonical_role_label(_mm_g.group(1).strip(), world_dir, existing)
                    _muse_text_g[_c_g] = (_muse_text_g.get(_c_g, "") + _mm_g.group(2)).strip()
            # 范围＝调度单焦内活跃 ∪ 有 ACTION 角色（焦外/背景角色走自推演·不属行动环·不表态）
            _conv_scope = {_canonical_role_label(_a, world_dir, existing) for _a in _active_roles} | _action_roles_canonical
            for _r in sorted(_conv_scope):
                _conc = _conv_segs.get(_r, "")
                if not _conc:
                    hard.append((-1, f"角色 {_r} 缺 ###SCHEDULE 收敛段逐角色表态（窗口否/是·待用户否/是·见 phase_actor 闸门「收敛可验」）"))
                    continue
                _miss = [_t for _t in ("窗口", "待用户") if not re.search(_t + r"\s*(否|是)", _conc)]
                if _miss:
                    hard.append((-1, f"角色 {_r} 的收敛段表态缺项（缺: {'、'.join(_miss)}·须窗口否/是·待用户否/是）"))
                    continue
                # ⑬g3b 窗口自报核（phase_actor 收敛核对·窗口耗尽）：脚本未耗尽 ⇒ 不得判「窗口是」
                if re.search(r"窗口\s*是", _conc) and _win_exhausted_now is False:
                    hard.append((-1, f"角色 {_r} 收敛段判「窗口是」（耗尽），但脚本按同口径算出本批后剩余≈{_remain_after}分钟（未耗尽）——自报与脚本不符（phase_actor 收敛核对·窗口耗尽）"))
                # ⑬g3c 待用户核（phase_actor 收敛核对·待用户新行动）：第二人称 POV 免锚点（其行动只能来自
                #      用户输入·无 ACTION 可锚）；其余角色须有所指且本批 ACTION／MUSE 有等候明示（等/待/候）。
                if re.search(r"待用户\s*是", _conc):
                    if _second_person_g and _norm_char_key(_r) in _pov_norm:
                        pass
                    else:
                        if "等" not in _conc:
                            hard.append((-1, f"角色 {_r} 的收敛段判待用户是却无所指（须写出等用户角色的什么行动·见 phase_actor 待用户新行动）"))
                            continue
                        if not re.search(r"[等待候]", (_act_text_g.get(_r, "") + _muse_text_g.get(_r, ""))):
                            hard.append((-1, f"角色 {_r} 的收敛段判待用户是，但本批其 ACTION／MUSE 无等候明示（等/待/候·须与所指一致·见 phase_actor 待用户新行动）"))
                # ⑬g3d 链收敛闭合（phase_actor 链收敛·两条件封闭）：两项皆否＝该角色本应续环 ⇒ 只可能由窗口耗尽收束
                _all_no = all(re.search(_t + r"\s*否", _conc) for _t in ("窗口", "待用户"))
                if _all_no and _win_exhausted_now is False:
                    hard.append((-1, f"角色 {_r} 收敛段判「窗口否·待用户否」（两条件皆否＝该角色本应续环），但脚本算出本批后本轮窗口仍剩≈{_remain_after}分钟（未耗尽）——链收敛不成立：续环缺失或收敛理由不成立（见 phase_actor 链收敛）"))
        # ⑬h 轨迹 APPEND（有 ACTION 角色本批须含连续行动轨迹 APPEND·⑬d 意图循环门依赖轨迹文本·无轨迹=门静默）。
        _trace_roles = set()
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not _append or _key_path != "连续行动轨迹":
                continue
            if not (_file_key.startswith(CHAR_STATE_PREFIX) and _file_key.endswith("_state")):
                continue
            _fp, _ = resolve_char_file(existing, _file_key, world_dir)
            if _fp is None:
                continue
            _trace_roles.add(_norm_char_key(_fp.stem[len(CHAR_STATE_PREFIX):-len("_state")]))
        _canon_by_norm = {_norm_char_key(a): a for a in _action_roles_canonical}
        _missing_trace_append = sorted({_canon_by_norm.get(n, n) for n in ({_norm_char_key(a) for a in _action_roles_canonical} - _trace_roles)})
        if _missing_trace_append:
            hard.append((-1, f"ACTION 行动角色缺本批 连续行动轨迹 APPEND: {_missing_trace_append}（轨迹必写·轮次/行动/目的/结果/他人反应/计划变化/未完成意图七子字段·见 actor_decision.md 写入节）"))
        # ⑬i MUSE 字数下限（失忆探针·与 writer 字数线同构）：三段结构＋权重判定最底线；
        #     仅豁免第二人称 POV（用户转写·短合法）；第一/三人称 POV 须走完整环（提示禁"扩写心声"·只做失忆整改）。
        #     底线值存于本处常量；文档侧（phase_*.md）写的是更高的**生成目标**——目标引导生成、底线做机械拦截，两者刻意分离。
        try:
            _ws_narr = str((yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}).get("叙事约定", "") or "")
        except Exception:
            _ws_narr = ""
        _second_person = "第二人称" in _ws_narr
        _muse_text = {}
        for _ml in ctx.get("muse") or []:
            _mm = re.match(r"^\s*([^:|：]+)[:：]\s*(.*)$", str(_ml), re.DOTALL)
            if _mm and _mm.group(1).strip():
                _canon = _canonical_role_label(_mm.group(1).strip(), world_dir, existing)
                _muse_text[_canon] = (_muse_text.get(_canon, "") + _mm.group(2)).strip()
        for _role_m, _text_m in sorted(_muse_text.items()):
            if _role_m not in _action_roles_canonical:
                continue
            if _second_person and _norm_char_key(_role_m) in _pov_norm:
                continue
            _wcm = len(re.sub(r"\s+", "", _text_m))
            if _wcm < _MUSE_MIN_CHARS:
                hard.append((-1, f"角色 {_role_m} MUSE 心声仅 ≈{_wcm} 字，低于 token 下限——疑似未走决策环（失忆）：先重读 references/phase_actor.md＋references/actor_decision.md，再重做④（1.1–1.5）。本段未落盘。"))
        # ⑬i2 轮次计数禁入（元信息禁区·组装泄漏兜底）：轮次是系统层元数据（回退裁剪基准），
        #     永不进入角色认知与叙事——时间一律转叙事时间。只拦高精度模式（两位数及以上数字＋
        #     轮：二十三轮/第十二轮/10轮·日常“一轮/三轮/三轮车/一轮明月”不拦·误伤≈0）；“循环/
        #     脚本/偏离”等词日常可无辜，不进脚本（判不了·留组装纪律＋抽查）。POV 豁免口径同⑬i。
        _yuanlun_re = re.compile(r"(第\s*)?([一二三四五六七八九十]{2,}|十[一二三四五六七八九]?|\d{2,})\s*轮(?![车])")
        _action_text = {}
        for _al in ctx.get("action") or []:
            _am = re.match(r"^\s*([^:|：]+)[:：]\s*(.*)$", str(_al), re.DOTALL)
            if _am and _am.group(1).strip():
                _canon_a = _canonical_role_label(_am.group(1).strip(), world_dir, existing)
                _action_text[_canon_a] = (_action_text.get(_canon_a, "") + _am.group(2)).strip()
        for _role_y in sorted(set(_muse_text) | set(_action_text)):
            if _role_y not in _action_roles_canonical:
                continue
            if _second_person and _norm_char_key(_role_y) in _pov_norm:
                continue
            for _src_y, _txt_y in (("MUSE", _muse_text.get(_role_y, "")), ("ACTION", _action_text.get(_role_y, ""))):
                _hit_y = _yuanlun_re.search(_txt_y or "")
                if _hit_y:
                    hard.append((-1, f"角色 {_role_y} {_src_y} 含轮次计数‘{_hit_y.group(0)}’——轮次是系统层元数据（回退裁剪基准），永不进入角色认知与叙事：组装侧时间线/记忆先剥`轮次:`行、时间转写叙事时间（第X日/早晨/刚才）；先重读 references/subagent_prompt.md「组装转换矩阵·元信息禁区」，修正组装输入后重推决策环再重做④。本段未落盘。"))
                    break
        _changed_char_roles = set()
        _written_decision = {}
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not _file_key.startswith(CHAR_STATE_PREFIX):
                continue
            _fp, _ = resolve_char_file(existing, _file_key, world_dir)
            if _fp is None:
                continue
            _name = _fp.stem[len(CHAR_STATE_PREFIX):-len("_state")]
            _changed_char_roles.add(_name)
            if _key_path == "decision":
                try:
                    _value = yaml.safe_load(_content) or {}
                except Exception:
                    _value = {}
                if isinstance(_value, dict):
                    _written_decision.setdefault(_name, set()).update(
                        field for field in DECISION_SUBFIELDS if field in _value and not _is_template_value(_value[field]))
            elif _key_path.startswith("decision."):
                _field = _key_path.split(".", 1)[1]
                if _field in DECISION_SUBFIELDS and not _is_template_value(_content):
                    _written_decision.setdefault(_name, set()).add(_field)
        for _role in sorted(_changed_char_roles):
            _old_missing = set(_decision_template_fields(_states_by_name.get(_role, {})))
            # 首次物化是所有 CHAR_state 写入角色的前置条件；已物化角色只有焦内 ACTION
            # 才进入运行层六字段更新，背景角色/焦外保留轻量状态增量。
            _required = set(DECISION_SUBFIELDS if _old_missing else
                            (DECISION_RUNTIME_FIELDS if _role in _action_roles_canonical else ()))
            _missing = _required - _written_decision.get(_role, set())
            if _missing:
                _phase = "首次物化" if _old_missing else "运行层更新"
                hard.append((-1, f"角色 {_role} 的 decision {_phase}不完整，缺: {sorted(_missing)}——先有实体决策，再进入角色路由或产 ACTION/轨迹"))
        # ⑫b 行动前置物化（硬性·仅有 ACTION 的非 POV 角色）：位置/核心状态/妆扮/压力水平/防御有效性须为实体值
        #     （空值/[占位]均视为未物化）；服饰须为非空列表（模板初始 []·物化后按 CHAR_.md 外在特征填充基线）。
        #     首次物化门（decision 八项）不动·本门只查行动依据（无落点/无状态/无档位即行动=决策空转）。
        #     同批物化有效（磁盘值＋本批最后写入叠加后判定）；POV 豁免（用户角色从简·有 ACTION 亦不查）。
        _disk_by_norm = {_norm_char_key(_n): (_d if isinstance(_d, dict) else {})
                         for _n, _d in _states_by_name.items()}
        _skel_writes = {}
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not _file_key.startswith(CHAR_STATE_PREFIX) or _append:
                continue
            _fp2, _ = resolve_char_file(existing, _file_key, world_dir)
            if _fp2 is None:
                continue
            _nm2 = _fp2.stem[len(CHAR_STATE_PREFIX):-len("_state")]
            _skel_writes[(_norm_char_key(_nm2), _key_path)] = _content
        for _role in sorted(_action_roles_canonical):
            _nk = _norm_char_key(_role)
            if _nk in _pov_norm:
                continue
            _disk = _disk_by_norm.get(_nk, {})
            _miss = []
            for _f in ACTION_SKELETON_STR_FIELDS:
                _eff = _skel_writes.get((_nk, _f), None)
                if _eff is None:
                    _eff = _disk.get(_f)
                if _eff is None or (isinstance(_eff, str) and _is_template_value(_eff)) \
                        or (not isinstance(_eff, str) and not str(_eff).strip()):
                    _miss.append(_f)
            _fc = _skel_writes.get((_nk, "服饰"), None)
            if _fc is not None:
                try:
                    _parsed = yaml.safe_load(_fc)
                except Exception:
                    _parsed = None
                if isinstance(_parsed, list):
                    _dress_ok = any(str(x).strip() for x in _parsed)
                elif isinstance(_parsed, str):
                    _dress_ok = not _is_template_value(_parsed)
                else:
                    _dress_ok = _parsed is not None and bool(str(_parsed).strip())
            else:
                _dv = _disk.get("服饰")
                if isinstance(_dv, list):
                    _dress_ok = any(str(x).strip() for x in _dv)
                elif isinstance(_dv, str):
                    _dress_ok = not _is_template_value(_dv)
                else:
                    _dress_ok = _dv is not None and bool(str(_dv).strip())
            if not _dress_ok:
                _miss.append("服饰")
            if _miss:
                hard.append((-1, f"角色 {_role} 有 ACTION 但行动前置字段未物化，缺: {sorted(_miss)}——位置/核心状态/妆扮/服饰/压力/防御须先有实体值（同批物化有效·见 keys.md 骨架物化规则/phase_actor 先决状态转换）"))
        # ⑫c 位置值域（硬性·keys.md「位置」）：CHAR_state.位置 非空实体值必须命中 regions/ 目录树
        #     REGION 节点后缀路径（角色认知根开始·括号注自动剥除）。有目录树的世界里解析失败=非法值——
        #     非法位置会致盲区域一致性检查（场景切换主判据·见 _region_consistency），故在写入口硬顶回。
        if (world_dir / "regions").is_dir():
            for _kind, _file_key, _key_path, _content, _append in ops:
                if _kind != "write" or _append or _key_path != "位置":
                    continue
                if not (_file_key.startswith(CHAR_STATE_PREFIX) and _file_key.endswith("_state")):
                    continue
                if _is_template_value(_content):
                    continue
                if _pos_region_node(world_dir, _content) is not None:
                    continue
                hard.append((-1, f"角色状态 {_file_key}.位置 值非法: '{str(_content).strip()}'——必须为 regions/ 目录树节点后缀路径（角色认知根开始·剥括号注后须命中 REGION 节点·如 Sweetwater/Main Street·见 keys.md「位置」）；POV 跨区域时先走场景切换（scene_management §移动场景协议）再写位置"))
        # ⑬ 计划-动作一致性（值域化·phase_actor/keys 同步）：覆盖源＝actor_decision.md D3 长期计划巡检 判定（角色判断），
        #     轨迹 `计划变化` 是本轮**记录**（不驱动覆盖）——gate 只做双向一致性核对：
        #     记 `调整` 却未覆盖 → 拦；本轮有轨迹却覆盖而未记 `调整` → 拦。
        #     例外：首次建立 decision.当前计划（盘上旧值为空/模板占位）→ 放行——骨架物化规则要求同批必写首条轨迹，
        #     此时「覆盖而未记调整」是规则的必然结果，不是违规。
        _plan_changed, _plan_overwritten, _has_trace = set(), set(), set()
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not (
                    _file_key.startswith(CHAR_STATE_PREFIX) and _file_key.endswith("_state")):
                continue
            if _append and _key_path == "连续行动轨迹":
                _has_trace.add(_norm_char_key(_file_key))
                if re.search(r"计划变化\s*:\s*调整", _content):
                    _plan_changed.add(_norm_char_key(_file_key))
            elif _key_path == "decision.当前计划":
                _plan_overwritten.add(_norm_char_key(_file_key))
        _missing_plan = _plan_changed - _plan_overwritten
        if _missing_plan:
            hard.append((-1, f"轨迹标记计划已调整（计划变化: 调整——）但未覆盖 decision.当前计划: {sorted(_missing_plan)}——计划改变须同批覆盖当前计划"))
        _missing_trace = (_plan_overwritten & _has_trace) - _plan_changed
        if _missing_trace:
            # 首次建立放行：盘上 decision.当前计划 为空/模板占位 → 本轮是首次建立，不是「覆盖既有计划」
            _old_plan = {}
            for _nm, _dt in _load_char_states(world_dir):
                _dec = _dt.get("decision") if isinstance(_dt, dict) else None
                _old_plan[_norm_char_key(f"{CHAR_STATE_PREFIX}{_nm}_state")] = (
                    _dec.get("当前计划") if isinstance(_dec, dict) else None)
            _missing_trace = {k for k in _missing_trace if not _is_template_value(_old_plan.get(k))}
        if _missing_trace:
            hard.append((-1, f"覆盖了 decision.当前计划 但本轮轨迹 计划变化 未记「调整」: {sorted(_missing_trace)}——覆盖与记录须同批一致；轨迹写 `计划变化: 调整——客观概括`"))
        # ⑬d 意图循环拦截（phase_actor 僵持再评估·机核判据=未完成意图字符串）：
        #   本轮轨迹 未完成意图 与状态文件最近 2 条（上轮/上上轮）完全相同 → 连续 3 轮同意图 → 拦。
        #   放行=本轮意图与任一历史不同；动作词/幅度换皮绕不过意图字符串；焦外轻量（无轨迹）不查。
        _cur_intent = {}  # norm name -> 本轮轨迹 未完成意图
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not _append or not (
                    _file_key.startswith(CHAR_STATE_PREFIX) and _file_key.endswith("_state")):
                continue
            if _key_path != "连续行动轨迹":
                continue
            _fp, _ = resolve_char_file(existing, _file_key, world_dir)
            if _fp is None:
                continue
            _name = _fp.stem[len(CHAR_STATE_PREFIX):-len("_state")]
            try:
                _blocks = yaml.safe_load(_content) or []
            except Exception:
                _blocks = []
            if isinstance(_blocks, list):
                for _b in _blocks:
                    if isinstance(_b, dict) and str(_b.get("未完成意图", "") or "").strip():
                        _cur_intent[_norm_char_key(_name)] = str(_b.get("未完成意图", "")).strip()
        for _nk, _intent in _cur_intent.items():
            _hist_pairs = []
            for _name0, _data in _states_by_name.items():
                if _norm_char_key(_name0) == _nk:
                    _hist_pairs = [(t.get("轮次"), str(t.get("未完成意图", "") or "").strip())
                                   for t in (_data.get("连续行动轨迹") or []) if isinstance(t, dict)]
                    break
            # 计数按轮次去重（同轮多环＝同一轮·取该轮末环的 未完成意图）：
            _last2 = []
            _seen_rounds = []
            for _rd, _it in reversed(_hist_pairs):
                if _rd in _seen_rounds:
                    continue
                _seen_rounds.append(_rd)
                if _it:
                    _last2.append(_it)
                if len(_last2) == 2:
                    break
            _last2.reverse()
            if len(_last2) == 2 and all(x == _intent for x in _last2):
                hard.append((-1, f"角色 {_nk} 意图循环——未完成意图连续 3 轮相同（{_intent}）：僵持再评估须换意图"
                                 "（先读 decision.失败后续·或换路径/目标重估/抓新机会·见 phase_actor 僵持再评估；"
                                 "放行=本轮意图与近 3 轮任一不同）"))
    elif ops and not stage:
        # 未声明阶段的兼容路径（迁移期维护批）：沿用综合检查
        if not has_ct_op:
            soft.append((-1, "完整推进轮 change set 应含 ≥1 条 CT 推进/注册（conflicts.CT-XX）——查询轮豁免"))
        if not has_ws_time:
            soft.append((-1, "完整推进轮 change set 应含 world_state.时间.具体时间 推进（查询轮豁免）"))
        if not has_ws_round:
            soft.append((-1, "完整推进轮 change set 应含 world_state.轮次 +1（查询轮豁免）"))
        if not has_ws_summary:
            soft.append((-1, "完整推进轮 change set 应含 world_state.前情描述（≤100字状态短语·查询轮豁免）"))
        if not has_scene_timeline:
            soft.append((-1, "完整推进轮 change set 应含 scene_state.场景时间线 追加（查询轮豁免）"))

    # ⑬c 角色覆盖声明（硬性——角色批必须显式说明行动角色是否落到 CHAR_state）
    if has_char_op:
        coverage_raw = _parse_role_coverage(meta_lines)
        coverage = {
            _canonical_role_label(role, world_dir, existing): status
            for role, status in coverage_raw.items()
        }
        reaction_roles = {
            _canonical_role_label(role, world_dir, existing)
            for role in _action_roles(action_lines)
        }
        submitted_roles = set()
        for _kind, _file_key, _key_path, _content, _append in ops:
            if _kind != "write" or not _file_key.startswith(CHAR_STATE_PREFIX) or not _file_key.endswith("_state"):
                continue
            _fp, _ = resolve_char_file(existing, _file_key, world_dir)
            if _fp is not None:
                submitted_roles.add(_fp.stem[len(CHAR_STATE_PREFIX):-len("_state")])
        if not coverage:
            hard.append((-1, "###META 缺少角色覆盖声明：角色批必须写 `角色覆盖: Name=更新,Other=更新(在轨·轻量)`"))
        else:
            for role in sorted(reaction_roles):
                normalized = _canonical_role_label(role, world_dir, existing)
                status = coverage.get(normalized)
                if status is None:
                    hard.append((-1, f"角色覆盖声明缺少 ###ACTION 行动角色: {role}"))
                elif not status.startswith("更新"):
                    hard.append((-1, f"角色覆盖声明 {role}=「{status}」非法——合法状态仅 `更新` / `更新(在轨·轻量)`（「无变化」通道已废止：歧义=易执行为无反应冻结——焦外角色一律自推演更新·在轨循环角色标 更新(在轨·轻量)）"))
                elif normalized not in submitted_roles:
                    hard.append((-1, f"角色覆盖声明标记 {role}=更新，但批次缺 CHAR_state 写入"))
            for role in sorted(submitted_roles):
                if role not in coverage:
                    hard.append((-1, f"CHAR_state 已写入但角色覆盖声明缺少: {role}"))

    # ⑭ 跨叙事提醒（软性——CROSS_NARRATIVES.md 存在时，完整推进轮应核对深匹配）
    if (world_dir / "story_architecture" / "CROSS_NARRATIVES.md").exists() and has_ct_op:
        soft.append((-1, "CROSS_NARRATIVES.md 存在——完整推进轮应核对跨叙事深匹配（SKILL ④: 浅匹配=登记不操作；深匹配=注入可写行为偏移；激活=注册新 CT；每轮最多激活一条·同线间隔≥3轮）"))
    # ⑮ 行为偏移落地提醒（软性——change set 含「行为偏移」标记 → 叙事阶段必须落地）
    if any("行为偏移" in content for _, _, _, content, _ in ops):
        soft.append((-1, "change set 含「行为偏移」标记——叙事阶段必须如实落地该偏移（W3 核验·可观察行为·不解释来源）"))

    # ⑯ 记忆留痕逐角色对照（硬性·批次级）：###META 记忆✓ 后跟逐角色同类计数留痕
    # （格式 `记忆✓ {角色}:{计数}·{已触发|未达}`·空格分隔·角色名以下划线代空格）
    # 批次写了 CHAR_state 的角色必须出现在留痕中——防「扫旧同类计数只做主线角色」的注意力遗漏
    # （Angela 案例：轮次 16-19 信念提炼计数只对 Guest 发生·贴线角色同类链从未进入计数视野）；
    # 留痕标「已触发」→ 批次必须含该角色 ###APPEND: 记忆锚点（认知决策与落盘一致性）；
    # 信念提炼的 信念演化 联动由 validate「6g2 门槛满足未升档」软告警承载——此处不加闸门（④角色已是注意力负担最重阶段）。
    char_roles = set()
    for _i, (_k, _fk, _kp, _c, _a) in enumerate(ops):
        if _k != "write" or not _fk.startswith(CHAR_STATE_PREFIX) or not _fk.endswith("_state"):
            continue
        _fp, _ = resolve_char_file(existing, _fk, world_dir)
        if _fp is not None:
            char_roles.add(_fp.stem[len(CHAR_STATE_PREFIX):-len("_state")])
    # 维护批豁免：###STAGE: 维护（或 --maintenance）＝同轮续批字段修复/数据归一·非 ④角色工作段，
    # 无 MUSE/SCHEDULE/角色覆盖可言——本闸门（逐角色记忆✓ 留痕）不应拒其字段修复写入。
    if char_roles and not maintenance and stage == "角色":
        # 角色覆盖允许分布在多条 META；记忆✓ 也按全部 META 行解析，避免第二条 META 被静默忽略。
        meta_text = " ".join(str(line or "") for line in meta_lines)
        traced = {}  # 角色 → 判定（已触发/未达）
        for m in re.finditer(r"记忆✓\s*(.*?)(?=\s+记忆✓|$)", meta_text):
            for tok in m.group(1).split():
                mm = re.match(r"^(.+?):(\d+)(?:·(已触发|未达))?$", tok)
                if mm:
                    role_label = _canonical_role_label(mm.group(1), world_dir, existing)
                    traced[role_label] = mm.group(3) or "未达"
        for role in sorted(char_roles):
            if role not in traced:
                hard.append((-1, f"###META 记忆✓ 留痕缺角色: {role}（逐角色同类计数必列·格式 `记忆✓ {{角色}}:{{计数}}·{{已触发|未达}}`·角色名以下划线代空格·查询轮豁免）"))
            elif traced[role] == "已触发":
                has_anchor = any(
                    _k == "write" and _fk.startswith(CHAR_STATE_PREFIX) and _fk.endswith("_state")
                    and _kp == "记忆锚点"
                    and resolve_char_file(existing, _fk, world_dir)[0] is not None
                    and resolve_char_file(existing, _fk, world_dir)[0].stem[len(CHAR_STATE_PREFIX):-len("_state")] == role
                    for _k, _fk, _kp, _c, _a in ops
                )
                if not has_anchor:
                    hard.append((-1, f"###META 记忆✓ 留痕标 {role}:已触发·但批次缺该角色 记忆锚点 写入（###KEY: 覆盖或 ###APPEND: 追加）"))

    # ⑬c-2 导演调度单点名角色覆盖（硬性——③调度单的 焦内活跃/背景/焦外 cast 必须被角色覆盖声明）
    # 复用 角色覆盖 对账：调度单命名的已知角色 = 更新(→CHAR_state 写) 或 更新(在轨·轻量)(→CHAR_state 写)；
    # 「无变化」通道废止（歧义=易执行为无反应冻结）；未覆盖 → 拦。
    # POV 豁免：用户角色（第二人称无指令可无决策无行动）不强制覆盖声明/CHAR_state 写。
    if not maintenance and stage == "角色" and (has_char_op or any("角色覆盖" in (ln or "") for ln in meta_lines)):
        sched_roles = _schedule_cast_roles(world_dir)
        try:
            _pov_skip = {_norm_char_key(p) for p in _pov_role_names(world_dir, existing)}
        except Exception:
            _pov_skip = set()
        sched_roles = {r for r in sched_roles if _norm_char_key(r) not in _pov_skip}
        if sched_roles:
            coverage2_raw = _parse_role_coverage(meta_lines)
            coverage2 = {
                _canonical_role_label(role, world_dir, existing): status
                for role, status in coverage2_raw.items()
            }
            submitted2 = set()
            for _kind, _fk, _kp, _c, _a in ops:
                if _kind == "write" and _fk.startswith(CHAR_STATE_PREFIX) and _fk.endswith("_state"):
                    _fp, _ = resolve_char_file(existing, _fk, world_dir)
                    if _fp is not None:
                        submitted2.add(_fp.stem[len(CHAR_STATE_PREFIX):-len("_state")])
            for role in sorted(sched_roles):
                status = coverage2.get(role)
                if status is None:
                    hard.append((-1, f"角色覆盖声明缺少调度单点名角色: {role}（③调度单点名·④自推演后在同批更新 CHAR_state）"))
                elif not status.startswith("更新"):
                    hard.append((-1, f"角色覆盖声明 {role}=「{status}」非法——合法状态仅 `更新` / `更新(在轨·轻量)`（「无变化」通道已废止：④为其自推演更新 CHAR_state·在轨循环角色标 更新(在轨·轻量)）"))
                elif role not in submitted2:
                    hard.append((-1, f"角色覆盖声明标记 {role}=更新，但批次缺 CHAR_state 写入"))

    return hard, soft


def cmd_audit(world_dir: Path, input_file: str | None = None):
    """audit: 校验 stdin 或 --file 的阶段批次草案（###STAGE/###FILE/###KEY/###APPEND 格式），不落盘。
    硬性违规 → 列出全部并 exit 1（草案不合格）；仅软性警告 → 打印警告，exit 0（可写入）。"""
    raw_stdin = _read_input_utf8(input_file)
    ctx = parse_batch_entries(raw_stdin.split("\n"))
    ops, parse_errors = ctx["ops"], ctx["errors"]
    if raw_stdin.strip() and not ctx["stage"]:
        parse_errors.append("###STAGE 缺失——批次首行须为 `###STAGE: <阶段名>`；若首行看似正确仍报此错，检查文件是否带 BOM/编码损坏")
    hard, soft = check_batch(ops, world_dir, ctx, enforce_scene_dir=False)
    if ctx["stage"]:
        print(f"[AUDIT] ###STAGE 回显: {ctx['stage']}", file=sys.stderr)
    if ctx["storyline"]:
        print(f"[AUDIT] ###STORYLINE 回显: {ctx['storyline'][0][0]}", file=sys.stderr)
    if ctx["beat"]:
        print(f"[AUDIT] ###BEAT 回显: {ctx['beat'][0]}", file=sys.stderr)
    if ctx["action"]:
        sched = ctx["schedule"][0] if ctx["schedule"] else "（无）"
        print(f"[AUDIT] ###ACTION 回显: {len(ctx['action'])} 条行动卡 · SCHEDULE: {sched}", file=sys.stderr)
    if ctx["meta"]:
        print(f"[AUDIT] ###META 回显: {ctx['meta'][0]}", file=sys.stderr)
        if "记忆" not in ctx["meta"][0]:
            soft.append((0, "###META 静默自查锚点缺少 记忆✓ 槽（记忆✓=逐角色同类计数留痕·每出场角色必列·见 phase_actor.md）"))
    else:
        soft.append((0, "未检测到 ###META: 静默自查锚点——阶段批次必写（###STAGE 之后）：各阶段格式见 phase_*.md（查询轮/维护轮豁免）"))
    # scene_state 落点软提示（预检路径·场景目录由场记阶段3 init_scene 创建·先于批次写入）
    for _idx, _msg in soft:
        if _idx != -1 and "预检软提示" in _msg:
            print(f"[AUDIT] 软性提示: {_msg}", file=sys.stderr)
    if hard or parse_errors:
        print(f"[AUDIT] {len(hard) + len(parse_errors)} 个硬性违规——change set 不合格:", file=sys.stderr)
        for e in parse_errors:
            print(f"  - {e}", file=sys.stderr)
        for _, v in hard:
            print(f"  - {v}", file=sys.stderr)
        sys.exit(1)
    if soft:
        print(f"[AUDIT] 硬性检查通过（{len(soft)} 个软性警告·不拦截·validate 汇总）:", file=sys.stderr)
        for _, v in soft:
            print(f"  - {v}", file=sys.stderr)
    print("[AUDIT] OK——change set 通过硬性检查，可写入")


def quick_validate_summary(world_dir):
    """写入后自动触发：轻量关键项检查，只输出警告数摘要（详细列表见 validate 命令）。
    覆盖 SKILL.md 脚本校验线中最高价值项：记忆锚点总量/单条、焦点场景一致性、CT 键格式。"""
    warnings = []
    try:
        scene_dir = get_scene_dir(world_dir)
        # 记忆锚点（脚本校验线）
        for cfp in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
            try:
                cdata = yaml.safe_load(cfp.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            mem = cdata.get("记忆锚点", "")
            if isinstance(mem, list):
                total = sum(len(str(it.get("内容", ""))) for it in mem if isinstance(it, dict))
                if total > ANCHOR_LIMIT_TOTAL:
                    warnings.append(f"{cfp.name}: 记忆锚点 {total} 字 > {ANCHOR_LIMIT_TOTAL} 校验线——需执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）")
            elif isinstance(mem, str) and mem.strip():
                if len(mem) > ANCHOR_LIMIT_TOTAL:
                    warnings.append(f"{cfp.name}: 记忆锚点 {len(mem)} 字 > {ANCHOR_LIMIT_TOTAL} 校验线——需执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）")
        # 焦点场景 ↔ 场景目录
        ws_fp = world_dir / "states" / "world_state.yaml"
        if ws_fp.exists():
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8")) or {}
            focus = str(ws.get("焦点场景") or "").strip()
            if focus and scene_dir and not scene_dir.name.startswith(focus):
                warnings.append(f"焦点场景 '{focus}' 与当前场景目录 '{scene_dir.name}' 不一致")
        # CT 键格式
        c_fp = world_dir / "states" / "conflicts.yaml"
        if c_fp.exists():
            cdata = yaml.safe_load(c_fp.read_text(encoding="utf-8")) or {}
            for k in cdata:
                if not re.match(r"^CT-\d{2}$", str(k)):
                    extra = "（节拍表残留）" if str(k) == BEAT_TOP_KEY else ""
                    warnings.append(f"conflicts.yaml: 顶层键 '{k}' 不符合 CT-XX 格式{extra}")
    except Exception:
        pass
    if warnings:
        print(f"[VALIDATE] 写入完成，{len(warnings)} 个内容警告待处理（详细列表运行 validate 查看）", file=sys.stderr)
        for w in warnings[:5]:
            print(f"  - {w}", file=sys.stderr)
        if len(warnings) > 5:
            print(f"  …等 {len(warnings) - 5} 条", file=sys.stderr)


# ── 多段批次切分：按 ###STAGE: 行切段（每段自带阶段头·单阶段批次=单段特例·行为不变）──
def split_stage_segments(lines):
    starts = [i for i, ln in enumerate(lines) if ln.startswith("###STAGE:")]
    if not starts:
        return [lines]
    edges = ([0] if starts[0] > 0 else []) + starts + [len(lines)]
    return [lines[a:b] for a, b in zip(edges, edges[1:])]


def cmd_write_raw(world_dir: Path, extra: list[str], batch: bool = False, append_mode: bool = False, dry_run: bool = False, force: bool = False, input_file: str | None = None, resume_from: int | None = None, maintenance: bool = False):
    """
    write-raw: 直接写原始文本到指定字段，绕过 YAML 输入解析。
    append-raw: 追加到指定字段末尾（累积字段专用：记忆锚点/信念演化/场景时间线/关键场景信息）。

    单字段模式: worldctl.py <世界> write-raw <文件key> <YAML键路径> [内容]
                 worldctl.py <世界> append-raw <文件key> <YAML键路径> [内容]
    批量模式:   worldctl.py <世界> write-raw --batch / append-raw --batch
               批次文本来源: stdin（cat 管道）或 --file <UTF-8批次文件>（PowerShell 等无 heredoc 环境）
               格式:
                 ###FILE: <文件key>
                 ###KEY: <YAML键路径>      ← 覆盖写
                 <内容行...>
                 ###APPEND: <YAML键路径>   ← 追加写（字段不存在时等同新建）
                 <内容行...>
                 ###FILE: <另一个文件key>
                 ...

    文件key: scene_state, CHAR_Maeve Millay_state 等
    YAML键路径: 点分隔路径，如 "核心状态" 或 "子键.更深"
    内容: 单字段模式可选 CLI 参数，否则从 stdin 读取

    注意: write-raw --batch 非幂等——###APPEND: 重复执行会把累积字段（记忆锚点/场景时间线等）重复追加。
    同一批次只执行一次；执行后的确认用 read / validate / 重跑 --dry-run（只读），禁止重放 write 命令做验证。
    脚本内置重复追加检测：APPEND 内容已存在于字段中 → 自动跳过并打印 [SKIP]。
    多段批次：批次内可重复出现 ###STAGE: 行——每段独立走 解析→audit→段级闸门→STORYLINE/BEAT→写入 管线；
    段级闸门（默认启用·--force 豁免）：带 ###STAGE 声明且属批次类五阶段（戏剧家/编剧/导演/角色/场记）的段，
    必含项缺失或硬性违规=该段整体拦截 exit 1 不落盘（作家段豁免·W4 走 gate writer --check）。
    单阶段批次与无 ###STAGE 声明的维护批行为不变（audit 仍为单字段顶回）。
    合批白名单：多段合批仅限 [戏剧家编剧导演] 结构合批；角色段/场记段必须单段独批——
    同批同时含 角色+他段、或 场记+他段 = 跨层合批 [BATCH-FAIL] 零副作用整体拦截
    （--resume-from 重提 / --force 回退豁免）。
    批次含场记段（轮末）时落盘后自动附跑 round-check（仅报告不拦截）。
    --force（显式回退专用·仅 --batch）：绕过 audit ④ 轮次单调 与 ⑬b 轨迹覆盖写——回退手工重建（无快照）时用；
    其余数据完整性硬性检查（① 角色反应三件套/② 载体/⑤ scene_state 落点）照常拦截。回退后必做残留扫描 + validate。
    """

    def write_one(file_key: str, key_path_str: str, content: str, append: bool = False):
        """写单个字段到指定文件。append=True 时追加到末尾。成功返回 True，失败返回 False。"""
        scene_dir = get_scene_dir(world_dir)
        existing = discover_files(world_dir, scene_dir)
        # file_key 归一化（剥 .yaml/.yml 与路径前缀）——与审计路径 check_batch 同源；
        #   否则 `###FILE: conflicts.yaml` / `states/CHAR_X_state.yaml` 能解析到文件、audit 也放行，
        #   却跳过本函数内的字段级专属处理（conflicts 列表归一 / 结构化字段判定）→ 类型损坏或覆盖写
        file_key = _normalize_file_key(file_key)
        key_path = key_path_str.split(".")
        # conflicts.yaml 路径归一化：去掉多余的 `conflicts.` 根前缀
        if file_key == "conflicts" and key_path and key_path[0] == "conflicts":
            key_path = key_path[1:]

        filepath, note = resolve_char_file(existing, file_key, world_dir)
        if filepath is None and file_key == "pending_actions":
            # pending_actions：缺失时按模板建（对齐 init_scene·保证焦外记录层可写）
            filepath = pending_actions_path(scene_dir, create=True)
            if filepath is None:
                print("[ERR] pending_actions 创建失败（缺场景目录或写盘失败）", file=sys.stderr)
                return False
        elif filepath is None:
            # CHAR_ key 未命中（多义/零命中）：拒绝新建并给出候选·note 已是可直接打印的完整 [ERR] 文本
            if note:
                print(note, file=sys.stderr)
                return False
            # scene_state 解析失败：准确诊断焦点场景目录/文件状态（避免「未知文件 key」误导为 FILE key 写错）
            if file_key == "scene_state":
                if scene_dir is None:
                    print("[ERR] scene_state 落点错误: 无法定位当前焦点场景目录——先确认 world_state.焦点场景 后再写入", file=sys.stderr)
                elif not (scene_dir / "scene_state.yaml").exists():
                    print(f"[ERR] scene_state 落点错误: 焦点场景目录/文件不存在（{scene_dir}）——先执行 init_scene 创建场景（scene_card/start_snapshot/INDEX ACTIVE）后再写入", file=sys.stderr)
            else:
                print(f"[ERR] 未知文件 key: {file_key}", file=sys.stderr)
            return False
        if note:
            print(note, file=sys.stderr)

        if filepath.name == "world_map.yaml":
            print("[ERR] world_map 禁用点路径写入（键名可含空格/点·点路径与 shell 分词均不支持）——请用 write 命令（YAML diff 合并·含单字段更新）", file=sys.stderr)
            return False

        if filepath.exists():
            try:
                data = yaml.safe_load(filepath.read_text(encoding="utf-8")) or {}
            except Exception as e:
                print(f"[ERR] {file_key} 解析失败，拒绝写入（防止静默清空）: {e}", file=sys.stderr)
                return False
        else:
            data = {}

        target = data
        for k in key_path[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]
        leaf = key_path[-1]
        # 结构化累积字段形态/类型校验——与 --dry-run 共用同一纯函数（预演与实跑同源·防预演假阳性）。
        # 校验通过后 is_structured_field / is_list_item_content 继续供下方覆盖分支（2935/2943）复用。
        _shape_err, is_structured_field, is_list_item_content = _append_shape_check(file_key, key_path, content, append)
        if _shape_err:
            print(f"[ERR] {_shape_err}", file=sys.stderr)
            return False
        if append and is_structured_field:
            # 解析 change set 中给出的列表元素（可能多条）——直接用 yaml 解析（与 write_yaml 同款）
            # 形态/类型已由 _append_shape_check 校验为合法列表，此处不再重复判定。
            new_items = yaml.safe_load(content)
            if leaf in STR_LIST_COERCE_FIELDS:
                new_items = _coerce_str_list(content)
            else:
                new_items = [it for it in new_items if isinstance(it, dict)]

            existing_val = target.get(leaf, [])
            if isinstance(existing_val, str):
                # 模板占位残留（templates/CHAR_state.yaml 骨架占位·如 '[我知道哪些地方（去过/被告知/目睹）]'）——视为空·不混入列表
                if re.fullmatch(r"\s*\[[^\]]*\]\s*", existing_val):
                    existing_val = []
                else:
                    existing_val = [{"轮次": "", "内容": ent.strip()}
                                    for ent in re.split(r"\n\s*(?:·\s*)?(?=\[)", existing_val)
                                    if ent.strip()]
            # 重复追加检测：已知地点按元素相等；伏笔按 线索 相等；其余按 轮次+内容 判断
            for item in new_items:
                dup = False
                for e in existing_val:
                    if leaf not in STR_LIST_COERCE_FIELDS and not isinstance(e, dict):
                        # 旧版散文/概括条目（字符串元素）——无法结构化去重·跳过比对不崩溃
                        # （兼容存量数据；validate 6i-b 另行提示归一）
                        continue
                    if leaf in STR_LIST_COERCE_FIELDS:
                        if str(e) == str(item):
                            dup = True
                            break
                    elif leaf == "伏笔":
                        if str(e.get("线索", "")) == str(item.get("线索", "")):
                            dup = True
                            break
                    elif leaf == "连续行动轨迹":
                        if (str(e.get("轮次", "")) == str(item.get("轮次", ""))
                                and str(e.get("行动", "")) == str(item.get("行动", ""))):
                            dup = True
                            break
                    elif leaf == "场景时间线":
                        if (str(e.get("轮次", "")) == str(item.get("轮次", ""))
                                and str(e.get("时间", "")) == str(item.get("时间", ""))):
                            dup = True
                            break
                    elif leaf == "道具" and str(e.get("ID", "")) == str(item.get("ID", "")):
                        dup = True
                        break
                    elif _elems_equal(e, item):
                        dup = True
                        break
                if not dup:
                    existing_val.append(item)
                else:
                    print(f"[SKIP] {file_key}.{'.'.join(key_path)} 重复追加已跳过（{'条目已存在' if leaf in STR_LIST_COERCE_FIELDS else ('线索已存在' if leaf == '伏笔' else '元素完全相同已存在')}）", file=sys.stderr)
            if file_key.startswith(CHAR_STATE_PREFIX) and leaf == "连续行动轨迹" and len(existing_val) > TRAJECTORY_WINDOW:
                existing_val = existing_val[-TRAJECTORY_WINDOW:]
                print(f"[TRIM] {file_key}.连续行动轨迹 已自动裁剪至最近 {TRAJECTORY_WINDOW} 轮（窗口滚动·删最旧块）", file=sys.stderr)
            target[leaf] = existing_val
            write_yaml(filepath, data)
            print(f"[OK] {file_key}.{'.'.join(key_path)} 已追加 {len(new_items)} 条结构化元素", file=sys.stderr)
            return True
        if append and leaf in target and isinstance(target[leaf], str) and target[leaf]:
            existing_val = target[leaf]
            # 模板占位残留（templates/CHAR_state.yaml 骨架占位·如 '[最近5轮动作序列…]'）——视为空·不当前缀
            if re.fullmatch(r"\s*\[[^\]]*\]\s*", existing_val):
                existing_val = ""
            # 重复追加检测（硬防护·防同一批次重放/同一内容重复追加）：
            # 批次重放时 content 完全一致，必然作为子串存在于字段值中 → 跳过
            elif content.strip() and content.strip() in existing_val:
                print(f"[SKIP] {file_key}.{'.'.join(key_path)} 重复追加已跳过（内容已存在——同一批次只执行一次，禁止重放 write 命令验证）", file=sys.stderr)
                return True
            target[leaf] = (existing_val.rstrip("\n") + "\n" if existing_val else "") + content
        elif not append and is_structured_field and leaf in STR_LIST_COERCE_FIELDS:
            # 字符串列表字段（已知地点/物理锚点）：类型统一=list[str]——
            # 散文（多行）与 YAML 列表两种输入一律由脚本归一，杜绝「列表被写成字符串」的类型损坏
            new_items = _coerce_str_list(content)
            target[leaf] = new_items
            write_yaml(filepath, data)
            print(f"[OK] {file_key}.{'.'.join(key_path)} 已覆盖（字符串列表·{len(new_items)} 条）", file=sys.stderr)
            return True
        elif not append and is_structured_field and (is_list_item_content or content.strip() in ("[]", "{}")):
            # KEY 覆盖结构化列表字段：content 为 yaml 列表文本（- item / []）→ 解析为列表全量替换
            # （字段级替换意图与 APPEND 增量区分；非列表文本仍按原始文本覆盖）
            try:
                new_items = yaml.safe_load(content)
            except Exception:
                print(f"[ERR] {file_key}.{'.'.join(key_path)} 结构化覆盖内容不是合法 YAML 列表，拒绝写入", file=sys.stderr)
                return False
            if not isinstance(new_items, list):
                print(f"[ERR] {file_key}.{'.'.join(key_path)} 结构化覆盖内容必须是 YAML 列表（- 轮次: ... / - 地点名 / []）", file=sys.stderr)
                return False
            if leaf == "已知地点":
                new_items = [str(it).strip() for it in new_items if isinstance(it, str) and it.strip()]
            else:
                new_items = [it for it in new_items if isinstance(it, dict)]
            target[leaf] = new_items
            write_yaml(filepath, data)
            print(f"[OK] {file_key}.{'.'.join(key_path)} 已覆盖（结构化列表·{len(new_items)} 条）", file=sys.stderr)
            return True
        else:
            # 包裹引号归一：输入侧单/双引号=批次文本通道的运输保护，落盘前剥净（多层累积一并归一）——
            #   磁盘永远存裸值、read 显示干净形态，杜绝「LLM 抄回带引号值再加一层」的逐轮累积；
            #   落盘安全由 yaml.dump 封装承担。APPEND 追加路径不受影响（prose 拼接不剥）。
            # 映射/列表多行内容自动解析（2026-08-17 加入·方案A）：多行 YAML 块（嵌套映射/列表）解析为 dict/list 再写入——
            #   修复「嵌套记录字段（维护名单.{角色}/时间线.{ID}/外部倒计时.{CD}/已探索区域.{区域}）被写成字符串·读取端读不到」；
            #   单行标量保持字符串（防 轮次/时间 等类型漂移）；解析失败/无结构（场景时间线等字符串块）按原字符串
            content = _strip_wrapping_quotes(content)
            # CT 列表字段单行兼容（2026-09-06）：事件线引用/关联角色 的单行 `[SL-01]` / `- SL-01` 解析为列表——
            #   修复「keys.md 示例 [SL-01] / 单行列表被当字符串落盘 → round-check 悬空」的文档-解析器不一致
            if (file_key == "conflicts" and len(key_path) == 2 and key_path[1] in ("事件线引用", "关联角色")
                    and not append):
                _items = _parse_single_line_list(content)
                if _items is not None:
                    target[leaf] = _items
                    write_yaml(filepath, data)
                    print(f"[OK] {file_key}.{'.'.join(key_path)} 已写入（单行列表兼容·{len(target[leaf])} 项）")
                    return True
            # 类型安全网：目标字段现值已是列表 + 单行内容为标量列表 → 按列表写——
            #   防「列表被单行字符串覆盖」的类型降级；与 FILE key 拼写、字段是否在白名单均无关
            if not append and isinstance(target.get(leaf), list):
                _items = _parse_single_line_list(content)
                if _items is not None:
                    target[leaf] = _items
                    write_yaml(filepath, data)
                    print(f"[OK] {file_key}.{'.'.join(key_path)} 已写入（列表归一·{len(_items)} 项）")
                    return True
            if "\n" in content:
                try:
                    _parsed = yaml.safe_load(content)
                except Exception:
                    _parsed = None
                if isinstance(_parsed, (dict, list)):
                    content = _parsed
            target[leaf] = content

        write_yaml(filepath, data)
        op = "已追加" if append else "已写入"
        # 回显标签区分类型：content 被 yaml 解析为列表/映射时显示条目数，避免 "N 项" 被误读为字节数
        if isinstance(content, list):
            _label = f"{len(content)} 项"
        elif isinstance(content, dict):
            _label = f"{len(content)} 键"
        else:
            _label = f"{len(content)}b"
        print(f"[OK] {file_key}.{'.'.join(key_path)} {op} ({_label})")
        return True

    # ── 批量模式（支持多段 ###STAGE：每段独立走完整 解析→audit→写入 管线·失败语义不变·批次文本只读一次）──
    if batch:
        if resume_from is not None:
            print("[OK] --resume-from 仅作用于段切片·段内原子性与非幂等语义不变（段号按原始批次 1 起始计）", file=sys.stderr)
        raw_stdin = _read_input_utf8(input_file)
        lines = raw_stdin.split("\n")

        def run_batch_segment(seg_lines, seg_no, applied_ops, new_line_ids):
            lines = seg_lines

            # 解析 + 语义不变量检查（audit）——硬性违规 → 单字段顶回（不整批拒绝）
            ctx = parse_batch_entries(lines)
            ops, parse_errors = ctx["ops"], ctx["errors"]
            # resume_from 重提语义：外层已切片为「失败段及其后」——这些段全部属重提（磁盘可能已部分落盘·如轮次）
            # → 轮次单调走防倒退语义（new==old 放行·仍禁真回退 new<old），其余硬性检查照常（不改 force 全局豁免）
            hard, soft = check_batch(ops, world_dir, ctx, force=force, resume_from=(resume_from is not None), maintenance=maintenance)
            if maintenance:
                print("[MAINT] 维护批模式：段级完整性闸豁免（角色覆盖/必含项/施压方向/轨道/cast）·op 级合法性校验照常", file=sys.stderr)
            blocked = {idx for idx, _ in hard}
            if ctx["stage"]:
                print(f"[AUDIT] ###STAGE 回显: {ctx['stage']}", file=sys.stderr)
            if ctx["storyline"]:
                print(f"[AUDIT] ###STORYLINE 回显: {ctx['storyline'][0][0]}", file=sys.stderr)
            if ctx["beat"]:
                print(f"[AUDIT] ###BEAT 回显: {ctx['beat'][0]}", file=sys.stderr)
            if ctx["action"]:
                sched = ctx["schedule"][0] if ctx["schedule"] else "（无）"
                print(f"[AUDIT] ###ACTION 回显: {len(ctx['action'])} 条行动卡 · SCHEDULE: {sched}", file=sys.stderr)
            if ctx["meta"]:
                print(f"[AUDIT] ###META 回显: {ctx['meta'][0]}", file=sys.stderr)
            else:
                print("[AUDIT] 软性警告: 未检测到 ###META: 静默自查锚点——阶段批次必写（查询轮/维护轮豁免）", file=sys.stderr)
            for e in parse_errors:
                print(f"[AUDIT] 解析失败: {e}", file=sys.stderr)
            if parse_errors:
                print(f"[GATE] 批次含 {len(parse_errors)} 条解析失败——该批未落盘·修正后重提交"
                      f"（解析失败=该 op 不可用·不得静默跳过；--dry-run/--force/--maintenance 同样拦截）", file=sys.stderr)
                sys.exit(1)
            for idx, v in hard:
                print(f"[AUDIT] 硬性违规——拒绝该字段写入: {v}", file=sys.stderr)
            # op 级软性警告当场可见（写时提醒·枚举错位等落盘前可改）；批次级(-1)软警仍由 quick_validate_summary 汇总
            for idx, v in soft:
                if idx >= 0:
                    print(f"[AUDIT] 软性警告: {v}", file=sys.stderr)
            # 批次级软性警告不在此逐条打印（避免噪音）——由 quick_validate_summary 汇总（validate 明细）

            # ── 段级闸门计算（gate 内嵌·默认两批形态）：必含项缺失/硬性违规=该段整体拦截不落盘 ──
            # 位置在 --dry-run 分支与 STORYLINE/BEAT/字段写入之前 → FAIL=本段零副作用，修正后重提交本段即可。
            # 复用上方 check_batch(via="write") 结果——落盘前校验用推进语义，与此处时序一致。
            # --force 回退批与无 ###STAGE 声明段跳过（维护/回退流程依赖单字段顶回语义继续）。
            # 2026-09-19 修复：闸门计算上提到 --dry-run 之前——原先 dry-run 提前 return，段级闸门
            #   （空壳段 / 导演 _check_climax_exit / 「{stage}批应含」软项提升）整层不在预演路径上，
            #   且预演恒 exit 0 → 「预演通过」≠「实跑通过」（实测：空壳段预演 0 顶回 exit 0；
            #   实跑 [GATE] 段闸门未过 + [BATCH-FAIL] exit 1）。预演与实跑自此同源。
            seg_gate_fails = []
            if not force and not maintenance:
                if ctx["stage"] and ctx["stage"] in BATCH_GATE_STAGES:
                    seg_gate_fails.extend(msg for _, msg in hard)
                    seg_gate_fails.extend(msg for idx, msg in soft
                                          if idx == -1 and msg.startswith(f"{ctx['stage']}批应含"))
                    # 空壳段（无写入/结构动作）：必含项引擎按「查询/维护豁免」跳过——但带 ###STAGE
                    # 的工作段不允许空壳（维护批应去声明；查询轮不出批次）。
                    # ②无豁免：D1 弧线定位必落盘（必含项见 check_batch 编剧分支）
                    if not ops and not ctx["storyline"] and not ctx["beat"]:
                        seg_gate_fails.append(
                            f"{ctx['stage']}段无任何写入操作与结构动作——空壳段"
                            f"（维护/恢复批请去掉 ###STAGE 声明·阶段段必含本阶段产出）")
                    if ctx["stage"] == "导演":
                        cv, _ck = _check_climax_exit(world_dir, ops, ctx["beat"])
                        seg_gate_fails.extend(cv)
                elif ctx["stage"] == "作家":
                    print("[GATE] 作家段不经批次闸门（W4 由 gate writer --check 于叙事输出前独立核验）", file=sys.stderr)

            # ── --dry-run 预演：与实跑同源（含段级闸门）·对比磁盘差异·不落盘 ──
            if dry_run:
                scene_dir = get_scene_dir(world_dir)
                existing = discover_files(world_dir, scene_dir)
                unknown_keys = 0
                shape_blocks = 0   # 结构化 append 形态/类型预检拦截数（实跑=op 级失败·部分落盘）
                # 段级拦截的段：实跑=整段零副作用 → 预演的逐 op 列表必须全部标 [顶回]（与实跑同形）
                _seg_abort = bool(ctx["stage"] and ctx["stage"] in BATCH_GATE_STAGES and seg_gate_fails)
                _field_hard_n = sum(1 for i, _ in hard if i >= 0)
                _batch_hard_n = sum(1 for i, _ in hard if i < 0)
                _blocked_n = len(ops) if _seg_abort else _field_hard_n
                print(f"[DRY-RUN] 预演 {len(ops)} 条操作，{_blocked_n} 条被顶回（不落盘）"
                      f"｜字段级顶回 {_field_hard_n} · 批次级拦截 {_batch_hard_n} · 段级拦截 {len(seg_gate_fails)}")
                for idx, (kind, file_key, key_path_str, content, append) in enumerate(ops):
                    if _seg_abort or idx in blocked:
                        print(f"  [顶回] {file_key}.{key_path_str}")
                        if file_key.startswith(CHAR_STATE_PREFIX):
                            _blocked_fp, _blocked_note = resolve_char_file(existing, file_key, world_dir)
                            if _blocked_note:
                                print("    " + _blocked_note.replace("\n", "\n    "))
                        continue
                    if kind == "delete":
                        print(f"  [删除] {file_key}.{key_path_str}")
                        continue
                    # file_key 归一化——与 write_one 同源（否则 `###FILE: conflicts.yaml` 在预演里
                    #   解析失败被误报未知 key、实跑却因归一化成功 → 预演假阳性）
                    _fk_norm = _normalize_file_key(file_key)
                    fp, _note = resolve_char_file(existing, _fk_norm, world_dir)
                    if fp is None and _fk_norm == "pending_actions":
                        fp = pending_actions_path(get_scene_dir(world_dir), create=False)
                    if fp is None:
                        unknown_keys += 1
                        if _note:
                            print("  " + _note.replace("\n", "\n  "))
                        else:
                            print(f"  [ERR] 未知文件 key: {_fk_norm}（dry-run 拦截·实写将拒绝该字段）")
                        continue
                    # 结构化 append 形态/类型预检——与 write_one 共用同一纯函数（预演与实跑同源）：
                    #   实跑此处 write_one 会 return False → op_failures → exit 1（且其余 op 已落盘·部分写入）
                    _shape_err, _isf, _ilic = _append_shape_check(_fk_norm, key_path_str.split("."), content, append)
                    if _shape_err:
                        shape_blocks += 1
                        print(f"  [预演拦截] {_fk_norm}.{key_path_str} —— {_shape_err}")
                        continue
                    old_val = None
                    if fp.exists():
                        try:
                            d = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
                            tgt = d
                            for k in key_path_str.split("."):
                                if k in tgt and isinstance(tgt[k], dict):
                                    tgt = tgt[k]
                                else:
                                    tgt = None
                                    break
                            old_val = tgt if tgt is not None else None
                        except Exception:
                            pass
                    if old_val is None:
                        print(f"  [新增] {file_key}.{key_path_str}")
                    elif str(old_val) == content:
                        print(f"  [无变化] {file_key}.{key_path_str}")
                    else:
                        action = "追加" if append else "覆盖"
                        print(f"  [{action}] {file_key}.{key_path_str}（旧 {len(str(old_val))}b → 新 {len(content)}b）")
                if unknown_keys:
                    print(f"[DRY-RUN] ⚠ {unknown_keys} 条未知文件 key——实写将被拒绝（请检查 ###FILE: 的 key 是否与 discover_files 注册一致）")
                if _batch_hard_n:
                    print(f"[DRY-RUN] ⚠ 批次级拦截 {_batch_hard_n} 条（明细见上方 [AUDIT] 硬性违规）")
                print("[DRY-RUN] ⚠ 非幂等：同一批次只执行一次；执行后确认用 read/validate，禁止重放 write 命令验证")
                # 预演判定＝实跑预测（退出码硬性·2026-09-19）：三层同源——
                #   ① seg_gate_fails 非空 → 实跑整段拦截（零副作用）→ exit 1
                #   ② unknown_keys / shape_blocks > 0 → 实跑 op 级失败（其余 op 已落盘·部分写入）→ exit 1
                #   ③ 仅字段级顶回 → 实跑仍成功（部分字段被顶回）→ exit 0 并显式提示
                _op_fails_n = unknown_keys + shape_blocks
                if seg_gate_fails:
                    print(f"[GATE] 预演判定：不通过——实跑将整段拦截·零副作用（本批为 --dry-run·未落盘）:", file=sys.stderr)
                    for _gm in seg_gate_fails:
                        print(f"  - {_gm}", file=sys.stderr)
                    print("[DRY-RUN] 预演判定：不通过（exit 1）——先按上方清单修正再提交实跑", file=sys.stderr)
                    sys.exit(1)
                if _op_fails_n:
                    print(f"[DRY-RUN] 预演判定：不通过（exit 1）——实跑将有 {_op_fails_n} 个 op 级失败"
                          f"（未知 key {unknown_keys} · 结构形态 {shape_blocks}）：其余 op 仍会落盘（部分写入）·修正后重提交本段",
                          file=sys.stderr)
                    sys.exit(1)
                if _field_hard_n:
                    print(f"[DRY-RUN] 预演判定：通过（exit 0）——实跑可落盘；注意 {_field_hard_n} 个字段将被顶回（批次仍成功·部分落盘）", file=sys.stderr)
                else:
                    print("[DRY-RUN] 预演判定：通过（exit 0）——实跑可落盘", file=sys.stderr)
                return

            # ── 段级闸门（gate 内嵌·默认两批形态）：必含项缺失/硬性违规=该段整体拦截不落盘 ──
            # 计算已上提到 --dry-run 分支之前（2026-09-19）——预演与实跑同源；此处只消费结果。
            # 位置仍在 STORYLINE/BEAT 与字段写入之前 → FAIL=本段零副作用，修正后重提交本段即可。
            if seg_gate_fails:
                print(f"[GATE] {ctx['stage']}段闸门未过——该段未落盘·整段拦截·修正后重提交本段:", file=sys.stderr)
                for _gm in seg_gate_fails:
                    print(f"  - {_gm}", file=sys.stderr)
                sys.exit(1)

            # ── ###STORYLINE / ###BEAT 自动执行（结构/指针落盘·失败拦批——LLM 不手动调用）──
            # 「新线」引用（方案A·2026-09-04）：###STORYLINE: add 的 SL-XX 由脚本自动递增分配——
            # LLM 无法在写批次时预知实际 ID。本批 add 的真实 ID 记入 new_line_ids 队列，
            # 后续 ###BEAT: set 新线 <拍> 时替换为该 ID（跨段可见：②段 add → ③段 set 新线）。
            # 节点落位回填队列（本段内）：(SL-XX, [节拍名…])——由 ###STORYLINE 行内参数
            #   `承载节拍=A,B`（add/rewrite）／`落定节拍=A,B`（close）携带，批末（本段字段写入完成后）
            #   由脚本落到 故事弧线.节点落位.{节拍} = SL-XX——② 的 D1 预先规划全表、结构动作回填，
            #   顺序固定（D1 先写全表 → 本回填覆盖），故不存在同批同键双写歧义。
            _beat_landing = []
            for action, payload in ctx["storyline"]:
                parts = action.split()
                _beats = []
                _clean = []
                for _p in parts:
                    if _p.startswith("承载节拍=") or _p.startswith("落定节拍="):
                        _beats += [b.strip() for b in _p.split("=", 1)[1].split(",") if b.strip()]
                    else:
                        _clean.append(_p)
                parts = _clean
                if not parts or parts[0] not in ("add", "rewrite", "close", "clear"):
                    print(f"[FAIL] ###STORYLINE 动作非法: {action!r}（合法: add / rewrite N / close N / clear N——结构动作·②编剧）——批次拦截", file=sys.stderr)
                    sys.exit(1)
                stdin_text = "\n".join(payload) if payload is not None else None
                try:
                    _ret = cmd_storyline(world_dir, parts, stdin_text=stdin_text)
                except SystemExit as e:
                    print(f"[FAIL] ###STORYLINE 执行失败: {action}（exit {e.code}）——storylines 未更新·批次拦截·修正后重提", file=sys.stderr)
                    sys.exit(1)
                if parts[0] == "add" and _ret is not None:
                    new_line_ids.append(str(_ret))
                    if _beats:
                        _beat_landing.append((str(_ret), _beats))
                elif parts[0] in ("rewrite", "close") and _beats and len(parts) >= 2:
                    _beat_landing.append((_norm_sl_id(parts[1]), _beats))
                applied_ops.append((seg_no, f"###STORYLINE: {action}"))
            for action in ctx["beat"]:
                parts = action.split()
                # 「新线」占位替换：add 刚建的那条线（脚本分配 ID·LLM 不需预知）；未消费可重复引用同批新线
                if len(parts) >= 2 and parts[1] == "新线":
                    if not new_line_ids:
                        print(f"[FAIL] ###BEAT 引用「新线」但本批无已建事件线（###STORYLINE: add 先于 ###BEAT·或结构动作已随此前段成功落盘——重提时 read states/storylines.yaml 填实际 SL-XX）——批次拦截", file=sys.stderr)
                        sys.exit(1)
                    parts[1] = new_line_ids[-1]
                try:
                    cmd_beat(world_dir, parts)
                except SystemExit as e:
                    print(f"[FAIL] ###BEAT 执行失败: {action}（exit {e.code}）——direction 指针未更新·批次拦截·修正后重提", file=sys.stderr)
                    sys.exit(1)
                applied_ops.append((seg_no, f"###BEAT: {action}"))

            # 逐条写入：顶回违规字段，其余照写；任何实际写入失败都使该段失败，不能伪报成功。
            written_count = 0
            op_failures = []
            for idx, (kind, file_key, key_path_str, content, append) in enumerate(ops):
                if idx in blocked:
                    continue
                if kind == "delete":
                    if cmd_delete(world_dir, [file_key, key_path_str]):
                        written_count += 1
                    else:
                        op_failures.append((idx, file_key, key_path_str))
                    continue
                if write_one(file_key, key_path_str, content, append=append):
                    written_count += 1
                else:
                    op_failures.append((idx, file_key, key_path_str))
            if op_failures:
                print(f"[FAIL] {len(op_failures)} 个操作实际失败（其余 {written_count} 个已落盘·KEY 幂等、APPEND 靠查重）——重提：纯 KEY 批只补失败 op；角色段（###STAGE: 角色）整段重发，或补提/字段修复批加 --maintenance（段级闸豁免·op 级照常）——批次不得报告成功:", file=sys.stderr)
                for _idx, _fk, _kp in op_failures:
                    print(f"  - op#{_idx}: {_fk}.{_kp}", file=sys.stderr)
                sys.exit(1)
            # 节点落位回填（本段字段写入完成后·覆盖 D1 批首写入的「待定」）——
            #   本批建线/收束携带的 承载节拍/落定节拍，在此落到 故事弧线.节点落位.{节拍} = SL-XX。
            if _beat_landing:
                _bf = _load_storylines(world_dir)
                if not isinstance(_bf, dict):
                    _bf = {}
                _arc = _bf.get("故事弧线")
                if not isinstance(_arc, dict):
                    _arc = {}
                    _bf["故事弧线"] = _arc
                _nl = _arc.get("节点落位")
                if not isinstance(_nl, dict):
                    _nl = {}
                    _arc["节点落位"] = _nl
                _act = str(_arc.get("当前幕", "") or "")
                _act_key = next((k for k in ARC_BEATS if k in _act), None)
                _backfilled = []
                for _sid, _bs in _beat_landing:
                    _ln = (_bf.get(STORYLINE_TOP_KEY) or {}).get(_sid)
                    if "高潮" in _bs and isinstance(_ln, dict):
                        _bn = [str((_b or {}).get("拍名", "") or "").strip()
                               for _b in (_ln.get("拍序") or []) if isinstance(_b, dict)]
                        if "顶点" not in _bn:
                            print(f"[WARN] 事件线 {_sid} 承载节拍含「高潮」但拍序无「顶点」拍——高潮须落为顶点收束（beat_structure §一·第三幕）·请核对", file=sys.stderr)
                    for _b in _bs:
                        if _act_key and _b not in ARC_BEATS[_act_key]:
                            print(f"[WARN] 承载节拍 '{_b}' 不在当前幕（{_act}）的节拍清单内——键域=当前幕节拍（权威=beat_structure.md §一）·已回填但请核对", file=sys.stderr)
                        _nl[_b] = _sid
                        _backfilled.append(f"{_b}={_sid}")
                write_yaml(world_dir / "states" / STORYLINES_FILE, _bf)
                print(f"[OK] 节点落位 已回填: {' · '.join(_backfilled)}（承载线由脚本分配 ID·② 无需预知）", file=sys.stderr)
            op = "批量追加" if append_mode else "批量写入"
            # 批次账本（各段·落盘成功后才写——闸门拦截/op 失败已在上方 exit，不落账本）
            ctx["blocked"] = blocked
            write_round_ledger(world_dir, ctx)
            # 结构/指针落盘结果置于收尾（tail 可见·无需重放批次确认）
            if ctx["storyline"] or ctx["beat"]:
                print("[OK] ###STORYLINE/###BEAT 已自动执行（storylines 结构 / direction 指针·本轮事件线动作）", file=sys.stderr)
            if blocked:
                print(f"[OK] {op}完成：{written_count} 个操作落盘，{len(blocked)} 个字段被顶回（硬性违规）")
            else:
                print(f"[OK] {op}完成，共 {written_count} 个操作")
            return


        segments = split_stage_segments(lines)
        # 合批白名单（角色自治防火墙·机械兜底）：
        # 允许多段合批仅限 [戏剧家编剧导演] 结构合批；角色段/场记段必须单段独批。
        # 同批同时含 角色+他段、或 场记+他段 = 跨层合批——零副作用整体拦截。
        # 各段内部 gate 仍逐段独立校验（戏剧家段需 CT op·角色段需行动卡三件套等）。
        # 作家段不在合并批·经 write_narrative 独立落盘。
        # 逐段单批（每批一段）与无 ###STAGE 维护/回退批不受影响。
        if len(segments) >= 2 and not force and resume_from is None:
            _declared = [_seg[0][len("###STAGE:"):].strip()
                         for _seg in segments if _seg and _seg[0].startswith("###STAGE:")]
            _has_actor = any("角色" in _d for _d in _declared)
            _has_keeper = any("场记" in _d for _d in _declared)
            _cross = (_has_actor and len(_declared) > 1) or (_has_keeper and len(_declared) > 1)
            if _cross:
                print("[BATCH-FAIL] 跨层合批拦截——角色段/场记段必须单段独批（允许多段合批仅限[戏剧家编剧导演]）:", file=sys.stderr)
                print(f"  声明段: {'/'.join(_declared) if _declared else '（无）'}", file=sys.stderr)
                print("  拆批重提：[①②③]结构合批 → ④角色独批 → ⑤场记独批（--dry-run 同样受此检查）", file=sys.stderr)
                sys.exit(1)
        # --resume-from <N>：只执行段 N 及其后（失败后的重提通道·免重跑已成功段）——
        # 仅当原始批次确有 ≥N 段时合法；段号按原始批次（1 起始）计。
        _tot = len(segments)
        if resume_from is not None:
            if resume_from < 1 or resume_from > _tot:
                print(f"[ERR] --resume-from {resume_from} 越界（本批次段总数 {_tot}）", file=sys.stderr)
                sys.exit(1)
            segments = segments[resume_from - 1:]
        # 轮末判定：批次含「场记」段（场记单独一批时仅场记阶段附跑 round-check——
        # 其他阶段的批次收尾时 world_state 三件套未写，round-check FAIL 属预期噪音，跳过）
        _keeper_round = any(
            _seg and _seg[0].startswith("###STAGE:") and "场记" in _seg[0]
            for _seg in segments
        )
        applied_ops = []  # 已成功落盘的结构动作（###STORYLINE/###BEAT·重提时必须剔除·防非幂等重复）
        new_line_ids = []  # 本批 add 实际分配的 SL-XX（「新线」引用解析队列·跨段共享）
        _start_no = resume_from if resume_from is not None else 1
        for _i, _seg in enumerate(segments):
            seg_no = _start_no + _i
            if len(segments) > 1:
                print(f"[BATCH] ── 段 {seg_no}/{_tot}（重提从 {_start_no} 起） ──", file=sys.stderr)
            try:
                run_batch_segment(_seg, seg_no, applied_ops, new_line_ids)
            except SystemExit:
                _done = sorted({n for n, _ in applied_ops})
                print(f"[BATCH-FAIL] 段 {seg_no}/{_tot} 中止——后续段未执行·批次失败", file=sys.stderr)
                if _done:
                    print("[BATCH-FAIL] 已完整落盘段: " + ", ".join(f"段{n}" for n in _done), file=sys.stderr)
                    print(f"[BATCH-FAIL] 重提时走 `--resume-from {seg_no}`（只跑段 {seg_no} 及其后·不去重跑已成功段）", file=sys.stderr)
                if applied_ops:
                    print("[BATCH-FAIL] 以下结构动作已落盘（重提批次中必须剔除·防重复创建/指针重复推进）:", file=sys.stderr)
                    for sn, op in applied_ops:
                        print(f"[BATCH-FAIL]   [段{sn}] {op}", file=sys.stderr)
                else:
                    print("[BATCH-FAIL] 无已落盘结构动作（本段未产生 ###STORYLINE/###BEAT·重提不需剔除）", file=sys.stderr)
                sys.exit(1)
        if not dry_run:
            quick_validate_summary(world_dir)  # 写入后自动触发轻量校验（每轮必跑·全批一次）
            if _keeper_round:
                # 轮完整性收尾（场记批自动附跑·仅报告不拦截）：FAIL=按 phase_keeper 修复或上报
                try:
                    print("[ROUND] —— 轮完整性收尾检查（场记批自动附跑·仅报告不拦截）——", file=sys.stderr)
                    cmd_round_check(world_dir)
                except SystemExit as e:
                    if e.code:
                        print(f"[ROUND] round-check 未全过(exit {e.code})——按 phase_keeper「轮完整性收尾检查」修复或上报", file=sys.stderr)
        return

    # ── 单字段模式（原有逻辑） ──
    scene_dir = get_scene_dir(world_dir)
    existing = discover_files(world_dir, scene_dir)

    if len(extra) < 2:
        hint = ""
        try:
            raw = sys.stdin.buffer.read()
            if raw.strip():
                if b"###FILE:" in raw or b"###KEY:" in raw:
                    hint = "检测到 ###FILE:/###KEY: 记录格式——记录式批量请用 write-raw --batch（stdin 或 --file 批次文件·中文编码安全）"
                else:
                    hint = "检测到整份 YAML 输入——整份覆盖请用 write --full（stdin YAML）；增量合并用 write"
        except Exception:
            hint = ""
        msg = f"[ERR] 用法: worldctl.py <世界> {'append-raw' if append_mode else 'write-raw'} <文件key> <YAML键路径> [内容]"
        if hint:
            msg += "\n       " + hint
        print(msg, file=sys.stderr)
        sys.exit(1)

    file_key = extra[0]
    key_path_str = extra[1]

    # 内容：CLI 参数优先，否则 stdin
    if len(extra) >= 3:
        content = extra[2]
        if not content.isascii():
            print("[ERR] 单字段模式仅限短 ASCII 值——中文/多行内容经 CLI 参数会随 locale 解码损坏文件，请用 write-raw --batch（stdin 或 --file 批次文件·编码安全通道）", file=sys.stderr)
            sys.exit(1)
    else:
        content = _read_stdin_utf8()

    if not append_mode and content == "":
        print(f"[ERR] 空值覆盖已拒绝: {file_key}.{key_path_str}（write-raw 值不能为空；追加请用 append-raw）", file=sys.stderr)
        sys.exit(1)

    if not write_one(file_key, key_path_str, content, append=append_mode):
        sys.exit(1)

# ── DELETE ───────────────────────────────────────────────────────
def cmd_delete(world_dir: Path, extra: list[str]) -> bool:
    """
    delete: 删除指定键路径。
    用法: worldctl.py <世界> delete <文件key> <YAML键路径>
    示例: worldctl.py westworld delete conflicts CT-05        ← 删除整条 CT
          worldctl.py westworld delete pending_actions 已完成.PA-002
    返回: True=已删除；False=未删除（用法/文件/路径/键任一不成立）——调用方不得当成功处理。
    """
    if len(extra) < 2:
        print("[ERR] 用法: worldctl.py <世界> delete <文件key> <YAML键路径>", file=sys.stderr)
        return False
    file_key = extra[0]
    key_path_str = extra[1]

    scene_dir = get_scene_dir(world_dir)
    existing = discover_files(world_dir, scene_dir)
    # file_key 归一化——与 write_one / check_batch 同源（`###DELETE: conflicts.yaml …` 亦须命中 conflicts 专属路径处理）
    file_key = _normalize_file_key(file_key)
    filepath, note = resolve_char_file(existing, file_key, world_dir)
    if filepath is None:
        if note:
            print(note, file=sys.stderr)
        else:
            print(f"[ERR] 未知文件 key: {file_key}", file=sys.stderr)
        return False
    if note:
        print(note, file=sys.stderr)

    if filepath.name == "world_map.yaml":
        print("[ERR] world_map 禁用点路径删除（键名可含空格/点·点路径与 shell 分词均不支持）——请用 write 命令（YAML diff 合并）", file=sys.stderr)
        return False

    if not filepath.exists():
        print(f"[FAIL] 删除失败：{file_key} 文件不存在（无删除目标）", file=sys.stderr)
        return False

    try:
        data = yaml.safe_load(filepath.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"[ERR] {file_key} 解析失败: {e}", file=sys.stderr)
        return False

    key_path = key_path_str.split(".")
    # conflicts.yaml 路径归一化：去掉多余的 `conflicts.` 根前缀
    if file_key == "conflicts" and key_path and key_path[0] == "conflicts":
        key_path = key_path[1:]

    target = data
    for k in key_path[:-1]:
        if not isinstance(target, dict) or k not in target or not isinstance(target[k], dict):
            print(f"[ERR] 路径不存在: {key_path_str}", file=sys.stderr)
            return False
        target = target[k]

    last = key_path[-1]
    if not isinstance(target, dict) or last not in target:
        print(f"[FAIL] 删除失败：键不存在 {key_path_str}（无删除目标）", file=sys.stderr)
        return False

    # 删除前备份——状态 YAML 不入 git，删错已存在的键不可逆；备份失败即中止（不可回滚就不执行）
    try:
        bak_dir = world_dir / "tmp"
        bak_dir.mkdir(parents=True, exist_ok=True)
        bak = bak_dir / f"{filepath.name}.delete.{_ts()}.bak"
        shutil.copy2(filepath, bak)
    except Exception as e:
        print(f"[ERR] 删除前备份失败: {e}——不执行删除", file=sys.stderr)
        return False

    del target[last]
    write_yaml(filepath, data)
    print(f"[OK] 已删除 {file_key}.{key_path_str}（原文件备份: tmp/{bak.name}）")
    return True

# ── VALIDATE ──────────────────────────────────────────────────────


def cmd_grep(world_dir: Path, keyword: str):
    """在所有状态文件中搜索关键词，输出注册原文——核对元素注册数据的标准工具（D11/W4 前置·防凭印象改写元素形态）。"""
    if not keyword:
        print("用法: worldctl.py <世界> grep <关键词>")
        return
    scene_dir = get_scene_dir(world_dir)
    files = discover_files(world_dir, scene_dir)
    # 额外扫描所有场景的 scene_state.yaml（不只焦点场景——核对历史注册原文必需，防止凭印象改写已有元素形态）
    scenes_dir = world_dir / "scenes"
    if scenes_dir.is_dir():
        for d in sorted(scenes_dir.iterdir()):
            if d.is_dir() and (d / "scene_state.yaml").exists():
                files[f"scenes/{d.name}/scene_state.yaml"] = d / "scene_state.yaml"
    hits = []
    for key, fp in sorted(files.items()):
        if not fp.exists():
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if keyword in line:
                hits.append(f"{key}:{i}: {line.strip()}")
    if hits:
        print(f"[GREP] '{keyword}' 共 {len(hits)} 处（文件key:行号: 内容）：")
        for h in hits:
            print(f"  {h}")
        print("  → 使用已有元素前先核对注册原文（形态/位置/状态），禁止凭印象改写元素。")
    else:
        print(f"[GREP] '{keyword}' 无匹配——该元素未在任何 scene_state/状态文件注册，使用即幻觉。")



def cmd_scan(world_dir: Path, extra: list[str], live_only: bool = False):
    """scan: 全仓残留检查（标准入口，替代手拼 grep --include——BusyBox grep 不支持 --include）。
    递归扫描 worlds/<世界>/ 下所有 .md/.yaml/.yml 文件（排除历史轮转 narrative.*.md、批次原文账本与 archive）。
    退出码: 0=无匹配（干净）· 1=有匹配（残留存在）· 2=用法错误。
    用途: 修改数据/规则后检查旧字段是否残留——失败就是失败，不靠 || echo 兜底。
    """
    if not extra:
        print("用法: worldctl.py <世界> scan <关键词> [--live]  （--live=仅当前文件，跳过历史轮转/账本/archive）", file=sys.stderr)
        sys.exit(2)
    keyword = extra[0]
    world_dir = world_dir.resolve()
    hits = []
    files = sorted(world_dir.rglob("*"))
    for fp in files:
        if not fp.is_file():
            continue
        if fp.suffix.lower() not in (".md", ".yaml", ".yml"):
            continue
        if not live_only:
            # 默认全仓（含历史轮转文件——残留可能藏在旧 narrative）
            pass
        else:
            # --live: 排除历史轮转归档（narrative 轮转 + 批次原文账本 .ledger_r*.yaml）与 archive 目录
            if re.search(r"narrative\.\d{8}_\d{6}\.md$", fp.name) or re.search(r"narrative\.r\d+\.\d{8}_\d{6}\.md$", fp.name):
                continue
            if re.match(r"\.ledger_r.*\.yaml$", fp.name):
                continue
            if "archive" in fp.parts:
                continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = fp.relative_to(world_dir)
        for i, line in enumerate(text.splitlines(), 1):
            if keyword in line:
                hits.append(f"{rel}:{i}: {line.strip()}")
    if hits:
        print(f"[SCAN] '{keyword}' 共 {len(hits)} 处残留：")
        for h in hits:
            print(f"  {h}")
        sys.exit(1)
    print(f"[SCAN] '{keyword}' 无匹配——干净 ✅")
    sys.exit(0)



def _ct_sides(desc: str) -> list[str]:
    """从 CT 对抗双方 文本解析角色名（'A（注释） vs B（注释）' → [A, B]·抽象方无状态文件时调用方跳过）。"""
    if not desc:
        return []
    sides = re.split(r"\s+vs\s+", desc, maxsplit=1)
    if len(sides) < 2:
        sides = re.split(r"vs", desc, maxsplit=1)
        if len(sides) < 2:
            return []
    out = []
    for s in sides:
        name = s.split("（", 1)[0].split("(", 1)[0].strip()
        if name:
            out.append(name)
    return out


def _char_state_field_value(state: dict, field: str):
    """取 CHAR_state 关键字段值——列表字段（记忆锚点/信念演化）返回条数（基准比较用）。"""
    v = state.get(field)
    if field in CLIMAX_LIST_FIELDS:
        return len(v) if isinstance(v, list) else 0
    if isinstance(v, str):
        return v
    if v is None:
        return ""
    return str(v)


def _climax_principals(line: dict | None) -> list[str]:
    """读事件线顶点拍的 顶点约束.关系主体。无顶点约束 → []。"""
    if not isinstance(line, dict):
        return []
    for b in (line.get("拍序") or []):
        if isinstance(b, dict) and str(b.get("拍名", "") or "").strip() == "顶点" and isinstance(b.get(CLIMAX_CONSTRAINT_KEY), dict):
            cons = b[CLIMAX_CONSTRAINT_KEY]
            return [str(x).strip() for x in (cons.get("关系主体") or []) if str(x).strip()]
    return []


def _climax_baseline_snapshot(world_dir: Path, sl_id: str, line: dict | None = None) -> dict:
    """快照 顶点约束.关系主体 的 CHAR_state 声明维度字段（进入顶点拍时记录·顶点拍起点状态）。
    仅关系主体（外部爆破者=压力供应方·其自身状态变化不计入出线——防"改旁观者凑验收"）。
    返回 {角色名: {字段: 基准值}}——无约束/无状态文件时返回空 dict（出线时拦）。"""
    principals = _climax_principals(line)
    if not principals:
        return {}
    existing = discover_files(world_dir, get_scene_dir(world_dir))
    snap: dict[str, dict] = {}
    for s in principals:
        key = f"{CHAR_STATE_PREFIX}{s}{CHAR_STATE_SUFFIX}".removesuffix(".yaml")
        fp2, _ = resolve_char_file(existing, key, world_dir)
        if fp2 is None or not fp2.exists():
            continue
        try:
            st = yaml.safe_load(fp2.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if not isinstance(st, dict):
            continue
        snap[s] = {f: _char_state_field_value(st, f) for f in SUBSTANTIVE_FIELDS}
    return snap


def _snapshot_climax_baseline(line: dict, world_dir: Path, n: str) -> None:
    """进入顶点拍时，自动快照 顶点约束.关系主体 的实质状态字段为 基准快照（脚本自动·LLM 不填不读）。
    落档 states/.climax_baseline_{SL}.yaml（脚本私有·不进 storylines 与任何读取面——对比面不预声明）。"""
    snap = _climax_baseline_snapshot(world_dir, n, line)
    _climax_baseline_fp(world_dir, n).write_text(
        yaml.dump(snap, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8", newline="")


def _norm_sl_id(n) -> str:
    """事件线 id 归一化：纯数字 N / SL-N → SL-XX（两位）。"""
    s = str(n).strip()
    m = re.match(r"^(?:SL-)?(\d+)$", s, re.IGNORECASE)
    if m:
        return f"{STORYLINE_ID_PREFIX}{int(m.group(1)):02d}"
    return s


def _load_storylines(world_dir: Path) -> dict:
    fp = world_dir / "states" / STORYLINES_FILE
    if not fp.exists():
        return {}
    try:
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _load_direction(world_dir: Path) -> dict:
    fp = world_dir / "states" / DIRECTION_FILE
    if not fp.exists():
        return {}
    try:
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _save_direction(world_dir: Path, dr: dict):
    write_yaml(world_dir / "states" / DIRECTION_FILE, dr)


def _storyliner_unref_and_must_add(sl_map: dict, dr: dict, cd: dict):
    """②编剧「未引用活跃线 CT 且无活跃线可接」判定——gate storyliner 与 precheck 共用·单一判据源。
    返回 (must_add, unref_ct, active_sl)：
      · active_sl = storylines 中 状态=活跃 的事件线
      · unref_ct  = conflicts 中 事件线引用 不含任何活跃 SL 的 CT（在表即未收束·收束的已从 conflicts 移除）
      · must_add  = unref_ct 非空 ∧ 无活跃线可接（无活跃线，或 当前拍==余波 且 无其他非余波活跃线可接）
    兑现半（余波是否已兑现）由③回判+审计承担·本判据只做结构半；余波单拍线不计入可接。"""
    active_sl = {k for k, v in (sl_map or {}).items()
                 if isinstance(v, dict) and str(v.get("状态", "") or "").strip() == "活跃"}
    _norm_active = {re.sub(r"\s+", "", str(a).strip()) for a in active_sl}
    unref_ct = []
    if isinstance(cd, dict):
        for _ct, _cv in cd.items():
            if not re.match(r"^CT-", str(_ct)) or not isinstance(_cv, dict):
                continue
            _refs = _cv.get("事件线引用") or []
            if not isinstance(_refs, list):
                _refs = [str(_refs)]
            _hits = {re.sub(r"\s+", "", str(r).strip()) for r in _refs if str(r).strip()}
            if not (_hits & _norm_active):
                unref_ct.append(_ct)
    _cur_sl = str((dr or {}).get("当前事件线", "") or "").strip()
    _cur_beat = str((dr or {}).get("当前拍", "") or "").strip()
    _beats_non_aftermath = ("铺垫", "接触", "升级", "顶点")
    _has_non_aftermath_active = any(
        k != _cur_sl and isinstance(v, dict)
        and any(str(b.get("拍名", "") or "").strip() in _beats_non_aftermath
                for b in (v.get("拍序") or []) if isinstance(b, dict))
        for k, v in (sl_map or {}).items() if k in active_sl)
    _no_active = (not active_sl) or (_cur_beat == "余波" and not _has_non_aftermath_active)
    return (bool(unref_ct) and _no_active), unref_ct, active_sl


def _unarchived_named_roles(world_dir: Path) -> list:
    """从 conflicts.CT*.关联角色 收集无 CHAR 档案/状态文件的具名角色（中文人名不做 NER·以结构化字段为准）。"""
    fp = world_dir / "states" / "conflicts.yaml"
    try:
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return []
    known = set()
    for fpx in list(world_dir.glob("characters/CHAR_*.md")) + list(world_dir.glob("states/CHAR_*_state.yaml")):
        stem = fpx.stem
        if stem.startswith("CHAR_"):
            stem = stem[len("CHAR_"):]
        known.add(stem.replace("_state", "").strip())
    missing = []
    seen = set()
    for ct in (data.values() if isinstance(data, dict) else []):
        if not isinstance(ct, dict):
            continue
        for raw in (ct.get("关联角色") or []):
            name = re.split(r"[（(]", str(raw))[0].strip()
            if name and name not in known and name not in seen:
                seen.add(name)
                missing.append(name)
    return missing


def _check_climax_exit(world_dir: Path, ops, beat_lines) -> tuple[list[str], bool]:
    """顶点出线核验（硬性·gate director --check 调用·收束需要证明）：
    批次声明 `###BEAT: advance SL-XX 余波` 且 direction 当前拍=顶点 时——
    ① 顶点约束齐备（关系主体≥2/核心张力/变化维度合法/非玩家爆破≥1·缺=拦）；
    ② 基准快照存在（进入顶点拍时脚本自动记录·缺=拦）；
    ③ 关系主体的声明维度字段任一实质变化（≠基准快照·当前文件+批次写 op 预演·来源不限——主体选择/对手/
       外部爆破/世界事件皆可）——主体全无变化=顶点未落地（拦·撤回③导演）；
    ④ 爆破结算声明：本批 direction.承接判断 须含一行「爆破兑现：<事实>」或「爆破豁免：<理由>」——
       非玩家爆破是设计承诺·出线必须对它表态（验表态存在·不验演出本身）。
    ⑤ 张力结算声明：承接判断 须含一行「张力结算：<核心张力是否被推至临界·以何为凭>」——
       顶点约束=目的声明（关系必须被推至的转变临界）·爆破只是手段；判定为未达临界（含被爆破/意外打断）
       → 必须追加「张力去向：<登记进余波拍或新线的承接方式>」——张力未落地的顶点不允许静默出线。
    验收=关系主体的声明维度发生实质变化（任一来源）；外部爆破者为加压力量·演出不参与验收·但出线须对它结算表态。
    返回 (违规消息列表, 是否执行了核验)。"""
    violations: list[str] = []
    checked = False
    if not beat_lines:
        return violations, checked
    sl_id = None
    for bl in beat_lines:
        m = re.match(r"^advance\s+(\S+)\s+余波\s*$", str(bl).strip())
        if m:
            sl_id = _norm_sl_id(m.group(1))
            break
    if sl_id is None:
        return violations, checked
    checked = True
    # direction：当前事件线/当前拍=顶点 才核验（非顶点出线不拦截）
    dr = _load_direction(world_dir)
    if str(dr.get("当前事件线", "") or "").strip() != sl_id:
        return violations, checked
    if str(dr.get("当前拍", "") or "").strip() != "顶点":
        return violations, checked
    # storylines：读事件线与顶点约束
    st = _load_storylines(world_dir)
    line = (st.get(STORYLINE_TOP_KEY) or {}).get(sl_id)
    if not isinstance(line, dict):
        violations.append(f"顶点出线（advance {sl_id} 余波）失败——storylines 无事件线 {sl_id}")
        return violations, checked
    cons = None
    for b in (line.get("拍序") or []):
        if isinstance(b, dict) and str(b.get("拍名", "") or "").strip() == "顶点":
            cons = b.get(CLIMAX_CONSTRAINT_KEY)
            break
    if not isinstance(cons, dict):
        violations.append(f"顶点出线（advance {sl_id} 余波）缺 顶点约束（Vertex Constraint——关系主体/核心张力/变化维度/非玩家爆破·建线/换线时预填·旧字段 顶点落点 需 rewrite）")
        return violations, checked
    principals = [str(x).strip() for x in (cons.get("关系主体") or []) if str(x).strip()]
    if len(set(principals)) < 2:
        violations.append("顶点约束.关系主体 需 ≥2 去重角色（顶点的单位是关系不是单人·不区分玩家/NPC）")
        return violations, checked
    if not str(cons.get("核心张力", "") or "").strip():
        violations.append("顶点约束.核心张力 为空（必须被推至临界的未决问题·点名赌注所在）")
        return violations, checked
    dims = [str(d).strip() for d in (cons.get("变化维度") or []) if str(d).strip()]
    bad_dims = [d for d in dims if d not in DIM_ENUM]
    if not dims or bad_dims:
        violations.append(f"顶点约束.变化维度 非法（{bad_dims or '空'}——枚举: {'/'.join(DIM_ENUM)}）")
        return violations, checked
    blasters = [str(x).strip() for x in (cons.get("非玩家爆破") or []) if str(x).strip()]
    if not blasters:
        violations.append("顶点约束.非玩家爆破 为空（≥1 外部角色或事件——压力供应方：主体全静止时逼上悬崖的力量·防死锁）")
        return violations, checked
    # 基准快照（脚本私有落档·进入顶点拍时自动记录）——缺则拦
    baseline = _load_climax_baseline(world_dir, sl_id)
    if not isinstance(baseline, dict) or not baseline:
        violations.append(f"顶点基线未建档（beat set/advance 进入顶点拍时脚本自动落档）·先 deepen {sl_id}·建档后再出线")
        return violations, checked
    # ④ 爆破结算声明：本批 direction.承接判断 对非玩家爆破表态——兑现事实或豁免理由
    _verdict_txt = ""
    for _kind, _fk, _kp, _content, _append in ops:
        if _kind == "write" and str(_fk).strip().lower() == "direction" and str(_kp).strip() == "承接判断":
            _verdict_txt = str(_content)
    if not re.search(r"爆破(兑现|豁免)\s*[:：]", _verdict_txt):
        violations.append(
            "顶点出线批缺 爆破结算——direction.承接判断 须一行「爆破兑现：<非玩家爆破实际发生了什么>」或「爆破豁免：<为何不经爆破出线>」（约束五字段的出线表态·防爆破要素被静默丢弃）"
        )
    # ④b 张力结算声明：顶点约束=目的声明（关系必须被推至的转变临界）·爆破只是手段——出线必须对目的表态；
    #    张力未落地（含被爆破/意外打断）的顶点不允许静默出线——须显式登记去向由余波/新线兑现
    _m_tension = re.search(r"张力结算\s*[:：]\s*([^；;\n]*)", _verdict_txt)
    if not _m_tension:
        violations.append(
            "顶点出线批缺 张力结算——direction.承接判断 须一行「张力结算：<核心张力是否被推至临界·以何为凭>」（顶点的目的是关系被推至临界·手段可千变万化·验收只认目的）"
        )
    elif re.search(r"未达临界|未推至临界|被打断|中断|悬置", _m_tension.group(1)) and not re.search(r"张力去向\s*[:：]", _verdict_txt):
        violations.append(
            "张力结算为未达临界——direction.承接判断 须追加一行「张力去向：<显式登记进余波拍或新线的承接方式>」（张力未落地的顶点不允许静默出线·悬置的赌注必须有人接）"
        )
    # 预演比较：关系主体的实质状态字段任一 ≠ 基准 = 真实变化发生（任一来源·比对面=脚本层常量·不预声明）
    existing = discover_files(world_dir, get_scene_dir(world_dir))
    changed_any = False
    detail: list[str] = []
    for side, base_fields in baseline.items():
        if not isinstance(base_fields, dict):
            continue
        key = f"{CHAR_STATE_PREFIX}{side}{CHAR_STATE_SUFFIX}".removesuffix(".yaml")
        fp2, _ = resolve_char_file(existing, key, world_dir)
        cur: dict = {}
        if fp2 is not None and fp2.exists():
            try:
                d2 = yaml.safe_load(fp2.read_text(encoding="utf-8")) or {}
                cur = d2 if isinstance(d2, dict) else {}
            except Exception:
                cur = {}
        for field, base in base_fields.items():
            val = _char_state_field_value(cur, field)
            for kind, fk, kp, content, append in ops:
                if kind != "write" or fk != key or kp != field:
                    continue
                if field in CLIMAX_LIST_FIELDS:
                    n_items = 0
                    if isinstance(content, str):
                        n_items = content.count("\n- ") + (1 if content.strip().startswith("- ") else 0)
                    val = (val + n_items) if append else n_items
                else:
                    if not append:
                        val = content
            if str(val) != str(base):
                changed_any = True
                detail.append(f"{side}.{field}: {base!r} → {val!r}")
    if not changed_any:
        violations.append(
            f"顶点未落地——演出未产生足以证明临界达成的真实改变（基线比对未通过）·留顶点（###BEAT: deepen {sl_id}）·非玩家爆破可加压；判线作废则 ###STORYLINE: rewrite {sl_id} 重声明 顶点约束"
        )
    else:
        print("[GATE] 顶点出线核验通过（收束证明成立）", file=sys.stderr)
    return violations, checked


def _load_audit_words(world_dir: Path) -> tuple[set, list, set]:
    """W4 词表加载（世界级配置·可移植性修复）：worlds/{世界}/audit_words.yaml 优先，缺省用内置通用词表。
    返回 (锚点词集, 位置冲突模式 [(正则, [冲突词])], 豁免专名集)。"""
    default_anchor = {"门", "窗", "床", "楼梯", "钢琴", "吧台", "暗门", "金库", "后厨", "油灯",
                      "纸玫瑰", "大门", "正门", "散桌", "房间", "门帘", "教堂", "月台", "墙根",
                      "柜台", "长椅", "地窖", "盖板", "楼梯口", "窗户", "酒杯", "筷子"}
    default_loc = [
        ("二楼", ["楼下", "一楼", "下楼", "走上楼去弹"]),
        ("一楼", ["楼上", "二楼", "上楼"]),
        ("吧台后", ["门外", "街上"]),
        ("后厨", ["二楼"]),
        ("门口", ["楼上"]),
    ]
    default_known = {
        "Guest", "Mesa", "QA", "游客", "便衣", "灰衣", "前门便衣",
        "Westworld", "Sweetwater", "Mariposa", "Delos", "Welcome", "Center",
        "Host", "Hosts", "Smart", "Ammo", "Mesa Hub", "The Maze", "Maze",
    }
    fp = world_dir / "audit_words.yaml"
    if fp.exists():
        try:
            data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
            if isinstance(data, dict):
                anchor = {str(w) for w in (data.get("锚点词") or [])} or default_anchor
                loc = [tuple(x) for x in (data.get("位置冲突") or []) if isinstance(x, list) and len(x) == 2] or default_loc
                known = {str(w) for w in (data.get("豁免专名") or [])} or default_known
                return anchor, loc, known
        except Exception:
            pass
    return default_anchor, default_loc, default_known


# 场景头行判据（形如 `场景名 · 第1日 09:52 · 轮次 16`）——跨场景轮的合并正文含两条头行，
# 剥离全部头行后再做 W1/W4/W5/长度统计（头行不是叙事正文）。
_SCENE_HEADER_RE = re.compile(r"·\s*轮次\s*\d+")


def _strip_scene_headers(text: str) -> str:
    """剥掉所有场景头行（单场景轮 1 条·跨场景轮 2 条）。"""
    return "\n".join(ln for ln in text.splitlines() if not _SCENE_HEADER_RE.search(ln))


def _split_narr_sentences(text: str) -> list[str]:
    """W5 复读检测·分句（与 gate writer --check 同一套逻辑）：去场景头行·按句末标点切分·短句过滤。"""
    body = _strip_scene_headers(text)
    parts = re.split(r"[。！？\n]+", body)
    out = []
    for p in parts:
        p = re.sub(r"\s+", "", p.strip())
        if len(p) >= 12:
            out.append(p)
    return out


def _check_writer_repetition(raw: str, world_dir: Path) -> list[str]:
    """W5 复读机械拦截：本轮正文 vs 最近 3 个叙事轮转文件。
    整句原文复用 ≥2 句，或长分句（连续 15 字）复用 ≥3 处 → 拦截。
    循环世界合法重复（短称谓/专名）因短句过滤与阈值不受影响；史料不足（<1 个旧文件）跳过。"""
    scenes_dir = world_dir / "scenes"
    if not scenes_dir.is_dir():
        return []
    cands = sorted(scenes_dir.glob("*/narrative.r*.*.md"), key=lambda p: p.stat().st_mtime)
    if not cands:
        return []
    prev_files = cands[-3:]
    prev_sents: set[str] = set()
    prev_combined = []
    for fp in prev_files:
        try:
            txt = fp.read_text(encoding="utf-8")
        except Exception:
            continue
        sents = _split_narr_sentences(txt)
        prev_sents.update(sents)
        prev_combined.append("".join(sents))
    if not prev_sents:
        return []
    combined = "".join(prev_combined)
    cur_sents = _split_narr_sentences(raw)
    exact = [s for s in cur_sents if s in prev_sents]
    clause_hits = []
    for s in cur_sents:
        if s in prev_sents or len(s) < 15:
            continue
        for i in range(0, len(s) - 15 + 1, 5):
            if s[i:i + 15] in combined:
                clause_hits.append(s)
                break
    fails = []
    if len(exact) >= 2:
        shown = " / ".join("「" + s[:20] + "…」" for s in exact[:3])
        fails.append(f"整句复用 {len(exact)} 句：{shown}")
    if len(clause_hits) >= 3:
        shown = " / ".join("「" + s[:20] + "…」" for s in clause_hits[:3])
        fails.append(f"长分句复用 {len(clause_hits)} 处：{shown}")
    return fails


def cmd_gate(world_dir: Path, extra: list[str], check_mode: bool = False, input_file: str | None = None, target: str | None = None, style: str | None = None):
    """gate: 六阶段流程闸门——各阶段批次出口核验。
    用法: worldctl.py <世界> gate dramatist|storyliner|director|actor|keeper|writer [--check] [--file 批次文件] [--target 大约数] [--style sepia|dialogue|explicit]
    - 无 --check: 输出该阶段人工审计清单，要求逐项作答（通过/不通过/跳过+证据）。
    - 带 --check: 批次类从 stdin 或 --file 读该阶段批次（###STAGE 声明），运行可代码化检查——
      Single Writer 越权（硬）+ 阶段必含项（soft→硬拦）+ 字段级硬性检查（同一 check_batch 引擎）；
      director 另跑顶点出线核验；writer 读叙事跑 W4 锚点/人物存在性核验。不合格 exit 1。"""
    phase = extra[0] if extra else ""
    PHASE_CN = {"dramatist": "戏剧家", "storyliner": "编剧", "director": "导演",
                "actor": "角色", "keeper": "场记", "writer": "作家"}
    CHECKLISTS = {
        "dramatist": [
            "C1 冲突推进: ≥1 条 CT 推进/注册（推进池非空·判据=phase_dramatist D10）",
            "C2b 施压方向: 本轮推进的每条 CT 已带 CT-{XX}.施压方向（余波已兑现批豁免——只结算不施压；枚举：死局两难/防御踩爆/关系爆破/不可逆代价/维持；四爆破缺压力说明·说明写压力来源/受力点/转变方向；停滞旗标在场时禁全维持）（判据=phase_dramatist D11）",
            "C2 代价: CT 对抗双方可核验变化（资源易主/控制权易手/新增伤害/被迫选择/关系档位）（判据=phase_dramatist D1）",
            "C3 实质推进: 对抗加码或重大转折（冷却不写弱）（判据=phase_dramatist D5）",
            "C4 抽象方: 显现机制+本轮出手形态+抵抗痕迹（判据=phase_dramatist D8）",
            "C5 循环轨道: 偏离检测（决策/行动 vs CHAR_.md 默认循环时间线基线）+冲突化+兜底（判据=phase_dramatist D7/D8）",
            "C6 CT 存续: 收束判据＝相位=休眠 ∧ 被争夺资源已有定论 ∧ 无未决时机 → ###DELETE: CT-XX；休眠≠消解（相位=休眠的 CT 仍挂在 conflicts）（判据=phase_dramatist D6）",
            "C7 压力扫描逐源: 十源＋爆破源逐源表态（人际/目标/资源/轨道/跨叙事/时间/环境/法则/扩散/兜底/爆破源）——缺任一＝本层未扫描（判据=phase_dramatist D8）",
        ],
        "storyliner": [
            "S1 建线与取材: 合并触发（机械硬拦）——未引用活跃线 CT 且无活跃线可接（无活跃线，或余波已兑现且无其他非余波活跃线可接）→必含 add；含add时META须回显取材来源且该CT未命中活跃线（判据=phase_storyliner D4/D5）",
            "S2 归位与收束: escalation_flags.不承接在场→必含 add/rewrite/clear 三问定原线去向（三分支恒命中一格）；close必带一行 收束摘要；余波拍戏剧问题限沉淀类（判据=phase_storyliner D2/D3）",
            "S3 拍序设计: 每拍戏剧问题有边界可回答（禁无界持续描述）＋字段齐备＋拍名∈五段式枚举不重复＋拍序≥2拍（判据=phase_storyliner D6）",
            "S4 顶点约束: 关系主体≥2 + 核心张力点名赌注所在 + 变化维度 + 非玩家爆破≥1（外部加压·防死锁）（判据=phase_storyliner D6）",
            "S5 弧线定位与节拍落位: storylines.故事弧线 vs SETTING 弧线声明（当前幕/张力基调）——须含 ###KEY: 故事弧线.*；节点落位 键域=当前幕节拍清单且本幕节拍列全（待定堆积=宏观结构跟不上的信号）（判据=phase_storyliner D1）",
            "S6 LOOPS 融入: 在轨节拍并入结构（无来源标记·角色层不知晓）（D6 附加约束）",
        ],
        "director": [
            "R1 回判: 上轮结果 vs 当前拍戏剧问题（四维度·含意外事件）",
            "R2 承接判断: 当前拍继续的理由或进入下一拍的理由（已写入 direction）",
            "R3 演出状态: 上升/持续/转折/收束/停滞（停滞→escalation flag）",
            "R4 guidance: 问题+张力方向·禁预写角色行动",
            "R5 场景切换: 物理变化/跨天必切（机械规则）",
        ],
        "actor": [
            "A1 行动卡三件套 + 有条件代价: ###ACTION 驱动/情绪/强度（缺一拒绝）·`代价` 命中条件才写（audit ①/①b/⑨）",
            "A2 反顺从四则: 档案强度/抽象方显现/认知闸门/VB 升级路径；取舍与代价引自 1.4 账本",
            "A3 认知上限: 循环档位速查（脚本/漂移/觉醒/变质·元视角禁令）",
            "A4 用户角色: 行动资格=仅用户输入·禁引擎代笔定性抉择",
            "A5 记忆: 入锚记下来（actor_decision.md 写入节）+ 角色覆盖/记忆✓ 留痕",
            "A6 计划-动作一致性: 覆盖源＝actor_decision.md D3 长期计划巡检 判定；轨迹 计划变化 是本轮记录——记「调整」却未覆盖、或覆盖而未记「调整」= 拦",
        ],
        "keeper": [
            "K1 场景事实: 场景时间线/出场摘要（集合索引）/道具锚点线索",
            "K2 世界事实: 时间/轮次/前情/倒计时走表",
            "K3 落点: 焦点场景目录（world_state.焦点场景 唯一权威）",
            "K4 轮完整: round-check 收尾",
            "K5 Single Writer: 场记批不写 CHAR_state（角色意志文件·唯一写者=④角色）",
        ],
        "writer": [
            "W1 POV 过滤: 单镜头·只写 POV 感知与身体显影·他人内心与意图不入文·焦外不进正文",
            "W2 代价在纸上 + 特异性（换人测试·复读机械拦截见 --check）",
            "W3 一致性: 卡里记的事不得增减·怎么讲全归作家（逐条转抄叙述措辞=不通过·行为可写且优先·台词照卡上那句的意思说成这个人会说的话·字句由作家定）·行为偏移落地不解释来源",
            "W4 锚点约束: 元素/人物存在性（代码化核对）",
            "W6 文学自查: 对照 narrative_style_sepia（删什么：三并列/连词堆叠/抽象大词簇/反思尾·句长参差·朗读·白名单先查；补什么：语气词/单音节动词/主语省略/平实说话标签·按语域定档；变质地：相邻段落勿同一质·人工项）",
        ],
    }
    if phase not in PHASE_CN:
        print("用法: worldctl.py <世界> gate dramatist|storyliner|director|actor|keeper|writer [--check]", file=sys.stderr)
        print("  dramatist/storyliner/director/actor/keeper: 阶段批次闸门（stdin/--file=该阶段 ###STAGE 批次）", file=sys.stderr)
        print("  writer: 叙事输出闸门（stdin/--file=叙事正文·W4 代码化核验·可选 --target 大约目标数/--style 风格路径）", file=sys.stderr)
        print("  --check: 运行可代码化硬性核验，不合格 exit 1", file=sys.stderr)
        sys.exit(1)

    stage_cn = PHASE_CN[phase]
    print("=" * 60, file=sys.stderr)
    print(f"[GATE] {stage_cn}阶段出口闸门（独立审计·默认不通过·逐项找茬）", file=sys.stderr)
    for line in CHECKLISTS[phase]:
        print("  " + line, file=sys.stderr)
    print("  输出格式: 逐项 {通过|不通过|跳过}+证据 → 全部通过才进下一阶段", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    if not check_mode:
        return

    if phase == "writer":
        if check_mode:
            raw = _read_input_utf8(input_file)
            if not raw.strip():
                print("[GATE] 未提供叙事（stdin/--file 为空）——W1/W3 无法代码化核验，请人工逐项作答", file=sys.stderr)
                return
            # 正文＝剥掉所有场景头行（单场景轮 1 条·跨场景轮 2 条）；W1/W4/W5/长度统计一律在正文上做。
            # 跨场景轮（write_narrative --scene2）提交的是**合并正文**——长度下限按本轮合并正文计，不因拆段各拦一次。
            _body = _strip_scene_headers(raw)
            # W4 可代码化部分（与 write_narrative.py 同一套逻辑）：叙事「」内专名若命中锚点词，
            # 必须与注册名有完整包含关系；位置型锚点核对叙事同语境无矛盾位置词
            registered = {}
            scenes_dir = world_dir / "scenes"
            if scenes_dir.is_dir():
                for sdir in sorted(scenes_dir.iterdir()):
                    ssp = sdir / "scene_state.yaml"
                    if ssp.exists():
                        try:
                            sdata = yaml.safe_load(ssp.read_text(encoding="utf-8"))
                        except Exception:
                            continue
                        if not isinstance(sdata, dict):
                            continue
                        for fld in ("物理锚点", "道具"):
                            val = sdata.get(fld)
                            if not val:
                                continue
                            if isinstance(val, list):
                                for it in val:
                                    if isinstance(it, dict) and str(it.get("名称", "") or "").strip():
                                        # 注册名称+描述（W4 包含关系匹配·desc=位置/状态）
                                        registered.setdefault(str(it["名称"]).strip(),
                                                              f"{str(it.get('位置', '') or '').strip()} {str(it.get('状态', '') or '').strip()}")
                                continue
                            for line in str(val).splitlines():
                                line = line.strip()
                                m = re.match(r"^(?:\d+\.\s*|[A-Z]+\d*\s+|[·\-]\s*)?([^:：—]+?)\s*[:：—]\s*(.*)$", line)
                                if m:
                                    registered.setdefault(m.group(1).strip(), m.group(2).strip())
                                pm = re.match(r"^\|\s*P\d+\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|", line)
                                if pm:
                                    registered.setdefault(pm.group(1).strip(), pm.group(2).strip())
            anchor_words, LOC_PATTERNS, KNOWN_NO_CHAR = _load_audit_words(world_dir)
            quoted = set(re.findall(r"「([^」]{1,12})」", _body))
            suspect = []
            # 对话语境跳过：前 4 字含言语动词 或 「」内以句末标点结尾 → 是台词，不是空间元素引用
            SPEECH_VERBS = r"说|问|答|叫|喊|骂|复述|念|低声道|开口|吼|嚷|应声"
            for q in quoted:
                pos = _body.find("「" + q + "」")
                prev = _body[max(0, pos - 4):pos]
                is_speech = bool(re.search(SPEECH_VERBS, prev)) or q.endswith(("。", "？", "！", "——"))
                if is_speech:
                    continue
                hit_word = next((w for w in anchor_words if w in q), None)
                if not hit_word:
                    continue
                matches = [(rname, rdesc) for rname, rdesc in registered.items()
                           if q == rname or q in rname or rname in q]
                if not matches:
                    suspect.append(f"{q}（未注册——「{hit_word}」在注册表中无包含关系匹配）")
                    continue
                ctx = _body[max(0, _body.find(q) - 25): _body.find(q) + len(q) + 25]
                for rname, rdesc in matches:
                    for loc_re, conflict_words in LOC_PATTERNS:
                        if re.search(loc_re, rdesc):
                            for cw in conflict_words:
                                if cw in ctx:
                                    suspect.append(f"{q}（注册「{rname}」位置含「{loc_re}」但叙事同语境出现「{cw}」）")
                                    break
            # W4 人物存在性（可代码化项·与 gate_writer.md 一致）：叙事中具名角色 vs CHAR_*.md
            # 规则：每个具名/有台词/有行动的人物必须有 CHAR_.md（新人物二选一：补注册/降级背景剪影）
            # 代码化边界：只能可靠拦截「英文专名型」新人物；描述性称谓（骑马者/长外套）由写作时数据忠诚③人工拦截
            char_md_names = set()
            for fp in world_dir.glob("characters/CHAR_*.md"):
                stem = fp.stem[len("CHAR_"):].strip()
                if stem:
                    char_md_names.add(stem)
            # 豁免：非角色专名（场景/组织/道具/系统）+ Guest/玩家 + 已知无档案的叙事称谓
            # 词表来源=audit_words.yaml（缺省内置通用词表·见 _load_audit_words）
            # 提取叙事中出现的英文专名（大写开头词/词组·排除句首·排除全大写缩写）
            name_pat = re.compile(r"\b([A-Z][a-zA-Z]+(?:[\s][A-Z][a-zA-Z]+)*)\b")
            text_no_speech = re.sub(r"「[^」]*」", "", _body)  # 去对话（台词内人名不算引用）
            found_names = set()
            for m in name_pat.finditer(text_no_speech):
                name = m.group(1).strip()
                # 排除句首（前一个非空白字符是句号/叹号/问号/破折号——换行不算句首）
                prev_ch = text_no_speech[max(0, m.start() - 1):m.start()]
                if prev_ch in "。！？—":
                    continue
                found_names.add(name)
            # 从 found_names 中挑出「非豁免 且 非 CHAR 名单」的 → 缺失档案
            char_suspect = []
            for n in sorted(found_names):
                if n in KNOWN_NO_CHAR:
                    continue
                if any(n == real or n in real or real in n for real in char_md_names):
                    continue
                # 可能误报（普通英文词/地名）——仅当该名在叙事中承担行动者角色才报：
                # 后续出现「XX说/问/答/喊」或「XX 从/走/进/推」结构
                action_ctx = re.search(rf"{re.escape(n)}\s*(说|问|答|喊|吼|嚷|开口|走进|走出|推门|站在|从门外|从街角|翻身下马)", _body)
                if action_ctx:
                    char_suspect.append(f"{n}（叙事中作为行动者出现但 CHAR_*.md 缺失——阶段1 补注册或降级背景剪影）")
            if char_suspect:
                print(f"[GATE] W4 人物存在性失败——叙事中具名行动人物无 CHAR_*.md: {char_suspect}（数据忠诚③人物项·新人物二选一：补注册/降级不具名不说话）", file=sys.stderr)
                sys.exit(1)
            if suspect:
                print(f"[GATE] W4 锚点核验失败——叙事「」内元素疑似未注册或位置冲突: {suspect}（请用 worldctl.py <世界> grep <元素名> 核对注册原文）", file=sys.stderr)
                sys.exit(1)
            print("[GATE] W4 锚点核验通过（叙事「」内专名均已注册且位置一致）", file=sys.stderr)
            # W1/W2 机械拦截（沉浸模式可代码化的部分）：抽象失去宣言 + 引擎术语入叙述句
            _narr_body = re.sub(r"「[^」]*」", "", _body)
            _w1_fails = []
            _loss_pat = re.compile(r"(你失去了|她失去了|他失去了|你已失去|不再由你决定|再也不能.*回到|失去了.*控制权|失去了.*距离)")
            for _m in _loss_pat.finditer(_narr_body):
                _ctx = _narr_body[max(0, _m.start() - 30): _m.end() + 30].strip().replace("\n", " ")
                _w1_fails.append(f"抽象失去宣言:「{_ctx}」")
            _engine_terms = ["代价", "施压方向", "紧迫度", "记忆僭越", "内部状态", "顶点约束", "偏离登记", "防御有效性", "被争夺资源", "施压", "CT-0", "SL-0"]
            for _term in _engine_terms:
                if _term in _narr_body:
                    _w1_fails.append(f"引擎术语入文:「{_term}」")
            if _w1_fails:
                print(f"[GATE] W1/W2 显影失败——叙事含上帝视角/引擎术语直说: {_w1_fails}（W1禁上帝视角+引擎术语不入文；W2代价须写成可观察显影，见 phase_writer.md W1/W2）", file=sys.stderr)
                sys.exit(1)
            print("[GATE] W1 显影核验通过（无抽象失去宣言·无引擎术语入叙述句）", file=sys.stderr)
            # W5 复读机械拦截（代码化·注意力零负担）：本轮 vs 最近 3 个叙事轮转文件
            _w5_fails = _check_writer_repetition(_body, world_dir)
            if _w5_fails:
                print(f"[GATE] W5 特异性失败——叙事复用前文句式: {_w5_fails}（按 phase_writer.md W5 取材管道重写：只写本轮新变量·余光限一句且换感官通道）", file=sys.stderr)
                sys.exit(1)
            print("[GATE] W5 特异性核验通过（无跨轮整句/长分句复用）", file=sys.stderr)
            # 长度统计（软性·不拦截）：只回报本轮正文 token 估算值（篇幅由作家按 phase_writer.md「长度与风格」自定）
            # 口径=剥掉所有场景头行后的完整正文（含对话）去空白，token 估算=CJK 字符按 1:1·其余字符每 4 个计 1 token
            # 跨场景轮提交的是合并正文——本节长度即**本轮**长度（write_narrative --scene2 不拆段各算）
            _plain = re.sub(r"\s+", "", _body)
            _cjk = len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", _plain))
            _other = len(_plain) - _cjk
            _wc = _cjk + ((_other + 3) // 4)
            if target:
                print(f"[GATE] 定靶回显: 大约目标 ≈{target} tokens·本轮正文 ≈{_wc} tokens", file=sys.stderr)
            if style:
                print(f"[GATE] 风格回显: 本轮风格路径={style}", file=sys.stderr)
            if _wc < _WRITER_MIN_TOKENS:
                print(f"[GATE] 长度硬拦: 本轮正文 ≈{_wc} tokens, 低于 token 下限（查询轮/维护轮豁免·维护短文本走 write_narrative --force）——未按作家指引执行（疑似失忆）: 先重读 references/phase_writer.md ＋本轮风格 references/narrative_style_*.md, 再重做作家阶段（生成→落盘）。叙事未落盘。", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"[GATE] 长度统计: 本轮正文 ≈{_wc} tokens（启发式估算·CJK按1:1·其他÷4·含对话）", file=sys.stderr)
            print("[GATE] 回合收尾提醒（沉浸式）：正文只含叙事·回合结束零正文输出（状态摘要/执行汇报/叙事复述/下一步引导一律禁止）", file=sys.stderr)
            return

    # ── 批次类闸门（dramatist/storyliner/director/actor/keeper）──
    raw = _read_input_utf8(input_file)
    if not raw.strip():
        print(f"[GATE] 未提供 {stage_cn} 批次——gate --check 不复检已落盘状态·须把本段批次文本（含 ###STAGE 行）经 stdin/--file 提交——闸门拦截：不进下一阶段", file=sys.stderr)
        sys.exit(1)
    ctx = parse_batch_entries(raw.split("\n"))
    ops, parse_errors = ctx["ops"], ctx["errors"]
    if ctx["stage"] != stage_cn:
        print(f"[GATE] ###STAGE 缺失或与阶段不匹配（声明={ctx['stage'] or '无'}·期望={stage_cn}）——批次首行须为 `###STAGE: {stage_cn}`；若首行看似正确仍报此错，检查文件是否带 BOM/编码损坏", file=sys.stderr)
        sys.exit(1)
    hard, soft = check_batch(ops, world_dir, ctx, enforce_scene_dir=False, via="gate")
    # 回显
    if ctx["stage"]:
        print(f"[GATE] ###STAGE 回显: {ctx['stage']}", file=sys.stderr)
    if ctx["storyline"]:
        print(f"[GATE] ###STORYLINE 回显: {ctx['storyline'][0][0]}", file=sys.stderr)
    if ctx["beat"]:
        print(f"[GATE] ###BEAT 回显: {ctx['beat'][0]}", file=sys.stderr)
    if ctx["action"]:
        sched = ctx["schedule"][0] if ctx["schedule"] else "（无）"
        print(f"[GATE] ###ACTION 回显: {len(ctx['action'])} 条行动卡 · SCHEDULE: {sched}", file=sys.stderr)
    if ctx["meta"]:
        print(f"[GATE] ###META 回显: {ctx['meta'][0]}", file=sys.stderr)
    else:
        print("[GATE] 软性告警: 未检测到 ###META: 静默自查锚点（查询轮/维护轮豁免）", file=sys.stderr)
    for _idx, _msg in soft:
        if _idx != -1 and "预检软提示" in _msg:
            print(f"[GATE] 软性提示: {_msg}", file=sys.stderr)
    # 阶段不匹配 = 硬拦（防把别的阶段批次喂进错误闸门）
    if ctx["stage"] and ctx["stage"] != stage_cn:
        hard.append((-1, f"###STAGE '{ctx['stage']}' 与闸门阶段 {stage_cn} 不匹配——各阶段批次走自己的闸门"))
    # 阶段必含项（soft→硬拦）
    batch_required = [msg for idx, msg in soft if idx == -1 and msg.startswith(f"{stage_cn}批应含")]
    # director：顶点出线核验（advance SL-XX 余波）
    climax_violations = []
    if phase == "director":
        climax_violations, _climax_checked = _check_climax_exit(world_dir, ops, ctx["beat"])
    # storyliner：空拍提醒（软性·建线应预设完整拍序）
    if phase == "storyliner":
        for n, ln in sorted((_load_storylines(world_dir).get(STORYLINE_TOP_KEY) or {}).items()):
            if isinstance(ln, dict):
                for w in _empty_beat_warnings(ln):
                    print(f"[GATE] 提醒: 事件线 {n} {w}", file=sys.stderr)
    hard_msgs = [msg for _, msg in hard]
    if parse_errors or hard_msgs or batch_required or climax_violations:
        print(f"[GATE] {stage_cn}阶段代码化核验失败——批次不合格:", file=sys.stderr)
        for e in parse_errors:
            print(f"  - {e}", file=sys.stderr)
        for msg in hard_msgs:
            print(f"  - {msg}", file=sys.stderr)
        for msg in batch_required:
            print(f"  - {msg}", file=sys.stderr)
        for msg in climax_violations:
            print(f"  - {msg}", file=sys.stderr)
        sys.exit(1)
    # 其余软性提醒打印不拦截
    for idx, msg in soft:
        if idx == -1 and not msg.startswith(f"{stage_cn}批应含"):
            print(f"[GATE] 提醒: {msg}", file=sys.stderr)
    print(f"[GATE] {stage_cn}阶段代码化核验通过（硬性必含项齐备）——人工清单请逐项作答", file=sys.stderr)



# ── CONFLICTS_SEED 净化（init-states 物化前置）──────────────────
# 模板是 Markdown 文档（标题/引用块/HTML 注释/占位骨架），原样拼进 states/conflicts.yaml
# 会让 YAML 解析失败（`> **角色（硬性）：**` → block scalar 报错）。物化前剥离非数据行。
_SEED_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_SEED_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
_SEED_HEADING_BARE_RE = re.compile(r"^\s{0,3}#{1,6}\s*$")
_SEED_QUOTE_RE = re.compile(r"^\s*>")
_SEED_HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
_SEED_PLACEHOLDER_VALUE_RE = re.compile(r"^\s*[^\s#][^:\n]*:\s*\[[^\[\]]*\]\s*(?:\(例[:：].*\))?\s*$")
_SEED_PLACEHOLDER_ITEM_RE = re.compile(r"^\s*-\s*\[[^\[\]]*\]\s*(?:\(例[:：].*\))?\s*$")
_SEED_EXAMPLE_ITEM_RE = re.compile(r"^\s*-\s*\(例[:：].*\)\s*$")
_SEED_CT_HEAD_RE = re.compile(r"^CT-\d{2,}:\s*$")
_SEED_KEY_ONLY_RE = re.compile(r"^\s*[^\s#][^:\n]*:\s*$")


def _seed_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _prune_orphan_keys(lines: list[str]) -> list[str]:
    """剔除无子行的键行（`key:` 形态）——递归到稳定。

    YAML 块序列允许列表项与父键同缩进（`关联角色:` 后跟同缩进的 `- 张三`），
    故「有子行」= 下一条非空行缩进更深，或同缩进且以 `-` 开头。
    """
    while True:
        keep, changed = [True] * len(lines), False
        for i, line in enumerate(lines):
            if not _SEED_KEY_ONLY_RE.match(line):
                continue
            base = _seed_indent(line)
            has_child = False
            for j in range(i + 1, len(lines)):
                nxt = lines[j]
                if not nxt.strip():
                    continue
                ind = _seed_indent(nxt)
                if ind > base or (ind == base and nxt.lstrip().startswith("-")):
                    has_child = True
                break
            if not has_child:
                keep[i], changed = False, True
        lines = [l for l, k in zip(lines, keep) if k]
        if not changed:
            return lines


def _sanitize_seed_text(text: str) -> tuple[str, int]:
    """CONFLICTS_SEED.md → 可物化为 YAML 的正文；返回 (净化后文本, 剥离行数)。

    模板是 Markdown 文档（标题/引用块/分隔线/说明段落/占位骨架），原样拼进
    states/conflicts.yaml 会让 YAML 解析失败。两道净化：

    1. **剥离噪声行**：HTML 注释 `<!-- ... -->`（含跨行）、Markdown 标题行、引用块行（`>`）、
       分隔线（`---`）、未填写的空占位行（`[占位]` / `[占位] (例: ...)` / 纯 `- (例: ...)`）。
    2. **只提取顶层 `CT-XX:` 块**（连同其缩进子行）——SEED 的数据面就是 CT 条目，
       模板正文/编写说明/合格示范段落一律不物化；块内无子行的键行递归剔除，
       故「未填写的骨架」净化后为空而非残留空壳。
    """
    body = _SEED_HTML_COMMENT_RE.sub("", text)
    rows = []
    for raw in body.splitlines():
        line = raw.rstrip()
        if (_SEED_HEADING_RE.match(line) or _SEED_HEADING_BARE_RE.match(line)
                or _SEED_QUOTE_RE.match(line) or _SEED_HR_RE.match(line)
                or _SEED_PLACEHOLDER_VALUE_RE.match(line)
                or _SEED_PLACEHOLDER_ITEM_RE.match(line)
                or _SEED_EXAMPLE_ITEM_RE.match(line)):
            continue
        rows.append(line)

    blocks, cur = [], None
    for line in rows:
        if _SEED_CT_HEAD_RE.match(line):
            if cur is not None:
                blocks.append(cur)
            cur = [line]
        elif cur is not None:
            if not line.strip() or _seed_indent(line) > 0:
                cur.append(line)
            else:
                blocks.append(cur)
                cur = None
    if cur is not None:
        blocks.append(cur)

    kept = []
    for blk in blocks:
        while blk and not blk[-1].strip():
            blk.pop()
        blk = _prune_orphan_keys(blk)
        if blk:
            kept.append("\n".join(blk))

    out = "\n\n".join(kept).strip("\n")
    dropped = max(len(body.splitlines()) - len(out.splitlines()), 0)
    return out, dropped


def cmd_init_states(world_dir: Path):
    """首次启动物化（幂等·缺什么补什么·已存在跳过）——session_recovery.md 第二章 Step 0 的脚本化：
    - states/conflicts.yaml     ← 物化 story_architecture/CONFLICTS_SEED.md（净化 Markdown/注释/空占位后复制+头注释·只落结构字段）
    - states/world_state.yaml   ← templates/world_state.yaml（叙事约定为空时提示 LLM 按世界设定填写）
    - states/world_map.yaml     ← templates/world_map.yaml（有 regions/ 时随后自动 map-sync 对账）
    - scenes/{焦点场景}/pending_actions.yaml ← 场景初始化（init_scene.py）创建（states/ 不物化·场景级）
    - states/CHAR_{名}_state.yaml ← templates/CHAR_state.yaml 骨架（自主性初始值解析自 CHAR_.md
      「世界法则·循环注册」；外部者/管理者角色删除自主性行）
    全部 LF 行尾（newline=""）。LLM 后续按加载序列继续（读静态/动态→校验→循环核对→描绘）。"""
    states = world_dir / "states"
    states.mkdir(parents=True, exist_ok=True)
    tpl_dir = SKILL_DIR / "templates"
    created = []

    def write_lf(fp: Path, text: str):
        with open(fp, "w", encoding="utf-8", newline="") as f:
            f.write(text)

    # 1. conflicts.yaml ← CONFLICTS_SEED.md（只物化结构字段——种子本身即结构字段；节拍留空由戏剧家首轮填充）
    conflicts_fp = states / "conflicts.yaml"
    seed_fp = world_dir / "story_architecture" / "CONFLICTS_SEED.md"
    if conflicts_fp.exists():
        print("[SKIP] conflicts.yaml 已存在（唯一权威·不覆盖）")
    elif not seed_fp.exists():
        print("[ERR] 缺 story_architecture/CONFLICTS_SEED.md——先按第一章创建世界", file=sys.stderr)
        return 1
    else:
        header = (
            "# conflicts.yaml — CT 注册表（上帝视角·禁代词·人名）\n"
            "# 物化自 story_architecture/CONFLICTS_SEED.md（首次启动·init-states）——SEED 只读不改，本文件自此为唯一权威\n"
            "# CT 状态字段（上轮结算.关系状态/上轮结算.内部状态/相位）由①戏剧家每轮结算填充；事件线结构=storylines.yaml（###STORYLINE·②编剧）；演出指针=direction.yaml（###BEAT·③导演）\n\n"
        )
        seed_body, seed_dropped = _sanitize_seed_text(seed_fp.read_text(encoding="utf-8"))
        if not seed_body:
            print(f"[WARN] CONFLICTS_SEED.md 净化后无数据行（已剥离 {seed_dropped} 行 Markdown/注释/空占位）——"
                  f"SEED 仍为模板骨架未填写。conflicts.yaml 将只含头注释、无 CT 条目："
                  f"请填好 SEED 后删除 states/conflicts.yaml 重跑 init-states；或由①戏剧家首轮注册 CT", file=sys.stderr)
        else:
            try:
                yaml.safe_load(seed_body)
            except yaml.YAMLError as e:
                print(f"[ERR] CONFLICTS_SEED.md 净化后仍无法解析为 YAML: {e}", file=sys.stderr)
                print("      conflicts.yaml 未写入——请检查 SEED 是否残留 Markdown 结构或未闭合引号后重试。", file=sys.stderr)
                return 1
        write_lf(conflicts_fp, header + seed_body + "\n")
        if seed_dropped:
            print(f"  · conflicts.yaml 净化: 剥离 {seed_dropped} 行 Markdown/HTML 注释/空占位")
        created.append("conflicts.yaml ← CONFLICTS_SEED.md")

    # 2-4. 模板复制（world_state / world_map / storylines / direction）——pending_actions 为场景级·随场景初始化创建
    for tpl_name in ("world_state.yaml", "world_map.yaml", STORYLINES_FILE, DIRECTION_FILE):
        fp = states / tpl_name
        if fp.exists():
            print(f"[SKIP] {tpl_name} 已存在")
        else:
            write_lf(fp, (tpl_dir / tpl_name).read_text(encoding="utf-8"))
            created.append(f"{tpl_name} ← templates/{tpl_name}")

    # 5. CHAR_state 骨架（按 characters/CHAR_*.md）
    chars_dir = world_dir / "characters"
    if chars_dir.is_dir():
        for cmd_fp in sorted(chars_dir.glob("CHAR_*.md")):
            name = cmd_fp.stem[len("CHAR_"):]
            if not name:
                continue
            cs_fp = states / f"CHAR_{name}_state.yaml"
            if cs_fp.exists():
                print(f"[SKIP] CHAR_{name}_state.yaml 已存在")
                continue
            tpl_text = (tpl_dir / "CHAR_state.yaml").read_text(encoding="utf-8")
            md_text = cmd_fp.read_text(encoding="utf-8", errors="ignore")
            m_type = re.search(r"\*\*角色类型\*\*[:：]\s*(\S+)", md_text)
            m_auto = re.search(r"\*\*自主性初始值\*\*[:：]\s*(\S+)", md_text)
            is_loop = bool(m_type and "循环角色" in m_type.group(1))
            auto_val = m_auto.group(1) if m_auto else ""
            if is_loop and auto_val in AUTO_ORDER:
                tpl_text = re.sub(r"^自主性:.*$", f"自主性: {auto_val}", tpl_text, flags=re.M)
                note = f"自主性={auto_val}"
            else:
                tpl_text = re.sub(r"^自主性:.*\n?", "", tpl_text, flags=re.M)
                note = "外部者（无自主性行）" if not is_loop else f"自主性初始值非法/缺失（{auto_val or '空'}）——已删行，LLM 按档案补判"
            write_lf(cs_fp, tpl_text)
            created.append(f"CHAR_{name}_state.yaml ← templates/CHAR_state.yaml（{note}）")

    # 6. 有 regions/ → 镜像层对账（补全目录树节点）
    cmd_map_sync(world_dir)

    # 7. 叙事约定为空 → 提示 LLM 填写（创作决策·脚本不代填）
    ws_fp = states / "world_state.yaml"
    if ws_fp.exists():
        try:
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8")) or {}
            if not str(ws.get("叙事约定", "") or "").strip():
                print("[TODO] world_state.叙事约定 为空——LLM 按世界设定填写（POV 视角/叙事人称/认知边界）")
        except Exception:
            pass

    if created:
        print(f"[OK] init-states 物化 {len(created)} 个文件:")
        for c in created:
            print(f"  + {c}")
    else:
        print("[OK] init-states: 全部动态文件已存在（幂等·零写入）")
    return 0


def cmd_map_sync(world_dir: Path):
    """world_map 对账补全（镜像层）：遍历 regions/ 目录树 → 缺失节点补入（类型/档案从档案复制·层级镜像目录树）
    有 regions/ 目录时 world_map=镜像层·节点/层级/类型/档案全部由此命令派生；validate 报告缺失时运行本命令。"""
    wm_fp = world_dir / "states" / "world_map.yaml"
    regions_dir = world_dir / "regions"
    if not regions_dir.is_dir():
        print("[SKIP] 无 regions/ 目录——world_map 走迷雾制·无需对账")
        return
    wm = {}
    if wm_fp.exists():
        try:
            wm = yaml.safe_load(wm_fp.read_text(encoding="utf-8")) or {}
        except Exception:
            wm = {}
    if not isinstance(wm, dict) or "已探索区域" not in wm:
        wm = {"已探索区域": {}}
    explored = wm["已探索区域"]
    added = []

    def ensure_node(parent, name, rel_path):
        """在 parent dict 中找/建节点；parent=None 表示顶层 explored"""
        if parent is None:
            node = explored.get(name)
        else:
            node = (parent.get("子区域") or {}).get(name)
        if node is None or not isinstance(node, dict):
            node = {}
            arch = f"regions/{rel_path}/REGION.md"
            txt = (world_dir / arch).read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*-\s*类型:\s*(\S+)", txt, re.M)
            if m:
                node["类型"] = m.group(1)
            node["档案"] = arch
            if parent is None:
                explored[name] = node
            else:
                parent.setdefault("子区域", {})[name] = node
            added.append(f"已探索区域.{rel_path}")
        return node

    def walk(d, parent, rel):
        for sub in sorted(d.iterdir()):
            if not sub.is_dir():
                continue
            name = sub.name
            sub_rel = f"{rel}/{name}" if rel else name
            if not (sub / "REGION.md").is_file():
                continue
            node = ensure_node(parent, name, sub_rel)
            walk(sub, node, sub_rel)

    walk(regions_dir, None, "")
    if added:
        wm["已探索区域"] = explored
        wm_fp.write_text(yaml.dump(wm, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8", newline="")
        print(f"[OK] world_map 对账补全 {len(added)} 个缺失节点:")
        for a in added:
            print(f"  + {a}")
    else:
        print("[OK] world_map 已与 regions/ 目录树同步（无缺失节点）")


def cmd_validate(world_dir: Path) -> int:
    """验证状态文件（格式错误 + 内容级警告）。返回 errors 数量——调用方据此决定退出码：
    顶层 `validate` 子命令 errors>0 → exit 1（硬闸）；内容警告不阻断（exit 0）。
    内部调用方（cmd_fix）可忽略返回值。"""
    scene_dir = get_scene_dir(world_dir)
    files = discover_files(world_dir, scene_dir)
    errors = []
    for key, fp in sorted(files.items()):
        try:
            data = yaml.safe_load(fp.read_text(encoding="utf-8"))
            if data is None:
                errors.append(f"{key}: 空文件")
        except yaml.YAMLError as e:
            errors.append(f"{key}: YAML 解析错误: {e}——修复提示: 字段值含半角冒号+空格（': '）或列表语法时需用引号包裹（对齐同字段正常写法·如 scene_state 关键场景信息参考 S05 的 '区域档案: ...' 单引号格式）；坏文件无法被 write-raw 解析时会拒绝写入——先用编辑器直接修复引号后再走 write-raw")
        except Exception as e:
            errors.append(f"{key}: {e}")
    # 检查未转换的 .md 文件（仅检查状态文件，排除角色设定文件和世界观文件）
    state_md_patterns = ["world_state.md", "conflicts.md", "pending_actions.md", "scene_state.md"] + \
                       [f.name for f in world_dir.glob(f"{CHAR_STATE_PREFIX}*_state.md")]
    for state_md_name in state_md_patterns:
        fp = world_dir / state_md_name
        if not fp.exists():
            # 可能在子目录
            if scene_dir:
                fp = scene_dir / state_md_name
            if not fp.exists():
                continue
        if fp.suffix == ".md" and not fp.name.endswith(".bak"):
            if fp.parent == world_dir:
                yaml_fp = world_dir / "states" / (fp.stem + ".yaml")
            else:
                yaml_fp = fp.with_suffix(".yaml")
            if not yaml_fp.exists():
                errors.append(f"{fp.name}: 仍为 .md 格式，未转换为 .yaml")
    # ── 内容级检查（警告，不阻断）──
    warnings = []
    # 1. conflicts.yaml 顶层键应为 CT-XX（节拍表已迁 storylines——残留=未迁移）
    conflicts_fp = world_dir / "states" / "conflicts.yaml"
    if conflicts_fp.exists():
        try:
            cdata = yaml.safe_load(conflicts_fp.read_text(encoding="utf-8"))
            if isinstance(cdata, dict):
                for k, v in cdata.items():
                    if re.match(r"^CT-\d{2}$", str(k)):
                        _pv = str((v or {}).get(PRESSURE_KEY) or "").strip() if isinstance(v, dict) else ""
                        _pe, _pd = _split_pressure(_pv)
                        if _pe and _pe not in PRESSURE_ENUM:
                            warnings.append(f"conflicts.yaml: {k}.{PRESSURE_KEY} '{_pv}' 非法（枚举: {'/'.join(PRESSURE_ENUM)}）")
                        elif _pe and _pe != PRESSURE_HOLD and not _pd:
                            warnings.append(f"conflicts.yaml: {k}.{PRESSURE_KEY} 四爆破方向'{_pe}'缺少压力说明——建议补写‘压力来源+受力点+转变方向’")
                    elif str(k) == PRESSURE_KEY:
                        warnings.append(f"conflicts.yaml: 顶层键 '{PRESSURE_KEY}' 为旧版残留（施压方向已改为 CT 子字段 CT-XX.{PRESSURE_KEY}）——建议清理")
                    elif not re.match(r"^CT-\d{2}$", str(k)):
                        extra = "（节拍表残留）" if str(k) == BEAT_TOP_KEY else ""
                        warnings.append(f"conflicts.yaml: 顶层键 '{k}' 不符合 CT-XX 格式{extra}")
                st = _load_storylines(world_dir)
                sl_map = st.get(STORYLINE_TOP_KEY) or {}
                # 1-legacy. CT 已迁移字段残留检测 + 事件线引用有效性
                for k, cv in cdata.items():
                    if not re.match(r"^CT-\d{2}$", str(k)) or not isinstance(cv, dict):
                        continue
                    legacy_hit = [f for f in CT_LEGACY_KEYS if f in cv]
                    if legacy_hit:
                        warnings.append(f"conflicts.yaml: {k} 含已迁移字段 {legacy_hit}（→ storylines+direction+CHAR_state）")
                    refs = cv.get("事件线引用")
                    if isinstance(refs, str) and refs.strip():
                        warnings.append(f"conflicts.yaml: {k}.事件线引用 为字符串 '{refs[:40]}'，应为 YAML 列表（如 [SL-01] / 逐行 '- SL-01'）——类型损坏·write-raw KEY 覆盖为列表")
                    elif isinstance(refs, list):
                        bad = [str(r) for r in refs if str(r) not in sl_map]
                        if bad:
                            warnings.append(f"conflicts.yaml: {k}.事件线引用 指向不存在的事件线 {bad}")
                # 1b. direction ↔ storylines 三方对账（当前拍指针权威=direction·结构权威=storylines）
                dr = _load_direction(world_dir)
                if dr:
                    cur_sl = str(dr.get("当前事件线", "") or "").strip()
                    cur_beat = str(dr.get("当前拍", "") or "").strip()
                    if not cur_sl and sl_map:
                        warnings.append("direction.yaml: 当前事件线为空但 storylines 有事件线——指针未设（③导演 ###BEAT: set）")
                    elif cur_sl and cur_sl not in sl_map:
                        warnings.append(f"direction.yaml: 当前事件线 '{cur_sl}' 不在 storylines.事件线 中")
                    elif cur_sl:
                        line = sl_map.get(cur_sl) or {}
                        names = [str(b.get("拍名", "")) for b in (line.get("拍序") or []) if isinstance(b, dict)]
                        if cur_beat and cur_beat not in names:
                            warnings.append(f"direction.yaml: 当前拍 '{cur_beat}' 不在事件线 {cur_sl} 的拍序中（拍序: {names}）")
                        q_dr = str(dr.get("当前戏剧问题", "") or "").strip()
                        q_st = ""
                        for b in (line.get("拍序") or []):
                            if isinstance(b, dict) and str(b.get("拍名", "") or "").strip() == cur_beat:
                                q_st = str(b.get("戏剧问题", "") or "").strip()
                                break
                        if q_dr and q_st and q_dr != q_st:
                            warnings.append(f"direction.yaml: 当前戏剧问题与 storylines 事件线 {cur_sl} 拍 '{cur_beat}' 不一致（缓存漂移·以 storylines 为准）")
                    perf = str(dr.get("演出状态", "") or "").strip()
                    if perf and perf not in PERF_STATES:
                        warnings.append(f"direction.yaml: 演出状态 '{perf}' 非法（枚举: {'/'.join(PERF_STATES)}）")
                    # 1b-2. 顶点基线落档存在性（软性·消息中性——不出具对比面字段清单）
                    if cur_sl and cur_beat == "顶点" and not _climax_baseline_fp(world_dir, cur_sl).exists():
                        warnings.append("direction.yaml: 当前拍=顶点 但基线落档缺失（进入顶点拍时脚本自动记录·私有落档）——出线核验将拦截·先 beat set/advance 顶点 建档")
                # 1b-3. 节点落位 键域（storylines·软警不拦截）：键须落在当前幕的节拍清单内——
                #       键域随当前幕而变（权威=beat_structure.md §一）；幕切换后旧幕键残留即告警。
                _arc = st.get("故事弧线") if isinstance(st, dict) else None
                _arc_act = str((_arc or {}).get("当前幕", "") or "") if isinstance(_arc, dict) else ""
                _arc_nl = (_arc or {}).get("节点落位") if isinstance(_arc, dict) else None
                if isinstance(_arc_nl, dict) and _arc_nl:
                    _act_key = next((k for k in ARC_BEATS if k in _arc_act), None)
                    if _act_key:
                        _stray = [k for k in _arc_nl if k not in ARC_BEATS[_act_key]]
                        if _stray:
                            warnings.append(f"storylines.yaml: 故事弧线.节点落位 含非当前幕（{_arc_act}）的节拍键 {'/'.join(_stray)}——键域=当前幕节拍清单（权威=beat_structure.md §一·幕切换时整体重写）")
                    elif _arc_act:
                        warnings.append(f"storylines.yaml: 故事弧线.当前幕 '{_arc_act}' 未落在三幕骨架（第一幕/第二幕/第三幕）内——节点落位 键域无法核对")
                # 1c. 顶点约束结构（storylines·Vertex Constraint 校验 + 旧字段残留告警）
                for n, ln in sl_map.items():
                    if not isinstance(ln, dict) or not ln:
                        continue
                    for b in (ln.get("拍序") or []):
                        if not isinstance(b, dict) or str(b.get("拍名", "") or "").strip() != "顶点":
                            continue
                        if "顶点落点" in b:
                            warnings.append(f"storylines.yaml: 事件线 {n} 顶点拍用旧字段 顶点落点（答题式 Outcome·已废弃）——rewrite 为 顶点约束")
                            continue
                        cons = b.get(CLIMAX_CONSTRAINT_KEY)
                        if not isinstance(cons, dict):
                            warnings.append(f"storylines.yaml: 事件线 {n} 顶点拍缺 顶点约束（关系主体/核心张力/变化维度/非玩家爆破）")
                            continue
                        principals = [str(x).strip() for x in (cons.get("关系主体") or []) if str(x).strip()]
                        if len(set(principals)) < 2:
                            warnings.append(f"storylines.yaml: 事件线 {n}.顶点约束.关系主体 需 ≥2 去重角色（顶点单位=关系）")
                        if not str(cons.get("核心张力", "") or "").strip():
                            warnings.append(f"storylines.yaml: 事件线 {n}.顶点约束.核心张力 为空")
                        dims = [str(d).strip() for d in (cons.get("变化维度") or []) if str(d).strip()]
                        if not dims or any(d not in DIM_ENUM for d in dims):
                            warnings.append(f"storylines.yaml: 事件线 {n}.顶点约束.变化维度 非法或为空（枚举: {'/'.join(DIM_ENUM)}）")
                        blasters = [str(x).strip() for x in (cons.get("非玩家爆破") or []) if str(x).strip()]
                        if not blasters:
                            warnings.append(f"storylines.yaml: 事件线 {n}.顶点约束.非玩家爆破 为空（≥1 外部角色或事件·压力供应方·防死锁）")
        except Exception:
            pass
    # 2. world_state.焦点场景（唯一权威源）↔ INDEX + 场景目录一致性
    index_fp = world_dir / "scenes" / "INDEX.md"
    ws_fp = world_dir / "states" / "world_state.yaml"
    focus_id = ""
    if ws_fp.exists():
        try:
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
            if isinstance(ws, dict):
                if ws.get("焦点场景"):
                    focus_id = str(ws["焦点场景"]).strip()
                elif not (ws.get("地点") or {}).get("焦点场景") and not (ws.get("地点") or {}).get("当前焦点场景"):
                    warnings.append("world_state.yaml: 缺顶层键 焦点场景（唯一权威源，应置于第一行）")
        except Exception:
            pass
    if focus_id:
        scenes_dir = world_dir / "scenes"
        dir_ok = False
        if scenes_dir.is_dir():
            for d in scenes_dir.iterdir():
                if d.is_dir() and d.name.startswith(focus_id):
                    dir_ok = True
                    break
        if not dir_ok:
            warnings.append(f"焦点场景 '{focus_id}': 无对应场景目录 scenes/{focus_id}-*")
        if index_fp.exists():
            index_text = index_fp.read_text(encoding="utf-8")
            if not re.search(rf"\|[ ]*{re.escape(focus_id)}[ ]*\|", index_text):
                warnings.append(f"焦点场景 '{focus_id}' 未在 scenes/INDEX.md 的表格行中找到")
            active_rows = re.findall(r"^\|\s*(S\d+)\s*\|.*\|\s*ACTIVE\s*\|", index_text, re.M)
            if active_rows and active_rows != [focus_id]:
                warnings.append(f"INDEX ACTIVE 行 {active_rows} 与 world_state.焦点场景 '{focus_id}' 不一致")
    elif ws_fp.exists() and index_fp.exists() and not focus_id:
        active_rows = re.findall(r"^\|\s*(S\d+)\s*\|.*\|\s*ACTIVE\s*\|", index_fp.read_text(encoding="utf-8"), re.M)
        if active_rows:
            warnings.append(f"world_state.焦点场景 为空，但 INDEX 标记 {active_rows} 为 ACTIVE——焦点场景唯一权威源缺失")
    # 3. CHAR_*_state.yaml 应有对应 CHAR_*.md
    for sf in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
        md_fp = world_dir / "characters" / (sf.name[: -len(CHAR_STATE_SUFFIX)] + ".md")
        if not md_fp.exists():
            warnings.append(f"{sf.name}: 无对应 {md_fp.name}")
    # 4. world_state.yaml 必要键
    ws_fp = world_dir / "states" / "world_state.yaml"
    if ws_fp.exists():
        try:
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
            if isinstance(ws, dict):
                for need in ("焦点场景", "时间", "全局标记"):
                    if need not in ws:
                        warnings.append(f"world_state.yaml: 缺顶层键 {need}")
        except Exception:
            pass
    # 4b. world_state 键表外字段（软性警告——无语义定义的漂移字段）
    if ws_fp.exists():
        try:
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
            if isinstance(ws, dict):
                WS_TOP_KEYS = {"焦点场景", "轮次", "时间", "外部倒计时", "全局标记", "时间线", "维护名单", "叙事约定"}
                WS_TIME_KEYS = {"基准时间", "具体时间", "时间流速比", "前情描述"}
                for k in ws:
                    if k not in WS_TOP_KEYS:
                        warnings.append(f"world_state.yaml: 未知顶层键 '{k}'（键表: 焦点场景/轮次/时间/外部倒计时/全局标记/时间线/维护名单/叙事约定）")
                # 旧键提示（2026-09-18 改名：重置记录 → 维护名单·不留兼容别名·读取端已全部改新键）
                if "重置记录" in ws:
                    warnings.append("world_state.yaml: 顶层键『重置记录』已改名为『维护名单』——请整表改名（旧键不被读取·周期重置判定将失效）")
                t = ws.get("时间")
                if isinstance(t, dict):
                    for k in t:
                        if k not in WS_TIME_KEYS:
                            warnings.append(f"world_state.yaml: 未知时间子键 '{k}'（键表: 基准时间/具体时间/时间流速比/前情描述）")
                loc = ws.get("地点")
                if isinstance(loc, dict):
                    for k in loc:
                        warnings.append(f"world_state.yaml: 地点.{k} 已废弃（当前区域→scene 区域关联·已探索区域→world_map 镜像·请删除该字段）")
        except Exception:
            pass
    # 4c. 场景骨架占位检查（scene_card 目标/钩子/焦外、start_snapshot 姿态/道具——创建后禁止带模板占位运行）
    # 模板占位特征 = [字段定义] 或 (例: 示例)——真实场景文件不应含这两类（templates/ 符号契约）
    PLACEHOLDER_RE = re.compile(r"\[[^\]]{2,40}\]|\(例:")
    scenes_dir = world_dir / "scenes"
    if scenes_dir.is_dir():
        for d in sorted(scenes_dir.iterdir()):
            if not d.is_dir():
                continue
            sc_fp = d / "scene_card.md"
            if sc_fp.exists():
                sc_text = sc_fp.read_text(encoding="utf-8", errors="ignore")
                if PLACEHOLDER_RE.search(sc_text):
                    warnings.append(f"{d.name}/scene_card.md: 场景目标/前情钩子/焦外等仍为模板占位（[字段定义]/(例:) 残留）——创建后应已填充，禁止带占位运行")
            ss_fp = d / "start_snapshot.md"
            if ss_fp.exists():
                ss_text = ss_fp.read_text(encoding="utf-8", errors="ignore")
                if PLACEHOLDER_RE.search(ss_text):
                    warnings.append(f"{d.name}/start_snapshot.md: 角色姿态/道具位置等仍为模板占位（[字段定义]/(例:) 残留）——创建后应已填充，禁止带占位运行")
    # 4c2. scene_card 区域关联检查（镜像层：区域行 ∈ regions/ 目录树·必填）
    regions_dir = world_dir / "regions"
    if regions_dir.is_dir():
        for card in sorted(world_dir.glob("scenes/*/scene_card.md")):
            txt = card.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\|\s*区域\s*\|\s*([^|]+?)\s*\|", txt, re.M)
            if not m:
                warnings.append(f"{card.relative_to(world_dir)}: 缺「区域」行（scene_card 模板必填·完整路径·从 regions/ 目录树引用既有档案）")
            else:
                arch = m.group(1).strip()
                if not (world_dir / arch).is_file():
                    warnings.append(f"{card.relative_to(world_dir)}: 区域指针悬空（{arch} 不存在——先核对 regions/ 既有档案·指针引用既有路径·确无档案才新建）")
    # 4c'. 焦外断线兜底（软警告·低频）：焦点场景 pending_actions 活跃中为空，但 调度单 点名焦外角色 → 提示补迁移/注册
    if scene_dir is not None and (scene_dir / "pending_actions.yaml").exists():
        try:
            _pa = yaml.safe_load((scene_dir / "pending_actions.yaml").read_text(encoding="utf-8")) or {}
            _act = _pa.get("活跃中")
            active_empty = not bool(isinstance(_act, dict) and _act)
        except Exception:
            active_empty = True
        if active_empty and re.search(r"焦外\s*=\s*(?!无)", _direction_schedule_text(world_dir)):
            warnings.append("焦点场景 pending_actions 活跃中为空，但 调度单 点名焦外角色——检查是否漏迁移/注册（见 scene_management 场景切换流程第6步）")
    # 4e. 已知地点后缀匹配（镜像层：条目 ∈ regions/ 目录树某节点路径的后缀——角色认知根开始·如 Sweetwater/Main Street）
    regions_dir = world_dir / "regions"
    if regions_dir.is_dir():
        tree_paths = [p.parent.relative_to(regions_dir).as_posix() for p in regions_dir.rglob("REGION.md")]
        for sf in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
            try:
                sd = yaml.safe_load(sf.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            places = sd.get("已知地点")
            if not isinstance(places, list):
                continue
            for pl in places:
                s = str(pl or "").strip()
                if not s:
                    continue
                if any(p == s or p.endswith("/" + s) for p in tree_paths):
                    continue
                # 自动对齐：条目分段与目录树节点分段按序对齐——末段可为场景子空间（并入目录节点）
                # （「Mesa Hub/Welcome Center 入境长廊」「Welcome Center/主厅」→ Mesa Hub/Welcome Center）
                _eparts = [x.strip() for x in s.split("/") if x.strip()]
                _align = _eparts[:-1] if len(_eparts) > 1 else _eparts
                _ok = False
                for _p in tree_paths:
                    _pparts = _p.split("/")
                    _pi = 0
                    _hit = True
                    for _ep in _align:
                        _found = False
                        while _pi < len(_pparts):
                            _seg = _pparts[_pi]
                            if _ep == _seg or _ep.startswith(_seg):
                                _pi += 1
                                _found = True
                                break
                            _pi += 1
                        if not _found:
                            _hit = False
                            break
                    if _hit:
                        _ok = True
                        break
                if not _ok:
                    warnings.append(f"{sf.name}: 已知地点 '{s}' 不在 regions/ 目录树（后缀路径应从目录节点名·角色认知根开始·如 Sweetwater/Main Street·粒度=目录节点级·场景子空间并入目录节点不单列·规范见 keys.md「已知地点」）")
            # 4e-2. 位置值域（内容警告·与 audit ⑫c 同判据）：存量非法位置会致盲区域一致性检查——
            #        写入口已被 audit 硬顶回，此处对存量数据出警告促修复（数据修复 2026-10-05）。
            _posv = sd.get("位置")
            if isinstance(_posv, str) and _posv.strip() and not _is_template_value(_posv):
                if _pos_region_node(world_dir, _posv) is None:
                    warnings.append(f"{sf.name}: 位置 '{_posv.strip()}' 不在 regions/ 目录树（值域=目录节点后缀路径·剥括号注后须命中 REGION 节点·如 Sweetwater/Main Street·见 keys.md「位置」——非法位置会致盲区域一致性检查/场景切换判据）")
    # 4d. 事件重置强制校验（loop_machinery §4 触发管道之二）——CHAR_state 当前状态含「重置完成/校准完成」类
    #     字段但该角色无 维护名单 条目 → 叙事演了重置、文件未执行联动表（补执行: worldctl.py <世界> reset-cycle --asset <角色>）
    reset_names = set()
    if ws_fp.exists():
        try:
            _ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
            if isinstance(_ws, dict):
                _rr = _ws.get("维护名单")
                if isinstance(_rr, dict):
                    reset_names = {str(k) for k in _rr}
        except Exception:
            pass
    RESET_DONE_RE = re.compile(r"重置完成|校准完成")
    for sf in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
        try:
            sd = yaml.safe_load(sf.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        name = sf.name[len(CHAR_STATE_PREFIX):-len(CHAR_STATE_SUFFIX)]
        if name in reset_names:
            continue
        blob = " ".join(str(sd.get(k, "") or "") for k in ("核心状态", "情绪", "位置"))
        if RESET_DONE_RE.search(blob):
            warnings.append(f"{sf.name}: 当前状态含『重置完成/校准完成』但无 维护名单 条目——事件重置未执行联动表（补执行: worldctl.py {world_dir.name} reset-cycle --asset {name}）")
    # 5. world_map.yaml（可选增强层·迷雾制·多层嵌套）——缺失时静默跳过，不影响运行
    wm_fp = world_dir / "states" / "world_map.yaml"
    if wm_fp.exists():
        try:
            wm = yaml.safe_load(wm_fp.read_text(encoding="utf-8"))
            if not isinstance(wm, dict) or "已探索区域" not in wm:
                warnings.append("world_map.yaml: 缺顶层键 已探索区域（迷雾制地图，初始应为 {}）")
            else:
                scenes_dir = world_dir / "scenes"
                WM_KEYS = {"类型", "方位", "连接", "发现于", "备注", "子区域", "档案"}
                def walk_map(node, path):
                    """递归检查 world_map 节点：未知键 / 发现于引用 / 子区域结构"""
                    if not isinstance(node, dict):
                        warnings.append(f"world_map.yaml {path}: 值应为映射（节点字段/子区域）")
                        return
                    for k in node:
                        if k not in WM_KEYS:
                            warnings.append(f"world_map.yaml {path}.{k}: 未知键（应为 类型/方位/连接/发现于/备注/子区域）")
                    found = str(node.get("发现于", "") or "").strip()
                    if found and (not scenes_dir.is_dir() or not any(
                            d.is_dir() and d.name.startswith(found) for d in scenes_dir.iterdir())):
                        warnings.append(f"world_map.yaml {path}: 发现于 '{found}' 无对应场景目录")
                    kids = node.get("子区域")
                    if kids is not None:
                        if not isinstance(kids, dict):
                            warnings.append(f"world_map.yaml {path}.子区域: 值应为区域名→节点的映射")
                        else:
                            for name, sub in kids.items():
                                walk_map(sub, f"{path}.{name}")
                for name, sub in (wm.get("已探索区域") or {}).items():
                    walk_map(sub, f"已探索区域.{name}")
                # regions/ 档案对账（可选增强层：有 regions/ 目录才检查）——已登记节点有 档案 指针 →
                # ① 指针悬空告警 ② 类型与档案不一致告警（单向派生对账·软告警·不是双权威）
                regions_dir = world_dir / "regions"
                if regions_dir.is_dir():
                    def walk_archive(node, path):
                        arch = str(node.get("档案", "") or "").strip()
                        if arch:
                            afp = world_dir / arch
                            if not afp.is_file():
                                warnings.append(f"world_map.yaml {path}.档案: 指针悬空（{arch} 不存在——先核对 regions/ 既有档案·指针引用既有路径·确无档案才新建）")
                            else:
                                txt = afp.read_text(encoding="utf-8", errors="ignore")
                                m = re.search(r"^\s*-\s*类型:\s*(\S+)", txt, re.M)
                                if m and node.get("类型") and m.group(1) != str(node.get("类型")):
                                    warnings.append(f"world_map.yaml {path}.类型: 与档案 {arch} 不一致（档案={m.group(1)}，map={node.get('类型')}——派生登记应从档案复制）")
                        for k, sub in (node.get("子区域") or {}).items():
                            walk_archive(sub, f"{path}.{k}")
                    for name, sub in (wm.get("已探索区域") or {}).items():
                        walk_archive(sub, f"已探索区域.{name}")
                    # 缺失节点报告（镜像层）：目录树节点不在 world_map → 提示运行 map-sync 对账补全
                    def _node_exists(node, parts):
                        cur = node
                        for p in parts:
                            if not isinstance(cur, dict):
                                return False
                            nxt = cur.get(p)
                            if nxt is None:
                                kids = cur.get("子区域") or {}
                                nxt = kids.get(p)
                                if nxt is None:
                                    return False
                            cur = nxt
                        return True
                    missing = []
                    def walk_tree(d, rel):
                        for sub in sorted(d.iterdir()):
                            if not sub.is_dir():
                                continue
                            name = sub.name
                            sub_rel = f"{rel}/{name}" if rel else name
                            if not (sub / "REGION.md").is_file():
                                continue
                            if not _node_exists(wm.get("已探索区域") or {}, sub_rel.split("/")):
                                missing.append(sub_rel)
                            walk_tree(sub, sub_rel)
                    walk_tree(regions_dir, "")
                    if missing:
                        shown = ", ".join(missing[:5]) + ("..." if len(missing) > 5 else "")
                        warnings.append(f"world_map.yaml: {len(missing)} 个目录树节点缺失——运行 `worldctl.py {world_dir.name} map-sync` 对账补全（镜像层·节点从目录树派生·禁止手写）: {shown}")
        except Exception:
            pass
    # 5b. foreshadow.yaml 伏笔闭环检查（可选文件·仅世界有该文件时检查）
    fs_fp = world_dir / "states" / "foreshadow.yaml"
    if fs_fp.exists():
        try:
            fdata = yaml.safe_load(fs_fp.read_text(encoding="utf-8"))
            f_list = fdata.get("伏笔", []) if isinstance(fdata, dict) else None
            if f_list is None:
                errors.append("foreshadow.yaml: 缺顶层键 伏笔（应为列表）")
            elif not isinstance(f_list, list):
                errors.append("foreshadow.yaml: 顶层键 伏笔 应为列表")
            else:
                cur_round = 0
                if ws_fp.exists():
                    try:
                        ws_cur = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
                        if isinstance(ws_cur, dict):
                            cur_round = int(ws_cur.get("轮次") or 0)
                    except Exception:
                        pass
                for i, it in enumerate(f_list, 1):
                    if not isinstance(it, dict):
                        warnings.append(f"foreshadow.yaml 伏笔[{i}]: 元素应为映射（线索/种下/时间/回收/状态）")
                        continue
                    clue = str(it.get("线索", "")).strip()
                    status = str(it.get("状态", "")).strip()
                    try:
                        plant = int(it.get("种下") or 0)
                    except (TypeError, ValueError):
                        plant = -1
                    try:
                        pay = int(it.get("回收") or 0)
                    except (TypeError, ValueError):
                        pay = 0
                    if not clue:
                        warnings.append(f"foreshadow.yaml 伏笔[{i}]: 缺 线索")
                    if status not in ("待回收", "已回收", "废弃"):
                        warnings.append(f"foreshadow.yaml 伏笔[{i}]: 非法状态 '{status}'（枚举：待回收/已回收/废弃）")
                    elif status == "已回收":
                        if pay == 0:
                            warnings.append(f"foreshadow.yaml 伏笔[{i}] '{clue}': 已回收但缺 回收 轮次")
                        elif plant > 0 and pay < plant:
                            errors.append(f"foreshadow.yaml 伏笔[{i}] '{clue}': 回收轮次 {pay} 早于种下轮次 {plant}（伏笔倒置·硬错）")
                    elif status == "待回收" and plant > 0 and cur_round - plant > 20:
                        warnings.append(f"foreshadow.yaml 伏笔[{i}] '{clue}': 种下 {plant} 轮已过 {cur_round - plant} 轮未回收（>20 轮·建议回收或废弃）")
        except Exception as e:
            warnings.append(f"foreshadow.yaml: 解析失败 {e}")
    # 5c. scene_state 结构化字段校验（场景时间线带轮次·道具按 ID——旧字符串格式软提示迁移）
    scene_dir2 = get_scene_dir(world_dir)
    if scene_dir2 and (scene_dir2 / "scene_state.yaml").exists():
        try:
            sd2 = yaml.safe_load((scene_dir2 / "scene_state.yaml").read_text(encoding="utf-8")) or {}
        except Exception:
            sd2 = {}
        tl = sd2.get("场景时间线", "")
        if isinstance(tl, list):
            bad = [it for it in tl if not isinstance(it, dict) or not str(it.get("轮次", "") or "").strip()
                   or not str(it.get("时间", "") or "").strip() or not str(it.get("事件", "") or "").strip()]
            if bad:
                warnings.append(f"{scene_dir2.name}/scene_state.yaml: 场景时间线 {len(bad)} 条缺 轮次/时间/事件 子字段（结构: 轮次/时间/事件）")
            rounds_seen = [str(it.get("轮次", "") or "") for it in tl if isinstance(it, dict)]
            dup_r = [r for r in set(rounds_seen) if rounds_seen.count(r) > 1]
            if dup_r:
                warnings.append(f"{scene_dir2.name}/scene_state.yaml: 场景时间线 轮次重复 {dup_r}（一轮一条·同轮多事件并入一条或注明）")
        elif isinstance(tl, str) and tl.strip():
            warnings.append(f"{scene_dir2.name}/scene_state.yaml: 场景时间线 仍是旧字符串格式（· 连接）——结构化迁移：- 轮次/时间/事件（回退裁剪需按轮次字段）")
        props = sd2.get("道具", "")
        if isinstance(props, list):
            pids = [str(it.get("ID", "") or "") for it in props if isinstance(it, dict)]
            dup_p = [i for i in set(pids) if pids.count(i) > 1]
            if dup_p:
                warnings.append(f"{scene_dir2.name}/scene_state.yaml: 道具 ID 重复 {dup_p}（ID 唯一）")
        elif isinstance(props, str) and props.strip():
            warnings.append(f"{scene_dir2.name}/scene_state.yaml: 道具 仍是旧表格字符串（|P1|…|）——结构化迁移：- ID/名称/位置/状态")

    # 6. CHAR_state 字段级校验（键表/人际动态档位/废弃键/全知视角/轨迹方向/decision 结构/偏离计数）
    CHAR_ALLOWED_KEYS = {"位置", "已知地点", "名字", "性别", "核心状态", "情绪", "人际动态",
                         "压力水平", "防御有效性", "防御形态", "崩溃表现", "信念演化", "记忆锚点",
                         "连续行动轨迹", "decision",
                         "偏离登记",
                         "自主性",
                         "健康", "妆扮", "服饰", "随身物品"}
    OMNI_PATTERN = re.compile(r"[他她]不知道")
    # 3b 前置（补实现·reset-cycle 注释已声称）：行动级偏离需有「法则」型 CT 承接（Host vs 法则·冲突化窗口归零）
    #    逐角色承接：CT 对抗双方含「法则」且 关联角色 含本角色名 → 该角色已被承接。
    #    全局判据会让「乙有法则 CT」掩盖「甲无承接」，故按角色建集合（角色名取 「（」 前主干）
    _c3b = {}
    try:
        _c3b = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        _c3b = {}
    _law_ct_roles = set()
    for _ct in (_c3b or {}).values():
        if not (isinstance(_ct, dict)
                and ("法则" in str(_ct.get("对抗双方", "") or "")
                     or "抽象方" in str(_ct.get("对抗双方", "") or ""))):
            continue
        for _raw in (_ct.get("关联角色") or []):
            _nm = re.split(r"[（(]", str(_raw))[0].strip()
            if _nm:
                _law_ct_roles.add(_nm)
    # 当前轮次（A1 豁免判据：信念演化存在本轮条目=本轮已完成升级留痕）
    _cur_round = ""
    try:
        _ws_cur = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8"))
        if isinstance(_ws_cur, dict):
            _cur_round = str(_ws_cur.get("轮次") or "").strip()
    except Exception:
        pass
    for cfp in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
        try:
            cdata = yaml.safe_load(cfp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(cdata, dict):
            continue
        cname = cfp.name
        # 6a. 未知顶层键（键表外字段=无语义定义的漂移字段）
        for k in cdata:
            if k not in CHAR_ALLOWED_KEYS:
                warnings.append(f"{cname}: 未知键 '{k}'（键表: 自主性/位置/已知地点/名字/性别/核心状态/情绪/人际动态/压力水平/防御有效性/防御形态/崩溃表现/信念演化/记忆锚点/连续行动轨迹/decision；外在物态扩展: 健康/妆扮/服饰/随身物品）")
        # 6b. 废弃键
        if "信任度" in cdata:
            warnings.append(f"{cname}: 顶层键 信任度 已废弃——唯一权威源=人际动态各对象行档位，应删除")
        # 6c. 人际动态行格式（一行=一个关系对象；{对象}: {档位}——{一句现状}）
        rel = cdata.get("人际动态", "")
        if isinstance(rel, str):
            for line in rel.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("（无"):
                    continue
                m = re.match(r"^([^:：]+):\s*([^-—]+)——(.+)$", line)
                if not m:
                    warnings.append(f"{cname}: 人际动态行格式不符「{{对象}}: {{档位}}——{{一句现状}}」: {line[:40]}")
                elif m.group(2).strip() not in RELATION_TIERS:
                    warnings.append(f"{cname}: 人际动态档位 '{m.group(2).strip()}' 非法（枚举: 稳固/信任/中立/防备/破裂/待重建）: {line[:40]}")
            if "→" in rel:
                warnings.append(f"{cname}: 人际动态含 →（旧 A→B 写法已废弃，每行=一个关系对象）")
        # 6d. 全知视角模式（他/她不知道——本角色未知须用「我」）
        for field in ("核心状态", "情绪", "人际动态", "信念演化"):
            val = cdata.get(field, "")
            if isinstance(val, str) and OMNI_PATTERN.search(val):
                warnings.append(f"{cname}: {field} 含「他/她不知道」——全知视角禁止，应改为「我不知道」或感知边界内描述")
        # 6f. 自主性枚举（仅循环角色字段——非法值=键表外漂移）
        auto = cdata.get("自主性", "")
        if auto and auto not in AUTO_ORDER:
            warnings.append(f"{cname}: 自主性 '{auto}' 非法（枚举: 脚本/漂移/觉醒/变质）")
        defense = cdata.get("防御有效性", "")
        pressure = cdata.get("压力水平", "")
        # 6g2. 变质判定门槛已满足但未升档（软提醒·④角色本批应执行升档+信念演化留痕）
        #      豁免：信念演化存在本轮条目——keys.md 硬性「升级=写自主性+同轮追加信念演化留痕」，故本轮有留痕=已升级的可机检证据。
        #      已知取舍（宁漏勿噪）：信念提炼也追加信念演化（不升级），故该豁免产生漏报而非误报。
        if (auto in AUTO_ORDER and auto != "变质"
                and str(pressure).strip() == AUTO_PROMOTE_PRESSURE and str(defense).strip() == AUTO_PROMOTE_DEFENSE):
            _bel = cdata.get("信念演化")
            _traced = isinstance(_bel, list) and _cur_round and any(
                isinstance(_it, dict) and str(_it.get("轮次", "") or "").strip() == _cur_round for _it in _bel)
            if not _traced:
                warnings.append(f"{cname}: 压力={AUTO_PROMOTE_PRESSURE} 且 防御={AUTO_PROMOTE_DEFENSE} 且 信念演化本轮（轮次 {_cur_round or '未读'}）无留痕——满足变质判定门槛（loop_machinery §5.3）·④角色本批应执行升档+信念演化留痕")
        # 6h. decision 结构（角色决策状态·子字段软校验——④角色阶段每轮补全）
        dec = cdata.get("decision")
        if dec is not None:
            DEC_SUB = {"核心诉求", "当前计划", "当前行动", "行动驱动", "行动对象", "行动窗口", "失败后续", "未完成意图"}
            if not isinstance(dec, dict):
                warnings.append(f"{cname}: decision 应为映射（八子字段：{'/'.join(sorted(DEC_SUB))}）——点路径逐层写（decision.核心诉求 等）")
            else:
                if "当前目标" in dec:
                    warnings.append(f"{cname}: decision 含旧键名 '当前目标'（已更名'核心诉求'——语义=核心欲望在所处情境中预期要达成的状态（答「什么样算成」·跨轮））——建议迁移")
                missing = [k for k in DEC_SUB if k not in dec]
                if missing:
                    warnings.append(f"{cname}: decision 缺子字段 {missing}（空值可留空但键应在·④角色阶段补全）")
                template_fields = _decision_template_fields(cdata)
                if template_fields and isinstance(cdata.get("连续行动轨迹"), list) and cdata.get("连续行动轨迹"):
                    warnings.append(f"{cname}: 有连续行动轨迹但 decision 仍含骨架占位 {template_fields}——决策空转；④先物化八字段再继续行动")
        # 6i. 连续行动轨迹（角色时间线·脚本按 10 轮窗口自动裁剪·增长告警+结构校验）
        track = cdata.get("连续行动轨迹")
        if isinstance(track, list) and track:
            total = sum(len(str(it.get("行动", "") or "")) + len(str(it.get("行动结果", "") or "")) for it in track if isinstance(it, dict))
            if total > ACTION_TRACK_LIMIT:
                warnings.append(f"{cname}: 连续行动轨迹 {total} 字 > {ACTION_TRACK_LIMIT} 告警线——角色计划复盘时压缩旧行动为概括条目（轨迹=原始时间线·记忆锚点=蒸馏层）")
            bad = [it for it in track if not isinstance(it, dict) or not str(it.get("轮次", "")).strip() or not str(it.get("行动", "")).strip()]
            if bad:
                warnings.append(f"{cname}: 连续行动轨迹 {len(bad)} 条缺 轮次/行动 子字段（结构: 轮次/行动/行动目的/行动结果/他人反应/计划变化/未完成意图）")
        # 6i-b. 结构化累积字段的旧格式（字符串）条目——功能兼容不阻断写入（S1 防崩）·归一提示
        for _sfn in ("记忆锚点", "信念演化", "偏离登记"):
            _sval = cdata.get(_sfn)
            if isinstance(_sval, list):
                _legacy = sum(1 for _e in _sval if not isinstance(_e, dict))
                if _legacy:
                    warnings.append(f"{cname}: {_sfn} 含 {_legacy} 条旧格式（字符串）条目——写入兼容已放行·建议 ④角色以 ###KEY 全量覆盖归一为结构化列表（元素: 轮次/时间/对象/内容）")
        # 6j. 3b 偏离登记承接（补实现）：有行动级偏离 且 本角色无「法则」型 CT 承接 → 告警（§5.1: 行动级偏离 1 次即注册）
        dev = cdata.get("偏离登记")
        _rname = cfp.stem[len(CHAR_STATE_PREFIX):-len("_state")]
        if isinstance(dev, list) and len(dev) >= 1 and _rname not in _law_ct_roles:
            warnings.append(f"{cname}: 偏离登记 {len(dev)} 次但无「法则」型 CT 承接本角色——行动级偏离 1 次即应注册「Host vs 法则」CT 并把 {_rname} 写入其 关联角色（冲突化窗口归零·loop_machinery §5.1）")
        # 6k. 随身物品持有物一致性（通用）：可转移重要持有物取得后应进随身物品（非服饰）
        _items = cdata.get("随身物品")
        if isinstance(_items, str):
            warnings.append(f"{cname}: 随身物品为字符串 '{str(_items)[:20]}'，应为 YAML 列表 [] / [- 物品]（类型污染·write-raw KEY 覆盖为列表）")
        elif isinstance(_items, list):
            _has_items = len([x for x in _items if str(x).strip()]) > 0
            # 近3轮轨迹含取得类动词但持有清单为空 → 通用漏写告警
            _track = cdata.get("连续行动轨迹") or []
            if isinstance(_track, list) and _track:
                _recent = _track[-3:] if len(_track) >= 3 else _track
                _acq_re = re.compile(r"接过|递出|握起|装入|收入|捡起|拿起|领到|获得|交出|易手")
                _has_acq = any(_acq_re.search(str(it.get("行动", "") or "")) for it in _recent if isinstance(it, dict))
                if _has_acq and not _has_items:
                    warnings.append(f"{cname}: 近3轮轨迹含取得/交出类动作但 随身物品 为空——可转移重要持有物（卡/契约/钥匙/武器/弹药/道具等）取得轮应全量重写随身物品并同步记忆锚点（actor_decision D4 状态写入判定）")

    # 7. world_state.时间线 粗粒度摘要校验（脚本校验线：条目≤10 | 单场景≤3转折点 | 总字数≤2500——超限告警，提示场记执行压缩维护）
    ws_fp = world_dir / "states" / "world_state.yaml"
    if ws_fp.exists():
        try:
            ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8"))
            tl = (ws.get("时间线") or {}) if isinstance(ws, dict) else {}
            if tl:
                if len(tl) > 10:
                    warnings.append(f"world_state.时间线: {len(tl)} 条 > 10 条上限——需压缩最旧场景条目")
                total = 0
                for sid, sv in tl.items():
                    if not isinstance(sv, dict):
                        warnings.append(f"world_state.时间线.{sid}: 值应为映射（时间/事件）")
                        continue
                    ev = sv.get("事件", "")
                    if not isinstance(ev, str):
                        continue
                    total += len(ev)
                    nodes = ev.count("·")
                    if nodes > 3:
                        warnings.append(f"world_state.时间线.{sid}: {nodes} 个转折点 > 3 上限——需压缩为 ≤3 条粗粒度摘要（明细在 scene_state 场景时间线）")
                if total > 2500:
                    warnings.append(f"world_state.时间线: 总字数 {total} > 2500 上限——需执行压缩维护")
        except Exception:
            pass

    # 8. CHAR_state 记忆锚点校验（仅总字数≤3000——超限告警，提示执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）；
    #    单条长度不设限——口径见 write_protocol.md 写入表 / keys.md「记录字段写法」）
    ANCHOR_LIMIT_TOTAL = 3000
    for cfp in sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}")):
        try:
            cdata = yaml.safe_load(cfp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(cdata, dict):
            continue
        mem = cdata.get("记忆锚点", "")
        if isinstance(mem, list):
            # 结构化列表：仅总内容字数 ≤3000（单条不设限）
            total = 0
            for it in mem:
                if not isinstance(it, dict):
                    continue
                total += len(str(it.get("内容", "")))
            if total > ANCHOR_LIMIT_TOTAL:
                warnings.append(f"{cfp.name}: 记忆锚点 {total} 字 > {ANCHOR_LIMIT_TOTAL} 校验线——需执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）")
            # 记忆并句/提炼兜底核验（actor_decision 1.1 回忆 / 1.4 账上信念称量 / 写入节落盘）：
            #   规则不靠计数触发——并句与信念转变由角色在思考里产出（1.1 想起旧记忆 → 1.4 账上称）；
            #   本项仅作**兜底信号**：同类长期只增不减 = 思考里从未并句（验证 A1 现象：无限追加从不并句）。
            #   对象字段缺省时按「对象缺省」降级只提示条数。
            from collections import defaultdict as _Ddict
            _by_obj = _Ddict(list)
            for _it in mem:
                if isinstance(_it, dict) and str(_it.get("内容", "") or "").strip():
                    _by_obj[str(_it.get("对象", "") or "〔未标对象〕")].append(_it)
            for _obj, _its in _by_obj.items():
                _n = len(_its)
                if _n >= 3:
                    warnings.append(f"{cfp.name}: 记忆锚点「{_obj}」同类 {_n} 条只增未并——并句与信念转变应由角色在思考里产出（1.1 想起旧记忆 → 1.4 账上称），写入节只负责落盘；此处为兜底信号，非触发判据")
            continue
        if not isinstance(mem, str) or not mem.strip():
            continue
        total = len(mem)
        if total > ANCHOR_LIMIT_TOTAL:
            warnings.append(f"{cfp.name}: 记忆锚点 {total} 字 > {ANCHOR_LIMIT_TOTAL} 校验线——需执行记忆淘汰（同类并句+低刺激遗忘·###KEY 覆盖全量重写）")
        # （单条长度不设限——不再做单条超限检测）
        # 8a. 重复条目检测（内容完全相同=重复事故残留；同 ID 不同内容=合法多轮条目不报）
        seen_lines, dup_lines = {}, []
        for line in mem.splitlines():
            line_s = line.strip()
            if not line_s:
                continue
            if line_s in seen_lines:
                dup_lines.append(line_s[:45])
            else:
                seen_lines[line_s] = True
        if dup_lines:
            shown = "；".join(f"「{d}…」" for d in dup_lines[:2])
            more = f" 等{len(dup_lines)}条" if len(dup_lines) > 2 else ""
            warnings.append(f"{cfp.name}: 记忆锚点 {len(dup_lines)} 条内容完全重复（重复事故残留——按完整 ID+内容判定去重；同 ID 不同内容=合法）——{shown}{more}")

    # 8b. 重置落地校验（触发：world_state.维护名单 登记了角色 → 对照该角色记忆锚点是否按 CHAR_state.自主性 压缩）
    try:
        ws_data = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws_data = {}
    # 8b-0. 循环机制完整性软告警（循环世界：SETTING 声明循环/重置关键词 → 周期倒计时应有周期条目）
    try:
        setting_fp = world_dir / "SETTING.md"
        setting_txt = setting_fp.read_text(encoding="utf-8", errors="ignore") if setting_fp.exists() else ""
        mech_kw = ("循环", "重置", "循环日终", "抹除记忆", "遗忘法则")
        is_loop_world = any(kw in setting_txt for kw in mech_kw)
        cd_data = ws_data.get("外部倒计时") or {}
        has_periodic = False
        if isinstance(cd_data, dict):
            for cd in cd_data.values():
                # 周期条目判据与 keys.md 倒计时协议对齐：「重置类须含到期时刻」——
                # 含 到期时刻 字段即视为周期条目；「威胁」关键词为兼容旧世界的旁路
                if isinstance(cd, dict) and ("到期时刻" in cd or "周期" in str(cd.get("威胁", "")) or "重置" in str(cd.get("威胁", "")) or "循环" in str(cd.get("威胁", ""))):
                    has_periodic = True
                    break
        if is_loop_world and not has_periodic:
            warnings.append("循环机制完整性: SETTING 声明循环/重置机制但外部倒计时无周期条目（含空表）——周期倒计时未初始化登记（见 session_recovery.md §第二章启动世界·循环机制核对）")
    except Exception:
        pass
    reset_rec = ws_data.get("维护名单") or {}
    if isinstance(reset_rec, dict):
        for rname, rspec in reset_rec.items():
            if not isinstance(rspec, dict):
                continue
            # 豁免条目（触发=豁免）不触发压缩校验——豁免=记忆保留·非重置压缩（2026-08-17 加入）
            if str(rspec.get("触发", "")).strip() == "豁免":
                continue
            cfp = world_dir / "states" / f"{CHAR_STATE_PREFIX}{rname}{CHAR_STATE_SUFFIX}"
            if not cfp.exists():
                continue
            try:
                cdata = yaml.safe_load(cfp.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            # 档位读 CHAR_state.自主性（角色自身）——维护名单是园区台账·不含角色主观状态（园区不知晓觉醒程度）
            rlvl = str(cdata.get("自主性", "") or "").strip()
            mem = cdata.get("记忆锚点", "")
            if isinstance(mem, list):
                has_frag = any("碎片" in str(it.get("内容", "")) or "碎片" in str(it.get("时间", "")) for it in mem if isinstance(it, dict))
                has_key = any("关键锚点" in str(it.get("内容", "")) for it in mem if isinstance(it, dict))
                old_ts_left = len([it for it in mem if isinstance(it, dict) and re.search(r"第\d+日", str(it.get("时间", "")))])
            elif isinstance(mem, str):
                has_frag = "碎片" in mem
                has_key = "关键锚点" in mem
                old_ts_left = len(re.findall(r"\[第\d+日/", mem))
            else:
                continue
            if rlvl == "脚本" and old_ts_left:
                warnings.append(f"重置落地校验: {cfp.name} 重置档位=脚本——应全清回基线·但记忆锚点仍有 {old_ts_left} 条带时间戳旧锚点残留")
            elif rlvl in ("漂移", "觉醒"):
                if not has_frag:
                    warnings.append(f"重置落地校验: {cfp.name} 重置档位={rlvl}——记忆锚点应含「碎片·缺时间感」压缩条目·但未找到")
                if rlvl == "觉醒" and not has_key:
                    warnings.append(f"重置落地校验: {cfp.name} 重置档位=觉醒——应保留关键锚点标记·但未找到「关键锚点」条目")
                if old_ts_left and rlvl == "漂移":
                    warnings.append(f"重置落地校验: {cfp.name} 重置档位=漂移——保留规则仅限「可揭示+重复≥2次+最后高刺激」·但有 {old_ts_left} 条带时间戳旧锚点残留")

    # 8c. 叙事新鲜度（焦点场景 narrative.md mtime vs world_state.yaml——叙事落后=可能未落盘）
    try:
        ws_fp2 = world_dir / "states" / "world_state.yaml"
        if ws_fp2.exists():
            ws2 = yaml.safe_load(ws_fp2.read_text(encoding="utf-8")) or {}
            focus_id2 = str(ws2.get("焦点场景", "") or "").strip()
            if focus_id2 and scene_dir and scene_dir.is_dir():
                nf = scene_dir / "narrative.md"
                if nf.exists():
                    if nf.stat().st_mtime < ws_fp2.stat().st_mtime - 300:  # 早于 world_state 5 分钟以上
                        warnings.append(f"叙事新鲜度: {scene_dir.name}/narrative.md 修改时间早于 world_state.yaml——叙事可能未落盘（每轮阶段2 叙事应经 write_narrative.py 写入，缺失=连续性断裂）")
                else:
                    warnings.append(f"叙事新鲜度: {scene_dir.name}/narrative.md 不存在（焦点场景叙事文件缺失）")
    except Exception:
        pass

    # 8d. CRLF 行尾检测（防 Windows/rsync 引入 CRLF——破坏 shell 语法与脚本解析）
    crlf_hits = []
    for cfp in sorted(world_dir.rglob("*")):
        if not cfp.is_file() or ".git" in cfp.parts:
            continue
        if cfp.suffix not in (".yaml", ".md", ".sh", ".txt"):
            continue
        try:
            if b"\r\n" in cfp.read_bytes():
                crlf_hits.append(str(cfp.relative_to(world_dir.parent)))
        except Exception:
            continue
    if crlf_hits:
        shown = "；".join(crlf_hits[:5])
        more = f" 等 {len(crlf_hits)} 个" if len(crlf_hits) > 5 else ""
        warnings.append(f"CRLF 行尾: {len(crlf_hits)} 个文件含 \\r\\n（Windows/rsync 引入·会破坏 shell 语法）——应转 LF（.gitattributes 已锁定 eol=lf，git add 自动规范化）: {shown}{more}")

    # 8e. 区域一致性（场景切换主判据·机械复核——硬拦在 round-check，此处仅提示）
    try:
        rc_fail = _region_consistency(world_dir)
        if rc_fail:
            warnings.append(rc_fail)
    except Exception:
        pass

    if errors:
        print(f"[VALIDATE] {len(errors)} 个问题（硬性·exit 1——坏文件必须先修复再继续）:")
        for e in errors:
            print(f"  - {e}")
    elif warnings:
        print(f"[VALIDATE] 格式通过 ✅，{len(warnings)} 个内容警告:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print(f"[VALIDATE] 全部 {len(files)} 个文件验证通过 ✅")
    return len(errors)

# ── STORYLINE / BEAT（结构归②编剧·指针归③导演）─────────────
def _storyline_usage():
    print("用法: worldctl.py <世界> storyline <子命令> [参数]   ← 事件线结构（states/storylines.yaml·②编剧唯一通道）", file=sys.stderr)
    print("  show [SL-XX]       读事件线（全部 / 指定）", file=sys.stderr)
    print("  add                stdin YAML 建线（id 自动递增 SL-XX·结构蓝图无当前拍——指针由③导演 ###BEAT: set 新线 落 direction·同批 add 用「新线」·跨批读后写实际 SL-XX）", file=sys.stderr)
    print("  rewrite SL-XX      stdin YAML 重规划（现实不承接·前提取翻但戏剧问题仍重要时）", file=sys.stderr)
    print("  close SL-XX        收束（线已演完：当前线须当前拍=余波·遗留线指针已切走凭摘要留档）——stdin YAML 必含一行 收束摘要；保留 名称/类型＋状态=已收束·清拍序·当前线收束时复位指针", file=sys.stderr)
    print("  clear SL-XX        废弃（不承接·三问全灭——前提崩塌/问题无意义/无承诺待兑现）——整条抹为空锚点·direction 指针自动复位", file=sys.stderr)
    print("add/rewrite stdin 事件线 YAML 骨架（拍序含顶点拍时须带 顶点约束 五字段）:", file=sys.stderr)
    print("  名称: 事件标识", file=sys.stderr)
    print("  类型: 对峙/追逃/营救/关系转折…", file=sys.stderr)
    print("  状态: 活跃", file=sys.stderr)
    print("  拍序:", file=sys.stderr)
    print("  - 拍名: 接触", file=sys.stderr)
    print("    空间: 地点 / 时间: 时刻（叙事时间落点） / 预估时长: N分钟 / 事件背景: 本拍依托的预设局面或上拍已落定事实", file=sys.stderr)
    print("    戏剧问题: 本拍必须回答的、有边界的戏剧问题", file=sys.stderr)
    print("    兑现形态: 证据易手/被迫承认/控制权转移/关系定性/退路封死", file=sys.stderr)
    print("  - 拍名: 顶点", file=sys.stderr)
    print("    空间: 地点 / 时间: 待定 / 预估时长: N分钟 / 戏剧问题: …", file=sys.stderr)
    print("    顶点约束:", file=sys.stderr)
    print("      关系主体:            # ≥2 去重·不区分玩家/NPC——顶点单位=关系", file=sys.stderr)
    print("      - 角色A", file=sys.stderr)
    print("      - 角色B", file=sys.stderr)
    print("      核心张力: 必须被推至临界的未决问题——点名赌注所在", file=sys.stderr)
    print("      变化维度: [关系, 认知, 决策, 资源 中选]  # 创作意图声明——想推动什么类型的转变·非验收映射", file=sys.stderr)
    print("      非玩家爆破:            # ≥1 外部角色或事件——压力供应方（主体全静止时逼上悬崖）", file=sys.stderr)


def _beat_usage():
    print("用法: worldctl.py <世界> beat <子命令> [参数]        ← 演出指针（states/direction.yaml·③导演唯一通道）", file=sys.stderr)
    print("  show               读 direction（当前事件线/当前拍/演出状态/guidance）", file=sys.stderr)
    print("  set SL-XX 拍名     初始指针（建线后由③导演设定起点拍·进入顶点时自动记录基准快照·同批 add 用「新线」·跨批写实际 SL-XX）", file=sys.stderr)
    print("  deepen SL-XX       续演当前拍（问题未兑现·正逼近临界·指针不动·无写入·旧名 stay）", file=sys.stderr)
    print("  advance SL-XX 拍名 推进指针（校验拍名在拍序中·禁回退·重规划走 storyline rewrite）", file=sys.stderr)


def _validate_storyline(line) -> str | None:
    """校验单条事件线结构（结构蓝图——无 当前拍·指针权威在 direction）。返回错误描述，None=通过。"""
    if not isinstance(line, dict):
        return "事件线必须是映射（名称/类型/状态/拍序）"
    if "名称" not in line or not str(line.get("名称", "")).strip():
        return "缺 名称（当前跨轮展开的戏剧事件标识）"
    seq = line.get("拍序")
    if not isinstance(seq, list) or not seq:
        return "拍序 必须是非空 yaml 列表（元素: 拍名/空间/时间/预估时长/戏剧问题/兑现形态）"
    names = []
    for b in seq:
        if not isinstance(b, dict):
            return "拍序 元素必须是映射（拍名/空间/时间/预估时长/戏剧问题）"
        nm = str(b.get("拍名", "")).strip()
        if nm not in BEAT_ENUM:
            return f"拍名 '{nm}' 非法（枚举: {'/'.join(BEAT_ENUM)}）"
        if nm in names:
            return f"拍名 '{nm}' 重复"
        names.append(nm)
        ev = str(b.get("戏剧问题", "") or "").strip()
        if not ev:
            return f"拍名 '{nm}' 缺戏剧问题（本拍必须回答的、有边界的戏剧问题·禁止空值）"
        if any(word in ev for word in ("加剧", "深化", "持续", "不断")) and not any(mark in ev for mark in ("？", "?")):
            return f"拍名 '{nm}' 的戏剧问题是无界持续描述（改写为可回答的戏剧问题）"
    if len(names) == 1:
        return "拍序仅1拍——新线从铺垫/接触起拍·至少含2拍·余波由 advance 推进到达"
    if names and names[0] == "余波":
        return "首拍为余波——新线从铺垫/接触起拍·余波由 advance 推进到达"
    return None


def _storyline_landing_error(line) -> str | None:
    """顶点约束（Vertex Constraint）校验（add/rewrite 时硬性·当场反馈）：
    拍序含顶点拍时必须有 顶点约束——关系主体 ≥2（去重·不区分玩家/NPC·顶点单位=关系）/
    核心张力非空（未决问题·点名赌注所在）/ 变化维度 ⊆ 枚举且非空 / 非玩家爆破 ≥1（外部角色或事件·加压力量）。
    五个字段声明的是临界本身——实现形式由现场演出决定。
    拍序无顶点拍 → 放行；旧字段 顶点落点（角色/内部变量/预期形态）在场 → 拒绝（rewrite 迁移）。"""
    for b in line.get("拍序") or []:
        if not isinstance(b, dict) or str(b.get("拍名", "") or "").strip() != "顶点":
            continue
        if "顶点落点" in b:
            return "顶点拍仍在用旧字段 顶点落点（答题式 Outcome·已废弃）——改写为 顶点约束（关系主体/核心张力/变化维度/非玩家爆破）后 rewrite"
        cons = b.get(CLIMAX_CONSTRAINT_KEY)
        if not isinstance(cons, dict):
            return "顶点拍缺 顶点约束（五字段：关系主体≥2/核心张力/变化维度/非玩家爆破≥1/基准快照）"
        principals = [str(x).strip() for x in (cons.get("关系主体") or []) if str(x).strip()]
        if len(set(principals)) < 2:
            return "顶点约束.关系主体 需 ≥2 去重角色（顶点的单位是关系不是单人·不区分玩家/NPC）"
        if not str(cons.get("核心张力", "") or "").strip():
            return "顶点约束.核心张力 为空（必须被推至临界的未决问题——一句话点名赌注所在）"
        dims = [str(d).strip() for d in (cons.get("变化维度") or []) if str(d).strip()]
        bad = [d for d in dims if d not in DIM_ENUM]
        if not dims or bad:
            return f"顶点约束.变化维度 非法（{bad or '空'}——枚举: {'/'.join(DIM_ENUM)}·立场/承诺/信息由认知·关系承载）"
        blasters = [str(x).strip() for x in (cons.get("非玩家爆破") or []) if str(x).strip()]
        if not blasters:
            return "顶点约束.非玩家爆破 为空（≥1 外部角色或事件——主体静止时的加压力量·防死锁）"
        if CLIMAX_BASELINE_KEY in cons:
            return f"顶点约束.{CLIMAX_BASELINE_KEY} 已改为脚本私有落档（.climax_baseline_*.yaml·自动记录）——从约束中移除该字段"
        break
    return None


def _next_storyline_id(beats: dict) -> str:
    """下一个事件线编号（SL-XX·数字递增两位；兼容旧纯数字 N）。"""
    max_n = 0
    for k in beats:
        m = re.match(r"^(?:SL-)?(\d+)$", str(k), re.IGNORECASE)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"{STORYLINE_ID_PREFIX}{max_n + 1:02d}"


def _empty_beat_warnings(line) -> list[str]:
    """检查事件线拍序：空间/时间/戏剧问题 任一为空的拍 → 警告列表。
    建线应预设完整拍序内容（拍=规划蓝图）；推进/换线后空拍仍在 = 现实与该拍无法承接（需 rewrite 补填或明确留空）。
    预估时长 / 兑现形态 缺失 → 各自独立软警（不计入硬性「内容不完整」·不阻塞）——
    预估时长缺失由③现场重估自愈；兑现形态缺失由③回判「自然完成判进」兜底（判据=phase_storyliner D6）。"""
    warns = []
    seq = line.get("拍序") or []
    if not isinstance(seq, list):
        return warns
    for b in seq:
        if not isinstance(b, dict):
            continue
        nm = str(b.get("拍名", "") or "").strip()
        missing = [f for f in ("空间", "时间", "戏剧问题") if not str(b.get(f, "")).strip()]
        if missing:
            warns.append(f"拍 '{nm}' 内容不完整（缺: {'/'.join(missing)}）——建线应预设完整拍序·现实与空拍无法承接·需 rewrite 补填")
            continue
        if not str(b.get("预估时长", "") or "").strip():
            warns.append(f"拍 '{nm}' 缺 预估时长（③时间窗口预算的默认源·建议补填 N分钟·缺失时③现场重估直接定值）")
        if not str(b.get("兑现形态", "") or "").strip():
            warns.append(f"拍 '{nm}' 缺 兑现形态（问题被回答时的可观察形态：证据易手/被迫承认/控制权转移/关系定性/退路封死·判据=phase_storyliner D6）")
    # 存量提醒（validate/遗留数据·新建由 _validate_storyline 硬拦）：单拍/首拍余波·顶点
    if isinstance(seq, list) and seq:
        _first = seq[0] if isinstance(seq[0], dict) else {}
        _first_beat = str(_first.get("拍名", "") or "").strip()
        if len(seq) == 1 and _first_beat == "余波":
            warns.append("单拍余波线——新线从铺垫/接触起拍·至少含2拍·余波由 advance 推进到达（存量线走 rewrite 补拍序）")
        elif _first_beat in ("余波", "顶点"):
            warns.append(f"首拍为'{_first_beat}'——新线从铺垫/接触起拍·余波由 advance 推进到达（存量线走 rewrite 补拍序）")
    return warns


def _warn_empty_beats(n: str, line) -> None:
    """对单条事件线打印空拍警告（add/rewrite 后调用·软性不拦截）。"""
    for w in _empty_beat_warnings(line):
        print(f"[WARN] {STORYLINE_TOP_KEY} 事件线 {n} {w}", file=sys.stderr)


def cmd_storyline(world_dir: Path, extra: list[str], stdin_text: str | None = None):
    """事件线结构维护（states/storylines.yaml）——②编剧唯一通道（###STORYLINE 自动执行·LLM 不直接改 YAML）。
    结构/枚举校验后机械写入。stdin_text: write-raw 自动执行时传入 add/rewrite 的事件线 YAML。"""
    fp = world_dir / "states" / STORYLINES_FILE
    data = _load_storylines(world_dir)
    beats = data.get(STORYLINE_TOP_KEY)
    if beats is None:
        beats = {}
    if not isinstance(beats, dict):
        print(f"[ERR] {STORYLINE_TOP_KEY} 已存在但非映射结构: {type(beats).__name__}", file=sys.stderr)
        sys.exit(1)

    if not extra or extra[0] in ("--help", "-h"):
        _storyline_usage()
        sys.exit(0 if extra else 1)
    sub = extra[0]

    if sub == "show":
        sid = _norm_sl_id(extra[1]) if len(extra) > 1 else None
        if sid is not None:
            line = beats.get(sid)
            if line is None:
                print(f"[ERR] {STORYLINE_TOP_KEY} 无事件线 {sid}", file=sys.stderr)
                sys.exit(1)
            out = {sid: line}
        else:
            out = beats
        yaml.dump(out, sys.stdout, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        return

    if sub == "add":
        line = yaml.safe_load(stdin_text if stdin_text is not None else _read_stdin_utf8())
        err = _validate_storyline(line) or _storyline_landing_error(line)
        if err:
            print(f"[ERR] 事件线结构校验失败: {err}", file=sys.stderr)
            sys.exit(1)
        n = _next_storyline_id(beats)
        beats[n] = line
        data[STORYLINE_TOP_KEY] = beats
        write_yaml(fp, data)
        print(f"[OK] {STORYLINE_TOP_KEY} 事件线 {n} 已建（{sub}）——起点指针由③导演 ###BEAT: set {n} <起点拍> 落 direction")
        _warn_empty_beats(n, line)
        return n

    if sub in ("rewrite", "close", "clear"):
        if len(extra) < 2:
            _storyline_usage()
            sys.exit(1)
        n = _norm_sl_id(extra[1])
        if n not in beats:
            print(f"[ERR] {STORYLINE_TOP_KEY} 无事件线 {n}", file=sys.stderr)
            sys.exit(1)
        dr = _load_direction(world_dir)
        ptr_on_line = str(dr.get("当前事件线", "") or "").strip() == n
        cur_beat = str(dr.get("当前拍", "") or "").strip()
        if sub == "close":
            if ptr_on_line and cur_beat != "余波":
                print(f"[ERR] 当前拍='{cur_beat}' 非余波——当前线未演完不收束（中途放弃走 clear·继续演出走 deepen）", file=sys.stderr)
                sys.exit(1)
            if not ptr_on_line:
                print(f"[OK] 遗留线收束（指针已切走·凭 收束摘要 定性留档——close 触发按线自身状态判断·不依赖 direction 指针）", file=sys.stderr)
            pl = yaml.safe_load(stdin_text if stdin_text is not None else _read_stdin_utf8())
            summary = str(pl.get("收束摘要", "")).strip() if isinstance(pl, dict) else ""
            if not summary:
                print("[ERR] close 缺 收束摘要（一行结局定性——不想留档说明该走 clear 废弃）", file=sys.stderr)
                sys.exit(1)
            old = beats[n] if isinstance(beats.get(n), dict) else {}
            closed = {"名称": str(old.get("名称", "") or "").strip() or n}
            ltype = str(old.get("类型", "") or "").strip()
            if ltype:
                closed["类型"] = ltype
            closed["状态"] = "已收束"
            closed["收束摘要"] = summary
            beats[n] = closed
            bfp = _climax_baseline_fp(world_dir, n)
            if bfp.exists():
                bfp.unlink()
                print(f"[OK] 基线落档已清理（{bfp.name}）", file=sys.stderr)
            if ptr_on_line:
                dr["当前事件线"] = ""
                dr["当前拍"] = ""
                dr["当前戏剧问题"] = ""
                _save_direction(world_dir, dr)
            data[STORYLINE_TOP_KEY] = beats
            write_yaml(fp, data)
            if ptr_on_line:
                print(f"[OK] {STORYLINE_TOP_KEY} 事件线 {n} 已收束（状态=已收束·留 名称/类型/收束摘要）——direction 指针已复位·当轮须 add 新线（取材按 phase_storyliner D5）并由③导演 set 新起点（否则 round-check FAIL）")
            else:
                print(f"[OK] {STORYLINE_TOP_KEY} 事件线 {n} 已收束（状态=已收束·留 名称/类型/收束摘要）——指针未动（当前事件线不受影响）")
            return
        if sub == "clear":
            if ptr_on_line and cur_beat == "余波":
                print(f"[WARN] 当前拍='余波'——线已演完·应走 close 收束留档（本次按废弃抹除执行）", file=sys.stderr)
            if ptr_on_line:
                dr["当前事件线"] = ""
                dr["当前拍"] = ""
                dr["当前戏剧问题"] = ""
                _save_direction(world_dir, dr)
                print(f"[OK] direction 指针已复位（事件线 {n} 废弃）", file=sys.stderr)
            beats[n] = {}
            bfp = _climax_baseline_fp(world_dir, n)
            if bfp.exists():
                bfp.unlink()
                print(f"[OK] 基线落档已清理（{bfp.name}）", file=sys.stderr)
        else:
            line = yaml.safe_load(stdin_text if stdin_text is not None else _read_stdin_utf8())
            err = _validate_storyline(line) or _storyline_landing_error(line)
            if err:
                print(f"[ERR] 事件线结构校验失败: {err}", file=sys.stderr)
                sys.exit(1)
            beats[n] = line
            _warn_empty_beats(n, line)
            bfp = _climax_baseline_fp(world_dir, n)
            if bfp.exists():
                bfp.unlink()
                print(f"[WARN] 旧基线落档已清理（{bfp.name}·结构替换后过期）——若停在顶点拍·需 beat set {n} 顶点 重拍", file=sys.stderr)
        data[STORYLINE_TOP_KEY] = beats
        write_yaml(fp, data)
        print(f"[OK] {STORYLINE_TOP_KEY} 事件线 {n} 已更新（{sub}）")
        return

    _storyline_usage()
    sys.exit(1)


def cmd_beat(world_dir: Path, extra: list[str]):
    """演出指针维护（states/direction.yaml）——③导演唯一通道（###BEAT 自动执行·LLM 不直接改 YAML）。
    set=初始指针 / deepen=续演当前拍（无写入）/ advance=推进（禁回退·进入顶点自动记录基准快照）。"""
    if not extra or extra[0] in ("--help", "-h"):
        _beat_usage()
        sys.exit(0 if extra else 1)
    sub = extra[0]
    if sub == "stay":
        sub = "deepen"
    st = _load_storylines(world_dir)
    beats = st.get(STORYLINE_TOP_KEY) or {}
    dr = _load_direction(world_dir)

    if sub == "show":
        yaml.dump(dr, sys.stdout, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        return

    if sub not in ("set", "deepen", "advance") or len(extra) < (3 if sub in ("set", "advance") else 2):
        _beat_usage()
        sys.exit(1)
    sid = _norm_sl_id(extra[1])
    line = beats.get(sid)
    if not isinstance(line, dict) or not (line.get("拍序") or []):
        print(f"[ERR] 事件线 {sid} 不存在或无拍序（先 ###STORYLINE: add 建线）", file=sys.stderr)
        sys.exit(1)
    names = [str(b.get("拍名", "")) for b in line.get("拍序", []) if isinstance(b, dict)]

    if sub == "deepen":
        if str(dr.get("当前事件线", "") or "").strip() != sid or not str(dr.get("当前拍", "") or "").strip():
            print(f"[ERR] direction 指针不在事件线 {sid}（当前: {dr.get('当前事件线', '')}/{dr.get('当前拍', '')}）——deepen 需已有指针（先 set）", file=sys.stderr)
            sys.exit(1)
        print(f"[OK] direction 事件线 {sid} 续演当前拍 {dr.get('当前拍')}（deepen·指针不动·下轮继续）", file=sys.stderr)
        return

    target = extra[2]
    if target not in names:
        print(f"[ERR] 拍名 '{target}' 不在事件线 {sid} 的拍序中（拍序拍名: {names}）", file=sys.stderr)
        sys.exit(1)
    if sub == "advance":
        cur_line = str(dr.get("当前事件线", "") or "").strip()
        cur = str(dr.get("当前拍", "") or "").strip()
        if cur_line == sid and cur and cur in names and names.index(cur) > names.index(target):
            print(f"[ERR] 当前拍回退（{cur}→{target}）不允许——节拍只向前推进（重规划走 ###STORYLINE: rewrite {sid}；误推进走快照恢复 snap.py load / 无快照手工重建 write-raw --batch --force＋残留扫描＋validate·见 rollback.md）", file=sys.stderr)
            sys.exit(1)
    if sub == "set":
        cur_line = str(dr.get("当前事件线", "") or "").strip()
        cur = str(dr.get("当前拍", "") or "").strip()
        if cur_line == sid and cur and target != cur:
            print(f"[ERR] set 仅用于跨线切换/空指针初始/同拍重锚——当前指针已在事件线 {sid}（当前拍={cur}）·同线换拍用 advance {sid} <下一拍>/续演用 deepen {sid}（禁以 set 同线指拍·防绕过 advance 禁回退与顶点出线核验；rewrite 后重建顶点基线用同拍 set {sid} {cur} 重锚）", file=sys.stderr)
            sys.exit(1)
    dr["当前事件线"] = sid
    dr["当前拍"] = target
    # 当前戏剧问题缓存（validate 对账 storylines·防复制漂移）
    for b in line.get("拍序", []):
        if isinstance(b, dict) and str(b.get("拍名", "") or "").strip() == target:
            dr["当前戏剧问题"] = str(b.get("戏剧问题", "") or "").strip()
            break
    # 时间窗口默认预算导出（拍级·脚本机械导出）：预算默认源=当前拍拍序的 预估时长（编剧建线预估）。
    # 进入新拍（拍标记≠目标拍·跨拍推进/重锚）→ 重置窗口（起点=当前世界时间·预算=该拍预估时长）；
    # ③现场重估写下的预算随拍带标记·同拍不动（重估优先）；预估时长缺失 → 清空预算·③现场重估定值。
    _preset = ""
    for b in line.get("拍序", []):
        if isinstance(b, dict) and str(b.get("拍名", "") or "").strip() == target:
            _preset = str(b.get("预估时长", "") or "").strip()
            break
    _win = dr.get("时间窗口") if isinstance(dr.get("时间窗口"), dict) else {}
    _win_beat = str(_win.get("拍", "") or "").strip()
    if _win_beat != target:
        _cur_time = str((yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}).get("时间", {}).get("具体时间", "") or "").strip()
        dr["时间窗口"] = {"拍": target, "起点": _cur_time, "预算": _preset}
        if _preset:
            print(f"[OK] 时间窗口 默认预算 ← 拍序预估时长（{target}·{_preset}·③可现场重估覆盖）", file=sys.stderr)
        else:
            print(f"[OK] 时间窗口 已重置（{target}·拍序无 预估时长·③现场重估定值）", file=sys.stderr)
    _save_direction(world_dir, dr)
    if target == "顶点":
        _snapshot_climax_baseline(line, world_dir, sid)
        st.setdefault(STORYLINE_TOP_KEY, {})[sid] = line
        write_yaml(world_dir / "states" / STORYLINES_FILE, st)
        print(f"[OK] 顶点约束.基准快照 已记录（事件线 {sid} 进入顶点拍·仅关系主体·按声明维度字段族）", file=sys.stderr)
        # 顶点爆破载体核验（软警·不拦）：顶点约束声明的 非玩家爆破 须有事实层载体可承载——
        #   两档与停滞加压同系统（事实层登记通道）：world_state.外部倒计时 / conflicts.CT-XX.关联角色。
        #   （scene_state.出场角色摘要 不计入：那是叙事层散文摘要·非事实登记通道·不能「承载」外部到场。）
        #   载体全无 = 爆破只活在设计文本里·顶点有长驻空转风险（①次轮触 CT 时由 CT待结算 自然补登）。
        #   软警而非硬拦：顶点跨多轮·入拍当轮爆破未必当即到场；此提示只暴露风险·不阻断推进。
        #   ⚠ 判据必须**按声明的爆破逐条对号**（2026-09-18 修）：旧实现只问「世界里有无任意载体」，
        #     而活跃世界恒有 CD-LOOP 之类的无关倒计时与非空 CT.关联角色 → 恒真 → 该软警永不触发，
        #     即便声明的爆破（如「Mesa 回收队抵达」）事实层零载体也同样被静默放过（r68 实际即此态）。
        #     改为：在载体集合中检索「该爆破是否有承载者」——爆破名（或其去括注关键词）须落在某载体的
        #     文本里，或该载体名出现在爆破描述中。命中任一即视为已登记；全不命中才报。
        _cons = None
        for _b in (line.get("拍序") or []):
            if isinstance(_b, dict) and str(_b.get("拍名", "") or "").strip() == "顶点":
                _cons = _b.get(CLIMAX_CONSTRAINT_KEY)
                break
        _blasters = [str(x).strip() for x in ((_cons or {}).get("非玩家爆破") or []) if str(x).strip()]
        if _blasters:
            # 载体集合：每条载体归一为可检索文本（含其名称与承载者）
            _carriers: list[str] = []
            try:
                _ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
            except Exception:
                _ws = {}
            for _cdk, _cdv in (_ws.get("外部倒计时") or {}).items():
                _bits = [str(_cdk)]
                if isinstance(_cdv, dict):
                    _bits += [str(_cdv.get(_n, "") or "") for _n in ("名称", "类型", "事件", "说明", "描述")]
                _carriers.append(" ".join(_bits))
            try:
                _cf = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
            except Exception:
                _cf = {}
            for _ck, _cv in _cf.items():
                if not str(_ck).startswith("CT-") or not isinstance(_cv, dict):
                    continue
                _rels = _cv.get("关联角色") or []
                if isinstance(_rels, str):
                    _rels = [_rels]
                _bits = [str(_ck), str(_cv.get("名称", "") or ""), str(_cv.get("描述", "") or "")]
                _bits += [str(_r) for _r in _rels if str(_r).strip()]
                _carriers.append(" ".join(_bits))
            if not _carriers:
                print(f"[WARN] 顶点约束.非玩家爆破 声明了 {'、'.join(_blasters[:3])}，但事实层未登记任何载体"
                      f"（外部倒计时/CT关联角色皆无）——爆破若长期无载体则只能停留在设计文本·"
                      f"顶点有长驻空转风险；首次触及资源/关系/退路的行动将触发 CT待结算 补登", file=sys.stderr)
            else:
                # 逐条爆破判定：爆破名/关键词 与 载体文本 互含即视为该爆破已登记
                def _blaster_registered(_bl: str) -> bool:
                    _bl_norm = re.sub(r"\s+", "", _bl)
                    # 关键词 = 去括注后的主句切出的实词片段（≥2 字·用于泛化「Mesa 回收队」这类点名）
                    _head = re.split(r"[（(]", _bl)[0]
                    _keys = [k for k in re.split(r"[\s·,，、;；/]+", _head) if len(k) >= 2]
                    for _c in _carriers:
                        _c_norm = re.sub(r"\s+", "", _c)
                        if _c_norm and (_c_norm in _bl_norm or _bl_norm in _c_norm):
                            return True
                        for _k in _keys:
                            if _k and _k in _c_norm:
                                return True
                    return False
                _unregistered = [b for b in _blasters if not _blaster_registered(b)]
                if _unregistered:
                    print(f"[WARN] 顶点约束.非玩家爆破 声明了 {'、'.join(_unregistered[:3])}"
                          f"{' 等' if len(_unregistered) > 3 else ''}，但事实层未在载体中检索到对应承载者"
                          f"（已查 外部倒计时 {len(_carriers)} 条载体）——该爆破只活在设计文本里·"
                          f"顶点有长驻空转风险；须登记其到场时钟（world_state.外部倒计时）或承载主体（CT-XX.关联角色）", file=sys.stderr)
    print(f"[OK] direction 事件线 {sid} 当前拍 → {target}（{sub}）", file=sys.stderr)


def cmd_tmp_clean(world_dir: Path):
    """清理世界临时文件目录（worlds/{世界名}/tmp/）——过程临时文件（批次/叙事草稿）用后即删；
    跨会话恢复时由加载序列调用。删除整个目录（下次写入可再生），不存在则提示无需清理。"""
    tmp_dir = world_dir / "tmp"
    if not tmp_dir.exists():
        print("[OK] tmp 目录不存在·无需清理")
        return
    n = sum(1 for _ in tmp_dir.rglob("*"))
    require_world_marker(world_dir)
    safe_rmtree(tmp_dir)
    print(f"[OK] tmp 清理完成: 删除 {n} 个文件（{world_dir.name}/tmp/）")


# ── LINT / FIX 引号/类型规范化 ────────────────────────────────────
_LEADING_SPECIAL = re.compile(r"^[\s]*(- |[\-\[\{\"#&*!|>%@`,? ])")
_YAML_BOOL_NULL = re.compile(r"^(yes|no|on|off|true|false|~|null)$", re.IGNORECASE)
_NUM_RE = re.compile(r"^(0[xXoO][0-9a-fA-F]+|\d+([.]\d*)?([eE][+-]?\d+)?|[+-]?\d+([.]\d*)?([eE][+-]?\d+)?)$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$")


def _strip_yaml_inline_comment(raw: str) -> str:
    """从 raw 值中剥离尾部 YAML 行内注释（# ...），保留引号包裹的实际值。
    处理：'...' # comment / "..." # comment / 无引号值尾部 # comment。"""
    raw_s = raw.rstrip()
    if not raw_s:
        return raw_s
    if raw_s.startswith("'"):
        i = 1
        while i < len(raw_s):
            if raw_s[i] == "'":
                if i + 1 < len(raw_s) and raw_s[i + 1] == "'":
                    i += 2
                else:
                    rest = raw_s[i + 1:].strip()
                    if not rest or rest.startswith("#"):
                        return raw_s[:i + 1]
                    return raw_s
            i += 1
    elif raw_s.startswith('"'):
        i = 1
        while i < len(raw_s):
            if raw_s[i] == "\\":
                i += 2
            elif raw_s[i] == '"':
                rest = raw_s[i + 1:].strip()
                if not rest or rest.startswith("#"):
                    return raw_s[:i + 1]
                return raw_s
            i += 1
    else:
        # 无引号值：剥离尾部 ` #...` 注释（YAML 规范：# 前须有空白才起注释）
        m = re.search(r"\s+#", raw_s)
        if m:
            candidate = raw_s[:m.start()].rstrip()
            if candidate:
                return candidate
    return raw_s


def _check_raw_needs_quoting(raw: str) -> tuple[bool, str]:
    """判断裸值是否需要引号包裹。返回 (needs_quote, reason)。"""
    if not raw:
        return False, ""
    # 先剥离注释再判断——注释不影响引号/类型安全
    clean = _strip_yaml_inline_comment(raw)
    # 已有引号包裹（单引号/双引号）→ 值安全，不需额外引号
    if (clean.startswith("'") and clean.endswith("'") and len(clean) >= 2) or \
       (clean.startswith('"') and clean.endswith('"') and len(clean) >= 2):
        return False, ""
    # 空容器 / block scalar 标记（去注释后）
    if clean in ("{}", "[]", "|", ">"):
        return False, ""
    # 以特殊字符开头 → 需引号
    if _LEADING_SPECIAL.match(clean):
        return True, "以特殊字符开头"
    # 含半角冒号+空格（YAML key: value 分隔符）→ 需引号
    if ":" in clean:
        for m in re.finditer(r":\s", clean):
            if m.start() > 0:
                return True, "含半角冒号+空格"
    # 隐式类型
    if _YAML_BOOL_NULL.match(clean):
        return True, "隐式类型(bool/null)"
    if _NUM_RE.match(clean) and not clean.startswith("0x") and not clean.startswith("0o"):
        return True, "隐式类型(数字)"
    if _DATE_RE.match(clean):
        return True, "隐式类型(日期)"
    return False, ""


def _to_single_quoted(val: str) -> str:
    escaped = val.replace("'", "''")
    return f"'{escaped}'"


def _detect_raw_needs_quoting(file_text: str) -> list[dict]:
    """逐行扫描原始 YAML 文本，报告需要引号包裹的值。"""
    issues = []
    in_block = False
    block_indent = 0
    in_multiline_quote = False  # 多行引号值（'...' 跨行）
    for lineno, line in enumerate(file_text.splitlines(), 1):
        if in_block:
            stripped = line.lstrip()
            if stripped and not stripped.startswith("#"):
                cur_indent = len(line) - len(stripped)
                if cur_indent <= block_indent:
                    in_block = False
                else:
                    continue
            elif not stripped:
                continue
            else:
                continue
        if in_multiline_quote:
            # 多行引号值：寻找闭合引号
            if "'" in line or '"' in line:
                # 简化检测：如果本行有闭合引号，退出多行模式
                for q in ("'", '"'):
                    if q in line:
                        # 检查是否有不被转义的闭合引号
                        count = line.count(q) - line.count(q * 2)
                        if count % 2 == 1:
                            in_multiline_quote = False
                            break
            continue
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^(\s*)(- )?(\S.*?)(:)(\s+.+)?$", line)
        if not m:
            continue
        indent, dash, key, colon, raw_part = m.groups()
        raw = (raw_part or "").strip() if raw_part else ""
        if raw in ("|", ">"):
            in_block = True
            block_indent = len(indent) + (2 if dash else 0) + len(key) + 1
            continue
        if not raw:
            continue
        if raw.startswith("[") and raw.endswith("]"):
            continue
        if raw.startswith("{") and raw.endswith("}"):
            continue
        # 检测多行引号值（起始引号但本行无闭合引号）
        if (raw.startswith("'") and not raw.endswith("'")) or \
           (raw.startswith('"') and not raw.endswith('"')):
            in_multiline_quote = True
            continue
        needs, reason = _check_raw_needs_quoting(raw)
        if needs:
            issues.append({"line": lineno, "key": key.strip(), "raw": raw, "reason": reason})
    return issues


def _fix_yaml_text(data: dict | list | None, original_text: str) -> str:
    """规范化 YAML：修复所有字符串值的引号/类型，保留 key 顺序、注释、block scalar。"""
    lines = original_text.splitlines(keepends=True)
    result = []
    in_block = False
    block_indent = 0
    in_multiline_quote = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if in_block:
            cur_indent = len(line) - len(stripped) if stripped else 999
            if stripped and not stripped.startswith("#"):
                if cur_indent <= block_indent:
                    in_block = False
                else:
                    result.append(line)
                    i += 1
                    continue
            elif not stripped:
                result.append(line)
                i += 1
                continue
            else:
                result.append(line)
                i += 1
                continue
        if in_multiline_quote:
            # 多行引号值：等待闭合引号
            result.append(line)
            if ("'" in line or '"' in line):
                for q in ("'", '"'):
                    if q in line:
                        count = line.count(q) - line.count(q * 2)
                        if count % 2 == 1:
                            in_multiline_quote = False
                            break
            i += 1
            continue
        if not stripped or stripped.startswith("#"):
            result.append(line)
            i += 1
            continue
        m = re.match(r"^(\s*)(- )?(\S.*?)(:)(\s+.+)?$", line.rstrip("\n"))
        if not m:
            result.append(line)
            i += 1
            continue
        indent, dash, key, colon, raw_part = m.groups()
        raw = (raw_part or "").strip() if raw_part else ""
        if raw in ("|", ">"):
            in_block = True
            block_indent = len(indent) + (2 if dash else 0) + len(key) + 1
            result.append(line)
            i += 1
            continue
        if not raw or (raw.startswith("[") and raw.endswith("]")) or (raw.startswith("{") and raw.endswith("}")):
            result.append(line)
            i += 1
            continue
        # 检测多行引号值（起始引号但本行无闭合引号）
        if (raw.startswith("'") and not raw.endswith("'")) or \
           (raw.startswith('"') and not raw.endswith('"')):
            in_multiline_quote = True
            result.append(line)
            i += 1
            continue
        already_quoted = (raw.startswith("'") and raw.endswith("'") and len(raw) >= 2) or \
                         (raw.startswith('"') and raw.endswith('"') and len(raw) >= 2)
        if already_quoted:
            inner = raw[1:-1]
            expected = _to_single_quoted(inner)
            if raw != expected:
                prefix = f"{indent}{dash or ''}{key}{colon} "
                result.append(f"{prefix}{expected}\n")
                i += 1
                continue
            result.append(line)
            i += 1
            continue
        needs_q, _ = _check_raw_needs_quoting(raw)
        if needs_q:
            prefix = f"{indent}{dash or ''}{key}{colon} "
            result.append(f"{prefix}{_to_single_quoted(raw)}\n")
            i += 1
            continue
        result.append(line)
        i += 1
    return "".join(result)


def cmd_lint(world_dir: Path):
    """lint: 逐文件报告 YAML 引号/类型问题（只读）。"""
    scene_dir = get_scene_dir(world_dir)
    files = discover_files(world_dir, scene_dir)
    total_issues = 0
    broken_files = 0
    for key in sorted(files):
        fp = files[key]
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERR] {key}: 读取失败: {e}")
            continue
        try:
            yaml.safe_load(text)
        except yaml.YAMLError as e:
            print(f"[BROKEN] {key}: YAML 解析错误: {e}")
            broken_files += 1
            continue
        issues = _detect_raw_needs_quoting(text)
        if issues:
            for iss in issues:
                print(f"  L{iss['line']:3d}  {iss['key']}:  {iss['raw'][:40]}  → {iss['reason']}")
            total_issues += len(issues)
            print(f"[WARN] {key}: {len(issues)} 个值需要引号/类型修复")
        else:
            print(f"[OK] {key}: 无问题")
    print(f"\n汇总: {len(files)} 个文件, {broken_files} 个坏文件（需手动修复）, {total_issues} 个值需要引号/类型修复")
    if broken_files:
        print("坏文件无法被 write-raw 解析·拒绝写入——先用编辑器直接修复引号后再走 write-raw")


def cmd_fix(world_dir: Path):
    """fix: 规范化重写所有 YAML 状态文件（snap 自动备份 + validate）。"""
    scene_dir = get_scene_dir(world_dir)
    files = discover_files(world_dir, scene_dir)
    fixed = 0
    skipped = 0
    broken = 0
    for key in sorted(files):
        fp = files[key]
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERR] {key}: 读取失败: {e}")
            continue
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            print(f"[SKIP] {key}: YAML 解析错误（坏文件·需手动修复）: {e}")
            broken += 1
            continue
        if data is None:
            print(f"[SKIP] {key}: 空文件")
            skipped += 1
            continue
        fixed_text = _fix_yaml_text(data, text)
        if fixed_text == text:
            skipped += 1
            continue
        bak = fp.with_suffix(".yaml.fix.bak")
        bak.write_text(text, encoding="utf-8", newline="")
        fp.write_text(fixed_text, encoding="utf-8", newline="")
        print(f"[FIX] {key}: 已修复（备份 → {bak.name}）")
        fixed += 1
    if fixed:
        print(f"\n已修复 {fixed} 个文件，跳过 {skipped} 个，坏文件 {broken} 个")
        print("正在 validate...")
        cmd_validate(world_dir)
    else:
        print(f"\n无需修复（{skipped} 个文件已是最新，坏文件 {broken} 个）")


def cmd_reset_cycle(world_dir: Path, world_name: str, asset: str = None):
    """循环世界重置——周期重置（循环日终/到期点）或事件重置（单角色 --asset）。
    周期（缺省）：机械重置在册全员·登记维护名单·重建周期倒计时。
    事件（--asset <角色>）：只机械重置指定角色·登记事件条目·不重建周期倒计时（叙事事件不移动周期重置点）。
    触发：周期=write-raw audit ④b 顶回后执行（或恢复序列 4.6②）；事件=叙事中角色被系统强制重置（loop_machinery §4 触发管道之二）。
    脚本做机械部分：
    连续行动轨迹清空 / 记忆锚点按自主性档位压缩（脚本全清·漂移/觉醒压缩+输出保留候选·变质保留）/
    状态字段回基线占位 / 压力防御回默认（觉醒/变质保留防御崩解）/ 人际动态与决策清空（LLM 按 CHAR_.md 默认循环时间线补写）/
    信念演化与自主性保留 / 自动存档（snap.py save _before_）/ 登记维护名单 / 周期模式重建周期倒计时（到期时刻+1 周期）。
    LLM 只做：保留候选确认/微调 + 状态字段按 CHAR_.md 默认循环时间线补写 + CT 节拍核查 + 重置叙事。"""
    ws_fp = world_dir / "states" / "world_state.yaml"
    if not ws_fp.exists():
        print("[ERR] world_state.yaml 不存在", file=sys.stderr)
        return 1
    ws = yaml.safe_load(ws_fp.read_text(encoding="utf-8")) or {}
    cur_time = str(ws.get("时间", {}).get("具体时间", "") or "").strip()
    cur_round = str(ws.get("轮次", "0") or "0").strip()
    cur_day = None
    _, _m = _parse_world_time(cur_time)
    if _m is None:
        print(f"[ERR] 当前时间无法解析（需 '第N日 HH:MM' 格式）: '{cur_time}'", file=sys.stderr)
        return 1
    dm, _ = _parse_world_time(cur_time)
    cur_day = dm

    # 定位周期重置倒计时（含 到期时刻）
    cds = ws.get("外部倒计时") or {}
    cd_id, cd_spec = None, None
    if isinstance(cds, dict):
        for cid, cspec in cds.items():
            if isinstance(cspec, dict) and str(cspec.get("到期时刻", "") or "").strip():
                cd_id, cd_spec = cid, cspec
                break
    if cd_id is None:
        print("[WARN] 未找到含 到期时刻 的周期倒计时——重置仍执行（周期倒计时登记见 session_recovery.md §第二章启动世界·循环机制核对）", file=sys.stderr)

    # 0. 自动存档（可回滚·存档失败即中止——不可回滚就不执行重置）
    # 安全加固：world_name 必须为合法世界目录名（禁空/路径分隔符/..·与 snap.py validate_name 同规则）——防非法名传入外部脚本
    if not world_name or re.search(r"[\\/]|\.\.", world_name):
        print(f"[ERR] 非法世界名 '{world_name}'——拒绝调用 snap.py（禁止路径分隔符/../相对路径穿越）", file=sys.stderr)
        sys.exit(1)
    snap_name = f"_before_reset_{'asset_' + asset if asset else 'cycle_' + world_name}_{_ts()}"
    snapshot_or_abort(world_name, snap_name)

    # 机械重置（周期=全员含焦外·事件=单角色 --asset）
    candidates = []          # (角色, 档位, 被压缩条目) 保留候选
    key_anchor_kw = ("承诺", "命名", "关系转折", "决定", "记得", "承诺", "他/她")
    if asset:
        cfps = [world_dir / "states" / f"{CHAR_STATE_PREFIX}{asset}{CHAR_STATE_SUFFIX}"]
        if not cfps[0].exists():
            print(f"[ERR] 未找到角色状态文件: {cfps[0].name}（--asset 用角色名·如 Angela）", file=sys.stderr)
            return 1
    else:
        cfps = sorted(world_dir.glob(f"states/{CHAR_STATE_PREFIX}*{CHAR_STATE_SUFFIX}"))
    for cfp in cfps:
        try:
            cdata = yaml.safe_load(cfp.read_text(encoding="utf-8")) or {}
        except Exception as e:
            print(f"[WARN] {cfp.name} 解析失败·跳过: {e}", file=sys.stderr)
            continue
        # 豁免判定（硬性）：自主性 字段仅循环角色有（模板语义）——外部者/管理者（Guest/Ford/Stubbs 等）
        #   无此字段 → 豁免周期重置（loop_machinery §4 豁免）。事件型角色（死亡即回收·如 Teddy/Hector）
        #   = 循环角色（有自主性字段）——周期时刻若活着度过当日，同样按「次日清晨仍按循环日终重置」执行，不豁免
        if "自主性" not in cdata or not str(cdata.get("自主性", "") or "").strip():
            print(f"[SKIP] {cfp.stem}: 无自主性字段（外部者/管理者·豁免周期重置）")
            continue
        # 豁免条目（2026-08-17 加入·2026-09-18 改名单语义）：维护名单 触发=豁免 → 跳过该资产
        #   豁免=名单条目·作用域由园区增删条目承载（不设期限字段·判定只读 触发）
        _rname = cfp.stem[len(CHAR_STATE_PREFIX):-len("_state")]
        _rr = ws.get("维护名单") or {}
        if isinstance(_rr, dict) and _rname in _rr and isinstance(_rr[_rname], dict) \
                and str(_rr[_rname].get("触发", "")) == "豁免":
            print(f"[SKIP] {cfp.stem}: 已豁免（维护名单·园区未对其执行维护）")
            continue
        lvl = str(cdata.get("自主性", "") or "").strip()
        old_mem = cdata.get("记忆锚点")
        # 记忆锚点按档位压缩
        if lvl == "脚本":
            new_mem = []
        elif lvl == "变质":
            new_mem = old_mem  # 几乎全保留（时间位抹除交给戏剧家）
        else:  # 漂移/觉醒：压缩为碎片 + 保留候选清单
            kept, removed = [], []
            if isinstance(old_mem, list):
                for it in old_mem:
                    if not isinstance(it, dict):
                        removed.append(it)
                        continue
                    content = str(it.get("内容", ""))
                    ts = str(it.get("时间", ""))
                    mark = str(it.get("标记", ""))
                    if "碎片" in content or "碎片" in ts or "可揭示" in mark:
                        kept.append(it)
                    elif lvl == "觉醒" and any(k in content for k in key_anchor_kw):
                        kept.append(it)
                    else:
                        removed.append(it)
                if kept and not any("碎片" in str(k.get("时间", "")) or "碎片" in str(k.get("内容", "")) for k in kept):
                    last = kept[-1] if kept else None
                    kept = kept[-1:]
                if not kept and removed:
                    last = removed[-1]
                    last = dict(last) if isinstance(last, dict) else {"内容": str(last)}
                    last["时间"] = "碎片"
                    kept = [last]
            elif old_mem:
                removed = [old_mem]
                last = dict(old_mem) if isinstance(old_mem, dict) else {"内容": str(old_mem)}
                last["时间"] = "碎片"
                kept = [last]
            new_mem = kept
            for it in removed:
                candidates.append((cfp.stem, lvl, str(it)[:120]))
        cdata["记忆锚点"] = new_mem if isinstance(new_mem, list) else ([] if not new_mem else [new_mem])
        # 轨迹清空（联动表·新循环从零累积）
        cdata["连续行动轨迹"] = []
        # decision 重置（联动表扩展）：当前计划回 CHAR_.md 默认循环时间线基线（LLM 按档案补写）·当前行动/未完成意图/行动窗口清空
        if isinstance(cdata.get("decision"), dict):
            for subk in ("当前计划", "当前行动", "未完成意图", "行动窗口"):
                cdata["decision"][subk] = ""
        # 状态字段回基线占位（LLM 按 CHAR_.md 默认循环时间线补写——脚本不解析自然语言）
        cdata["核心状态"] = ""
        cdata["情绪"] = ""
        cdata["人际动态"] = ""
        # 外在物态回基线（联动表）：健康/妆扮/服饰 回基线占位·随身物品 清空；变质=自我连续保留
        if lvl == "变质":
            pass
        else:
            cdata["健康"] = ""
            cdata["妆扮"] = ""
            cdata["服饰"] = []
            cdata["随身物品"] = []
        # 压力/防御回默认；觉醒/变质保留防御崩解状态
        cdata["压力水平"] = "低"
        if lvl in ("觉醒", "变质"):
            cur_def = str(cdata.get("防御有效性", "") or "").strip()
            cdata["防御有效性"] = cur_def if cur_def == "已彻底崩解" else "有效"
        else:
            cdata["防御有效性"] = "有效"
        # 防御形态/崩溃表现：脚本/漂移=清空回档案默认；觉醒/变质=保留（联动表·重构后的新防御随自我连续保留）
        if lvl in ("脚本", "漂移"):
            cdata["防御形态"] = ""
            cdata["崩溃表现"] = ""
        # 偏离登记全档位清空（联动表·机械计数事实·新循环从零累积·validate 3b 计数源重置）
        cdata["偏离登记"] = []
        # 已知地点：脚本=回基线（清空·LLM 按 CHAR_.md 默认循环时间线补常驻）；漂移/觉醒/变质=保留（保守不丢）
        if lvl == "脚本":
            cdata["已知地点"] = []
        # 信念演化/自主性/名字 保留（联动表）
        with open(cfp, "w", encoding="utf-8", newline="") as f:
            yaml.safe_dump(cdata, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"[OK] 重置 {cfp.stem}: 档位={lvl} · 记忆锚点→{len(new_mem) if isinstance(new_mem, list) else 1} 条 · 状态字段回基线")

    # 登记维护名单（{触发/重置日期/轮次}——周期=在册全员循环角色·事件=仅 asset）
    reset_rec = ws.get("维护名单") or {}
    if not isinstance(reset_rec, dict):
        reset_rec = {}
    for cfp in cfps:
        try:
            cdata = yaml.safe_load(cfp.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        # 豁免者（无自主性字段·外部者/管理者）不登记维护名单
        if "自主性" not in cdata or not str(cdata.get("自主性", "") or "").strip():
            continue
        name = cfp.stem[len(CHAR_STATE_PREFIX):-len("_state")]
        # 豁免条目不覆写——保留豁免标记（园区未执行维护·无新事实·validate 8b 跳过）
        _rr0 = ws.get("维护名单") or {}
        if isinstance(_rr0, dict) and name in _rr0 and isinstance(_rr0[name], dict) \
                and str(_rr0[name].get("触发", "")) == "豁免":
            continue
        reset_rec[name] = {"触发": "事件" if asset else "周期", "重置日期": f"第{cur_day}日", "轮次": cur_round}
    ws["维护名单"] = reset_rec

    # 重建周期倒计时（到期时刻 +1 周期·仅周期重置——事件不移动周期重置点）
    if cd_id is not None and asset is None:
        old_due = str(cd_spec.get("到期时刻", "") or "").strip()
        dd, dm = _parse_world_time(old_due)
        if dd is not None:
            nd = dd + 1
            new_due = f"第{nd}日 {old_due.split('日 ')[-1] if '日 ' in old_due else '07:00'}"
            cd_spec["到期时刻"] = new_due
            cd_spec["剩余时间"] = "1周期"
            ws.setdefault("外部倒计时", {})[cd_id] = cd_spec
            print(f"[OK] 周期倒计时 {cd_id} 重建: 到期时刻 {old_due} → {new_due}")
    with open(ws_fp, "w", encoding="utf-8", newline="") as f:
        yaml.safe_dump(ws, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    # 保留候选清单 + 提示
    print("\n【重置完成】" + ("（事件·单角色）" if asset else "（周期·全员）"))
    print(f"  时间 {cur_time} · 轮次 {cur_round} · 维护名单 {len(reset_rec)} 角色")
    print("【LLM 后续动作（非脚本）】")
    print("  1. 状态字段（核心状态/情绪/人际动态/已知地点）按该角色 CHAR_ 默认循环时间线当前时段补写")
    print("  2. 觉醒/漂移档保留候选确认——压缩掉的条目：")
    if candidates:
        for role, lvl, content in candidates[:20]:
            print(f"    · {role}（{lvl}）: {content}")
    else:
        print("    （无压缩条目）")
    print("  3. CT 节拍核查（挂载 CT 是否依赖被抹记忆）· 重置叙事（醒来·新一天帧）")
    return 0


def _ts():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def _focus_region_node(world_dir: Path) -> str | None:
    """当前焦点场景区域节点（scene_card「区域」行 → 'Westworld Park 1/Sweetwater/Main Street'）。
    与 _region_consistency 同源解析；无 regions/ 目录树 / 区域行挂空 → 返回 None。"""
    regions_dir = world_dir / "regions"
    if not regions_dir.is_dir():
        return None
    scene_dir = get_scene_dir(world_dir)
    if scene_dir is None:
        return None
    card_fp = scene_dir / "scene_card.md"
    if not card_fp.exists():
        return None
    m = re.search(r"^\|\s*区域\s*\|\s*([^|]+?)\s*\|", card_fp.read_text(encoding="utf-8", errors="ignore"), re.M)
    if not m:
        return None
    am = re.search(r"regions/(.+?)/REGION\.md$", m.group(1).strip().replace("\\", "/"))
    return am.group(1) if am else None


def _pos_region_node(world_dir: Path, pos_value) -> str | None:
    """把 CHAR_state.位置 值解析为 regions/ 目录树 REGION 节点（后缀匹配·括号注自动剥除）。
    命中返回节点路径（如 'Westworld Park 1/Sweetwater/Main Street'）；目录树缺失/值空/无法命中 → None。"""
    regions_dir = world_dir / "regions"
    if not regions_dir.is_dir():
        return None
    tree_paths = sorted(
        (p.parent.relative_to(regions_dir).as_posix() for p in regions_dir.rglob("REGION.md")),
        key=len, reverse=True,
    )
    if not tree_paths:
        return None
    pos = re.sub(r"[（(][^（）()]*[)）]", "", str(pos_value or "")).strip().replace("\\", "/").strip("/")
    if not pos:
        return None
    hits = [p for p in tree_paths if p == pos or p.endswith("/" + pos)]
    return hits[0] if len(hits) == 1 else (max(hits, key=len) if hits else None)


def _region_record_npcs(world_dir: Path, region_node: str | None) -> set:
    """读某 REGION.md 的「常驻NPC」行 → 角色全名 set（条目格式 `- CHAR_{名}（…）`）。
    region_node 为相对 regions/ 的路径（如 'Westworld Park 1/Sweetwater/Main Street'）；空/目录树缺失 → 空集。
    返回 CHAR_ 指针剥前缀后的角色名（保留括号外全名）。"""
    if not region_node:
        return set()
    fp = world_dir / "regions" / region_node / "REGION.md"
    if not fp.exists():
        return set()
    try:
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return set()
    npcs = set()
    in_npc = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("##"):
            in_npc = bool(re.match(r"^##\s*常驻NPC", s))
            continue
        if not in_npc:
            continue
        if s.startswith("-"):
            m = re.match(r"-\s*(?:CHAR_)?([^（(]+)", s)
            if m:
                nm = m.group(1).strip()
                if nm:
                    npcs.add(nm.replace("_", " "))
    return npcs


def _region_consistency(world_dir: Path) -> str | None:
    """区域一致性检查（场景切换主判据·机械复核）：
    POV 角色位置的 REGION 节点 vs 焦点场景 scene_card「区域」节点——不一致=空间已变但场景切换未执行。
    判据来源：scene_management §移动场景协议 主判据（有 regions/ 目录树时机械接管）。
    返回 FAIL 消息字符串；PASS 或无法判定（无目录树/路径解析不了→迷雾制世界走 LLM 三层规则判断）返回 None。"""
    regions_dir = world_dir / "regions"
    if not regions_dir.is_dir():
        return None
    tree_paths = sorted(
        (p.parent.relative_to(regions_dir).as_posix() for p in regions_dir.rglob("REGION.md")),
        key=len, reverse=True,
    )
    if not tree_paths:
        return None
    # 焦点场景区域节点（scene_card「区域」行）
    scene_node = _focus_region_node(world_dir)
    if scene_node is None:
        return None
    # POV 角色定位：叙事约定 POV=… 优先，CHAR_Guest* 兜底
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws = {}
    states_dir = world_dir / "states"

    def _char_state(name: str):
        fp = states_dir / f"{CHAR_STATE_PREFIX}{name}{CHAR_STATE_SUFFIX}"
        return fp if fp.exists() else None

    pov_fp = None
    mm = re.search(r"POV\s*=\s*([^；;\n]*)", str(ws.get("叙事约定", "") or ""))
    if mm:
        seg = mm.group(1)
        cands = re.findall(r"[（(]([^（）()]+)[)）]", seg) + [t for t in re.split(r"[·,，、\s]+", seg) if t]
        for c in cands:
            pov_fp = _char_state(c.strip())
            if pov_fp:
                break
    if pov_fp is None:
        guests = sorted(states_dir.glob(f"{CHAR_STATE_PREFIX}Guest*{CHAR_STATE_SUFFIX}"))
        pov_fp = guests[0] if guests else None
    if pov_fp is None:
        return None
    try:
        cs = yaml.safe_load(pov_fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    pos = re.sub(r"[（(][^（）()]*[)）]", "", str(cs.get("位置", "") or "")).strip().replace("\\", "/").strip("/")
    if not pos:
        return None
    # 后缀匹配（对齐 validate 4e：位置从角色认知根开始·不含顶层园区前缀）
    hits = [p for p in tree_paths if p == pos or p.endswith("/" + pos)]
    pos_node = hits[0] if len(hits) == 1 else (max(hits, key=len) if hits else None)
    if pos_node is None:
        # fail-closed（2026-10-05）：有 regions/ 目录树时，POV 位置值解析失败=数据非法——
        # 非法值会致盲区域一致性检查（场景切换主判据），必须硬错而非放行（原实现此处 return None=静默通过）。
        pov_name = pov_fp.name[len(CHAR_STATE_PREFIX):-len(CHAR_STATE_SUFFIX)]
        return (
            f"区域一致性 FAIL——POV '{pov_name}' 位置值非法: '{pos}'（剥括号注后不命中 regions/ 目录树任何 REGION 节点）"
            f"——位置值域=目录节点后缀路径（角色认知根开始·如 Sweetwater/Main Street·见 keys.md「位置」）；"
            f"先修位置数据，POV 跨区域时先走场景切换（scene_management §移动场景协议）再继续落盘"
        )
    # 途经节点豁免（REGION 类型=移动·如火车站月台/过境公路）：POV 途经不触发场景切换判据——
    # 途经不建场景（Waypoint 协议）；以该节点为目的地停驻时由场记建正式场景（scene_management §移动场景协议）
    try:
        _region_md = (regions_dir / pos_node / "REGION.md").read_text(encoding="utf-8")
        if re.search(r"^-\s*类型:\s*移动", _region_md, re.MULTILINE):
            return None
    except OSError:
        pass
    if pos_node != scene_node:
        pov_name = pov_fp.name[len(CHAR_STATE_PREFIX):-len(CHAR_STATE_SUFFIX)]
        return (
            f"区域一致性 FAIL——POV '{pov_name}' 所在区域节点 '{pos_node}' ≠ 焦点场景 {get_scene_dir(world_dir).name} "
            f"区域节点 '{scene_node}'（空间已变·场景切换未执行——按 scene_management §移动场景协议 主判据先执行场景切换流程再继续落盘）"
        )
    return None


def cmd_ledger(world_dir: Path, extra: list[str] | None = None):
    """批次原文账本查询（只读·取证面）——`ledger [轮次]`；缺轮次则列出并输出全部账本。

    账本由 write_round_ledger 在段批次落盘成功后自动写入（scenes/{段所属场景}/.ledger_r{N}.{阶段}.{ts}.yaml），
    内容=④段 MUSE/ACTION/SCHEDULE/META 原文 + 各段 阶段/META/op 索引。
    跨场景轮 ④段跑在焦点切换之前、账本落旧场景 → 本命令焦点场景优先、未命中回退扫全部场景。
    本命令是唯一读入口（账本不进 discover_files/read/加载面）。"""
    scenes_root = world_dir / "scenes"
    scene_dir = get_scene_dir(world_dir)
    search_dirs: list[Path] = []
    if scene_dir is not None and scene_dir.is_dir():
        search_dirs.append(scene_dir)
    if scenes_root.is_dir():
        for _sd in sorted(scenes_root.iterdir()):
            if _sd.is_dir() and _sd not in search_dirs:
                search_dirs.append(_sd)
    if not search_dirs:
        print("[ERR] 无场景目录——无账本可读（账本落点=scenes/{场景}/）", file=sys.stderr)
        sys.exit(1)

    def _all_ledgers() -> list:
        out = []
        for _sd in search_dirs:
            out.extend(_sd.glob(".ledger_r*.yaml"))
        return sorted(out)

    want = str(extra[0]).strip() if extra else ""
    if want:
        want = want[1:] if want[:1] in ("r", "R") else want
        pat = re.compile(rf"\.ledger_r{re.escape(want)}\..*\.yaml")
        targets = [p for p in _all_ledgers() if pat.fullmatch(p.name)]
        if not targets:
            have = sorted({re.match(r"\.ledger_r(.+?)\.", p.name).group(1)
                           for p in _all_ledgers() if re.match(r"\.ledger_r(.+?)\.", p.name)})
            print(f"[ERR] 账本不存在: 轮次 {want}——已落轮次: {'、'.join(have) if have else '（无）'}", file=sys.stderr)
            sys.exit(1)
    else:
        targets = _all_ledgers()
    if not targets:
        print("[INFO] 无账本——段批次落盘成功时自动写入")
        return
    _labels = sorted({p.parent.name for p in targets})
    print(f"[LEDGER] {'、'.join(_labels)}·{len(targets)} 份")
    for fp in targets:
        print(f"\n===== {fp.parent.name}/{fp.name} =====")
        try:
            print(fp.read_text(encoding="utf-8").rstrip("\n"))
        except Exception as e:
            print(f"[WARN] 读取失败: {e}", file=sys.stderr)


def cmd_cast_baseline(world_dir: Path):
    """场景 cast 基线查询（只读·exit 0 恒过）——输出当前焦点场景的基线名单与 scene_card 两栏覆盖情况。

    口径与 gate keeper cast 覆盖检查同源（_scene_cast_baseline / _cast_overlap_missing）：
    调度单四层点名角色无条件入基线；常驻NPC/关联角色按当前时刻时间线命中本场者入基线
    （子区域位置命中计入本场）。scene_management §6：init_scene 焦点切换后、写 scene_card 前运行，
    基线名单照填「出场角色」/「焦外/在场」两栏。"""
    baseline = _scene_cast_baseline(world_dir)
    missing = _cast_overlap_missing(world_dir, baseline)
    scene_dir = get_scene_dir(world_dir)
    print(f"[CAST-BASELINE] 焦点场景: {scene_dir.name if scene_dir else '（无焦点场景）'}")
    print(f"  基线名单({len(baseline)}): {'、'.join(sorted(baseline)) if baseline else '（空）'}")
    if missing:
        print(f"  缺失(须补入「出场角色」或「焦外/在场」两栏之一·具名·虚词不算覆盖): {'、'.join(missing)}")
    else:
        print("  cast 覆盖完整 ✅")
    return 0


def _scene_open_round(scene_dir) -> str:
    """读 start_snapshot.md 的「开场轮次」（入场帧冻结轮次）——缺失返回空串。
    round-check 用它判定入场帧豁免：场景创建当轮（开场轮次==世界轮次）时间线为空属合法状态。"""
    try:
        txt = (scene_dir / "start_snapshot.md").read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    m = re.search(r"开场轮次[:：]\s*(\d+)", txt)
    return m.group(1) if m else ""


def cmd_round_check(world_dir: Path):
    """轮完整性检查（⑤场记收尾调用·每轮）——六阶段分批写入后的状态一致性对账：
    ① direction 已写（或无事件线世界声明豁免）② world_state 三件套（时间/轮次/前情）
    ③ 焦点场景 场景时间线非空 ④ direction↔storylines↔CT.事件线引用 对账
    ⑥ 跳阶段硬检（轮次≥1：②建线/③落拍/①CT 结算痕迹——机械兜底，见 F3 设计）。
    输出逐项 PASS/FAIL；任一 FAIL exit 1（场记本阶段修复或上报）。"""
    fails = []
    st = _load_storylines(world_dir)
    sl_map = st.get(STORYLINE_TOP_KEY) or {}
    dr = _load_direction(world_dir)
    # ① direction
    if sl_map:
        if not dr:
            fails.append("direction.yaml 缺失——storylines 有事件线但导演状态文件不存在（③导演未写）")
        else:
            cur_sl = str(dr.get("当前事件线", "") or "").strip()
            if not cur_sl:
                fails.append("direction.当前事件线 为空——③导演本轮未写指针")
            elif cur_sl not in sl_map:
                fails.append(f"direction.当前事件线 '{cur_sl}' 不在 storylines 中")
            if dr and not str(dr.get("承接判断", "") or "").strip():
                fails.append("direction.承接判断 为空——③导演回判留痕缺失（核心三件之一）")
    else:
        print("[ROUND] storylines 无事件线——①direction 结构对账豁免；空表本身由⑥跳阶段硬检 FAIL", file=sys.stderr)
    # ② world_state 三件套
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws = {}
    for k, label in (("轮次", "轮次"), ("前情描述", "时间.前情描述")):
        if not str(ws.get(k, "") if k == "轮次" else (ws.get("时间", {}) or {}).get("前情描述", "") or "").strip():
            fails.append(f"world_state.{label} 缺失——⑤场记收尾未写")
    if not str((ws.get("时间", {}) or {}).get("具体时间", "") or "").strip():
        fails.append("world_state.时间.具体时间 缺失——⑤场记收尾未写")
    # ③ 焦点场景时间线
    scene_dir = get_scene_dir(world_dir)
    if scene_dir is None:
        fails.append("无法定位焦点场景目录——world_state.焦点场景 缺失或目录不存在")
    else:
        sfp = scene_dir / "scene_state.yaml"
        if not sfp.exists():
            fails.append(f"{scene_dir.name}/scene_state.yaml 不存在")
        else:
            try:
                sd = yaml.safe_load(sfp.read_text(encoding="utf-8")) or {}
                tl = str(sd.get("场景时间线", "") or "").strip()
                if not tl:
                    # 入场帧豁免：开场轮次==当前世界轮次=场景创建当轮——无剧情事件可记
                    # （scene_management §跨场景轮落盘顺序：入场帧元素不含场景时间线·时间线自首个剧情轮起记）
                    _open_r = _scene_open_round(scene_dir)
                    _cur_r = str(ws.get("轮次", "") or "").strip()
                    if _open_r and _cur_r and _open_r == _cur_r:
                        print(f"[ROUND] {scene_dir.name}/scene_state.场景时间线 为空——开场轮次({_open_r})==当前轮次·入场帧豁免", file=sys.stderr)
                    else:
                        fails.append(f"{scene_dir.name}/scene_state.场景时间线 为空——⑤场记未追加本轮事件")
            except Exception:
                fails.append(f"{scene_dir.name}/scene_state.yaml 解析失败")
    # ④ CT 引用对账
    try:
        cd = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        cd = {}
    for k, cv in cd.items():
        if re.match(r"^CT-\d{2}$", str(k)) and isinstance(cv, dict):
            refs = cv.get("事件线引用")
            bad = [str(r) for r in (refs if isinstance(refs, list) else ([refs] if isinstance(refs, str) and refs.strip() else [])) if str(r) not in sl_map]
            if bad:
                fails.append(f"conflicts.{k}.事件线引用 悬空: {bad}")
    # ⑥ 跳阶段硬检（叙事推进轮·轮次≥1）：①②③ 缺席时在此机械兜底——gate 是事前闸门，round-check 是收尾对账
    try:
        round_no = int(str(ws.get("轮次", "") or 0))
    except (TypeError, ValueError):
        round_no = 0
    if round_no >= 1:
        if not sl_map:
            fails.append("storylines.事件线 为空——②编剧未建线（阶段完整性硬性：推进轮任何阶段不得缺席·工作流见 SKILL.md 每轮流程）")
        else:
            cur_beat = str(dr.get("当前拍", "") or "").strip() if dr else ""
            if not cur_beat:
                fails.append("direction.当前拍 为空——③导演未落拍（###BEAT set/deepen 必写·指针缺失=演出无锚）")
        settled = any(
            str(cv.get("施压方向", "") or "").strip() or cv.get("上轮结算")
            for k, cv in cd.items()
            if re.match(r"^CT-\d{2}$", str(k)) and isinstance(cv, dict)
        )
        if not settled:
            msg = "conflicts 无任何结算痕迹（全部 CT 的 施压方向/上轮结算 均空）——①戏剧家未推进任何 CT"
            if round_no >= 3:
                fails.append(f"{msg}（首轮宽限已过·轮次={round_no}）")
            else:
                print(f"[ROUND] 软性告警: {msg}（首轮宽限内·轮次≥3 转 FAIL）", file=sys.stderr)
    # ⑤ 区域一致性（场景切换主判据·机械复核）
    rc_fail = _region_consistency(world_dir)
    if rc_fail:
        fails.append(rc_fail)
    # ⑤b 转场执行核验（③导演已写转场决策 → ⑤场记必须落地·round-check 封口）：
    #     direction.转场.目标场景 非空 但 world_state.焦点场景 未更新到该目标 = 转场决策已写而未执行。
    #     审计 R2/K1/K2 现象：可能被⑥作家手动建场景目录绕过。焦点场景=scene_management 唯一权威源，
    #     执行转场必须更新它（init_scene + 更新 world_state.焦点场景）。
    _trans = _map_field(dr.get("转场"))
    _target = (_trans.get("目标场景") or None)
    _tgt_str = str(_target).strip() if _target else ""
    # 「无」/空 = 已清除语义（keys.md 转场行）——escalation_flags 的写「无」惯例迁移到转场不再误报
    if _tgt_str and _tgt_str != "无":
        _tgt_id = re.search(r"S\d{2,}", _tgt_str)
        _cur_focus = str(ws.get("焦点场景", "") or "").strip()
        if _tgt_id:
            _expect = _tgt_id.group(0)
            if not _cur_focus.upper().startswith(_expect.upper()):
                fails.append(
                    f"转场决策 目标={_tgt_str} 已写（direction.转场.目标场景）但世界焦点场景仍为 '{_cur_focus}'——⑤场记转场未执行"
                    f"（须 init_scene 建新场景 + 更新 world_state.焦点场景；禁止由⑥作家手动建目录绕过）"
                )
        else:
            if _cur_focus.upper() not in _tgt_str.upper():
                fails.append(
                    f"转场决策 目标={_tgt_str}（direction.转场.目标场景）与当前焦点场景 '{_cur_focus}' 不一致——⑤场记转场未执行"
                )
    if fails:
        print(f"[ROUND] 轮完整性检查 FAIL（{len(fails)} 项）:", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)
    print("[ROUND] 轮完整性检查通过 ✅（direction/世界三件套/场景时间线/引用对账）")


def cmd_precheck(world_dir: Path):
    """本轮调度信号导出器（只读·不拦截·exit 0 恒过）——把 gate/round-check 必然强制的**机械义务**前置暴露，
    让 LLM 第一射即满足（act 前告知·而非 gate 失败后修·避免最贵的重提）。
    判据全部从现有状态可导出·只读不写。
    v0.28：结构基线缺失（最高优先级·必须先行初始化）+ escalation_flags.CT待结算（①必含 CT op）+ 时间窗口已耗导出。
    覆盖范围（诚实边界）：仅状态可导出的机械义务；用户指令加压/重大事件/回判张力等**推断类触发**需 LLM
    自行判定（输出末尾明示·防 LLM 把本预检当全量触发器）。
    与 --dry-run（批内解析+audit+差价）/ gate --check（单段复验）分工：本命令=跨阶段状态义务预曝光。"""
    dr = _load_direction(world_dir)
    st = _load_storylines(world_dir)
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws = {}
    try:
        cd = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        cd = {}

    flags = dr.get("escalation_flags") or {}
    sl_map = st.get(STORYLINE_TOP_KEY) or {}
    cur_sl = str(dr.get("当前事件线", "") or "").strip()
    cur_beat = str(dr.get("当前拍", "") or "").strip()

    findings = []  # (标记, 触发, 必含项/参考提示, 违反后果)
    structural = False  # 本轮是否存在结构层义务（有任一→末尾不出合批提示）
    _init_round = False  # 结构基线缺失=需先行初始化（供合批提示与义务区判定）
    # ── v0.28 结构基线（最高优先级·机械判定·不可豁免）──
    # 齐备 = conflicts 有≥1 活跃 CT ∧ storylines 有≥1 活跃线 ∧ direction.当前拍 非空
    _active_ct = [k for k, v in cd.items() if isinstance(v, dict) and str(k).startswith("CT-")] if isinstance(cd, dict) else []
    _active_sl = [k for k, v in sl_map.items()
                  if isinstance(v, dict) and str(v.get("状态", "") or "").strip() == "活跃"] if isinstance(sl_map, dict) else []
    if not _active_ct or not _active_sl or not cur_beat:
        structural = True
        _init_round = True
        _what = []
        if not _active_ct:
            _what.append("conflicts 无活跃 CT")
        if not _active_sl:
            _what.append("storylines 无活跃线")
        if not cur_beat:
            _what.append("direction.当前拍 空")
        findings.append(("●", f"结构基线缺失（{(' ∨ ').join(_what)}）——必须先行初始化·不可豁免",
                         "①戏剧家本批必注册/推进 CT（兜底四源）→ ②编剧必建线（取材=①产出）→ ③导演必 set 指针+guidance+调度单+窗口{起点,预算}",
                         "世界无法启动（gate 结构层硬拦）"))
    # ── 停滞旗标（有→①戏剧家必须加压兑现）──
    _f_stall = isinstance(flags, dict) and any("停滞" in str(k) and _flag_active(v) for k, v in flags.items())
    if _f_stall:
        structural = True
        findings.append(("●", "escalation_flags.停滞 在场（上轮僵持）",
                         f"①戏剧家本批必须写 CT-XX.{PRESSURE_KEY} ≥1 条 ≠ 维持（四爆破方向四选一·停滞旗标当轮消化）",
                         "gate dramatist 拦"))
    # ── 不承接旗标（有→②编剧必须三问定原线去向）──
    _f_untaken = isinstance(flags, dict) and any("不承接" in str(k) and _flag_active(v) for k, v in flags.items())
    if _f_untaken:
        structural = True
        findings.append(("●", "escalation_flags.不承接 在场（上轮原计划失效）",
                         "②编剧本批必须三问定该线去向（前置/问题/承诺 → 保留挂起+add 新线 / rewrite / clear）",
                         "gate storyliner 拦"))
    # ── v0.28 CT待结算旗标（有→①戏剧家必须结算/重估 CT）──
    _f_ctsettle = isinstance(flags, dict) and any("CT待结算" in str(k) and _flag_active(v) for k, v in flags.items())
    if _f_ctsettle:
        structural = True
        findings.append(("●", "escalation_flags.CT待结算 在场（上轮演出触及 CT——资源/控制权/关系/退路）",
                         "①戏剧家本批必须含 conflicts CT op（结算/重估·推进池重估紧迫度）",
                         "gate dramatist 拦（旗标在场但①批无 CT op=拦）"))
    # ── 偏离提示旗标（③导演职责7 判出「持续偏离」→ 唤醒①按偏离者四件套处理）──
    _f_deviat = isinstance(flags, dict) and any("偏离提示" in str(k) and _flag_active(v) for k, v in flags.items())
    if _f_deviat:
        structural = True
        findings.append(("●", "escalation_flags.偏离提示 在场（③导演判出循环轨道持续偏离）",
                         "①戏剧家本批按偏离者四件套处理（冲突化/埋后果=①·状态结算=④·回归判定=③）",
                         "gate dramatist 拦"))
    # ── v0.29 时间窗口状态导出（拍级·脚本机械判定·③④共用口径·含跨日修正）──
    #    上轮落盘 节拍决策=继续当前拍 → trigger 附标记（该状态事实的唯一承载位）
    _same_beat_prev = str(dr.get("节拍决策", "") or "").strip().startswith("继续当前拍")
    _bm, _elapsed, _remain, _exhausted = _window_status(world_dir)
    if _bm is None:
        findings.append(("◎", "时间窗口 未设定或预算未解析——③应设 窗口{起点,预算}（格式：N分钟）",
                         "—（无窗口则④无节流依据·precheck 提示）",
                         "—（参考信息·非硬性）"))
    else:
        _info = f"时间窗口（拍级）预算={_bm}分钟"
        if _elapsed is not None:
            if _remain < 0:
                _info += f" 已耗≈{_elapsed}分钟 超预算≈{-_remain}分钟"
            else:
                _info += f" 已耗≈{_elapsed}分钟 剩余≈{_remain}分钟"
        if _same_beat_prev:
            _info += "（上轮 节拍决策=继续当前拍）"
        if _exhausted is True:
            structural = True
            findings.append(("●", _info + " · 窗口已耗尽",
                             "③按回判表验收判定：已答→advance / 未答且意图仍在推进本拍问题→续演（批内重设窗口·起点=当前世界时间·新拍级预算） / 未答且意图已不再推进→escalation_flags.停滞",
                             "gate director 连续同拍核验（上轮=继续当前拍 时·窗口已耗尽必须明确表态）"))
        elif _exhausted is False:
            findings.append(("◎", _info + " · 窗口未耗尽",
                             "③导演本批默认续演当前拍（###BEAT: deepen SL-XX）·问题提前回答可 advance·验收点=窗口耗尽·写 deepen 须在 direction.承接判断 点名调度单各角色的「未完成意图」及待改变状态",
                             "—（参考信息·非硬性）"))
        else:
            findings.append(("◎", _info + " · 剩余不可判定（缺起点或时间格式未解析）",
                             "③补设 窗口{起点,预算}（起点=当前世界时间·预算=N分钟）·本轮按未耗尽处理",
                             "—（参考信息·非硬性）"))
    # ── 空表→建线（事件线空但指针非空=悬空·必须补建）──
    _empty_table = bool(not sl_map and cur_sl)
    if _empty_table:
        structural = True
        findings.append(("○", "storylines.事件线 空 且 direction.当前事件线 非空",
                         "②编剧本批必须 ###STORYLINE: add（建线后③导演 ###BEAT: set 落起点指针）",
                         "gate storyliner / round-check 拦"))
    # ── 未引用 CT 且无活跃线可接（②必含 add·判据与 gate storyliner 同源）──
    #    基线缺失轮已由上方结构基线项覆盖（②必建线）·此处只报结构基线齐备下的残留情形
    _must_add, _unref_ct, _ = _storyliner_unref_and_must_add(sl_map, dr, cd)
    _must_add_new = _must_add and not _init_round
    if _must_add_new:
        structural = True
        findings.append(("●", f"未引用活跃线 CT 且无活跃线可接（{'/'.join(_unref_ct)}）",
                         "②编剧本批必须 ###STORYLINE: add（D4 合并触发·取材=与焦点场景关联的未引用 CT·细则见 phase_storyliner D5 取材）",
                         "gate storyliner 拦"))
    # ── 顶点拍（当前拍=顶点·③导演出线核验 + ⑥作家顶点轮）──
    if cur_sl and cur_beat == "顶点":
        structural = True
        cons = None
        _line = sl_map.get(cur_sl)
        if isinstance(_line, dict):
            for _b in (_line.get("拍序") or []):
                if isinstance(_b, dict) and str(_b.get("拍名", "") or "").strip() == "顶点":
                    cons = _b.get(CLIMAX_CONSTRAINT_KEY)
                    break
        req = "③导演按顶点出线核验（advance 余波须带 爆破结算+张力结算 双表态）；①戏剧家核对/登记爆破源载体（职责2「顶点爆破源登记」·每轮必查）；⑥作家本轮=顶点轮（篇幅按 phase_writer「长度与风格」自定）"
        if isinstance(cons, dict):
            findings.append(("●", f"当前拍=顶点（{cur_sl}）·顶点约束齐备", req, "gate director 出线核验"))
        else:
            findings.append(("▲", f"当前拍=顶点（{cur_sl}）·但 顶点约束 缺失或非映射（拍序未填）", req, "gate director 出线核验（缺约束即拦）"))
    # ── 转场决策挂钩（③导演已写转场决策 → ⑤场记本批必须执行场景切换）──
    #    R5/scene_management §场景切换流程：「转场决策→⑤执行」；若 direction.转场.目标场景 已非空而未执行，
    #    则可能被⑥作家手动建目录绕过（审计 R2/K1/K2 现象）。precheck 只读提示·不拦截——转场执行由⑤场记该批落地。
    _trans = _map_field(dr.get("转场"))
    _target = _trans.get("目标场景") or None
    _tgt_str = str(_target).strip() if _target else ""
    # 「无」/空 = 已清除语义；目标==当前焦点 = 已执行（init_scene 正常路径会自动清·旁路残留降级为参考提示）
    if _tgt_str and _tgt_str != "无":
        _tgt_id = re.search(r"S\d{2,}", _tgt_str)
        _cur_focus = str(ws.get("焦点场景", "") or "").strip()
        _executed = (_cur_focus.upper().startswith(_tgt_id.group(0).upper()) if _tgt_id
                     else bool(_cur_focus) and _cur_focus.upper() in _tgt_str.upper())
        if _executed:
            findings.append(("○", f"转场已执行（目标={_tgt_str}＝当前焦点 {_cur_focus}）·direction.转场 残留",
                             "建议③导演回判批清除（整键写 {}）",
                             "参考提示·非义务"))
        else:
            structural = True
            findings.append(("●", f"③导演已写转场决策：目标={_tgt_str}（direction.转场.目标场景）",
                             "⑤场记本批先走场景切换流程（冻结+时间线压缩+init_scene+world_state.焦点场景 更新）——禁止在⑥作家手动建场景目录绕过",
                             "round-check / gate keeper 落点拦"))
    # ── ④角色义务（循环世界·本轮状态已可导出·无推断）──
    _char_states = _load_char_states(world_dir)
    _loop_names = [n for n, d in _char_states if str(d.get("自主性", "") or "").strip() in AUTO_ORDER]
    if _loop_names:
        _sched_roles = _schedule_cast_roles(world_dir)
        # 仅本轮相关调度角色才需硬性覆盖（与 gate actor 同源）；其余在轨循环角色走轻量推演，按需不强制
        _relevant = [n for n in _loop_names if n in _sched_roles]
        if _relevant:
            findings.append(("●", f"循环世界（本轮相关调度）：{'/'.join(_relevant)}",
                             "④角色本批：③调度单点名角色必须进『角色覆盖』声明（『无变化』通道已废止）；在轨循环角色走轻量推演——计划层不重新合成（当前计划＝CHAR_.md 默认循环时间线物化的基线·维护归 actor_decision.md D3 长期计划巡检）",
                             "gate actor 拦（角色覆盖对账）/ 计划联动告警"))
        else:
            findings.append(("○", f"循环世界（在轨{_loop_names.__len__()}名·本轮无循环角色调度）",
                             "④角色走轻量推演·本轮无调度则不强制覆盖（有调度/升档关联时恢复 ●）",
                             "—"))
    # ── 场景基线 cast 覆盖（⑤场记义务·本场景应出现角色须入 scene_card cast）──
    #   判据与 gate keeper 同源：_scene_cast_baseline（POV∪本场常驻NPC∪conflicts关联∪调度单）。
    #   常驻NPC 只取按当前时刻时间线命中本场者（NPC 会动·时间线命中别处不硬套），无时间线者按注册地保守纳入。
    #   本阶段=机械义务清单（只报「缺不缺」·不替导演/场记决定排哪层——去向由各自层内正向规则定）。
    _bl_roles = _scene_cast_baseline(world_dir)
    _scene_missing = _cast_overlap_missing(world_dir, _bl_roles)
    if _scene_missing:
        findings.append(("●", f"进入/处于场景基线：本场景应出现角色未入 cast（缺: {'/'.join(sorted(_scene_missing))}）",
                         "⑤场记本批按 cast 派生源物化 scene_card cast——常驻NPC 入『出场角色』(焦内) 或『焦外/在场』(焦外)·时间线命中别处的角色不入 cast（按 REGION 静态归属保守纳入者需复核当前时刻）",
                         "gate keeper 转场后硬拦"))
    # ── 变质判定门槛已满足（④角色本批应升档·与 A0 硬检同门槛）──
    _promotable = [n for n, d in _char_states
                   if str(d.get("压力水平", "") or "").strip() == AUTO_PROMOTE_PRESSURE
                   and str(d.get("防御有效性", "") or "").strip() == AUTO_PROMOTE_DEFENSE
                   and str(d.get("自主性", "") or "").strip() not in ("", "变质")]
    if _promotable:
        findings.append(("●", f"变质判定门槛已满足：{'/'.join(_promotable)}（压力={AUTO_PROMOTE_PRESSURE} 且 防御={AUTO_PROMOTE_DEFENSE}）",
                         "④角色本批执行升档+信念演化留痕。写入顺序（硬性）：压力/防御 → 自主性 → 信念演化 → 压力回落",
                         "未升档=validate 软告警；未达门槛却升档=A0 脚本硬拦"))
    # ── 周期重置到期（⑤场记写 时间.具体时间 会被 ④b 顶回·判据与 ④b 同源）──
    _tt = ws.get("时间") or {}
    _cday, _cmin = _parse_world_time(str(_tt.get("具体时间", "") or "")) if isinstance(_tt, dict) else (None, None)
    _due = _cycle_reset_due(ws, _cday, _cmin)
    if _due:
        findings.append(("▲", f"周期重置到期时刻 {_due[0]} 已被当前时间越过·维护名单无覆盖 {_due[1]}",
                         f"先执行 `worldctl.py {world_dir.name} reset-cycle`（全员机械重置+登记+重建倒计时）再写 world_state.时间.具体时间",
                         "④b 重置点机械拦截（硬性顶回）"))
    # ── 区域一致性（切场景主判据·机械复核）──
    rc_fail = _region_consistency(world_dir)
    if rc_fail:
        structural = True
        findings.append(("●", "POV 区域 ≠ 焦点场景区域（空间已变·场景切换未执行）",
                         "⑤场记本批先走场景切换流程（冻结+时间线压缩+init_scene+world_state.焦点场景 更新）",
                         "round-check FAIL"))
    else:
        tt = ws.get("时间") or {}

        def _date(s: str):
            m = re.search(r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日", s or "")
            return m.group(0) if m else None

        _base, _spec = _date(str(tt.get("基准时间", "") or "")), _date(str(tt.get("具体时间", "") or ""))
        if _base and _spec and _base != _spec:
            structural = True
            findings.append(("▲", f"时间曾跨天（基准 {_base} ≠ 具体 {_spec}）",
                             "⑤场记先走场景切换流程（跨天必切·无豁免——场景=地点×时间区间）",
                             "scene_management 硬性"))

    # ── 唤醒判定（机械信号·Step1 编排任务单直接取用·语义触发见末尾覆盖边界）──
    _d_src = []
    if _init_round:
        _d_src.append("基线缺失")
    if cur_sl and cur_beat == "顶点":
        _d_src.append("顶点拍")
    if _f_stall:
        _d_src.append("停滞旗标")
    if _f_ctsettle:
        _d_src.append("CT待结算旗标")
    if _f_deviat:
        _d_src.append("偏离提示旗标")
    _s_src = []
    if _init_round:
        _s_src.append("基线缺失")
    if _f_untaken:
        _s_src.append("不承接旗标")
    if _empty_table:
        _s_src.append("空表+指针非空")
    if _must_add_new:
        _s_src.append("未引用CT+无活跃线可接")
    if cur_beat == "余波":
        _s_src.append("余波拍（advance 已落·收束/承接判定归②）")
    # ── 空间脱钩检测（v0.30·机械信号→②编剧唤醒）：当前拍拍序空间与焦点场景区域标记不可匹配 → ②三问归位 ──
    #    判据=局面级：本拍预设局面所在的物理空间已不在当前焦点场景（r56 型失效——场景离开拍空间而③未判行2·预设与现实脱钩）。
    #    标记面=焦点 REGION 标题两侧段＋scene_card 场景名（不含子区域——子区域名会吞掉「Mariposa 前厅散客桌」这类相邻场所文本）。
    #    归一化包含匹配（双向）；不可匹配 → 唤醒②三问归位后信号自清（自愈型·非拦截型·误唤成本=②一次确认）。
    _beat_space = ""
    if cur_sl and cur_beat and isinstance(sl_map, dict):
        _sl_entry = sl_map.get(cur_sl)
        if isinstance(_sl_entry, dict) and isinstance(_sl_entry.get("拍序"), list):
            for _b in _sl_entry["拍序"]:
                if isinstance(_b, dict) and str(_b.get("拍名", "") or "").strip() == cur_beat:
                    _beat_space = str(_b.get("空间", "") or "").strip()
                    break
    if _beat_space:
        _mk: list[str] = []
        _focus_node = _focus_region_node(world_dir)
        if _focus_node:
            _fp = world_dir / "regions" / _focus_node / "REGION.md"
            if _fp.exists():
                for ln in _fp.read_text(encoding="utf-8", errors="ignore").splitlines():
                    s = ln.strip()
                    if s.startswith("# ") and "/" in s:
                        for _part in s.lstrip("#").split("/"):
                            if _part.strip():
                                _mk.append(_part.strip())
        _sc_dir = get_scene_dir(world_dir)
        if _sc_dir is not None and (_sc_dir / "scene_card.md").exists():
            _m_card = re.search(r"^\|\s*场景名\s*\|\s*([^|]+?)\s*\|",
                                (_sc_dir / "scene_card.md").read_text(encoding="utf-8", errors="ignore"), re.M)
            if _m_card:
                for _part in re.split(r"[·,，、]", _m_card.group(1).strip()):
                    if _part.strip():
                        _mk.append(_part.strip())
        if _mk:
            _ns_beat = re.sub(r"\s+", "", _beat_space)
            _matched = any(
                (re.sub(r"\s+", "", m) in _ns_beat) or (bool(_ns_beat) and _ns_beat in re.sub(r"\s+", "", m))
                for m in _mk if m
            )
            if not _matched:
                _s_src.append("空间脱钩")
                structural = True
                findings.append(("●", f"当前拍空间脱钩——拍序空间「{_beat_space}」与焦点场景区域标记（{'/'.join(_mk[:3])}…）不可匹配",
                                 "②编剧本批必须三问定归属（该拍/该线：挂起·改写拍序空间·或开新线承接实际演出——归位后信号自清）——三选一前先判本拍材料是否已兑现：已兑现→走挂起/开新线，不得只改写拍序空间（对齐空间会掩盖空拍）",
                                 "信号每轮重复在场直至②归位（拍序空间与焦点场景重新可匹配·或当前拍切至可匹配拍）"))
    _d_txt = ("唤醒（" + "/".join(_d_src) + "）") if _d_src else "未唤醒"
    _s_txt = ("唤醒（" + "/".join(_s_src) + "）") if _s_src else "未唤醒"
    print("[PRECHECK] 唤醒判定（机械信号·语义触发见末尾覆盖边界）: "
          f"①戏剧家 {_d_txt} | ②编剧 {_s_txt} | ③导演 恒跑 | ④角色 恒跑 | ⑤场记 恒跑 | ⑥作家 恒跑")

    if not findings:
        print("[PRECHECK] 本轮无状态可导出的机械义务（正常推进：各阶段走轻路径/常规路径）")
    else:
        print("[PRECHECK] 本轮义务预检（只读·不拦截·exit 0 恒过）——状态可导出的机械义务：")
        for mark, trig, req, when in findings:
            _label = "参考提示" if str(when).strip().startswith("—") else "本批必含"
            print(f"[PRECHECK] {mark} {trig}\n          ↳ {_label}: {req}\n          ↳ 否则: {when}")
        print("[PRECHECK] 标记: ● 必做义务·◎ 参考信息·▲ 数据/前置异常（先修再进）·○ 补建义务（硬软以每条的「本批必含 / 参考提示」为准）")

    if not structural:
        print("[PRECHECK] 结构层无机械义务·可合批（SKILL.md 结构层合批条款·①上轮结算/压力扫描照常）")

    # ── SNAPSHOT 数据区（参考数据·非义务——义务区已在前面·本区只供各阶段取数·不构成行为指令）──
    loop_names = [n for n, _d in _load_char_states(world_dir) if str(_d.get("自主性", "") or "").strip() in AUTO_ORDER]
    if loop_names:
        timelines = _parse_char_timeline(world_dir)
        cur_min, _t = _parse_world_current_min(world_dir)
        _bm, *_ = _window_status(world_dir)
        _wmin = _bm if _bm is not None else 30
        # §1a 临近互锁事件（更重要·前置：③调度单「即将触发事件」预判·LOOPS 跨角色互锁时刻表·与窗口重叠）
        interlocks = _loops_interlocks(world_dir)
        near = _loops_interlocks_near(interlocks, cur_min, _wmin)
        print(f"\n[PRECHECK] SNAPSHOT §1a 临近互锁事件（窗口 {_wmin} 分钟·参考数据·非义务——③调度单「即将触发事件」预判）:")
        if not near:
            print("  （窗口内无互锁事件）")
        for s0, e0, ev, roles in near:
            print(f"  {s0 // 60:02d}:{s0 % 60:02d}-{e0 // 60:02d}:{e0 % 60:02d} | {ev} | {'/'.join(roles)}")
        # §1b 循环轨道对照（偏离基线·范围=调度单点名循环角色 ∪ 当前焦点区 REGION 常驻NPC ∪ §1a 互锁涉及角色）
        relevant = sorted(_loop_relevant_roles(world_dir))
        print("\n[PRECHECK] SNAPSHOT §1b 循环轨道对照（参考数据·非义务——偏离基线核对·范围=调度单点名循环角色 ∪ 当前焦点区常驻NPC ∪ §1a互锁涉及角色）:")
        # 维护名单状态标（loop_machinery §2.3）：豁免=园区已撤销管辖 → 无生效基线 → 不构成偏离。
        #   就地标注=省去「为判偏离而打开 loop_machinery.md」的前置加载——Step1 只读本快照即可裁定。
        print("  （判读：维护名单「豁免」= 园区已撤销对其管辖 → 无生效基线 → 不构成行动级偏离·免偏离代价·免「Host vs 法则」CT 注册（loop_machinery §2.3）；「周期/事件」= 在册·预设 vs 实际 的差异才构成偏离）")
        _maint = ws.get("维护名单") or {}
        _maint_by_key = {}
        if isinstance(_maint, dict):
            for _mk, _mv in _maint.items():
                _maint_by_key[_norm_char_key(_mk)] = _mv

        def _maint_label(nm: str) -> str:
            spec = _maint.get(nm) if isinstance(_maint, dict) else None
            if spec is None:
                spec = _maint_by_key.get(_norm_char_key(nm))
            trig = str(spec.get("触发", "") or "").strip() if isinstance(spec, dict) else ""
            if trig == "豁免":
                return "｜维护名单: 豁免（无生效基线·不构成偏离）"
            return f"｜维护名单: {trig}" if trig else "｜维护名单: 未登记"

        for name in relevant:
            rows = timelines.get(name) or []
            loc, ac, inwin = _char_timeline_preset(rows, cur_min)
            actual = ""
            for _cn, cd in _load_char_states(world_dir):
                if _norm_char_key(_cn) == _norm_char_key(name):
                    actual = str(cd.get("位置", "") or "").strip()
                    break
            mark = ""
            if inwin:
                mark = ""
            else:
                mark = "（时段外）" if rows else "（无时间线）"
            print(f"  {name} | 预设: {loc or '(未解析)'}·{ac or ''} | 实际: {actual or '(缺)'} {mark}{_maint_label(name)}")

    # §2 元素注册清单（全场景物理锚点/道具/关键场景信息——非焦点场景索引·替代⑥每轮多次 grep）
    print("\n[PRECHECK] SNAPSHOT §2 元素注册索引（参考数据·非义务——scene_state 元素名·焦点场景照常走数据就绪全貌·跨场景原文深查仍 grep）:")
    _focus_scene = str(ws.get("焦点场景", "") or "").strip()
    _idx_lines = []
    try:
        _scenes_dir = world_dir / "scenes"
        for _sd in sorted(_scenes_dir.iterdir()) if _scenes_dir.is_dir() else []:
            if not _sd.is_dir():
                continue
            _ssp = _sd / "scene_state.yaml"
            if not _ssp.exists():
                continue
            try:
                _ss = yaml.safe_load(_ssp.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            if not isinstance(_ss, dict):
                continue
            _nm = _sd.name
            _flags = []
            if _nm.startswith(_focus_scene):
                _flags.append("焦点")
            _anchors = _ss.get("物理锚点") or []
            _props = _ss.get("道具") or []
            _keys = _ss.get("关键场景信息") or []
            _items = []
            for _lst in (_anchors, _props, _keys):
                if isinstance(_lst, list):
                    for _it in _lst:
                        if isinstance(_it, dict):
                            _nm_i = str(_it.get("名称", "") or _it.get("ID", "") or "").strip()
                        else:
                            _nm_i = str(_it).strip()
                        if _nm_i and _nm_i not in _items:
                            _items.append(_nm_i)
                elif isinstance(_lst, str) and _lst.strip():
                    for _l in _lst.splitlines():
                        _l = _l.strip().lstrip("- ").strip()
                        if _l and _l not in _items:
                            _items.append(_l)
            _idx_lines.append(f"  {'●' if '焦点' in _flags else '○'} {_nm}" + (f"（{'/'.join(_flags)}）" if _flags else "") + (f": {'、'.join(_items)}" if _items else "（无元素）"))
    except Exception:
        pass
    if not _idx_lines:
        print("  （无 scene_state 元素可索引）")
    else:
        for _l in _idx_lines:
            print(_l)

    # §3 骨架待物化角色清单（任一状态骨架占位·④先决状态转换的输入）
    # 收窄到本轮相关角色（同 §1b 三源并集·剔除偏远跨区角色的无关骨架——Lawrence/Bernard/MiB 等不物化）
    print("\n[PRECHECK] SNAPSHOT §3 骨架占位未清角色（本轮相关·参考数据——④骨架物化前置·通常为空）:")
    _relevant_key = {_norm_char_key(n) for n in _loop_relevant_roles(world_dir)}
    _skeleton = []
    for _cn, cd in _load_char_states(world_dir):
        if _norm_char_key(_cn) not in _relevant_key:
            continue
        for _f in ("位置", "核心状态", "妆扮", "服饰"):
            _v = cd.get(_f)
            if isinstance(_v, str) and re.fullmatch(r"\s*\[[^\]]*\]\s*", _v):
                _skeleton.append(_cn)
                break
        else:
            if _decision_template_fields(cd):
                _skeleton.append(_cn)
    if not _skeleton:
        print("  （无骨架占位角色）")
    else:
        for _cn in sorted(set(_skeleton)):
            print(f"  {_cn}")

    print("[PRECHECK] 覆盖边界: 仅状态可导出的机械义务；唤醒判定行的「未唤醒」仅指机械信号未命中——用户指令加压 / 循环轨道偏离（§1b 对照·Step1 判） / 重大事件→事件扩散（①关联角色并集） / ③导演回判张力、变化维度是否达临界 等推断类触发由 LLM 自行判定，不在此列（窗口耗尽已由上方窗口状态项与 escalation_flags.停滞 机械导出·③D2/D4 判定）")
    print("[PRECHECK] 提示: 批次级预演走 `--dry-run`·单段复验走 `gate <阶段> --check`（与本次级义务预检互补·不重复）")
    return 0


def cmd_context(world_dir: Path, role: str | None = None):
    """Runtime Context 机械导出（v0.28·只读·exit 0 恒过）——direction 拍级字段编译（当前拍戏剧问题/guidance/
    调度单/时间窗口/转场）+ 推进池CT摘要 + 环境压力项 + 该角色相关事件/可观察行动。
    ④角色子 agent 组装通道优先引用（省重复读多文件 token）；输出不足则按 phase_actor 数据就绪逐项读。"""
    dr = _load_direction(world_dir)
    st = _load_storylines(world_dir)
    try:
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        ws = {}
    try:
        cd = yaml.safe_load((world_dir / "states" / "conflicts.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        cd = {}

    cur_sl = str(dr.get("当前事件线", "") or "").strip()
    cur_beat = str(dr.get("当前拍", "") or "").strip()

    print(f"[CONTEXT] {world_dir.name} · 当前拍: {cur_sl}/{cur_beat or '(未设)'} · 世界时间: {str((ws.get('时间') or {}).get('具体时间', '')) or '(未设)'} · 轮次: {ws.get('轮次', '-')}")
    # 拍问题（若当前拍对应 storylines 拍序则取戏剧问题）
    _drama_q = ""
    _payoff = ""
    if cur_sl and isinstance(st.get(STORYLINE_TOP_KEY) or {}, dict):
        _line = (st.get(STORYLINE_TOP_KEY) or {}).get(cur_sl)
        if isinstance(_line, dict):
            for _b in (_line.get("拍序") or []):
                if isinstance(_b, dict) and str(_b.get("拍名", "") or "").strip() == cur_beat:
                    _drama_q = str(_b.get("戏剧问题", "") or "").strip()
                    _payoff = str(_b.get("兑现形态", "") or "").strip()
                    break
    if _drama_q:
        print(f"  拍问题: {_drama_q}")
    if _payoff:
        print(f"  兑现形态: {_payoff}")
    # guidance（③每轮重判落盘·无复用）
    _g = str(dr.get("guidance", "") or "").strip()
    if _g:
        print(f"  guidance: {_g}")
    # 调度单（四层）
    _sched = str(dr.get("调度单", "") or "").strip()
    if _sched:
        print(f"  调度单: {_sched}")
    # 转场（③已判切换场景 → ④须把 POV 位置落到目标场景）
    _tr = _map_field(dr.get("转场"))
    _tr_tgt = str(_tr.get("目标场景", "") or "").strip()
    if _tr_tgt and _tr_tgt != "无":
        print(f"  转场: 目标场景={_tr_tgt}（③已判切换场景·POV 位置须落到该场景·⑤按场景切换流程执行）")
    # 时间窗口（拍级·剩余由脚本导出·v0.29）
    _win = _map_field(dr.get("时间窗口"))
    if isinstance(_win, dict) and str(_win.get("预算", "") or "").strip():
        _bm3, _el3, _re3, _exh3 = _window_status(world_dir)
        _wline = f"  时间窗口: 预算={_win.get('预算')} 起点={_win.get('起点', '(未设)')}"
        if _re3 is not None:
            _wline += f" 剩余≈{_re3}分钟"
        if _exh3 is True:
            _wline += " · 已耗尽（链收敛·③验收判定中）"
        elif _exh3 is False:
            _wline += " · 未耗尽（按决策环继续产行动）"
        else:
            _wline += " · 剩余不可判定"
        print(_wline)
    # 推进池CT摘要（紧迫度优先·逐条一行）
    _cts = sorted(
        [k for k, v in cd.items() if isinstance(v, dict) and str(k).startswith("CT-")],
        key=lambda k: {"🔴": 0, "🟡": 1, "🟢": 2}.get(str(cd[k].get("紧迫度", "") or "").strip(), 3),
    )
    if _cts:
        print("  推进池CT:")
        for _ct in _cts[:5]:
            _cv = cd[_ct]
            _urgency = str(_cv.get("紧迫度", "") or "").strip() or "?"
            _desc = str(_cv.get("描述", "") or "").strip()
            _press = str(_cv.get("施压方向", "") or "").strip()
            print(f"    {_ct}[{_urgency}] {(_desc[:40] + '…') if len(_desc) > 40 else _desc}" + (f" · 施压: {_press[:30]}" if _press else ""))
    else:
        print("  推进池CT: （无）")
    # 环境压力（外部倒计时/关键标记）
    _cds = (ws.get("外部倒计时") or {})
    if isinstance(_cds, dict) and _cds:
        print("  外部倒计时:")
        for _k, _v in list(_cds.items())[:3]:
            if isinstance(_v, dict):
                # 标签取值兼容：重置类用 威胁·事件类用 名称/说明（keys.md：周期倒计时写 威胁+到期时刻；
                # 非周期事件类倒计时写 名称+说明·无 威胁）——旧实现只读 威胁 → 事件类倒计时在 context 显示为空
                _lbl = str(_v.get("威胁", "") or _v.get("名称", "") or "").strip()
                if not _lbl:
                    _lbl = str(_v.get("说明", "") or "").strip()[:24]
                print(f"    {_k}: {_lbl}·剩余 {_v.get('剩余时间', '') or _v.get('剩余', '')}")
    # 指定角色相关（可观察行动/位置——从 CHAR_state 读）
    if role:
        _name = role.replace("_", " ").strip()
        _hit = None
        for _cn, _d in _load_char_states(world_dir):
            if _norm_char_key(_cn) == _norm_char_key(_name):
                _hit = _d
                break
        if _hit is not None:
            _pos = str(_hit.get("位置", "") or "").strip() or "?"
            _intent = str((_hit.get("decision") or {}).get("未完成意图", "") or "").strip() or "?"
            _act = str((_hit.get("decision") or {}).get("当前行动", "") or "").strip() or "?"
            print(f"  [{_name}] 位置={_pos} · 当前行动={_act[:40]} · 未完成意图={_intent[:40]}")
        else:
            print(f"  [{_name}] （无 CHAR_state·待物化）")
    return 0


def _parse_world_current_min(world_dir: Path):
    """读 world_state.时间.具体时间 → (cur_min:int|None, time_str:str)。与 in-track / precheck 共用同一时间源。"""
    try:
        cur = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        cur = {}
    t = str((cur.get("时间") or {}).get("具体时间") or "")
    m = re.search(r"(\d{1,2}):(\d{2})", t)
    cur_min = (int(m.group(1)) * 60 + int(m.group(2))) if m else None
    return cur_min, t


def _map_field(raw):
    """映射型 direction 字段容错取值 → dict（缺/非法 → {}）。

    存量脏数据兼容：历史批次曾把映射字段写成**带引号的字符串标量**——
    时间窗口 `'{起点: …, 预算: 45分钟}'`（YAML 载入即 str，`.get()` 抛
    AttributeError → window_status 返回全 None → ③拿不到余量 → 停滞判据第一
    合取项无法判真 → 永远滑向续演默认）；转场 `'{"目标场景": …}'`（同型：
    precheck 挂钩 / round-check 执行核验 / K6 硬拦三处静默跳过 → ③的切换场景
    决策到不了 ⑤）。此处统一归一：str 走 `yaml.safe_load` 再解析一次（JSON 是
    YAML 子集·Inline mapping 语法与 YAML 同源·比 literal_eval 更宽容「第1日」
    等非 Python 字面量），仍非法则返回 {}。precheck / context / gate /
    round-check 各处消费共用本函数——单一容错口径。"""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            again = yaml.safe_load(raw)
            if isinstance(again, dict):
                return again
        except Exception:
            pass
    return {}


def _window_status(world_dir: Path):
    """时间窗口状态导出（拍级·单一口径）→ (budget_min:int|None, elapsed_min:int|None, remain_min:int|None, exhausted:bool|None)。

    budget_min=预算分钟（'N分钟' 解析·失败 None）；elapsed_min=已耗=世界时间−窗口.起点（按 日*1440+分
    计·跨日修正）；remain_min=预算−已耗；exhausted=剩余<=0（True/False/None=状态不可判定）。
    供 precheck / context / gate 连续同拍共用的唯一计算口径——LLM 零解析。"""
    try:
        _win = _map_field(_load_direction(world_dir).get("时间窗口"))
        if not _win:
            return (None, None, None, None)
        budget = str(_win.get("预算", "") or "").strip()
        start = str(_win.get("起点", "") or "").strip()
        bm = None
        if budget:
            try:
                bm = int(budget.rstrip("分钟").strip())
            except Exception:
                bm = None
        if bm is None:
            return (bm, None, None, None)
        ws = yaml.safe_load((world_dir / "states" / "world_state.yaml").read_text(encoding="utf-8")) or {}
        cur = str((ws.get("时间") or {}).get("具体时间", "") or "").strip()
        if not cur:
            return (bm, None, None, None)
        if not start:
            # 起点缺失（存量线/历史落盘）：以当前世界时间为起点兜底——本拍计时自此起算·
            # 窗口不因缺字段而整体失效（③补设起点后回归正常口径）。
            start = cur
        d1, m1 = _parse_world_time(cur)
        d2, m2 = _parse_world_time(start)
        if d1 is None or d2 is None:
            return (bm, None, None, None)
        elapsed = max(0, (d1 * 1440 + m1) - (d2 * 1440 + m2))
        remain = bm - elapsed
        return (bm, elapsed, remain, remain <= 0)
    except Exception:
        return (None, None, None, None)


def _parse_char_timeline(world_dir: Path):
    """读全部 CHAR_.md「默认循环时间线」表 → {角色名: [(start_min, end_min, 位置, 动作), ...]}。
    与 in-track 共用；无时间线的角色记为 {角色名: []}。"""
    out = {}
    chars_dir = world_dir / "characters"
    if not chars_dir.is_dir():
        return out
    for cfp in sorted(chars_dir.glob("CHAR_*.md")):
        try:
            lines = cfp.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        in_table = False
        rows = []
        for ln in lines:
            if "默认循环时间线" in ln:
                in_table = True
                continue
            if not in_table:
                continue
            s = ln.strip()
            if s.startswith("|") and s.count("|") >= 3:
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) >= 3:
                    sm = re.search(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", cells[0])
                    if sm:
                        rows.append((int(sm.group(1)) * 60 + int(sm.group(2)),
                                     int(sm.group(3)) * 60 + int(sm.group(4)), cells[1], cells[2]))
            elif s and not s.startswith("#") and "|" not in s:
                break
        name = cfp.stem[len("CHAR_"):].replace("_state", "").strip()
        out[name] = rows
    return out


def _char_timeline_preset(rows, cur_min):
    """在某个角色的时间线段列中，取当前时刻命中的 (位置, 动作)；未命中取最早段。
    返回 (loc, action, is_in_window)；cur_min 为 None 时取最早段并标 is_in_window=False。"""
    if not rows:
        return ("", "", False)
    if cur_min is None:
        s0, e0, loc, ac = rows[0]
        return (loc, ac, False)
    hit = next(((loc, ac) for s0, e0, loc, ac in rows if s0 <= cur_min <= e0), None)
    if hit:
        return (hit[0], hit[1], True)
    return (rows[0][2], rows[0][3], False)


def _loops_interlocks(world_dir: Path):
    """读 story_architecture/LOOPS.md「跨角色互锁时刻表」→ [(start_min, end_min, 事件, [角色...], is_trigger), ...]。
    仅取可解析时段行；`触发式`（无时刻区间）行记 is_trigger=True 交由 LLM 判定（不属机械窗口扫描）。
    角色列以 `/` 分隔归一到字符串名。"""
    fp = world_dir / "story_architecture" / "LOOPS.md"
    if not fp.exists():
        return []
    try:
        lines = fp.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []
    out = []
    in_table = False
    for ln in lines:
        s = ln.strip()
        if "跨角色互锁时刻表" in ln:
            in_table = True
            continue
        if not in_table:
            continue
        if s.startswith("|") and s.count("|") >= 3:
            # 跳过表头（含「时刻」列）与分隔行（含 --- ）
            if any(x in s for x in ("---", "时刻", "互锁事件")):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 3:
                continue
            tm, ev, roles = cells[0], cells[1], cells[2]
            is_trigger = ("触发式" in tm) or ("触发" in tm)
            # 解析多个时段（如 09:30-11:00 / 11:30 / 触发式）
            spans = re.findall(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", tm)
            if spans:
                pts = re.findall(r"(\d{1,2}):(\d{2})", tm)
            else:
                pts = []
            roles_l = [r.strip() for r in re.split(r"[/、]", roles) if r.strip()]
            if spans:
                for a, b, c2, d2 in spans:
                    out.append((int(a) * 60 + int(b), int(c2) * 60 + int(d2), ev, roles_l, False))
            elif pts:
                for a, b in pts:
                    out.append((int(a) * 60 + int(b), int(a) * 60 + int(b), ev, roles_l, False))
            else:
                out.append((None, None, ev, roles_l, True))
    return out


def _loops_interlocks_near(interlocks, cur_min, window_min):
    """取与 [cur_min, cur_min+window_min] 区间重叠的互锁行（含进行中+即将开始）；单点按点落在窗口内判定。
    cur_min 为 None → 全部跳过（无时间基准）；interval 行 start/end 任一 None → 跳过（触发式/无时段由 LLM 判）。"""
    if cur_min is None:
        return []
    lo, hi = cur_min, cur_min + window_min
    out = []
    for (s0, e0, ev, roles, is_trigger) in interlocks:
        if is_trigger or s0 is None or e0 is None:
            continue
        # 区间重叠：s0 <= hi 且 e0 >= lo（进行中/即将开始都覆盖；单点 s0==e0 按点判定）
        if s0 <= hi and e0 >= lo:
            out.append((s0, e0, ev, roles))
    return out


def cmd_in_track(world_dir: Path):
    """只读查询：按各循环角色预设时间线，输出此刻各循环角色应在哪/做什么（供导演调度参考·不改任何角色）。"""
    cur_min, t = _parse_world_current_min(world_dir)
    print(f"# 世界时间: {t or '(未知)'}")
    timelines = _parse_char_timeline(world_dir)
    if not timelines:
        print("# 无 characters/ 目录")
        return
    for name, rows in sorted(timelines.items()):
        if not rows:
            print(f"- {name}: 无可用时间线")
            continue
        loc, ac, _inwin = _char_timeline_preset(rows, cur_min)
        if cur_min is None:
            print(f"- {name}: {loc} · {ac}（时间未解析·取最早段）")
        elif _inwin:
            print(f"- {name}: {loc} · {ac}")
        else:
            print(f"- {name}: {loc} · {ac}（时段外·取最早段）")


# ── CLI ───────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="WorldSim 批量状态管理 V2")
    parser.add_argument("world", help="世界名")
    parser.add_argument("action", choices=["read", "write", "write-raw", "append-raw", "delete", "convert", "validate", "audit", "grep", "scan", "gate", "storyline", "beat", "reset-cycle", "round-check", "tmp-clean", "map-sync", "init-states", "lint", "fix", "in-track", "precheck", "cast-baseline", "context", "ledger"])
    parser.add_argument("--files", help="read 时限定文件 key 列表，逗号分隔")
    parser.add_argument("--full", action="store_true", help="write 时全量覆写")
    parser.add_argument("--batch", action="store_true", help="write-raw/append-raw 批量模式：stdin 为 ###FILE/###KEY/###APPEND 记录格式（⚠非幂等：APPEND 重复执行会重复追加·同一批次只执行一次·验证用 read/validate/--dry-run）")
    parser.add_argument("--file", help="write-raw/append-raw --batch、gate/audit --check 的批次文本文件（UTF-8·兼容 BOM·等价 stdin）——PowerShell 等无 heredoc 环境的编码安全通道")
    parser.add_argument("--dry-run", action="store_true", help="write-raw/append-raw 预演（实跑前硬性闸·判据=退出码）：解析+audit+段级闸门+op 级形态预检+对比磁盘差异，不落盘；exit 1=实跑必失败（禁提交·段级闸门拦截或 op 级失败），exit 0=通过（必要条件·不模拟磁盘异常）")
    parser.add_argument("--resume-from", type=int, help="write-raw/append-raw --batch 仅执行段 N 及其后（按原始批次段号 1 起始·失败重提时免重跑已成功段——须先按 [BATCH-FAIL] 报告剔除已落盘结构动作）")
    parser.add_argument("--check", action="store_true", help="gate 代码化核验模式：从 stdin 读 change set（dramatist）或叙事（writer），运行可代码化检查，不合格 exit 1")
    parser.add_argument("--target", help="gate writer 专用（可选）：大约目标 token 数（如 1200）")
    parser.add_argument("--style", choices=["sepia", "dialogue", "explicit"], help="gate writer 专用（可选）：本轮叙事风格路径")
    parser.add_argument("--live", action="store_true", help="scan 仅当前文件（排除历史轮转 narrative.*.md 与 archive）")
    parser.add_argument("--force", action="store_true", help="write-raw/append-raw --batch: 显式回退轮·绕过 audit ④ 轮次单调/⑬b 轨迹覆盖写（其余硬性检查照常·回退后必做残留扫描+validate）")
    parser.add_argument("--maintenance", action="store_true", help="write-raw/append-raw --batch: 维护批模式——豁免段级完整性闸（角色覆盖/ACTION↔decision 共现/必含项/施压方向/轨道/cast），op 级合法性校验照常（格式/白名单/单写者/结构化 APPEND/轮次单调）。用途=同轮续批字段修复/数据归一，一批只含增量 op")
    parser.add_argument("--asset", help="reset-cycle: 事件重置指定角色（单角色模式·登记事件条目·不重建周期倒计时）")
    parser.add_argument("extra", nargs="*", help="write-raw/append-raw 的额外参数: <文件key> <YAML键路径> [内容]")
    # storyline/beat 子命令 help 直达（argparse 内建 --help 会拦截并打印全局 help）
    argv = sys.argv[1:]
    if len(argv) >= 3 and argv[1] in ("storyline", "beat") and argv[2] in ("--help", "-h"):
        fn = cmd_storyline if argv[1] == "storyline" else cmd_beat
        fn(get_world_dir(argv[0]), ["--help"])
        sys.exit(0)
    args = parser.parse_args()

    world_dir = get_world_dir(args.world)

    if args.action == "read":
        # 文件过滤：--files a,b,c 或位置参数（commands.md：位置参数=文件 key 过滤）
        files_filter = None
        if args.files:
            files_filter = args.files.split(",")
        elif args.extra:
            files_filter = [a for a in args.extra if not a.startswith("-")]
        cmd_read(world_dir, files_filter)
    elif args.action == "write":
        cmd_write(world_dir, full_replace=args.full)
    elif args.action == "write-raw":
        cmd_write_raw(world_dir, args.extra, batch=args.batch, dry_run=args.dry_run, force=args.force, input_file=args.file, resume_from=args.resume_from, maintenance=args.maintenance)
    elif args.action == "append-raw":
        cmd_write_raw(world_dir, args.extra, batch=args.batch, append_mode=True, dry_run=args.dry_run, force=args.force, input_file=args.file, resume_from=args.resume_from, maintenance=args.maintenance)
    elif args.action == "delete":
        sys.exit(0 if cmd_delete(world_dir, args.extra) else 1)
    elif args.action == "convert":
        cmd_convert(world_dir)
    elif args.action == "validate":
        sys.exit(0 if cmd_validate(world_dir) == 0 else 1)
    elif args.action == "audit":
        cmd_audit(world_dir, input_file=args.file)
    elif args.action == "grep":
        keyword = " ".join(args.extra)
        cmd_grep(world_dir, keyword)
    elif args.action == "scan":
        cmd_scan(world_dir, args.extra, live_only=args.live)
    elif args.action == "gate":
        cmd_gate(world_dir, args.extra, check_mode=args.check, input_file=args.file, target=args.target, style=args.style)
    elif args.action == "storyline":
        cmd_storyline(world_dir, args.extra)
    elif args.action == "beat":
        cmd_beat(world_dir, args.extra)
    elif args.action == "reset-cycle":
        sys.exit(cmd_reset_cycle(world_dir, args.world, asset=args.asset))
    elif args.action == "round-check":
        cmd_round_check(world_dir)
    elif args.action == "cast-baseline":
        sys.exit(cmd_cast_baseline(world_dir))
    elif args.action == "precheck":
        sys.exit(cmd_precheck(world_dir))
    elif args.action == "context":
        cmd_context(world_dir, args.extra[0] if args.extra else None)
    elif args.action == "map-sync":
        cmd_map_sync(world_dir)
    elif args.action == "init-states":
        sys.exit(cmd_init_states(world_dir) or 0)
    elif args.action == "tmp-clean":
        cmd_tmp_clean(world_dir)
    elif args.action == "lint":
        cmd_lint(world_dir)
    elif args.action == "fix":
        cmd_fix(world_dir)
    elif args.action == "in-track":
        cmd_in_track(world_dir)
    elif args.action == "ledger":
        cmd_ledger(world_dir, args.extra)

if __name__ == "__main__":
    main()
