import time

import pytest

from bin.cache import Cache


@pytest.fixture
def cache(tmp_path):
    return Cache(tmp_path / "test.db")


# seen_messages dedup
def test_message_not_seen_initially(cache):
    assert cache.seen("<id@example.com>") is False


def test_mark_and_check_seen(cache):
    cache.mark_seen("<id@example.com>", verdict="safe")
    assert cache.seen("<id@example.com>") is True


def test_mark_seen_returns_verdict(cache):
    cache.mark_seen("<id@example.com>", verdict="phishing")
    assert cache.get_verdict("<id@example.com>") == "phishing"


def test_different_messages_independent(cache):
    cache.mark_seen("<a@example.com>", verdict="safe")
    assert cache.seen("<b@example.com>") is False


# sender_cache TTL
def test_no_sender_verdict_initially(cache):
    assert cache.sender_verdict("bob@scam.xyz") is None


def test_cache_sender_verdict(cache):
    cache.cache_sender_verdict("bob@scam.xyz", verdict="phishing", confidence=92, ttl=3600)
    result = cache.sender_verdict("bob@scam.xyz")
    assert result is not None
    assert result["verdict"] == "phishing"
    assert result["confidence"] == 92


def test_sender_verdict_expires(cache):
    cache.cache_sender_verdict("bob@scam.xyz", verdict="phishing", confidence=92, ttl=0)
    # tiny sleep to cross the "now" boundary
    time.sleep(0.01)
    assert cache.sender_verdict("bob@scam.xyz") is None


def test_sender_verdict_overwrites(cache):
    cache.cache_sender_verdict("bob@scam.xyz", verdict="safe", confidence=10, ttl=3600)
    cache.cache_sender_verdict("bob@scam.xyz", verdict="phishing", confidence=88, ttl=3600)
    result = cache.sender_verdict("bob@scam.xyz")
    assert result["verdict"] == "phishing"
    assert result["confidence"] == 88


# trusted_senders allowlist
def test_sender_not_trusted_initially(cache):
    assert cache.is_trusted("alice@friend.com") is False


def test_add_and_check_trusted(cache):
    cache.add_trusted("alice@friend.com")
    assert cache.is_trusted("alice@friend.com") is True


def test_trusted_is_case_insensitive(cache):
    cache.add_trusted("Alice@FRIEND.com")
    assert cache.is_trusted("alice@friend.com") is True
    assert cache.is_trusted("ALICE@friend.COM") is True


def test_add_trusted_idempotent(cache):
    cache.add_trusted("alice@friend.com")
    cache.add_trusted("alice@friend.com")
    # no exception, still trusted
    assert cache.is_trusted("alice@friend.com") is True


# persistence across Cache() instances
def test_persistence(tmp_path):
    db = tmp_path / "persist.db"
    c1 = Cache(db)
    c1.mark_seen("<id@a.com>", verdict="safe")
    c1.add_trusted("alice@friend.com")
    c1.cache_sender_verdict("bob@scam.xyz", verdict="phishing", confidence=90, ttl=3600)
    c1.close()

    c2 = Cache(db)
    assert c2.seen("<id@a.com>") is True
    assert c2.is_trusted("alice@friend.com") is True
    assert c2.sender_verdict("bob@scam.xyz")["verdict"] == "phishing"


def test_stats(cache):
    cache.mark_seen("<a>", verdict="safe")
    cache.mark_seen("<b>", verdict="phishing")
    cache.mark_seen("<c>", verdict="phishing")
    cache.add_trusted("alice@friend.com")

    stats = cache.stats()
    assert stats["seen_messages"] == 3
    assert stats["trusted_senders"] == 1
