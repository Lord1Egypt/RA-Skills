# ShowMeAI 通用 Skill

**[English](README.md) | 中文**

## 这是什么

这是一个不绑定 Agent 平台的 ShowMeAI 创意媒体 Skill，覆盖图片生成与编辑、视频、图片转 3D、语音、音乐、图片放大和抠图。它适合 Codex、Hermes、WorkBuddy、OpenClaw 及其他能运行 Python 的 Agent 用户；它不能替代 ShowMeAI 账号或 API Key。

当前版本以 [SKILL.md](SKILL.md) 为准。2.1.0 版加入运行时强制的渐进式首次引导：Key 验证和默认模型确认是两个独立步骤，请求类别完成配置前不能开始生成。

## 核心能力

- 图片首选模型为 `gemini-3.1-flash-image`（Nano Banana 2），用户可在向导中改选当前分组可用的其他模型。
- 可分别配置图片、视频、3D、语音和音乐的默认模型，以及数量、尺寸、宽高比、分辨率、清晰度、时长、音色等模型专属参数。
- Key 只需配置一次。向导先调用 `/v1/models` 验证，再保存到操作系统应用配置目录，并限制凭据文件权限。
- 长任务会持续轮询到最终成功或失败；任务提交后立即落盘，Agent 或终端意外中断后可以恢复。
- 成功结果会下载到可预测的本地路径，并输出 `MEDIA:<绝对路径>`，不会只返回远程链接或任务 ID。
- 1–10 张图片的数量要求会通过原生批量或有界并行补全实现，并汇总用量、报告实际请求次数。
- 原有命令保留为兼容入口。
- 首次配置由运行时强制检查，而不是只依赖 Agent 文案；类别配置完成后，后续请求直接使用已保存默认值，不会反复询问模型。

## 环境要求

- Python 3.10+
- [ShowMeAI API Key](https://api.showmeai.art)
- 无第三方 Python 依赖

## 快速开始

1. 把仓库复制或安装为 Agent Skill。
2. 让 Agent 阅读 [SKILL.md](SKILL.md)。
3. 首次运行 `python3 scripts/showmeai.py setup`。
4. 确认第一次使用的媒体类别的默认模型和支持参数。
5. 直接用自然语言提出创意任务，或使用下方命令。

## 触发方式

- “生成一张 16:9 的产品主视觉并保存到本地。”
- “把这张图片做成带声音的 5 秒 720p 视频。”
- “用 ShowMeAI 把这个透明 PNG 转成 GLB 模型。”
- “把我的默认图片模型和默认分辨率配置好。”

## 适合谁

适合希望在不同 Agent 宿主中复用同一套 ShowMeAI 工作流、只配置一次 Key，或需要异步媒体任务可靠完成的个人和团队。如果是在应用服务端直接集成 HTTP API，应使用 ShowMeAI API 文档和常规应用客户端。

## 安装与首次配置

把这个 Skill 安装或复制到任意 Agent 的 Skill 目录，并让 Agent 阅读 `SKILL.md`。运行时使用系统原生路径，不依赖 Codex、Hermes、WorkBuddy 或 OpenClaw 的目录结构。

本机交互式配置：

```bash
python3 scripts/showmeai.py setup
```

本地 TTY 向导会验证 Key、拉取该 Key 令牌分组能看到的模型，并引导选择默认模型和支持参数。Agent 辅助模式先验证 Key，然后必须把模型选择展示给用户并保存用户的明确决定，不会静默接受默认值。

### 可直接发给 Agent 的安装引导

把下面这段话发给可信任的 Agent；等 Agent 已启动标准输入流程后再提供 Key：

> 阅读这个 Skill 的 `SKILL.md`。在询问创作内容前，先执行 `doctor --category <请求类别> --json`。如果缺少 Key，执行 `setup --key-stdin --json`，通过标准输入传入我的 ShowMeAI Key，不得回显，也不得把 Key 放进命令参数。如果需要首次引导，执行 `onboarding models --category <请求类别> --json`，先展示推荐模型，再展示这个 Key 当前令牌分组可用的备选模型和支持参数，并让我选择；使用 `onboarding apply` 保存选择。必须提醒我不同令牌分组可调用的模型不同。首次引导成功前不得生成；类别配置完成后不得重复询问 Key 或模型，除非我要求修改。不得为 ShowMeAI 创建或修改 OpenClaw、WorkBuddy、Hermes、Codex 或其他宿主配置文件。

如果 Agent 无法安全地向进程写入标准输入，请由用户亲自在终端运行交互式向导。不要把 Key 写进 shell 命令、URL、Git 文件或公开对话。

## 令牌分组必须注意

`/v1/models` 返回的是当前 API Key 所属令牌分组可用的模型，不是 ShowMeAI 全部模型。不同分组可调用的模型不同。找不到目标模型时，请在 ShowMeAI 控制台切换令牌分组或启用自动分组，然后重新执行：

```bash
python3 scripts/showmeai.py models
python3 scripts/showmeai.py doctor
```

任务型能力如果无法通过 `/v1/models` 验证，会标记为 `verify_on_use`，实际调用时再确认可用性。

新发布的创意模型可能标记为 `verified_uncataloged`：当前 Key 确实可见并可选择，但本地尚未收录其专属参数结构，在目录更新前应使用 API 默认参数。

## 配置位置

| 系统 | 默认配置目录 |
|---|---|
| macOS | `~/Library/Application Support/ShowMeAI Skill/` |
| Linux | `${XDG_CONFIG_HOME:-~/.config}/showmeai-skill/` |
| Windows | `%APPDATA%\ShowMeAI Skill\` |

Key 单独保存在 `credentials`，支持权限控制的系统上会设置为仅当前用户可读写。非敏感偏好保存在 `config.json`。可用 `SHOWMEAI_CONFIG_DIR`、`SHOWMEAI_CONFIG_FILE`、`SHOWMEAI_STATE_DIR` 覆盖路径。`SHOWMEAI_API_KEY` 优先级最高；旧变量 `Showmeai_API_KEY` 只为迁移兼容。

ShowMeAI 不需要任何 Agent 宿主配置目录。运行 `python3 scripts/showmeai.py paths --json` 可以查看实际使用的 ShowMeAI 专属路径。不要把 Key 写入 `.openclaw`、`.workbuddy`、`.hermes`、`.codex` 或宿主 `.env`。

常用配置命令：

```bash
python3 scripts/showmeai.py config show
python3 scripts/showmeai.py onboarding status --category image
python3 scripts/showmeai.py onboarding models --category image
python3 scripts/showmeai.py onboarding apply --category image --model gemini-3.1-flash-image --params-json '{"n":1,"image_size":"1K","aspect_ratio":"1:1"}'
python3 scripts/showmeai.py config set defaults.image.model gpt-image-2
python3 scripts/showmeai.py config set defaults.image.params '{"n":1,"size":"auto","quality":"high","output_format":"png"}'
python3 scripts/showmeai.py setup --replace-key
```

`config set` 是底层兼容命令。通过它修改某个类别的默认值后，该类别会自动回到 `needs_defaults`；请使用 `onboarding apply` 验证并确认新模型和参数。

## 使用示例

```bash
# 新配置默认使用 gemini-3.1-flash-image
python3 scripts/showmeai.py image --prompt "云层之上的发光城市" --image-size 2K --aspect-ratio 16:9

# 图片编辑，可重复传入 --input
python3 scripts/showmeai.py image --prompt "改成水彩海报" --input source.png

# 视频会持续轮询并下载最终文件
python3 scripts/showmeai.py video --prompt "纸船穿过月光下的湖面" --resolution 720p --duration 5 --audio

# 图片转 3D，通常推荐透明背景 PNG
python3 scripts/showmeai.py 3d --image character.png --format glb --steps 10

# 文字转语音
python3 scripts/showmeai.py tts --text "欢迎使用 ShowMeAI" --voice alloy

# 音乐生成
python3 scripts/showmeai.py music --mode inspiration --description "温暖的电影氛围音乐"

# 图片处理
python3 scripts/showmeai.py pic upscale --image portrait.png --type face --scale-factor 2
python3 scripts/showmeai.py pic remove-bg --image product.png --type object
```

`--json` 可以放在命令任意位置，输出紧凑的机器可读 JSON。完整参数请运行 `<command> --help`。

运行时把所有图片模型的 `--count`（1–10）视为结果数量契约。模型原生支持数量参数时优先直接使用；否则或上游返回不足时，会进行有界的并行单图补充请求。`--concurrency` 控制并行上限，默认值为 4。结果会报告实际请求次数，每次物理请求均可能单独计费。上游也可能在保持宽高比的同时调整自定义尺寸的实际像素。

## 持久轮询与恢复

视频、3D、音乐和图片处理命令不会因为 API 只返回任务 ID 就结束。运行时采用有上限的退避轮询，定期向标准错误输出心跳；默认只在终态成功、终态失败时停止，或者用户显式设置 `--max-wait`。成功后会下载全部结果。

任务在首次轮询前和每次响应后都会保存。如果进程中断，可恢复：

```bash
python3 scripts/showmeai.py tasks list
python3 scripts/showmeai.py tasks resume
```

默认输出根目录为 `./showmeai-output/`，按媒体类别分目录；已有文件绝不会被覆盖。

## 详细文档

- [配置与凭据](references/configuration.md)
- [图片模型与参数](references/image.md)
- [视频工作流](references/video.md)
- [3D 工作流](references/three-d.md)
- [语音与音乐](references/audio.md)
- [轮询与恢复](references/polling.md)
- [ShowMeAI API 文档](https://showmeai.apifox.cn)
- [Agent 行为说明](SKILL.md)
- [架构设计](DESIGN.md)
- [版本记录](CHANGELOG.md)

## 边界与注意事项

- 模型是否可见、是否能调用取决于 API Key 的令牌分组。
- 不同模型的参数不能混用；不支持的字段会被过滤或拒绝。
- 多图补全可能产生多个计费请求；自定义尺寸即使被接受，上游也可能输出相同宽高比的另一组像素尺寸。
- 宿主强制杀死进程后无法继续在线轮询，但已持久化的任务可以恢复。
- Skill 会下载远程媒体，请确保输出目录空间充足且内容适合保存。

## 文件结构

下方带注释的文件树是 `SKILL.md` 引用的正式发行文件清单。

```text
showmeai-skill/
├── SKILL.md                 # Agent 路由与强制行为
├── README.md                # 英文说明
├── README.zh-CN.md          # 中文说明
├── DESIGN.md                # 架构与安全边界
├── CHANGELOG.md             # 版本记录
├── data/
│   └── model-catalog.json   # 创意模型与参数目录
├── references/
│   ├── configuration.md     # 配置、Key、分组与默认值
│   ├── image.md             # 图片模型与参数
│   ├── video.md             # Seedance 视频工作流
│   ├── three-d.md           # 图片转 3D 工作流
│   ├── audio.md             # 语音与音乐工作流
│   ├── image-tools.md       # 放大与抠图
│   └── polling.md           # 终态轮询与恢复规则
├── scripts/
│   ├── showmeai.py          # 统一命令入口
│   ├── showmeai_core/       # 配置、目录、HTTP、输出和任务模块
│   ├── gen.py               # 旧版图片兼容入口
│   ├── video_gen.py         # 旧版视频兼容入口
│   └── image_to_3d.py       # 旧版 3D 兼容入口
└── tests/
    └── test.py              # 离线契约与运行测试
```

旧版 `gen.py`、`video_gen.py` 和 `image_to_3d.py` 会转发到统一运行时；新项目建议直接使用 `showmeai.py`。

MIT License。
