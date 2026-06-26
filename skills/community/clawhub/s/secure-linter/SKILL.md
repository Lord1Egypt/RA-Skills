---
name: secure_linter
description: 安全代码 Linter：扫描漏洞、密钥泄露和代码异味
version: 0.1.0
metadata:
  {"openclaw": {"requires": {"bins": []}}}
---
# 代码审查助手

当用户要求审查代码时，按以下步骤：

1. **理解语言**：识别代码语言（JavaScript/Python/Go/Rust等）
2. **检查常见漏洞**：
   - SQL 注入
   - XSS
   - 硬编码密钥
   - 边界检查缺失
3. **代码质量**：
   - 重复代码
   - 过长函数
   - 魔法数字
4. **输出格式**：
   - 问题行号
   - 风险等级（高/中/低）
   - 修复建议

使用 `browser` 或 `web_fetch` 查看相关安全指南（如 OWASP）以补充知识。