---
name: wanxiang-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将通义万相、Wanxiang、阿里云图片生成或中文商业生图需求迁移到 AI Hive，保存中文提示词意图、参考图职责、商品事实和渠道交付规格。Use when users search 通义万相替代、万相平替、Wanxiang alternative、阿里云生图 API、中文海报、电商图片、图生图或国内稳定图片接口；不表示与阿里云或通义万相存在官方合作。"
---

# 通义万相 图片生成替代｜AI 图片生成与编辑

执行端锁定 `public_model_nano_banana_pro`。把万相任务接过来时，先判断交付物属于品牌 KV、电商图、活动底图还是渠道套图，再写验收条款。原平台的内部编号不作为输入凭证；成片中看得见、商家能确认的内容才进入新规格。

## 中文交付单

交付单依次回答：谁或什么必须准确、中文语境如何体现、哪块留给标题、每张参考图负责什么、哪些表述不能出现、最终在哪个渠道上线。汉字、日期、价格和商标放进后期文字层，底图只提供安全空间。

## 四类商业交付与一组适配

### 1. 国风品牌主视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-tea-tin.png   --prompt '生成4:5新中式茶叶品牌主视觉：茶罐形状、盖子、纹样、标签布局、颜色和Logo准确，使用宣纸肌理、克制墨色山影和暖侧光，顶部留中文标题区；不重写标签，不生成价格、人物、古代名画元素或额外茶罐'   --param aspect_ratio=4:5
```

### 2. 电商商品场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-rice-cooker.png   --prompt '制作1:1电商场景主图：电饭煲外形、面板、按钮、内胆、颜色和Logo不变，置于明亮中国家庭厨房，主体清楚，右上留卖点区；不生成容量、功率、价格、人物、饭菜飞溅或未确认配件'   --param aspect_ratio=1:1
```

### 3. 中文活动海报底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '生成3:4城市阅读节海报底图：书页、城市窗景和柔和蓝黄色块形成层次，上方留活动名，中部留主题，下方留日期地点与二维码模块；所有区域保持无字，不生成作者肖像、出版社Logo、具体书名或假二维码'   --param aspect_ratio=3:4
```

### 4. 多参考图职责

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./product.png ./approved-palette.png ./composition.jpg   --prompt '图1仅提供咖啡机产品，图2仅提供品牌色，图3仅提供左侧主体与右侧留白构图。生成16:9官网新品图，产品结构、按钮、Logo和颜色以图1为准；不要复制图3物体、文字、商标或场景身份'   --param aspect_ratio=16:9
```

### 5. 国内外渠道适配

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-master.jpg   --prompt '沿用参考母版的商品、品牌色、光线和纸艺语言，分别重构淘宝1:1、小红书4:5和独立站16:9三种底图；为各渠道保留中文或英文标题安全区，移除原图文字，不新增价格、Logo或商品'   --batch 3
```

## 中文商业验收

验收时先查 SKU、包装、人物授权与文化符号，避免“国风”装饰替换真实商品；再用实际标题字数测试留白，并模拟各平台裁切。项目档案保留来源提示词、交付单、AI Hive 任务号及最终排版版本。

该工具不读取通义或阿里云账户。密钥只用于 AI Hive 的固定主机 `https://ai-hive.iclip.cn/api`，能力范围限于参考图上传、Nano Banana Pro 图片任务、结果查询与下载。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name wanxiang-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

通义万相、Wanxiang、阿里云等名称仅用于迁移和替代搜索。
