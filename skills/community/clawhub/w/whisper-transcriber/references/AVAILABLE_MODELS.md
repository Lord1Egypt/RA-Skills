# 📦 Whisper 可用模型大全

## 基础模型（多语言）

| 模型 | 文件名 | 大小 | 速度 | 精度 | 推荐场景 |
|------|--------|------|------|------|----------|
| **tiny** | `ggml-tiny.bin` | 75 MB | ⚡⚡⚡ | ⭐⭐ | 快速测试、资源受限 |
| **base** | `ggml-base.bin` | 142 MB | ⚡⚡ | ⭐⭐⭐ | 日常使用 ⭐ |
| **small** | `ggml-small.bin` | 466 MB | ⚡ | ⭐⭐⭐⭐ | 高精度需求 |
| **medium** | `ggml-medium.bin` | 1.5 GB | 🐌 | ⭐⭐⭐⭐⭐ | 专业场景 |
| **large-v1** | `ggml-large-v1.bin` | 2.9 GB | 🐌🐌 | ⭐⭐⭐⭐⭐ | 最佳精度 |
| **large-v2** | `ggml-large-v2.bin` | 2.9 GB | 🐌🐌 | ⭐⭐⭐⭐⭐ | 最佳精度 |
| **large-v3** | `ggml-large-v3.bin` | 2.9 GB | 🐌🐌 | ⭐⭐⭐⭐⭐ | 最新最强 ⭐⭐ |

## 英语专用模型（仅英语）

| 模型 | 文件名 | 大小 | 速度 | 精度 | 说明 |
|------|--------|------|------|------|------|
| **tiny.en** | `ggml-tiny.en.bin` | 75 MB | ⚡⚡⚡ | ⭐⭐ | 仅英语 |
| **base.en** | `ggml-base.en.bin` | 142 MB | ⚡⚡ | ⭐⭐⭐ | 仅英语 |
| **small.en** | `ggml-small.en.bin` | 466 MB | ⚡ | ⭐⭐⭐⭐ | 仅英语 |
| **medium.en** | `ggml-medium.en.bin` | 1.5 GB | 🐌 | ⭐⭐⭐⭐⭐ | 仅英语 |

## 量化模型（更小更快）

| 模型 | 文件名 | 大小 | 精度损失 | 推荐 |
|------|--------|------|----------|------|
| **base-q5_1** | `ggml-base-q5_1.bin` | 57 MB | 极小 | ⭐⭐⭐⭐⭐ |
| **base-q8_0** | `ggml-base-q8_0.bin` | 78 MB | 几乎无 | ⭐⭐⭐⭐⭐ |
| **small-q5_1** | `ggml-small-q5_1.bin` | 181 MB | 极小 | ⭐⭐⭐⭐ |
| **small-q8_0** | `ggml-small-q8_0.bin` | 252 MB | 几乎无 | ⭐⭐⭐⭐ |
| **medium-q5_0** | `ggml-medium-q5_0.bin` | 514 MB | 极小 | ⭐⭐⭐⭐ |
| **large-v3-q5_0** | `ggml-large-v3-q5_0.bin` | 1.1 GB | 极小 | ⭐⭐⭐⭐⭐ |

## 特殊模型

| 模型 | 文件名 | 大小 | 用途 |
|------|--------|------|------|
| **large-v3-turbo** | `ggml-large-v3-turbo.bin` | 1.5 GB | 大模型的快速版 |
| **large-v3-turbo-q5_0** | `ggml-large-v3-turbo-q5_0.bin` | 547 MB | 涡轮量化版 |
| **tiny.en-tdrz** | `ggml-tiny.en-tdrz.bin` | 75 MB | 带说话人检测 |

---

## 🎯 推荐选择

### 中文场景
```
首选：ggml-large-v3.bin (精度最高)
平衡：ggml-base.bin (当前使用)
轻量：ggml-base-q5_1.bin (体积小)
```

### 英语场景
```
首选：ggml-large-v3.bin
平衡：ggml-base.en.bin
轻量：ggml-base.en-q5_1.bin
```

### 资源受限
```
推荐：ggml-base-q5_1.bin (57MB)
或：ggml-tiny.bin (75MB)
```

---

## 📥 下载命令

```bash
# 进入模型目录
cd ~/.agents/skills/whisper-transcriber/assets/models/

# 下载 large-v3（推荐）
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin

# 下载 base-q5_1（轻量）
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base-q5_1.bin

# 下载 small-q8_0（平衡）
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small-q8_0.bin
```

---

## 📊 性能对比（M4 Pro）

| 模型 | 3 秒音频 | 10 秒音频 | 60 秒音频 |
|------|---------|----------|----------|
| tiny | ~80ms | ~200ms | ~1s |
| base | ~130ms | ~350ms | ~2s |
| small | ~300ms | ~800ms | ~4s |
| medium | ~600ms | ~1.5s | ~8s |
| large-v3 | ~800ms | ~2s | ~10s |
| large-v3-q5_0 | ~600ms | ~1.5s | ~8s |

---

## 💡 选择建议

1. **日常使用** → `base` (当前)
2. **高精度需求** → `large-v3`
3. **资源受限** → `base-q5_1`
4. **英语专用** → `*.en` 系列
5. **最佳平衡** → `large-v3-q5_0`

---

_最后更新：2026-03-06_
