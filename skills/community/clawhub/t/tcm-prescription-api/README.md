# 中医药方剂查询 (TCM Prescription API)

中医药方剂 API 查询技能。通过 REST API 接口查询中医药方剂数据库，支持方剂搜索、详情查看、分类浏览和症状推荐。

## 功能特性

- **方剂搜索**：按关键词或分类搜索方剂，支持模糊匹配
- **方剂详情**：查看方剂的完整资料，包括组成、功用、主治、方解、方歌、用法用量、禁忌、加减变化
- **分类浏览**：浏览 20 大方剂分类（解表剂、清热剂、补益剂等）
- **症状推荐**：根据症状描述智能推荐匹配方剂
- **API Key 认证**：注册用户获取完整访问权限

## 快速开始

### 1. 获取 API Key

1. 访问 [中医药方网站](https://119.91.226.122) 注册账号
2. 登录后在「个人中心」生成 API Key
3. 配置环境变量：`export TCM_API_KEY=<your_key>`

### 2. 使用 API

```bash
# 搜索方剂（无需认证）
curl -s "https://119.91.226.122/api/prescriptions/search?q=桂枝汤"

# 查看方剂详情（无需认证）
curl -s "https://119.91.226.122/api/prescriptions/1"

# 浏览方剂分类（无需认证）
curl -s "https://119.91.226.122/api/prescriptions/categories"

# 根据症状推荐方剂（需要 API Key）
curl -s -X POST "https://119.91.226.122/api/prescriptions/recommend" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TCM_API_KEY" \
  -d '{"symptoms": ["头痛", "发热", "恶风"]}'
```

## API 基础信息

| 项目 | 值 |
|------|-----|
| API 基础地址 | `https://119.91.226.122/api` |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 速率限制 | 每分钟 100 次请求 |
| 认证方式 | API Key（请求头 `X-API-Key`） |

## 技能文件

```
tcm-prescription-api/
├── SKILL.md              # 技能主文件（触发条件、执行流程）
├── README.md             # 本文件
├── references/
│   └── api-reference.md  # API 完整参考文档
└── scripts/
    └── query_prescriptions.sh  # 命令行查询工具
```

## 在 CodeBuddy 中使用

安装此技能后，直接用自然语言查询方剂：

- "查一下桂枝汤"
- "麻黄汤的组成是什么"
- "解表剂有哪些方剂"
- "头痛发热恶风，推荐什么方剂"

API Key 通过环境变量 `TCM_API_KEY` 配置，无需在对话中直接输入。

## 依赖

- `curl` - HTTP 请求
- `python3` - JSON 格式化

## 开发者

- **Phal Studio**
- 客服邮箱：guest@phalstudio.tech

## 许可

MIT-0
