# 管线细节：数值、阈值、踩坑记录

所有数字都来自实测（许嵩《天龙八部之宿敌》，1280×720，CPU-only，12 逻辑核）。

## 00 总体

| 阶段 | 输入 | 输出 | 耗时 |
|---|---|---|---|
| 01 歌词 | 网易云 song id | `01/lyrics.json` | 2s |
| 02 音源 | B 站 BV 号 | `02/orig.wav` `02/inst.wav` `02/audio.json` | 40s |
| 03 分离 | `02/orig.wav` | `03/vocal.wav` `03/resid.wav` | 101s |
| 04 旋律 | `03/vocal.wav` + `02/inst.wav` | `04/melody.json` `04/chords.json` | 90s |
| 05 对格 | `04/melody.json` + 填词 | `05/en_lines.json` | 2s |
| 06 演唱 | `05/en_lines.json` + `02/inst.wav` | `06/vocal_*.wav` `06/mix_*.wav` | 10min |
| 07 画面 | `06/mix_*.wav` + `05/en_lines.json` | `07/full_*.mp4` | 10min |
| 08 成片 | `07/*.mp4` | `final/*.mp4` | 30s |

## 四个「写错就整轮白做」的坑

先看这一节。v1 交付后被否，全部原因都在这四条里。

1. **音符边界不能等分**（04）。按汉字数均分 slot 再取段中位 = 凭空猜音符。
   实测 52 行里 **0 行**与原唱吻合，听感就是「调子、停顿全不在原处」。
2. **低音泄漏不能当过滤墙**（04）。泄漏是一根窄尖峰（midi 45.2），用
   「中位 − N」当墙会连带删掉真实低音，旋律塌成连续同音。
3. **`n_out` 的时间轴分母是帧率不是采样率**（06）。写成 `/ SR` 会把
   4.74 秒压成 43 毫秒，整行只取第 0 帧频谱包络 → 所有元音共用一个共振峰，
   听起来像念同一个「呃」。这是「机器音」的第一真凶。
4. **TTS 的静音必须裁掉再拉伸**（06）。edge-tts 首尾带静音，被同样倍数拉长后
   变成句中长空洞。实测 `<−40dB` 占比 0.54（原唱 0.10），裁后 0.08。

## 01 歌词

`https://music.163.com/api/song/lyric?id=<id>&lv=1&kv=1&tv=-1`，必须带
`Referer: https://music.163.com`。

- 搜 id：`https://music.163.com/api/search/get?s=<词>&type=1&limit=5`。
- **同名歌很多**，用时长交叉验证（《宿敌》= 167691，263.3s）。搜到别的歌会让后面全错。
- 解析 `[mm:ss.xx]`，去掉元数据行。
- 每行槽位 `slot = min(next_t - t, 0.62 * 汉字数 + 1.2)`：
  用下一行起点会跨过间奏（实测有 28s 的长间奏），必须用字数封顶。
- 副歌重复：按行文本去重，52 行里只有 28 行唯一。

## 02 音源

B 站是唯一稳定的完整音源（网易 outer/url 已失效，第三方试听接口只给 30s）。

```
GET https://www.bilibili.com                       # 拿 buvid cookie
GET https://api.bilibili.com/x/web-interface/view?bvid=…
GET https://api.bilibili.com/x/player/playurl?bvid=…&cid=…&fnval=16&fourk=1
    → max(dash["audio"], key=lambda x: x["bandwidth"])["baseUrl"]
GET baseUrl  (Referer: https://www.bilibili.com/video/<bv>)
```

原曲与伴奏**必须对齐**：两者时长不同（265.94s vs 263.15s），直接叠加会全程错位。

- 用 chroma 互相关求偏移：`librosa.feature.chroma_cqt`，hop 2048，
  在 60–80s 的能量高峰段算，得分 0.934。
- **返回值语义写死成 `a[off + t] ≈ b[t]`**。`off = -2.60` 表示伴奏内容早 2.60s，
  要给伴奏头部补 2.60s 静音。符号搞反会让整首歌飘 5 秒。
- 波形互相关不可信（相关系数只有 0.067，全是噪声）。
- 对齐后：orig / inst 首个发声点 6.06s / 6.10s，总长 265.75s。

## 03 人声分离

MDX-Net ONNX（`aaatmy/uvr-mdx-net-onnx` 的 `UVR-MDX-NET-Voc_FT.onnx`，63.7MB，
走 hf-mirror）。

```
n_fft=6144  hop=1024  dim_f=3072  dim_t=256
输入 (4, 3072, 256) float32 = 双声道 × (实部, 虚部)
```

两个必须做对的地方：

1. **STFT 要截到 3072 个频点**（`librosa.stft(...)[:3072]`）。6144 点 FFT 给 3073 个
   频点，多一个就 `InvalidArgument: index: 2 Got: 3073 Expected: 3072`。
2. **输出是复数掩码，要和输入谱做复数乘法**，不能直接 istft：

   ```python
   re = a * mr - b * mi
   im = a * mi + b * mr
   ```

   直接 istft 输出会得到 rms 0.0004 的死寂。

实测：RTF 0.38（20s 音频 7.2s），整曲 101s；分离后谐波占比 0.29 → 0.91，
voiced 86%。**频谱相减（orig − gain×inst）试过，残余 99.5%，全是贝斯，不可用。**

## 04 旋律（v3 重写）

**只从人声轨提，绝不对伴奏做 pyin**——伴奏会给出恒定 midi 50.4 的贝斯，
voiced 只有 36.9%。

```
pyin(fmin=120, fmax=900, sr=22050, hop_length=256, frame_length=2048)
```

### 低音泄漏：陷波，不是设墙

分离后仍残留贝斯。它是**一根窄尖峰**，不是宽带。测法：只统计
「不在任何歌词行内」的 voiced 帧 F0 直方图（bin 0.25 半音），取最密 bins 的中点。
本例得到 `{midi: 45.12, frames: 5261}`。

```python
bad = np.abs(midi - leak) < 1.5     # ±1.5 半音
midi = np.where(bad, np.nan, midi)
```

v1 用的是 `floor = 全局中位 − 6 ≈ 51.2` 的硬墙，把 48–51 的**真实低音全部删掉**，
于是每行都塌成「连续同音」——这是旋律听不出起伏的第二个原因。

### 换音点：定数 DP，不是等分

约束：这一行有几个汉字，就有几个音符。

```python
def dp_fixed_k(x, k, min_len):   # x = 该行的 F0 轮廓（nan 已插值）
    # 最小化「每个音段内 F0 方差之和」
    # 前缀界把复杂度压到 O(k·n²)
```

- `k = 该行汉字数`，`min_len ≈ 3` 帧。
- 段内取中位音高作为音符，**同时保留真实 t0/t1/dur**（结构从 `int` 升级为
  `{t0, t1, dur, midi}`）。乐句的停顿感全靠这个 t0/t1，丢了下游只能重新均分。
- 定数是必须的。曾试参数化 penalty（0.6–6.0）让 DP 自己决定段数，
  结果每行切成 13–51 段 0.02s 的碎片，完全不可用。

### 其它后处理

- `clean_contour`：线性插值补洞 → 5 帧均值平滑 → 对 250ms 运行中位做八度修复
  `m - 12*np.round((m - ref)/12)`。
- `snap_light(tol=0.42)`：**只在已经离音阶 ≤0.42 半音时才吸附**，不强行改音。
  v1 无条件 snap 会把真实半音抹成音阶内音，抹掉旋律的张力。
- 重复行投票**只投票音高**，各次出现保留各自时间（三次副歌的 t0 不同）。
  投票前先按八度对齐参考副本，否则一个读低八度的副本能拉歪 12 个半音。
- 实测输出：`52 lines, 316 notes, scale proximity 252/316 = 80%,
  31 lines unified, pitch range 47.0 .. 70.0`。

第一行的修正可作为回归基准：v1 `56 56 56 56 61 58 54` →
v3 `56 49 56 56 61 57 54`，原唱实测 `56.2 48.8 56.0 56.5 60.8 57.3 53.9`。

## 05 对格

每行英文的音节数（`cmudict` 计，无词条用元音组回退）必须等于该行音符数。
不等就 `exit 1`，不要放行——少一个音节，06 会把两个音节硬塞进一个音符。

`normalise_notes()` 同时接受 v1 的 int 列表和 v3 的 dict，旧 run 不会因升级报错。
`fit_report.txt` 含押韵分组（`rhyme_key()` 取重读元音及其后所有音素）与 timing check。

## 06 演唱（WORLD 重绘，v3 重写）

思路：TTS 给出**自然音素与共振峰**，WORLD 只改 f0 与时长。

```
edge-tts (WordBoundary) → 按词切 → cmudict 按音素切音节
  → trim_silence: 裁掉首尾静音，同步位移 word marks
  → 每音节: 辅音保留原始时长(≤55ms)，元音吃掉剩余音乐时值
  → WORLD 分析 (harvest/cheaptrick/d4c) → 分段线性重采样对齐目标帧边
  → f0 = 原唱轮廓(contour_at) + 音符网格兜底
  → pw.synthesize → 轻响度归一 → 短混响 → 与伴奏混音
```

### 三个必须做对的地方

1. **`warp()` 的时间轴**：`tau = np.arange(n_out) / FPS_F + dst[0]`，
   `FPS_F = 200`（WORLD 的 5ms 帧率）。**分母写成 `SR` 就等于把整句压进 43ms**，
   所有元音共用第 0 帧的共振峰 → 机器音。修好后 pyin voiced 0.00 → 0.79，
   ASR 词召回 0% → 72%。
2. **裁静音**：`trim_silence(y, marks, thresh_db=-38.0, pad=0.02)`，按 RMS 包络找
   首个/末个超过 −38dB 的帧，切掉并同步位移 marks。不裁的话静音被同样倍数拉伸。
3. **f0 用原唱轮廓，不用阶梯音高**：阶梯式音高听感是电音化的。
   实测 jerk v1 0.0033 / v3 0.0173 / 原唱 0.0213 —— v1 把自然的音高抖动抹平了 6 倍。
   `singer_contour()` 对 `03/vocal.wav` 跑 pyin（hop 128 → fps 172.3），
   缓存在 `06/tts_cache/contour.npz`。**低于 midi 46.5 的帧置 NaN**，
   否则分离残留的次低音会在每行第一个词冒成一声低吼。`--contour 0` 可关。

### 不要再做的事

- ❌ `tanh(out*1.6)*0.62` 软限幅 —— 削波产生爆裂感（crackle）。
  改成只做响度归一 `gain = clip((med/env)**0.28, 0.55, 1.9)` + 10ms 淡入淡出。
- ❌ 噪声脉冲响应混响（`rng.standard_normal` + `fftconvolve`）—— 宽带噪声源，
  稀疏段能听到「嘶」。改用 Schroeder 梳状+全通（`room()`，无噪声源）。
- ❌ `shape_dynamics` 的盖章式逐音节包络 —— 响度过于规则 = 没有生气。

### 关键数值

- `pw.cheaptrick(x, f0, temporal_positions, fs)` 与 `pw.d4c(...)` **都必须传
  temporal_positions**，只给 3 个参数报 TypeError。
- edge-tts rate 下限 **−50%**（再低平台钳制在 3.14s 不动）。
  故 `pick_rate` 二分区 `[-50, 45]`，5 轮收敛；rate 吃不掉的交给 WORLD 拉长。
- `max_cons = 0.055s`：辅音保留时长上限。辅音一长就变成朗诵。
- 句尾音 `w[-1] = 1.25`（余韵）。
- 默认 `--octave 0`（伴奏就在原调上）、`--contour 1.0`、`--vox-gain 1.60`、
  `--inst-gain 0.60`。混音实测：人声 −20.6 dBFS、伴奏 −16.0 dBFS，
  用 1:0.82 会让人声被完全盖住。

### 已否决的路线（别再试）

- **TD-PSOLA**：HNR 与共振峰更自然（jerk 0.0192），但降八度时 grain 间距大于窗宽，
  接缝有颗粒感（hf 0.0066 vs WORLD 0.0039）；加 grain 重采样后 hf 0.0031 但
  **音高误差 12 半音**（自动选调降到 98Hz，太闷），ASR 只有 17–24%。
- **自动降八度**：按「离说话音高最近」选会把旋律压到 98Hz，ASR 反而更差。
  改为「舒适区 `[speak-2, speak+12]`，0 优先」。
- **onset 检测切音节**：实测 12 行里 exact match **0/12**，中文持续元音没有 onset。

## 07 画面

Python 逐帧画（Pillow）→ rawvideo 管道喂 ffmpeg，实测 82fps，
整曲 7973 帧约 10 分钟。比 `showcqt` / `showspectrum` 好看得多，
后两个只适合快速出个占位。

- 频谱条：64 条对数分布条带，**每条减去自己的时间中位数再除以 95 分位**。
  只用全局 max 归一化，一次贝斯重击就会把整首歌的其余部分压平。
  频点要按 bin 对齐且严格递增，否则空条带算出 NaN（`Mean of empty slice`）。
- 每帧从静帧重建背景，不要 `np.roll` 上一帧——否则上一句歌词会留残影。
- 粒子要按固定 id 运动（`ember_params(pid)`），每帧重播随机种子会让它们乱闪。
- 字幕：中英双行，英文 34px Times、中文 19px msyh，带阴影。
  第一行英文的 6.5s 内显示标题卡。
- 输出文件名必须带 voice（`full_male.mp4` / `full_female.mp4`），
  否则两个版本互相覆盖（踩过）。

## 08 成片

`loudnorm=I=-14:TP=-1.5:LRA=11`（各平台的统一化目标），视频流 `-copy` 不重编码。
`-movflags +faststart` 让网页能边下边播。
**`loudnorm` 内部会重采样到 192kHz 并保留，必须显式 `-ar 44100`**，否则成品标称 96kHz。

## 验收（`scripts/_qa_*.py`）

| 指标 | 脚本 | 门槛 | v1(旧) | v3(当前) | 原唱 |
|---|---|---|---|---|---|
| 音高误差 | `_qa_vocal.py` | < 0.5 半音 | 0.42 | **0.19 / 0.20** | — |
| HNR | `_qa_hnr.py` | > 20 dB | 17.5 | **24.0 / 22.5** | 21.9 |
| jitter | `_qa_hnr.py` | 接近原唱 | 0.70% | 0.54% | 1.59% |
| jerk | `_qa_vocal.py` | 接近 0.021 | 0.0091 | **0.0173 / 0.0176** | 0.0213 |
| ASR 词召回 | `_qa_asr.py` | > 65% | 48%(女) | **69% 男 / 74% 女** | — |
| 行内 <−40dB | `_diag_gaps.py` | < 0.15 | — | **0.08** | 0.10 |

faster-whisper 复听用 `beam_size=5, vad_filter=False`，**必须传 numpy 数组**
（传路径会抛 av 错误）。

## 已知上限

- 英文可懂度：主句全可辨，被伴奏掩住的个别人称代词/单复数仍会听错。
  这不是参数问题——真人翻唱同一个伴奏也会有同样的掩蔽。
- 音色是 TTS 的气声感，不是真人歌手的咬字与颤音。要更进一步只能上 RVC
  （见 `references/upgrade-rvc.md`），需要 GPU 或极长等待。
- 汉语声调信息在翻译时就丢了；英文靠重音位置对齐旋律，这是填词阶段决定的。
