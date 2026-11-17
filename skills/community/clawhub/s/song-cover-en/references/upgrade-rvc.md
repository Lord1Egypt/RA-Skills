# 升级路径：让音色更像真人歌手（RVC）

当前管线在 06 阶段用的是 TTS 的音色。音高、时长、共振峰都对，
但咬字是播音腔，没有歌手的沙哑、气声和颤音。要跨过这一步只有换音色模型，
本机能提供的选择如下。

## 为什么不默认开

- **无 GPU**：AMD/Intel 集显，torch CPU 推理一首 4 分钟的歌是分钟到小时级，
  且 RVC 的 f0 提取（rmvpe）在 CPU 上比 GPU 慢一个数量级。
- 模型体积大：hubert 360MB + rmvpe 345MB + 目标音色模型 100MB 起。
- 链路长：HuBERT 特征 → 音色转换 → 再叠回 WORLD 的 f0/时长，任一环出错都是噪音。

所以把它标成可选升级，而不是默认路径。

## 已核实的可用资产（都从 hf-mirror 走）

| 文件 | 体积 | 来源 |
|---|---|---|
| `vec-256-layer-9.onnx` | 279.8MB | `ozada/onnx_rvc` |
| `rmvpe.onnx` | 344.9MB | `ozada/onnx_rvc`（或 `ohnoitsaninja/rvc-base-onnx` 的 `assets/rmvpe.onnx`） |
| `hubert_base_layer12_nomask_32000.onnx` | 360.1MB | `ohnoitsaninja/rvc-base-onnx` |
| `beyonce.onnx` | 105.4MB | `ozada/onnx_rvc`（示例音色） |

`vec-256-layer-9.onnx` 已实测可加载：

```
输入: ('source', [1, 1, 'sample_length'])
输出: ('embed', ['Addembed_dim_0', 'Addembed_dim_1', 256])
```

即 256 维 HuBERT 特征，采样率 16k。

## 接入方式

最省事的位置是 **06 与 07 之间**，把 `06/vocal_male.wav` 当成 RVC 的输入源：

```
vocal_*.wav  →  RVC(音色模型)  →  vocal_*_rvc.wav  →  重新混音  →  07
```

这样 07/08 完全不用改。注意：

1. RVC 自己会改 f0 和时长；**转换后必须再校一次音高**（逐音节 midi 中位数），
   否则 `--voice male` 那条链路上辛苦对齐的旋律会被它带跑。
2. 转换后响度会变，`06_sing.py` 里的 `vox_gain = 1.85` 要重测。
   测法：`20*log10(rms)`，人声要比伴奏高 5–7 dB。
3. 音色模型要与歌的调性、性别匹配。拿女声模型转男声旋律会出假声。

## 训练自己的音色（需要 GPU）

不要在本机试。要训练就在有显卡的机器上跑 RVC 官方训练脚本，
需要 10 分钟以上的干净人声、无混响、无伴奏。训练完导出 ONNX 再拷回来。

## 其他候选路线（都因为无 GPU 否决）

| 方案 | 否决原因 |
|---|---|
| ACE-Step / DiffRhythm | 扩散模型，CPU 上整曲是小时级 |
| so-vits-svc | 需训练，且推理依赖 GPU |
| DiffSinger 英文歌声 | hf-mirror 上只有角色模型（nyaru 等），无通用英文音色 |
| OpenUtau | 无现成 Windows 包与英文音源库 |

如果哪天有了 GPU，DiffRhythm（`ASLP-lab/DiffRhythm-1_2`）是最省事的方向：
给它歌词和参考音频，它直接出整曲人声，可以完全取代 04/05/06 三个阶段。
