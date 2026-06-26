# 微信公众号文章自动发布 Skill - 技术方案

## 📋 项目概述

开发一个 OpenClaw Skill，用于自动发布微信公众号文章。

## 🎯 功能需求

### 核心功能
1. **微信 API 认证**: 使用 AppID/AppSecret 获取 Access Token
2. **文章素材上传**: 支持上传封面图片、正文图片、视频等
3. **图文消息创建**: 组装图文消息（标题、作者、封面、正文等）
4. **文章发布**: 支持草稿箱保存和群发发布
5. **发布状态查询**: 查询文章发布状态

### 扩展功能（后续版本）
- 草稿管理（列表、编辑、删除）
- 已发布文章管理
- 定时发布
- 分组群发

## 🛠 技术方案

### 技术栈
- **语言**: TypeScript
- **运行时**: Node.js (>=18)
- **依赖**:
  - `axios`: HTTP 请求
  - `form-data`: 文件上传
  - `typescript`: 类型支持

### 项目结构

```
wechat-mp-publisher/
├── SKILL.md                    # Skill 定义文件
├── README.md                   # 项目说明
├── package.json                # 依赖配置
├── tsconfig.json               # TypeScript 配置
├── src/
│   ├── index.ts               # 主入口
│   ├── auth.ts                # AccessToken 管理
│   ├── media.ts               # 素材上传
│   ├── article.ts             # 图文消息管理
│   └── types.ts               # 类型定义
├── scripts/
│   ├── publish.ts             # 发布文章 CLI
│   ├── upload-media.ts        # 上传素材 CLI
│   └── query-status.ts        # 查询状态 CLI
├── config/
│   └── default.json           # 默认配置模板
└── tests/
    └── *.test.ts              # 测试文件
```

### OpenClaw Tool 设计

```yaml
tools:
  wechat-mp-publish:
    description: 发布微信公众号文章
    params:
      title: 文章标题
      content: 正文内容 (支持 HTML)
      author: 作者名 (可选)
      cover_media_id: 封面图片 media_id
      digest: 摘要 (可选)
      content_source_url: 原文链接 (可选)
      publish: 是否立即发布 (默认 false，保存为草稿)
  
  wechat-mp-upload-media:
    description: 上传素材到微信服务器
    params:
      file_path: 本地文件路径
      type: 素材类型 (image/thumb/video)
  
  wechat-mp-query-draft:
    description: 查询草稿列表
    params:
      offset: 分页偏移
      count: 每页数量
  
  wechat-mp-delete-draft:
    description: 删除草稿
    params:
      media_id: 草稿 media_id
```

### 配置文件设计

```json
{
  "wechat_mp": {
    "app_id": "your-app-id",
    "app_secret": "your-app-secret",
    "access_token_cache_file": "~/.openclaw/.wechat_mp_token.json"
  },
  "defaults": {
    "author": "默认作者名"
  }
}
```

## 🔐 安全设计

1. **Token 缓存**: AccessToken 缓存到本地文件，避免频繁请求
2. **配置隔离**: 配置文件放在 ~/.openclaw/ 下，不提交到版本控制
3. **环境变量支持**: 支持通过环境变量配置敏感信息

## 📚 微信 API 参考

### 获取 Access Token
```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

### 上传图文消息内的图片
```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=ACCESS_TOKEN
Content-Type: multipart/form-data
```

### 上传图文消息素材
```
POST https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=ACCESS_TOKEN
Content-Type: application/json
```

### 发布草稿
```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN
```

## 📅 开发计划

| 阶段 | 任务 | 预计时间 |
|-----|------|---------|
| 1 | 项目初始化和基础结构 | 30分钟 |
| 2 | AccessToken 管理模块 | 30分钟 |
| 3 | 素材上传模块 | 45分钟 |
| 4 | 图文消息管理模块 | 45分钟 |
| 5 | CLI 工具封装 | 30分钟 |
| 6 | Skill 文档编写 | 20分钟 |
| 7 | 测试和调试 | 30分钟 |

总计: 约 4 小时

## ⚠️ 注意事项

1. 微信认证服务号才有群发接口权限
2. 测试号只能发布给管理员
3. 发布前需要在微信公众平台配置 IP 白名单
4. 群发接口每月有次数限制

## ✅ 验收标准

- [ ] 能正确获取和缓存 AccessToken
- [ ] 能上传图片素材并获取 media_id
- [ ] 能创建图文消息并保存为草稿
- [ ] 能通过 OpenClaw Tool 发布文章
- [ ] 有完整的错误处理
- [ ] 文档完整
