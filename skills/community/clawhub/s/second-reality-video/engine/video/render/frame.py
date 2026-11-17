"""R2 帧渲染器契约：无时序的逐帧渲染。

为什么单独一个文件
----------------
HLD §4 把 R2 从"条件化 video diffusion"改写为**逐帧独立**的帧渲染器：
输入只含单帧 Scene IR，不含任何跨帧上下文。本文件把这个契约写成
**可静态检查**的形式 —— 审计维度 31 `render_is_frame_independent`。

判据（全部静态、确定性，不依赖任何视觉判定）
--------------------------------------------
1. Scene IR schema 不含任何跨帧字段，且顶层与实体层都是
   `additionalProperties: false`（多一个字段就多一条可塞跨帧状态的口子）；
2. 每个渲染器的像素入口 `render_ir` 的签名不含任何跨帧参数；
3. 给定一帧 IR 实例时，其顶层与实体层都不含跨帧字段。

实现用 `ast` 解析源码，**不 import 渲染器** —— 审计器不该为了查契约
把 pygame 拉进来。本模块只依赖标准库。
"""

import ast
import json
from pathlib import Path
from typing import Dict, List, Optional

from video.render.tier import RenderTier

# 跨帧字段名黑名单（IR 里出现即违规）
CROSS_FRAME_FIELDS = frozenset({
    "prev_frames", "prev_frame", "previous_frames", "previous_frame",
    "prev_state", "prev_states", "last_frames", "last_frame",
    "frame_history", "temporal_context", "temporal_state",
    "history_frames", "state_history",
})

# 跨帧参数名黑名单（渲染入口签名里出现即违规）
CROSS_FRAME_PARAMS = frozenset({
    "prev_frames", "prev_frame", "previous_frames", "previous_frame",
    "prev_state", "prev_states", "last_frames", "last_frame",
    "frame_history", "temporal_context", "temporal_state",
    "history_frames", "state_history", "frames", "history",
})

# 渲染层的像素入口名 —— 唯一被允许产生像素的函数
RENDER_ENTRY = "render_ir"

RENDER_DIR = Path(__file__).resolve().parent
VIDEO_DIR = RENDER_DIR.parent
SCENE_IR_SCHEMA = VIDEO_DIR / "scene_ir.schema.json"


class FrameRenderer(RenderTier):
    """R2 帧渲染器基类：逐帧独立，输入只有单帧 Scene IR。

    契约（见 HLD §4.2 / §8.1）：
    - 像素入口固定为 `render_ir(scene_ir)`，**不接受任何跨帧上下文**；
    - `render(frame_state, shot, ctx)` 只是把旧入口转译成 IR 的兼容层，
      同样不引入跨帧状态；
    - 权重哈希、采样种子、硬件必须如实写进 `provenance()`，
      复现口径是"同环境可复现"，**不得宣称逐字节**。

    本类是**契约**，不是实现：真正的像素来自训练好的权重
    （教师 = R1，配对数据契约见 HLD §4.3）。
    """

    def __init__(self, assets: Optional[Dict] = None):
        self.assets = assets or {}

    @property
    def tier_id(self) -> str:
        return "R2-frame"

    @property
    def version(self) -> str:
        """契约版本。

        有权重时由子类改为 `weights_sha256[:16]`（权重哈希，不是自增版本号）；
        无权重的契约基类用契约自身的版本标识 —— **不冒充**某个权重哈希。
        """
        return "r2-frame-contract/1"

    def render_ir(self, scene_ir: Dict) -> bytes:
        """由训练好的权重渲染单帧。返回未压缩 RGB24 字节。"""
        raise NotImplementedError(
            "R2 帧渲染器尚未实现：需要训练权重。教师=R1 确定性渲染器，"
            "配对数据契约见 HLD §4.3，接口契约见 MANUAL §8.1。"
        )

    def render(self, frame_state: Dict, shot: Dict, ctx) -> bytes:
        """兼容入口：先把 FrameState 编译成 Scene IR，再交给 `render_ir`。

        与 R1 同构 —— 渲染层的**唯一**输入合同是单帧 Scene IR。
        这里不做任何跨帧聚合。
        """
        from video.scene_ir import compile_scene_ir

        scene_ir = compile_scene_ir(frame_state, shot, assets=self.assets,
                                    frame_index=ctx.frame_index, sub=ctx.sub)
        return self.render_ir(scene_ir)

    def provenance(self) -> Dict:
        return {
            "tier": "R2",
            "tier_id": self.tier_id,
            "input_contract": "scene_ir",
            "temporal_context": False,
            "weights_sha256": None,
            "seed": None,
            "hardware": None,
            "note": "R2 帧渲染器未训练：无权重可声明。",
        }


# ---------------------------------------------------------------- 静态检查


def _iter_dict_keys(node):
    """递归产出 dict 里的所有键名。"""
    if isinstance(node, dict):
        for key, value in node.items():
            yield str(key)
            yield from _iter_dict_keys(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_dict_keys(item)


def _check_schema(schema: Dict) -> List[str]:
    """schema 不得含跨帧字段；且必须封闭（additionalProperties=false）。"""
    violations = []
    for key in _iter_dict_keys(schema):
        if key.lower() in CROSS_FRAME_FIELDS:
            violations.append("Scene IR schema 含跨帧字段 `%s`" % key)
    props = schema.get("properties")
    if isinstance(props, dict):
        # JSON Schema 里 additionalProperties 与 properties 同级，不是它的子项
        if schema.get("additionalProperties") is not False:
            violations.append(
                "Scene IR schema 顶层不是封闭的（additionalProperties != false）"
                " —— 跨帧状态可从多出的字段塞进来")
        entities = props.get("entities")
        if isinstance(entities, dict):
            items = entities.get("items")
            if isinstance(items, dict) and items.get("additionalProperties") is not False:
                violations.append(
                    "Scene IR schema 的 entity 不是封闭的"
                    "（additionalProperties != false）")
    return violations


def _check_entry_signatures(render_dir: Path) -> (List[str], List[str]):
    """用 ast 静态检查每个渲染器的 `render_ir` 签名。"""
    violations = []
    checked = []
    for path in sorted(render_dir.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name != RENDER_ENTRY:
                continue
            params = [a.arg for a in node.args.args]
            params += [a.arg for a in node.args.kwonlyargs]
            if node.args.vararg:
                params.append(node.args.vararg.arg)
            if node.args.kwarg:
                params.append(node.args.kwarg.arg)
            bad = [p for p in params if p.lower() in CROSS_FRAME_PARAMS]
            checked.append("%s:%s(%s)" % (path.name, node.name, ", ".join(params)))
            if bad:
                violations.append(
                    "%s 的 %s 接受跨帧参数 %s" % (path.name, node.name, ", ".join(bad)))
    return violations, checked


def _check_ir_instance(scene_ir: Dict) -> List[str]:
    """给定的 IR 实例不得含跨帧字段。"""
    violations = []
    for key in _iter_dict_keys(scene_ir):
        if key.lower() in CROSS_FRAME_FIELDS:
            violations.append("Scene IR 实例含跨帧字段 `%s`" % key)
    return violations


def check_render_independence(scene_ir: Optional[Dict] = None,
                              schema_path: Optional[Path] = None,
                              render_dir: Optional[Path] = None) -> Dict:
    """维度 31 的判定式：渲染层无时序上下文。

    Returns:
        {"ok": bool, "violations": [...], "checked": [...], "schema": str}
    """
    schema_path = Path(schema_path) if schema_path else SCENE_IR_SCHEMA
    render_dir = Path(render_dir) if render_dir else RENDER_DIR

    violations: List[str] = []
    checked: List[str] = []

    if not schema_path.exists():
        violations.append("Scene IR schema 缺失：%s" % schema_path)
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        violations.extend(_check_schema(schema))

    sig_violations, checked = _check_entry_signatures(render_dir)
    violations.extend(sig_violations)

    if scene_ir is not None:
        violations.extend(_check_ir_instance(scene_ir))

    return {
        "ok": not violations,
        "violations": violations,
        "checked": checked,
        "schema": str(schema_path),
        "render_entry": RENDER_ENTRY,
    }


__all__ = [
    "CROSS_FRAME_FIELDS",
    "CROSS_FRAME_PARAMS",
    "RENDER_ENTRY",
    "FrameRenderer",
    "check_render_independence",
]
