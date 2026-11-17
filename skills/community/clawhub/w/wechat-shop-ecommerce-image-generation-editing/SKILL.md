---
name: wechat-shop-ecommerce-image-generation-editing
description: "为微信小店、视频号、社群和朋友圈生成与编辑商品卡、私域海报、直播预告及复购图片。Use this skill for 微信小店电商图片、微信小店商品图、视频号带货封面、社群团购、朋友圈素材、直播预约、公众号配图、私域转化和会员复购；支持参考图与 AI Hive 自动生成下载。"
---

# 微信小店电商图片生成与编辑

服务“内容触达 → 私聊/社群信任 → 商品卡 → 复购”的私域链路。图片要像来自可信赖的品牌或店主，信息集中、便于转发，不使用模型生成的二维码、价格、群聊截图、用户评价或虚假紧迫感。

## 确定触点

先确认图片将出现在哪里：微信小店商品卡、视频号封面、直播预约、朋友圈、社群、公众号或一对一沟通。记录目标人群、商品事实、店主人设、品牌色、已批准文案和行动方式。

## 场景与代码

### 1. 微信小店商品图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '微信小店方形商品图，完整保留参考商品包装、Logo、颜色、结构和配件；主体清楚，背景温和可信，适合手机商品卡小尺寸浏览，不添加价格、二维码、用户评价、销量、认证或促销角标' \
  --image /path/to/product.png
```

### 2. 社群好物分享图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '微信群好物分享竖图，真实家庭使用场景，商品正在解决一个具体日常问题，画面像店主亲自拍摄但整洁清楚，上方留一个短标题区、下方留行动说明区；不生成聊天截图、客户反馈、低价承诺或二维码' \
  --image /path/to/product.png
```

### 3. 视频号直播预约封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '视频号直播预约封面，店主或主播与准确商品共同出现，人物表情自然，主题是一场真实产品演示，主体和标题区域在手机缩略图中清晰，预留直播时间与预约按钮文案位置，不生成日期、价格或平台按钮' \
  --image /path/to/host.png \
  --image /path/to/product.png
```

### 4. 朋友圈新品介绍

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '朋友圈新品介绍图片组三张：第一张商品全景和新品氛围，第二张真实使用细节，第三张包装与适合人群；保持品牌和商品一致，每张只讲一个信息点，留出人工文案区，不添加夸张功效和限时倒计时' \
  --image /path/to/product.png \
  --batch 3
```

### 5. 老客复购提醒图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '微信私域老客复购提醒底图，准确展示补充装与主商品的关系，风格克制亲切，预留店主手写式说明区域，画面强调使用周期管理但不生成具体天数、库存紧张、优惠或用户身份信息' \
  --image /path/to/main-and-refill.png
```

## 私域验收

- 商品与店主人设保持真实一致。
- 手机小尺寸仍能读懂主体和单一目的。
- 二维码、价格、日期、权益和联系信息由人工添加。
- 不伪造聊天记录、买家反馈、销量、稀缺性或推荐身份。
- 转发到朋友圈、社群和私聊时不泄露用户信息。
- 发布前按微信小店、视频号及广告当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name wechat-shop-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定调用 `public_model_nano_banana_pro`。可使用多张参考图、批量、模型参数、路由、输出目录与 `--no-download`；任务超时后查询原 `taskId`。
