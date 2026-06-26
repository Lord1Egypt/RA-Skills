---
name: yq-bilibili-skill
description: 哔哩哔哩CLI工具，支持抓取视频详情/字幕/AI摘要/评论/相关视频，提取音频并分割为ASR-ready WAV片段，获取用户资料/视频列表/关注列表，搜索用户或视频，热门视频/全站排行榜，动态时间线，收藏夹/稍后观看/观看历史，点赞/投币/一键三连等互动操作。当用户要求获取B站视频信息、下载音频、查询UP主信息、搜索B站内容、获取热门榜单、查看收藏夹、执行B站互动操作时使用。
version: 1.0.0
---

# yq-bilibili-skill - 哔哩哔哩数据抓取与互动

## 简介

这是一个基于 `bilibili-cli` 的Agent Skill，提供哔哩哔哩视频、音频、用户信息抓取以及互动功能的完整解决方案。

## 核心功能

### 1. 视频相关功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 视频详情 | `bili video <BV号>` | 获取视频基本信息 |
| 字幕 | `bili video <BV号> --subtitle` | 获取字幕(纯文本) |
| 字幕时间轴 | `bili video <BV号> --subtitle-timeline` | 获取带时间轴的字幕 |
| 导出SRT | `bili video <BV号> -st --subtitle-format srt` | 导出为SRT格式 |
| AI摘要 | `bili video <BV号> --ai` | 获取AI生成的视频摘要 |
| 评论 | `bili video <BV号> --comments` | 获取热门评论 |
| 相关视频 | `bili video <BV号> --related` | 获取相关视频推荐 |

### 2. 音频提取功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 下载并分割 | `bili audio <BV号>` | 下载音频并分割为25秒WAV片段 |
| 自定义片段时长 | `bili audio <BV号> --segment 60` | 设置60秒分割 |
| 完整音频 | `bili audio <BV号> --no-split` | 保持完整m4a格式 |
| 自定义输出目录 | `bili audio <BV号> -o ~/data/` | 指定输出路径 |

### 3. 用户相关功能

| 功能 | 命令 | 说明 |
|------|------|------|
| UP主资料 | `bili user <UID>` | 获取UP主个人资料 |
| 搜索用户 | `bili user "<用户名>"` | 按名称搜索用户 |
| UP主视频列表 | `bili user-videos <UID> --max 20` | 获取视频列表(最多20个) |

### 4. 发现与搜索功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 热门视频 | `bili hot` | 获取热门视频(第1页) |
| 分页热门 | `bili hot --page 2 --max 10` | 第2页,前10条 |
| 全站排行榜 | `bili rank` | 3日排行榜 |
| 自定义天数 | `bili rank --day 7 --max 30` | 7日榜,前30 |
| 搜索用户 | `bili search "<关键词>"` | 搜索用户 |
| 搜索视频 | `bili search "<关键词>" --type video --max 5` | 搜索视频 |
| 搜索分页 | `bili search "<关键词>" --page 2` | 下一页 |
| 动态时间线 | `bili feed` | 获取关注动态 |
| 分页动态 | `bili feed --offset <cursor>` | 通过cursor翻页 |

### 5. 收藏与历史功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 收藏夹列表 | `bili favorites` | 获取收藏夹列表 |
| 收藏夹内容 | `bili favorites --page 2` | 收藏夹视频(第2页) |
| 关注列表 | `bili following` | 获取关注列表 |
| 稍后观看 | `bili watch-later` | 获取稍后观看列表 |
| 观看历史 | `bili history` | 获取观看历史 |

### 6. 互动功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 点赞 | `bili like <BV号>` | 给视频点赞 |
| 投币 | `bili coin <BV号>` | 给视频投币 |
| 一键三连 | `bili triple <BV号>` | 点赞+投币+收藏 |
| 取关 | `bili unfollow <UID>` | 取消关注 |

### 7. 认证相关

| 功能 | 命令 | 说明 |
|------|------|------|
| 登录状态 | `bili status` | 检查登录状态 |
| 扫码登录 | `bili login` | QR码登录 |
| 个人信息 | `bili whoami` | 详细个人资料 |

## 输出格式

所有命令支持以下输出格式:

| 参数 | 说明 |
|------|------|
| `--yaml` | YAML格式输出(推荐用于AI处理) |
| `--json` | JSON格式输出(结构化数据) |

## 通用参数

| 参数 | 说明 |
|------|------|
| `--page N` | 分页号 |
| `--max N` | 最大结果数 |
| `--offset N` | 翻页游标 |
| `-o PATH` | 输出目录 |
| `--day N` | 排行榜天数(3或7) |

## 环境变量

```bash
# 覆盖默认输出模式
OUTPUT=yaml|json|rich|auto
```

## 认证说明

bilibili-cli采用3层认证策略:
1. **已保存凭证** - 从 `~/.bilibili-cli/credential.json` 加载
2. **浏览器Cookies** - 自动从Chrome/Firefox/Edge/Brave提取
3. **扫码登录** - `bili login` 在终端显示二维码

**权限说明:**
- 大部分命令无需登录
- 字幕/收藏/关注/稍后观看/历史/动态需要登录
- 点赞/投币/三连/取关/发布动态需要写入权限

## 常见问题排查

| 问题 | 解决方案 |
|------|----------|
| `需要登录` | 运行 `bili login` 扫码,或确保浏览器已登录bilibili |
| `HTTP 412` 限流 | 等待后重试,或减少 `--max` 数量 |
| `无法提取BV号` | 检查BV格式,必须是BV+10位字符 |
| `NetworkError` | 检查网络,代理需支持目标域名 |
| `不支持写操作` | 重新 `bili login` 获取完整权限 |

## 安装方式

```bash
# 推荐: uv工具(快速隔离)
uv tool install bilibili-cli

# 或: pipx
pipx install bilibili-cli

# 需要音频功能
uv tool install "bilibili-cli[audio]"
pipx install "bilibili-cli[audio]"
```

## 使用示例

### 示例1: 获取视频详情(AI友好格式)
```bash
bili video BV1ABcsztEcY --yaml
```

### 示例2: 下载音频并分割为ASR片段
```bash
bili audio BV1ABcsztEcY --segment 25 -o ./audio/
```

### 示例3: 搜索并获取视频评论
```bash
bili search "Python教程" --type video --max 10
bili video BV1xxx --comments --yaml
```

### 示例4: 获取UP主全部视频
```bash
bili user-videos 946974 --max 50
```

### 示例5: 查看热门榜单
```bash
bili hot --page 1 --max 20
bili rank --day 7
```

### 示例6: 登录并执行互动
```bash
bili login
bili triple BV1ABcsztEcY --json
```
