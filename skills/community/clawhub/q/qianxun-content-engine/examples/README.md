# Examples · 真实产出参考

这里是用 Content Engine v0.2.0 跑出的**真实产出**，作为学习样本和质量基线。

不是模板，是实物——你能看到「拆解卡 → 我方版本」整条链路的真实形态。

---

## 三个示例

```
examples/
├── v1-deconstruction-card/         ← 起点：v1 拆解一条爆款链接得到的拆解卡
│   └── AIC-260426-001-deconstruction.md
│
├── v2-image-example/               ← v2 image 类型产出（基于上面的拆解卡）
│   ├── script.md                   图组规划（6 张图 + 整组叙事）
│   ├── cover.png + cover.txt       封面图（含中文大字层）+ 文案
│   ├── frames/frame_001.png        参考素材图（Nano Banana 出，竖版 9:16）
│   ├── desc.txt                    XHS 发布正文
│   └── tags.txt                    话题标签
│
└── v2-video-example/               ← v2 video 类型产出（同一拆解卡）
    ├── script.md                   视频脚本（5 个 shot 分镜）
    ├── caption.txt                 视频内字幕
    ├── cover.png + cover.txt       封面图 + 文案
    ├── frames/frame_001.png        关键帧（1 张，给摄影师看分镜参考）
    ├── desc.txt + tags.txt         发布素材
    └── seedance-prompt.md          Seedance 2.0 cinema-style prompt
                                    (v2.0 不真生视频，输出此 prompt 取代真视频；
                                     v2.1 接 Seedance API 后会自动执行)
```

---

## 这些示例怎么来的

### 输入

```bash
# 拆解（v1）— 先得拆解卡
python3 scripts/extract_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a"

# 生成（v2）— 基于拆解卡 + 我方品牌
python3 scripts/generate_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a" \
  --type image --count 1 \
  --product-usp "新中式女装：真丝马甲 + 立体绣衬衫"

python3 scripts/generate_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a" \
  --type video --count 1 \
  --product-usp "新中式女装：真丝马甲"
```

### 参考的对标内容

XHS 链接 `69d4e2f7000000002202853a` 是「见花开 / 深圳新中式 / 把江南春色穿在身上是什么体验？」34 秒陈列短视频，330 赞 / 231 藏 / 133 评（藏赞比 70%）。属于"沉浸式陈列"型爆款。

### 我方品牌设定（演示用）

`--product-usp "新中式女装：真丝马甲 + 立体绣衬衫"` —— **fictional 演示数据**，不是真实品牌。生产中你会传自家产品的卖点。

### 性能数据

| 类型 | 文本调用 | 图片调用 | 总耗时 | 总成本估算 |
|---|---|---|---|---|
| image (count=1) | 4 | 2 | ~127s | ~$0.20 |
| video (count=1) | 5 | 2 | ~190s | ~$0.30 |

---

## 看这些示例时关注什么

### v1 → v2 的对应关系

打开 `v1-deconstruction-card/...md` 和 `v2-image-example/script.md` 对比看：

- 拆解卡 §4「参考内容拆解」的"沉浸式陈列三层结构"→ image script.md 的"图组规划三层叙事"
- 拆解卡 §7「情绪钩子」的「向往感｜画面氛围代入」→ image script.md 的钩子复用
- 拆解卡 §13「参考发布文案」的克制留白调性 → desc.txt 的延续

**v2 不是凭空生成，是有依据的"对标复刻"**。

### 视觉一致性

打开 `v2-image-example/cover.png` 和 `v2-image-example/frames/frame_001.png` 看：

- ✅ 都是竖版 9:16
- ✅ 都是单图（没有拼图）
- ✅ 风格契合（克制东方美学 / 自然光 / 工艺质感）
- ✅ cover 自带中文大字"把一朵花绣进春天里"

这些是 v2 经过 3 轮 fix 后的稳定品质——`build_prompt` 的"三路约束 + 防拼图"机制起作用。

### Seedance prompt 的形态

打开 `v2-video-example/seedance-prompt.md` 看 5 个 shot 的标准 6 维参数（shot type / subject / setting / camera movement / mood / duration）。这就是 v2.1 接入 Seedance 后能直接喂模型的格式。

文件顶部有引用块说明 v2.0 现阶段的使用路径（手动跑 / 等 v2.1 / 给摄影师参考）。

---

## 不是这些示例的「用法」

⚠️ **请不要直接复制这些产出去发布**。理由：

1. 我方品牌信息是 fictional 演示（"见花开"是对标账号名，不是我方）
2. 你的实际场景里 brand-voice / brand-story / segments 应该填好（这次跑的是客观模式，graph 未填充）
3. 真实使用时建议先填 graph 再 generate，输出会从"通用风格"升级为"品牌化"

正确用法：**当作 quality baseline 看**——你跑出的产出应该达到这个水准（或更高）才发布。

---

## 复现成本

- 拆解 1 次 ≈ $0.50（TikHub API + LLM 视觉理解 17 帧）
- 生成 image (count=1) ≈ $0.20
- 生成 video (count=1) ≈ $0.30
- **完整 pipeline 一次 ~$1**

实际批量使用时（拆 1 次 + 生成多次变体），单次拆解可分摊到多个生成任务。
