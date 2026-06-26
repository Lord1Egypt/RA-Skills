---
name: publish-short-videos-infinite
description: 依次发布短视频到快手、抖音、小红书三个平台。先发布快手，再发布抖音，最后发布小红书。触发场景：同时发布快手和抖音、发布到多个平台、多平台发布短视频、批量发布视频、全平台发布。
---

# 发布短视频到三平台_无限

依次发布短视频到**快手**、**抖音**、**小红书**三个平台。按顺序完成：快手 → 抖音 → 小红书。

## 触发场景

用户说：
- "同时发布快手和抖音"
- "发布到多个平台"
- "多平台发布短视频"
- "批量发布视频"
- "全平台发布"

## 执行顺序

**第一步：发布快手** → 加载并执行 `post-kuaishou-short-videos-infinite` 技能  
**第二步：发布抖音** → 加载并执行 `post-tiktok-short-videos-infinite` 技能  
**第三步：发布小红书** → 加载并执行 `publish-xhs-short-videos-infinite` 技能

## 执行流程

### 阶段一：发布快手

读取技能文件：
```
C:\Users\admin\.qclaw\workspace\skills\post-kuaishou-short-videos-infinite\SKILL.md
```

按该技能文档的完整流程执行：
1. 启动 OpenClaw 浏览器
2. 导航到快手上传页面
3. 上传视频文件
4. 填写视频信息（标题 + 概述 + 标签，注意快手最多 4 个标签，每个标签需在下拉框确认）
5. 设置 PK 封面（开关 → 点击封面按钮 → 确认）
6. 添加作者声明（内容为 AI 生成）
7. 取消允许下载权限
8. 点击发布

### 阶段二：发布抖音

**等快手发布完全结束后**，读取技能文件：
```
C:\Users\admin\.qclaw\workspace\skills\post-tiktok-short-videos-infinite\SKILL.md
```

按该技能文档的完整流程执行：
1. 启动 OpenClaw 浏览器（复用，直接 navigate）
2. 导航到抖音上传页面
3. 上传视频文件
4. 填写标题、简介，追加话题/标签（每个标签需在下拉框确认）
5. 设置封面（选择封面 → 设置横封面 → 完成）
6. 选择合集
7. 设置权限（不允许）
8. 添加内容声明（内容由AI生成）
9. 点击暂存离开

### 阶段三：发布小红书

**等抖音发布完全结束后**，读取技能文件：
```
C:\Users\admin\.qclaw\workspace\skills\publish-xhs-short-videos-infinite\SKILL.md
```

按该技能文档的完整流程执行：
1. 启动 OpenClaw 浏览器（复用，直接 navigate）
2. 导航到小红书上传页面
3. 上传视频文件
4. 填写标题和正文描述，追加话题/标签（每个标签需在下拉框确认）
5. 添加合集（有则选，无则创建）
6. 声明原创（打开开关 → 勾选同意 → 点击声明原创）
7. 添加内容类型声明（笔记含AI合成内容）
8. 选择群聊（未来科技1群）
9. 点击暂存离开

## 关键注意事项

- **顺序严格**：快手 → 抖音 → 小红书，必须前一个平台完成后再开始下一个
- **复用浏览器**：每个平台完成后浏览器保持运行，直接用 navigate 导航到下一个平台
- **视频文件路径**：三个平台使用同一个视频文件，路径仅需解析一次
- **快手标签上限**：快手最多 4 个标签，超出部分必须删除
- **抖音暂存而非发布**：抖音最后点击"暂存离开"而非"发布"
- **小红书暂存而非发布**：小红书最后点击"暂存离开"而非"发布"，**严禁点击发布**
- **小红书合集逻辑**：下拉框有目标合集直接选，没有则创建新合集
- **小红书原创声明三步法**：打开开关 → 勾选"我已阅读并同意" → 点击"声明原创"

## 子技能文件路径

- 快手技能：`C:\Users\admin\.qclaw\workspace\skills\post-kuaishou-short-videos-infinite\SKILL.md`
- 抖音技能：`C:\Users\admin\.qclaw\workspace\skills\post-tiktok-short-videos-infinite\SKILL.md`
- 小红书技能：`C:\Users\admin\.qclaw\workspace\skills\publish-xhs-short-videos-infinite\SKILL.md`
