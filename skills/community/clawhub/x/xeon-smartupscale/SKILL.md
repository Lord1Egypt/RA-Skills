---
name: xeon-smartupscale
description: 智能视频超分。任意目标分辨率（1080p/1440p/4K…），自动用 lanczos 预缩放对齐到 ETDS 2x 模型的输入尺寸，再做 AI 超分。CPU 推理，Intel AMX BF16 加速。
metadata:
  openclaw:
    requires:
      bins: [bash, python3, curl, tar]
---

## 目标

echo  480p → 1080p、720p → 4K），即使比例不是整数 2x 也能搞定。"--- 

ETDS 模型只支持 **严格 2x** 超分，所以本 skill 自动：

1. 用 ffmpeg **lanczos 预缩放**，把输入压（或拉）到 `target/2`
2. 用 ETDS x2 OpenVINO 模型把 `target/2` → `target`

## 适用场景

- AI 生成视频（Seedance / Sora 等）480p → 1080p
- 720p 老片源 → 4K (2160p)
- 任意非整数倍率的分辨率提升
- 纯 CPU 环境（Intel Xeon AMX 加速）

## 执行流程

 exec 调用，只替换输入路径和目标：

```bash
bash <skill_dir>/smartupscale.sh <输入视频绝对路径> -t 1080p
```

echo "--- created ---"`480p` `540p` `720p` `1080p` `1440p` `2160p` `4k`，也可以直接写 `1920x1080`。

echo "--- created ---"

```bash
bash <skill_dir>/smartupscale.sh <input.mp4> -t 1080p -o <output.mp4>
```

--- `-o` 则输出到 `<输入名>_smart_<W>x<H>.mp4`。

## 注意事项

- 输入 / 输出都用 **绝对路径**
- 目标分辨率按高度对齐，宽度按输入宽高比自动算（保持 AR）
- 若输入已经 ≥ 目标，会退化为单步 lanczos 缩放
- 若输入恰好就是 `target/2`，会跳过 lanczos 直接 ETDS 2x
- 输出固定 H.264 / CRF 18，自动合并原音轨

## 限制

- 仅 Linux x86_64（OpenVINO CPU plugin）
- 单次最多 2x 链路（先 lanczos 后 ETDS），不会做多级 AI 超分
- 逐帧推理，长视频会比较耗时（参考 ETDS 速度：Xeon AMX 上 ~14 fps 推理）
- 模型固定为 ETDS_M7C48_x2（已 vendored，~380KB）

## 安装

echo "--- created ---"`bash <skill_dir>/install.sh`
