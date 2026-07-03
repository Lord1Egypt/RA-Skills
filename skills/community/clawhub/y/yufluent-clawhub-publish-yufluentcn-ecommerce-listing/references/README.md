# 规范文件说明

**权威源**：仓库根目录 `harness/platforms/`（由 Harness Composer 注入 Prompt）。

本目录为 **只读镜像**，供 OpenClaw / 离线查阅；**请勿直接编辑**（CI 会与 harness 比对 SHA256）。

## 同步命令

修改 `harness/platforms/` 后执行：

```powershell
python scripts/sync-listing-references.py
```

校验：

```powershell
python scripts/verify-listing-references-sync.py
```

## 文件映射

| 本目录文件 | Harness 权威源 |
|------------|----------------|
| `platform-rules-amazon.md` | `harness/platforms/amazon/rules.md` |
| `amazon-style-guide.md` | `harness/platforms/amazon/style-guide.md` |
| `shopify-best-practices.md` | `harness/platforms/shopify/rules.md` |
| `tiktok-shop-tips.md` | `harness/platforms/tiktok/rules.md` |
| `pricing-table.md` | （技能专用，不参与同步） |

架构见 [docs/Harness架构.md](../../../docs/Harness架构.md)。
