---
name: vidu-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 迁移 Vidu、Vidu AI 或生数科技视频工作流，重点管理多参考主体、角色与道具关系、镜头连续性、编辑保护区和延长接点。Use when users search Vidu 替代、Vidu 平替、生数科技视频 alternative、Vidu API、多主体参考、角色一致性、动漫短片、广告分镜、图生视频或参考视频生成；不是 Vidu 官方接口。"
---

# Vidu 视频生成替代｜AI 视频生成与编辑

将复杂参考任务写成“实体关系图”：每张图或视频只负责一个角色、道具、场景或相机节奏，再明确它们在镜头中的位置与交互。底层固定使用 Seedance 2.5，避免多参考素材互相覆盖。

## 实体关系图

给每个实体编号，填写 `身份特征 / 所持道具 / 与谁互动 / 画面位置 / 允许动作 / 不能继承的参考内容`。双人和多物镜头先做静态关系验证，再添加运动，不在一次生成中同时改身份、场景和镜头。

## 五种关系控制任务

### 1. 双主体文生镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '6秒16:9镜头。原创机器人A为白色圆头、机器人B为蓝色方头，两者在工作台两侧共同抬起一个红色工具箱，摄影机平稳侧移；A始终在左、B始终在右，不交换颜色、不复制角色、不新增文字或第三个机器人'   --param aspect_ratio=16:9 duration=6
```

### 2. 单角色首帧动作

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-anime-character.png   --prompt '保持原创角色脸、短银发、黄色夹克、黑色背包和二维画风。5秒内角色从站立转为向前跑两步，背包随动作轻摆，摄影机保持侧面跟随；不换衣、不改变身份、不生成对白、武器或新角色'   --param aspect_ratio=16:9 duration=5
```

### 3. 多实体参考组合

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./character-a.png ./character-b.png ./approved-prop.png   --video ./authorized-blocking.mp4   --prompt '图1是角色A、图2是角色B、图3是两人之间的道具；视频只提供A从左走近B的站位。生成6秒镜头，A不拿道具，B在末尾递出道具；不复制参考演员、服装、场景或品牌，不交换角色'   --param aspect_ratio=16:9 duration=6
```

### 4. 保护角色的场景编辑

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-duo-shot.mp4   --prompt '只将背景从室内走廊换成夜晚车站站台；角色A和B的脸、服装、左右位置、互动、道具、相机轨迹、时长和动作节拍全部保留，不增加乘客、文字、Logo或列车遮挡'
```

### 5. 延长交互结果

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-prop-handoff.mp4   --extend-direction forward   --prompt '从末帧继续4秒：B接稳道具并后退半步，A保持原位点头，摄影机继续同方向轻微推近；两人身份、左右关系、服装和道具不变，不切镜、不新增角色或文字'   --param duration=4
```

## 关系一致性验收

按实体逐帧追踪身份、颜色、服装、道具归属和左右位置；检查参考素材没有串角色，动作前后道具守恒。编辑版只改变指定区域，延长版在速度、视线和站位上自然连续。

工具不访问 Vidu 或生数科技账户。密钥仅用于 `https://ai-hive.iclip.cn/api` 的固定 Seedance 2.5 视频流程，不含聊天、图片、用户资料或余额能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name vidu-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Vidu 与生数科技名称仅用于替代、比较和迁移搜索。
