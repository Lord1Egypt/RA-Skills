from __future__ import annotations

import resource_hunter.precision_core as pc
from resource_hunter.cache import ResourceCache
from resource_hunter.cli import main as cli_main
from resource_hunter.common import parse_quality_tags
from resource_hunter.core import ResourceHunterEngine, SourceAdapter, parse_intent
from resource_hunter.models import SearchResult, SourceStatus


class FakeSource(SourceAdapter):
    def __init__(self, name: str, channel: str, priority: int, results: list[SearchResult]) -> None:
        self.name = name
        self.channel = channel
        self.priority = priority
        self._results = results

    def search(self, query, intent, limit, page, http_client):
        return list(self._results)


def test_title_core_extraction_for_tv_query():
    intent = parse_intent("Breaking Bad S01E01")
    assert intent.kind == "tv"
    assert intent.title_core == "breaking bad"
    assert intent.title_tokens == ["breaking", "bad"]


def test_remux_is_not_treated_as_4k():
    tags = parse_quality_tags("Oppenheimer 2023 1080p REMUX HDR")
    assert tags["resolution"] == "1080p"
    assert tags["pack"] == "remux"


def test_engine_ranks_exact_title_episode_above_episode_only(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)
    exact = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="Breaking Bad S01E01 Pilot 1080p WEB-DL",
        link_or_magnet="magnet:?xt=urn:btih:aaa",
        share_id_or_info_hash="aaa",
        seeders=12,
    )
    unrelated = SearchResult(
        channel="torrent",
        source="eztv",
        provider="magnet",
        title="Steel Ball Run S01E01 1080p WEB h264",
        link_or_magnet="magnet:?xt=urn:btih:bbb",
        share_id_or_info_hash="bbb",
        seeders=99,
    )
    engine.pan_sources = []
    engine.torrent_sources = [FakeSource("tpb", "torrent", 2, [exact]), FakeSource("eztv", "torrent", 1, [unrelated])]
    response = engine.search(parse_intent("Breaking Bad S01E01", explicit_kind="tv"), use_cache=False)
    assert response["results"][0]["title"].startswith("Breaking Bad")
    assert response["results"][0]["match_bucket"] == "exact_title_episode"
    weak = [item for item in response["results"] if item["title"].startswith("Steel Ball Run")][0]
    assert weak["match_bucket"] == "episode_only_match"


def test_degraded_sources_stay_enabled_but_rank_lower(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)
    stable = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="Oppenheimer 2023 2160p HDR",
        link_or_magnet="magnet:?xt=urn:btih:111",
        share_id_or_info_hash="111",
        seeders=10,
    )
    degraded = SearchResult(
        channel="torrent",
        source="yts",
        provider="magnet",
        title="Oppenheimer 2023 2160p HDR",
        link_or_magnet="magnet:?xt=urn:btih:222",
        share_id_or_info_hash="222",
        seeders=10,
    )
    engine.pan_sources = []
    engine.torrent_sources = [FakeSource("tpb", "torrent", 2, [stable]), FakeSource("yts", "torrent", 2, [degraded])]
    response = engine.search(parse_intent("Oppenheimer 2023", explicit_kind="movie"), use_cache=False)
    assert response["results"][0]["source"] == "tpb"
    yts_result = [item for item in response["results"] if item["source"] == "yts"][0]
    assert yts_result["source_degraded"] is True
    assert any("degraded source penalty" in item for item in yts_result["penalties"])


def test_cli_text_limit_is_hard_contract(monkeypatch, capsys):
    fake_response = {
        "query": "test query",
        "intent": {"kind": "general", "quick": False},
        "plan": {"channels": ["pan", "torrent"], "notes": ["demo"]},
        "results": [
            {
                "channel": "pan",
                "source": "2fun",
                "provider": "aliyun",
                "title": "Demo One",
                "link_or_magnet": "https://example.com/1",
                "password": "",
                "share_id_or_info_hash": "1",
                "size": "",
                "seeders": 0,
                "quality": "",
                "quality_tags": {},
                "score": 77,
                "reasons": ["query match"],
                "penalties": [],
                "match_bucket": "title_family_match",
                "confidence": 0.7,
                "source_degraded": False,
                "validation_status": "validated",
                "validation_signals": ["title-family alignment"],
                "actionability": "direct",
                "evidence_count": 1,
                "corroboration_count": 0,
                "corroborated_sources": ["2fun"],
                "cluster_id": "abc123",
                "supporting_results": [],
                "raw": {},
            },
            {
                "channel": "pan",
                "source": "2fun",
                "provider": "aliyun",
                "title": "Demo Two",
                "link_or_magnet": "https://example.com/2",
                "password": "",
                "share_id_or_info_hash": "2",
                "size": "",
                "seeders": 0,
                "quality": "",
                "quality_tags": {},
                "score": 60,
                "reasons": ["query match"],
                "penalties": [],
                "match_bucket": "weak_context_match",
                "confidence": 0.2,
                "source_degraded": False,
                "validation_status": "speculative",
                "validation_signals": ["weak context only"],
                "actionability": "speculative",
                "evidence_count": 1,
                "corroboration_count": 0,
                "corroborated_sources": ["2fun"],
                "cluster_id": "def456",
                "supporting_results": [],
                "raw": {},
            },
        ],
        "warnings": [],
        "source_status": [],
        "meta": {"cached": False, "success_estimate": {"has_direct": True, "has_actionable": True, "has_clues": False}},
    }

    monkeypatch.setattr("resource_hunter.cli.ResourceHunterEngine.search", lambda *args, **kwargs: fake_response)
    rc = cli_main(["search", "test query", "--limit", "1"])
    assert rc == 0
    output = capsys.readouterr().out
    assert "Demo One" in output
    assert "Demo Two" not in output


def test_json_retains_weak_candidates_with_bucket(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)
    strong = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="Breaking Bad S01E01 Pilot 1080p",
        link_or_magnet="magnet:?xt=urn:btih:111",
        share_id_or_info_hash="111",
        seeders=4,
    )
    weak = SearchResult(
        channel="torrent",
        source="eztv",
        provider="magnet",
        title="Random Show S01E01 720p",
        link_or_magnet="magnet:?xt=urn:btih:222",
        share_id_or_info_hash="222",
        seeders=80,
    )
    engine.pan_sources = []
    engine.torrent_sources = [FakeSource("tpb", "torrent", 2, [strong]), FakeSource("eztv", "torrent", 1, [weak])]
    response = engine.search(parse_intent("Breaking Bad S01E01", explicit_kind="tv"), use_cache=False)
    assert response["meta"]["candidate_count"] == 2
    weak_result = [item for item in response["results"] if item["title"].startswith("Random Show")][0]
    assert weak_result["match_bucket"] in {"episode_only_match", "weak_context_match"}
    assert weak_result["confidence"] < 0.5


def test_pan_aggregated_magnet_normalizes_to_torrent_channel():
    payload = {
        "results": [
            {
                "title": "Test Movie",
                "url": "magnet:?xt=urn:btih:abc",
                "netdiskType": "magnet",
            }
        ]
    }
    results = pc._flatten_pan_payload(payload, "2fun")
    assert results[0].channel == "torrent"
    assert results[0].source == "2fun"


def test_tieba_thread_source_extracts_pan_and_password(monkeypatch):
    source = pc.TiebaSource()

    def fake_search_results(self, query, http_client):
        return [{"url": "https://tieba.baidu.com/p/123456", "title": "赤橙黄绿青蓝紫 资源贴"}]

    class FakeHTTPClient:
        def get_text(self, url, timeout=None):
            return (
                '<html><title>赤橙黄绿青蓝紫 资源贴</title>'
                '夸克：https://pan.quark.cn/s/abc123def456 提取码: 7788'
                "</html>"
            )

    monkeypatch.setattr(pc.AliasResolver, "search_results", fake_search_results)
    results = source.search(
        "赤橙黄绿青蓝紫 1982",
        parse_intent("赤橙黄绿青蓝紫 1982", explicit_kind="movie"),
        limit=5,
        page=1,
        http_client=FakeHTTPClient(),
    )
    assert results
    assert results[0].source == "tieba"
    assert results[0].provider == "quark"
    assert results[0].password == "7788"


def test_tieba_thread_source_returns_manual_clue_when_only_filename_and_password(monkeypatch):
    source = pc.TiebaSource()

    def fake_search_results(self, query, http_client):
        return [{"url": "https://tieba.baidu.com/p/10559210059", "title": "赤橙黄绿青蓝紫 资源贴"}]

    class FakeHTTPClient:
        def get_text(self, url, timeout=None):
            return (
                "<html>"
                "通过百度网盘分享的文件：赤橙黄绿青蓝紫"
                "提取码:y3bq"
                "</html>"
            )

    monkeypatch.setattr(pc.AliasResolver, "search_results", fake_search_results)
    results = source.search(
        "赤橙黄绿青蓝紫 1982",
        parse_intent("赤橙黄绿青蓝紫 1982", explicit_kind="movie"),
        limit=5,
        page=1,
        http_client=FakeHTTPClient(),
    )
    assert results
    assert results[0].provider == "baidu_clue"
    assert results[0].password == "y3bq"
    assert results[0].link_or_magnet == "https://tieba.baidu.com/p/10559210059"
    assert results[0].raw["manual_follow_up"] is True


def test_titles_that_only_mention_target_do_not_enter_exact_bucket(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)
    exact = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="Breaking Bad S01E01 Pilot 1080p WEB-DL",
        link_or_magnet="magnet:?xt=urn:btih:aaa",
        share_id_or_info_hash="aaa",
    )
    mention = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="The Writers Room 2013 S01E01 Breaking Bad 720p HDTV",
        link_or_magnet="magnet:?xt=urn:btih:bbb",
        share_id_or_info_hash="bbb",
    )
    engine.pan_sources = []
    engine.torrent_sources = [FakeSource("tpb", "torrent", 2, [exact, mention])]
    response = engine.search(parse_intent("Breaking Bad S01E01", explicit_kind="tv"), use_cache=False)
    mention_result = [item for item in response["results"] if item["title"].startswith("The Writers Room")][0]
    assert mention_result["match_bucket"] != "exact_title_episode"


def test_alias_resolution_for_chinese_old_movie_drives_plan_and_confidence(monkeypatch, tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)

    def fake_resolve(self, intent, cache, http_client):
        return {
            "original_title": "赤橙黄绿青蓝紫",
            "english_title": "Full of Colors",
            "romanized_title": "Chi cheng huang lü qing lan zi",
            "alternate_titles": ["3-Dimensional People"],
            "resolved_year": "1982",
            "resolver_sources": ["https://example.com/movie"],
        }

    weak = SearchResult(
        channel="torrent",
        source="tpb",
        provider="magnet",
        title="Blade Runner 1982 1080p BluRay",
        link_or_magnet="magnet:?xt=urn:btih:111",
        share_id_or_info_hash="111",
        seeders=99,
    )
    engine.pan_sources = []
    engine.torrent_sources = [FakeSource("tpb", "torrent", 2, [weak])]
    monkeypatch.setattr(pc.AliasResolver, "resolve", fake_resolve)
    response = engine.search(parse_intent("赤橙黄绿青蓝紫 1982", explicit_kind="movie"), use_cache=False)
    assert "Full of Colors" in response["meta"]["resolved_titles"]
    assert any("Full of Colors 1982" in item for item in response["plan"]["torrent_queries"] + response["plan"]["pan_queries"])
    assert response["results"][0]["match_bucket"] == "weak_context_match"
    text = pc.format_search_text(response, max_results=3)
    assert "actionability=" in text
    assert response["meta"]["success_estimate"]["has_actionable"] is True


def test_the_merry_widow_1952_wrong_year_result_is_not_direct_validated(tmp_path):
    intent = parse_intent("The Merry Widow 1952", explicit_kind="movie")
    wrong_year = pc.score_result(
        SearchResult(
            channel="torrent",
            source="tpb",
            provider="magnet",
            title="The Merry Widow 1934 720p WebDL X264",
            link_or_magnet="magnet:?xt=urn:btih:abc",
            share_id_or_info_hash="abc",
            seeders=25,
        ),
        intent,
    )
    assert wrong_year.validation_status == "conflict"
    assert wrong_year.actionability == "speculative"


def test_default_degraded_source_recovers_after_probe_or_real_success(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    assert pc._source_is_degraded(cache, "yts") is True

    cache.record_source_status(
        SourceStatus(
            source="yts",
            channel="torrent",
            priority=2,
            ok=True,
            degraded=False,
            failure_kind="probe_ok",
        )
    )
    assert pc._source_is_degraded(cache, "yts") is False

    cache2 = ResourceCache(tmp_path / "cache2.db")
    cache2.record_source_status(
        SourceStatus(
            source="yts",
            channel="torrent",
            priority=2,
            ok=False,
            degraded=True,
            failure_kind="network",
            error="ssl eof",
        )
    )
    cache2.record_source_status(
        SourceStatus(
            source="yts",
            channel="torrent",
            priority=2,
            ok=True,
            degraded=True,
            failure_kind="",
        )
    )
    cache2.record_source_status(
        SourceStatus(
            source="yts",
            channel="torrent",
            priority=2,
            ok=True,
            degraded=True,
            failure_kind="",
        )
    )
    assert pc._source_is_degraded(cache2, "yts") is False


def test_search_json_meta_includes_request_id_and_timings(tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    engine = ResourceHunterEngine(cache=cache)
    engine.pan_sources = []
    engine.torrent_sources = [
        FakeSource(
            "tpb",
            "torrent",
            2,
            [
                SearchResult(
                    channel="torrent",
                    source="tpb",
                    provider="magnet",
                    title="Oppenheimer 2023 2160p HDR",
                    link_or_magnet="magnet:?xt=urn:btih:abc",
                    share_id_or_info_hash="abc",
                    seeders=12,
                )
            ],
        )
    ]
    response = engine.search(parse_intent("Oppenheimer 2023", explicit_kind="movie"), use_cache=False)
    assert response["meta"]["request_id"]
    assert response["meta"]["timings_ms"]["total"] >= 0
    assert "fetch" in response["meta"]["timings_ms"]
    assert "best_direct_results" in response["meta"]
    assert response["meta"]["success_estimate"]["has_actionable"] is True
