# videototext 技能附带源码

本目录是从主仓库抽出的**最小子集**，与 `SKILL.md` 中的字幕/总结说明一致，便于离线查阅或在独立环境中导入。

## 目录结构

- `app/core/settings.py` — 环境变量（`.env` 放在**技能包根目录**，与 `SKILL.md` 同级，不是放在 `code/` 下）
- `app/core/errors.py` — `AppError` / `ErrorCodes`
- `app/services/bilibili_subtitle.py` — B 站 API、Cookie、节流、轨道与校验
- `app/services/summary.py` — OpenAI 兼容总结
- `app/utils/bilibili_subtitle_validate.py` — 时长覆盖与标题匹配
- `app/utils/url_tools.py` — 短链、BV、分 P
- `app/extractors/base.py` — `ParseContext` 基类
- `app/extractors/bilibili.py` — yt-dlp 元数据/音频与字幕编排

## 运行前准备

1. 安装依赖（在技能包根目录执行）：

   ```bash
   pip install -r requirements-code.txt
   ```

2. 将 **`code` 的父目录**加入 `PYTHONPATH` 并不够；应把 **`code` 目录本身** 作为包搜索根（使能 `import app`）：

   **PowerShell（Windows）**

   ```powershell
   $env:PYTHONPATH = "d:\path\to\videototext\code"
   ```

   **Bash**

   ```bash
   export PYTHONPATH="/path/to/videototext/code"
   ```

3. 在技能包根目录（与 `SKILL.md` 同级）放置 `.env`，配置 `SESSDATA`、`SUMMARY_LLM_*` 等（变量名可参考主仓库根目录 `.env.example`）。`settings.py` 已针对「技能包目录结构」解析该 `.env`。

## 与主仓库的关系

主仓库路径：`app/...`。若主仓库代码更新，请**同步替换**本 `code/app` 下对应文件，或重新从仓库复制；技能说明仍以仓库为准。
