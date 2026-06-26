# 云效工作项管理 Skill

通过云效 OpenAPI 管理工作项（任务、需求、缺陷等）。

## 安装后配置

安装此 skill 后，需要编辑 `config.json` 填写你的云效信息：

```json
{
  "org_id": "你的组织ID",
  "token": "你的个人访问令牌",
  "user_id": "你的用户ID",
  "default_project": "默认项目名称",
  "default_project_id": "默认项目ID"
}
```

### 获取方式

1. **组织 ID (org_id)**：云效组织管理后台 → 基本信息
2. **个人访问令牌 (token)**：云效个人设置 → 个人访问令牌 → 创建令牌
   - 权限需要：项目协作 > 工作项 > 读写
3. **用户 ID (user_id)**：可通过 API 或云效后台获取

## 功能

- 查询项目列表
- 查询工作项详情
- 创建工作项（任务、需求、缺陷等）
- 更新工作项标题、描述

## 使用示例

```
# 查询项目
python3 scripts/list_projects.py

# 创建任务（需指定项目）
python3 scripts/create_workitem.py --subject "任务标题" --project "项目名"

# 查询任务详情
python3 scripts/get_workitem.py <workitem_id>
```