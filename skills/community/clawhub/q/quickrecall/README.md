# 宙一记忆系统 v3 — 初始化说明

## 架构

本系统把封装技能中的记忆引擎能力**内化到工作区**。

```
memo-lib/
├── memory.js          ← 记忆引擎核心（从封装技能复制，适度精简）
├── MEMORY_STORE.json  ← 持久化存储文件（自动管理，不要手动编辑）
└── README.md          ← 本文件

scripts/
└── memo.cjs           ← CLI 工具：写入/检索/查询/压缩/状态
```

## 如何使用

### 写入一条记忆

```bash
node scripts/memo.cjs add "内容" [importance=1.0] [tag1,tag2]
```

### 检索记忆

```bash
node scripts/memo.cjs query "关键词" [k=5] [min_imp=0]
```

### 查看状态

```bash
node scripts/memo.cjs status
```

### 压缩旧记忆

```bash
node scripts/memo.cjs compact [group_size=5] [min_imp=0.5]
```

## 封装技能 vs 宙一记忆系统

封装技能（卖的产品）：
- 独立部署，接受外部请求
- x402 支付验证
- REST API 对外暴露
- 多租户隔离

宙一记忆系统（这里）：
- 本地文件持久化，直接读写
- 无支付、无网络依赖
- 在启动流程中自动调用（AGENTS.md）
- 只有我一个用户
- 但要完整保留：语义检索、权重、时间衰减、压缩能力
