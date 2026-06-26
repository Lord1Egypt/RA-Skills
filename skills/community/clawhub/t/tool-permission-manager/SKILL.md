---
name: tool-permission-manager
description: 工具分级授权 - 细粒度管理每个工具的使用权限
---

# Tool Permission Manager - 工具权限管理器

## 功能
对每个工具进行细粒度授权管理，控制谁能使用什么工具。

## 权限等级

### 1. 公开（Public）
无需确认，直接使用
| 工具 | 说明 |
|------|------|
| read | 读取文件 |
| web_search | 网络搜索 |
| 笔记相关 | 读写笔记 |

### 2. 警告（Warning）
使用前显示警告
| 工具 | 说明 |
|------|------|
| exec | 执行命令 |
| write | 写入文件 |

### 3. 审批（Approval）
使用前需确认
| 工具 | 说明 |
|------|------|
| message | 发送消息 |
| cron | 定时任务 |
| sessions | 会话管理 |

### 4. 禁止（Forbidden）
不可使用
| 工具 | 说明 |
|------|------|
| gateway | 网关配置 |
| delete | 删除文件 |

## 权限配置
```json
{
  "public": ["read", "web_search"],
  "warning": ["exec", "write"],
  "approval": ["message", "cron"],
  "forbidden": ["gateway", "delete"]
}
```

## 使用方式
自动根据工具类型判断权限等级。
用户可通过"授权XXX工具"动态调整权限。
