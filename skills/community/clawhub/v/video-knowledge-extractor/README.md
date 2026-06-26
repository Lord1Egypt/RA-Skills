# 中文视频知识抽取器

把视频、音频、播放列表或本地文件整理成适合知识库沉淀的内容。

## 这套技能能做什么

- 视频转知识笔记
- 音频转摘要
- 播放列表批量整理
- 本地文件夹批量转写
- 自动生成章节、要点、行动项和结构化 JSON

## 支持的输入

- 视频链接
- 音频链接
- 本地视频文件路径
- 本地音频文件路径
- 本地文件夹路径
- 播放列表
- 批量 URL 列表

如果是本地文件夹，脚本会自动递归查找可处理的媒体文件。

## 输出文件

- `summary.md`
- `notes.md`
- `chapters.md`
- `knowledge.json`
- `manifest.json`

## 怎么用

把输入直接交给这个 skill 即可。  
更多上手示例见 [examples.md](examples.md)。

## LLM 配置

如果设置了下面三个环境变量，脚本会自动调用 OpenAI 兼容接口做后处理：

- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

没有配置时，会回退到本地规则继续输出结果。

## 目录结构

- `scripts/`：处理入口脚本
- `output_templates/`：固定导出模板
- `agents/openai.yaml`：技能展示信息

