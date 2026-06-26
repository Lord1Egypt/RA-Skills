# Speech Recognition 语音识别

将 AMR/SILK 格式的语音转换为文字。

## 环境要求

- Python 虚拟环境：`source /opt/conda/bin/activate py314`
- 依赖包：`pysilk`, `faster-whisper`
- 模型路径：`/opt/workspace/yby_workspace/whisper-model`

## 使用方式

```python
from skills.speech_recognition import transcribe_audio

text = transcribe_audio("/path/to/audio.amr")
print(text)
```

## 实现逻辑

1. 读取 AMR/SILK 格式文件
2. 使用 `pysilk` 解码为 PCM 数据
3. 保存为 WAV 文件
4. 使用 `faster-whisper` 转写为文字
5. 返回识别结果

## 支持格式

- QQ 语音：`.amr` (SILK_V3 编码)
- 标准 AMR：`amr`, `amrnb`, `amrwb`

## 依赖安装

```bash
source /opt/conda/bin/activate py314
pip install pysilk faster-whisper
```

## 模型下载

需要从 HuggingFace 下载 faster-whisper 模型：

```bash
python3 -m huggingface_hub snapshot-download \
  --repo-type model \
  --repo-id Systran/faster-whisper-base \
  --local-dir /opt/workspace/yby_workspace/whisper-model
```

需要的文件：
- `model.bin`
- `config.json`
- `tokenizer.json`
- `vocabulary.txt`
