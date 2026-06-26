# SeedDrop 快速上手

## 1. 安装

```bash
clawhub install seeddrop
```

## 2. 配置品牌资料

```bash
seeddrop setup
```

按提示输入：
- 产品/品牌名称
- 一句话描述
- 监控关键词（多个用逗号分隔）
- 使用的平台（bilibili, tieba, zhihu, xiaohongshu）
- 回复模式（approve = 人工审核, auto = 自动发送）

## 3. 添加平台凭证

```bash
seeddrop auth add bilibili
seeddrop auth add tieba
```

需要提供对应平台的 Cookie。推荐配合 SocialVault 管理凭证：

```bash
clawhub install socialvault
socialvault add bilibili
```

## 4. 运行监控

```bash
seeddrop monitor bilibili
seeddrop monitor tieba 编程
seeddrop monitor all
```

## 5. 查看报告

```bash
seeddrop report
seeddrop report weekly
```

## 平台 Cookie 获取

| 平台 | 必需字段 | 获取方式 |
|------|---------|---------|
| B站 | SESSDATA, bili_jct | 浏览器 DevTools → Application → Cookies |
| 贴吧 | BDUSS, STOKEN | 浏览器 DevTools → Network → 请求头 Cookie |
| 知乎 | z_c0, d_c0 | 浏览器 DevTools → Application → Cookies |
| 小红书 | a1, web_session | 浏览器 DevTools → Application → Cookies |

> **注意**：贴吧的 BDUSS 必须从请求头获取，Cookie-Editor 导出的 BDUSS_BFESS 不可用。

## 推荐搭配

安装 **SocialVault** 后可自动管理 Cookie 续期，特别是小红书（Cookie 仅 12 小时有效）。
