"""第 0 层：身份根（Identity Root）。

主身份密钥对 + Shamir 分片托管。宪法锚点 soul_hash = SHA-256(主身份公钥) 不变。
主私钥仅在创世瞬间存在，随后立即分片并清除明文。
日常登录使用设备凭证（见 credentials.py），不触碰主私钥。
"""

from . import keys


class IdentityRoot:
    """主身份密钥对 + Shamir 分片托管。

    生成后主私钥立即分片（threshold-of-num_shares），明文主私钥被清除。
    恢复时需凑齐 threshold 份分片重建。
    """

    def __init__(self, threshold: int = 3, num_shares: int = 5):
        if not (1 <= threshold <= num_shares):
            raise ValueError("threshold must satisfy 1 <= threshold <= num_shares")
        self.threshold = threshold
        self.num_shares = num_shares
        self._master_pubkey = None
        self._shares = []  # [(x, y), ...]

    @property
    def master_pubkey(self) -> bytes:
        if self._master_pubkey is None:
            raise RuntimeError("identity root not generated")
        return self._master_pubkey

    @property
    def soul_hash(self) -> str:
        return keys.derive_soul_hash_from_pubkey(self.master_pubkey)

    @property
    def shares(self) -> list:
        """分片列表（应分别托管给独立方，勿集中保存）。"""
        return list(self._shares)

    def generate(self) -> bytes:
        """生成主身份密钥对并分片。返回主身份公钥。明文主私钥立即清除。"""
        kp = keys.generate_user_keypair()
        self._master_pubkey = kp["pubkey"]
        self._shares = keys.shamir_split(kp["secret"], self.threshold, self.num_shares)
        # 明文主私钥不保留：分片即唯一恢复途径
        return self._master_pubkey

    def recover(self, shares) -> bytes:
        """由 threshold 份分片重建主私钥。调用方负责立即使用并清除。"""
        if len(shares) < self.threshold:
            raise ValueError(
                "insufficient shares: need %d, got %d" % (self.threshold, len(shares))
            )
        return keys.shamir_combine(shares[: self.threshold])
