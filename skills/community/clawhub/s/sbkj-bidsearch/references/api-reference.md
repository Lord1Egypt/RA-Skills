# 接口索引

基地址：`https://gate.gov-bid.com/outer-gateway/bid`。所有接口 Key 从安全配置读取。

## 招中标项目

| 场景 | 方法路径 |
| --- | --- |
| 普通搜索 | `/searchProjectApi` |
| 项目编号搜索 | `/getProjectByProjectNumber` |
| 官方结构化详情 | `/getZTBStructreDetail` |
| 正文详情 | `/getZTBProjectDetail` |
| 附件列表 | `/getZTBProjectFiles` |
| AI专用搜索 | `/SearchProjectForAI` |
| 合同搜索 | `/searchProjectContactApi` |
| AI重写搜索条件 | `/aiSearchSubmitPolling` |
| AI行业搜索 | `/industryReasoning` |
| 采集源网址 | `/getCollectUrl` |

## 企业画像

| 场景 | 方法路径 |
| --- | --- |
| 企业基本信息 | `/companyProfileSummary` |
| 企业联系电话 | `/companyProfileContacts` |
| 企业合作客户 | `/companyProfileCustomers` |
| 企业供应商 | `/companyProfileSuppliers` |

## 拟在建项目

| 场景 | 方法路径 |
| --- | --- |
| 搜索 | `/searchNZJProjectApi` |
| 详情 | `/getNZJProjectDetail` |
| 附件 | `/getNZJProjectFileList` |

## AI模型训练定制化

| 场景 | 方法路径 |
| --- | --- |
| LLM招中标结构化 | `/ztbAiStructureInfo` |
| 招中标分类推理 | `/categoryReasoning` |

详细请求参数、响应字段和示例以用户提供的 `接口文档_2026-07-30.md` 为准；实现接口时按业务场景读取本 Skill 的工作流文件，不要只根据接口名猜测字段。
