# 初始化工作流（首次使用）

目标：把“私人路径/名称”自动填充到 `config.yaml`，填好后可直接执行主 skill。

## 1) 定位 skill 目录

当前 skill 根目录（本文件同级）即为：
- `SKILL.md`
- `config.template.yaml`
- `config.yaml`（初始化后生成）

## 2) 自动探测环境路径（建议）

按顺序探测并选第一个存在的路径：

- `workspace_dir` 候选：
  1. `~/.openclaw/workspace`
  2. 当前会话工作目录

- `soul_path` 候选：
  1. `<workspace_dir>/SOUL.md`
  2. `~/.openclaw/workspace/SOUL.md`

- `memory_root_path` 候选：
  1. `<workspace_dir>/MEMORY.md`
  2. `~/.openclaw/workspace/MEMORY.md`

- `daily_memory_dir` 候选：
  1. `~/.openclaw/memory`
  2. `<workspace_dir>/memory`

- `daily_memory_pattern` 默认：`YYYY-MM-DD.md`

- `diary_text_dir`：
  - 默认创建：`<workspace_dir>/scene/<你的日记场景>/日记历史记录/文字`
  - 如果没有场景目录，可用：`<workspace_dir>/diary/text`

- `news_summary_dir`（可选）：
  - 若存在则填：`<workspace_dir>/scene/每日简报/news/Summary`
  - 不存在可留空并将 `optional.include_news_context=false`

## 3) 生成配置

从模板复制：
- `config.template.yaml` → `config.yaml`

再将上面探测值写入 `config.yaml`。

## 4) 首次运行前校验

至少确认以下路径可用：
- `paths.soul_path`
- `paths.memory_root_path`（可选但建议）
- `paths.daily_memory_dir`
- `paths.diary_text_dir`（不存在就创建）

并确保：
- `output.image_width = 1080`

## 5) 成功标准

初始化完成后，执行主 skill 时：
1. 能读取 `config.yaml`
2. 能按配置找到 SOUL / MEMORY / 每日 memory
3. 能写出 `YYYY-MM-DD.md`
4. 能产出 `diary-YYYY-MM-DD.png`（宽度 1080）
