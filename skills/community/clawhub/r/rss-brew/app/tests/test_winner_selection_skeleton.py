from rss_brew.compat import run_pipeline_v2 as rp


def test_rank_key_prefers_higher_new_articles_then_deep_set_then_time():
    low = {"new_articles": 1, "deep_set_count": 9, "finalize_finished_at": "2026-01-01T00:00:00+00:00"}
    high = {"new_articles": 2, "deep_set_count": 0, "finalize_finished_at": "2026-01-01T00:00:00+00:00"}
    assert rp.rank_key(high) > rp.rank_key(low)


def test_rank_key_tie_breaks_on_deep_set_count():
    low = {"new_articles": 5, "deep_set_count": 1, "finalize_finished_at": "2026-01-01T00:00:00+00:00"}
    high = {"new_articles": 5, "deep_set_count": 2, "finalize_finished_at": "2026-01-01T00:00:00+00:00"}
    assert rp.rank_key(high) > rp.rank_key(low)


def test_rank_key_tie_breaks_on_finalize_finished_at():
    early = {"new_articles": 5, "deep_set_count": 2, "finalize_finished_at": "2026-01-01T00:00:00+00:00"}
    late = {"new_articles": 5, "deep_set_count": 2, "finalize_finished_at": "2026-01-01T00:00:01+00:00"}
    assert rp.rank_key(late) > rp.rank_key(early)


def test_select_winner_returns_none_for_empty_list():
    assert rp.select_winner([]) is None


def test_select_winner_uses_rank_key_ordering():
    candidates = [
        {"run_id": "r1", "new_articles": 2, "deep_set_count": 1, "finalize_finished_at": "2026-01-01T00:00:00+00:00"},
        {"run_id": "r2", "new_articles": 2, "deep_set_count": 2, "finalize_finished_at": "2026-01-01T00:00:00+00:00"},
        {"run_id": "r3", "new_articles": 1, "deep_set_count": 999, "finalize_finished_at": "2026-01-01T00:00:00+00:00"},
    ]
    winner = rp.select_winner(candidates)
    assert winner is not None
    assert winner["run_id"] == "r2"
