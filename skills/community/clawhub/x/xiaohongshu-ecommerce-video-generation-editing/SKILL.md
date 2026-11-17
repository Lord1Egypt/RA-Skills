---
name: xiaohongshu-ecommerce-video-generation-editing
description: "为小红书电商与品牌合作生成和编辑商品页演示、可购物笔记视频、开箱测评、蒲公英合作及聚光投放素材。Use this skill for 小红书电商视频、小红书商品视频、可购物笔记、品牌合作、蒲公英、聚光广告、开箱、真实测评、商品演示和UGC素材；支持 Seedance 与 AI Hive 自动交付。"
---

# 小红书电商视频生成与编辑

把商品事实放进真实内容表达，同时满足品牌审核与购买理解。该 Skill 偏向可购物笔记、商品页和商业合作交付，不承诺爆款，也不生成虚假体验与评论。

## 商业内容简报

确认笔记主题、真实使用资料、商品与包装、可证明卖点、适用人群、限制、创作者授权、合作披露、品牌审核点和目标动作。先锁定事实，再设计内容语气。

## 场景与代码

### 1. 可购物笔记商品演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '9:16小红书可购物笔记视频，保持商品包装、Logo、颜色与配件准确；从真实使用问题进入，连续展示操作、一个细节证据和适合人群，生活化但清楚，不生成体验结论、价格、评论、功效或商品标签UI'
```

### 2. 开箱与包装内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '小红书开箱视频，根据商家资料连续拆封，清楚展示主商品和已提供配件，再完成第一次正确使用；自然手机拍摄感，不增加赠品、惊喜反应、用户评价、价格或未提供功能'
```

### 3. 蒲公英品牌合作版本

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/creator-draft.mp4 \
  --prompt '在保留创作者身份、真实体验和商品演示的前提下整理品牌合作版：压缩重复段落，补一个清楚细节证据，为批准的合作披露和商品信息留位置；不改变创作者原意，不新增背书、承诺或优惠'
```

### 4. 参考内容节奏但保持原创

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/note-rhythm.mp4 \
  --image /path/to/product.png \
  --prompt '只参考视频的生活化节奏、镜头时长和证据顺序，使用准确商品生成原创小红书内容；不复制创作者、台词、场景、品牌、音乐、评论或具体体验结论'
```

### 5. 聚光广告清晰版

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/organic-note.mp4 \
  --prompt '重制为聚光广告“使用过程”版本：保留创作者与真实商品，把具体问题前置，压缩寒暄，完整保留操作和细节证明，结尾只留一个行动位置；不增加评价、前后效果、优惠或稀缺性'
```

## 商业内容验收

- 商品、创作者、体验资料和操作事实真实连续。
- 开箱内容与包装清单准确。
- 合作版不改变创作者表达含义。
- 披露、商品标签、价格和 CTA 在正式发布流程添加。
- 不伪造评论、点赞、收藏、体验或效果。
- 发布前按小红书社区、电商和商业合作当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name xiaohongshu-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

使用文生、图生、参考、编辑或延长模式，按需传入素材、参数、路由与输出目录。
