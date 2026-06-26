# 通用 TeamBition 任务管理 Skill
支持多应用配置的 TeamBition 任务创建/查询工具，适配不同 Agent 绑定不同 TeamBition 应用。

## 配置项（Agent 绑定 Skill 时需填写）
| 配置名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| TEAMBITION_APP_ID | 字符串 | 是 | TeamBition 开放平台应用 ID |
| TEAMBITION_APP_SECRET | 字符串 | 是 | TeamBition 开放平台应用秘钥 |
| TEAMBITION_ACCESS_TOKEN | 字符串 | 否 | 预配置的访问令牌（可选，无则自动获取） |
| TEAMBITION_ORG_ID | 字符串 | 否 | 团队/组织 ID（可选） |
| TEAMBITION_DEFAULT_PROJECT_ID | 字符串 | 否 | 默认项目 ID（创建任务时可不传 project_id） |

## 调用参数（Agent 调用 Skill 时传参）
### 1. 创建任务（action=create_task）
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | 字符串 | 是 | 固定值：create_task |
| project_id | 字符串 | 否 | 项目 ID（无则用配置的默认值） |
| title | 字符串 | 是 | 任务标题 |
| content | 字符串 | 否 | 任务描述/内容 |
| assignee | 字符串 | 否 | 任务负责人 ID |

### 2. 查询任务（action=get_task）
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | 字符串 | 是 | 固定值：get_task |
| task_id | 字符串 | 是 | 任务 ID |

## 返回值说明
返回 TeamBition API 原始响应结果，创建任务成功示例：
{
  "code": 0,
  "data": {
    "_id": "task_xxxxxx",
    "title": "选品任务-无线充电器",
    "projectId": "proj_xxxxxx",
    "createdAt": "2026-03-18T10:00:00Z"
  }
}