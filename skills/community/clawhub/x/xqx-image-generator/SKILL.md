---
name: xqx-image-generator
description: "使用火山引擎Ark进行文生图，支持生成头像、封面、海报、配图等，适用于用户请求包含‘生成图片’、‘AI绘图’等关键词的场景"
metadata:
  openclaw:
    requires:
      env:
        - ARK_API_KEY
        - ARK_IMAGE_MODEL
    primaryEnv: ARK_API_KEY
---

# XQX Ark 文生图 Skill

使用火山引擎 Ark (豆包) OpenAI 兼容接口进行文生图；接口为 OpenAI 兼容风格，适用于短句标题与长篇结构化创意或海报类需求。

**本 skill 不下载图片文件**，**只把可访问的图片 URL 返回给调用方**（通过标准输出；含过程日志，末行为 URL）。需保存到本地（如 `./assets/cover.jpg`）时，由 **调用方或上层工作流** 自行下载，不在本仓库脚本内实现。

## OpenClaw Agent 指令（必读）

由 **本 skill 驱动的 Agent** 在调用文生图时，应按下述顺序操作；**不要把用户提供的全文提示词塞进一条 exec 命令行**。

1. **工作目录**：使用 OpenClaw **当前任务的工作目录**（workspace 根目录，例如存放 `TOOLS.md` 的 `$HOME/.openclaw/workspace`，或该任务绑定的项目根——以运行时配置为准）。下文记为「工作目录」。
2. **先写临时文件**：在工作目录下创建目录 `wdatas/`（若不存在），将用户提供的描述 **原文** 写入 **`工作目录/wdatas/xqx-img-prompt.txt`**，编码 **UTF-8**。可覆盖上次内容；路径固定，**不要**向用户索取或解析自定义路径。
3. **再执行脚本**：在 **工作目录作为进程当前工作目录（cwd）** 的前提下执行  
   `python <本 skill 的 scripts/xqximage.py> --file` 或带上可选尺寸 `... -f 4K`。  
   脚本只从 **`./wdatas/xqx-img-prompt.txt`**（相对 cwd）读取，因此 **cwd 必须是步骤 1 的工作目录**。

短提示词仍可直接：`python .../xqximage.py "一句话" [size]`。

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `ARK_API_KEY` | 是 | 火山 Ark API Key |
| `ARK_IMAGE_MODEL` | 是 | 方舟文生图模型 ID 或推理端点 ID（与控制台配置一致，**无默认值**） |

**获取方式**：由调用方在运行前注入环境变量（本机 shell、`export`、CI 密钥、Agent 配置等）。若你使用 OpenClaw 工作区内的 `TOOLS.md` 仅作为本机备忘，可自行在其中写 `export` 并 `source`，但须遵守下方安全说明。

**安全说明（必读）**：`ARK_API_KEY` 是敏感凭证。请勿把真实密钥写入可被他人访问的共享文档、Wiki 或提交到 Git；勿将含密钥的 `TOOLS.md` 放在多人协作仓库或公共同步盘中。优先使用本机私有配置、操作系统/密钥管理器或 CI 密钥注入；脚本只从进程环境变量读取，不会将密钥写回磁盘。

**本机 `TOOLS.md` 示例**（占位符仅作格式参考，请替换为你自己的密钥管理方式）：

```
export ARK_API_KEY="你的API Key"
export ARK_IMAGE_MODEL="你的推理端点或模型 ID"  # 必填
```

**当前 shell 手动设置示例**：

```
export ARK_API_KEY="你的API Key"
export ARK_IMAGE_MODEL="你的推理端点或模型 ID"  # 必填
```

## 依赖

仅使用 Python 标准库，无需安装额外依赖。

## 使用方式

```
python scripts/xqximage.py <prompt> [size]
python scripts/xqximage.py --file | -f [size]
```

短提示词可直接写在命令行。**长文案**（海报说明、多段需求等）请用 **`--file` 模式**，避免 OpenClaw `exec` 等对命令行长度、引号与特殊字符的限制。

### `--file` 模式（Agent / 长文案）

与上文 **「OpenClaw Agent 指令」** 一致：由 Agent **先将用户内容写入 OpenClaw 工作目录下的 `wdatas/xqx-img-prompt.txt`**，再在该工作目录为 `cwd` 时执行脚本。

1. 工作目录下确保存在 `wdatas/`。
2. 将完整提示词写入 **`wdatas/xqx-img-prompt.txt`**（UTF-8；路径相对工作目录固定，脚本不接受自定义目录参数）。
3. 执行：`python scripts/xqximage.py --file` 或 `python scripts/xqximage.py -f 4K`。

脚本从 **`./wdatas/xqx-img-prompt.txt`** 相对 **进程当前工作目录** 读取；`cwd` 须与写入文件时所用工作目录相同。脚本路径可为 skill 安装路径，与工作目录无关。

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | 二选一 | 图片描述（短文案走命令行） |
| `--file` / `-f` | 二选一 | 从 `./wdatas/xqx-img-prompt.txt` 读入长文案 |
| size | 可选 | 尺寸：2K、4K、2560x1440 等，默认 2K |


### 尺寸选项

- `2K` - 默认
- `4K`
- `1456x816`、`2048x2048`、`2560x1440`、`1440x2560`、`2304x1728`、`1728x2304`

## 示例

```
# 基本用法
python scripts/xqximage.py "星际穿越，黑洞，电影大片，动感"

# 指定 4K 尺寸
python scripts/xqximage.py "可爱的猫咪" 4K

# 指定 16:9 比例
python scripts/xqximage.py "风景照" 2560x1440

# 长文案：先写入工作目录 wdatas/xqx-img-prompt.txt，再执行
python scripts/xqximage.py --file
python scripts/xqximage.py -f 4K

```

## 输出说明

- **返回给调用方**：执行成功后，**向调用方交付图片 URL**（标准输出；最后一行为纯 URL，便于 Agent/脚本解析）。本 skill **不**把图片写入磁盘，无「保存路径」类参数。
- **链接说明**：多为带签名的临时地址，过期后需重新调用生成。
- **再分发**：调用方将 URL 转给用户即可；若需本地文件，由调用方在 skill 之外下载或交给其它流程（例如公众号配图需本地化时，按对应 publisher skill 操作）。

## 文件结构

```
xqx-image-generator/
├── SKILL.md         # 本文件
├── requirements.txt # 依赖
└── scripts/
    ├── xqximage.py  # 主脚本
```

OpenClaw 工作目录（非本仓库内）由 Agent 在运行时创建：

```
<工作目录>/
└── wdatas/
    └── xqx-img-prompt.txt   # Agent 写入用户提示词后，再执行 --file
```

## API 参考

- **base_url**: `https://ark.cn-beijing.volces.com/api/v3`
- **接口**: OpenAI images.generate 兼容
- **参数**: prompt, size, watermark, response_format
