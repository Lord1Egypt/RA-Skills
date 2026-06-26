# 小红书自动化技能 V2

基于 Chrome DevTools Protocol (CDP) 的小红书完整自动化方案。

## 功能特性

- ✅ **认证登录** - 二维码登录、手机号验证码登录
- ✅ **内容发布** - 图文发布、视频发布、长文发布
- ✅ **搜索发现** - 关键词搜索、首页浏览、笔记详情
- ✅ **社交互动** - 评论、回复、点赞、收藏
- ✅ **复合运营** - 竞品分析、热点追踪

## 修复记录 (v2.0.0)

### 2026-03-07
- **修复 Chrome 启动问题** - 添加 `--no-sandbox` 和 `--disable-setuid-sandbox` 参数，支持 root 用户运行
- **优化登录流程** - 支持二维码和手机号两种登录方式
- **验证发布功能** - 成功发布测试帖子

## 快速开始

```bash
# 1. 检查登录状态
python scripts/cli.py check-login

# 2. 登录（二维码）
python scripts/cli.py login

# 3. 发布图文
python scripts/cli.py publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/path/to/image.jpg"
```

## 命令参考

### 认证管理
| 命令 | 功能 |
|------|------|
| `check-login` | 检查登录状态 |
| `login` | 二维码登录 |
| `phone-login --phone <号码> --code <验证码>` | 手机号登录 |
| `delete-cookies` | 退出登录 |

### 内容发布
| 命令 | 功能 |
|------|------|
| `publish` | 发布图文 |
| `publish-video` | 发布视频 |
| `long-article` | 发布长文 |

### 搜索发现
| 命令 | 功能 |
|------|------|
| `list-feeds` | 获取首页推荐 |
| `search-feeds --keyword <关键词>` | 搜索笔记 |
| `get-feed-detail --feed-id <ID>` | 查看笔记详情 |
| `user-profile --user-id <ID>` | 查看用户主页 |

### 社交互动
| 命令 | 功能 |
|------|------|
| `post-comment --feed-id <ID> --content <内容>` | 发表评论 |
| `reply-comment --comment-id <ID> --content <内容>` | 回复评论 |
| `like-feed --feed-id <ID>` | 点赞/取消点赞 |
| `favorite-feed --feed-id <ID>` | 收藏/取消收藏 |

## 技术架构

- **Chrome CDP** - 通过 Chrome DevTools Protocol 控制浏览器
- **反检测机制** - 模拟真实用户行为，绕过平台检测
- **Cookie 持久化** - 登录状态自动保存，下次免登录

## 目录结构

```
xiaohongshu-v2/
├── scripts/
│   ├── cli.py              # 主 CLI 入口
│   ├── chrome_launcher.py  # Chrome 启动器
│   └── xhs/                # 核心模块
│       ├── cdp.py          # CDP 封装
│       ├── login.py        # 登录逻辑
│       ├── publish.py      # 发布逻辑
│       ├── search.py       # 搜索逻辑
│       ├── comment.py      # 评论逻辑
│       ├── stealth.py      # 反检测参数
│       └── selectors.py    # CSS 选择器
├── skill.json
└── SKILL.md
```

## 依赖

- Python 3.10+
- Google Chrome 120+
- 见 `requirements.txt`

## 许可证

MIT
