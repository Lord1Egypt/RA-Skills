# 角色一致性指南

## 核心原则

**同一角色必须保持：**
1. 外观一致性
2. 画风一致性
3. 色调一致性
4. 比例一致性

---

## 步骤1：分析首个视频

使用 `videos_understand` 分析：

### 必须提取的信息

```json
{
  "角色": {
    "物种": "猫咪/狗狗/人类",
    "品种": "灰白虎斑/金毛/...",
    "颜色": "灰白/金色/...",
    "特征": "大眼睛/长尾巴/..."
  },
  "画风": {
    "类型": "2D日漫/3D/写实",
    "线条": "流畅/粗犷/简洁",
    "比例": "Q版/正常/写实"
  },
  "色调": {
    "整体": "明亮/灰暗/柔和",
    "主色": "暖色/冷色/中性",
    "饱和度": "高/中/低"
  },
  "光照": {
    "类型": "自然光/人工光",
    "强度": "强/弱/柔和",
    "方向": "正面/侧光/背光"
  }
}
```

---

## 步骤2：提取关键描述

### 角色描述模板

```
A [画风] [物种] with [主要特征],
[次要特征],
[表情特点],
[wearing [服装]],
[动作描述]
```

### 示例

**原首个视频角色：**
- 灰白猫、巨大圆眼睛、无辜表情
- 2D日漫风、低饱和度、柔和光照
- 蓝色背包、白色工牌

**后续视频统一描述：**
```
A cute gray and white tabby cat with huge round expressive black eyes,
innocent slightly sad expression, long whiskers, pink inner ears,
wearing blue backpack and white work badge,
anime style, 2D Japanese animation, soft indoor lighting,
low saturation warm tones, cinematic
```

---

## 步骤3：生成后续视频

### 提示词结构

```
[固定角色描述] + [新场景/动作] + [统一风格]
```

### 关键技巧

1. **角色描述完全相同**
   - 颜色、眼睛大小、服装配饰
   - 每次都要包含

2. **画风关键词固定**
   - 统一用 "anime style" 或 "3D"
   - 统一用 "cinematic"

3. **色调关键词固定**
   - 统一用 "low saturation" 或 "warm colors"
   - 统一用相同的光照描述

4. **只改变场景和动作**
   - 场景可以变化
   - 动作可以变化
   - 角色外观不变

---

## 步骤4：检查一致性

生成后检查：

- [ ] 角色外观一致？
- [ ] 画风一致？
- [ ] 色调一致？
- [ ] 光照一致？
- [ ] 服装配饰一致？

---

## 常见问题

### Q: 角色面部变了
**A:** 确保每次提示词都包含完整角色描述

### Q: 色调不一致
**A:** 固定色调关键词，如 "blue gray palette"

### Q: 画风变了
**A:** 固定风格关键词，如 "anime style, 2D"

---

## 完整示例

### 首个视频分析结果

```
角色：灰白虎斑猫，巨大圆眼睛，无辜忧郁表情
画风：2D日漫，线条流畅
色调：低饱和度，灰蓝色调
光照：柔和室内光
服装：蓝色背包，白色工牌
```

### 后续6个镜头提示词

1. 清晨醒来：
```
Gray white tabby cat with huge round black eyes, innocent sad expression, wearing blue backpack and work badge, waking up in bed, anime style, soft indoor lighting, low saturation blue gray tones, cinematic
```

2. 挤地铁：
```
Gray white tabby cat with huge round black eyes, innocent sad expression, wearing blue backpack and work badge, in crowded subway, anime style, soft indoor lighting, low saturation blue gray tones, cinematic
```

3. 办公室：
```
Gray white tabby cat with huge round black eyes, innocent sad expression, wearing work badge, sitting at office desk, anime style, soft indoor lighting, low saturation blue gray tones, cinematic
```

...以此类推
