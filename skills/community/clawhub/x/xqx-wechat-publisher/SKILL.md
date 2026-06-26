---
name: wechat-publisher
description: "Markdown 发布为微信公众号草稿（wenyan-cli；主题、代码高亮）。公众号发布。"
metadata:
  openclaw:
    requires:
      env:
        - WECHAT_APP_ID
        - WECHAT_APP_SECRET
    primaryEnv: WECHAT_APP_SECRET
---

# wechat-publisher

## Agent Instructions

**触发条件**：用户提到「发布到公众号」「wechat publish」「公众号发布」等。

**执行流程**：
1. 确认 Markdown 文件路径
2. 检查 frontmatter 是否包含 `title` 和 `cover`
3. **若 cover 缺失**：调用 xqx-image-generator 生成封面（见「图片生成」）
4. **若正文需配图**：调用 xqx-image-generator（见「图片生成」）
5. **图片必须本地化**：生成后下载到文章目录（如 `./assets/`），frontmatter 与正文用本地路径，**禁止只用 URL**
6. 在 wechat-publisher 目录执行：`python scripts/publish.py <path>`；失败见 [references/troubleshooting.md](references/troubleshooting.md)

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `WECHAT_APP_ID` | 是 | 公众号 AppID |
| `WECHAT_APP_SECRET` | 是 | 公众号 AppSecret |

**`WECHAT_APP_ID` 与 `WECHAT_APP_SECRET` 必须同时配置，缺一不可**（缺一则 `publish.py` 无法取 token）。`metadata.openclaw.primaryEnv` 仅用于注册表/客户端标示「主凭证」字段，**两项均在 `requires.env` 中且均为必填**。

可由进程环境注入，或由 `publish.py` 从工作空间的 `TOOLS.md` 中获得 `WECHAT_APP_ID` / `WECHAT_APP_SECRET`的值。勿将真实凭证提交到 Git。运行机 IP 须在 [公众平台](https://mp.weixin.qq.com/) → 开发 → 基本配置 → **IP 白名单**。

## 图片生成

调用 **xqx-image-generator** 文生图；该 skill **只返回图片 URL**，须**自行下载**到文章目录（如 `./assets/cover.jpg`），frontmatter / 正文写本地路径。

**封面（cover 缺失）**：提示词用文章 `title` + 用户指定风格；宽高比默认 16:9；`cover: ./assets/cover.jpg`

**正文配图**：提示词按用户指定或上下文；默认 16:9；正文 `![](./assets/xxx.jpg)`

## 运行要求与命令

- **Python**：执行 `publish.py`
- **npm / Node**：首次需安装 `wenyan-cli`（脚本会执行 `npm install -g @wenyan-md/cli`）；之后依赖 `wenyan` 命令

**Frontmatter**（缺一报错「未能找到文章封面」）：

```markdown
---
title: 文章标题（必填）
cover: ./assets/cover.jpg
---

# 正文...
```

**发布**（cwd 为 wechat-publisher）：

```
cd $OPENCLAW_WORKSPACE/wechat-publisher
python scripts/publish.py /path/to/article.md
```

主题与高亮：`python scripts/publish.py article.md [theme] [highlight]`，默认 `lapis`、`solarized-light`。失败最多再试 3 次。

## 核心约束

| 项目 | 要求 |
|------|------|
| title | 必填 |
| cover | 必填（官方文档可省 cover，当前工具链实测需填） |
| 图片 | 本地路径；wenyan 上传素材 |
| 代码块 | 自动高亮 + Mac 风格 |

## 参考资料

- [references/themes.md](references/themes.md)
- [references/troubleshooting.md](references/troubleshooting.md)
