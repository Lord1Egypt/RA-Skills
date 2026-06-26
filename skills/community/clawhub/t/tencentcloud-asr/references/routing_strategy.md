# 音频路由与大文件处理策略

> **何时必须阅读本文件**：
> - 输入是公网 `http://` / `https://` URL
> - 音频超过 60 秒
> - 文件可能超过 3MB / 100MB
> - 需要在 `flash_recognize.py` 与 `file_recognize.py` 之间做选择
> - 需要判断当前脚本是否支持 body 上传

## 核心结论

1. **公网 URL 默认直接走异步录音文件识别**
   - 直接调用 `file_recognize.py rec "<PUBLIC_URL>"`
   - 不要先本地下载、探测、转码、再路由
2. **只有 `file_recognize.py rec` 真实失败时，才进入下一层诊断**
   - URL 不可下载 / 非公网可访问：提示用户提供可公网访问的 URL
   - 时长超过 `5h`：转入本地下载 + 规范化 + 切片链
   - 格式/解码失败：再考虑本地下载 + FFmpeg 规范化
   - 用户明确要求同步返回：才把同步路径当作显式例外
3. **本地文件默认仍按短音频 / Flash / 切片链处理**
   - 先规范化为 `16kHz`、单声道、`pcm_s16le`、`.wav`
   - 再按时长和大小选择脚本
4. **如果用户已经具备 COS 上传能力，可把“上传标准 WAV 到 COS 后走异步 URL”作为优先优化分支**
   - 仅适用于最终生成的公网 URL 对应音频 `<=5h`
   - 这个分支的价值是避免本地切片和多次 Flash 调用，不是绕过 `CreateRecTask` 的 `5h` 上限

## 硬阈值

- `SHORT_MAX_SECONDS = 60`
- `SENTENCE_MAX_BYTES = 3145728`（3MB）
- `FLASH_MAX_SECONDS = 7200`（2 小时）
- `FLASH_MAX_BYTES = 104857600`（100MB）
- `FILE_ASYNC_MAX_SECONDS = 18000`（5 小时）
- `FILE_BODY_MAX_BYTES = 5242880`（5MB）
- `SEGMENT_SECONDS = 1800`（30 分钟）

## 第 1 部分：公网 URL

### 1.1 默认路径

如果输入本来就是公网 `http://` / `https://` URL，默认直接执行：

```bash
python3 <SKILL_DIR>/scripts/file_recognize.py rec "<PUBLIC_URL>"
```

默认不要先做这些事：

- 不要先下载到本地再判断
- 不要先用 `inspect_audio.py` 探测 URL 元数据
- 不要先为了 URL 探测去安装 `ffprobe`
- 不要先手动 `curl`、`file`、`grep` 做临时判断

正确做法是：先打异步 URL 识别，只有真实失败时再继续诊断。

### 1.2 URL 失败后的处理

当 `file_recognize.py rec "<PUBLIC_URL>"` 失败时，按错误分流：

1. **URL 不可下载 / 非公网可访问**
   - 直接提示用户换成可公网下载的 URL
   - 不要先尝试本地转码

2. **时长超过 `5h`**
   - 下载到本地
   - 规范化成标准 WAV
   - 切片后逐片走 `flash_recognize.py`

3. **格式错误 / 解码失败**
   - 下载到本地
   - 用 FFmpeg 规范化后再走本地链

4. **用户明确要求同步立即返回**
   - 这时才考虑把一句话识别或本地 Flash 当作例外路径
   - 但这不是默认策略

### 1.3 URL 场景下何时允许例外

只有命中以下任一条件，才不要默认坚持异步 URL 路径：

- 用户明确要求同步、立刻返回
- `file_recognize.py rec` 已真实失败
- URL 对应音频超过 `5h`

## 第 2 部分：本地处理链

### 2.1 先规范化

本地文件统一优先探测：

```bash
python3 <SKILL_DIR>/scripts/inspect_audio.py "<LOCAL_AUDIO_FILE>"
```

如果返回 `requires_ffprobe_or_ffmpeg`，先执行：

```bash
python3 <SKILL_DIR>/scripts/ensure_ffmpeg.py --execute
```

如果满足以下任一条件，就必须转码生成本地标准 WAV：

- `sample_rate != 16000`
- `channels != 1`
- `container_format != "wav"`

统一转码命令：

```bash
ffmpeg -y -i "<INPUT_AUDIO>" -ac 1 -ar 16000 -c:a pcm_s16le "<NORMALIZED_WAV>"
```

### 2.2 本地文件脚本选择

对 `WORKING_AUDIO_FILE` 读取：

- `duration_seconds`
- `file_size_bytes`

然后按下面顺序判断：

1. 如果同时满足：
   - `duration_seconds <= 60`
   - `file_size_bytes <= 3145728`
   使用：
   ```bash
   python3 <SKILL_DIR>/scripts/sentence_recognize.py "<WORKING_AUDIO_FILE>"
   ```

2. 如果同时满足：
   - `duration_seconds <= 7200`
   - `file_size_bytes <= 104857600`
   使用：
   ```bash
   python3 <SKILL_DIR>/scripts/flash_recognize.py "<WORKING_AUDIO_FILE>"
   ```

3. 如果同时满足：
   - 用户已经有可用的 COS 上传能力
   - 能把 `WORKING_AUDIO_FILE` 上传成公网可下载 URL
   - `duration_seconds <= 18000`
   那么优先考虑：
   ```bash
   python3 <SKILL_DIR>/scripts/file_recognize.py rec "<PUBLIC_URL_FOR_WORKING_AUDIO_FILE>"
   ```

4. 如果命中以下任一条件：
   - `duration_seconds > 7200`
   - `file_size_bytes > 104857600`
   那么必须先切片，再逐片使用 `flash_recognize.py`

### 2.3 固定切片方案

切片命令：

```bash
ffmpeg -y -i "<WORKING_AUDIO_FILE>" -f segment -segment_time 1800 -c:a pcm_s16le -ar 16000 -ac 1 "<SEGMENT_DIR>/part_%03d.wav"
```

切片后对每一个分片都必须确认：

- `duration_seconds <= 7200`
- `file_size_bytes <= 104857600`

然后逐片执行：

```bash
python3 <SKILL_DIR>/scripts/flash_recognize.py "<SEGMENT_FILE>"
```

最后按文件名顺序拼接文本结果。

## 第 3 部分：什么时候才允许 `file_recognize.py`

命中以下任一条件时，可以主动选择 `file_recognize.py rec`：

1. 输入是公网 URL
2. 用户明确要求异步任务 / `TaskId` / `--no-poll`
3. 用户明确要求 `--res-text-format 4` 或 `--res-text-format 5`
4. 用户已经有 COS 上传分支，想用 URL 避开本地切片
5. 本地磁盘空间不足，无法完成规范化或切片

不要把 `file_recognize.py` 当成所有本地大文件的默认方案。

## 第 4 部分：脚本上传方式校验

当前脚本对“通过 body 传音频内容”的支持如下：

### `sentence_recognize.py`

- 本地文件：支持
- URL：支持
- 实现方式：
  - 本地文件走 `SourceType=1 + Data + DataLen`
  - URL 走 `SourceType=0 + Url`

### `flash_recognize.py`

- 本地文件：支持
- URL：脚本输入支持，但会先下载，再用请求 `Body` 上传原始字节
- 实现方式：
  - 最终总是 `POST Body` 传音频二进制

### `file_recognize.py`

- 本地文件：仅 `<= 5MB` 支持
- URL：支持
- 实现方式：
  - 本地小文件走 `SourceType=1 + Data + DataLen`
  - 公网 URL 走 `SourceType=0 + Url`

## 第 5 部分：为什么不默认要求 COS

腾讯云官方对 `CreateRecTask` 的要求是“公网可下载 URL”，并不是“必须 COS”。

因此：

- 如果用户已经给了公网可下载 URL，不要默认要求 COS
- 如果用户给的是本地大文件，也不要先让用户配 COS
- 如果用户已经具备 COS 上传能力，优先上传**规范化后的标准 WAV**，然后把返回的公网 URL 交给 `file_recognize.py rec`
- 即使走 COS，仍然必须满足 `CreateRecTask` 的 URL 时长上限 `<=5h`
