---
name: seedream-5-lite-product-retouch
description: "使用 Seedream 5.0 Lite 精修授权商品照片，修复灰尘、划痕、褶皱、反光、边缘和背景瑕疵，同时保持商品结构、材质、标签与商业事实不变。Use this skill for Seedream 5 Lite product retouch、商品精修、产品修图、电商修图、金属反光、透明包装、服装褶皱、食品摄影、淘宝京东抖音小红书亚马逊 Shopify 商品图片后期；通过 AI Hive 编辑指定图片。"
---

# Seedream 5.0 Lite 商品精修

固定使用 `public_model_seedream_5_0_lite`，必须提供商品图片。精修是“清理可逆瑕疵并恢复拍摄意图”，不是重做商品。先列出允许修复与禁止改变的项目，再提交编辑。

## 瑕疵清单

按灰尘污点、划痕、褶皱、曝光、色偏、反光、边缘、背景、透视和标签可读性分类。将商品结构、真实颜色、材质纹理、Logo、包装文字、容量、数量和认证列为锁定项。无法确定是瑕疵还是产品特征时，保留原样并请求确认。

## 场景与代码

### 1. 金属表面反光整理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./kettle-raw.jpg \
  --prompt '精修这张不锈钢水壶照片：去除拍摄现场杂乱反射、灰尘和小指纹，保留拉丝金属纹理、壶身真实弧度、壶嘴、把手、盖子和Logo；建立连续柔和的竖向高光，不改变颜色、容量、结构或背景构图' \
  --param aspect_ratio=1:1
```

### 2. 化妆品包装清洁

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./serum-raw.png \
  --prompt '清理精华液瓶身与滴管上的灰尘、细小水渍和背景脏点，校正轻微曝光不均；瓶型、液体颜色、标签版式、全部文字、容量和Logo必须逐字逐位保持，玻璃仍有真实厚度与折射，不生成新文字或磨皮式塑料质感'
```

### 3. 服装平铺褶皱控制

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./shirt-flatlay.jpg \
  --prompt '精修平铺衬衫：去除运输造成的尖锐折痕、毛屑和背景灰点，保留自然布料起伏、织纹、领型、袖口、纽扣数量、缝线、尺码标和真实色彩；不改变版型、收腰程度、长度或增加配饰' \
  --param aspect_ratio=4:5
```

### 4. 透明瓶边缘与液体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./drink-bottle-raw.jpg \
  --prompt '精修透明饮料瓶：清除背景杂点与瓶外壁不必要污迹，增强瓶缘分离度，保持液体真实色泽、液位、气泡、瓶盖结构、标签文字和透明折射；不改变容量、不增加冰块水果、不制造夸张冷凝水或替换标签'
```

### 5. 食品照片自然清理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./cookies-raw.jpg \
  --prompt '精修曲奇商品照：清除盘边碎屑和背景污点，平衡暖色偏差，保留每块曲奇的真实数量、大小差异、烘烤纹理和巧克力分布；只改善拍摄瑕疵，不复制曲奇、不增加馅料、不制造拉丝效果或改变包装内容' \
  --param aspect_ratio=4:5
```

## 对照验收

- 在100%与200%视图逐项比较原图，确认没有新缺陷或商品漂移。
- 标签、Logo、颜色、数量、结构和配件与原图完全一致。
- 反光和阴影连续但不“磨平”材质，透明物仍有真实折射。
- 食品与服装保留合理自然差异，不用复制纹理填补区域。
- 保存原片、瑕疵清单、提示词、任务 ID 与批准成品。

## 助手边界

工具只上传命令中指定的图片，查询固定 Seedream 5.0 Lite 图片模型和路由价格，提交编辑任务、轮询并下载结果。认证请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。Key 可通过 `init` 以 `0600` 权限本地保存；没有聊天、视频、钱包或账户查询。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-product-retouch
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不要修掉真实损伤后把二手或瑕疵品冒充新品；面向消费者的成品应保留商品事实。
