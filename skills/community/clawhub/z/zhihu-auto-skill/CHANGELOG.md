# 变更日志

## v2.0.0 (2026-05-09)

### 正式发布 — 双通道架构

知乎自动化 Skill v2.0 采用全新的双通道架构设计，将读操作（HTTP API）与写操作（浏览器自动化）分离，显著提升了稳定性、速度和可维护性。

#### 新架构

```
                  ┌──────────────────┐
                  │  AI Agent / 用户  │
                  └────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐  ┌────────────┐  ┌──────────────┐
   │ HTTP 读通道 │  │ 浏览器写通道 │  │ Python OpenAPI│
   │ 热榜/搜索   │  │ 文章/想法   │  │ 圈子互动      │
   │ 用户/问答   │  │ 互动/问答   │  │ (可选)        │
   └────────────┘  └────────────┘  └──────────────┘
```

#### 6 大功能模块

| 模块 | CLI 脚本 | 通道 |
|:----|:---------|:----:|
| 📝 **发布文章** | `zhihu-publish.js article` | 浏览器写通道 |
| 💭 **发布想法** | `zhihu-publish.js thought` | 浏览器写通道 |
| ❓ **回答问题** | `zhihu-answer.js` | 浏览器写通道 |
| 🙋 **提问** | `zhihu-ask.js` | 浏览器写通道 |
| 👍 **互动（点赞/评论/关注）** | `zhihu-interact.js` | 浏览器写通道 |
| 🔥 **数据提取（热榜/搜索/用户/问题）** | `zhihu-extract.js` | HTTP 读通道 |

#### 新增特性

- **双通道架构**：读操作走 HTTP API（更快），写操作走浏览器自动化（更稳）
- **Cookie AES-256-GCM 加密存储**：加密密钥通过 `ZHIHU_COOKIE_KEY` 环境变量管理，支持密钥轮换
- **Playwright Stealth 反爬保护**：贝塞尔鼠标轨迹、逐字输入、TLS 指纹伪装
- **智能签名引擎（zse-123）**：适配器模式支持多种签名算法，支持 C3b 前向兼容和 WebWorker 计算
- **Plan B 降级策略**：HTTP 签名失败自动降级到浏览器通道
- **崩溃自动恢复**：`withCrashRecovery` 机制自动重建浏览器会话
- **指数退避限流**：遇到限流时自动退避（30s → 1min → 3min → 10min）
- **选择器自动降级**：`config/selectors.json` 支持主/备/兜底三级选择器
- **沙箱测试模式**：`ZHIHU_TEST_MODE=sandbox` 隔离测试环境

#### 12 个核心模块

- `zhihu-core.js` — Cookie 加密/浏览器管理/日志/重试
- `zhihu-signature.js` — 签名生成（适配器模式）
- `zhihu-http.js` — HTTP 读通道
- `zhihu-browser.js` — 浏览器自动化
- `zhihu-publish.js` — 发布文章 + 想法
- `zhihu-interact.js` — 点赞 + 评论 + 关注
- `zhihu-answer.js` — 回答问题
- `zhihu-ask.js` — 提问
- `zhihu-extract.js` — 数据提取
- `zhihu-bridge.js` — Python 桥接
- `zhihu-export-cookie.js` — Cookie 导出
- `python/zhihu_bot.py` — OpenAPI 圈子互动

---

## v1.x (历史版本)

v1.x 为单通道架构（纯浏览器自动化），代码已不再维护。建议升级到 v2.0 获取更好的性能和稳定性。
