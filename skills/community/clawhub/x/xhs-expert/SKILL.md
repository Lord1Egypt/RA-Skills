---
name: xhs-expert
description: |
  小红书运营专家技能。能够搜索笔记、采集数据、互动操作（点赞/评论/收藏/关注），
  分析内容趋势，批量运营账号。
  当用户要求"搜索小红书"、"小红书运营"、"搜索xhs内容"、"批量互动"、
  "分析小红书"、"xhs数据分析"时触发。
---

# 🐾 XHS Expert - 小红书运营专家技能

> 基于 content-discovery-sdk 蓝图重构，修复所有已知bug，完全可运行

## 技能能力

| 能力 | 说明 | 命令 |
|------|------|------|
| **内容发现** | 搜索笔记、获取详情、采集评论 | `xhs explore search` |
| **社交互动** | 点赞、收藏、评论、关注 | `xhs interact like/collect/comment/follow` |
| **批量操作** | 批量点赞、批量评论 | `xhs interact batch-like` |
| **账号管理** | 登录、状态检查 | `xhs auth status/login` |
| **数据查询** | 本地数据统计 | `xhs data stats` |

## 架构

```
用户输入 → SKILL路由 → CLI命令 → Python模块 → 小红书API
                                      ↓
                              Cookie持久化
```

## 核心模块

| 模块 | 职责 |
|------|------|
| `xhs_client.py` | API客户端、签名算法、Cookie管理 |
| `state_parser.py` | `__INITIAL_STATE__`解析、笔记/评论建模 |
| `feed_collector.py` | 搜索采集、详情采集、评论采集 |
| `interaction_handler.py` | 点赞、收藏、评论、关注 |
| `chrome_launcher.py` | 浏览器启动、Stealth注入 |
| `cookie_manager.py` | Cookie持久化、多账号切换 |

## CLI命令

### 认证管理

```bash
# 检查登录状态
xhs auth status

# 浏览器扫码登录
xhs auth login --profile default
```

### 内容发现

```bash
# 搜索笔记
xhs explore search --keyword "电动车" --max 20 --sort general

# 获取笔记详情
xhs explore detail --note-id <note_id> --include-comments

# 输出到文件
xhs explore search --keyword "电动车" --output results.json
```

### 社交互动

```bash
# 点赞
xhs interact like --note-id <note_id>

# 取消点赞
xhs interact like --note-id <note_id> --action remove

# 收藏
xhs interact collect --note-id <note_id>

# 评论
xhs interact comment --note-id <note_id> --content "写得真好！"

# 关注用户
xhs interact follow --user-id <user_id>

# 批量点赞
xhs interact batch-like --note-ids "id1,id2,id3" --delay 2.0
```

### 数据查询

```bash
# 本地数据统计
xhs data stats
```

## 意图路由

| 用户输入 | 路由 | CLI命令 |
|----------|------|---------|
| "搜索电动车相关笔记" | xhs-explore | `explore search -k 电动车` |
| "这篇笔记讲了什么" | xhs-explore | `explore detail -n <id>` |
| "给我点个赞" | xhs-interact | `interact like -n <id>` |
| "写个评论" | xhs-interact | `interact comment -n <id> -c <content>` |
| "关注这个博主" | xhs-interact | `interact follow -u <user_id>` |
| "批量点赞" | xhs-interact | `interact batch-like -n <ids>` |
| "登录状态" | xhs-auth | `auth status` |

## 执行流程

### 1. 搜索笔记

```
用户: "搜索电动车相关笔记"
  ↓
识别意图: explore (内容发现)
  ↓
确认参数: keyword="电动车", max=20
  ↓
执行: xhs explore search -k 电动车 -m 20
  ↓
返回: 笔记列表 + 摘要统计
```

### 2. 批量互动

```
用户: "给这10篇笔记点赞"
  ↓
识别意图: interact (互动操作)
  ↓
确认参数: note_ids=[...], action="add"
  ↓
[强制确认] 显示目标范围，等待用户回复"确认"
  ↓
执行: xhs interact batch-like -n "id1,id2,..." --delay 2.0
  ↓
返回: 操作结果汇总
```

## 安全约束

### 执行前检查

1. [ ] 已确认操作目标（笔记ID/用户ID）
2. [ ] 已确认登录状态（`xhs auth status`）
3. [ ] 已确认批量操作范围

### 强制确认（必须用户明确回复"确认"）

1. **发表评论** - 显示评论内容，等待确认
2. **批量互动 (>5)** - 显示目标范围，等待确认
3. **关注用户** - 显示用户信息，等待确认

### 禁止事项

1. **禁止使用通用浏览器技能**（如browseruse）操作小红书
2. **禁止硬编码选择器** - 必须使用 `__INITIAL_STATE__` 解析
3. **禁止跳过登录检查** - 所有操作前验证登录态
4. **禁止静默失败** - 任何错误必须给出可操作的提示

## 常见问题

### Q: 被检测/签名失败怎么办？

签名算法是反爬核心，当前SDK使用简化版SHA256签名。
生产环境建议：
1. 使用浏览器模式（`auth login`）获取真实Cookie
2. 使用Selenium注入真实签名
3. 降低请求频率

### Q: 如何处理验证码？

触发验证时，提示用户手动在浏览器完成验证，然后重试。

### Q: Cookie过期了怎么办？

运行 `xhs auth login` 重新扫码登录。

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| HTTP客户端 | httpx (异步) |
| 浏览器 | Playwright (CDP + Stealth) |
| CLI框架 | Click |
| 数据建模 | dataclass |

## 验证清单

- [ ] `xhs auth status` 返回正确登录状态
- [ ] `xhs explore search` 返回结构化笔记列表
- [ ] `xhs explore detail` 返回笔记详情和评论
- [ ] `xhs interact like` 成功点赞
- [ ] `xhs interact comment` 成功评论
- [ ] `xhs interact batch-like` 批量操作正常

## 项目结构

```
~/.openclaw/workspace/skills/xhs-expert/
├── SKILL.md                    # 本文件（主路由）
├── scripts/
│   ├── __init__.py
│   ├── chrome_launcher.py     # Chrome启动器
│   ├── xhs_client.py          # API客户端
│   ├── state_parser.py        # __INITIAL_STATE__解析
│   ├── feed_collector.py      # 内容采集器
│   ├── interaction_handler.py  # 互动处理器
│   ├── cookie_manager.py       # Cookie管理器
│   └── cli.py                 # CLI入口
└── pyproject.toml
```

## 下一步

遇到具体任务时：

1. 确认用户意图（搜索/互动/批量操作）
2. 检查登录状态
3. 执行对应CLI命令
4. 返回结构化结果

---

*🐾 Built from content-discovery-sdk blueprint (v1.0.0)*
*Fixes: playwright._impl deprecation, async syntax errors, Click param mapping*
