# Synapse Skills v2.0.0 发布说明

**发布日期**: 2026-04-10
**版本**: v2.0.0 (Brain/Hands 架构升级)

---

## 概述

v2.0.0 是 Synapse Skills 的重大架构升级。新增 synapse-brain 作为持久调度核心，实现 Brain/Hands 架构：

- **synapse-brain** (新增) — OpenClaw 持久调度 Agent，跨会话状态管理 + 多 Agent 编排
- **synapse-wiki** — 知识库管理系统（v2.0: Brain 兼容 + code 互操作）
- **synapse-code** — 代码开发工作流引擎（v2.0: Brain 集成 + wiki 互操作）

---

## 新增：synapse-brain

### 核心功能
- **Session 持久化** — state.json 跨会话恢复，不再从零开始
- **意图路由** — 自动识别用户意图并路由到正确的 Skill
- **子代理调度** — 管理 1-8 个子代理并行执行
- **状态可视化** — 随时查询项目进度

### 安装
```bash
git clone https://github.com/ankechenlab-node/synapse-brain.git
cd synapse-brain && ./install.sh
```

---

## synapse-code 升级

### 新增
- Brain/Hands 集成 — 可作为 Hand Agent 被 synapse-brain 调度
- wiki 互操作 — Pipeline 完成自动触发知识沉淀
- 4 种运行模式 — standalone / lite / full / parallel

### 变更
- 默认模式改为 standalone（降低新手门槛）
- 保留 `--legacy` flag 兼容旧 pipeline.py 工作流

---

## synapse-wiki 升级

### 新增
- Brain 兼容 — 可被 task_router 识别路由
- code 互操作 — 接收 synapse-code Pipeline 完成后的自动知识沉淀

---

## 安装方式

### 方式 1：从源码安装
```bash
git clone https://github.com/ankechenlab-node/synapse-brain.git
git clone https://github.com/ankechenlab-node/synapse-code.git
git clone https://github.com/ankechenlab-node/synapse-wiki.git

cd synapse-brain && ./install.sh
cd ../synapse-code && ./install.sh
cd ../synapse-wiki && ./install.sh
```

### 方式 2：从 ClawHub 安装
```bash
npx clawhub install synapse-brain
npx clawhub install synapse-code
npx clawhub install synapse-wiki
```

---

## 配置说明

### synapse-brain 配置
安装后自动生成 `config.json`：
```json
{
  "brain": {
    "state_dir": "~/.openclaw/brain-state",
    "auto_save": true,
    "skills": { "code": "synapse-code", "wiki": "synapse-wiki" }
  }
}
```

### synapse-code 配置
```json
{
  "pipeline": { "workspace": "~/pipeline-workspace", "auto_log": true },
  "interop": { "wiki_enabled": true, "wiki_root": "~/my-project/wiki" }
}
```

---

## 依赖要求

| 技能 | 依赖 |
|------|------|
| synapse-brain | Python 3.10+ |
| synapse-code | Python 3.x, npm (GitNexus 可选) |
| synapse-wiki | Python 3.x |

---

## 测试报告

| 技能 | 测试项 | 结果 |
|------|--------|------|
| synapse-brain | 意图分类 8/8, CRUD, Session, 子代理 | **全部通过** |
| synapse-code | 7 脚本语法, shell 语法 | **全部通过** |
| synapse-wiki | 6 脚本语法, shell 语法 | **全部通过** |

---

## 升级路径

### 从 v1.x 升级到 v2.0.0

1. 安装 synapse-brain（新依赖）
2. 更新 synapse-code 和 synapse-wiki
3. 旧 pipeline.py 工作流通过 `--legacy` flag 继续兼容
4. 建议：编辑 config.json 启用 wiki 互操作

---

## 反馈与支持

- GitHub Issues: https://github.com/ankechenlab-node/synapse-brain/issues
- GitHub Issues: https://github.com/ankechenlab-node/synapse-code/issues
- GitHub Issues: https://github.com/ankechenlab-node/synapse-wiki/issues

---

## 许可证

MIT License — 详见各项目 LICENSE 文件
