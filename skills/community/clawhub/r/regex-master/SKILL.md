# regex-master

## 技能概述
正则表达式生成、测试、解释与可视化工具集。帮助用户快速构建、验证和理解正则表达式，提供自然语言描述到正则的自动转换。

## 何时使用
- 需要从零构建正则表达式时
- 需要解释现有正则的含义时
- 需要测试正则是否匹配目标文本时
- 需要提取文本中特定模式的数据时

## 使用方法

### 基础用法
```python
from scripts.regex_engine import RegexMaster

rm = RegexMaster()

# 测试正则是否匹配
result = rm.test("^\d{11}$", "13800138000")
# -> {"match": true, "groups": []}

# 解释正则含义
explanation = rm.explain("^(?=.*[A-Z])(?=.*\d).{8,}$")
# -> 密码强度检查：至少8位，含大写字母和数字

# 从自然语言生成正则
pattern = rm.generate("提取中国大陆手机号")
# -> "1[3-9]\\d{9}"

# 在文本中提取所有匹配
matches = rm.extract_all("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b", text)
# -> ["user@example.com", "admin@test.org"]
```

## 文件结构
```
regex-master/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   └── regex_engine.py      # 核心引擎
├── examples/
│   └── basic_usage.py         # 使用示例
└── tests/
    └── test_regex_master.py   # 单元测试
```

## 依赖
- `re` (Python 内置)
- 可选: `regex` 库提供更强大的正则支持

## 标签
regex, pattern-matching, text-processing, developer-tools