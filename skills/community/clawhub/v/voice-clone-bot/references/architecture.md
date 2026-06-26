# voice-clone-bot — 系统设计文档

> 本文档面向**后续接手的 Agent 或开发者**，详细阐述系统架构、设计决策与扩展指南。
> 面向最终用户的快速开始指南请参阅 `README.md`。
> Agent 触发规范请参阅 `SKILL.md`。

---

## 1. 项目愿景

voice-clone-bot 为大模型 Agent（如 OpenClaw）提供一套**完全解耦、高拟真度、轻量泛用的语音到语音（Voice-to-Voice）克隆插件**。

核心交互闭环：
1. 用户在聊天端（如 Telegram）发送语音 → ASR 技能（如 openai-whisper）识别并保存原始录音
2. LLM 生成文字回复
3. **本插件**使用用户的原声作为音色锚点，将文字合成为克隆声音后发送回去

本插件**不干涉** ASR 和 LLM，仅专注于 TTS 与零样本语音克隆。

---

## 2. 架构总览

```
┌─────────────────────────────────────────────────┐
│                   Agent (OpenClaw)                │
│                                                   │
│  1. ASR 识别用户语音 (openai-whisper)              │
│  2. LLM 生成文字回复                               │
│  3. 调用 run_tts.sh --text "..." --ref_audio "..." │
│  4. 获取输出路径，附加 MEDIA:<path>                 │
└────────────────────┬────────────────────────────┘
                     │ bash
          ┌──────────▼──────────┐
          │   scripts/run_tts.sh │ ← 自动检测 venv / 自动启动守护进程
          └──────────┬──────────┘
                     │ HTTP POST /clone
          ┌──────────▼──────────┐
          │   server/app.py      │ ← FastAPI 常驻守护进程 (端口由 .env 配置)
          │   └── core_tts.py    │ ← 引擎工厂 + 长文本切片
          │       ├── F5-TTS     │
          │       ├── CosyVoice  │
          │       ├── ChatTTS    │
          │       └── OpenVoice  │
          └─────────────────────┘
```

### 关键设计决策

| 决策 | 理由 |
| --- | --- |
| **常驻守护进程** | 大模型权重加载耗时 20-40 秒，必须常驻内存避免每次冷启动 |
| **run_tts.sh 统一入口** | Agent 无需关心 venv/端口/进程管理，脚本自动处理一切 |
| **引擎工厂模式** | 通过 `TTS_BACKEND` 环境变量零侵入切换引擎，新引擎只需继承 `BaseTTSEngine` |
| **全局模型沙盒** | 所有权重统一存放于 `~/.openclaw/models/voice-clone/`，避免重复下载和脏乱 |
| **长文本自动切片** | 按标点断句、逐片推理、numpy 拼接，突破单次推理 10-20 秒的长度限制 |

---

## 3. 目录结构

```
voice-clone-bot/
├── SKILL.md                      # Agent 标准技能文档（符合 Anthropics Skill 规范）
├── ARCHITECTURE.md               # 本文件：系统设计文档
├── README.md                     # 面向人类的快速开始指南
├── scripts/
│   ├── auto_installer.sh         # 默认引擎(F5-TTS)安装 + OpenClaw 技能注册
│   ├── install_cosyvoice.sh      # CosyVoice 引擎安装
│   ├── install_chattts.sh        # ChatTTS 引擎安装
│   ├── install_openvoice.sh      # OpenVoice V2 引擎安装
│   ├── run_tts.sh                # 统一入口（自动守护进程管理 + 推理转发）
│   ├── uninstall.sh              # 清理脚本（支持按引擎卸载 / 全量卸载 / 彻底清除）
│   └── tts_client.py             # 轻量 HTTP 客户端
└── server/
    ├── app.py                    # FastAPI 守护服务入口
    ├── core_tts.py               # 多引擎工厂 + 断句切片 + 拼接
    └── requirements.txt          # F5-TTS 基础 pip 依赖
```

---

## 4. 引擎工厂 (Engine Factory)

位于 `server/core_tts.py`。

### 4.1 类层次

```
BaseTTSEngine (ABC)
├── F5TTSEngine         # NATIVE_SPEED_SUPPORT = True
├── CosyVoiceEngine     # NATIVE_SPEED_SUPPORT = False (ffmpeg 后处理)
├── ChatTTSEngine       # NATIVE_SPEED_SUPPORT = False (ffmpeg 后处理)
└── OpenVoiceEngine     # NATIVE_SPEED_SUPPORT = False (ffmpeg 后处理)
```

### 4.2 扩展新引擎

要添加新的 TTS 引擎，只需：

1. 在 `core_tts.py` 中创建新类继承 `BaseTTSEngine`
2. 实现 `load()` 和 `synthesize_chunk()` 两个方法
3. 在 `ENGINE_REGISTRY` 字典中注册
4. 编写对应的 `scripts/install_xxx.sh`
5. 如果引擎原生支持语速，设置 `NATIVE_SPEED_SUPPORT = True`

```python
class MyNewEngine(BaseTTSEngine):
    NATIVE_SPEED_SUPPORT = False

    def load(self):
        # 加载模型权重
        pass

    def synthesize_chunk(self, text, ref_audio, speed=1.0):
        # 生成单个句子的音频
        # return (np.ndarray, sample_rate)
        pass

# 注册
ENGINE_REGISTRY["mynew"] = MyNewEngine
```

### 4.3 语速控制机制

- **原生支持**(F5-TTS)：`speed` 参数直接传入模型推理，质量最高
- **后处理支持**(其他引擎)：通过 `ffmpeg atempo` 滤镜变速，在 0.5-2.0 范围内效果良好

### 4.4 情绪与语气控制

所有零样本克隆引擎（F5-TTS, CosyVoice, OpenVoice）的情绪**由参考音频决定，而非文字标签**。

工作原理是声学特征提取（Acoustic Feature Extraction）：模型从参考录音中提取说话者的音色、语速、情感等韵律特征，然后将这些特征"移植"到生成的文字上。

因此，控制情绪的正确做法是：**选择情绪匹配的参考音频**。

额外说明：ChatTTS 除支持克隆外，还支持在文字中嵌入 `[laugh]`(笑声)、`[uv_break]`(停顿) 等专属标签进行细粒度韵律控制。

---

## 5. 长文本切片算法

位于 `core_tts.py` 的 `split_text_to_chunks()` 函数。

单次推理安全上限约 150 个字符。超出后自动切片：

1. **一级切分**：按 `。！？.!?；;` 分割为句子
2. **二级切分**：超长句子按 `，,、` 切割为短语
3. **三级兜底**：仍然超长的文本按字数强制截断
4. **拼接**：所有片段推理后用 `np.concatenate` 无缝拼合

---

## 6. 自动化运维机制

### 6.1 run_tts.sh 工作流

```
run_tts.sh 被调用
    │
    ├── venv 不存在？ ──→ 自动执行 auto_installer.sh
    │
    ├── 配置端口无响应？ ──→ nohup 后台启动 app.py
    │                        阻塞等待就绪（最长 120 秒）
    │
    └── 转发参数给 tts_client.py ──→ POST /clone ──→ 输出音频路径
```

### 6.2 auto_installer.sh 工作流

```
1. 创建 ~/.openclaw/models/voice-clone/ 全局模型目录
2. 创建 venv 并安装 requirements.txt
3. 在 ~/.openclaw/skills/ 下建立软链接注册技能
```

### 6.3 uninstall.sh 功能

| 命令 | 效果 |
| --- | --- |
| `bash scripts/uninstall.sh` | 杀进程 + 删 venv + 移除注册 |
| `bash scripts/uninstall.sh --engine cosyvoice` | 仅删除 CosyVoice 源码 |
| `bash scripts/uninstall.sh --purge` | 上述全部 + 删除数 GB 模型权重 |

---

## 7. 环境与平台兼容

| 平台 | 加速方式 | 备注 |
| --- | --- | --- |
| macOS (Apple Silicon) | MPS | 自动检测，所有引擎兼容 |
| Linux (NVIDIA GPU) | CUDA | 自动检测 |
| Windows / CPU-only | CPU | 可用但推理较慢 |

环境隔离通过以下机制保障：
- `HF_HOME` 和 `MODELSCOPE_CACHE` 在 `app.py` 启动前强制注入
- 所有依赖安装在项目本地 `venv/` 中
- 各引擎的外部源码克隆在 `venv/` 内部（如 `venv/CosyVoice/`）

---

## 8. API 参考

### POST /clone

```json
{
  "text": "要合成的文字",
  "ref_audio_path": "/absolute/path/to/reference.ogg",
  "speed": 1.0,
  "output_dir": "/custom/path/"
}
```

响应：
```json
{
  "status": "success",
  "output_audio_path": "/absolute/path/to/generated_audio/reply_xxxx.ogg"
}
```
