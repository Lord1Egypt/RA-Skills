"""RenderTier abstract interface."""

from abc import ABC, abstractmethod
from typing import Dict, Protocol


class RenderContext:
    """Context passed to renderer for frame generation."""
    
    def __init__(self, shot: Dict, frame_index: int, tick: int, sub: int):
        self.shot = shot
        self.frame_index = frame_index
        self.tick = tick
        self.sub = sub
        self.camera = shot.get("camera", {})
        self.framing = shot.get("framing", {})
        self.overlay = shot.get("overlay", {})


class RenderTier(ABC):
    """Abstract interface for render tiers (R1 deterministic / R2 frame).

    输入合同（审计维度 31 `render_is_frame_independent` 的对象）：
    像素入口固定为 `render_ir(scene_ir)` —— **单帧** Scene IR，
    不接受任何跨帧上下文。子类不得引入 `prev_frames` 之类的参数；
    违规会让架构退化成生成式视频模型，跨帧漂移与身份丢失会重新回来。
    """

    # 渲染层输入合同标识（写进 manifest 与 provenance）
    INPUT_CONTRACT = "scene_ir"

    @property
    @abstractmethod
    def tier_id(self) -> str:
        """Return tier identifier (e.g., 'R1-deterministic', 'R2-frame')."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return renderer/model version hash."""
        pass

    @abstractmethod
    def render_ir(self, scene_ir: Dict) -> bytes:
        """渲染**单帧** Scene IR，返回未压缩 RGB24 字节。

        这是渲染层唯一被允许产生像素的入口，且**不接受任何跨帧上下文**
        （无 prev_frames / 无上一帧像素 / 无时间聚合量）。
        """
        pass

    @abstractmethod
    def render(self, frame_state: Dict, shot: Dict, ctx: RenderContext) -> bytes:
        """渲染单帧，返回**未压缩 RGB24 字节**（宽×高×3）。

        返回未压缩缓冲而非 PNG：编码走 ffmpeg rawvideo 管道，
        避免逐帧落盘与容器级不确定性。

        这是**兼容入口**：把旧的 FrameState 形态转译成 Scene IR 后交给
        `render_ir`。它同样不引入跨帧状态。

        Args:
            frame_state: FrameState dict from state_feed
            shot: Shot dict from ShotGraph
            ctx: RenderContext with camera/framing info

        Returns:
            Frame as raw RGB24 bytes
        """
        pass

    @abstractmethod
    def provenance(self) -> Dict:
        """Return provenance information for manifest.

        Returns:
            Dict with code_hash, model_hash, seed, hardware info
        """
        pass
