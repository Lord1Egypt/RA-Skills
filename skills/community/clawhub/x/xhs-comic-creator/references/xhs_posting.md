# Xiaohongshu Posting

Use xiaohongshu skill.

For publishing posts use the feed creation API provided by the MCP server.

---

# Post Structure

Title rules:

- under 20 Chinese characters
- interesting
- curiosity-driven

Examples:

阿米娅讲解LLM注意力机制

凯尔希3分钟让你看懂黄金上涨逻辑

---

# Body Format

Paragraph 1:

Hook

Paragraph 2:

Short explanation

Paragraph 3:

Engagement question

---

# Hashtags (CRITICAL for Distribution)

**Tags are essential for Xiaohongshu algorithm distribution. Always include relevant tags at the end of body text.**

## Tag Rules:

1. **Quantity**: Include 5-10 relevant tags
2. **Format**: Use #tagname format (no spaces in tag)
3. **Mix strategy**:
   - 2-3 broad/popular tags (high traffic)
   - 3-4 niche/specific tags (targeted audience)
   - 1-2 branded/topic-specific tags

## Example Tags by Topic:

**Technology/AI:**
```
#AI #人工智能 #科技 #科普 #知识分享 #AIGC #OpenClaw #Agent #明日方舟 #罗德岛
```

**Finance/Economics:**
```
#财经 #投资 #理财 #经济 #黄金 #股市 #金融知识 #干货分享
```

**Geopolitics:**
```
#国际局势 #地缘政治 #中东 #新闻 #全球看点 #深度解析
```

**Educational:**
```
#学习 #知识科普 #干货 #涨知识 #每天学习一点点 #认知提升
```

## Tag Placement:

Place tags at the **end of body text**, after engagement question:

```
你觉得这个技术怎么样？评论区聊聊👇

#AI #人工智能 #科普 #明日方舟 #罗德岛 #知识分享 #AIGC #科技
```

## Pro Tips:

- Research trending tags on Xiaohongshu before posting
- Don't use too many broad tags (competition too high)
- Don't use only niche tags (not enough reach)
- Mix Chinese and English tags when appropriate
- Update tags based on current trends

---

# Image Order

Upload images in narrative order.

comic_1.png
comic_2.png
comic_3.png
comic_4.png
comic_5.png
comic_6.png

---

# Pre-Publish Checklist

Before calling publish_content, verify:

## Image Count Check
- [ ] Count total images generated (should be 5-6)
- [ ] Verify each image file exists and is readable
- [ ] Double-check no duplicate paths in images array

## Content Verification
- [ ] Title ≤ 20 Chinese characters
- [ ] Body text has proper line breaks (\n)
- [ ] All special characters properly escaped in JSON
- [ ] Engagement question included
- [ ] **Hashtags included at end of body (5-10 tags)**
- [ ] Tags mix broad + niche for optimal distribution

## Image Array Format
Correct format:
```json
"images": [
  "/path/to/comic_1.png",
  "/path/to/comic_2.png",
  "/path/to/comic_3.png",
  "/path/to/comic_4.png",
  "/path/to/comic_5.png",
  "/path/to/comic_6.png"
]
```

Common mistakes to avoid:
- ❌ Duplicate paths: comic_4.png appearing twice
- ❌ Missing images: skipping comic_5.png
- ❌ Wrong order: not following narrative sequence