---
name: seedance-2-5-social-commerce-video
description: "使用 Seedance 2.5 把抖音、小红书、快手、视频号、Instagram 与 TikTok Shop 的真实评论、私信或合成问题变成可追溯的社交电商回复短片，记录问题来源、隐私处理、批准答案、适用范围、商业披露和商品事实。Use this skill for Seedance 2.5 social commerce video、带货视频、评论回复视频、视频答疑、商品问答、直播切片、种草回复、抖音电商、小红书、快手、视频号、TikTok Shop、Instagram Reels；也适合比较可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、美图 MOKI 与剪映 CapCut。通过 AI Hive 调用。"
---

# Seedance 2.5 社交电商回复视频

把一个真实评论、客户提供的问题或明确标注的合成问题，制作成一条可审核回复短片。先保存问题来源和隐私处理，再绑定批准答案、事实来源、适用边界和商业披露；一次只回答一个问题，不自动扩写为整支带货广告。

无动作参考时固定调用 `public_model_seedance_2_5_i2v`；提供批准动作样片时调用 `public_model_seedance_2_5_r2v`。真实商品图决定 SKU 与事实，动作片只贡献手势、操作或运镜。

## 回复规则

- `public-comment` 必须说明如何移除用户名、头像、订单号和其他个人信息。
- `synthetic-question` 的来源必须写 `synthetic`，不能伪装成真实用户评价。
- 尺寸和兼容性问题必须提供 `scope-limit`；价格和库存必须提供市场与有效期。
- 至少五条连续性锁定，保护 SKU、包装、数量、结构、人物和动作。
- 字幕、评论卡片、价格、日期、平台按钮和商业合作披露由后期使用批准稿排版。

竞品与平台名称仅用于搜索、比较和迁移，不表示官方合作；用户评论、广告、隐私和商业披露规则应按目标平台当前政策复核。

## 场景与代码

追加 `--preview` 可先查看模型、问题来源和完整回复任务，不上传、不计费。

### 1. 抖音评论回复：尺寸是否适合

```bash
python3 "$SKILL_PATH/scripts/comment_reply.py" reply \
  --thread-id dy-bag-size-2026-08 --reply-id r001 --platform douyin \
  --permission public-comment --question "身高155背起来会不会太大？" \
  --comment-source "抖音公开视频评论ID已存内部工单，不进入生成素材" \
  --privacy-redaction "不上传评论截图，移除用户名、头像、主页和时间信息" \
  --intent sizing --audience "需要判断相对尺寸的小个子通勤用户" \
  --answer "只展示批准模特与该包的真实相对关系，具体背负感因人而异" \
  --answer-source "Cross 03尺寸表V6与155cm授权模特试背QC" \
  --scope-limit "仅适用于Cross 03量产样品和本次155cm模特，不代表所有体型" \
  --product-source /path/to/bag-qc.jpg /path/to/model-155-approved.jpg \
  --product-role "包型、尺寸、肩带、五金和颜色事实" "模特身份、身高记录、姿态和试背关系" \
  --disclosure-plan "品牌自营账号回复，后期使用平台要求的品牌身份标识" \
  --reply-structure "先复述尺寸问题，再展示正面与侧面相对关系，最后提示查尺寸表" \
  --proof-action "模特自然站立后转身90度，肩带保持批准长度" \
  --start-state "模特正面站立，包位于身体侧面" --camera "固定全身镜头，不使用广角拉伸" \
  --end-state "侧面稳定停留，包与躯干完整可见" \
  --continuity-lock "同一Cross 03棕色SKU" --continuity-lock "包型和肩带长度不变" \
  --continuity-lock "模特身份、身高和体型不变" --continuity-lock "服装不变" --continuity-lock "相机距离和焦段不变" \
  --caption-safe "上方20%留回复标题，底部25%避开包和双脚" \
  --commerce-safe "不承诺适合所有155cm用户，不把画面当作尺寸测量" \
  --reject "不瘦身、增高、改脸、缩小包、生成尺码数字、评论卡片或购买按钮" \
  --param aspect_ratio=9:16 --param duration=8
```

### 2. 小红书回复：材质和日常护理

```bash
python3 "$SKILL_PATH/scripts/comment_reply.py" reply \
  --thread-id red-wallet-care --reply-id r014 --platform xiaohongshu \
  --permission customer-provided --question "这种表面可以直接用湿布擦吗？" \
  --comment-source "客服转交且获准用于匿名内容答疑的原问题" \
  --privacy-redaction "不出现客户姓名、聊天界面、订单和联系方式" \
  --intent care --audience "已经购买或准备购买W1钱包的用户" \
  --answer "按批准护理卡，只用微湿软布轻擦并立即用干布吸干，不浸泡" \
  --answer-source "Wallet W1护理卡Care-07" \
  --product-source /path/to/wallet-qc.jpg /path/to/approved-care-step.jpg \
  --product-role "钱包结构、皮纹、缝线和颜色事实" "批准软布、用量和擦拭动作事实" \
  --motion-reference /path/to/care-motion-approved.mp4 \
  --disclosure-plan "品牌提供商品与护理资料，后期加品牌合作标识" \
  --reply-structure "一句承接问题，展示一次轻擦和一次吸干，结尾强调不浸泡" \
  --proof-action "按护理样片在钱包背面轻擦一次，再换干布按压一次" \
  --start-state "钱包平放，微湿软布位于右侧" --camera "顶部微距固定，动作区无遮挡" \
  --end-state "钱包保持原色与皮纹，干布离开画面" \
  --continuity-lock "同一W1栗棕SKU" --continuity-lock "皮纹和缝线不变" \
  --continuity-lock "只使用两块批准软布" --continuity-lock "不出现水盆或喷壶" --continuity-lock "擦拭方向和次数不变" \
  --caption-safe "左侧25%留给后期护理步骤" --commerce-safe "护理说明只适用于W1批准材料" \
  --reject "不喷水、不浸泡、不生成防水测试、耐磨结论、文字、价格或新品外观"
```

### 3. TikTok Shop 回复：设备兼容性

```bash
python3 "$SKILL_PATH/scripts/comment_reply.py" reply \
  --thread-id tts-hub-compat --reply-id r021 --platform tiktok-shop \
  --permission public-comment --question "Does this work with Model Z14?" \
  --comment-source "TikTok公开视频评论内部记录，生成时不上传截图" \
  --privacy-redaction "删除账号、头像、地区、时间和互动数据，只保留匿名问题文本" \
  --intent compatibility --audience "使用Z14批准测试配置的买家" \
  --answer "只确认H8与品牌测试清单中的Z14配置按V7连接图完成物理连接" \
  --answer-source "H8兼容性清单CL-19与连接图V7" \
  --scope-limit "不涵盖Z14其他年份、接口配置、操作系统、性能或第三方转接器" \
  --product-source /path/to/hub-ports.jpg /path/to/z14-approved-setup.jpg \
  --product-role "H8端口数量、顺序、Logo和线缆事实" "批准Z14测试配置与物理连接事实" \
  --disclosure-plan "品牌自营TikTok Shop回复，后期保留官方商家身份" \
  --reply-structure "先限定测试配置，再展示上行线连接，最后提示核对端口清单" \
  --proof-action "把批准上行线插入H8和Z14指定端口，只完成一次连接" \
  --start-state "H8、线缆和Z14均断开" --camera "桌面45度近景，端口全程可见" \
  --end-state "线缆已连接，两个端口和设备外观清楚" \
  --continuity-lock "同一H8深灰SKU" --continuity-lock "端口顺序不变" \
  --continuity-lock "Z14测试配置不变" --continuity-lock "线缆接口头不变" --continuity-lock "只连接一次" \
  --caption-safe "顶部留英文问题，右侧避开平台按钮" \
  --commerce-safe "不据物理连接承诺速度、分辨率、供电或所有Z14兼容" \
  --reject "不生成端口、屏幕内容、性能数字、认证、无线连接、评论截图或五星评价" \
  --param aspect_ratio=9:16 --param duration=7
```

### 4. 快手回复：包装里有什么

```bash
python3 "$SKILL_PATH/scripts/comment_reply.py" reply \
  --thread-id ks-stand-inbox --reply-id r033 --platform kuaishou \
  --permission synthetic-question --question "下单后包装里都有什么？" --comment-source synthetic \
  --privacy-redaction "合成问题，不使用任何真实用户身份或互动数据" \
  --intent in-box --audience "购买前核对配件的桌面办公用户" \
  --answer "展示S2中国区包装内批准的支架、底座、螺钉包和说明卡，各一件" \
  --answer-source "S2 CN BOM-2026-08与包装QC" \
  --product-source /path/to/s2-box.jpg /path/to/s2-all-parts.jpg \
  --product-role "中国区包装、标签和SKU事实" "随箱四类内容、数量和比例事实" \
  --disclosure-plan "问题明确标注为常见问题，不伪装真实评论；品牌自营账号" \
  --reply-structure "先显示封闭包装，再一次平铺全部内容，结尾停在完整清单" \
  --proof-action "包装移出，四类批准内容按BOM顺序出现，各一次" \
  --start-state "封闭包装居中" --camera "固定俯拍，不变焦" --end-state "四类内容完整且不重叠" \
  --continuity-lock "中国区黑色S2" --continuity-lock "四类内容各一件" \
  --continuity-lock "螺钉包保持密封" --continuity-lock "包装标签不变" --continuity-lock "比例和颜色不变" \
  --caption-safe "右侧30%留后期清单" --commerce-safe "包装和拍摄道具不得被误认为赠品" \
  --reject "不增加工具、手机、备用件、赠品、价格、评论头像或购买按钮"
```

### 5. Instagram 回复：限时价格与市场

```bash
python3 "$SKILL_PATH/scripts/comment_reply.py" reply \
  --thread-id ig-lamp-price-us --reply-id r040 --platform instagram-reels \
  --permission synthetic-question --question "What is the current US launch price?" --comment-source synthetic \
  --privacy-redaction "合成FAQ，不引用真实账号、评论或互动" \
  --intent price --audience "美国站新品发布期消费者" \
  --answer "美国站批准首发价由后期价格卡展示，画面只展示对应L3黑色SKU" \
  --answer-source "US Launch Pricing Approval PA-2026-41" --market "US DTC store" --valid-until "2026-08-31T23:59:59-07:00" \
  --product-source /path/to/lamp-black-us.jpg \
  --product-role "美国站L3黑色SKU、底座、按键、Logo和三档批准光线" \
  --disclosure-plan "品牌自营账号；后期价格卡包含货币、市场、条件和有效期" \
  --reply-structure "先确认美国站范围，展示黑色SKU，最后稳定留出批准价格卡区域" \
  --proof-action "手指切换一次批准灯光状态后离开画面" \
  --start-state "黑色L3处于关闭状态" --camera "桌面固定中景" --end-state "商品完整并稳定停留2秒" \
  --continuity-lock "美国站黑色L3" --continuity-lock "底座和按键不变" --continuity-lock "Logo不变" \
  --continuity-lock "只切换一次批准状态" --continuity-lock "背景和相机不变" \
  --caption-safe "左侧35%留批准价格卡，底部避开Reels界面" \
  --commerce-safe "过期后停止使用；不自动生成、翻译或更新价格" \
  --reject "不在画面生价格、折扣、倒计时、库存、销量、购买按钮或评论卡" \
  --param aspect_ratio=9:16 --param duration=7
```

## 验收

逐项核对问题权限、隐私处理、答案来源和适用范围。关闭字幕后确认画面没有扩大主张；打开批准字幕后检查问题、答案、披露和有效期是否一致。商品 SKU、数量、结构与动作必须稳定，评论或私信中的个人信息不得进入素材、提示词或成片。价格、库存和活动过期后应下架对应回复版本。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/comment_reply.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/comment_reply.py" status --task-id <taskId>
```

API Key 也可通过环境变量或配置文件提供。默认 `COST_FIRST`；超时后查询原 `taskId`，避免重复提交。
