# Regex Master

正则表达式大师 — 生成、测试、解释、提取一站式工具。

## Features

| 功能 | 说明 |
|------|------|
| 智能生成 | 根据自然语言描述自动生成正则表达式 |
| 在线测试 | 测试正则是否匹配目标文本，返回捕获组 |
| 语义解释 | 将复杂的正则表达式翻译成人类可读的中文说明 |
| 批量提取 | 从文本中提取所有匹配项，支持命名捕获组 |
| 常用模板 | 内置邮箱、手机号、身份证、URL等常见模式 |
| 可视化辅助 | 输出正则的结构树，帮助理解嵌套逻辑 |

## Quick Start

```python
from scripts.regex_engine import RegexMaster

rm = RegexMaster()

# 1. 测试正则
rm.test(r"^\d{4}-\d{2}-\d{2}$", "2026-04-27")
# { "match": True, "groups": [] }

# 2. 生成正则 — "匹配 IPv4 地址"
rm.generate("匹配 IPv4 地址")
# "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

# 3. 解释正则
rm.explain(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$")
# 密码强度检查：至少8位，包含大写字母、小写字母和数字

# 4. 批量提取
rm.extract_all(r"\b\w+@\w+\.\w+\b", "Contact: alice@test.com, bob@demo.io")
# ["alice@test.com", "bob@demo.io"]

# 5. 常用模板
rm.get_template("email")
# "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
```

## Templates

内置常用正则模板：

- `email` — 邮箱地址
- `phone_cn` — 中国大陆手机号
- `idcard` — 身份证号码
- `url` — URL 链接
- `ipv4` — IPv4 地址
- `date_iso` — ISO 日期格式
- `chinese_chars` — 中文字符
- `hex_color` — 十六进制颜色值
- `credit_card` — 信用卡号（简单校验）

## Installation

无需额外依赖，纯 Python 内置 `re` 模块实现。

可选安装 `regex` 库以获得更强大的引擎支持：
```bash
pip install regex
```

## License
MIT