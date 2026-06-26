# 小红书开放平台 API 配置指南

## 概述

小红书开放平台提供 API 接口用于笔记发布。使用前需在平台注册并创建应用，获取凭证后配置环境变量。

## 申请流程

### 1. 注册开发者

- 访问 [open.xiaohongshu.com](https://open.xiaohongshu.com)
- 使用小红书账号登录
- 完成开发者实名认证（企业或个人）

### 2. 创建应用

- 在控制台创建新应用
- 选择应用类目（根据实际用途选择）
- 申请「笔记发布」相关接口权限
- 获取 **App Key** 和 **App Secret**

### 3. 审核周期

- 通常 1–5 个工作日
- 需提交应用场景说明

### 4. 配置凭证

在 `~/.openclaw/.env` 或进程环境中设置：

```bash
export XIAOHONGSHU_APP_KEY=your_app_key
export XIAOHONGSHU_APP_SECRET=your_app_secret
```

## 接口说明

本 skill 使用的接口（以官方最新文档为准）：

| 接口 | 方法 | 路径 |
|------|------|------|
| 获取 Token | POST | `/api/v1/oauth2/access_token` |
| 上传图片 | PUT | `/api/media/v1/upload/web/permit` |
| 发布笔记 | POST | `/api/sns/v1/note/post` |

若接口变更，请以 [小红书开放平台文档](https://school.xiaohongshu.com/open) 为准。

## 限制与注意事项

- **内容审核**：发布的笔记需经平台审核，违规内容会被拒绝
- **频率限制**：API 有调用次数限制，避免短时间内大量发帖
- **图片要求**：JPG/PNG，单张 ≤10MB
- **标题长度**：≤20 字
- **正文长度**：≤1000 字
- **图片数量**：1-9 张

## 无凭证时的用法

未配置 API 凭证时，脚本自动切换到草稿模式，输出格式化内容供手动复制：

```bash
python3 scripts/post.py --title "标题" --content "正文" --tags "探店，咖啡"
```

## 常见问题

### Q: 个人账号能申请 API 吗？

A: 目前小红书 API 主要面向企业用户，个人账号较难申请。建议使用草稿模式或等待浏览器自动化功能。

### Q: 发布失败怎么办？

A: 检查以下几点：
1. API 凭证是否正确
2. 图片格式和大小是否符合要求
3. 内容是否违反社区规范
4. 是否超过频率限制

### Q: 如何批量发布？

A: 可以编写脚本循环调用 `post.py`，但注意控制频率，避免触发限流。
