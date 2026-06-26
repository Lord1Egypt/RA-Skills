"""Doc-review patterns for sensitive file references."""

SECRET_PATH_PATTERNS = [
    r"~/.openclaw/secrets\.json",
    r"\bsecrets\.json\b",
    r"\bconfig\.json\b",
]

SAFE_DOC_CONTEXT_PATTERNS = [
    r"does not read",
    r"do not read",
    r"no direct reads",
    r"not read",
    r"won't read",
    r"avoid",
    r"removed",
    r"remove",
    r"example",
    r"examples",
    r"pattern",
    r"patterns",
    r"scanner",
    r"trigger",
    r"triggers",
    r"keyword",
    r"keywords",
    r"容易触发",
    r"优先看",
    r"命中",
    r"典型形式",
    r"高风险关键词",
    r"不会",
    r"不读取",
    r"不读",
    r"移除",
    r"删除",
]

UNSAFE_DOC_CONTEXT_PATTERNS = [
    r"read.{0,40}secrets\.json",
    r"secrets\.json.{0,40}read",
    r"load.{0,40}config\.json",
    r"config\.json.{0,40}load",
    r"use.{0,40}config\.json",
    r"config\.json.{0,40}use",
    r"从.{0,20}secrets\.json.{0,20}读取",
    r"从.{0,20}config\.json.{0,20}读取",
    r"secrets\.json.{0,20}读取",
    r"config\.json.{0,20}读取",
    r"config\.json.{0,20}依赖",
    r"自动读取.{0,40}secrets",
]
