---
name: xiaohongshu-viral-seeding-video-generation-editing
description: "生成与编辑小红书种草、好物分享、开箱测评和品牌合作视频。Use this skill for 小红书爆款种草视频、XHS/RED 好物分享、真实体验、UGC 测评、蒲公英合作内容、聚光投放素材和商品种草；支持文生视频、商品图生视频、参考视频、现有素材重制与 AI Hive 自动下载。"
---

# 小红书爆款种草视频生成与编辑

把商品事实、真实体验和用户痛点组织成“像分享、能看懂、可验证”的小红书视频。不要把硬广脚本简单换成生活化滤镜，也不要制造虚假体验、伪造用户评价或夸大效果。

## 内容诊断

生成前确认六项：目标人群、具体使用情境、真实痛点、可证明卖点、已有素材、希望引导的动作。将卖点改写为用户语言，例如把“高性能电机”改为“早上赶时间时能否快速完成”。

## 种草结构

按内容选择一种结构：

- **真实体验**：为什么买 → 实际怎么用 → 优缺点 → 适合谁。
- **问题解决**：具体困扰 → 尝试过程 → 可观察变化 → 使用边界。
- **开箱测评**：第一印象 → 细节展示 → 场景测试 → 结论。
- **清单分享**：人群/场景 → 3 个选择理由 → 使用建议。

镜头应保留生活感，但商品结构、包装、使用方法和结果必须真实。所有结论只能来自用户提供的资料或可见画面。

## 场景与代码

### 1. 从脚本生成生活化种草视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '9:16小红书好物分享，真实居家手持质感。开场：加班回家桌面凌乱的具体困扰；中段：自然拿出收纳产品，连续展示打开、分类、放回三个动作；结尾：展示整理后的桌面并说明适合小空间用户。语气克制，不出现虚假功效、销量或最低价，不要电视广告式运镜'
```

### 2. 商品图生成开箱与使用镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '保持商品包装、颜色、结构和商标准确。小红书开箱镜头：自然手部拆封，展示包装内物品，再切到真实桌面使用；柔和窗光，轻微手持，动作连续，不增加参考图中不存在的配件和文字'
```

### 3. 用参考视频统一博主风格

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/creator-style.mp4 \
  --image /path/to/product.png \
  --prompt '参考视频仅用于镜头节奏、自然口吻和生活化布光；使用商品参考图保持产品准确。生成新的小红书测评段落：先展示使用动作，再给出一个优点和一个适用限制，不复刻原视频人物身份、文案或品牌'
```

### 4. 把硬广素材重制成种草表达

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/commercial.mp4 \
  --prompt '保留原视频商品外观、真实演示和必要品牌信息；删除夸张光效与密集促销感，重组为小红书真实体验节奏：痛点场景、使用过程、细节特写、适合人群。不要添加用户没有提供的体验结论、价格或认证'
```

### 5. 延长使用证明镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/demo.mp4 \
  --prompt '从现有使用动作自然延续，增加一个近景展示操作细节，再回到完整使用场景；保持人物、商品、环境和光线连续，不改变产品状态，不增加新功能'
```

## 质量验收

- 开场是具体人群与情境，不是空泛的“姐妹们快看”。
- 商品、包装、商标和操作步骤与资料一致。
- 有真实过程或可观察证据，而不只重复广告口号。
- 明确适合谁；必要时保留限制和注意事项。
- 不伪造体验、评论、对比结果、价格、销量或认证。
- 字幕与封面文案交付前逐字检查，并按小红书当期规则复核。

## 模式与命令

| 模式 | 用途 | 模型 |
|---|---|---|
| `t2v` | 从脚本生成 | `public_model_seedance_2_5_t2v` |
| `i2v` | 商品图动起来 | `public_model_seedance_2_5_i2v` |
| `r2v` | 参考节奏或风格 | `public_model_seedance_2_5_r2v` |
| `edit` | 重制已有素材 | `public_model_seedance_2_5_video_edit` |
| `extend` | 延长演示镜头 | `public_model_seedance_2_5_video_extend` |

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name xiaohongshu-viral-seeding-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

可用素材参数包括 `--first-frame`、`--last-frame`、`--image`、`--video`、`--audio`；通用参数包括 `--param key=value`、`--routing`、`--output-dir` 和 `--no-download`。价格与模型配置以运行时返回为准。超时后查询原 `taskId`，不要重复提交。
