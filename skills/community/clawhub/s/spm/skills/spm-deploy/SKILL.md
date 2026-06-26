---
name: spm-deploy
version: 1.0.0
description: 部署规范 — 部署模式/回滚/监控/环境管理。SPM Phase 5 自动引用。
---

# SPM Deploy — 部署规范

## 自动检测

SPM Phase 5 交付阶段自动引用本技能。

## 独立使用

"按 spm-deploy 规范部署这个项目。"

---

## 部署模式

| 模式 | 怎么工作 | 适合 |
|------|---------|------|
| **滚动更新** | 逐个替换实例，始终保持在线 | 无状态服务 |
| **蓝绿部署** | 新版本全量部署，切换流量 | 需要秒级回滚 |
| **金丝雀** | 新版本先 10% 流量，验证后全量 | 高风险变更 |

```bash
# ✅ 简单项目的滚动更新
docker compose pull
docker compose up -d --no-deps app

# ✅ 需要验证的金丝雀
# 1. 部署 canary 实例
# 2. 10% 流量路由到 canary
# 3. 监控 5 分钟（错误率/延迟）
# 4. OK → 100% 流量 / 不OK → 撤回
```

---

## 回滚

```
✅ 每次部署前记录当前版本 → 一键回滚
✅ 数据库迁移有 DOWN 脚本
✅ 回滚后跑 smoke test

❌ "改了一行，不会有问题" → 不准备回滚
❌ 改 schema 没有 DOWN 迁移
```

```bash
# 快速回滚
git revert HEAD --no-edit && git push
# 或
docker compose up -d app  # 用旧镜像重启
```

---

## 环境管理

```
✅ 环境严格分离: development / staging / production
✅ staging 和生产环境一致（同样数据库、同样配置规模）
✅ .env.example 在仓库，.env.production 在密钥管理服务
✅ 生产环境用密钥管理服务（不是 .env 文件）

❌ staging 用 SQLite，生产用 PostgreSQL
❌ "这个配置只在生产需要，staging 不需要"
❌ 生产密钥在 .env 里，跟代码同级目录
```

---

## 部署检查清单

```
部署前:
□ 所有测试通过
□ CI 绿色
□ staging 验证通过
□ 回滚方案已准备
□ 数据库迁移已测试

部署中:
□ 先部署到 staging
□ 跑 smoke test: curl /health
□ 检查错误日志

部署后:
□ 监控 5 分钟（错误率、延迟、CPU）
□ 通知相关方
□ 异常 → 立即回滚
```

---

## Agent 部署反模式

| # | 反模式 | 后果 |
|---|--------|------|
| 1 | 不准备回滚 | 回不去了 |
| 2 | 生产环境手动改文件 | 下个人不知道改了什么 |
| 3 | "staging 不用测，直接上生产" | staging 白建了 |
| 4 | 部署后不监控 | 部署成功了，服务 30 秒后挂了，没人知道 |
| 5 | 密钥硬编码在 Dockerfile | 镜像一推，密钥全网可见 |
