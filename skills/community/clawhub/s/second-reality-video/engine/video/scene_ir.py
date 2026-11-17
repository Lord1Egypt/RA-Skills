"""Scene IR：逻辑层与像素层之间唯一的合同。

    frame = render(scene_ir, shot)
    scene_ir = compile(frame_state, shot, assets)

设计约束（与 R1 确定性契约同源）
-------------------------------
- 纯函数：不读墙钟、不写回世界状态、不依赖 dict 遍历序；
- 只携带事实：实体 / 位置 / needs / 身份哈希 / 相机 / 画幅 / 事件；
- 不携带像素，也不承诺画法 —— 投影是渲染器的事；
- 同一 `(frame_state, shot, assets, frame_index, sub)` 必得同一 JSON 与 digest。

为什么要有这一层
----------------
当前 `RenderTier.render(frame_state, shot, ctx)` 让渲染器直接读 FrameState，
逻辑（谁在哪、身份是谁）和画法（怎么打光、怎么上材质）混在一个入口。
Scene IR 把前者固定成可 diff、可断言、可哈希的中间表示。
接入渲染适配器后，R1 与 R2 都消费同一份 IR，结构无法被"画回来"。

现状（Phase 0.5）
----------------
`render` 仍直接读 FrameState；本模块先固化逻辑层合同，并提供独立校验入口。
把渲染器改成消费 IR 属下一步，未在本次改动中完成 —— 不在文档里冒充已完成。
"""

import hashlib
import json
from typing import Dict, List, Optional

SCHEMA_VERSION = "second-reality.scene-ir/1"

DEFAULT_RESOLUTION = [1920, 1080]
DEFAULT_FPS = 30
DEFAULT_ASPECT = "16:9"


def _round(value, ndigits: int = 6) -> float:
    return round(float(value), ndigits)


def _canonical(obj) -> str:
    """稳定序列化：排序键、无多余空白 —— digest 的唯一口径。"""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def asset_hash(asset: Optional[Dict]) -> Optional[str]:
    """外观资产摘要；None 表示该实体没有登记身份资产。"""
    if not asset:
        return None
    return hashlib.sha256(_canonical(asset).encode("utf-8")).hexdigest()


def _embedding_digest(asset: Optional[Dict]) -> Optional[str]:
    if not asset:
        return None
    embedding = asset.get("embedding")
    if not embedding:
        return None
    material = _canonical([_round(v, 8) for v in embedding])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _palette(asset: Optional[Dict]) -> List[str]:
    if not asset:
        return []
    palette = asset.get("palette") or []
    # 排序消除资产内部顺序差异；只保留可解析的 #RRGGBB
    return sorted(str(c) for c in palette)


def _safe_int(value, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _safe_float(value, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def compile_scene_ir(frame_state: Dict, shot: Dict, assets: Optional[Dict] = None,
                     frame_index: int = 0, sub: int = 0) -> Dict:
    """把一帧世界事实编译成 Scene IR。

    Args:
        frame_state: `state_feed.extract_tick_state` 的产物（或插值后的子帧）
        shot: ShotGraph 中的单条 shot（只含相机 / 画幅 / overlay）
        assets: `identity_assets.build_assets` 的产物；缺省时身份字段为 null
        frame_index: 全片帧序号（写进 IR 便于定位；不参与身份判定）
        sub: tick 内的子帧序号
    """
    assets = assets or {}
    souls = frame_state.get("souls") or {}

    camera_in = shot.get("camera") or {}
    origin = camera_in.get("origin") or [0.0, 0.0]
    framing = shot.get("framing") or {}
    resolution = framing.get("resolution") or DEFAULT_RESOLUTION

    entities: List[Dict] = []
    # 固定字典序：dict 遍历序不稳定，IR 必须与进程无关
    for soul in sorted(souls):
        data = souls[soul] or {}
        position = data.get("position") or [0.0, 0.0, 0.0]
        asset = assets.get(soul)
        entities.append({
            "id": soul,
            "kind": "soul",
            # render_class：实体类别绑定。给将来的 R2（神经渲染）用 ——
            # 它必须知道"这是几何体"还是"这是人"，否则生成模型会按自己的
            # 训练先验把人形/写实化，悄悄改写世界观。绑定在 IR 里，
            # 模型拿到的是**被约束的**类别，而不是自由发挥的提示词。
            "render_class": "soul",
            "position": [_round(v) for v in position],
            "needs": {k: _round(v) for k, v in sorted((data.get("needs") or {}).items())},
            "relationships": {k: _round(v) for k, v in
                              sorted((data.get("relationships") or {}).items())},
            "identity": {
                "asset_hash": asset_hash(asset),
                "embedding_digest": _embedding_digest(asset),
                "palette": _palette(asset),
            },
        })

    events = []
    for e in frame_state.get("events") or []:
        interact = e.get("interact") or {}
        events.append({
            "order_seq": e.get("order_seq"),
            "soul": e.get("soul"),
            "action": e.get("action"),
            "pos": [_round(v) for v in (e.get("pos") or [0.0, 0.0, 0.0])],
            # 社交交互：谁和谁、亲密度多少 —— 字幕桥与结构验收都读它
            "interact": {
                "partner": interact.get("partner"),
                "strength": _round(interact.get("strength") or 0.0),
                "closeness": _round(interact.get("closeness") or 0.0),
            },
        })

    return {
        "schema": SCHEMA_VERSION,
        "world_id": frame_state.get("world_id"),
        "genesis_seed": frame_state.get("genesis_seed"),
        "tick": frame_state.get("tick"),
        "frame_index": _safe_int(frame_index, 0),
        "sub": _safe_int(sub, 0),
        "source": {
            "content_digest": frame_state.get("content_digest"),
        },
        "camera": {
            "mode": camera_in.get("mode"),
            "origin": [_round(v) for v in origin],
            "target_soul": camera_in.get("target_soul"),
            "zoom": _safe_float(camera_in.get("zoom"), 1.0),
            "fov": _safe_float(camera_in.get("fov"), 60.0),
            "height": _safe_float(camera_in.get("height"), 50.0),
        },
        "framing": {
            "aspect": framing.get("aspect", DEFAULT_ASPECT),
            "resolution": [_safe_int(resolution[0], DEFAULT_RESOLUTION[0]),
                           _safe_int(resolution[1], DEFAULT_RESOLUTION[1])],
            "fps": _safe_int(framing.get("fps"), DEFAULT_FPS),
        },
        "overlay": shot.get("overlay") or {},
        "entities": entities,
        "events": events,
        "delta": frame_state.get("delta") or {},
    }


def scene_ir_digest(scene_ir: Dict) -> str:
    """Scene IR 的内容摘要 —— 结构层的复现锚。"""
    return hashlib.sha256(_canonical(scene_ir).encode("utf-8")).hexdigest()


def scene_ir_sequence_digest(irs: List[Dict]) -> str:
    """整段 Scene IR 摘要：逐行稳定序列化后整体哈希。"""
    lines = [json.dumps(ir, ensure_ascii=False, sort_keys=True) for ir in irs]
    material = "\n".join(lines)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def write_scene_ir(irs: List[Dict], output_path: str) -> str:
    """写入 JSONL，并返回整份序列的摘要（与 scene_ir_sequence_digest 同口径）。"""
    from pathlib import Path

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for ir in irs:
            f.write(json.dumps(ir, ensure_ascii=False, sort_keys=True) + "\n")
    return scene_ir_sequence_digest(irs)
