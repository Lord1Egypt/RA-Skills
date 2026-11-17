import json
import os
import content_db as cdb


def test_resolve_data_root_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    assert cdb.resolve_data_root() == str(tmp_path)


def test_dump_and_parse_frontmatter_roundtrip():
    meta = {
        "id": "2026-07-27-maotai",
        "created": "2026-07-27",
        "platform": ["抖音", "B站"],
        "tags": ["白酒", "财报"],
        "title": "茅台跌停:压垮它的不是股价",
        "series": "",
        "status": "pending",
        "metrics": {"views": None, "likes": None},
    }
    text = cdb.dump_frontmatter(meta) + "\n正文台词第一句\n"
    parsed, body = cdb.parse_frontmatter(text)
    assert parsed["platform"] == ["抖音", "B站"]
    assert parsed["tags"] == ["白酒", "财报"]
    assert parsed["metrics"] == {"views": None, "likes": None}
    assert parsed["title"] == "茅台跌停:压垮它的不是股价"
    assert parsed["series"] == ""
    assert "正文台词第一句" in body


def test_slugify_handles_chinese_and_punct():
    # 所有非词字符(标点、空格)各自压成单个 dash,首尾 dash 去掉
    assert cdb.slugify("茅台跌停!复盘 2026") == "茅台跌停-复盘-2026"


def test_archive_creates_file_and_index(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    import archive_content as ac
    path = ac.archive(
        topic="茅台跌停复盘", title="茅台跌停!三个信号",
        script_body="开头钩子...", platform=["抖音"], tags=["白酒"],
        created="2026-07-27",
    )
    assert os.path.isfile(path)
    index = json.load(open(os.path.join(str(tmp_path), "index.json"), encoding="utf-8"))
    ids = [e["id"] for e in index["entries"]]
    assert "2026-07-27-茅台跌停复盘" in ids
    entry = index["entries"][0]
    assert entry["status"] == "pending"
    assert entry["title"] == "茅台跌停!三个信号"


def test_archive_appends_series_member(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    import archive_content as ac
    ac.archive(topic="第一期", title="T1", script_body="a",
               platform=["抖音"], tags=[], series="涨停复盘", created="2026-07-27")
    ac.archive(topic="第二期", title="T2", script_body="b",
               platform=["抖音"], tags=[], series="涨停复盘", created="2026-07-28")
    series_file = os.path.join(str(tmp_path), "series", cdb.slugify("涨停复盘") + ".md")
    meta, _ = cdb.parse_frontmatter(open(series_file, encoding="utf-8").read())
    assert len(meta["members"]) == 2


def test_archive_duplicate_id_gets_suffix(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    import archive_content as ac
    p1 = ac.archive(topic="同题", title="T", script_body="a",
                    platform=["抖音"], tags=[], created="2026-07-27")
    p2 = ac.archive(topic="同题", title="T2", script_body="b",
                    platform=["抖音"], tags=[], created="2026-07-27")
    assert p1.endswith("2026-07-27-同题.md")
    assert p2.endswith("2026-07-27-同题-2.md")
    import query_db as q
    assert len(q.load_entries()) == 2  # both archived, index has both


def _seed(tmp_path, monkeypatch):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    import archive_content as ac
    ac.archive(topic="茅台跌停复盘", title="茅台三个信号", script_body="a",
               platform=["抖音"], tags=["白酒"], series="复盘", created="2026-07-27")
    ac.archive(topic="宁德时代估值", title="宁王还能买吗", script_body="b",
               platform=["B站"], tags=["新能源"], series="复盘", created="2026-07-28")


def test_search_matches_topic_and_tags(monkeypatch, tmp_path):
    _seed(tmp_path, monkeypatch)
    import query_db as q
    hits = q.search("白酒")
    assert len(hits) == 1 and hits[0]["topic"] == "茅台跌停复盘"


def test_list_series_sorted(monkeypatch, tmp_path):
    _seed(tmp_path, monkeypatch)
    import query_db as q
    members = q.list_series("复盘")
    assert [m["created"] for m in members] == ["2026-07-27", "2026-07-28"]


def test_top_by_views(monkeypatch, tmp_path):
    _seed(tmp_path, monkeypatch)
    import update_metrics as um
    um.update("2026-07-28-宁德时代估值", {"views": 9000}, publish_date="2026-07-29")
    um.update("2026-07-27-茅台跌停复盘", {"views": 100}, publish_date="2026-07-28")
    import query_db as q
    ranked = q.top(2, by="views")
    assert ranked[0]["id"] == "2026-07-28-宁德时代估值"


def test_load_entries_rebuilds_when_index_missing(monkeypatch, tmp_path):
    _seed(tmp_path, monkeypatch)
    os.remove(os.path.join(str(tmp_path), "index.json"))
    import query_db as q
    assert len(q.load_entries()) == 2


def test_end_to_end(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTENT_DB_ROOT", str(tmp_path))
    import archive_content as ac
    import query_db as q
    import update_metrics as um
    # 1. 存档两条同系列内容
    ac.archive(topic="第一期茅台", title="T1", script_body="稿1",
               platform=["抖音"], tags=["白酒"], series="复盘", created="2026-07-27")
    ac.archive(topic="第二期宁王", title="T2", script_body="稿2",
               platform=["B站"], tags=["新能源"], series="复盘", created="2026-07-28")
    # 2. 查重命中
    assert len(q.search("茅台")) == 1
    # 3. 系列列出两期
    assert len(q.list_series("复盘")) == 2
    # 4. 回填数据后 status=published 且排序生效
    um.update("2026-07-27-第一期茅台", {"views": 500}, publish_date="2026-07-28")
    ranked = q.top(1, by="views")
    assert ranked[0]["id"] == "2026-07-27-第一期茅台"
    assert ranked[0]["status"] == "published"


def test_query_absent_data_root_returns_empty(monkeypatch, tmp_path):
    missing = tmp_path / "never-created"
    monkeypatch.setenv("CONTENT_DB_ROOT", str(missing))
    import query_db as q
    assert q.search("anything") == []
    assert q.list_series("任意系列") == []
    assert q.top(5, by="views") == []
    assert not missing.exists()  # read must not create the dir
