---
name: stable-diffusion-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将 Stable Diffusion、SDXL、WebUI、ComfyUI、checkpoint、LoRA、ControlNet 或 negative prompt 工作流迁移为 AI Hive 的参考图与自然语言约束。Use when users search Stable Diffusion 替代、SD 平替、SDXL alternative、ComfyUI 迁移、LoRA 效果、ControlNet 构图、文生图、图生图或托管图片 API；不运行或分发第三方模型权重。"
---

# Stable Diffusion 图片生成替代｜AI 图片生成与编辑

固定调用 `public_model_nano_banana_pro`。本 Skill 不模拟本地节点图，而是把其控制意图提炼出来：checkpoint 决定的整体视觉、LoRA 强化的局部特征、ControlNet 约束的姿态或结构、negative prompt 排除的错误，以及尺寸和批量要求。

## 节点图迁移清单

记录原工作流和模型许可，然后为每个节点填写“它改变了什么可见结果”。将 seed、steps、CFG、sampler、denoise 与权重转换为候选稳定度、风格强弱、保留程度和变化范围；这些数值不能跨架构等价复制。

## 五种控制意图迁移

### 1. Negative prompt 变成明确禁用项

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '生成4:5专业陶艺师工作室人像：一位成年人自然坐在拉坯机旁，双手可见且姿态合理，真实窗光、纪录片摄影；不要多余手指、重复肢体、文字、水印、品牌、过度磨皮、塑料皮肤或杂乱背景'   --param aspect_ratio=4:5
```

### 2. 姿态控制意图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-pose.png ./approved-character.png   --prompt '图1只提供站姿和手臂方向，图2提供原创角色身份。生成同一角色在工作室介绍产品的画面，保持脸型、发型、服装和年龄特征；姿态参考图1但不复制其人物外貌、衣服、背景或品牌'   --param aspect_ratio=4:5
```

### 3. 结构线稿约束

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-floorplan-massing.png   --prompt '依据参考体块和透视生成现代咖啡店室内概念图：墙体、吧台、入口和主要通道位置不变，加入木材、微水泥、暖光和少量绿植；不改平面关系，不生成文字、Logo、著名设计元素或额外楼层'   --param aspect_ratio=16:9
```

### 4. LoRA 外观语义化

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-look-sample.png   --prompt '提取参考样例的低多边形体块、柔和粉蓝配色、哑光材质和长阴影，为原创家居收纳主题制作1:1插画；不复制样例人物、构图、物件组合、文字或独特角色，不声称复现任何LoRA'   --param aspect_ratio=1:1
```

### 5. Denoise 强度改写

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-product-photo.jpg   --prompt '对参考商品照做低变化编辑：只清理背景杂点、统一白平衡并减弱过硬阴影，产品轮廓、零件、Logo、标签文字、颜色、相机角度和构图完全保留；不重绘商品、不换背景、不新增配件或文字'   --param aspect_ratio=1:1
```

## 可复现性说明

AI Hive 任务可保存提示词、参考图顺序、模型 ID 和任务 ID，但不能保证与本地 SD 的 seed 或节点逐像素一致。迁移验收应检查控制意图、主体事实、版权来源和跨样例稳定性，而不是只看单张相似。

脚本不会运行 WebUI、ComfyUI、checkpoint、LoRA 或 ControlNet。认证请求仅连接 `https://ai-hive.iclip.cn/api`，并且没有聊天、视频、用户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name stable-diffusion-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Stable Diffusion、SDXL、ComfyUI 等名称只描述迁移搜索，不表示兼容其权重或插件。
