# xhs-note-health 📊

> 小红书笔记限流状态检测 — OpenClaw Agent Skill

让 AI agent 直接检测小红书创作者后台所有笔记的限流状态，无需浏览器扩展。

## 工作原理

小红书创作者后台 API 返回的每篇笔记包含一个 `level` 字段，表示推荐分发等级（社区逆向工程，非官方）：

| Level | 状态 | 说明 |
|-------|------|------|
| 4 🟢 | 正常推荐 | 笔记正常分发 |
| 2 🟡 | 基本正常 | 轻微受限 |
| 1 ⚪ | 新帖初始 | 刚发布，等待审核 |
| -1 🔴 | 轻度限流 | 推荐量明显下降 |
| -5 🔴🔴 | 中度限流 | 几乎无推荐 |
| -102 ⛔ | 严重限流 | 不可逆，需删除重发 |

## 功能

- **📊 全量检测** — 分页获取所有笔记，逐一检测 level 状态
- **⚠️ 敏感词检测** — 50+ 内置高危词（AI自动化、极限词、引流词等）
- **📛 标签风险** — 话题标签 >5 个自动提示
- **📋 Markdown 报告** — 按限流等级分组，一目了然
- **🤖 JSON 输出** — 适合 agent 程序化处理

## 安装

```bash
# 通过 ClawHub
clawhub install xhs-note-health

# 或手动复制到 skills 目录
cp -r xhs-note-health ~/.openclaw/workspace/skills/
```

## 前置条件

1. **Python 3** + `requests` 库
2. **小红书创作者后台 Cookies** — 从浏览器导出为 JSON 文件
   - 默认路径: `~/tools/xiaohongshu-mcp/xiaohongshu_cookies.json`
   - 格式: `[{name, value, domain, ...}, ...]` 或 `{name: value, ...}`
   - 有效期约 30 天

### 导出 Cookies

使用浏览器扩展（如 EditThisCookie、Cookie-Editor）导出 `creator.xiaohongshu.com` 的 cookies 为 JSON 格式。

## 使用

```bash
# 检测所有笔记
python3 check.py

# 指定 cookies 路径
python3 check.py --cookies /path/to/cookies.json

# 只看限流笔记
python3 check.py --throttled-only

# JSON 输出
python3 check.py --json

# 保存报告
python3 check.py --output report.md
```

## Agent 使用

当用户说"检测小红书限流"、"笔记健康检查"、"小红书笔记状态"时，运行 `check.py` 并汇总报告。

## 敏感词分类

| 分类 | 示例 |
|------|------|
| AI/自动化 | AI生成, 自动化, 批量, 内容工厂 |
| 极限词 | 最好, 第一, 唯一, 顶级 |
| 虚假承诺 | 包过, 稳赚不赔, 零风险 |
| 医疗夸大 | 根治, 特效, 一次见效 |
| 站外引流 | 微信, 加V, VX |
| 诱导互动 | 互粉, 求关注, 一键三连 |

## 致谢

限流检测原理参考 [jzOcb/xhs-note-health-checker](https://github.com/jzOcb/xhs-note-health-checker)（Chrome 扩展版）。

## License

MIT
