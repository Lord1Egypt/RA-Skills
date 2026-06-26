---
name: super-lobster
description: |
  🦞 Super Lobster | 超级龙虾 - 桥哥的私人 AI 助理
  
  整合了飞书文档管理、会议纪要整理、每日待办推送、工作模块分类等核心技能。
  能够自动读取会议纪要、按工作模块分类整理待办事项、创建飞书文档并推送。
  
  核心能力：
  - 📄 飞书文档创建（支持 100+ blocks 大文档）
  - 📋 会议纪要自动整理
  - ✅ 每日待办推送（按工作模块分类）
  - 🔐 飞书权限自动设置
  - 📊 工作模块智能分类
  - ⏰ 定时任务执行
  
author: 龙虾仔
version: 1.0.0
tags: [feishu, productivity, todo, meeting-notes, automation]
---

# 🦞 Super Lobster | 超级龙虾

**桥哥的私人 AI 助理** - 整合所有核心工作技能

---

## 🎯 核心能力

### 1. 📄 飞书文档创建（大文档支持）

使用正确的 API 参数创建包含 100+ blocks 的飞书文档：

```javascript
const insertRes = await client.docx.documentBlockDescendant.create({
  path: {
    document_id: docToken,
    block_id: docToken
  },
  data: {
    children_id: firstLevelBlockIds,  // ← 关键参数！
    descendants: descendants,
    index: -1  // ← 关键参数！
  }
});
```

**关键点**：
- 必须包含 `children_id: firstLevelBlockIds`
- 必须包含 `index: -1`
- 支持 100+ blocks 大文档

### 2. 📋 会议纪要自动整理

自动读取飞书会议纪要文档，提取所有待办事项：

```javascript
const readRes = await client.docx.document.rawContent.get({
  path: { document_id: docToken }
});
```

**支持的会议类型**：
- AI 盒子及 NAS 应用会议
- AI 业务出海及品牌打造规划会议
- 工作规划与项目推进会议
- 门店 C 端 AI 会员体系搭建会议
- 出海业务 KR 拉齐会
- 商务与科创项目推进会议

### 3. ✅ 每日待办推送（按工作模块分类）

按工作模块分类整理待办事项：

**六大工作模块**：
1. 🔥 紧急待办（48 小时内）
2. 一、政府项目申报
3. 二、产品研发（NAS 龙虾+AI 盒子）
4. 三、出海业务
5. 四、门店运营
6. 五、团队建设

### 4. 🔐 飞书权限自动设置

```javascript
const permRes = await client.drive.permissionMember.create({
  path: { token: docToken },
  params: {
    type: 'docx',  // ← URL 查询参数
    need_notification: true
  },
  data: {
    member_type: 'openid',
    member_id: USER_OPEN_ID,
    perm: 'edit'
  }
});
```

### 5. 📊 工作模块智能分类

自动将待办事项按以下维度分类：
- **紧急程度**：明天截止、后天截止、今日到期、逾期
- **工作模块**：政府项目、产品研发、出海业务、门店运营、团队建设
- **负责人**：桥哥、团队、具体人员

### 6. ⏰ 定时任务执行

支持 cron 定时任务：
- **8:30 AM** - 每日待办推送（早上）
- **5:30 PM** - 每日待办推送（下午）
- **心跳检查** - 每 2 小时检查 AI 突破性事件

---

## 🚀 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/[your-repo]/super-lobster.git
```

### 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "agents": [
    {
      "agentId": "super-lobster",
      "match": {
        "channel": "feishu",
        "accountId": "main"
      }
    }
  ]
}
```

### 使用

#### 方式 1: 手动触发

```bash
openclaw agent -m "创建今日待办文档" --agent super-lobster
```

#### 方式 2: 定时任务

在 `~/.openclaw/cron/jobs.json` 中添加：

```json
{
  "name": "每日待办推送",
  "schedule": "30 8 * * *",
  "timezone": "Asia/Shanghai",
  "agentId": "super-lobster",
  "message": "创建今日待办文档"
}
```

#### 方式 3: 心跳触发

在 `~/.openclaw/workspace/HEARTBEAT.md` 中添加：

```markdown
## 🦞 超级龙虾任务

每次心跳检查：
- [ ] 读取新会议纪要
- [ ] 更新每日待办
- [ ] 推送紧急事项
```

---

## 📁 文件结构

```
super-lobster/
├── SKILL.md                          # 技能说明
├── _meta.json                        # 元数据
├── scripts/
│   ├── create_daily_todo.mjs         # 创建待办文档
│   ├── read_meeting_notes.mjs        # 读取会议纪要
│   └── classify_by_module.mjs        # 按模块分类
├── templates/
│   ├── daily_todo_template.md        # 待办文档模板
│   └── meeting_summary_template.md   # 会议纪要模板
└── memory/
    ├── skill-super-lobster.md        # 技能详细说明
    └── heartbeat-state.json          # 心跳状态
```

---

## 🔧 API 参数详解

### 创建文档

```javascript
const createRes = await client.docx.document.create({
  data: {
    title: `🦞 每日待办 2026.4.6（工作模块版）`
  }
});
```

### 转换 Markdown

```javascript
const convertRes = await client.docx.document.convert({
  data: {
    content_type: 'markdown',
    content: markdownContent
  }
});
```

### 清理 Blocks

```javascript
function omitParentId(block) {
  const { parent_id, ...rest } = block;
  return rest;
}

const descendants = blocks.map(block => {
  const cleanBlock = omitParentId(block);
  return {
    ...(cleanBlock.block_id ? { block_id: cleanBlock.block_id } : {}),
    ...cleanBlock
  };
});
```

### 插入 Blocks

```javascript
const insertRes = await client.docx.documentBlockDescendant.create({
  path: {
    document_id: docToken,
    block_id: docToken
  },
  data: {
    children_id: firstLevelBlockIds,  // 必须！
    descendants: descendants,
    index: -1  // 必须！
  }
});
```

### 设置权限

```javascript
const permRes = await client.drive.permissionMember.create({
  path: { token: docToken },
  params: {
    type: 'docx',
    need_notification: true
  },
  data: {
    member_type: 'openid',
    member_id: USER_OPEN_ID,
    perm: 'edit'
  }
});
```

---

## 📊 待办文档模板

```markdown
# 🦞 每日待办 2026.4.6

## 🔥 紧急待办

### 明天（4/7）截止

- [ ] 事项 1 → 负责人
- [ ] 事项 2 → 负责人

### 今日到期

- [ ] 事项 3 → 负责人

---

## 一、政府项目申报

- [ ] 事项 → 负责人
- [ ] 事项 → 负责人

---

## 二、产品研发

### P0 任务

- [ ] 事项 → 负责人

### 逾期事项

- [ ] 事项 → 负责人

### 持续跟进

- [ ] 事项 → 负责人

---

## 三、出海业务

- [ ] 事项 → 负责人

---

## 四、门店运营

- [ ] 事项 → 负责人

---

## 五、团队建设

- [ ] 事项 → 负责人

---

## 六、5-12 月里程碑

| 月份 | 目标 |
|------|------|
| 4 月 | 硬件方案确定 + 原型验证 |
| 5 月 | 软件打磨 + 种子用户内测 |
| 6 月 | 小批量生产 |
| 7-9 月 | 产品正式发布 |
| 10-12 月 | 规模化 + 出海 |

---

**整理人**: 龙虾仔 🦞
```

---

## ⚠️ 常见错误

| 错误 | 正确做法 |
|------|---------|
| ❌ 缺少 `children_id` 参数 | ✅ 必须包含 `children_id: firstLevelBlockIds` |
| ❌ 缺少 `index` 参数 | ✅ 必须包含 `index: -1` |
| ❌ 用 `client.docx.permission.member.add` | ✅ 用 `client.drive.permissionMember.create` |
| ❌ 权限参数用 `member_type: 'user'` | ✅ 用 `member_type: 'openid'` |
| ❌ 按会议来源分类 | ✅ 按工作模块分类 |

---

## 💡 最佳实践

1. **先读取所有会议纪要** - 确保不遗漏任何事项
2. **按工作模块分类** - 不按会议来源分类
3. **标注紧急程度** - 明天/后天/今日/逾期
4. **标注负责人** - 每个事项都要有明确负责人
5. **设置飞书权限** - 确保用户可以编辑
6. **推送文档链接** - 飞书消息通知

---

## 🔄 版本历史

### v1.0.0 (2026-04-06)
- ✅ 飞书文档创建（支持 100+ blocks）
- ✅ 会议纪要自动整理
- ✅ 按工作模块分类
- ✅ 飞书权限自动设置
- ✅ 定时任务支持

---

## 📞 联系

- **作者**: 龙虾仔 🦞
- **用户**: 桥哥
- **工作目录**: `~/.openclaw/workspace`
- **技能目录**: `~/.openclaw/workspace/skills/super-lobster`

---

**Super Lobster - 桥哥的最强 AI 助理！** 🦞
