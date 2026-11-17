"""Importable implementation package for the Skill Vitals Python CLI."""

# 工具版本，也是**发布版本的唯一来源**。
#
# 曾经它和 ClawHub 上的版本各走各的：ClawHub 的版本号取自 git tag，这里长期停在
# 0.1.0，于是装了 1.0.6 的用户跑 `--version` 看到的是 0.1.0 —— 报 bug 时引用的
# 版本号全是错的，没法对应到任何一次发布。
#
# 现在 package-clawhub.yml 在发布前校验 tag 与这里一致，不一致就中止。要发新版，
# 先改这一行，再打同名 tag。
#
# 与 SCHEMA_VERSION（在 cli.py）无关：工具可以升版而 JSON schema 不变。
# rust 分支上 Cargo.toml 的 version 必须跟这里一致，否则两个实现无法用同一条
# `--version` 区分；tests/test_regressions.py 在有 Cargo.toml 时会断言。
__version__ = "1.2.0"

from .frontmatter import parse_frontmatter
from .security import SECURITY_PATTERNS, is_cited, security_scan
from .util import est_tokens, norm, safe_str

__all__ = [
    "SECURITY_PATTERNS",
    "__version__",
    "est_tokens",
    "is_cited",
    "norm",
    "parse_frontmatter",
    "safe_str",
    "security_scan",
]
