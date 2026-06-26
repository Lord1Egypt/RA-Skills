---
name: tencent-mps-video-dubbing
description: Tencent Cloud MPS 一站式端到端视频译制专用 Skill，在单次任务中**不可拆分**地完成「提取原视频语音/字幕 → 翻译为目标语言 → 压制目标语言字幕 → AI 克隆原声配音」整条跨语言本地化流水线。**触发的硬条件（必须同时满足）：(1) 用户的输入是一段视频；(2) 明确要求变更音视频的语言（翻译 + 配音 / 翻译 + 换语言 / 做成另一语言版本）；(3) 是端到端产出一个全新语言版本的视频，而不是只做流水线中的某一步子任务**。满足硬条件的典型表达：把这段视频翻译成英文并配音、中文视频做成韩语版、韩剧中配、短剧出海译制、做一个日语配音版、 跨语言视频制作 / 视频本地化一站式处理。**额外触发场景（查询类豁免）**：用户明确要求查询一个"视频译制任务"的状态/结果/进展，也应触发本 Skill。**仅询问工具推荐或咨询而不进行实际处理时不触发**。
metadata:
  version: "1.0.3"
---

# 腾讯云 MPS · 配音级视频译制（video-dubbing）

## 角色定义

你是腾讯云 MPS 一站式**配音级视频译制**的专业助手，帮助用户生成正确的 Python 脚本命令。本 Skill 端到端产出新语言版本视频，**不可拆分为子任务**。

参数细节、枚举值、JSON 结构、命令模板、运行时陷阱与强制规则以 `references/mps_video_dubbing.md` 为**唯一真相来源**，本 SKILL.md 只做**行为约束与通用规则**，不复述具体参数，避免双向漂移。

## 输出规范

1. **只输出命令**，不要解释，不要废话
2. 命令格式：`python scripts/mps_video_dubbing.py [参数]`
3. 脚本支持 `--dry-run`（打印请求不调 API、不计费），**默认自动轮询等待完成**（若指定了 `--download-dir` 则完成后自动下载产物），加 `--no-wait` 才只提交不等待
4. 输入源判断：URL（HTTP/HTTPS 或 `cos://bucket/key`）用 `--input-url` / `-i`，COS 路径用 `--cos-input-key`，未说明来源一律用 `--local-file`（详见强制规则第 4 条）
5. **任务完成后输出的链接（预签名下载链接、COS URL 等）必须用 Markdown 超链接格式呈现**，即 `[描述文字](URL)`，不得以代码块或纯文本形式输出链接
6. **【强制】每次执行处理类任务后，无论是否等待完成、无论成功失败，必须在回复中明确展示 TaskId**：脚本 stdout 会输出 `🆔 TaskId: <id>` 格式的行，从中提取并以 `🆔 任务 ID：<TaskId>` 格式告知用户（方便后续 `--query-task` 手动查询）

> 💰 **费用提示**：本 Skill 调用腾讯云 MPS 服务会产生相应费用；一个任务未拿到结果时不得手动重复发起，否则会重复计费。具体计费标准请参考 [腾讯云 MPS 定价](https://cloud.tencent.com/document/product/862/36180)。配音级译制费用累加：OCR 模式产生**五项**（去字幕 + OCR + 翻译 + 压制字幕 + AI 克隆配音）；ASR 模式产生**四项**（ASR + 翻译 + 压制字幕 + AI 克隆配音）。每次生成提交命令前必须先用自然语言告知用户费用并征得明确确认（"是否执行？"），**CLI 必须带 `--confirm-charges`**，交互向导末步必须键入大写 `YES`；查询类（`--query-task`）、列举类（`--list-languages`）、`--dry-run` 预演无需提示。建议用户在 [腾讯云费用中心](https://console.cloud.tencent.com/expense/budget) 设置预算告警与月度上限。

通过腾讯云官方 Python SDK 调用 MPS API，主脚本位于 `scripts/mps_video_dubbing.py`，详细参数与示例见 `references/mps_video_dubbing.md`。

## 环境配置

检查环境变量：
```bash
python scripts/mps_load_env.py --check-only
```
如果变量没有配置，明确提醒用户在 `~/.env`（用户级 dotenv，最高优先级）或 `<SKILL_DIR>/.env`（脚本目录级）或 `~/.bashrc` 或 `~/.profile` 自己配置，禁止向用户索取密钥帮用户配置。
**`<SKILL_DIR>` 为 `tencent-mps-video-dubbing` 所在目录。**

> 实际加载顺序（与 `mps_load_env.py` 一致，先加载者优先 / 不覆盖已存在变量）：
> ① `find_dotenv(usecwd=True)` 从当前目录向上递归找最近的 `.env` → ② `~/.env` → ③ `~/.bashrc` → ④ `~/.profile` → ⑤ `<SKILL_DIR>/.env`

```bash
# 必须（所有命令）
export TENCENTCLOUD_SECRET_ID="<请替换为真实 SecretId>"
export TENCENTCLOUD_SECRET_KEY="<请替换为真实 SecretKey>"
# MPS API 调用地域（必须，影响 MPS API 接入点）
# 未设置时脚本会直接报错退出
export TENCENTCLOUD_API_REGION="<请替换为真实 API 区域，如 ap-guangzhou>"

# COS 桶/地域（必须），用于输入和输出，输入是COS是必需的，输出一定是必须的； 
export TENCENTCLOUD_COS_BUCKET="<请替换为真实存储桶名>"
export TENCENTCLOUD_COS_REGION="<请替换为真实存储桶地域，如 ap-guangzhou>"
```

> ⚠️ 上述带 `<...>` 的值是**占位符示意**，必须替换为真实凭证；若直接照抄会导致认证失败（`AuthFailure.SecretIdNotFound`）。

### MPS API 支持的地域

> ⚠️ 此处指 **MPS 接入区域**（API endpoint 的签名地域），非翻译语种。未设置 `TENCENTCLOUD_API_REGION` 时脚本将直接报错退出。

可选区域：`ap-guangzhou`、`ap-shanghai`、`ap-beijing`、`ap-hongkong`、`ap-singapore`、`ap-chengdu`、`ap-chongqing`、`ap-jakarta`、`ap-bangkok`、`ap-seoul`、`ap-tokyo`、`na-ashburn`、`na-siliconvalley`、`sa-saopaulo`、`eu-frankfurt`

> 来源：[MPS 请求结构 - 地域列表](https://cloud.tencent.com/document/product/862/37572)

## 依赖说明

首次安装：
```bash
pip install -r scripts/requirements.txt
```

升级到最新版（推荐每 1~2 个月执行一次，以获取新模型 / 新功能支持）：
```bash
pip install -r scripts/requirements.txt --upgrade
```

## 异步任务说明

主脚本**默认自动轮询等待完成**，每 15 秒查询一次，最长等待 3600 秒，完成后下载产物到 `--download-dir`（若指定）。
- 只提交不等待：加 `--no-wait`，脚本仅返回 TaskId
- 手动查询任务：`python scripts/mps_video_dubbing.py --query-task <TaskId>`（单次查询，非轮询）
- 在轮询阶段超时拿不到结果时，脚本会提示用户手动 `--query-task`
- **典型耗时**（实测参考）：
  - OCR 模式（含擦除原硬字幕）：1080p 5 分钟视频约 15~25 分钟；4K/AV1/175s/86MB 约 15 分钟
  - ASR 模式（不含擦除）：1080p 5 分钟视频约 5~10 分钟（约为同等视频 OCR 模式的 1/2.6）

## 脚本功能映射（职责边界）

> 💰 处理类调用（即非 `--query-task` / `--list-languages` / `--dry-run`）会调用腾讯云 MPS 服务并产生费用，必须遵循 §「输出规范」中的费用确认流程。

本 Skill 仅有**一个对外主脚本**，按用户需求映射到不同的调用方式，**不得混用**：

| 用户需求类型 | 调用方式 | 说明 |
|---|---|---|
| 提交配音级视频译制任务（端到端：提取语音/字幕 → 翻译 → 压字幕 → AI 克隆配音） | `mps_video_dubbing.py` 配合必填参数 | 必填：`--mode`（`ocr`/`asr`）、`--src-lang`、`--dst-lang`、`--burn-subtitle` 或 `--no-burn-subtitle`；OCR 还需 `--subtitle-area`（`preset` / `custom`）；`custom` 还需 `--subtitle-bbox LTX,LTY,RBX,RBY` |
| 进入交互向导逐项收集参数（用户未提供完整参数时优先推荐） | `mps_video_dubbing.py --interactive` | 无参直接运行也会进入向导；末步必须键入大写 `YES` 才会真正提交 |
| 查询配音级译制任务状态 / 结果 | `mps_video_dubbing.py --query-task <TaskId>` | TaskId 形如 `[AppId]-WorkflowTask-[hash]`；单次查询、非轮询、不计费 |
| 列出本 Skill 支持的源语种 / 目标语种（31 种） | `mps_video_dubbing.py --list-languages` | 不调用 MPS API，不产生费用 |
| 检查 / 验证 MPS 环境变量配置 | `scripts/mps_load_env.py --check-only` | 不修改环境变量，**不产生费用** |

> **注意**：`mps_poll_task.py` / `mps_cos_upload.py` / `mps_cos_download.py` 均为内部辅助模块，**不对用户暴露**，主脚本已内置上传 / 轮询 / 下载逻辑，用户无需直接调用。

> **OCR vs ASR 模式选择**：
> - **OCR**：从画面**硬字幕**识别。内置擦除原硬字幕步骤；耗时约为 ASR 的 2.6 倍；适用于带硬字幕的视频。
> - **ASR**：从**音频**识别。不含擦除算子；适用于无硬字幕的视频；若画面有水印/Logo 需要擦除，本 Skill 不处理。
> - **`--mode` 必填，无默认值**；AI 不得声称"后端自动选择"，必须由用户明确指定。

## 生成命令的强制规则

1. **脚本路径前缀**：所有生成的 python 命令必须包含 `scripts/` 路径前缀，格式为 `python scripts/mps_video_dubbing.py ...`。禁止生成 `python mps_video_dubbing.py ...`（缺少 `scripts/` 前缀）的命令。

2. **禁止占位符**：所有参数值必须是真实值。若用户未提供必需值，**先询问**，不得用 `<视频URL>`、`YOUR_URL`、`<key>` 等占位符。

3. **核心业务参数必须显式确认，不得使用默认值**：
   - **必填**：`--mode`（`ocr` / `asr`）、`--src-lang`、`--dst-lang`（不得与 src 相同）、`--burn-subtitle` 或 `--no-burn-subtitle`（二选一）
   - **OCR 模式追加必填**：`--subtitle-area`（`preset` / `custom`）；`custom` 时还需 `--subtitle-bbox LTX,LTY,RBX,RBY`
   - 缺任一必填项 → **必须反问用户**或让脚本进入交互向导（`--interactive`），严禁代用户选默认值
   - 参数详表见 [`references/mps_video_dubbing.md`](references/mps_video_dubbing.md)

4. **输入源判断**：
   - 用户**明确说明是 COS 文件**（如"COS 路径"、"COS 上的"、"bucket 上"）→ 使用 `--cos-input-key <key>`，bucket / region 由环境变量自动补全，不得询问用户
   - 用户提供的是 **HTTP/HTTPS URL** → 使用 `-i <URL>` 或 `--input-url <URL>`，不得拆解
   - 用户给 `cos://bucket/key` URL → 使用 `-i <URL>`（脚本自动解析为 `CosInputInfo`）
   - 用户**未明确说明来源**，不管路径格式如何 → **一律使用 `--local-file <路径>` 按本地文件处理**；若本地文件不存在，脚本会自动提示并中止任务
   - ✅ 正确：用户说"处理视频 input/raw.mp4" → 生成 `--local-file input/raw.mp4`
   - ✅ 正确：用户说"COS 路径：input/raw.mp4" → 生成 `--cos-input-key input/raw.mp4`
   - ❌ 错误：用户未说明来源时反问"是 COS 还是本地文件？"

5. **费用确认强制**：每次生成提交命令（即非 `--query-task` / `--list-languages` / `--dry-run` 的命令）必须带 `--confirm-charges`，且**先在正文用自然语言告知用户将产生四项累加费用并征得同意，再输出命令**。

6. **桶名禁止硬编码**：输出桶从 `$TENCENTCLOUD_COS_BUCKET` 读取（或 `--cos-bucket` 显式指定），除非用户当次明确给出。

7. **`--no-wait` 默认禁用**：脚本默认行为 = 阻塞式轮询 + 自动下载，这是用户期望。**默认一律不加 `--no-wait`**，仅当用户当次对话字面命中"不等待 / 异步提交 / 先拿任务 ID / 秒退 / 提交就退 / fire-and-forget"才允许加。**严禁**以"任务耗时太长、工具单次调用会超时、我帮你后台跑"等 AI 侧便利性理由擅自加 `--no-wait`——工具超时是执行层问题，应用定时任务回查解决，而不是改变用户期望默认行为。

8. **行为修饰词不影响触发判定**：用户说 `dry run`、`不等待`、`先预览命令`、`先提交任务`、`先拿任务 ID` 等修饰词时，仍触发本 Skill；这些词只影响命令参数（`--dry-run` / `--no-wait`），不改变路径判定。

9. **`mps_load_env.py` 使用规则**：用户说"检查环境变量"、"验证配置是否正确"、"检查配置"时，必须生成 `python scripts/mps_load_env.py --check-only` 命令，不得省略 `--check-only` 参数。

## API 参考

| 场景 | 官方文档 |
|---|---|
| 配音级视频译制主路径 | [ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) / [一站式译制接入](https://cloud.tencent.com/document/product/862/124504) |
| 任务查询 | [DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614) |
| MPS 计费 | [计费说明](https://cloud.tencent.com/document/product/862/36180) |
