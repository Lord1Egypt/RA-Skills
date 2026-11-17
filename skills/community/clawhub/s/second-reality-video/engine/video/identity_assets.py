"""Identity assets: soul_hash → appearance embedding (ledger-anchored)."""

import hashlib
import json
from typing import Dict, Optional
from pathlib import Path


class IdentityAssetRegistry:
    """Registry mapping soul_hash to AppearanceAsset.
    
    In production, this would be anchored in HistoryLedger.
    For Phase 0, it's an in-memory registry with JSON persistence.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self._assets: Dict[str, Dict] = {}
        self.storage_path = storage_path
        
        if storage_path and Path(storage_path).exists():
            self._load(storage_path)
    
    def register(self, soul_hash: str, asset: Dict) -> str:
        """Register an appearance asset for a soul.
        
        Args:
            soul_hash: Unique soul identifier
            asset: AppearanceAsset dict with ref_images, embedding, palette, seed
            
        Returns:
            Asset hash (for ledger anchoring)
        """
        # Compute asset hash
        content = json.dumps(asset, sort_keys=True, ensure_ascii=False)
        asset_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Store with metadata
        self._assets[soul_hash] = {
            "asset": asset,
            "asset_hash": asset_hash,
        }
        
        if self.storage_path:
            self._save(self.storage_path)
        
        return asset_hash
    
    def get(self, soul_hash: str) -> Optional[Dict]:
        """Get appearance asset for a soul.
        
        Args:
            soul_hash: Unique soul identifier
            
        Returns:
            AppearanceAsset dict or None
        """
        entry = self._assets.get(soul_hash)
        return entry["asset"] if entry else None
    
    def get_hash(self, soul_hash: str) -> Optional[str]:
        """Get asset hash for audit verification.
        
        Args:
            soul_hash: Unique soul identifier
            
        Returns:
            Asset SHA-256 hash or None
        """
        entry = self._assets.get(soul_hash)
        return entry["asset_hash"] if entry else None
    
    def verify_persistence(self, soul_hash: str, expected_hash: str) -> bool:
        """Verify that a soul's asset hasn't changed (identity persistence).
        
        Args:
            soul_hash: Unique soul identifier
            expected_hash: Expected asset hash from manifest
            
        Returns:
            True if hashes match
        """
        actual_hash = self.get_hash(soul_hash)
        return actual_hash == expected_hash
    
    def _save(self, path: str):
        """Save registry to JSON."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self._assets, f, ensure_ascii=False, indent=2)
    
    def _load(self, path: str):
        """Load registry from JSON."""
        with open(path, 'r', encoding='utf-8') as f:
            self._assets = json.load(f)
    
    def to_dict(self) -> Dict:
        """Serialize entire registry."""
        return self._assets


def build_assets(souls, genesis_seed: int) -> Dict[str, Dict]:
    """为给定灵魂集合构建外观资产。

    这是身份恒定性的**唯一来源**：生产链路与复验链路必须调用同一函数，
    否则像素层会因造色不同而分歧（此坑已在复验中实测踩中过）。
    """
    return {soul: generate_demo_asset(soul, seed=genesis_seed)
            for soul in sorted(souls)}


def assets_digest(assets: Dict[str, Dict]) -> str:
    """资产集合摘要 —— 跨镜头/跨分支比对身份是否恒定（第 29 维判据）。"""
    blob = json.dumps(assets, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def generate_demo_asset(soul_hash: str, seed: int = 42) -> Dict:
    """Generate a deterministic demo appearance asset for testing.
    
    Args:
        soul_hash: Soul identifier
        seed: Random seed for deterministic generation
        
    Returns:
        AppearanceAsset dict
    """
    import random
    # 注意：不能用内置 hash() —— str 的 hash 受 PYTHONHASHSEED 随机化，
    # 跨进程不稳定，会直接破坏渲染的像素级复现。
    soul_seed = int.from_bytes(
        hashlib.sha256(soul_hash.encode("utf-8")).digest()[:8], "big"
    )
    rng = random.Random(seed + soul_seed)
    
    # Generate deterministic palette
    palette = [
        f"#{rng.randint(0, 255):02x}{rng.randint(0, 255):02x}{rng.randint(0, 255):02x}"
        for _ in range(3)
    ]
    
    return {
        "soul_hash": soul_hash,
        "embedding": [rng.random() for _ in range(16)],  # 16-dim embedding
        "palette": palette,
        "seed": seed,
        "ref_images": [],  # Would contain reference image paths in production
    }
