---
name: video-classifier
description: "Classify unstructured long videos by selecting them in the backend and applying tags. Use when: user wants to classify videos, tag videos with specific labels, batch categorize video content, classify unstructured videos, tag videos in video management backend, add videos to structure, video classification workflow, 视频分类, 无结构视频, 加入结构, 视频标签. The user will provide the tag name and the number of videos to classify."
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python3"] } } }
---

# Video Classifier Skill

**IMPORTANT: Use the browser tool to automate this workflow. Do NOT ask the user to do manual steps.**

## Backend Info
- URL: https://staff.bluemv.net/d.php
- Profile: chrome (with CDP debugging)

## CRITICAL: Browser Automation Steps

You MUST use the browser tool (browser.profile.chrome) to complete this task:

1. **Navigate to backend**: Use `browser.navigate` to open https://staff.bluemv.net/d.php

2. **Click menu**: Use `browser.click` to:
   - Click [视频管理] menu
   - Select [小视频]

3. **Set filters**: Use browser actions to:
   - Check 展示 → 显示
   - Select 类型 → 长视频
   - Select 结构 → 无结构视频
   - Set 刷新时间: 2023-01-10 to today
   - Fill 标签: [user-provided tag]

4. **Select all videos**: Use `browser.check` to check all matching videos

5. **Submit**: Use `browser.click` to:
   - Click [加入结构]
   - Select the tag
   - Click 确认 (Confirm)

## Usage Examples

```
User: "帮我分类视频，标签是狼"
→ Execute with tag="狼"

User: "帮我分类20个视频，标签是狮子"  
→ Execute with tag="狮子", count=20

User: "今天分类200个老虎视频"
→ Execute with tag="老虎", count=200
```

## Common Tags

狼、熊、狮子、老虎、大象、猴子、鸟类、水族、家禽、爬行动物

## Notes

- User must be logged in to https://staff.bluemv.net/d.php before starting
- Process in batches of 50-100 for better reliability
- Daily target: 200 video classifications
- Take screenshots at key steps for verification
