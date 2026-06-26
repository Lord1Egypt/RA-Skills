# TAPD API 配置示例

## tapd.json 配置

```json
{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret",
  "workspaces": [
    {
      "id": "12345678",
      "name": "项目A",
      "default": true,
      "description": "主项目工作空间"
    },
    {
      "id": "87654321",
      "name": "项目B",
      "description": "次项目工作空间"
    }
  ]
}
```

## 环境变量配置（可选）

```bash
# 优先级高于 tapd.json
export TAPD_CLIENT_ID="your-client-id"
export TAPD_CLIENT_SECRET="your-client-secret"
export TAPD_WORKSPACE_ID="12345678"
```

## OAuth 应用设置

### 1. 应用信息

- **应用名称**: 自定义（例如：OpenClaw Integration）
- **应用类型**: 企业自建应用
- **回调地址**: 不需要（使用 client_credentials 模式）

### 2. 应用权限

必需权限：
- ✅ 需求 (stories)
- ✅ 任务 (tasks)  
- ✅ 缺陷 (bugs)
- ✅ 迭代 (iterations)

可选权限：
- 发布计划 (releases)
- 测试用例 (tcases)
- Wiki (wikis)
- 评论 (comments)

### 3. 安全设置

**IP 白名单**（推荐）：
```
# 本地开发
127.0.0.1
::1

# 办公网络
192.168.1.0/24

# 云服务器
203.0.113.50
```

## 工作空间 ID 获取

### 方法 1: 从 URL 获取

```
https://www.tapd.cn/12345678/prong/stories/view/1112345678001000001
                   ^^^^^^^^
                   workspace_id
```

### 方法 2: API 查询

```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  "https://api.tapd.cn/workspaces/projects"
```

返回：
```json
{
  "data": [
    {
      "Workspace": {
        "id": "12345678",
        "name": "示例项目",
        "creator": "...",
        "created": "2023-01-01"
      }
    }
  ]
}
```

## 状态码映射

### 需求状态 (Stories)

| 状态码 | 中文 | 英文 | 说明 |
|--------|------|------|------|
| planning | 规划中 | Planning | 需求池 |
| status_1 | 待评审 | To Review | 待评审 |
| status_2 | 待实现 | To Do | 已评审 |
| status_3 | 实现中 | In Progress | 开发中 |
| status_4 | 待验收 | To Verify | 待测试 |
| resolved | 已完成 | Resolved | 已完成 |
| closed | 已关闭 | Closed | 已关闭 |

### 优先级 (Priority)

| 值 | 标签 | 说明 |
|----|------|------|
| 1 | Low | 低 |
| 2 | Nice To Have | 中低 |
| 3 | Middle | 中 |
| 4 | High | 高 |

## API 限流规则

- **单应用**: 600 次/分钟
- **单工作空间**: 300 次/分钟
- **建议**: 批量查询 + 缓存

## 错误码参考

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | access_token 无效 | 重新获取 token |
| 403 | 应用未授权访问项目 | 在项目中安装应用 |
| 429 | 请求过于频繁 | 降低请求频率 |
| 500 | 服务器错误 | 稍后重试 |

## 字段说明

### 需求 (Story)

```json
{
  "id": "1112345678001000001",
  "name": "需求标题",
  "description": "需求描述",
  "status": "status_3",
  "priority": "4",
  "owner": "负责人;",
  "creator": "创建人",
  "created": "2026-03-05 09:54:14",
  "modified": "2026-03-05 10:00:00",
  "iteration_id": "1112345678001000002",
  "story_type": "user_story"
}
```

### 任务 (Task)

```json
{
  "id": "1112345678001000003",
  "name": "任务标题",
  "status": "status_3",
  "owner": "负责人;",
  "priority": "3",
  "created": "2026-03-05 10:00:00"
}
```

### 缺陷 (Bug)

```json
{
  "id": "1112345678001000004",
  "title": "缺陷标题",
  "status": "new",
  "current_owner": "当前处理人;",
  "priority": "4",
  "severity": "fatal",
  "created": "2026-03-05 11:00:00"
}
```
