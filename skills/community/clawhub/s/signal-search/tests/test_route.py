import route


def test_default_l1():
    assert route.classify_tier("推荐一部电影")[0] == "L1"


def test_l0_fact():
    assert route.classify_tier("珠穆朗玛峰海拔多少")[0] == "L0"
    assert route.classify_tier("2026-08-07 是星期几")[0] == "L0"


def test_l2_compare():
    assert route.classify_tier("对比 Redis 与 Memcached 作为缓存")[0] == "L2"
    assert route.classify_tier("为什么推荐系统容易形成信息茧房")[0] == "L2"


def test_l3_research():
    assert route.classify_tier("调研 agentic search 前沿方案")[0] == "L3"


def test_explicit_override():
    tier, reason = route.classify_tier("随便", {"required_tier": "L3"})
    assert tier == "L3" and reason == "用户指定"


def test_parse_override():
    q, t = route.parse_override("/signal L3 调研某问题")
    assert q == "调研某问题" and t == "L3"
    q2, t2 = route.parse_override("普通查询")
    assert q2 == "普通查询" and t2 is None


def test_routing_memory_hits_golden():
    # 预热集的典型边界查询应命中缓存并给出预期档位
    assert route.classify_tier("TCP 和 UDP 的核心区别")[0] == "L0"
    assert route.classify_tier("谁发明了万维网")[0] == "L1"
    assert route.classify_tier("调研小微企业所得税优惠")[0] == "L2"
