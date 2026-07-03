---
risk_level: LOW
high_risk_operations:
  - none
data_access: none
network_access: none
external_services: none
filesystem_write:
  - .standardization/semantic-split/data/*.json
description: >
  semantic-split 是纯 NL 处理+JSON 生成的技能。所有操作在 LLM 内部完成，
  不涉及网络请求、外部 API 调用或系统文件删除。仅写入标准化数据目录。
---

# permissions.md

## skill-standardization 权限声明头部

基于 skill-standardization 渐进式披露规范的权限说明

| 声明项 | 值 | 说明 |
|--------|-----|------|
 — 权限说明

## skill-standardization 权限声明头部

| 声明项 | 值 | 说明 |
|--------|-----|------|
| 风险等级 | LOW | 无网络请求、无文件删除、无敏感数据访问 |
| 文件删除操作 | 无 | json_manager.py 仅读写，不删除 |
| 网络请求 | 无 | 无外部 API 调用 |
| subprocess 调用 | 无 | 纯文件操作 |
| 敏感数据访问 | 无 | 不处理个人/敏感信息 |

## 风险等级：LOW

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 文件删除 | ✅ 无 | 无文件删除操作 |
| 网络请求 | ✅ 无 | 无外部 API/网络请求 |
| subprocess 调用 | ✅ 无 | json_manager.py 纯文件操作 |
| 敏感数据访问 | ✅ 无 | 不处理个人/敏感信息 |
