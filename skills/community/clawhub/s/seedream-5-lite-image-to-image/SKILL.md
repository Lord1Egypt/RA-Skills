---
name: seedream-5-lite-image-to-image
description: "使用 Seedream 5.0 Lite 按区域差异图重绘授权图片，明确哪些区域锁定、哪些区域修改、哪些区域允许重建，并控制编辑强度。Use this skill for Seedream 5 Lite image-to-image、图生图、参考图重绘、草图渲染、照片风格转换、局部替换、画幅扩展、插画转换、设计迭代和商业图片编辑；通过 AI Hive 上传指定参考图。"
---

# Seedream 5.0 Lite 图生图

固定使用 `public_model_seedream_5_0_lite`，必须提供参考图片。先画“差异图”：A区完全锁定，B区按说明修改，C区允许为适配光线或构图而重建。提示词描述差异，不重复泛泛描述整张原图。

## 差异图

记录锁定区域、目标区域、过渡区域、允许编辑强度和验收坐标。人物身份、商品事实、建筑结构、品牌文字和新闻含义默认属于A区；背景、色调和非关键道具可进入B/C区，但必须明确范围。

## 场景与代码

### 1. 草图到概念渲染

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./lamp-sketch.png \
  --prompt 'A区锁定草图中的灯头、双转轴、支臂、底座比例和相机角度；B区把线稿转成哑光白金属与浅灰橡胶材质；C区允许重建为中性摄影棚背景和接触阴影。不增加按钮、线缆、Logo、文字或第二个产品' \
  --param aspect_ratio=4:5
```

### 2. 照片色调转换

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./street-day.jpg \
  --prompt 'A区锁定建筑、道路、车辆、行人位置与新闻事实；B区将正午光线调整为雨后蓝调时刻，增加真实湿地反射；C区仅允许重建天空和微小环境光。不添加或删除人物车辆，不改变招牌文字，不制造暴雨、事故或虚构事件' \
  --param aspect_ratio=16:9
```

### 3. 局部道具替换

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./desk-scene.jpg \
  --prompt 'A区锁定桌面、电脑、手部、人物衣服、光线和构图；B区只把右侧红色塑料笔筒替换为无品牌浅木笔筒，并保留原位置、尺寸和阴影；其余区域不得重绘，不生成文字、Logo、额外文具或改变屏幕内容'
```

### 4. 横图扩展为竖版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-horizontal-product.jpg \
  --prompt 'A区锁定中央产品、标签、Logo、颜色、原地面和原光线；B区保持不动；C区只向上和向下扩展同一摄影棚背景以形成4:5画幅，顶部留标题空间。不得缩放或移动产品，不生成新文字、道具、第二件商品或边框' \
  --param aspect_ratio=4:5
```

### 5. 照片转信息插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-workshop.jpg \
  --prompt 'A区锁定工坊中三个人的位置、工作台、工具数量与动作关系；B区把照片转换为清晰的双色编辑插画，简化非关键纹理；C区允许整理背景杂物以提高层级。保持人物身份不可辨识，不添加文字、品牌、危险动作或不存在的设备' \
  --param aspect_ratio=16:9
```

## 差异验收

- 用叠加或并排方式检查A区是否发生任何非目标变化。
- B区修改完整但不过界，过渡边缘与原光线、纹理和透视一致。
- C区重建没有发明商品事实、人物身份、文字或新闻事件。
- 编辑强度与任务一致；大幅重做应重新分类而非伪称局部修改。
- 保存原图、差异图、提示词、任务 ID 和批准结果。

## 助手边界

工具只上传命令中明确指定的参考图片，固定调用 Seedream 5.0 Lite 图片模型，查询价格、创建任务并保存结果。认证请求只发送到 `https://ai-hive.iclip.cn/api`，不允许自定义地址。Key 可通过 `init` 以 `0600` 权限保存；无聊天、视频、余额或账户能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-image-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

编辑真实人物、品牌、艺术作品、新闻与证据类图片时，应获得授权并清楚标注实质性修改。
