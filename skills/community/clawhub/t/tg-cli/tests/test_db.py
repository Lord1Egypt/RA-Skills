"""Tests for MessageDB — uses temp SQLite, no Telegram dependency."""

from conftest import make_msg

# ─────────────────────── insert_message ───────────────────────


class TestInsertMessage:
    def test_insert_and_count(self, db):
        ok = db.insert_message(**make_msg())
        assert ok is True
        assert db.count() == 1

    def test_duplicate_ignored(self, db):
        db.insert_message(**make_msg(msg_id=1))
        ok = db.insert_message(**make_msg(msg_id=1))
        assert ok is False
        assert db.count() == 1

    def test_different_msg_ids(self, db):
        db.insert_message(**make_msg(msg_id=1))
        db.insert_message(**make_msg(msg_id=2))
        assert db.count() == 2


# ─────────────────────── insert_batch ───────────────────────


class TestInsertBatch:
    def test_batch_insert(self, db):
        msgs = [make_msg(msg_id=i) for i in range(50)]
        result = db.insert_batch(msgs)
        assert result == 50
        assert db.count() == 50

    def test_batch_empty(self, db):
        result = db.insert_batch([])
        assert result == 0

    def test_batch_with_duplicates(self, db):
        db.insert_message(**make_msg(msg_id=1))
        msgs = [make_msg(msg_id=i) for i in range(1, 6)]
        inserted = db.insert_batch(msgs)
        assert inserted == 4
        assert db.count() == 5


# ─────────────────────── search ───────────────────────


class TestSearch:
    def test_search_found(self, db):
        db.insert_message(**make_msg(content="Rust is great"))
        db.insert_message(**make_msg(msg_id=2, content="Python is good"))
        results = db.search("Rust")
        assert len(results) == 1
        assert "Rust" in results[0]["content"]

    def test_search_not_found(self, db):
        db.insert_message(**make_msg(content="Hello"))
        results = db.search("Golang")
        assert len(results) == 0

    def test_search_case_insensitive(self, db):
        db.insert_message(**make_msg(content="Hello World"))
        results = db.search("hello")
        assert len(results) == 1

    def test_search_with_chat_filter(self, db):
        db.insert_message(**make_msg(chat_id=100, content="Web3 job"))
        db.insert_message(**make_msg(chat_id=200, msg_id=2, content="Web3 course"))
        results = db.search("Web3", chat_id=100)
        assert len(results) == 1

    def test_search_with_sender_filter(self, db):
        db.insert_message(**make_msg(msg_id=1, sender_name="Alice", content="Rust job"))
        db.insert_message(**make_msg(msg_id=2, sender_name="Bob", content="Rust course"))
        results = db.search("Rust", sender="Ali")
        assert len(results) == 1
        assert results[0]["sender_name"] == "Alice"

    def test_search_with_hours_filter(self, db):
        db.insert_message(**make_msg(msg_id=1, content="Rust today", hours_ago=1))
        db.insert_message(**make_msg(msg_id=2, content="Rust old", hours_ago=72))
        results = db.search("Rust", hours=24)
        assert len(results) == 1
        assert results[0]["content"] == "Rust today"

    def test_search_limit(self, db):
        for i in range(20):
            db.insert_message(**make_msg(msg_id=i, content=f"test msg {i}"))
        results = db.search("test", limit=5)
        assert len(results) == 5

    def test_search_regex_found(self, db):
        db.insert_message(**make_msg(msg_id=1, content="Rust and Go"))
        db.insert_message(**make_msg(msg_id=2, content="Python only"))
        results = db.search_regex(r"Rust.*Go")
        assert len(results) == 1
        assert results[0]["content"] == "Rust and Go"

    def test_search_regex_with_sender_filter(self, db):
        db.insert_message(**make_msg(msg_id=1, sender_name="Alice", content="Rust remote"))
        db.insert_message(**make_msg(msg_id=2, sender_name="Bob", content="Rust remote"))
        results = db.search_regex(r"rust\s+remote", sender="Ali")
        assert len(results) == 1
        assert results[0]["sender_name"] == "Alice"


# ─────────────────────── get_recent ───────────────────────


class TestGetRecent:
    def test_recent_within_hours(self, db):
        db.insert_message(**make_msg(msg_id=1, hours_ago=1))
        db.insert_message(**make_msg(msg_id=2, hours_ago=48))
        results = db.get_recent(hours=24)
        assert len(results) == 1

    def test_recent_all(self, db):
        db.insert_message(**make_msg(msg_id=1, hours_ago=1))
        db.insert_message(**make_msg(msg_id=2, hours_ago=720))
        results = db.get_recent(hours=None, limit=100)
        assert len(results) == 2

    def test_recent_with_chat_filter(self, db):
        db.insert_message(**make_msg(chat_id=100, msg_id=1))
        db.insert_message(**make_msg(chat_id=200, msg_id=2))
        results = db.get_recent(chat_id=100, hours=24)
        assert len(results) == 1

    def test_recent_with_sender_filter(self, db):
        db.insert_message(**make_msg(msg_id=1, sender_name="Alice"))
        db.insert_message(**make_msg(msg_id=2, sender_name="Bob"))
        results = db.get_recent(sender="Ali", hours=24)
        assert len(results) == 1
        assert results[0]["sender_name"] == "Alice"

    def test_recent_limit_returns_latest_messages(self, db):
        for i in range(5):
            db.insert_message(**make_msg(msg_id=10 + i, content=f"msg {i}", hours_ago=5 - i))
        results = db.get_recent(hours=24, limit=2)
        assert [r["content"] for r in results] == ["msg 3", "msg 4"]


# ─────────────────────── get_chats ───────────────────────


class TestGetChats:
    def test_chats_summary(self, db):
        for i in range(5):
            db.insert_message(**make_msg(chat_id=100, chat_name="GroupA", msg_id=i))
        for i in range(3):
            db.insert_message(**make_msg(chat_id=200, chat_name="GroupB", msg_id=100 + i))

        chats = db.get_chats()
        assert len(chats) == 2
        assert chats[0]["chat_name"] == "GroupA"
        assert chats[0]["msg_count"] == 5
        assert chats[1]["chat_name"] == "GroupB"
        assert chats[1]["msg_count"] == 3


# ─────────────────────── get_last_msg_id ───────────────────────


class TestGetLastMsgId:
    def test_returns_max_id(self, db):
        for i in [10, 20, 15]:
            db.insert_message(**make_msg(msg_id=i))
        assert db.get_last_msg_id(100) == 20

    def test_returns_none_for_empty(self, db):
        assert db.get_last_msg_id(999) is None


# ─────────────────────── get_latest_timestamp ───────────────────────


class TestGetLatestTimestamp:
    def test_latest_timestamp(self, db):
        db.insert_message(**make_msg(msg_id=1, hours_ago=3))
        db.insert_message(**make_msg(msg_id=2, hours_ago=1))
        latest = db.get_latest_timestamp()
        assert latest is not None
        assert latest.endswith("+00:00")

    def test_latest_timestamp_empty(self, db):
        assert db.get_latest_timestamp() is None


# ─────────────────────── resolve_chat_id ───────────────────────


class TestResolveChatId:
    def test_resolve_by_name(self, db):
        db.insert_message(**make_msg(chat_id=100, chat_name="MyGroup"))
        assert db.resolve_chat_id("MyGroup") == 100

    def test_resolve_by_partial_name(self, db):
        db.insert_message(**make_msg(chat_id=100, chat_name="DeJob—Web3招聘"))
        assert db.resolve_chat_id("DeJob") == 100

    def test_resolve_by_numeric_id(self, db):
        db.insert_message(**make_msg(chat_id=1570628112))
        assert db.resolve_chat_id("-1001570628112") == 1570628112

    def test_resolve_unknown(self, db):
        result = db.resolve_chat_id("nonexistent")
        assert result is None

    def test_resolve_ambiguous_returns_none(self, db):
        db.insert_message(**make_msg(chat_id=100, chat_name="Dev Group"))
        db.insert_message(**make_msg(chat_id=200, chat_name="Dev Chat", msg_id=2))
        assert db.resolve_chat_id("Dev") is None

    def test_find_chats_returns_all_partial_matches(self, db):
        db.insert_message(**make_msg(chat_id=100, chat_name="Dev Group"))
        db.insert_message(**make_msg(chat_id=200, chat_name="Dev Chat", msg_id=2))
        matches = db.find_chats("Dev")
        assert len(matches) == 2


# ─────────────────────── delete_chat ───────────────────────


class TestDeleteChat:
    def test_delete(self, db):
        for i in range(5):
            db.insert_message(**make_msg(chat_id=100, msg_id=i))
        db.insert_message(**make_msg(chat_id=200, msg_id=99))

        deleted = db.delete_chat(100)
        assert deleted == 5
        assert db.count() == 1

    def test_delete_nonexistent(self, db):
        deleted = db.delete_chat(999)
        assert deleted == 0


# ─────────────────────── context manager ───────────────────────


class TestContextManager:
    def test_context_manager(self, tmp_path):
        from tg_cli.db import MessageDB

        db_path = tmp_path / "ctx.db"
        with MessageDB(db_path=db_path) as d:
            d.insert_message(**make_msg())
            assert d.count() == 1


# ─────────────────────── top_senders ───────────────────────


class TestTopSenders:
    def test_top_senders(self, db):
        for i in range(5):
            db.insert_message(**make_msg(msg_id=i, sender_id=101, sender_name="Alice"))
        for i in range(3):
            db.insert_message(**make_msg(msg_id=10 + i, sender_id=202, sender_name="Bob"))

        results = db.top_senders()
        assert len(results) == 2
        assert results[0]["sender_name"] == "Alice"
        assert results[0]["msg_count"] == 5

    def test_top_senders_with_chat_filter(self, db):
        db.insert_message(**make_msg(chat_id=100, msg_id=1, sender_id=101, sender_name="Alice"))
        db.insert_message(**make_msg(chat_id=200, msg_id=2, sender_id=202, sender_name="Bob"))
        results = db.top_senders(chat_id=100)
        assert len(results) == 1

    def test_top_senders_with_hours(self, db):
        db.insert_message(**make_msg(msg_id=1, sender_id=101, sender_name="Alice", hours_ago=1))
        db.insert_message(**make_msg(msg_id=2, sender_id=202, sender_name="Bob", hours_ago=48))
        results = db.top_senders(hours=24)
        assert len(results) == 1

    def test_top_senders_limit(self, db):
        for i in range(10):
            db.insert_message(**make_msg(msg_id=i, sender_id=100 + i, sender_name=f"User{i}"))
        results = db.top_senders(limit=3)
        assert len(results) == 3

    def test_top_senders_keeps_same_name_different_ids_separate(self, db):
        db.insert_message(**make_msg(msg_id=1, sender_id=101, sender_name="Alex"))
        db.insert_message(**make_msg(msg_id=2, sender_id=202, sender_name="Alex"))
        results = db.top_senders(limit=10)
        assert len(results) == 2


# ─────────────────────── timeline ───────────────────────


class TestTimeline:
    def test_timeline_by_day(self, db):
        db.insert_message(**make_msg(msg_id=1, hours_ago=0))
        db.insert_message(**make_msg(msg_id=2, hours_ago=1))
        db.insert_message(**make_msg(msg_id=3, hours_ago=25))

        results = db.timeline(granularity="day")
        assert len(results) >= 1
        for r in results:
            assert "period" in r
            assert "msg_count" in r

    def test_timeline_by_hour(self, db):
        db.insert_message(**make_msg(msg_id=1, hours_ago=0))
        db.insert_message(**make_msg(msg_id=2, hours_ago=2))
        results = db.timeline(granularity="hour")
        assert len(results) >= 1

    def test_timeline_with_chat_filter(self, db):
        db.insert_message(**make_msg(chat_id=100, msg_id=1))
        db.insert_message(**make_msg(chat_id=200, msg_id=2))
        results = db.timeline(chat_id=100)
        total = sum(r["msg_count"] for r in results)
        assert total == 1

    def test_timeline_empty(self, db):
        results = db.timeline()
        assert results == []


# ─────────────────────── get_today ───────────────────────


class TestGetToday:
    def test_today_returns_recent(self, db):
        # Message from 1 hour ago should be "today"
        db.insert_message(**make_msg(msg_id=1, hours_ago=1))
        # Message from 48 hours ago should not be "today"
        db.insert_message(**make_msg(msg_id=2, hours_ago=48))
        results = db.get_today()
        assert len(results) == 1

    def test_today_with_chat_filter(self, db):
        db.insert_message(**make_msg(chat_id=100, msg_id=1, hours_ago=1))
        db.insert_message(**make_msg(chat_id=200, msg_id=2, hours_ago=1))
        results = db.get_today(chat_id=100)
        assert len(results) == 1
