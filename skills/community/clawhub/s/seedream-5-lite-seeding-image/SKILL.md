---
name: seedream-5-lite-seeding-image
description: "使用 Seedream 5.0 Lite 为推荐笔记建立可见事实、作者判断与需证明说法的分层画面，并预留合作关系和 AI 合成披露。Use this skill for Seedream 5 Lite recommendation visuals、种草图片、小红书笔记、抖音好物内容、Instagram UGC、创作者合作图、开箱观察、使用记录、生活方式内容和透明商业传播；通过 AI Hive 处理授权素材。"
---

# Seedream 5.0 Lite 种草图片

固定使用 `public_model_seedream_5_0_lite`。把推荐内容拆为三种来源：镜头直接呈现的东西、作者完成真实试用后才能写的判断、品牌必须拿材料证明的说法。生成阶段只负责第一层视觉；其余两层分别交给创作者和合规负责人确认。

## 三级证据表

建立一张说法登记表，逐项填写 SKU 资料、拍摄身份、物品实际摆放、肉眼可见细节、作者待确认感受、证明文件编号、禁止措辞、合作关系标识、AI 合成标识和画布位置。无法落到资料或真实体验的句子不进入发布稿。

## 场景与代码

### 1. 水彩工具开箱观察

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-watercolor-kit.png \
  --prompt '制作水彩工具开箱观察图：保持参考颜料盒、色块数量、画笔、调色盘、包装和Logo，按实际装箱内容俯拍展开，右侧留创作者笔记与合作披露区；只展示可见物品与颜色，不生成绘画水平承诺、用户评价、文字、价格或额外画材' \
  --param aspect_ratio=3:4
```

### 2. 旅行收纳实装

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-packing-cubes.png \
  --prompt '生成旅行收纳袋实装观察图：保持三个收纳袋的尺寸、网面、拉链、颜色和Logo，打开行李箱展示按真实尺度放入衬衫、袜子和洗漱包，左侧留内容说明与合作披露区；不生成容量数字、压缩倍数、航空公司标识、人物、文字或第四个收纳袋' \
  --param aspect_ratio=4:5
```

### 3. 宠物用品日常摆放

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-feeding-mat.png \
  --prompt '把参考宠物餐垫放在家中喂食角，保持轮廓、材质、颜色、纹理和Logo，放置两个已确认适配的无品牌食碗，画面顶部留日常记录和披露区；不生成宠物健康改善、清洁测试、文字、价格、宠物身份或额外商品' \
  --param aspect_ratio=3:4
```

### 4. 阳台园艺记录

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-watering-can.png \
  --prompt '制作浇水壶阳台园艺记录图：保持壶身、壶嘴、把手、颜色和Logo，在普通阳台花盆旁展示正常拿取状态，右下留合作披露与使用笔记区；不生成植物生长前后对比、容量数字、人物脸、文字、价格或第二把浇水壶' \
  --param aspect_ratio=4:5
```

### 5. 黑胶唱片清洁流程

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-record-brush.png \
  --prompt '生成黑胶唱片刷使用记录图：保持参考刷子的握柄、刷毛、颜色、Logo和包装，在唱片机旁展示沿唱片纹路轻刷的正常动作，另附刷毛局部近景，顶部留操作说明与披露区；不生成音质提升结论、用户评价、文字、价格或第二把刷子' \
  --param aspect_ratio=4:5
```

## 发布核验与留档

- 为成图中每个物件和暗示标注来源：SKU资料、现场观察或允许生成。
- 作者判断必须在真实试用后单独签认，不能由模型代写成“亲测”。
- 品牌说法关联证明文件和批准人；缺少编号就从图文方案移除。
- 合作关系与合成标识在首屏可见，不藏进折叠区或容易裁掉的位置。
- 归档原始商品资料、说法登记表、生成任务、人工修改和发布链接，便于撤回与更正。

## 助手边界

该命令行入口只做 Seedream 5.0 Lite 图片任务：接收文字，可选读取命令里点名的图片，向 `https://ai-hive.iclip.cn/api` 查询价格与提交任务，再把结果保存到指定目录。接口地址不可改写；工具不读取账户资料，也没有对话、视频和资金相关命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-seeding-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不得伪造消费者证言、达人合作、检测、疗效、销量或使用前后结果；平台规则以发布当天为准。
