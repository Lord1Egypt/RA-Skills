# 发布到 ClawHub

> 这是一个 **适配 wewe-rss 的公众号抓取与文档导出工具**。

## 发布前检查

确保仓库根目录包含：

- `SKILL.md`
- `manifest.yaml`
- `_meta.json`
- `README.md`
- `LICENSE`
- `scripts/`

## 建议仓库名

建议使用：

- GitHub 仓库名：`wewe-rss-wechat-export`
- ClawHub slug：`wewe-rss-wechat-export`
- 展示名称：`wewe-rss WeChat Export`

## 发布方式一：从 skill 目录直接发布

```bash
clawhub login
clawhub publish . --slug wewe-rss-wechat-export --name "wewe-rss WeChat Export" --version 1.0.0 --tags "wewe-rss,wechat,public-account,export,docx" --changelog "Initial public release."
```

## 发布方式二：从 zip 包发布

```bash
clawhub login
clawhub publish . \
  --slug wewe-rss-wechat-export \
  --name "wewe-rss WeChat Export" \
  --version 1.0.0 \
  --tags "wewe-rss,wechat,public-account,export,docx" \
  --changelog "Initial public release."
```

## 发布文案建议

### 名称

`wewe-rss WeChat Export`

### 简介

适配 wewe-rss 的公众号抓取与文档导出工具。可将微信公众号 / JSON feed 批量导出为清洗后的 DOCX 文档，并支持日期前缀命名、完整验收产物保留与 zip 打包。

### 标签

- wewe-rss
- wechat
- public-account
- export
- docx

## 发布后安装

用户可通过 ClawHub / OpenClaw 安装并使用这个 skill。

## 注意事项

1. 真实发布前请确认作者名、仓库地址和版本号
2. 如果要公开 GitHub 仓库，请检查是否包含不该公开的本地路径或测试产物
3. 若后续做大版本更新，请同步修改：
   - `manifest.yaml`
   - `_meta.json`
   - `CHANGELOG.md`
