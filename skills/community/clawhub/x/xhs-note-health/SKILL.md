---
name: xhs-note-health
version: "1.1.0"
description: "检测小红书笔记限流状态。通过创作者后台 API 获取所有笔记的 level 字段，判断限流等级、敏感词命中、标签风险。"
author: "d (voidborne)"
---

# 小红书笔记健康检测 (xhs-note-health)

检测小红书创作者后台所有笔记的限流状态，无需浏览器扩展。

## 原理

小红书创作者后台 API `/api/galaxy/v2/creator/note/user/posted` 返回的每篇笔记包含 `level` 字段，表示推荐分发等级：

| Level | 状态 | 说明 |
|-------|------|------|
| 4 🟢 | 正常推荐 | 笔记正常分发 |
| 2 🟡 | 基本正常 | 轻微受限 |
| 1 ⚪ | 新帖初始 | 刚发布，等待审核 |
| -1 🔴 | 轻度限流 | 推荐量明显下降 |
| -5 🔴🔴 | 中度限流 | 几乎无推荐 |
| -102 ⛔ | 严重限流 | 不可逆，需删除重发 |

## 前置条件

1. **Cookies 文件** — 需要小红书创作者后台的有效 cookies
   - 默认路径: `~/tools/xiaohongshu-mcp/xiaohongshu_cookies.json`
   - 可通过 `--cookies` 参数指定其他路径
   - 格式: JSON 数组，每个元素包含 `name` 和 `value` 字段
   - Cookies 有效期约 30 天，过期需重新从浏览器导出

2. **Python 3** + `requests` 库

## 使用方法

```bash
# 检测所有笔记
python3 <skill_dir>/check.py

# 指定 cookies 路径
python3 <skill_dir>/check.py --cookies /path/to/cookies.json

# 只看限流笔记
python3 <skill_dir>/check.py --throttled-only

# 按点赞数排序
python3 <skill_dir>/check.py --sort likes

# JSON 输出（适合程序处理）
python3 <skill_dir>/check.py --json

# 保存报告到文件
python3 <skill_dir>/check.py --output report.md
```

## Agent 使用指南

当用户要求检测小红书笔记限流状态时：

1. 运行 `check.py` 脚本获取结果
2. 汇总报告：总笔记数、各 level 分布、限流笔记列表、敏感词命中
3. 如果 cookies 过期 (返回 401/903)，提醒用户重新导出 cookies

### 示例调用

```bash
python3 ~/.openclaw/workspace/skills/xhs-note-health/check.py --json
```

解析 JSON 输出后，给用户一份简洁的中文报告。

## 敏感词检测

内置 50+ 高危敏感词，覆盖以下类别：
- AI/自动化相关
- 极限词/绝对化用语
- 虚假承诺
- 医疗功效夸大
- 站外引流词
- 诱导互动
- 营销限时词

## 致谢

限流检测原理参考 [jzOcb/xhs-note-health-checker](https://github.com/jzOcb/xhs-note-health-checker)（Chrome 扩展版）。
