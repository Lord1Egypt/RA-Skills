---
name: viking-memory-ultra
description: >-
  Viking Memory System Ultra - 分层记忆基座。特性：动态回流（语义晋升）、智能权重（对数增长）、可逆归档（多粒度摘要）。
  核心脚本：sv_write, sv_read, sv_find, sv_autoload, sv_promote, sv_weight, sv_compress, sv_archive, sv_decompress。
version: 1.3.0
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env: ["VIKING_HOME", "SV_WORKSPACE"]
      bins: ["bash", "python3", "curl"]
    always: false
    os: ["linux", "darwin"]
---

# Viking Memory System Ultra v1.3.0

## 概述

Viking Memory System Ultra 是分层记忆管理系统，支持：
- 分层记忆: hot → warm → cold → archive
- 动态回流: 语义相似度驱动的冷记忆晋升
- 智能权重: 对数增长 + 上下文相关性
- 可逆归档: 多粒度摘要 + 按需解压

## 核心脚本

| 脚本 | 功能 |
|------|------|
| sv_write.sh | 写入记忆 |
| sv_read.sh | 读取记忆 |
| sv_find.sh | 搜索记忆 |
| sv_autoload.sh | 自动加载 |
| sv_promote.sh | 动态回流晋升 |
| sv_weight.sh | 权重计算 |
| sv_compress_v2.sh | 压缩调度 |
| sv_archive_summary.sh | 归档摘要 |
| sv_decompress.sh | 解压恢复 |

## 安装

```bash
clawhub install viking-memory-ultra
```
