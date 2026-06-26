# Phase 4B 实施计划 — npm 包化 + 增强

> **方案版本：** v6 Final
> **状态：** 🎉 **全部完成**
> **更新日期：** 2026-05-06

---

## 4B1：Cloud Functions npm 包化（W1-2）

### 状态：✅ 完成

| 交付项 | 文件 | 说明 |
|--------|------|------|
| @website-skeleton/shared | `packages/shared/package.json` + src/index.js | v3.0.0，导出 sharing/ 全部模块 |
| @website-skeleton/payment | `packages/payment/package.json` + src/index.js | v1.0.0，支付验证工具函数 |
| @website-skeleton/admin | `packages/admin/package.json` + src/index.js | v1.0.0，租户管理函数 |
| 根 package.json | `package.json`（新建） | monorepo workspaces + type:module + build/test/publish scripts |
| npm 发布工作流 | package.json scripts | `npm run publish:all` 一键发布三个包 |

## 4B2：Edge auth 内联 + 构建同步（W2-3）

### 状态：✅ 完成

| 交付项 | 文件 | 说明 |
|--------|------|------|
| sync-sharing.js | `scripts/sync-sharing.js` | --check/--sync/--ci 三种模式，md5Dir + copy + hash verify |
| CI 集成 | package.json scripts | `npm run build` 调用 sync-sharing.js |

同步验证：✅ 3 个目标目录全部一致（npm package / Edge inline / Cloud shared）

## 4B3：版本兼容性基础设施（W3-4）

### 状态：✅ 完成

| 交付项 | 文件 | 说明 |
|--------|------|------|
| CHANGELOG.md | `CHANGELOG.md` | v1.0→v2.x→v3.0 完整变更记录 |
| MIGRATION.md | `MIGRATION.md` | Phase 3→4A 零停机迁移指南（DB/JWT/KV/API/权限） |
| semver 策略 | CHANGELOG.md 头部 | 明确 Major/Minor/Patch 定义 |

## 4B4：支付回调二次加固

### 状态：✅ **已在 4A W4 完成**
- cloud-functions/api/pay/wx-notify.js（移入 Cloud Functions，修复 import 路径）

## 4B5：KV 热 key 分散

### 状态：✅ 完成

| 交付项 | 文件 | 说明 |
|--------|------|------|
| FNV-1a hash | `sharing/kv-keys.js` | fnv1a() + getShardSessionKey(tenant, sessionId, 64) |
| 触发条件 | 文档注释 | KV 延迟 > 200ms 持续 5 分钟 → P2 告警 |

## 4B6：计费 MVP — KV 计数器

### 状态：✅ 完成

| 交付项 | 文件 | 说明 |
|--------|------|------|
| 滑动窗口计数 | `sharing/quota.js` | getSlidingWindowCount() 60分钟窗口，1分钟槽位 |
| 计费事件记录 | `sharing/quota.js` | recordBillingEvent() 原子递增 |
| 403 升级提示 | `sharing/quota.js` | checkBillingQuota() → upgrade message |

## 最终验证

| 检查项 | 结果 |
|--------|------|
| 语法检查 | ✅ 全部通过 |
| 同步脚本验证 | ✅ 3 目标目录完全一致 |
| Phase 4B 总计 | **6/6 子项全部完成** |

### 集成测试结果（本地纯逻辑）

| 分类 | 通过 | 需部署 | 总计 |
|------|------|--------|------|
| 功能测试（F1-F6） | 6 | 0 | 6 |
| 安全测试（S-01~S-08） | 5 | 2（S-05, S-07） | 7* |
| **总计** | **11** | **2** | **13** |

> *S-03（超配额）需要实际操作 KV，当前版本暂未计入。2 项待部署 EdgeOne 后运行。|
