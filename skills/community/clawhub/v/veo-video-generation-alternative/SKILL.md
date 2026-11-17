---
name: veo-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将 Google Veo、Veo 3、Google Flow 或电影化视频需求迁移为镜头覆盖计划，支持文生、首帧图生、参考摄影、视频编辑与延长。Use when users search Veo 替代、Veo 3 平替、Google video alternative、Veo API、广告片、电影摄影、产品视频、镜头运动或视频编辑；不调用 Google Veo，也不承诺原生音频能力。"
---

# Veo 视频生成替代｜AI 视频生成与编辑

按摄影覆盖而不是“一个提示词拍完整支片”来组织任务。为每个镜头确定景别、焦点、相机高度、运动、光线和可剪辑出点；底层固定使用 Seedance 2.5 五种模式。声音、对白和混音不假定由本 Skill 生成，应在后期独立制作。

## 摄影覆盖单

填写 `镜头用途 / 景别 / 焦点主体 / 相机位置 / 运动轨迹 / 光线 / 入出点 / 后期声音备注`。同一场景至少保留建立镜头、动作镜头和细节镜头的关系，不在单条短片里频繁切景别。

## 五个摄影任务

### 1. 建立镜头

```bash
python3 "$SKILL_PATH/scripts/veo_coverage.py" establish \
  --purpose '清晨山谷木屋的建立镜头' \
  --framing '大全景到全景' \
  --subject '山谷中的现代木屋' \
  --camera '从树梢高度开始，朝向入口' \
  --motion '缓慢下降并轻推向入口' \
  --light '雾沿谷底移动，主光从右后方' \
  --out '木屋入口稳定落在画面中央' \
  --protect '单一连续镜头；不生成文字、Logo、人物复制、建筑变形或突然变焦' \
  --param aspect_ratio=16:9 duration=6
```

### 2. 产品细节首帧

```bash
python3 "$SKILL_PATH/scripts/veo_coverage.py" detail \
  --start-frame ./approved-camera-detail.png \
  --purpose '产品机身细节镜头' \
  --framing '微距特写' \
  --subject '批准首帧中的相机机身和镜头环' \
  --camera '贴近镜头环并与刻度平行' \
  --motion '沿镜头环缓慢横移' \
  --focus '从前环移到机身标识并停稳' \
  --protect '机身、镜头、按钮、刻度、Logo和材质不变；不生成手、文字、配件或第二台相机' \
  --param aspect_ratio=16:9 duration=5
```

### 3. 摄影路径参考

```bash
python3 "$SKILL_PATH/scripts/veo_coverage.py" track \
  --reference-image ./approved-car.png ./approved-road.png \
  --reference-video ./authorized-crane-path.mp4 \
  --purpose '汽车广告的运动覆盖镜头' \
  --framing '低位全景到斜侧全景' \
  --subject '图1唯一汽车与图2道路环境' \
  --camera '从汽车右后方低位开始' \
  --motion '只借用视频从低位升高并向左绕行的摄影路径' \
  --protect '不复制参考视频车辆、场景和文字；汽车结构、颜色、Logo和行驶方向不变' \
  --param aspect_ratio=16:9 duration=6
```

### 4. 光线连续性编辑

```bash
python3 "$SKILL_PATH/scripts/veo_coverage.py" relight \
  --source-video ./authorized-interior-shot.mp4 \
  --purpose '修复室内镜头的光线连续性' \
  --subject '原人物与窗外过曝区域' \
  --camera '保持原镜头位置和路径' \
  --light '只把窗外恢复为柔和阴天亮度，并让人物边缘光连续' \
  --protect '人物、动作、焦点变化、时长、脸、服装和背景结构不变；不生成文字或新物体'
```

### 5. 延长可剪辑出点

```bash
python3 "$SKILL_PATH/scripts/veo_coverage.py" outro \
  --source-video ./approved-dolly-shot.mp4 \
  --purpose '为产品推近镜头补足干净出点' \
  --subject '产品正面' \
  --camera '延续末帧的摄影机位置与方向' \
  --motion '继续同速推近后平稳减速' \
  --focus '始终保持产品正面清晰' \
  --out '人物手在画外退出，形成稳定产品画面' \
  --protect '不切镜，不改变产品、光线、色彩或新增文字' \
  --param duration=3
```

## 摄影验收

检查景别、焦点、相机高度和运动是否符合覆盖单；光线方向、运动惯性与出点必须连续。声音字段只作为后期备注，不声称视频包含对白、配乐或同步音效。保留任务号与剪辑采用记录。

脚本不访问 Google、Veo 或 Flow。认证流量只到 `https://ai-hive.iclip.cn/api`，固定调用 Seedance 2.5 视频模型。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/veo_coverage.py" setup --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/veo_coverage.py" check --task-id <taskId>
```

Veo、Veo 3、Google Flow 名称仅用于比较和迁移搜索。
