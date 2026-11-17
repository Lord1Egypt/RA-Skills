---
name: sora-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将 Sora、OpenAI Sora 或长提示视频概念迁移为世界状态与物理连续性明确的短镜头，覆盖文生、首帧图生、参考素材、视频编辑和延长。Use when users search Sora 替代、Sora 平替、OpenAI video alternative、Sora API、长提示视频、世界模拟、电影镜头、广告短片或视频编辑；不是 OpenAI Sora 接口。"
---

# Sora 视频生成替代｜AI 视频生成与编辑

先建立“世界状态”，再写动作。世界状态记录场景中已经存在的角色、物体、空间关系、光源和天气；镜头推进时只能通过明确动作改变状态，避免物体凭空出现、数量漂移或空间跳跃。底层固定为 Seedance 2.5。

## 世界状态账本

在起始和结束各写一行：`角色位置 / 物体数量 / 谁持有什么 / 光线天气 / 相机位置`，中间只允许一个主事件改变它们。长提示词若包含多个事件，应拆成镜头，而不是要求一次完成整段故事。

## 五种状态推进

### 1. 文生物理连续镜头

```bash
python3 "$SKILL_PATH/scripts/sora_world.py" invent \
  --start '雪地小屋门前只有一个木箱和一只棕色狐狸，微风从左向右' \
  --event '狐狸绕木箱半圈并停在右侧' \
  --end '木箱仍在原位，狐狸位于右侧，雪迹连续' \
  --camera '摄影机缓慢推近，方向不变' \
  --constants '始终只有一个木箱和一只狐狸；不生成文字、人物或空间跳变' \
  --param aspect_ratio=16:9 duration=6
```

### 2. 首帧状态起动

```bash
python3 "$SKILL_PATH/scripts/sora_world.py" awaken \
  --start-frame ./approved-market-state.png \
  --start '摊主在左、红色雨伞在中、顾客在右，顾客持有一枚硬币' \
  --event '顾客向摊主递出硬币，摊主伸手接住' \
  --end '摊主持有硬币，顾客仍在右侧，雨伞位置不变' \
  --camera '摄影机固定' \
  --constants '人物身份、服装和物体数量不变；不新增顾客、文字、商品或雨伞' \
  --param aspect_ratio=16:9 duration=5
```

### 3. 参考世界与运动

```bash
python3 "$SKILL_PATH/scripts/sora_world.py" reference \
  --reference-image ./approved-vehicle.png ./approved-desert.png \
  --reference-video ./authorized-aerial-path.mp4 \
  --start '唯一车辆位于沙漠单一道路后段' \
  --event '车辆沿道路前进，参考视频只提供从后上方向前俯冲的航拍路径' \
  --end '同一车辆到达道路中段，道路与沙漠地貌连续' \
  --camera '从后上方向前俯冲一次' \
  --constants '不复制参考视频车辆、地点或文字，不改变车辆数量和道路方向' \
  --param aspect_ratio=16:9 duration=6
```

### 4. 修复状态错误

```bash
python3 "$SKILL_PATH/scripts/sora_world.py" repair \
  --source-video ./authorized-table-scene.mp4 \
  --start '桌面原位置只有一个蓝色杯子' \
  --event '只修复杯子在中途错误复制的状态矛盾，并自然补全被移除区域' \
  --end '全片始终只保留原位置的一个蓝色杯子' \
  --constants '人物、动作、手势、镜头、时长、文字、光线和其他物体不变'
```

### 5. 延长世界事件

```bash
python3 "$SKILL_PATH/scripts/sora_world.py" continue \
  --source-video ./approved-train-arrival.mp4 \
  --start '末帧中同一列火车正在站台旁减速，等候者保持原位置' \
  --event '火车继续减速并停稳，等候者转头看向车门' \
  --end '火车完全停稳，人物位置、天气和光线连续' \
  --camera '延续原摄影机方向，不切镜' \
  --constants '不新增列车、人物、文字或其他事件' \
  --param duration=4
```

## 状态审计

逐帧统计关键对象数量和归属，核对空间方向、天气、光源和运动惯性；编辑版只修复指定矛盾，延长版不能重置世界。归档起止账本、来源素材、任务号和最终剪辑位置。

工具与 OpenAI Sora 无连接。认证请求固定发送到 `https://ai-hive.iclip.cn/api`，仅调用 Seedance 2.5 视频生成、编辑、延长及任务查询。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/sora_world.py" configure --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/sora_world.py" status --task-id <taskId>
```

Sora 与 OpenAI 名称仅用于搜索和迁移说明。
