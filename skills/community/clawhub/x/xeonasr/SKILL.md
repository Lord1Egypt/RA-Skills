# Xeon TTS

基于 OpenVINO Qwen3-TTS Base/Custom 模型的本地语音合成技能，面向 OpenClaw 的 QQBOT 工作流使用。

## 目标

- 安装本地双服务：5002 Flask TTS，9002 Node TTS Workflow
- 自动配置目标机器自己的 OpenClaw 配置，但只写入 `channels.qqbot.xeonTts`
- 与 xeonasr 共存，不覆盖 `tools.media.audio` 或 `channels.qqbot.stt`
- 支持两个工作流：音色克隆、指定语气 TTS

## 什么时候应该调用 xeontts

只有在以下场景才使用 xeontts：

- 用户明确要“克隆音色”“克隆声音”“复制我的声音”
- 用户要求“用某种语气朗读/播报/生成语音”
- 用户要把音频生成到本地文件，而不是做转写

以下场景禁止走 xeontts：

- 识别语音
- 语音转文字
- 听写
- STT / ASR

这些请求必须交给 xeonasr，以避免任务冲突。

## OpenClaw / QQBOT 使用规则

### 规则 1：音色克隆必须分两步走

当用户说“我要克隆音色”时：

1. 立即把当前会话切到 clone 流程
2. 回复用户上传 3 到 5 秒参考音频
3. 在收到参考音频前，不要直接开始合成
4. 如果机器上已安装 xeonasr，QQBOT 发来的语音会先命中 ASR；此时应由 ASR 把音频转交给 xeontts，而不是按普通转写处理
5. 收到音频后必须先校验时长
6. 如果时长小于 3 秒或大于 5 秒，直接拒绝并提示重新上传
7. 校验通过后，再让用户发送要朗读的文本
8. 使用 Base 模型生成音频并落盘

### 规则 2：指定语气生成默认走 Custom 模型

当用户说“用开心的语气朗读……”“生成语音……”时：

1. 解析用户是否指定了语气
2. 如果没有指定，默认使用 `普通`
3. 使用 Custom 模型生成音频
4. 把结果保存到本地 `outputs/`
5. 回复用户文件路径

### 规则 3：必须做时长保护

- 参考音频：3 到 5 秒
- Base 克隆输出：最多约 20 秒
- Custom 输出：最多约 30 秒

如果用户显式要求更长时长，或者文本长度估算会明显超过上限，必须直接提示用户拆分内容，而不是盲目提交推理。

### 规则 4：必须明确告知文件保留期

- 参考音频和生成结果默认只保留 7 天
- 超过保留期后，系统会自动清理 `references/` 和 `outputs/` 中的旧文件
- 在提示用户上传参考音频、以及告知生成完成时，都要明确告诉用户这一点

## 安装流程

当 OpenClaw、QQBOT 或其他代理被要求安装这个 skill 时，按下面流程执行：

1. 安装 skill

   ```bash
   clawhub install xeontts
   cd "$HOME/.openclaw/workspace/skills/xeontts"
   ```

2. 执行安装脚本

   ```bash
   bash install.sh
   ```

3. 安装脚本会完成这些事情

- 创建 Python 3.10 环境
- 从 PyPI 安装 `xdp-tts-service`
- 生成 `config.json` 与 `tts_config.json`
- 尝试下载 Base / Custom OV 模型
- 仅在显式提供旧兼容参数时，才额外下载 Base checkpoint
- 配置 OpenClaw 的 `channels.qqbot.xeonTts`
- 启动 5002 与 9002
- 注册用户级 systemd 服务
- 运行 `self_check.sh`

当前默认模型仓库：

- `aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8`
- `aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8`

## 运行时端口

| 服务 | 端口 | 作用 |
|------|------|------|
| Flask TTS | 5002 | 真正执行 TTS 推理 |
| Node Workflow | 9002 | 解析 QQBOT 任务、维护会话状态、校验音频/文本时长 |

## OpenClaw 配置约定

xeontts 只会写入如下配置块：

```json
{
  "channels": {
    "qqbot": {
      "xeonTts": {
        "enabled": true,
        "baseUrl": "http://127.0.0.1:9002",
        "cloneModel": "qwen3_tts_0.6b_base_openvino",
        "customModel": "qwen3_tts_0.6b_custom_openvino"
      }
    }
  }
}
```

这意味着：

- 不会覆盖现有 `channels.qqbot.stt`
- 不会动 `tools.media.audio`
- 不会和 xeonasr 抢同一条 STT 链路

## 常用命令

```bash
cd "$HOME/.openclaw/workspace/skills/xeontts"

bash start_all.sh
bash stop_tts.sh
bash self_check.sh
curl http://127.0.0.1:5002/api/health
curl http://127.0.0.1:9002/health
```

## 关键接口

- `POST /api/workflow/message`
  - 作用：根据用户消息判断是 clone 还是 custom TTS，或者提示补充参考音频
- `POST /api/workflow/reference-audio`
  - 作用：上传参考音频，校验 3 到 5 秒后入库
- `POST /api/tts/custom-speak`
  - 作用：直接调用 Custom 模型生成语音
- `POST /api/tts/clone-speak`
  - 作用：直接调用 Base 模型做音色克隆

## 故障排查

- 如果 `5002` 不通，先检查 `tts.log`
- 如果 `9002` 不通，先检查 `skill.log`
- 如果参考音频总是被拒绝，先确认机器上是否有可用的 `ffprobe`；当前版本对 WAV 参考音频也支持无 `ffprobe` 回退校验
- 如果用户说的是转写意图，不要误用 xeontts
- 如果 Base 模型报错，优先让用户更换更干净的 3 到 5 秒参考音频
- 当前默认发布形态只要求 `Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8`，不再默认要求原始 Base checkpoint
- 只有旧导出模型缺少 processor 或 speech tokenizer 权重时，才需要补 `BASE_CHECKPOINT_PATH`