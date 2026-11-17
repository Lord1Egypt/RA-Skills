"""R1 确定性渲染器：把 FrameState 投影成像素。

确定性契约（硬标准）
--------------------
给定同一 `(frame_state, shot, ctx)`，本渲染器必须产出**逐字节相同的 RGB 缓冲**。
因此：
  - 不读 wall clock（需要时间时只用 `ctx.tick`）；
  - 不依赖 dict 遍历序（一切遍历先 sorted）；
  - 不使用 `random` 模块；一切随机感来自对内容的 sha256 派生；
  - 不写回世界状态（纯函数，对应 representation_isolation 审计维度）。

画面与 demo/virtual_world.py 的等距投影同源（2:1 菱形，TW2=16 / TH2=8），
但去掉 350px 侧栏、输出纯视口。画质升级（资产包 / 3D）属 Phase 1，不在本文件。
"""

import hashlib
import math
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import pygame
except ImportError:
    raise ImportError("pygame required for R1 rendering: pip install pygame")

from video.render.tier import RenderTier, RenderContext
from video.scene_ir import compile_scene_ir
from video import bitmap_font

# ---- 等距投影常量（与 demo 同源）----
TW2 = 16
TH2 = 8
Z_SCALE = 1.2

# ---- 调色板（与 demo 的动漫调色板保持同一观感）----
PALETTE = {
    "sky_top": (118, 176, 236),
    "sky_bot": (216, 238, 248),
    "grass": (146, 204, 124),
    "grass_line": (120, 176, 106),
    "shadow": (30, 40, 70),
    "ink": (38, 34, 44),
    "ground_bg": (10, 11, 14),
}

FORBIDDEN_ACTION_KEYS = ("set_needs", "move_agent", "force_event")


class DeterministicRenderer(RenderTier):
    """R1：确定性等距渲染，输出未压缩 RGB 缓冲（供 ffmpeg rawvideo 管道）。"""

    def __init__(self, world_size: int = 60, cell_size: int = 32,
                 assets: Optional[Dict[str, Dict]] = None):
        self.world_size = world_size
        self.cell_size = cell_size
        self.assets = assets or {}
        self._version_hash = self._compute_version()

        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        if not pygame.get_init():
            pygame.init()

    # ---- RenderTier ----

    @property
    def tier_id(self) -> str:
        return "R1-deterministic"

    @property
    def version(self) -> str:
        return self._version_hash

    def _compute_version(self) -> str:
        """渲染器版本 = 本文件源码的 sha256（第三方可复算）。"""
        source = Path(__file__).read_bytes()
        return hashlib.sha256(source).hexdigest()[:16]

    def render(self, frame_state: Dict, shot: Dict, ctx: RenderContext) -> bytes:
        """兼容入口：先把 FrameState 编译成 Scene IR，再交给 render_ir。

        保留这个方法是为了不破坏 render / verify 的既有调用；
        新代码应直接调用 `render_ir()` —— 它才是渲染层真正的输入合同。
        """
        scene_ir = compile_scene_ir(frame_state, shot, assets=self.assets,
                                    frame_index=ctx.frame_index, sub=ctx.sub)
        return self.render_ir(scene_ir)

    def render_ir(self, scene_ir: Dict) -> bytes:
        """渲染一帧 Scene IR，返回 RGB24 未压缩字节。

        只读 `scene_ir`：相机、实体、身份调色板、画幅全部来自 IR；
        不读 FrameState，不读墙钟。同一份 IR 必得同一缓冲。
        """
        framing = scene_ir.get("framing") or {}
        width, height = framing.get("resolution") or [1920, 1080]
        screen = pygame.Surface((width, height))
        view = self._resolve_view_ir(scene_ir, width, height)

        self._draw_sky(screen, width, height)
        self._draw_island(screen, view, width, height)
        self._draw_agents(screen, scene_ir.get("entities") or [], view)
        self._draw_overlay(screen, scene_ir, width, height)

        return pygame.image.tobytes(screen, "RGB")

    def provenance(self) -> Dict:
        return {
            "tier": "R1",
            "version": self._version_hash,
            "renderer": "pygame-iso-deterministic",
            "input_contract": "scene_ir",
            "source_sha256": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
            "projection": {"tw2": TW2, "th2": TH2, "z_scale": Z_SCALE},
            "world_size": self.world_size,
        }

    # ---- overlay：字幕桥 ----

    def _draw_overlay(self, screen, scene_ir: Dict, width: int, height: int):
        """按 shot 的 overlay 配置叠加图层。当前只实装字幕（caption_from=ledger）。

        字幕内容全部来自 IR 里的事实（谁做了什么行动、和谁交互、谁的哪个需求
        最匮乏），不写死任何剧情 —— 观众看到的是世界**正在发生**什么，
        不是一句旁白。这是把抽象世界变得可读的那座桥。
        """
        overlay = scene_ir.get("overlay") or {}
        if overlay.get("caption_from") != "ledger":
            return
        caption = self._ledger_caption(scene_ir)
        if not caption:
            return
        max_scale = max(2, height // 360)
        caption, scale = self._fit_caption(caption, width, max_scale)
        bar_h = bitmap_font.text_height(scale) + 8
        # 半透明底板：字幕必须始终可读，但不能把画面内容挡死
        bar = pygame.Surface((width, bar_h), pygame.SRCALPHA)
        bar.fill((10, 12, 18, 190))
        screen.blit(bar, (0, height - bar_h))
        bitmap_font.draw_text(screen, caption, 10, height - bar_h + 4,
                              (235, 238, 245), scale)

    def _fit_caption(self, caption: str, width: int, max_scale: int):
        """挑一个能放下整行字幕的字号；实在放不下就截断加省略号。

        字幕绝不能被画布右缘切掉 —— 半句话比没有字幕更糟。
        """
        limit = max(20, width - 20)
        scale = max(1, max_scale)
        while scale > 1 and bitmap_font.text_width(caption, scale) > limit:
            scale -= 1
        if bitmap_font.text_width(caption, scale) <= limit:
            return caption, scale
        trimmed = caption
        while trimmed and bitmap_font.text_width(trimmed + "..", scale) > limit:
            trimmed = trimmed[:-1]
        return trimmed.rstrip() + "..", scale

    def _ledger_caption(self, scene_ir: Dict) -> str:
        """从账本事件流生成一行字幕。"""
        events = scene_ir.get("events") or []
        counts: Dict[str, int] = {}
        bonds = 0
        for event in events:
            action = event.get("action")
            if action:
                counts[action] = counts.get(action, 0) + 1
            interact = event.get("interact") or {}
            if action == "socialize" and interact.get("partner"):
                bonds += 1
        if not counts:
            return ""
        parts = ["{0} {1}".format(a, counts[a]) for a in sorted(counts)]
        line = "  ".join(parts)
        if bonds:
            line += "  |  bonds {0}".format(bonds)
        # 报**最低需求的均值**而不是全局最小值：最小值常年贴着 0，
        # 是个没有信息量的数字；均值才反映"世界整体缺什么"。
        averages: Dict[str, List[float]] = {}
        for entity in scene_ir.get("entities") or []:
            for key, value in (entity.get("needs") or {}).items():
                averages.setdefault(key, []).append(float(value))
        if averages:
            worst = min(sorted(averages), key=lambda k: sum(averages[k]) / len(averages[k]))
            values = averages[worst]
            line += "  |  low {0} {1:.2f}".format(
                worst, sum(values) / len(values))
        return line

    # ---- 相机：声明即实现 ----

    def _resolve_view_ir(self, scene_ir: Dict, width: int, height: int) -> Dict:
        """把 scene_ir.camera 解析成 (center_x, center_y, rotation, scale)。

        四种 mode 全部实装；遇到未知 mode 直接抛错，不做静默降级。
        旋转角只由 tick 决定 → 确定性，且与墙钟无关。
        """
        camera = scene_ir.get("camera") or {}
        mode = camera.get("mode")
        entities = {e.get("id"): e for e in (scene_ir.get("entities") or [])}
        tick = scene_ir.get("tick") or 0

        cx, cy, rot = 0.0, 0.0, 0.0
        origin = camera.get("origin") or [0.0, 0.0]
        cx, cy = float(origin[0]), float(origin[1])

        # "auto" = 取字典序最小的实体（确定性，且不把具体身份写进导演层）
        target = camera.get("target_soul")
        if target == "auto":
            target = sorted(entities)[0] if entities else None

        if mode == "static":
            pass
        elif mode == "follow":
            if target in entities:
                pos = entities[target]["position"]
                cx, cy = float(pos[0]), float(pos[1])
        elif mode == "orbit":
            if target in entities:
                pos = entities[target]["position"]
                cx, cy = float(pos[0]), float(pos[1])
            period = float(camera.get("period_ticks", 300))
            rot = 2.0 * math.pi * (float(tick) % max(1.0, period)) / max(1.0, period)
        elif mode == "aoi":
            radius = float(camera.get("radius", 10.0))
            scale_fit = (width / 2.0) / max(1e-6, (TW2 * max(1.0, radius)))
            return {"cx": cx, "cy": cy, "rot": rot, "scale": scale_fit}
        else:
            raise ValueError(
                f"unsupported camera mode '{mode}' "
                f"(expected static|follow|orbit|aoi)"
            )

        return {"cx": cx, "cy": cy, "rot": rot,
                "scale": float(camera.get("zoom", 1.0))}

    def _project(self, px: float, py: float, pz: float, view: Dict,
                 width: int, height: int) -> Tuple[int, int]:
        """世界坐标 → 屏幕坐标（2:1 等距 + 可选旋转 + 缩放）。"""
        dx, dy = px - view["cx"], py - view["cy"]
        if view["rot"]:
            c, s = math.cos(view["rot"]), math.sin(view["rot"])
            rx, ry = dx * c - dy * s, dx * s + dy * c
        else:
            rx, ry = dx, dy
        scale = view["scale"]
        sx = width / 2.0 + (rx - ry) * TW2 * scale
        sy = height * 0.55 + (rx + ry) * TH2 * scale - pz * TH2 * Z_SCALE * scale
        return int(sx), int(sy)

    # ---- 绘制 ----

    def _draw_sky(self, screen: pygame.Surface, width: int, height: int):
        top, bot = PALETTE["sky_top"], PALETTE["sky_bot"]
        horizon = int(height * 0.62)
        for y in range(horizon):
            t = y / max(1, horizon)
            color = tuple(int(a + (b - a) * t) for a, b in zip(top, bot))
            pygame.draw.line(screen, color, (0, y), (width, y))
        pygame.draw.rect(screen, PALETTE["ground_bg"],
                         (0, horizon, width, height - horizon))

    def _draw_island(self, screen: pygame.Surface, view: Dict,
                     width: int, height: int):
        """等距菱形岛：外框 + 每 4 格一条网格线（3600 个菱形太慢，取稀疏线）。"""
        half = self.world_size / 2.0
        corners_world = [(-half, -half), (half, -half), (half, half), (-half, half)]
        corners = [self._project(x, y, 0.0, view, width, height)
                   for x, y in corners_world]
        pygame.draw.polygon(screen, PALETTE["grass"], corners)

        step = 4.0
        n = int(self.world_size / step)
        for i in range(n + 1):
            g = -half + i * step
            a = self._project(g, -half, 0.0, view, width, height)
            b = self._project(g, half, 0.0, view, width, height)
            c = self._project(-half, g, 0.0, view, width, height)
            d = self._project(half, g, 0.0, view, width, height)
            pygame.draw.line(screen, PALETTE["grass_line"], a, b, 1)
            pygame.draw.line(screen, PALETTE["grass_line"], c, d, 1)

    def _draw_agents(self, screen: pygame.Surface, entities: List[Dict],
                     view: Dict):
        # 先画影子：保证确定性绘制顺序（按实体 id 字典序）
        ordered = sorted(entities, key=lambda e: e.get("id") or "")
        for entity in ordered:
            px, py, pz = entity.get("position") or [0.0, 0.0, 0.0]
            sx, sy = self._project(px, py, 0.0, view, screen.get_width(),
                                   screen.get_height())
            shadow_w = max(4, int(7 * view["scale"]))
            pygame.draw.ellipse(screen, PALETTE["shadow"],
                                (sx - shadow_w, sy - shadow_w // 2,
                                 shadow_w * 2, shadow_w))

        for entity in ordered:
            px, py, pz = entity.get("position") or [0.0, 0.0, 0.0]
            sx, sy = self._project(px, py, pz, view, screen.get_width(),
                                   screen.get_height())
            body_h = max(6, int(14 * view["scale"]))
            body_w = max(4, int(8 * view["scale"]))
            color = self._soul_color(entity)
            pygame.draw.rect(screen, color,
                             (sx - body_w // 2, sy - body_h, body_w, body_h))
            pygame.draw.circle(screen, PALETTE["ink"], (sx, sy), 1)
            self._draw_need_bar(screen, entity.get("needs", {}), sx, sy - body_h - 8,
                                body_w)

    def _draw_need_bar(self, screen: pygame.Surface, needs: Dict,
                       sx: int, sy: int, width: int):
        """需求条：只画最紧迫一层的长度，颜色由紧迫度决定（内容驱动，非哈希）。"""
        if not needs:
            return
        key = sorted(needs)[0]
        lowest = min(needs.values()) if needs else 1.0
        bar_w = max(width, 10)
        filled = int(bar_w * max(0.0, min(1.0, lowest)))
        pygame.draw.rect(screen, (40, 40, 55), (sx - bar_w // 2, sy, bar_w, 3))
        color = (238, 90, 90) if lowest < 0.3 else (
            (238, 196, 80) if lowest < 0.6 else (96, 222, 110))
        pygame.draw.rect(screen, color, (sx - bar_w // 2, sy, filled, 3))

    def _soul_color(self, entity: Dict) -> Tuple[int, int, int]:
        """身份色：直接取 Scene IR 里的调色板（其来源是账本锚定的外观资产）。

        IR 没有调色板时，用实体 id 的内容派生确定色 —— 与旧实现同口径，
        但不再依赖渲染器内部 assets，渲染层只消费 IR。
        """
        palette = (entity.get("identity") or {}).get("palette") or []
        if palette:
            hex_color = sorted(palette)[0]
            return (
                int(hex_color[1:3], 16),
                int(hex_color[3:5], 16),
                int(hex_color[5:7], 16),
            )
        digest = hashlib.sha256(str(entity.get("id", "")).encode("utf-8")).digest()
        return (128 + digest[0] % 96, 128 + digest[1] % 96, 128 + digest[2] % 96)
