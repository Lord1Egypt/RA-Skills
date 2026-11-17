"""敏感信息脱敏 — 对文本中的 PII 做掩码，便于安全分享 / 安全推送。

默认掩码对象（启用 --mask 时生效）：
  - 手机号（大陆 11 位）
  - 身份证号（18 位 / 15 位）
  - 银行卡号（13~19 位连续数字，仅保留末 4 位）
  - 电子邮箱

说明：基于正则启发式，不能 100% 覆盖所有隐私，但能挡住绝大多数
在聊天记录里直接出现的个人敏感字段。若需更高强度（如金额、姓名、
地址），请在自动化 prompt 中追加 AI 级别的脱敏要求。
"""

import re

# 顺序很重要：先处理结构化长串（邮箱/身份证），再处理短串（手机/银行卡），
# 避免彼此误伤。每条规则被替换后混入非数字字符，后续规则不会再命中。
_PATTERNS = [
    # 电子邮箱
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
     lambda m: _mask_email(m.group(0))),
    # 身份证号 18 位：6 位地址 + 8 位出生 + 3 位顺序 + 1 位校验
    (re.compile(r"(?<!\d)(\d{6})(\d{8})(\d{3}[\dXx])(?!\d)"),
     lambda m: m.group(1) + "********" + m.group(3)),
    # 身份证号 15 位（老式）
    (re.compile(r"(?<!\d)(\d{6})(\d{6})(\d{3})(?!\d)"),
     lambda m: m.group(1) + "******" + m.group(3)),
    # 手机号（大陆 11 位，1[3-9] 开头）
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
     lambda m: m.group(0)[:3] + "****" + m.group(0)[-4:]),
    # 银行卡号（13~19 位连续数字，保留末 4 位）
    (re.compile(r"(?<!\d)\d{13,19}(?!\d)"),
     lambda m: "****" + m.group(0)[-4:]),
]


def _mask_email(email):
    user, _, domain = email.partition("@")
    if len(user) <= 1:
        u = "*"
    elif len(user) == 2:
        u = user[0] + "*"
    else:
        u = user[0] + "***" + user[-1]
    return f"{u}@{domain}"


def mask_text(text):
    """对单个字符串脱敏，返回脱敏后的字符串。"""
    if not text:
        return text
    for pat, fn in _PATTERNS:
        text = pat.sub(fn, text)
    return text


def mask_lines(lines):
    """对字符串列表逐条脱敏。"""
    return [mask_text(line) for line in lines]
