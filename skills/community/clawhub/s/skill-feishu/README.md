# README.md - skill-feishu

这个 skill 用于**收集和记录飞书开放平台的 API 文档**，存放在 `open-apis/` 目录下。

## 目的

将飞书开放平台的 API 文档整理成本地 Markdown 文档，方便离线查阅和引用。

## 目录结构

```
skills/skill-feishu/
├── SKILL.md          - Skill 使用规范和规则说明
├── README.md         - 本文档
└── open-apis/        - 飞书 API 文档集合
    ├── README.md     - API 分类说明
    ├── TEMPLATE.md   - API 文档模板
    └── *.md          - 各 API 的完整文档
```

## API 分类

| 分类 | 说明 |
|------|------|
| `auth-*.md` | 认证相关 API（tenant_access_token, user_access_token） |
| `authen-*.md` | OAuth 2.0 认证 API |
| `contact-v3-*.md` | 通讯录 v3 API（用户、部门管理） |
| `im-*.md` | 消息 API |
| `passport-*.md` | 用户登录信息 API |

## 使用说明

1. 查看 `SKILL.md` 了解文档收集规则和禁止操作
2. 参考 `open-apis/TEMPLATE.md` 创建新的 API 文档
3. 已记录的 API 列表见 `open-apis/README.md`
