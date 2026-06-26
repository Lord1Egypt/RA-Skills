# Sage CPO 与公司 DNA

`~/.sage` 是所有 Sage Skill 共用的公司事实层。CPO 读取通用公司事实，产品专属事实写入 `~/.sage/product/`。

公司事实和产品事实都应读取和写回 `~/.sage`；如需在 workspace 浏览，只生成只读 `sage-mirror/`。

## 启动读取

1. 读取 `references/cpo-identity.md`，加载 CPO 常驻身份和产品判断底座。
2. `~/.sage/INDEX.md`
3. `~/.sage/MANIFEST.yaml`
4. 与问题相关的通用目录：
   - `products_and_services/`
   - `operations_and_workflows/`
   - `memory_and_insights/`
5. 产品专属目录：`product/`
6. 产品操作系统类问题读取 `references/cpo-product-operating-system.md`；具体场景再读取 `references/cpo-scenarios.md`。

## 产品扩展目录

首次需要产品专属记忆时运行 `scripts/ensure_product_extension.sh`，创建：

```text
~/.sage/product/
├── users.md
├── feedback.md
├── roadmap.md
├── experiments.md
├── metrics.md
├── packaging.md
└── open-questions.md
```

## 工作区镜像

当用户想在当前工作区阅读公司 DNA 时，运行 `scripts/mirror_sage.sh`，生成 `sage-mirror/`。镜像只读，不能当作写入目标；`~/.sage` 仍是唯一真源。
