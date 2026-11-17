---
name: runway-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将 Runway、Runway AI、Gen-4 或生成式视频制作需求迁移为可追踪的镜头版本，支持文生、首帧图生、参考素材、视频编辑与延长。Use when users search Runway 替代、Runway 平替、Gen-4 alternative、Runway API、AI 电影镜头、广告视频、生成式编辑、扩镜或视频延长；不访问 Runway 项目，也不表示技术兼容。"
---

# Runway 视频生成替代｜AI 视频生成与编辑

把每个生成镜头当作制作资产，而不是一次性结果。建立镜头编号、源素材、版本目的、保护区、唯一变化和剪辑去向；底层固定调用 Seedance 2.5 的 t2v、i2v、r2v、edit、extend。

## 镜头版本板

为镜头填写 `Shot ID / 入点 / 主动作 / 相机 / 出点 / 保护项 / 本版只改什么 / 目标剪辑位`。一次版本只解决一个问题，例如相机速度、背景、动作幅度或收尾长度，避免无法判断哪个改动有效。

## 五种版本任务

### 1. 建立文生镜头 V1

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '6秒16:9制作镜头 SH010-V1。黄昏工业码头，一辆无品牌电动货车缓慢驶过湿地面，摄影机低机位横向跟拍，最后车辆停在画面右侧；运动方向和车身稳定，不生成文字、Logo、第二辆车、跳切或不可能反射'   --param aspect_ratio=16:9 duration=6
```

### 2. 从批准首帧起动

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./SH020-approved-start.png   --prompt 'SH020-V2：首帧产品外形、按钮、材质、颜色和Logo锁定。5秒内摄影机从正面缓慢移到右侧约20度，产品不自行旋转，末帧留下右侧留白；不新增文字、手、配件或第二件产品'   --param aspect_ratio=16:9 duration=5
```

### 3. 分离参考职责

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./approved-character.png ./approved-location.png   --video ./authorized-dolly-rhythm.mp4   --prompt 'SH030-V1：图1锁定原创人物，图2锁定车站环境，视频只提供缓慢后拉节奏。生成角色走到站台边停下的6秒镜头；不复制参考视频演员、服装和地点，不改变人物身份或场景结构'   --param aspect_ratio=16:9 duration=6
```

### 4. 背景版本修改

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./SH040-approved-performance.mp4   --prompt 'SH040-V3只修改背景：把白色摄影棚改为深灰无缝背景，并保持原人物、表演、服装、口型、镜头轨迹、阴影方向、时长和剪辑点不变；不生成文字、Logo或道具'
```

### 5. 补足剪辑尾长

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./SH050-approved-cut.mp4   --extend-direction forward   --prompt 'SH050-V2从末帧延长3秒：摄影机继续同速向后移动，演员保持视线方向并自然停步，环境运动连续，最后形成稳定远景；不切镜、不改变身份、服装、光线或新增人物'   --param duration=3
```

## 交付验收

先核对 Shot ID 和本版唯一变化，再逐帧检查保护区、动作方向、相机速度与出点。编辑版和延长版必须与批准源片检查接缝；保留版本板、任务 ID、源素材授权和最终剪辑使用记录。

脚本不会读取 Runway 账号或云端工程。认证通信仅到 `https://ai-hive.iclip.cn/api`，五种模式固定对应 Seedance 2.5，不包含聊天、图片、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name runway-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Runway、Gen-4 名称仅用于替代和迁移搜索。
