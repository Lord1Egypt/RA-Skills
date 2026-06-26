`reelonce-skill` 是 ReelOnce 的总控 skill，当前推荐按以下流程理解：

1. `planning`
   负责统一生成分镜、角色/场景/道具、声音映射，并写出 `narration.json` 与 `assets.json`。
2. `asset_generation`
   负责资产图、分镜图、TTS 音频。
3. `shot_render`
   负责镜头视频片段，可选使用 `shot` 分镜图或 `asset` 资产图作为参考图。
4. `remotion_preview`
   负责 Remotion React 工程。
5. `render`
   负责最终 MP4。

说明：

- `skills/reelonce-skill/scripts/run.py` 只是薄入口，直接调用已安装的 `reelonce` 包。
- `skills/reelonce-skill/scripts/agent_api.py` 会透传 `--reference-image-source` 与 `--debug-video-prompt`，与包内 `reelonce-skill` CLI 保持一致。
- 推荐按仓库根目录执行 `pip install -e ".[dev]"` 安装依赖，并通过 `cp env.local.example env.local` 初始化环境变量模板。
- `narration`、`asset-extractor` 已不再作为独立顶层流程暴露。
- 当前数据库默认位于 `output/{project_id}/animation.db`，按项目隔离。
- 商业视频服务的参考图输入遵循“有 URL 就传 URL，没有云存储就转 base64”的策略。
- 旧的 `narration.json`、`assets.json`、数据库字段和最终产物路径保持不变。
