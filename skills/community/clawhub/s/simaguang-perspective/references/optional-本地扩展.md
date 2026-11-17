# 可选：本地扩展（需要外部项目才有意义）

本文件收的是**依赖外部项目目录**的扩展流程。技能包单独安装、没有任何外部项目时，这些流程可以整段跳过，判断尺、协议、模板、脚本照常工作。

## 外部项目目录怎么认

标志：目录下存在 `书籍蒸馏/` 或 `PIPELINE_STATE.md`。

解析顺序（`scripts/project_paths.py`）：

1. 环境变量 `SIMAGUANG_PROJECT_DIR`（显式指定，最高优先）
2. 相对探测：当前工作目录 / 脚本目录 / 包根逐级向上找标志目录
3. 都没有 → 打印指引，告诉用户怎么设置环境变量；脚本退化为写包内 `handoff/`

```bash
export SIMAGUANG_PROJECT_DIR="/path/to/项目根"     # macOS / Linux
setx SIMAGUANG_PROJECT_DIR "D:\path\to\项目根"     # Windows
```

## 自我学习闭环（原 SKILL.md 章节）

- 每次分析后内部记录置信度、知识缺口、用户纠正到 `学习记录/学习日志.md`。
- "复盘学习日志"时运行 `scripts/review_learning_log.py`；历史事件自学运行 `scripts/self-learn-next.sh`。
- 进化记录（三家分晋→索取边界尺、TikTok×林深案例碰撞、每周热点复盘）见 `references/进化判断尺.md` 和 `学习记录/` 目录。
- 无外部项目时的等价做法：把这三项写进当前对话或用户指定的单个文件，跑 `scripts/review_learning_log.py --input <文件>` 复盘。

## 路由索引与书籍技能包

`references/技能路由索引.md` 的 28 个簇指向 `书籍蒸馏/*/skills/*/SKILL.md`——那是作者本地蒸馏产物，不随包发布。

- 有项目：按簇路由到具体书籍技能包，能引用原书出处。
- 无项目：直接用 `SKILL.md` 的「协议索引」加载包内 58 份协议，出处标注写「未接入书籍技能包」。

## 名人图片缓存

`scripts/fetch-celebrity.py` 写 `~/.cache/simaguang-celebrity/`（可用 `SIMAGUANG_STATE_DIR` 覆盖），图片经 `images.weserv.nl` 代理取，不直连 Commons 原图。缓存可随时删，重跑即重建。

## 相关脚本（都支持降级）

| 脚本 | 无外部项目时 |
| --- | --- |
| `scripts/build_skill_index.py` | 提示设置 `SIMAGUANG_PROJECT_DIR` 后退出（rc=2），不写坏索引 |
| `scripts/audit_skill_index.py` | 审计报告写包内 `handoff/` |
| `scripts/build_handoff.py` | 交接卡写包内 `handoff/`，三节数据标 `[no project dir]` |
| `scripts/check_distillation_quality.py` | 提示设置环境变量后退出（rc=2） |
| `scripts/test_routing_coverage.py` | 命中率回归照跑（只依赖包内配置），报告写包内 `handoff/` |
| `scripts/archive_work_product_feedback.py` | 归档写包内 `handoff/` |
