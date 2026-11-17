---
name: seedance-2-5-product-video
description: "用 Seedance 2.5 把真实商品图和产品主档变成可剪辑的产品宣传片镜头包，覆盖 Hero、材质微距、机构演示、人与产品互动、尺度证明和品牌结尾。Use this skill for Seedance 2.5 product video、产品宣传视频、商品展示视频、品牌宣传片、TVC、Product Film、Hero Shot、材质特写、产品演示、Amazon Product Video、淘宝天猫详情页、抖音小红书、TikTok Shop、Shopify；也适合比较可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、美图 MOKI 与剪映 CapCut。通过 AI Hive 调用。"
---

# Seedance 2.5 产品宣传视频

先锁定产品事实和全片视觉系统，再分别生成 Hero、微距、机构、使用、尺度与结尾镜头。无动作参考时固定调用 `public_model_seedance_2_5_i2v`；提供 `--motion-reference` 时调用 `public_model_seedance_2_5_r2v`，只借动作与运镜。真实产品图始终优先于风格参考。

## 适用场景

- 新品发布、官网 Hero、发布会、门店屏幕、TVC、产品功能片与详情页。
- 淘宝、天猫、京东、抖音、小红书、Amazon、TikTok Shop、Shopify、Reels 与 Shorts 商品视频。

竞品与平台名称仅用于搜索、比较和迁移，不代表官方合作；发布前复核渠道规则。

## 先建立产品影片圣经

同一支片复用 `film-id`、产品主档、影片命题、场景、色板、灯光与镜头；用 `shot-id` 对应分镜。至少四条 `continuity-lock` 锁定外观、结构、Logo、数量或人物；明确相机起点、运动、终点和剪辑余量。

`mechanism / interaction / scale` 三类镜头必须提供 `--demonstrated-fact` 与 `--fact-source`。模型生成的画面不是产品证据；没有批准来源，就不应演示该事实。

## 场景与代码

每条命令都可追加 `--preview`，先查看模型、素材职责和完整提示词，不上传、不计费。

### 1. 手机新品 Hero 镜头

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id aurora-phone-launch --shot-id s010-hero --shot-role hero \
  --delivery "官网与发布会16:9，8秒" --audience "关注工业设计的旗舰手机用户" \
  --film-thesis "用一整块克制的金属与玻璃表达可靠精密" \
  --product-record "Aurora X，深海蓝SKU，批准量产外观V12，三摄数量与接口不得变化" \
  --product-source /path/to/front.png /path/to/back.png /path/to/side.png \
  --product-role "正面屏幕与边框事实" "背板、三摄和Logo事实" "厚度、按键与接口事实" \
  --set-design "无缝深蓝摄影棚，只有低矮黑色展示台" \
  --palette "深海蓝、石墨黑、极少冷白高光" \
  --lighting "左后方窄轮廓光扫过金属边框，正面柔光保持屏幕黑" \
  --lens "85mm产品镜头，中浅景深，几何透视克制" \
  --camera-start "背面三摄45度近景" --camera-move "缓慢绕行90度并轻微下降" \
  --camera-end "完整正面居中，屏幕保持纯黑" --subject-action "手机固定，只由展示台缓慢转动" \
  --continuity-lock "深海蓝颜色不变" --continuity-lock "三颗镜头数量与位置不变" \
  --continuity-lock "Logo形状和方向不变" --continuity-lock "按键、开孔和接口不变" \
  --edit-handles "开头和结尾各稳定停留12帧" --copy-safe "右侧25%保留后期标题安全区" \
  --reject "不点亮屏幕，不生成系统界面、悬浮零件、光束、参数或文案" \
  --param aspect_ratio=16:9 --param duration=8
```

### 2. 香水材质微距

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id amber-eau-film --shot-id s020-material --shot-role material \
  --delivery "TVC与小红书裁切母版4:5，6秒" --audience "重视瓶器与香氛审美的消费者" \
  --film-thesis "让琥珀玻璃与真实液体颜色成为主角" \
  --product-record "Amber No.7 50ml量产瓶，批准瓶盖、标签、液位和琥珀色" \
  --product-source /path/to/bottle-front.jpg /path/to/glass-macro.jpg \
  --product-role "瓶型、标签、瓶盖和液位事实" "批准玻璃纹理与液体颜色事实" \
  --set-design "暖灰石材台面与无缝背景，不放花材" \
  --palette "琥珀、暖灰、少量金色反射" --lighting "大面积侧逆光穿过瓶肩，标签保持可辨" \
  --lens "100mm微距，焦点从瓶肩玻璃移动到标签压纹" \
  --camera-start "瓶肩玻璃占满画面" --camera-move "极慢横移并完成一次焦点转移" \
  --camera-end "标签压纹清楚的四分之三构图" --subject-action "产品和液面完全静止" \
  --continuity-lock "瓶型不变" --continuity-lock "液位与颜色不变" \
  --continuity-lock "标签文字与压纹不变" --continuity-lock "瓶盖材质与比例不变" \
  --edit-handles "起止各稳定停留10帧，焦点转移只发生一次" \
  --copy-safe "画面内不生成文字，顶部15%可供后期排版" \
  --reject "不增加水珠、花瓣、烟雾、液体飞溅、宝石或未提供装饰"
```

### 3. 咖啡磨豆机机构演示

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id grinder-g2-demo --shot-id s030-mechanism --shot-role mechanism \
  --delivery "天猫详情页16:9，8秒" --audience "需要看懂清洁步骤的家庭咖啡用户" \
  --film-thesis "精确结构让日常清洁更直观" \
  --product-record "Grinder G2黑色SKU，批准上盖、豆仓、刀盘和锁止标记" \
  --product-source /path/to/grinder.jpg /path/to/burr-removal.jpg \
  --product-role "整机外观与控制区事实" "刀盘拆卸方向与部件数量事实" \
  --set-design "干净厨房操作台，背景无其他电器" --palette "黑、银、浅橡木" \
  --lighting "顶部柔光配右侧轮廓光，结构凹槽可见" --lens "50mm标准镜头，中等景深" \
  --camera-start "完整机器正面中景" --camera-move "机器不动，相机轻推到豆仓顶部" \
  --camera-end "上盖与可拆刀盘整齐放在机器右侧" \
  --subject-action "一只手按说明书方向旋开上盖并取出刀盘，只完成一次拆卸" \
  --demonstrated-fact "展示批准的上盖旋转方向和可拆刀盘清洁步骤" \
  --fact-source "Grinder G2量产说明书2026-07版第8页" \
  --continuity-lock "始终为黑色G2" --continuity-lock "刀盘结构与齿形不变" \
  --continuity-lock "部件数量不变" --continuity-lock "控制旋钮与标记不变" \
  --edit-handles "拆卸前后各稳定停留0.6秒" --copy-safe "左侧25%留给后期步骤编号" \
  --reject "不展示内部电机，不增加工具、咖啡豆、清洁刷、箭头或步骤文字" \
  --param aspect_ratio=16:9 --param duration=8
```

### 4. 耳机真实佩戴互动

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id buds-air-story --shot-id s040-interaction --shot-role interaction \
  --delivery "抖音与TikTok Shop 9:16，6秒" --audience "每天通勤的年轻用户" \
  --film-thesis "小巧产品自然进入通勤动作，而不是夸张表演" \
  --product-record "Buds Air薄荷绿SKU，一对耳机与一个充电盒，批准佩戴方向" \
  --product-source /path/to/buds-case.png /path/to/approved-fit.jpg \
  --product-role "耳机、充电盒、颜色、Logo与数量事实" "批准佩戴方向和耳部相对尺度" \
  --set-design "早晨地铁站入口，背景人流柔化" --palette "薄荷绿、混凝土灰、自然肤色" \
  --lighting "自然晨光，耳机边缘清楚，不做霓虹光效" --lens "65mm人像近景，背景柔化" \
  --camera-start "手持打开的充电盒近景" --camera-move "跟随右手将一只耳机放入右耳" \
  --camera-end "人物侧脸与右耳机稳定同框" --subject-action "取出一只右耳机并按批准方向佩戴" \
  --demonstrated-fact "一只耳机从充电盒取出并按批准方向佩戴" \
  --fact-source "Buds Air佩戴指南V5与批准模特适配照" \
  --continuity-lock "薄荷绿色不变" --continuity-lock "盒内始终只有一对耳机" \
  --continuity-lock "左右耳方向不交换" --continuity-lock "模特身份、耳型和服装不变" \
  --edit-handles "打开盒子前与佩戴完成后各稳定停留12帧" \
  --copy-safe "底部25%避开脸和产品，预留平台界面" \
  --reject "不生成手机界面、降噪波纹、音乐符号、额外耳机或听力功效"
```

### 5. 登机箱尺度证明

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id cabin-case-film --shot-id s050-scale --shot-role scale \
  --delivery "Amazon Product Video 16:9，7秒" --audience "担心箱体相对尺寸的跨境买家" \
  --film-thesis "用批准测试物建立尺度，不在画面中伪造数字" \
  --product-record "Cabin 20银色SKU，批准轮组、拉杆、把手和测试架" \
  --product-source /path/to/case-front.jpg /path/to/approved-sizer.jpg \
  --product-role "箱体、轮组、拉杆与颜色事实" "品牌批准测试架和相对尺度事实" \
  --set-design "简洁机场测试区，无航空公司标识" --palette "银、深蓝、白" \
  --lighting "均匀商业空间顶光，箱体边缘不与背景粘连" --lens "45mm标准视角，透视自然" \
  --camera-start "箱体与测试架完整并列" --camera-move "轻微侧向跟随箱体推入测试架" \
  --camera-end "箱体位于测试架内，四轮和顶部余量可见" --subject-action "工作人员一次将箱体平稳推入批准测试架" \
  --demonstrated-fact "展示该批准样品与品牌测试架的实际相对关系" \
  --fact-source "Cabin 20样品QC-2026-31与测试架校准记录" \
  --continuity-lock "银色SKU不变" --continuity-lock "箱体、轮组和把手比例不变" \
  --continuity-lock "测试架结构不变" --continuity-lock "工作人员服装与动作方向不变" \
  --edit-handles "推入前后各稳定停留0.5秒" --copy-safe "右上角留给后期批准尺寸" \
  --reject "不生成尺寸、登机承诺、航空公司Logo、认证章、容量结论或竞品"
```

### 6. 借参考运镜完成品牌结尾

```bash
python3 "$SKILL_PATH/scripts/product_film.py" shot \
  --film-id orbit-watch-film --shot-id s060-end --shot-role end-frame \
  --delivery "发布会与官网16:9，6秒" --audience "关注机械细节的腕表消费者" \
  --film-thesis "让表壳轮廓与表盘秩序成为品牌记忆" \
  --product-record "Orbit S黑盘钢带SKU，批准指针位置、刻度、表冠与链节" \
  --product-source /path/to/watch-front.png /path/to/watch-crown.png \
  --product-role "表盘、指针、刻度和钢带事实" "表冠、表壳侧面和链节事实" \
  --motion-reference /path/to/approved-orbit-camera.mp4 \
  --set-design "黑色镜面台面与深灰无缝背景" --palette "黑、钢银、冷白" \
  --lighting "窄条高光沿表壳移动，表盘保持可读" --lens "90mm产品镜头，浅景深" \
  --camera-start "表冠侧面极近景" --camera-move "只借参考片的半圆绕行节奏，速度平稳减缓" \
  --camera-end "腕表正面完整居中" --subject-action "腕表固定，指针和表带不运动" \
  --continuity-lock "黑色表盘不变" --continuity-lock "指针位置和刻度不变" \
  --continuity-lock "表冠与链节结构不变" --continuity-lock "反射中不出现其他物体" \
  --edit-handles "结尾完整正面稳定停留1秒，开头稳定停留8帧" \
  --copy-safe "下方20%留给后期品牌字标，画面内不生成字" \
  --reject "不借参考片的产品外观、场景或Logo，不生成齿轮、拆解、参数或日期" \
  --param aspect_ratio=16:9 --param duration=6
```

## 镜头包验收

1. 产品真实性：逐帧核对 SKU、颜色、材质、比例、结构、配件、包装、Logo 与可见文字。
2. 单镜头职责：Hero 负责记忆，Material 负责质感，Mechanism 负责批准动作；不要一个镜头承担三件事。
3. 视觉连续性：比较所有镜头的场景、色板、主光方向、镜头语言和反射环境。
4. 动作真实性：涉及拆装、佩戴、尺度或使用时，只表现批准步骤，不让画面替代说明书和测试证据。
5. 剪辑可用性：首尾稳定、运动方向可衔接、无突跳，安全区不遮挡产品。
6. 发布合规：参数、价格、功效、认证和活动文案由批准稿后期排版；模型不要代写。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/product_film.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/product_film.py" status --task-id <taskId>
```

API Key 也可通过 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json` 提供。默认路由是 `COST_FIRST`，同时支持 `SPEED_FIRST`、`SUCCESS_FIRST`、多个 `--param key=value`、`--no-download` 和自定义输出目录。超时后查询原 `taskId`，不要直接重复提交。
