# Model Contracts — SoulX-Singer / RMVPE / Whisper

## SoulX-Singer（704M 参数，Apache-2.0）

### 模型 IO
- 输入：`prompt_wav + prompt_metadata.json + target_metadata.json`
- 输出：24kHz 单声道 wav
- `model.pt` 2.82GB + `config.yaml`

### 元数据格式
每段 target 是一个 dict：
```json
{
  "time": [start_ms, end_ms],
  "duration": "0.23 0.34 0.26 ...",
  "phoneme": "<SP> en_HH-UW1 en_W ...",
  "note_pitch": "0 68 67 65 ...",
  "note_type": "1 2 2 2 3 ...",
  "f0": "0 220.5 233.1 ..."
}
```
- `note_type`: 1=休止, 2=普通音, 3=同字延音（lyric 写 `-`）
- `note_pitch`: MIDI 音高，0=休止
- `phoneme`: 空格分隔音素

### 音素格式
- 英文：`en_HH-UW1`（ARPAbet + 重音数字），多音节用 `-` 连接
- 中文：`zh_<拼音+声调>`（如 `zh_chu2`），整音节不拆分
- phone_set.json 共 2820 符号：前 9 个特殊符号 + `en_*` 70 个 + `zh_*` 1201 个

### 推理接口
```python
model.infer(meta, auto_shift=False, pitch_shift=0, n_steps=32, cfg=3, control="score", use_fp16=True)
```
- `control="score"`：音高由 `note_pitch` 决定，不需要 f0
- `auto_shift` 与 `pitch_shift` 互斥；**建议关闭 auto_shift**
- fp16 时 `model.half()` 但 `model.mel` 必须保持 fp32

### DataProcessor 注意
- `process(meta, wav)` **会就地修改 meta**（字符串→list）
- 修复：`json.loads(json.dumps(meta))` 深拷贝
- `sample_rate=24000, hop_size=480` → 50 帧/秒

## RMVPE（音高提取）

### ONNX IO
- 输入：`tensor(float) [1, 128, 'time']`（128 维 mel）
- 输出：`tensor(float) [1, T, 360]`（360 个 20-cent bin salience）

### 前端（必须精确）
- 采样率 **16kHz**，hop 160，n_fft 1024，128 mels，fmin 30，fmax 8000
- 变换：`np.log(np.maximum(fb @ spec, 1e-5))` + `htk=True` + `norm='slaney'`
- 时间轴补齐到 32 的倍数
- **输入必须 16kHz**（24kHz 会偏低 7.02 半音）

### cents 映射
```python
CENTS = 20.0 * np.arange(360) + 1997.3794084376191
f0 = 10.0 * 2**(cents/1200)
```
- `conf > 0.10` 才算有声

## Whisper-base（ASR 质检）
- **必须 16kHz 输入**（WhisperFeatureExtractor 硬编码）
- 24kHz 输入需 `soxr.resample(y, 24000, 16000)`

## UVR MDX-Net（人声分离）
- `N_FFT=6144, DIM_F=3072`，设计采样率 **44100Hz**
- 喂 22050Hz 会把内容当低八度处理
