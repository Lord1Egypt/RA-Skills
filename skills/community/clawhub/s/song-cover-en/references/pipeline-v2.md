# Pipeline v2 — 技术细节与踩坑记录

## 管线架构

```
01_lyrics.py    网易云歌词抓取
02_audio.py     B 站伴奏/原曲下载 + 对齐
03_separate.py  UVR MDX-Net 人声分离
04_melody.py    RMVPE 音高提取 + 音符切分
  [人工/LLM 写英文歌词]
05_align.py     DP 单调对齐 + SoulX 元数据构造
06_svs.py       SoulX-Singer 神经歌声合成
spectral_match.py  LTAS 频谱匹配（消除机器音）
add_vibrato.py     分数延迟颤音增强
mix_song.py        人声+伴奏混音 + 软限幅
07_art.py       ComfyUI 意象配图
08_video.py     歌词视频合成
```

## 关键踩坑记录

### 1. RMVPE 前端标定（决定音高准不准）
- **正确前端**: `np.log(np.maximum(fb @ spec, 1e-5))` + `htk=True` + `norm='slaney'`
- **错误前端**（dB 变换）: confidence 崩塌（median 0.03 vs 正确 0.55），人声帧被大量切掉
- **阈值**: `CONF_TH=0.10`（用官方 example 的 note_pitch 真值标定 F1 最高）
- **校准方法**: 官方 `en_target.mp3` + `en_target.json` 构成闭环标定集，扫 720 组前端参数

### 2. 音符碎片化（"念而非唱"的根因）
- RMVPE 忠实跟随细小音高抖动，`segment_notes` 把持续音切成 80ms 碎片
- 神经歌手需要几十毫秒建立元音共振峰，80ms 碎片只能发瞬态
- **修复**: `detrend_vibrato(midi, fps, win_s=0.20)` + `absorb_shards(notes, min_sung=0.12)`
- 效果: 中位音节 0.22s → 0.47s，<0.10s 音节 18% → 0%

### 3. LRC 时间戳不可靠
- 逐行抖动可达 ±6s（`drift = +0.0038*t - 0.79`，residual stdev 2.41s）
- **不能用 LRC 的 next_t 切音符**，必须由音符驱动对齐

### 4. DP 单调对齐（消除"英文段吞下一句"）
- 原方案按汉字数比例切割时间轴 → 音符密度不均匀 → 行边界漂移
- **修复**: `align_lines_to_notes(notes, need)` 动态规划，代价 `(k-need[i])²`
- 行边界严格连续不漂移，验证 0/52 行偏差

### 5. auto_shift 有害
- `auto_shift` 逐段计算 `f0_shift = round(median(prompt) - median(target))`
- 不同段落 shift 不同（+1/-1），破坏与原调一致性
- **修复**: `--no-auto-shift`（默认关），`control="score"` 时音符已锁音高

### 6. 分块渲染（解决超线性开销）
- 模型代价随序列长度超线性增长（79.4s→43s，117.6s→1909s）
- **修复**: `split_segment(seg, max_s=22)` + `--chunk-s 22`
- 切点必须在词边界（`word_start` 标志），否则 ASR 召回从 40% 掉到 32%

### 7. 扩散随机性（"嘶哑/机器音"的根因之一）
- `flow_matching.py` 的 `z = torch.randn(...)` 无 seed，每次渲染是新抽样
- fp16 vs fp32 corr 仅 0.05，证明不是精度问题
- **修复**: `--seed 42` + `torch.manual_seed(a.seed + ci)`

### 8. 频谱失衡（"机器音"的根因之二）
- 模型 1-3kHz 只有真人的 1/8，80-300Hz 是真人的 5.6 倍
- **修复**: `spectral_match.py` 零相位 LTAS 匹配到真人参考
- 效果: mid 10%→27.6%（真人 39.8%），low 35%→12.4%（真人 1.6%）

### 9. QA 采样率 bug
- RMVPE 假设 16kHz 输入，喂 24kHz → 所有音高偏低 7.02 半音
- **修复**: `soxr.resample(y, sr, 16000)` 喂进 RMVPE 前

### 10. UVR 分离采样率
- MDX-Net 设计采样率 44100Hz，喂 22050Hz → 人声被带限到约 1kHz
- **修复**: 用 44100Hz 输入（或接受音色带限 + 频谱匹配补偿）

### 11. DataProcessor 就地修改 meta
- `process()` 把 meta 的字符串字段改成 list，第二次调用报 `AttributeError`
- **修复**: `json.loads(json.dumps(meta))` 深拷贝

### 12. ComfyUI 分辨率限制
- `1344x768` 会 VAE 解码失败（`RuntimeError: Fault failed: 2`）
- **可用**: `1152x648` 或 `1024x576`

### 13. build_segment 空段
- 相邻 LRC 行音符窗口重叠，`sum(dur)` 超过窗口 → `fix` 变负 → 返回 None
- **修复**: 排序后先丢「被后一音符几乎完全覆盖」的音符

### 14. 变量遮蔽 bug
- `08_video.py` 内层 `for k in range(hgt)` 用 `a` 作混合系数，遮蔽 argparse 的 `a`
- **修复**: 改名 `blend`
