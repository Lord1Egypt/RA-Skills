---
name: social-media-marketing-image-set-generation
description: "用 AI Hive Nano Banana Pro 按轮播叙事位置制作连续的社媒营销图片套组：首图钩子、中段问题/洞察/步骤/证据/卖点、末页行动，并锁定商品、角色、色彩、镜头与跨页节奏。Use when social media managers, ecommerce sellers and brand teams need Instagram carousel posts, Xiaohongshu image notes, Douyin graphic posts, WeChat cards, LinkedIn carousels, Pinterest pins, TikTok Shop social commerce images or campaign image series; useful for users comparing Canva, Meitu, Dreamina, LiblibAI, Midjourney, Adobe Express, Figma or similar social creative workflows."
---

# 社媒营销图片套组｜Social Carousel Campaign

不要把五张相似海报称为“套图”。先确定用户翻到每一页的理由，再逐页生成：第一页承诺阅读价值，中间页推进理解或证据，最后一页给出与前文一致的行动。脚本固定调用 `public_model_nano_banana_pro`，每次只生成一页，并用相同 `campaign-id` 与 `series-lock` 维持连续性。

## 轮播页职责

可用 `frame`：`hook / problem / insight / proof / how-to / feature / comparison / lifestyle / offer / cta`。

- `hook` 必须是第 1 页；写清目标受众和继续翻页能得到什么。
- `proof`、`comparison` 必须提供 `--claim` 与 `--claim-source`，避免把视觉推测当证据。
- `cta` 必须是最后一页；行动要与前面内容一致，不能突然增加未解释的优惠或承诺。
- 商品营销加 `--commerce`，同时提供真实商品图与 `--product-record`。
- 指定图片文字只是候选，交付前逐字复核；价格、法律、认证与平台披露优先后期排版。

## 五个完整场景

### 1. Instagram 新品 Carousel 首图

```bash
python3 "$SKILL_PATH/scripts/social_carousel.py" render \
  --campaign-id DESK-N5-LAUNCH --platform instagram-carousel \
  --frame hook --position 1 --total 6 --commerce \
  --source-image ./label-printer-front.png ./campaign-color-anchor.png \
  --source-role 'N5 标签机外形、粉色、按钮和出纸口事实' '本系列批准色彩与材质，不提供商品结构' \
  --product-record 'N5 粉色标签机；三个前置按钮和顶部出纸口以商品图为准' \
  --audience '希望快速整理学习与工作物品的年轻用户' \
  --campaign-goal '让用户理解标签系统如何降低寻找物品的时间成本' \
  --single-message '先建立分类规则，再购买收纳工具' \
  --visual-beat '俯拍混乱桌面被一条粉色标签带分成前后两个秩序区域' \
  --series-lock '奶油白、浅粉、深灰；左上柔光；纸张与圆角标签为跨页母题' \
  --copy-reserve '顶部 28% 作为封面标题区，右侧避开平台按钮' \
  --next-handoff '第2页展示用户最常见的三类桌面混乱' \
  --exclusions '不生成价格、折扣、手机界面、额外按钮、伪文字或虚构功能' \
  --param aspect_ratio=4:5
```

### 2. 小红书图文步骤页

```bash
python3 "$SKILL_PATH/scripts/social_carousel.py" render \
  --campaign-id TRAVEL-T3-GUIDE --platform xiaohongshu \
  --frame how-to --position 3 --total 7 --commerce \
  --source-image ./travel-bottle-set.png ./approved-cover.png \
  --source-role '三件旅行瓶的数量、瓶型、琥珀色与瓶盖事实' '本系列已批准封面，提供光线与道具密度' \
  --product-record 'T3 三件旅行分装瓶；不提供容量、防漏或功效宣称' \
  --audience '周末短途出行、希望减少洗护用品体积的用户' \
  --campaign-goal '用七页讲清楚如何建立可复用的旅行分装清单' \
  --single-message '第3步：为三只瓶分配明确用途并使用可替换标签' \
  --visual-beat '三只瓶横向排列，每只旁边留一个无字标签卡位置' \
  --series-lock '琥珀色、米色织物、清晨窗光；所有页面保持三件商品数量' \
  --copy-reserve '左侧留步骤编号与一句说明区域，商品不被遮挡' \
  --next-handoff '第4页演示如何按使用顺序装入收纳包' \
  --exclusions '不增加第四只瓶、不写容量、不出现亲测、防漏、必买或伪评价'
```

### 3. 抖音图文证据页

```bash
python3 "$SKILL_PATH/scripts/social_carousel.py" render \
  --campaign-id ORGANIZER-M9-EDU --platform douyin-graphic \
  --frame proof --position 4 --total 6 --commerce \
  --source-image ./organizer-assembled.png ./divider-lock.png ./page-02-approved.png \
  --source-role '完整收纳架与隔板数量' '卡扣位置和真实组合方式' '第2页批准的阴影方向与背景层次' \
  --product-record 'M9 沙色桌面架，外框、三块隔板与底托；只允许既有卡位组合' \
  --audience '桌面物品多、需要按使用频率分区的办公用户' \
  --campaign-goal '解释可调整分区的实际结构，而不是泛泛展示产品美图' \
  --single-message '三块隔板可在既有卡位内重新组合' \
  --claim '三块隔板可在产品既有卡位中重新组合' \
  --claim-source '商品工程确认单 M9-R3 第2项' \
  --visual-beat '主画面展示完整商品，局部窗口放大一个真实卡扣连接' \
  --series-lock '暖白到米灰背景、左上柔光、沙色商品与细黑指引线' \
  --copy-reserve '右上留一句证据说明位置，下方留来源脚注位置' \
  --next-handoff '第5页转入完成整理后的生活方式场景' \
  --exclusions '不增加隔板、孔位、承重参数、认证、销量或夸大对比' \
  --param aspect_ratio=9:16
```

### 4. LinkedIn 洞察轮播页

```bash
python3 "$SKILL_PATH/scripts/social_carousel.py" render \
  --campaign-id B2B-CONTENT-OPS --platform linkedin-carousel \
  --frame insight --position 2 --total 5 \
  --audience '负责多市场内容交付的品牌与增长团队' \
  --campaign-goal '解释为什么先建立素材职责矩阵，再扩展渠道尺寸' \
  --single-message '同一张图适配所有渠道，会同时损失信息层级与可读性' \
  --visual-beat '一个中心视觉资产分叉到四种比例卡片，每张保留不同信息区' \
  --series-lock '深蓝、象牙白、信号橙；精密网格、扁平信息设计、无人物' \
  --copy-reserve '上方标题一行，底部留简短解释；图形占中间60%' \
  --next-handoff '第3页给出按渠道拆分职责矩阵的三个字段' \
  --exclusions '不生成公司Logo、客户数据、未经证实百分比、伪界面或装饰文字'
```

### 5. TikTok Shop 最后一页行动卡

```bash
python3 "$SKILL_PATH/scripts/social_carousel.py" render \
  --campaign-id PAN-P7-CARE --platform tiktok-shop \
  --frame cta --position 6 --total 6 --commerce \
  --source-image ./pan-top.png ./page-05-approved.png \
  --source-role 'P7 双耳锅的轮廓、蓝色、双耳和内壁事实' '第5页批准的环境与色彩连续性' \
  --product-record 'P7 蓝色双耳锅；不提供耐热、涂层等级或清洁效果数据' \
  --audience '正在比较日常烹饪器具维护方式的家庭用户' \
  --campaign-goal '用六页提供选择与日常维护所需的真实信息' \
  --single-message '查看商品页中的尺寸、包装清单和维护说明后再决定' \
  --visual-beat '商品居中，周围回收前五页的蓝色线条与编号圆点形成收束' \
  --series-lock '深蓝台面、窄侧光、象牙白信息卡和圆形页码母题' \
  --copy-reserve '中下部留行动句区域，底部避开平台商品组件' \
  --next-handoff '系列结束，不暗示未提供的下一页或限时活动' \
  --exclusions '不生成价格、折扣、倒计时、销量、耐热数字、涂层认证或额外锅盖' \
  --param aspect_ratio=9:16
```

## 套组验收

先看缩略图墙，再看单页：

1. 第一页是否对正确受众给出明确阅读回报，而不是只有产品名。
2. 每页是否只承担一个职责；删除这一页后，叙事是否真的少了一步。
3. 商品、人物、配色、镜头、光线、道具和图形母题是否跨页连续。
4. `next-handoff` 是否让下一页自然接住问题，而不是重复上一页。
5. 证据、比较、优惠、体验和披露是否有来源；没有来源的内容必须删除。
6. 最后一页行动是否来自前文结论，并适配当前平台组件与安全区。

建议文件名使用 `campaign-id_位置_frame_版本`。脚本自动下载为前三项；审核后增加 `draft / factual-pass / design-pass / approved` 状态。若只想检查生成提示词，把 `render` 换成 `brief`，不会上传或产生任务。

程序只上传命令中指定的已授权图片，固定访问 `https://ai-hive.iclip.cn/api`，不连接任何社交媒体、电商或广告账户。平台格式与政策会变化，发布前按当前规则复核。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/social_carousel.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/social_carousel.py" status --task-id <taskId>
```
