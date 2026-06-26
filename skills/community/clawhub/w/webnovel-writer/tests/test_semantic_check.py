"""测试 semantic_check.py"""
import tempfile
from pathlib import Path


def _write_chapter(directory, num, content):
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / f"第{num:03d}章.md"
    f.write_text(content, encoding="utf-8")


def test_tokenize_fallback():
    """无jieba时降级到按字分词"""
    import scripts.semantic_check as sc
    if sc.HAS_JIEBA:
        tokens = sc.tokenize("他走进了房间")
        assert len(tokens) > 0
    else:
        tokens = sc.tokenize("测试文本")
        assert tokens == list("测试文本")


def test_similarity():
    import scripts.semantic_check as sc
    # 完全相同
    assert sc.similarity("测试文本", "测试文本") == 1.0
    # 完全不同
    result = sc.similarity("abcdefg", "hijklmn")
    assert result < 0.5
    # 空
    assert sc.similarity("", "test") == 0.0


def test_find_semantic_duplicates():
    import scripts.semantic_check as sc

    with tempfile.TemporaryDirectory() as tmpdir:
        # 两章内容高度相似
        content = "这是第一段内容。" * 10 + "\n" + "相似的段落内容在这里。" * 10
        _write_chapter(Path(tmpdir), 1, content)
        _write_chapter(Path(tmpdir), 2, content)

        chapters = [(1, str(Path(tmpdir) / "第001章.md"), "第001章.md"),
                    (2, str(Path(tmpdir) / "第002章.md"), "第002章.md")]
        issues = sc.find_semantic_duplicates(chapters, threshold=0.5)
        # 应该检测到重复
        assert len(issues) > 0


def test_find_no_duplicates():
    import scripts.semantic_check as sc

    with tempfile.TemporaryDirectory() as tmpdir:
        _write_chapter(Path(tmpdir), 1, "完全不同的内容第一段。" * 20)
        _write_chapter(Path(tmpdir), 2, "另外完全不相关的第二段。" * 20)

        chapters = [(1, str(Path(tmpdir) / "第001章.md"), "第001章.md"),
                    (2, str(Path(tmpdir) / "第002章.md"), "第002章.md")]
        issues = sc.find_semantic_duplicates(chapters, threshold=0.9)
        assert len(issues) == 0


def test_extract_keywords():
    import scripts.semantic_check as sc
    result = sc.extract_keywords("这是一个测试文本用来测试关键词提取功能")
    assert len(result) > 0
    # 返回 (word, weight) 元组
    assert len(result[0]) == 2


def test_named_entity_scan():
    import scripts.semantic_check as sc
    result = sc.named_entity_scan("张三去了北京")
    assert "mode" in result
    if sc.HAS_JIEBA:
        assert "entities" in result
