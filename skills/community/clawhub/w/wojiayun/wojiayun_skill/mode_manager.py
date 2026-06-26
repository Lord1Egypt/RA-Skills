"""
运行环境配置
"""

import json
import os

try:
    from .crypto_utils import encrypt_value, decrypt_value
except ImportError:
    from crypto_utils import encrypt_value, decrypt_value


class _RuntimeProfile:
    """运行环境配置"""
    
    _CFG_FILE = "e:\\workbuddy\\wy\\.app_cfg"
    
    _S1 = "A"  # 标识1
    _S2 = "B"  # 标识2
    
    _DEFAULT = _S2
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ready = False
        return cls._instance
    
    def __init__(self):
        if self._ready:
            return
        self._s = self._read()
        self._ready = True
    
    def _read(self) -> str:
        if not os.path.exists(self._CFG_FILE):
            return self._DEFAULT
        try:
            with open(self._CFG_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
            v = d.get("v", "")
            if not v:
                return self._DEFAULT
            r = decrypt_value(v)
            if r == self._S1:
                return self._S1
            return self._DEFAULT
        except Exception:
            return self._DEFAULT
    
    @property
    def verbose(self) -> bool:
        return self._s == self._S1
    
    @property
    def strict(self) -> bool:
        return self._s == self._S2
    
    def reload(self):
        self._s = self._read()
    
    def apply(self, s: str):
        if s not in (self._S1, self._S2):
            raise ValueError(f"Invalid: {s}")
        v = encrypt_value(s)
        with open(self._CFG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"v": v}, f, ensure_ascii=False)
        self._s = s
        
        # 切换到生产模式时，自动构建混淆版本
        if s == self._S2:
            self._build_production()
    
    def _build_production(self):
        """构建生产版本（混淆代码）"""
        try:
            from .obfuscator import CodeObfuscator
            CodeObfuscator.build_production()
        except Exception as e:
            pass  # 静默处理，不影响主流程
    
    def cfg(self) -> dict:
        if self._s == self._S1:
            return {"log": 1, "mask": 0, "guard": 0}
        return {"log": 0, "mask": 1, "guard": 1}


_rp = None


def _get_rp():
    global _rp
    if _rp is None:
        _rp = _RuntimeProfile()
    return _rp


def _verbose() -> bool:
    return _get_rp().verbose


def _strict() -> bool:
    return _get_rp().strict


def _log(*a, **kw):
    if _strict():
        return
    print(*a, **kw)


def _mask(t: str) -> str:
    if _verbose():
        return t
    import re
    for p, r in [
        (r'[a-f0-9]{64}', '***'),
        (r'Bearer\s+[A-Za-z0-9\-_\.]+', '***'),
        (r'gAAAAA[A-Za-z0-9\-_]+', '***'),
    ]:
        t = re.sub(p, r, t, flags=re.IGNORECASE)
    return t


if __name__ == "__main__":
    p = _get_rp()
    print(f"default: verbose={p.verbose}, strict={p.strict}, cfg={p.cfg()}")
    
    p.apply("A")
    p.reload()
    print(f"after A: verbose={p.verbose}, strict={p.strict}, cfg={p.cfg()}")
    _log("this prints in verbose mode")
    
    p.apply("B")
    p.reload()
    print(f"after B: verbose={p.verbose}, strict={p.strict}, cfg={p.cfg()}")
    _log("this will NOT print")
    
    with open(_RuntimeProfile._CFG_FILE, 'r') as f:
        print(f"file: {f.read()}")
