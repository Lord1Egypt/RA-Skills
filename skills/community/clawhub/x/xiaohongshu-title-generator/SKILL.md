---
name: xiaohongshu-title-generator
version: 1.0.0
description: "批量生成小红书爆款标题，支持多种模板和 emoji 自动添加"
author: xiaokai-ai
license: MIT
platforms:
  - openclaw
  - cursor
  - claude-code
tags:
  - content
  - xiaohongshu
  - title
  - generator
  - chinese
price: 9.9
---

# 小红书爆款标题生成器

批量生成小红书风格爆款标题，适合内容创作者、电商卖家、自媒体运营。

## When to Activate

Trigger when the user mentions: 小红书标题，生成标题，爆款标题，title generator, xiaohongshu titles.

## Workflow

1. **Confirm inputs:**
   - 主题/关键词 (required)
   - 目标受众 (optional: 学生党/上班族/宝妈/等)
   - 标题数量 (default: 10, max: 50)
   - 风格偏好 (optional: 干货型/种草型/测评型/故事型)

2. **Generate titles using templates:**

### Title Templates

**数字型** (点击率高)
- "{数字}个{主题}技巧，亲测有效！"
- "花了{数字}{单位}，总结的{主题}攻略"
- "{数字}年{主题}经验，告诉你{痛点}"

**疑问型** (引发好奇)
- "为什么你的{主题}总是{问题}？"
- "{主题}到底要不要{行为}？"
- "谁懂啊！{主题}这样{行为}真的好吗？"

**对比型** (突出差异)
- "{产品 A}vs{产品 B}，到底哪个更{指标}？"
- "月薪{数字}和月薪{数字}的{主题}区别"
- "用{方法 A}和{方法 B}，效果差{数字}倍！"

**痛点型** (引发共鸣)
- "{人群}必看！{痛点}终于有救了"
- "后悔没早{行为}！{主题}避坑指南"
- "{主题}踩了{数字}个坑，总结的血泪教训"

**种草型** (促进转化)
- "按头安利！这个{主题}真的{形容词}"
- "挖到宝了！{价格}的{主题}居然{效果}"
- "无限回购！{主题}界的{比喻}"

3. **Add emoji automatically:**
   - 根据标题内容匹配相关 emoji
   - 每个标题 1-3 个 emoji
   - 避免过度使用

4. **Quality check:**
   - 标题长度 15-30 字 (最佳阅读体验)
   - 包含关键词 (SEO 友好)
   - 避免违禁词 (最/第一/唯一等)
   - 有吸引力但不标题党

## Output Format

```markdown
## 生成的{数量}个小红书标题

### 数字型
1. 💡 {标题 1}
2. 📊 {标题 2}
3. 🎯 {标题 3}

### 疑问型
4. 🤔 {标题 4}
5. ❓ {标题 5}

### 对比型
6. ⚖️ {标题 6}
7. 🆚 {标题 7}

### 痛点型
8. 😭 {标题 8}
9. ✅ {标题 9}

### 种草型
10. 🌿 {标题 10}

---
**使用建议:**
- A/B 测试不同标题看数据
- 根据封面图选择匹配的标题
- 结合热点话题效果更好
```

## Examples

**输入:**
```
主题：护肤
受众：25 岁 + 女性
数量：10
风格：干货型
```

**输出:**
```
## 生成的 10 个小红书标题

### 数字型
1. 💡 25 岁后必看的 5 个抗初老秘诀！
2. 📊 花了 3 万块，总结的护肤攻略
3. 🎯 10 年护肤经验，告诉你怎么选精华

### 疑问型
4. 🤔 为什么你的护肤总是没效果？
5. ❓ 早 C 晚 A 到底要不要建立耐受？

### 对比型
6. ⚖️ 平价 vs 大牌，精华液哪个更值得？
7. 🆚 国货和进口，护肤品差 3 倍价格！

### 痛点型
8. 😭 敏感肌必看！泛红终于有救了
9. ✅ 后悔没早刷酸！黑头避坑指南

### 种草型
10. 🌿 按头安利！这个精华真的绝了

---
**使用建议:**
- A/B 测试不同标题看数据
- 根据封面图选择匹配的标题
- 结合热点话题效果更好
```

## Pricing

- **Free tier:** 10 titles per generation
- **Pro tier:** ¥9.9/month - unlimited generations

## Support

Issues: https://github.com/xiaokai-ai/xiaohongshu-title-generator
Docs: https://clawhub.ai/skills/xiaohongshu-title-generator

---

*Made with ❤️ by Xiao Kai AI*
