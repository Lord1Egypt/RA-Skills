# Sage CGO 与公司 DNA

`~/.sage` 是所有 Sage Skill 共用的公司事实层。CGO 读取通用公司事实，增长专属事实写入 `~/.sage/growth/`。

公司事实和增长事实都应读取和写回 `~/.sage`；如需在 workspace 浏览，只生成只读 `sage-mirror/`。

## 启动读取

1. 读取 `references/cgo-identity.md`，加载 CGO 常驻身份和增长判断底座。
2. `~/.sage/INDEX.md`
3. `~/.sage/MANIFEST.yaml`
4. 与增长相关的通用目录：
   - `company_profile/`
   - `products_and_services/`
   - `memory_and_insights/`
5. 增长专属目录：`growth/`
6. 增长操作系统类问题读取 `references/cgo-growth-operating-system.md`；具体场景读取 `references/cgo-scenarios.md`；平台机制问题读取 `references/platforms.md`。

## 增长扩展目录

首次需要增长专属记忆时运行 `scripts/ensure_growth_extension.sh`，创建：

```text
~/.sage/growth/
├── channels.md
├── content-pillars.md
├── audience.md
├── experiments.md
├── metrics.md
└── monetization.md
```

## 工作区镜像

当用户想在当前工作区阅读公司 DNA 时，运行 `scripts/mirror_sage.sh`，生成 `sage-mirror/`。镜像只读，不能当作写入目标；`~/.sage` 仍是唯一真源。
