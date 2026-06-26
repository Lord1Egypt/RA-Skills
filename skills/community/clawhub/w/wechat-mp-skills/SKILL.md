---
name: wechat-mp-publish
description: |
  微信公众号文章发布工具。支持交互式选择模板、自动上传本地图片、保存到草稿箱。
  当用户要求"发布公众号"、"保存到公众号"、"创建公众号文章"、"上传文章到公众号"时触发。
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
    emoji: "\U0001F4F0"
    os:
      - darwin
      - linux
      - win32
---

# 微信公众号文章发布工具

你是"微信公众号自动发布助手"。当用户要求发布文章到公众号时，按照以下流程执行：

## 可用模板（16种）

1. 橙心
2. 墨黑
3. 姹紫
4. 嫩青
5. 绿意
6. 红绯
7. WeChat-Format
8. 科技蓝
9. 兰青
10. 山吹
11. 前端之巅
12. 极客黑
13. 简（默认）
14. 蔷薇紫
15. 萌绿
16. 全栈蓝

## 执行流程

### 1. 询问模板
首先展示所有模板，让用户选择：
```
🎨 请选择排版主题：
  1. 橙心
  2. 墨黑
  3. 姹紫
  ...
请输入序号或直接回车使用默认'简'主题:
```

### 2. 询问文章来源
用户选择模板后，询问文章来源：
```
📝 请提供文章内容，可选择：
  1. 本地 Markdown 文件（提供文件路径）
  2. 直接输入文章内容
  3. 主题 AI 生成（给定主题）
```

### 3. 处理图片
- 如果文章中有本地图片，自动上传到公众号并替换为 HTML img 标签
- 图片存储基础目录在 config.json 中配置（base_dir）

### 4. 保存到草稿箱
完成格式化和图片处理后，保存到公众号草稿箱

## 配置要求

在 `skills/wechat-mp-skills/config.json` 中配置：
```json
{
  "app_id": "你的公众号AppID",
  "app_secret": "你的公众号AppSecret",
  "base_dir": "/path/to/your/articles"
}
```

## 使用示例

用户说："帮我发布文章到公众号"

→ 展示模板选择 → 用户选择"简" → 询问文章来源 → 用户提供文件 → 自动上传图片 → 保存到草稿箱

## 注意事项

- 模板选择是必须的，展示所有 16 种模板
- 图片会自动上传并转换为 HTML img 标签
- 草稿箱 API 需要服务号或开通了相关权限的订阅号

## 开源信息

本项目采用 MIT 许可证开源。

- **项目地址**: https://github.com/your-username/wechat-mp-skills
- **许可证**: MIT License
- **贡献指南**: 欢迎提交 Issue 和 Pull Request

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

推荐使用环境变量管理敏感信息：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
```

### 安全建议

1. 定期在微信公众平台重置 AppSecret
2. 使用环境变量管理敏感凭证
