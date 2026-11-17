"""RenderManifest：渲染凭证 + 第三方复验。

分层复现口径（诚实边界条款）
----------------------------
- **状态层**：`content_digest` 序列 —— 确定性，可逐字节复验。
  （不含 `state_root`：其 Merkle 输入含 HLC 墙钟分量，跨运行不可能一致。）
- **像素层（R1）**：逐帧 sha256 序列 —— 确定性，可逐字节复验。
- **容器层**：mp4 sha256 —— 仅旁证，跨 ffmpeg 版本不保证一致。
- **像素层（R2 神经渲染）**：不可逐字节复现，只能「同权重/种子/硬件下可复现」，
  本 manifest 以 `model` 字段如实标注，不与 R1 混说。
"""

import hashlib
import json
import time
from typing import Dict, List, Optional
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives import serialization
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


class RenderManifest:
    """视频渲染凭证。字段分为「复现锚」「旁证」「边界声明」三类，不得混用。"""

    def __init__(self):
        self.data: Dict = {
            "version": "1.0",
            "created_at": "",
            "world_id": "",
            "genesis_seed": 0,
            "agent_count": 0,
            "tick_from": 0,
            "tick_to": 0,
            "ledger_range": {"from_block": "", "to_block": ""},
            # ---- 复现锚（确定性）----
            "content_digest_start": "",
            "content_digest_end": "",
            "frame_hashes_digest": "",
            "frame_count": 0,
            "video_sha256": "",
            "identity_assets_digest": "",
            "identity_assets_file": "",
            # ---- 旁证（非确定性，如实标注）----
            "state_root_start": "",
            "state_root_end": "",
            "state_root_note": "Merkle 输入含 HLC 墙钟分量，跨运行不一致，不作复现锚",
            "shot_graph_hash": "",
            "timebase": {"tps": 10, "fps": 30, "frames_per_tick": 3},
            "renderer": {},
            "model": None,
            # ---- 层级与合同（结构 / 像素分开写，不混说）----
            "scene_ir_digest": "",
            "scene_ir_file": "",
            "pixel_tier": {"id": "", "reproducibility": "", "note": ""},
            "asset_pipeline": {"kind": "", "digest": ""},
            "duration_s": 0.0,
            "frame_backing": {"total_frames": 0, "unbacked_frames": 0},
            # ---- 审计（真跑，不预置结论）----
            "audit": {"dimensions": 0, "verdict": "NOT_RUN", "summary": ""},
            # ---- 签名 ----
            "signer_pubkey": "",
            "signature": "",
        }

    # ---- world / 镜头 / 时基 ----

    def set_world_info(self, world_id: str, genesis_seed: int,
                       state_root_start: str = "", state_root_end: str = "",
                       ledger_from: str = "", ledger_to: str = ""):
        self.data["world_id"] = world_id
        self.data["genesis_seed"] = genesis_seed
        self.data["state_root_start"] = state_root_start
        self.data["state_root_end"] = state_root_end
        self.data["ledger_range"] = {"from_block": ledger_from, "to_block": ledger_to}

    def set_content_anchors(self, digest_start: str, digest_end: str,
                            frame_hashes_digest: str, frame_count: int):
        """设置确定性复现锚。"""
        self.data["content_digest_start"] = digest_start
        self.data["content_digest_end"] = digest_end
        self.data["frame_hashes_digest"] = frame_hashes_digest
        self.data["frame_count"] = frame_count

    def set_frame_backing(self, total_frames: int, unbacked_frames: int):
        """渲染守恒：无 state/content 背书的帧数必须为 0（对应第 30 维）。"""
        self.data["frame_backing"] = {
            "total_frames": total_frames,
            "unbacked_frames": unbacked_frames,
        }

    def set_shot_graph_hash(self, shot_hash: str):
        self.data["shot_graph_hash"] = shot_hash

    def set_world_params(self, agent_count: int, tick_from: int, tick_to: int):
        """记录重放世界所需的全部参数 —— 复验方据此独立重建，无需信任生产方。"""
        self.data["agent_count"] = agent_count
        self.data["tick_from"] = tick_from
        self.data["tick_to"] = tick_to

    def set_identity_assets(self, digest: str, registry_file: str = ""):
        """身份锚定：外观资产集合的摘要（第 29 维判据）。"""
        self.data["identity_assets_digest"] = digest
        self.data["identity_assets_file"] = registry_file

    def set_timebase(self, tps: int, fps: int):
        self.data["timebase"] = {"tps": tps, "fps": fps, "frames_per_tick": fps // tps}

    def set_renderer(self, renderer_provenance: Dict):
        self.data["renderer"] = renderer_provenance

    def set_model(self, model_provenance: Optional[Dict]):
        self.data["model"] = model_provenance

    def set_scene_ir(self, digest: str, file: str = ""):
        """结构层复现锚：整段 Scene IR 的摘要。"""
        self.data["scene_ir_digest"] = digest
        self.data["scene_ir_file"] = file

    def set_pixel_tier(self, tier_id: str, reproducibility: str, note: str = ""):
        """像素层可复现口径。R1=逐字节；R2=同权重/种子/硬件。"""
        self.data["pixel_tier"] = {
            "id": tier_id,
            "reproducibility": reproducibility,
            "note": note,
        }

    def set_asset_pipeline(self, kind: str, digest: str = ""):
        """资产来源：由创世参数派生，或离线烘焙后固化的常量。"""
        self.data["asset_pipeline"] = {"kind": kind, "digest": digest}

    def set_video_info(self, duration_s: float, video_hash: str):
        self.data["duration_s"] = duration_s
        self.data["video_sha256"] = video_hash

    def set_audit(self, dimensions: int, verdict: str, summary: str = ""):
        """写入**实际执行**的审计结果。不得由调用方编造 verdict。"""
        self.data["audit"] = {
            "dimensions": dimensions,
            "verdict": verdict,
            "summary": summary,
        }

    # ---- 签名 ----

    def set_signer(self, pubkey_hex: str):
        self.data["signer_pubkey"] = pubkey_hex

    def sign(self, private_key_bytes: Optional[bytes] = None):
        """签名。传入私钥时同时记录对应公钥，使 verify() 可独立完成。"""
        if not HAS_CRYPTO:
            raise RuntimeError(
                "cryptography package required for manifest signing: "
                "pip install cryptography"
            )
        if private_key_bytes is None:
            private_key = Ed25519PrivateKey.generate()
        else:
            private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)

        pubkey = private_key.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
        self.data["signer_pubkey"] = pubkey.hex()

        content = self._signable_content().encode()
        self.data["signature"] = private_key.sign(content).hex()

    def _signable_content(self) -> str:
        data_copy = dict(self.data)
        data_copy.pop("signature", None)
        data_copy.pop("created_at", None)   # 时间戳不可复现，排除在签名对象外
        return json.dumps(data_copy, sort_keys=True, ensure_ascii=False)

    def verify(self, public_key_bytes: Optional[bytes] = None) -> bool:
        """验签。默认使用 manifest 内记录的 signer_pubkey（无需外部输入）。"""
        if not HAS_CRYPTO:
            raise RuntimeError("cryptography package required for verification")
        if public_key_bytes is None:
            hex_key = self.data.get("signer_pubkey", "")
            if not hex_key:
                return False
            public_key_bytes = bytes.fromhex(hex_key)
        try:
            public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
            content = self._signable_content().encode()
            public_key.verify(bytes.fromhex(self.data["signature"]), content)
            return True
        except Exception:
            return False

    # ---- 落盘 ----

    def save(self, path: str):
        self.data["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"Manifest saved to {path}")

    @classmethod
    def load(cls, path: str) -> "RenderManifest":
        manifest = cls()
        with open(path, 'r', encoding='utf-8') as f:
            manifest.data = json.load(f)
        return manifest

    def to_dict(self) -> Dict:
        return dict(self.data)


def compute_video_hash(video_path: str) -> str:
    """mp4 容器哈希（旁证，非复现锚）。"""
    sha256 = hashlib.sha256()
    with open(video_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def deterministic_signing_key(genesis_seed: int) -> bytes:
    """由 genesis_seed 派生确定性的 Ed25519 私钥（32B）。

    Phase 0 用派生密钥，目的是让凭证可被第三方独立复算；
    生产环境必须改为真实身份密钥（system/keys.py 的 Passkey 链路）——
    本函数不是安全边界，manifest 内已如实标注。
    """
    material = f"nohn-manifest-signer|{genesis_seed}".encode("utf-8")
    return hashlib.sha256(material).digest()
