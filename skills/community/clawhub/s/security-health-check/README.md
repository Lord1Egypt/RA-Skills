# 🔒 Security Health Check — 个人数字安全体检

一键检查你的数字安全状况：邮箱泄露、密码强度、安全评分。

## 功能

| 检查项 | 说明 | 数据来源 |
|--------|------|----------|
| 📧 邮箱泄露 | 检查邮箱是否出现在数据泄露中 | HIBP API |
| 🔑 密码泄露 | 检查密码是否已被泄露（k-匿名，密码不离开本地） | HIBP Password API |
| 💪 密码强度 | 分析密码复杂度和暴力破解时间 | 本地计算 |
| 📊 安全评分 | 综合评分 0-100 分 | 综合分析 |
| 💡 安全建议 | 基于 HIBP 数据提供修复建议 | 智能推荐 |

## 安装

```bash
npx clawhub install security-health-check
```

## 使用

```bash
# 完整体检
python3 scripts/security_check.py --email your@email.com

# 仅检查密码
python3 scripts/security_check.py --password "your_password"

# JSON 格式输出
python3 scripts/security_check.py --email your@email.com --json
```

## 隐私

- **密码永远不离开本地**：使用 HIBP k-匿名前缀查询，只发送 SHA1 前5位
- **邮箱检查结果仅展示摘要**：不存储泄露原始数据
- **报告可随时删除**：所有生成的报告可手动清理

## License

MIT-0
