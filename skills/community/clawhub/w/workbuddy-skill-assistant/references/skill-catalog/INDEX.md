# Skill catalog 索引

> 这是运行时的轻量候选目录。先根据真实目标选主题，再只读取核心清单和命中的主题清单。

## 目录结构

| 层 | 文件 | 用途 |
|----|------|------|
| 通用核心 | [core.md](core.md) | 跨主题都可能复用的基础能力 |
| 画像映射 | [profile-theme-map.md](profile-theme-map.md) | 从用户目标或画像找到候选主题 |
| 主题积木 | [themes/](themes/) | 按任务领域提供少量候选 skill |

当前主题包括：

- [html-frontend.md](themes/html-frontend.md)
- [ppt-presentation.md](themes/ppt-presentation.md)
- [document-management.md](themes/document-management.md)
- [investment-analysis.md](themes/investment-analysis.md)
- [finance-accounting.md](themes/finance-accounting.md)
- [knowledge-management.md](themes/knowledge-management.md)
- [visualization.md](themes/visualization.md)

## 使用规则

1. 先读 `core.md`，再读画像映射命中的 1 个主题；
2. 只推荐能直接服务当前任务的 1–3 个候选；
3. 优先复用已装 skill，目录只用于发现缺口；
4. 先完成一次真实任务，再决定是否保留、组合或安装；
5. 目录维护和评分属于作者侧资料（源仓库 maintainers/，不随发布包分发），不在用户运行路径中自动执行。

## 目录字段

每个条目至少包含：

- `name`：可识别的 skill 名称；
- `slug`：安装或调用时使用的标识；
- `source`：来源；
- `purpose`：解决什么任务；
- `category`：所属主题。

`usability` 和 `composable` 只作为作者整理候选时的辅助信息，不合成为用户等级或综合分。
