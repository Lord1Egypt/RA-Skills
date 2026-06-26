# 飞书项目集成配置

> 本文件为研发统筹智能体与飞书项目 (Meegle) 的集成配置。
> 填写完毕后，智能体将在需求归档、任务拆解、开发/测试完成时自动同步飞书项目。

## 一、空间信息

- project_key: （必填，飞书项目空间标识，如 `MY_PROJECT`）
- project_name: （空间显示名称，用于确认）

## 二、工作项类型

> 通过 `workitem meta-types --project-key <project_key>` 获取可用类型。

- 需求: story
- 子任务: task
- 缺陷: bug

## 三、创建需求模板

> 通过 `workitem meta-fields --work-item-type story --project-key <project_key>` 获取可用模板。

- template_id: （必填，创建需求时使用的模板 ID）

## 四、状态映射

> 研发统筹阶段 → 飞书项目状态名称。根据项目实际工作流配置。

| 研发统筹阶段 | 飞书项目状态 |
|------------|------------|
| 需求已归档 | 待开发 |
| 开发中 | 开发中 |
| 开发完成 | 待测试 |
| 测试中 | 测试中 |
| 测试通过 | 已完成 |
| 测试不通过 | 待修复 |

## 五、角色映射（可选）

> 通过 `user search` 将姓名转换为 userkey。不填则创建时不指定负责人。

| 角色 | 姓名 | userkey |
|------|------|---------|
| 需求方 | | |
| 开发负责人 | | |
| 测试负责人 | | |

## 六、同步行为控制

- auto_sync: true （true = 自动同步；false = 仅手动触发）
- notify_on_sync: true （true = 每次同步后在对话中提示）
