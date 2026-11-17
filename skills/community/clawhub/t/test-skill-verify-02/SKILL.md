---
name: huawei-cloud-cce-list
description: 查询华为云CCE（云容器引擎）集群列表，支持表格化输出集群名称、状态、版本、节点数等关键字段
version: 1.0.0
triggers:
  - 查询华为云CCE集群
  - 列出CCE集群
  - CCE集群列表
  - 华为云容器集群查询
tools:
  - python3
  - huaweicloudsdk-cce
tags:
  - huawei-cloud
  - cce
  - query
  - cluster
  - list
---

# huawei-cloud-cce-list

## 安全硬约束
- AK/SK 仅从环境变量动态读取，不硬编码
- 所有 API 调用设 30s 超时
- 禁止将凭证写入日志、文件或评论
- 认证失败时不重试，直接输出明确错误信息

## Overview / 概述

查询华为云CCE（云容器引擎）集群列表的skill，通过huaweicloudsdk-cce调用CCE ListClusters API，获取指定区域下的所有集群信息并以表格形式输出。

**架构**：用户 → Python脚本 → huaweicloudsdk-cce → 华为云CCE API → 格式化输出

**适用场景**：
- 日常巡检：快速查看所有集群运行状态
- 资源管理：统计集群数量和版本分布
- 运维排障：查看集群版本和节点数量

## Prerequisites / 前置条件

1. Python 3.8+
2. 安装依赖：`pip install huaweicloudsdk-cce huaweicloudsdk-core`
3. 华为云AK/SK凭证（环境变量）：

   ```bash
   export HUAWEICLOUD_SDK_AK=your_access_key
   export HUAWEICLOUD_SDK_SK=your_secret_key
   ```
4. IAM 权限：需要 `cce:cluster:list` 权限

## Workflow / 工作流

1. 脚本启动 → 加载 AK/SK 环境变量
2. 初始化 BasicCredentials + CCE Client
3. 调用 ListClusters API
4. 解析响应 -> 提取名称/状态/版本/节点数
5. 表格化输出 -> 含表头和分隔线
6. 错误处理 -> 分类提示

## Core Commands / 核心命令

### 查询所有集群

```bash
python3 scripts/huawei-cloud-cce-list.py
```

### 指定区域查询

```bash
python3 scripts/huawei-cloud-cce-list.py --region cn-north-1
```

### 显示帮助

```bash
python3 scripts/huawei-cloud-cce-list.py --help
```

### 输出格式

```
名称            | 状态     | 集群版本  | 节点数
----------------|----------|-----------|--------
my-cluster       | Available | v1.27.3   | 3
```

## Parameter Confirmation / 参数确认

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--region` | 华为云区域 | `cn-north-4` |
| `--help` | 显示帮助 | - |

## KooCLI Command Format Standard

本 skill 使用 SDK 模式（huaweicloudsdk-cce），通过 Python SDK 直接调用 API，不涉及 KooCLI 命令格式。

## Reference Documents / 参考文档

- [SDK Center - CCE](https://console.huaweicloud.com/apiexplorer/#/ssdkcenter)
- [CCE API Reerence](https://support.huaweicloud.com/aipcecce/index.html)
- [CCE ListClusters](https://apiexplorer.developer.huaweicloud.com/apiexplorer/doc?product=CCE&api=ListClusters)
- [IAM 权限](references/iam-policies.md)
- [验证方法](references/verification-method.md)
- [数据流](references/dataflow-diagram.md)
- [验收标准](references/acceptance-criteria.md)