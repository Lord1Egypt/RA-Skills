---
name: xiaohongshu-ecommerce-image-generation-editing
description: "为小红书电商与品牌合作生成和编辑商品卡图片、笔记轮播、真实使用图、卖点证明及聚光广告素材。Use this skill for 小红书电商图片、小红书商品图、笔记轮播、种草套图、品牌合作、蒲公英、聚光广告、好物分享、商品详情和UGC素材；支持参考图保真及 AI Hive 生成。"
---

# 小红书电商图片生成与编辑

为“笔记内容 → 商品理解 → 购买决策”建立图片序列。它不同于笔记封面：首图负责吸引，后续图片需要呈现真实使用、细节证据、适合人群与购买边界。

## 笔记商品资料

收集商品、包装、真实体验资料、使用步骤、可证明卖点、适用与不适用情境、合作披露要求、品牌色和批准文案。不要生成虚假使用心得、买家评论、前后效果或未经提供的功效。

## 场景与代码

### 1. 商品卡准确图片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书商品卡图片，准确保留参考商品、包装、Logo、颜色和配件；主体完整清晰，背景自然生活化但不遮挡商品，适合手机浏览，不添加价格、评分、销量、平台标签、体验结论或功效' \
  --image /path/to/product.png
```

### 2. 种草笔记轮播

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成5张小红书种草轮播：具体使用困扰、商品出现、操作过程、细节证明、适合人群总结；保持商品和人物一致，每张只承担一个信息任务，真实生活摄影，预留短文案区，不伪造评价和结果' \
  --image /path/to/product.png \
  --image /path/to/person.png \
  --batch 5
```

### 3. 开箱与包装清单

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书开箱内容图，真实手部打开参考包装，清楚摆放主商品和已提供配件，每件只出现一次，商品文字与颜色保持准确；不添加赠品、惊喜反应、买家评价或优惠信息' \
  --image /path/to/package-contents.jpg
```

### 4. 品牌合作视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书品牌合作内容底图，创作者在真实场景自然使用准确商品，构图保留合作披露与审核文案区域，画面克制可信；不生成蒲公英标签、合作声明、用户反馈、折扣或未批准主张' \
  --image /path/to/creator.png \
  --image /path/to/product.png
```

### 5. 聚光广告图片假设

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一小红书商品生成3个聚光图片版本：真实痛点场景、使用过程、细节证据；保持商品、创作者与品牌色一致，每版只改变沟通假设，预留批准文案区，不生成前后效果、评论或承诺' \
  --image /path/to/product.png \
  --batch 3
```

## 内容验收

- 图片序列能从情境、使用到证据逐步回答购买问题。
- 商品、包装、创作者和操作连续准确。
- 使用心得与效果只来自真实资料。
- 合作披露、价格、商品标签和 CTA 在正式发布流程中添加。
- 不伪造评论、收藏、点赞、评价或转化结果。
- 发布前按小红书社区、电商与商业内容当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name xiaohongshu-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

可使用多张参考图、批量、实时模型参数、路由、输出目录与仅提交模式。保留每张图在笔记序列中的职责。
