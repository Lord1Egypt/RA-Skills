# -*- coding: utf-8 -*-
import pytest
from utils.webclient import check_url


def test_reject_non_https():
    with pytest.raises(ValueError):
        check_url('http://open.feishu.cn/x')


def test_reject_unknown_host():
    with pytest.raises(ValueError):
        check_url('https://evil.example.com/x')


def test_reject_localhost():
    with pytest.raises(ValueError):
        check_url('https://localhost/x')


def test_accept_whitelisted_host(monkeypatch):
    import utils.webclient as wc
    infos = [(None, None, None, '', ('1.2.3.4', 443))]
    monkeypatch.setattr(wc.socket, 'getaddrinfo', lambda *a, **k: infos)
    check_url('https://open.feishu.cn/x')


def test_reject_private_resolution(monkeypatch):
    import utils.webclient as wc
    infos = [(None, None, None, '', ('192.168.1.5', 443))]
    monkeypatch.setattr(wc.socket, 'getaddrinfo', lambda *a, **k: infos)
    with pytest.raises(ValueError):
        check_url('https://open.feishu.cn/x')
