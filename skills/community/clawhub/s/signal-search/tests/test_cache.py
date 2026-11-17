import os
import tempfile

import cache


def test_cache_enabled_roundtrip():
    tmp = tempfile.mkdtemp()
    cfg = {"cache": {"enabled": True, "ttl_minutes": 10, "dir": os.path.join(tmp, ".cache/")}}
    c = cache.Cache(cfg)
    c.put("k", {"v": 1})
    assert c.get("k") == {"v": 1}
    # 缺失返回 None
    assert c.get("missing") is None


def test_cache_disabled_noop():
    c = cache.Cache({"cache": {"enabled": False}})
    c.put("k", 1)
    assert c.get("k") is None
