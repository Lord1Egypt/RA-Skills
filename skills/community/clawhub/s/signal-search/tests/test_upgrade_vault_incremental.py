import vault


def test_incremental_report(tmp_path):
    p = vault.init_vault(str(tmp_path), "q", "L2")
    for i in range(1, 101):
        vault.write_item(p, i, "q", {"url": f"https://e.com/{i}", "text": f"证据{i}"})
    vault.render_report(p, sources=[{"url": f"https://e.com/{i}"} for i in range(1, 101)])
    # 增量：加 1 个新 item，再 render incremental（不应重复已有）
    vault.write_item(p, 101, "q", {"url": "https://e.com/101", "text": "证据101"})
    r2 = vault.render_report(
        p, sources=[{"url": f"https://e.com/{i}"} for i in range(1, 102)], incremental=True
    )
    assert "证据101" in r2
    assert r2.count("## 101-") == 1  # 新 item 不重复
    assert "https://e.com/1" in r2
    # 幂等：再 incremental 同 101 不翻倍
    r3 = vault.render_report(
        p, sources=[{"url": f"https://e.com/{i}"} for i in range(1, 102)], incremental=True
    )
    assert r3.count("## 101-") == 1
