"""离线烘焙资产：把模型产出的美术资产固化成仓库常量。

为什么要烘焙
------------
闭源视频 / 图像模型不能进渲染层（版本会漂移，复现锚会失效）；
但它们可以进**资产生产**环节。把生成结果落盘、哈希、提交，渲染器只读常量，
像素层仍然逐字节可复现 —— 这正是 Tier 2 的定义。

产物
----
    <out_dir>/baked_assets.json          # 资产本体（确定性 JSON）
    <out_dir>/baked_assets.manifest.json # 逐资产 sha256 + 集合 digest

校验
----
`load_baked_assets(verify=True)` 会重算 digest 与逐资产哈希；
任何手改、截断、换文件都会抛 ValueError，不静默通过。
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional

SCHEMA = "second-reality.baked-assets/1"
ASSETS_FILE = "baked_assets.json"
MANIFEST_FILE = "baked_assets.manifest.json"


def _canonical(obj) -> str:
    # 与 identity_assets.assets_digest 保持同一序列化口径（默认分隔符），
    # 否则同一份资产会得到两个不同 digest，attest 会误判。
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def asset_digest(asset: Dict) -> str:
    return hashlib.sha256(_canonical(asset).encode("utf-8")).hexdigest()


def assets_digest(assets: Dict[str, Dict]) -> str:
    """集合摘要只覆盖 soul → asset 的映射，与落盘格式无关。"""
    return hashlib.sha256(_canonical(assets).encode("utf-8")).hexdigest()


def bake_assets(assets: Dict[str, Dict], out_dir: str) -> Dict:
    """把资产写入 out_dir，并返回 manifest（含逐资产哈希）。"""
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)

    per_asset = {soul: asset_digest(asset) for soul, asset in sorted(assets.items())}
    manifest = {
        "schema": SCHEMA,
        "asset_count": len(assets),
        "digest": assets_digest(assets),
        "per_asset": per_asset,
    }

    (target / ASSETS_FILE).write_text(
        json.dumps({"schema": SCHEMA, "assets": assets},
                   ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8")
    (target / MANIFEST_FILE).write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8")
    return manifest


def load_baked_assets(out_dir: str, verify: bool = True) -> Dict[str, Dict]:
    """载入烘焙资产；verify=True 时逐项校验哈希。"""
    target = Path(out_dir)
    assets_path = target / ASSETS_FILE
    manifest_path = target / MANIFEST_FILE
    if not assets_path.exists() or not manifest_path.exists():
        raise FileNotFoundError(
            "baked assets missing: {0} / {1}".format(assets_path, manifest_path))

    payload = json.loads(assets_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = payload.get("assets") or {}

    if verify:
        if payload.get("schema") != SCHEMA or manifest.get("schema") != SCHEMA:
            raise ValueError("unexpected baked-assets schema")
        if assets_digest(assets) != manifest.get("digest"):
            raise ValueError("baked assets digest mismatch")
        for soul, expected in (manifest.get("per_asset") or {}).items():
            if soul not in assets:
                raise ValueError("baked asset missing: {0}".format(soul))
            if asset_digest(assets[soul]) != expected:
                raise ValueError("baked asset hash mismatch: {0}".format(soul))
    return assets


def asset_source(manifest: Optional[Dict]) -> str:
    """给 manifest 用的资产来源标签。"""
    if not manifest:
        return "derived-from-genesis"
    return "offline-baked:{0}".format(str(manifest.get("digest", ""))[:16])
