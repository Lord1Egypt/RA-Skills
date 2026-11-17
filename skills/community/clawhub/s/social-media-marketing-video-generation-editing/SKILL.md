---
name: social-media-marketing-video-generation-editing
description: "把一支批准的营销母版变成可追溯的多平台社媒视频版本矩阵：重构渠道版、生成平台原生Hook、延长循环或CTA/免责声明停留。Use this skill for 社媒营销视频生成与编辑、Social Media Video、抖音、小红书、视频号、快手、B站、Instagram Reels、TikTok、YouTube Shorts、Facebook、LinkedIn、Pinterest、多尺寸改版、横转竖、Cutdown、Hook、Loop、CTA；也适合比较可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、剪映 CapCut、美图 MOKI。通过 AI Hive 调用 Seedance 2.5。"
---

# 社媒营销视频生成与编辑

从一支批准母版派生渠道版本，而不是把同一个横屏视频机械裁成九宫格。每个版本记录 Campaign、渠道、目标、受众、唯一信息、必须保留内容和允许删减内容；这样抖音、小红书、视频号、Reels、TikTok 与 Shorts 可以共享品牌事实，又保持各自的开场节奏、构图和界面安全区。

## 三个入口

| 命令 | 任务 | 固定模型 |
|---|---|---|
| `adapt` | 重构批准母版的取景、节奏和镜头顺序 | `public_model_seedance_2_5_video_edit` |
| `hook` | 用批准关键帧和母版动作生成平台原生开场 | `public_model_seedance_2_5_r2v` |
| `tail` | 向后延长，用于循环、CTA停留或免责声明停留 | `public_model_seedance_2_5_video_extend` |

`adapt` 允许重新取景，但不把横屏简单中心裁切；`hook` 只替换开场，不重新发明整条片；`tail` 只延长最后一帧之后的内容，不改写原视频。字幕、价格、日期、法律声明和平台按钮始终使用批准稿后期排版。

竞品和平台名称仅用于搜索、比较与迁移，不代表 AI Hive 与其存在官方合作。发布规格、广告政策与安全区可能变化，批量生产前应按平台当前规则复核。

## 场景与代码

所有命令都支持 `--preview`：先输出模型、素材和完整任务，不上传、不计费。

### 1. 抖音 9:16 投放版

```bash
python3 "$SKILL_PATH/scripts/social_matrix.py" adapt \
  --campaign-id summer-sparkling --variant-id dy-conversion-a \
  --source-video /path/to/approved-master-16x9.mp4 \
  --platform douyin --objective conversion --audience "喜欢无糖气泡饮的都市上班族" \
  --one-message "开罐后立即感知清爽气泡，配方主张以批准包装为准" \
  --campaign-source "Campaign Brief SB-2026-08与量产包装QC" \
  --brand-source /path/to/can-front.png /path/to/can-side.png \
  --brand-role "罐身正面、Logo与口味色事实" "侧面配料区与罐体比例事实" \
  --format "9:16竖屏，15秒" --target-duration "15秒" --hook-deadline 1.5 \
  --must-keep "开罐动作与真实气泡近景" --must-keep "批准Hero罐身结尾" \
  --may-trim "横屏母版的环境建立和重复喝饮料镜头" \
  --invariant "同一青柠SKU" --invariant "Logo和包装文字不变" \
  --invariant "罐体比例不变" --invariant "人物身份和服装不变" \
  --edit-logic "第一秒用开罐动作建立声音与运动，随后交替人物反应和产品特写" \
  --caption-plan "底部字幕每屏一句，使用后期批准文案" \
  --cta-plan "最后1秒保留完整产品帧，后期叠加平台CTA" \
  --safe-zone "顶部15%和底部25%不放脸、Logo或开罐动作" \
  --reject "不生成价格、销量、购买按钮、功效、额外口味或夸张液体飞溅" \
  --param aspect_ratio=9:16 --param duration=15
```

### 2. 小红书 4:5 种草版

```bash
python3 "$SKILL_PATH/scripts/social_matrix.py" adapt \
  --campaign-id desk-reset --variant-id red-engagement-b \
  --source-video /path/to/desk-lamp-master.mp4 \
  --platform xiaohongshu --objective engagement --audience "租房桌面改造用户" \
  --one-message "一次触控切换批准的三档光线状态" \
  --campaign-source "Lamp L3说明书V6与品牌批准三档色温样片" \
  --brand-source /path/to/lamp.png /path/to/three-modes.jpg \
  --brand-role "灯体、底座、按键与Logo事实" "三档批准光线外观事实" \
  --format "4:5信息流，12秒" --target-duration "12秒" --hook-deadline 2 \
  --must-keep "手指一次触控动作" --must-keep "三档光线状态的真实顺序" \
  --may-trim "母版中重复的空间全景和包装镜头" \
  --invariant "黑色L3 SKU" --invariant "灯臂和底座比例不变" \
  --invariant "只出现三档批准状态" --invariant "人物、桌面和道具连续" \
  --edit-logic "先展示改造前桌面，再用一次触控串联三档状态，结尾回到完整桌面" \
  --caption-plan "顶部短标题与左侧步骤编号后期排版，画面不自动生字" \
  --cta-plan "结尾只保留收藏式提示空间，不生成购买按钮" \
  --safe-zone "右侧20%与底部20%避开产品和手" \
  --reject "不增加色温、智能App、语音控制、价格、评分或房间面积结论" \
  --param aspect_ratio=4:5 --param duration=12
```

### 3. Instagram Reels 原生 Hook

```bash
python3 "$SKILL_PATH/scripts/social_matrix.py" hook \
  --campaign-id trail-shoe-launch --variant-id reels-hook-01 \
  --master-video /path/to/approved-shoe-master.mp4 \
  --key-frame /path/to/approved-sole-keyframe.jpg \
  --brand-source /path/to/shoe-side.jpg /path/to/outsole.jpg \
  --brand-role "鞋面、配色和Logo事实" "鞋底纹路、分区和颜色事实" \
  --platform instagram-reels --audience "周末轻量徒步用户" --hook-seconds 2.5 \
  --hook-job "第一眼建立鞋底与湿石路面的真实接触，不承诺防滑等级" \
  --first-second "鞋底从画外进入，在批准测试石面完成一次落脚" \
  --proof-source "Trail R2批准产品QC与品牌测试场景样片TR-18" \
  --inherit "同一模特和服装" --inherit "同一Trail R2灰蓝SKU" \
  --inherit "母版阴天山径光线" --inherit "母版从左向右运动方向" \
  --action "只完成一次落脚和重心前移" \
  --camera "低机位短距离跟随，结尾回到母版首个侧面跑动构图" \
  --handoff "第2.5秒人物左脚离地，运动方向与母版第一镜一致" \
  --safe-zone "底部25%与右侧15%避开鞋底和脚踝" \
  --reject "不生成防滑数值、泥水爆炸、速度线、山峰字幕、额外鞋款或Logo" \
  --param aspect_ratio=9:16 --param duration=3
```

### 4. TikTok 无缝循环尾段

```bash
python3 "$SKILL_PATH/scripts/social_matrix.py" tail \
  --campaign-id ceramic-mug-loop --variant-id tiktok-loop-01 \
  --source-video /path/to/approved-pour-cut.mp4 \
  --platform tiktok --tail-job loop --extend-seconds 2 \
  --last-frame-state "咖啡流刚停止，杯子位于画面中央，手持壶在右上方" \
  --next-frame-match "接近首帧空杯中央、壶嘴从右上方刚进入的构图与亮度" \
  --preserve "同一白色杯子与釉面" --preserve "咖啡颜色和液位连续" \
  --preserve "手、壶和桌面位置连续" --preserve "相机固定且晨光方向不变" \
  --safe-zone "循环段不移动商品到右侧平台图标区" \
  --reject "不让液体倒流，不增加蒸汽、文字、Logo、第二只杯子或镜头切换" \
  --param duration=2
```

### 5. 视频号免责声明停留

```bash
python3 "$SKILL_PATH/scripts/social_matrix.py" tail \
  --campaign-id finance-webinar --variant-id channels-disclaimer-01 \
  --source-video /path/to/approved-webinar-end.mp4 \
  --platform wechat-channels --tail-job disclaimer-hold --extend-seconds 4 \
  --last-frame-state "讲者已停止讲话，品牌背景墙稳定，左下方为空" \
  --hold-purpose "为后期叠加批准的风险提示与活动主体信息提供4秒静止阅读时间" \
  --preserve "讲者身份、服装和表情" --preserve "背景墙Logo与比例" \
  --preserve "固定机位和焦段" --preserve "灯光、肤色和原始构图" \
  --safe-zone "左下40%保持干净，讲者与Logo不得进入" \
  --reject "不生成风险提示文字、二维码、联系方式、收益数字、手势或镜头运动" \
  --param duration=4
```

## 版本矩阵验收

1. 先对照母版：主体身份、商品、Logo、活动事实、人物关系和因果逻辑不能漂移。
2. 再看平台原生性：开场时限、画幅、字幕区、平台按钮区和观看节奏应符合渠道任务。
3. 关闭声音复看：唯一信息是否仍能看懂；打开声音后确认动作与原音节奏没有错位。
4. 逐帧检查重构边缘：不得拉伸脸和产品，不得因补画生成额外手指、配件、文字或场景。
5. 检查衔接：Hook 能否无跳帧接回母版，Loop 是否连续，停留段是否真正稳定可排版。
6. 保存 `campaign-id / variant-id / source-video / 批准来源 / 参数 / taskId`，才能追踪版本和复盘数据。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/social_matrix.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/social_matrix.py" status --task-id <taskId>
```

API Key 也可放入 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json`。默认使用 `COST_FIRST`，支持 `SPEED_FIRST`、`SUCCESS_FIRST`、多个 `--param key=value`、`--no-download` 和自定义输出目录。任务超时后查询原 `taskId`，不要直接重复提交。
