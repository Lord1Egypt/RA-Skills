"""Tests for input resolver."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from utils.resolver import resolve_input, ResolvedInput


class TestResolveURL:
    def test_bilibili_space_url(self):
        r = resolve_input("https://space.bilibili.com/946974")
        assert r.platform == "bilibili"
        assert r.uid == "946974"

    def test_bilibili_space_url_with_path(self):
        r = resolve_input("https://space.bilibili.com/946974/video")
        assert r.platform == "bilibili"
        assert r.uid == "946974"

    def test_youtube_handle(self):
        r = resolve_input("https://www.youtube.com/@MrBeast")
        assert r.platform == "youtube"
        assert r.uid == "MrBeast"

    def test_youtube_channel_id(self):
        r = resolve_input("https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA")
        assert r.platform == "youtube"
        assert r.uid == "UCX6OQ3DkcsbYNE6H8uQQuVA"

    def test_douyin_user(self):
        r = resolve_input("https://www.douyin.com/user/MS4wLjABAAAA123")
        assert r.platform == "douyin"
        assert r.uid == "MS4wLjABAAAA123"

    def test_tiktok_handle(self):
        r = resolve_input("https://www.tiktok.com/@khaby.lame")
        assert r.platform == "tiktok"
        assert r.uid == "khaby.lame"

    def test_instagram_profile(self):
        r = resolve_input("https://www.instagram.com/cristiano/")
        assert r.platform == "instagram"
        assert r.uid == "cristiano"

    def test_xiaohongshu_profile(self):
        r = resolve_input("https://www.xiaohongshu.com/user/profile/5a12345678")
        assert r.platform == "xiaohongshu"
        assert r.uid == "5a12345678"

    def test_kuaishou_profile(self):
        r = resolve_input("https://www.kuaishou.com/profile/3x1234abcd")
        assert r.platform == "kuaishou"
        assert r.uid == "3x1234abcd"

    def test_baijiahao_url(self):
        r = resolve_input("https://baijiahao.baidu.com/u?app_id=1234567890")
        assert r.platform == "baijiahao"
        assert r.uid == "1234567890"

    def test_iqiyi_user(self):
        r = resolve_input("https://www.iqiyi.com/u/abc123def")
        assert r.platform == "iqiyi"
        assert r.uid == "abc123def"

    def test_iqiyi_creator(self):
        r = resolve_input("https://www.iqiyi.com/creator/1571837496")
        assert r.platform == "iqiyi"
        assert r.uid == "1571837496"

    def test_wechat_video(self):
        r = resolve_input("https://channels.weixin.qq.com/someuser")
        assert r.platform == "wechat_video"
        assert r.uid == "someuser"

    def test_unsupported_url(self):
        with pytest.raises(ValueError, match="Unsupported platform"):
            resolve_input("https://www.unknown-platform.com/user123")

    def test_bare_domain_with_path(self):
        r = resolve_input("space.bilibili.com/946974")
        assert r.platform == "bilibili"
        assert r.uid == "946974"


class TestResolveNickname:
    def test_nickname_with_platform(self):
        r = resolve_input("影视飓风", platform_hint="bilibili")
        assert r.platform == "bilibili"
        assert r.nickname == "影视飓风"
        assert r.uid is None

    def test_nickname_without_platform_raises(self):
        with pytest.raises(ValueError, match="Cannot determine platform"):
            resolve_input("影视飓风")

    def test_nickname_with_platform_hint_normalized(self):
        r = resolve_input("MrBeast", platform_hint="YouTube")
        assert r.platform == "youtube"


class TestParseFollowerText:
    """Tests for the follower text parser in browser utils."""

    def test_parse_plain_number(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("12345") == 12345

    def test_parse_wan(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("123.4万") == 1234000

    def test_parse_yi(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("1.5亿") == 150000000

    def test_parse_k(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("5.2K") == 5200

    def test_parse_m(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("1.2M") == 1200000

    def test_parse_with_commas(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("1,234,567") == 1234567

    def test_parse_empty(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("") is None

    def test_parse_invalid(self):
        from utils.browser import parse_follower_text
        assert parse_follower_text("abc") is None


class TestExtractFollowerCount:
    """Tests for the contextual follower count extractor."""

    def test_extract_from_mixed_stats(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("81关注 2.1万粉丝 49.8万获赞与收藏") == 21000

    def test_extract_with_space(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("2.1万 粉丝") == 21000

    def test_extract_no_suffix(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("12345粉丝") == 12345

    def test_extract_yi(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("1.5亿粉丝") == 150000000

    def test_extract_no_keyword(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("81关注 49.8万获赞") is None

    def test_extract_custom_keyword(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("1.2万关注者", keyword="关注者") == 12000

    def test_extract_with_plus_and_newline(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("1万+\n粉丝") == 10000

    def test_extract_with_plus_no_newline(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("2.1万+粉丝") == 21000

    def test_extract_ignores_icp_number(self):
        from utils.browser import extract_follower_count
        text = "沪ICP备13030189号\n1万+\n粉丝"
        assert extract_follower_count(text) == 10000

    def test_extract_keyword_before_number(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("关注 459 粉丝 206.1万 获赞 6049.9万") == 2061000

    def test_extract_keyword_before_number_newline(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("粉丝\n206.1万") == 2061000

    def test_extract_keyword_touching_number(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("粉丝5075") == 5075

    def test_extract_empty(self):
        from utils.browser import extract_follower_count
        assert extract_follower_count("") is None
