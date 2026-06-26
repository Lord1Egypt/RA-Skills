import pytest

from bin.url_features import UrlFeatures, score_urls


# Individual feature detection
@pytest.mark.parametrize("url,expected", [
    ("http://203.0.113.5/login", True),
    ("http://192.168.1.50:8080/login", True),
    ("https://paypal.com/login", False),
    ("https://github.com", False),
])
def test_ip_literal(url, expected):
    assert UrlFeatures.from_url(url).ip_literal is expected


@pytest.mark.parametrize("url,expected", [
    ("http://bit.ly/xyz7A9", True),
    ("http://tinyurl.com/abc", True),
    ("https://t.co/short", True),
    ("https://goo.gl/xyz", True),
    ("https://paypal.com/login", False),
])
def test_shortener(url, expected):
    assert UrlFeatures.from_url(url).shortener is expected


def test_at_in_url():
    assert UrlFeatures.from_url("http://paypal.com@evil.ru/").at_in_url is True
    assert UrlFeatures.from_url("http://paypal.com/").at_in_url is False


def test_double_slash_in_path():
    assert UrlFeatures.from_url("http://site.com/a//evil.ru").double_slash_in_path is True
    assert UrlFeatures.from_url("http://site.com/a/b/c").double_slash_in_path is False


@pytest.mark.parametrize("url,expected_depth", [
    ("https://login.verify.secure.paypal.evil.ru", 4),  # 4 dots before tld boundary
    ("https://paypal.com", 0),
    ("https://mail.google.com", 1),
    ("https://a.b.c.d.example.xyz", 4),
])
def test_subdomain_depth(url, expected_depth):
    feats = UrlFeatures.from_url(url)
    assert feats.subdomain_depth == expected_depth


def test_deep_subdomain_flagged():
    # threshold: > 3
    assert UrlFeatures.from_url("https://a.b.c.d.e.example.com").deep_subdomain is True
    assert UrlFeatures.from_url("https://mail.google.com").deep_subdomain is False


def test_hyphenated_hostname():
    assert UrlFeatures.from_url("https://pay-pal-secure.com").hyphenated_hostname is True
    assert UrlFeatures.from_url("https://paypal.com").hyphenated_hostname is False


def test_long_url():
    short = "https://example.com/x"
    long_url = "https://example.com/" + "a" * 100
    assert UrlFeatures.from_url(short).long_url is False
    assert UrlFeatures.from_url(long_url).long_url is True


def test_https_token_in_hostname():
    assert UrlFeatures.from_url("https://https-paypal.ru").https_token_in_hostname is True
    assert UrlFeatures.from_url("https://paypal.com").https_token_in_hostname is False


def test_punycode():
    assert UrlFeatures.from_url("https://xn--pypal-4ve.com").punycode is True
    assert UrlFeatures.from_url("https://paypal.com").punycode is False


def test_explicit_port():
    assert UrlFeatures.from_url("http://example.com:8080/").explicit_port is True
    assert UrlFeatures.from_url("https://example.com/").explicit_port is False
    # standard http/https ports don't count
    assert UrlFeatures.from_url("http://example.com:80/").explicit_port is False
    assert UrlFeatures.from_url("https://example.com:443/").explicit_port is False


@pytest.mark.parametrize("url,expected", [
    ("https://paypal.tk", True),
    ("https://microsoft.xyz", True),
    ("https://paypal.com", False),
    ("https://paypal.org", False),
])
def test_cheap_tld_with_brand(url, expected):
    assert UrlFeatures.from_url(url).cheap_tld_with_brand is expected


# Red-flag counting and scoring
def test_red_flag_count_on_phish_url():
    feats = UrlFeatures.from_url("http://192.168.1.50:8080/login")
    # ip_literal + explicit_port
    assert feats.red_flag_count() == 2


def test_red_flag_count_on_clean_url():
    feats = UrlFeatures.from_url("https://github.com/user/repo")
    assert feats.red_flag_count() == 0


def test_score_urls_clean():
    urls = ["https://github.com/user/repo", "https://google.com"]
    r = score_urls(urls)
    assert r["score"] == 0
    assert r["red_flags_hit"] == 0


def test_score_urls_heavy_phish():
    urls = [
        "http://bit.ly/xyz",                           # shortener
        "http://192.168.1.50:8080/login",             # ip_literal + explicit_port
        "https://paypa1-secure.ru/login",             # hyphenated-ish (no, paypa1-secure has 1 hyphen)
    ]
    r = score_urls(urls)
    assert r["red_flags_hit"] >= 4
    assert r["score"] >= 60


def test_score_saturates_at_100():
    # many red flags → score capped at 100
    urls = ["http://https-paypa1-l0gin.a.b.c.d.tk:8080/@evil.ru"] * 5
    r = score_urls(urls)
    assert r["score"] == 100


def test_score_urls_empty():
    r = score_urls([])
    assert r["score"] == 0
    assert r["red_flags_hit"] == 0
    assert r["per_url_flags"] == []


def test_score_urls_reports_per_url_flags():
    urls = ["http://bit.ly/x", "https://github.com"]
    r = score_urls(urls)
    per = r["per_url_flags"]
    assert len(per) == 2
    assert per[0]["url"] == "http://bit.ly/x"
    assert "shortener" in per[0]["flags"]
    assert per[1]["flags"] == []
