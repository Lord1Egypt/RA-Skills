"""结构验收：只判断"世界是否按规则出现"，不评价像素好不好看。

分级
----
- error   : 架构违约，必须阻断渲染。当前判据：缺字段、相机非法、坐标非有限值、
            id 重复、身份资产跨帧漂移、render_class 非法、社交对象不存在。
- warning : 可疑但不阻断。当前判据：needs 越界、单帧位移超过阈值、调色板非法。

设计理由
--------
视频模型的幻觉发生在像素；本项目的对应风险发生在**结构**：
同一 soul 换了身份、实体瞬移、相机参数非法。这些问题在 FrameState 里就能判，
不需要视觉模型，也不该被"看起来还行"放过。
"""

import math
import re
from typing import Dict, List, Optional

from video.scene_ir import SCHEMA_VERSION

_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CAMERA_MODES = {"static", "follow", "orbit", "aoi"}
# 合法渲染类别。R2（神经渲染）必须按此渲染，不得按生成模型先验改写实体类别。
_RENDER_CLASSES = {"soul"}


def _is_finite(value) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _distance(a: List[float], b: List[float]) -> float:
    dims = min(len(a), len(b))
    return math.sqrt(sum((float(a[i]) - float(b[i])) ** 2 for i in range(dims)))


def validate_scene_ir(ir: Dict) -> Dict:
    """单帧结构校验。返回 {ok, errors, warnings}。"""
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(ir, dict):
        return {"ok": False, "errors": ["scene_ir 不是 dict"], "warnings": []}

    tag = "tick {0}".format(ir.get("tick"))

    if ir.get("schema") != SCHEMA_VERSION:
        errors.append("{0}: schema 不是 {1}".format(tag, SCHEMA_VERSION))
    if not ir.get("world_id"):
        errors.append("{0}: world_id 缺失".format(tag))
    if not isinstance(ir.get("entities"), list):
        errors.append("{0}: entities 必须是 list".format(tag))

    camera = ir.get("camera") or {}
    if camera.get("mode") not in _CAMERA_MODES:
        errors.append("{0}: 非法相机 mode={1}".format(tag, camera.get("mode")))
    origin = camera.get("origin") or []
    if len(origin) < 2 or not all(_is_finite(v) for v in origin[:2]):
        errors.append("{0}: 相机 origin 非法".format(tag))
    zoom = camera.get("zoom", 1.0)
    if not _is_finite(zoom) or float(zoom) <= 0:
        errors.append("{0}: 相机 zoom 必须为正数".format(tag))
    fov = camera.get("fov", 60.0)
    if not _is_finite(fov) or not (1.0 <= float(fov) <= 180.0):
        errors.append("{0}: 相机 fov 超出 (1,180)".format(tag))

    framing = ir.get("framing") or {}
    resolution = framing.get("resolution") or []
    if len(resolution) != 2 or not all(
            _is_finite(v) and int(v) > 0 for v in resolution):
        errors.append("{0}: resolution 非法".format(tag))
    fps = framing.get("fps")
    if not _is_finite(fps) or int(fps) <= 0:
        errors.append("{0}: fps 非法".format(tag))

    seen_ids = set()
    for index, entity in enumerate(ir.get("entities") or []):
        eid = entity.get("id")
        if not eid:
            errors.append("{0}: entities[{1}] 缺 id".format(tag, index))
            continue
        if eid in seen_ids:
            errors.append("{0}: 实体 id 重复 {1}".format(tag, eid))
        seen_ids.add(eid)

        position = entity.get("position") or []
        if len(position) < 2 or not all(_is_finite(v) for v in position):
            errors.append("{0}: {1} position 非有限值".format(tag, eid))

        render_class = entity.get("render_class")
        if not render_class:
            errors.append("{0}: {1} 缺 render_class".format(tag, eid))
        elif render_class not in _RENDER_CLASSES:
            errors.append("{0}: {1} render_class 非法 {2}".format(
                tag, eid, render_class))

        needs = entity.get("needs") or {}
        for key, value in needs.items():
            if not _is_finite(value):
                errors.append("{0}: {1} needs[{2}] 非有限值".format(tag, eid, key))
            elif not (0.0 <= float(value) <= 1.0):
                warnings.append("{0}: {1} needs[{2}]={3} 超出 [0,1]"
                                .format(tag, eid, key, value))

        identity = entity.get("identity") or {}
        asset = identity.get("asset_hash")
        if asset is not None and not _HEX64.match(str(asset)):
            errors.append("{0}: {1} asset_hash 非法".format(tag, eid))
        for color in identity.get("palette") or []:
            if not _HEX.match(str(color)):
                warnings.append("{0}: {1} 调色板非法 {2}".format(tag, eid, color))

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def validate_scene_sequence(irs: List[Dict], max_step: float = 20.0) -> Dict:
    """整段序列校验：逐帧 + 身份漂移 + 单帧位移。

    Args:
        irs: 按播放顺序排列的 Scene IR
        max_step: 单帧允许的最大位移（世界坐标单位）；超过仅告警，
                  因为世界规则可能允许快速移动，阈值由调用方决定。
    """
    errors: List[str] = []
    warnings: List[str] = []
    max_distance = 0.0
    entity_count_max = 0

    previous: Optional[Dict] = None
    known_ids = set()
    for ir in irs:
        for entity in ir.get("entities") or []:
            if entity.get("id"):
                known_ids.add(entity.get("id"))
    for ir in irs:
        result = validate_scene_ir(ir)
        errors.extend(result["errors"])
        warnings.extend(result["warnings"])
        entity_count_max = max(entity_count_max, len(ir.get("entities") or []))

        if previous is not None:
            prev_by_id = {e.get("id"): e for e in (previous.get("entities") or [])}
            for entity in ir.get("entities") or []:
                prev = prev_by_id.get(entity.get("id"))
                if not prev:
                    continue  # 新增实体是合法事件
                prev_asset = (prev.get("identity") or {}).get("asset_hash")
                cur_asset = (entity.get("identity") or {}).get("asset_hash")
                if prev_asset and cur_asset and prev_asset != cur_asset:
                    errors.append(
                        "tick {0}: 身份漂移 {1}（{2} → {3}）".format(
                            ir.get("tick"), entity.get("id"),
                            prev_asset[:12], cur_asset[:12])
                    )
                distance = _distance(prev.get("position") or [],
                                     entity.get("position") or [])
                max_distance = max(max_distance, distance)
                if distance > max_step:
                    warnings.append(
                        "tick {0}: {1} 单帧位移 {2:.2f} > {3:.2f}".format(
                            ir.get("tick"), entity.get("id"), distance, max_step)
                    )
        previous = ir

    # 社交对象必须真实存在于场景里 —— 关系图不能指向不存在的实体
    for ir in irs:
        for event in ir.get("events") or []:
            partner = (event.get("interact") or {}).get("partner")
            if partner and partner not in known_ids:
                errors.append("tick {0}: 社交对象 {1} 不存在于场景".format(
                    ir.get("tick"), partner))

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "frames": len(irs),
        "entity_count_max": entity_count_max,
        "max_step_distance": round(max_distance, 4),
    }


def format_report(result: Dict, scene_digest: str = "", label: str = "Scene IR") -> str:
    """把验收结果格式化成可落盘的文本报告。"""
    lines = [
        "=== 结构验收 / {0} ===".format(label),
        "frames         : {0}".format(result.get("frames", 0)),
        "entities (max) : {0}".format(result.get("entity_count_max", 0)),
        "max step dist  : {0}".format(result.get("max_step_distance", 0.0)),
        "scene digest   : {0}".format(scene_digest[:32] + "..." if scene_digest else "—"),
        "errors         : {0}".format(len(result.get("errors", []))),
        "warnings       : {0}".format(len(result.get("warnings", []))),
        "VERDICT        : {0}".format("PASS" if result.get("ok") else "FAIL"),
        "",
    ]
    for message in result.get("errors", []):
        lines.append("[ERROR]   " + message)
    for message in result.get("warnings", []):
        lines.append("[WARNING] " + message)
    return "\n".join(lines) + "\n"
