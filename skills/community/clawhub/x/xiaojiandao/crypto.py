from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass

try:
    from Crypto.Cipher import AES  # type: ignore
except ImportError:
    # 允许在没有安装依赖时加载模块，但在调用时报错
    AES = None


def _pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def _pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or (len(data) % block_size) != 0:
        raise ValueError("Invalid PKCS7 data length")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid PKCS7 padding")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding bytes")
    return data[:-pad_len]


def get_aes_key_by_pkg(pkgname: str) -> str:
    # 与 `scripts/hook_bgm_client.py` 保持一致
    mapping = {
        "com.biyi.wscissors": "wd.srv.yz.2025!@",
        "com.biyi.mscissors": "bz.srv.yz.2025!@",
    }
    return mapping.get(pkgname, "biyi#def!918.dyj")


def get_iv_by_pkg(pkgname: str, unix_ms: int) -> str:
    if not pkgname:
        raise ValueError("pkgname is empty")
    if unix_ms < 50 * 86400 * 365 * 1000:
        raise ValueError("unix_ms is less than 2020")
    sign = f"{pkgname}{unix_ms}"
    md5_hex = hashlib.md5(sign.encode("utf-8")).hexdigest()
    return md5_hex[8:24]


@dataclass(frozen=True)
class AesContext:
    pkgname: str

    def _ensure_aes(self):
        if AES is None:
            raise RuntimeError("缺少依赖：请先执行 `pip install pycryptodome`")

    def encrypt_to_base64(self, text: str, *, unix_ms: int) -> str:
        self._ensure_aes()
        key = get_aes_key_by_pkg(self.pkgname)
        iv = get_iv_by_pkg(self.pkgname, unix_ms)
        if len(key) != 16 or len(iv) != 16:
            raise ValueError(f"key/iv length must be 16 (key={len(key)}, iv={len(iv)})")
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        padded = _pkcs7_pad(text.encode("utf-8"), 16)
        encrypted = cipher.encrypt(padded)
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt_base64(self, b64_text: str, *, unix_ms: int) -> str:
        self._ensure_aes()
        key = get_aes_key_by_pkg(self.pkgname)
        iv = get_iv_by_pkg(self.pkgname, unix_ms)
        if len(key) != 16 or len(iv) != 16:
            raise ValueError(f"key/iv length must be 16 (key={len(key)}, iv={len(iv)})")
        encrypted = base64.b64decode(b64_text.encode("utf-8"))
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        padded = cipher.decrypt(encrypted)
        plain = _pkcs7_unpad(padded, 16)
        return plain.decode("utf-8")

