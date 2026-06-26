---
name: xiaohongshu-longpost-auto
description: When users have long-form content ready to publish on Xiaohongshu, automatically completes the entire process: login detection, long content segmentation optimization, AI-generated images, content filling, AI-generated tags, tag activation, original content declaration, and publishing.
---

# Xiaohongshu Automatic Long-Form Post Publishing

## Feature Overview

When users have long-form content ready to publish on Xiaohongshu, automatically completes the entire process: login detection, long content segmentation optimization, AI-generated images, content filling, AI-generated tags, tag activation, original content declaration, and publishing. Only QR code login requires manual operation; all other steps are fully automated.

## Trigger Conditions

Trigger this skill when the user mentions any of the following keywords:

- Xiaohongshu long-form post publishing
- Publish Xiaohongshu long-form post
- Automatically publish Xiaohongshu long-form post
- Xiaohongshu long-form notes
- Xiaohongshu article publishing
- 小红书长文发布
- 发布小红书长文
- 自动发小红书长文
- 小红书长文笔记
- 小红书文章发布

## Use Cases

- Users have existing long-form note content ready to publish on Xiaohongshu

## 🔄 Workflow

```
1. Content Preprocessing → 2. Login Detection → 3. Enter Publishing Page → 4. Fill Content → 
5. One-Click Formatting → 6. Select Template → 7. Generate Description → 8. Add Tags → 
9. Declare Original → 10. Publish
```

## Step-by-Step Guide

### 1️⃣ Content Preprocessing

**Segmentation Principles:**
- 300-500 characters per paragraph to maintain reading rhythm
- Add subheadings for easy browsing
- Front-load key information; present core points at the beginning of each paragraph
- Appropriate spacing with blank lines between paragraphs
- Moderate use of emojis ✨💡

**Content Structure:**
```
Opening Hook (50-100 chars) → Spark curiosity or resonate
Body Paragraphs (300-500 chars each) → Problem/Background → Analysis/Methods → Cases/Experience → Summary/Suggestions
Closing Interaction (50 chars) → Encourage comments or saves
```

### 2️⃣ Login Detection

**Visit:** `https://creator.xiaohongshu.com/`

| Status | Action |
|------|------|
| Logged in | Directly enter publishing page |
| Not logged in | Prompt user to scan QR code, wait for completion |

**Technical Implementation:**
```javascript
// Detect login status
browser.navigate('https://creator.xiaohongshu.com/')
// If redirected to /login page, not logged in
```

### 3️⃣ Enter Publishing Page

**Visit:** `https://creator.xiaohongshu.com/publish/publish`

**Operation Steps:**
1. Navigate to the publishing page
2. Click the **"Write Long-Form Post"** button
3. Click **"New Creation"** to enter the editor

**Technical Implementation:**
```javascript
browser.navigate('https://creator.xiaohongshu.com/publish/publish')
browser.snapshot() // Get page elements
browser.act({ kind: 'click', ref: 'e111' }) // Click "Write Long-Form Post"
browser.act({ kind: 'click', ref: 'e148' }) // Click "New Creation"
```

### 4️⃣ Fill Content

| Field | Requirements |
|------|------|
| Title | ≤20 characters, containing 1-2 keywords |
| Body Text | Paste preprocessed content |

**Technical Implementation:**
```javascript
// Fill title
browser.act({ kind: 'type', ref: 'e253', text: 'Title content' })

// Fill body text (inject using evaluate)
browser.act({
  kind: 'evaluate',
  fn: "() => { const editor = document.querySelector('[contenteditable]'); editor.textContent = 'Body content'; editor.dispatchEvent(new InputEvent('input', {bubbles: true})); return 'done'; }"
})
```

### 5️⃣ One-Click Formatting

Click the **"One-Click Formatting"** button; the system automatically optimizes the format.

**Technical Implementation:**
```javascript
browser.act({ kind: 'click', ref: 'e260' }) // Click "One-Click Formatting"
```

### 6️⃣ Select Template

| Template Type | Applicable Scenarios |
|----------|----------|
| Fresh Minimalist | Lifestyle sharing, reading notes |
| Workplace Expertise | Experience summaries, skill sharing |
| Vibrant Fashion | Beauty/fashion, trending topics |
| Warm Healing | Emotional stories, inspirational content |
| Professional Rigorous | Educational content, tutorials, guides |
| Logical Structure | Tech news, industry analysis |
| Simple Basic | General content |

> **Principle:** Choose based on content theme and target audience
> **Recommendation:** For tech/workplace content, select "Logical Structure" or "Workplace Expertise"

**Technical Implementation:**
```javascript
browser.act({ kind: 'click', ref: 'e334' }) // Click "Logical Structure" template
browser.act({ kind: 'click', ref: 'e647' }) // Click "Next"
```

### 7️⃣ Generate Body Description

**Optimization Principles:**

| Element | Requirements |
|------|------|
| Length | 50-100 characters |
| Content | Summarize core points or highlights |
| Tone | Conversational, friendly |
| Hook | Create suspense or highlight pain points at the beginning |
| Keywords | Include 1-2 search keywords |

**Example:**
- ❌ "This article introduces several methods for time management"
- ✅ "Same 24 hours, why can others get 3 times the work done? These 5 time management techniques doubled my productivity, number 3 is truly amazing!"

**Technical Implementation:**
```javascript
browser.act({ kind: 'type', ref: 'e706', text: 'Description content' })
```

### 8️⃣ Add Tags

**Tag Structure (5-8 total):**

| Type | Quantity | Example |
|------|------|------|
| Core Tags | 1-2 | #WorkplaceExpertise #LearningMethods |
| Niche Tags | 2-3 | #TimeManagement #Productivity |
| Popular Tags | 1-2 | #OfficeWorkers #Students |
| Long-Tail Tags | 1-2 | #PomodoroTechnique #MorningJournal |

**Checklist:**
- ✅ 5-8 tags total
- ✅ Highly relevant to content
- ✅ Balanced popularity (high traffic + precise)

**Technical Implementation:**
```javascript
browser.act({ kind: 'click', ref: 'e723' }) // Click "Topic" button
browser.act({ kind: 'click', ref: 'e1033' }) // Click recommended tag "#ArtificialIntelligence"
browser.act({ kind: 'click', ref: 'e712' }) // Click recommended tag "#LargeLanguageModels"
```

### 9️⃣ Declare Original

**Operation Steps:**
1. Check the **"Original Content Declaration"** checkbox
2. In the pop-up, check **"I have read and agree"**
3. Click the **"Declare Original"** button

**Technical Implementation:**
```javascript
browser.act({ kind: 'click', ref: 'e806' }) // Check original declaration
browser.act({ kind: 'click', ref: 'e1083' }) // Check agreement box
browser.act({ kind: 'click', ref: 'e1088' }) // Click "Declare Original"
```

### 🔟 Publish

**Pre-Publishing Checklist:**
- [ ] Title complete and engaging (≤20 characters)
- [ ] Body text formatting looks good
- [ ] Body description engaging (50-100 characters)
- [ ] Tags activated (5-8 tags)
- [ ] Original declaration checked

**Technical Implementation:**
```javascript
browser.act({ kind: 'click', ref: 'e1013' }) // Click "Publish"
```

**Publication Success Indicators:**
- Page displays green checkmark ✅
- Displays "Published Successfully" text
- Automatically returns to homepage after 3 seconds

## ⚠️ Important Notes

| Item | Description |
|------|------|
| Content Compliance | Must comply with Xiaohongshu community guidelines; avoid sensitive words |
| Image Copyright | AI-generated images should avoid copyright risks |
| Publishing Frequency | Avoid publishing too frequently in a short period (recommended interval > 1 hour) |
| Engagement Maintenance | Monitor comments after publishing and respond promptly |
| Title Length | Strictly control within 20 characters; otherwise cannot publish |
| Tag Count | Minimum 3, maximum 8, recommended 5-6 |

---

## 🛠️ Error Handling

| Error Scenario | Handling Method |
|----------|----------|
| Login expired | Prompt user to scan QR code again; wait for completion and continue |
| Element not found | Re-snapshot to get latest ref, retry up to 3 times |
| Content injection failed | Check contenteditable element, activate using focus()+click() |
| Image upload failed | Retry up to 3 times; if still failing, skip that image |
| Content moderation prompt | Prompt user to modify sensitive content |
| Publishing frequency limit | Prompt user to wait before retrying (typically 1-24 hours) |
| Title too long | Automatically truncate or have AI regenerate a shorter title |

**Debugging Tips:**
```javascript
// 1. Screenshot to confirm current page status
browser.screenshot({ fullPage: true })

// 2. Get latest element references
browser.snapshot({ refs: 'aria' })

// 3. Check if editor is editable
browser.act({ fn: "document.querySelector('[contenteditable]').isContentEditable" })
```

---

## 🔧 Technical Details

### Browser Automation Essentials

**1. Element Locating:**
- Use `refs: 'aria'` to obtain stable aria-ref locators
- Avoid using unstable XPath or CSS selectors

**2. Content Injection:**
```javascript
// Recommended method: Use evaluate + dispatchEvent
browser.act({
  kind: 'evaluate',
  fn: "() => {
    const editor = document.querySelector('[contenteditable]');
    editor.textContent = 'Content';
    editor.dispatchEvent(new InputEvent('input', { bubbles: true }));
    return 'done';
  }"
})
```

**3. Waiting Strategy:**
- Wait 500-1000ms after clicks to allow page to respond
- Use snapshot to confirm element state before proceeding

## 🔗 Reference Documentation

- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com/)
- [Xiaohongshu Community Guidelines](https://www.xiaohongshu.com/community_guidelines)
- [Xiaohongshu Long-Form Post Guide](https://creator.xiaohongshu.com/help)