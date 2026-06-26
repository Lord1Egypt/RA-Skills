# Secure Linter Skill

安全代码静态分析工具，集成到 OpenClaw Agent 中自动扫描漏洞。

## 功能

- 检测 SQL 注入、XSS、硬编码密钥
- 识别代码异味：重复逻辑、过长函数、魔法数字
- 输出：行号、风险等级（高/中/低）、修复建议

## 使用示例

**用户**：请审查以下 Python 代码安全问题：
```python
def process(user_input):
    sql = "SELECT * FROM users WHERE id = " + user_input
    cursor.execute(sql)
    return cursor.fetchall()
```

**Agent**（使用本技能）输出：
- 第 2 行：SQL 拼接 → SQL 注入风险（高）
  - 修复建议：使用参数化查询（cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,)））

## 配置

无需特殊配置，开箱即用。

## 限制

- 不执行实际代码（仅静态分析）
- 对于复杂业务逻辑可能需要人工复核