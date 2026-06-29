# PPT 生产 Subagent 协作协议 v1

## 总控：main / zm-ppt-deck-production-workflow

职责：
- 接收需求；
- 锁定内容大纲；
- 生成页面生产合同；
- 分派视觉、组装、审核任务；
- 判断 DONE / BLOCKED；
- 维护交付包和最终记录。

总控不直接生图，不直接替代专职 agent 做正式视觉。

---

## 1. content-architect

### 输入

- requirement.md
- 用户素材说明
- 历史成功案例
- PPT 制作标准

### 输出

- content_outline.md
- slide_contracts.md
- asset_manifest.md

### 质量门槛

- 每页有且只有一个核心认知；
- 页码、标题、副标题、主旨、核心结论齐全；
- 明确哪些内容进入页面，哪些由讲师口述；
- 明确真实素材与生图素材边界。

---

## 2. visual-producer / media-director

### 输入

- slide_contracts.md
- visual_brief_for_media_director.md
- real asset list
- style standard

### 输出

- 页面源图 P01.png ...
- prompts/
- generation_manifest.json
- failed_pages.md（如有）

### 禁止

- 不生成 Logo；
- 不生成页脚；
- 不生成页码；
- 不生成 Part 标签；
- 不生成二维码；
- 不伪造真实产品界面、真实人物、真实数据。

### 返工规则

主体画面出错，重新生成完整页面源图，不做局部贴片补丁。

---

## 3. ppt-assembler

### 输入

- 页面源图；
- Logo / 二维码 / 真实素材；
- post-process standard；
- page order；
- footer/page number rules。

### 输出

- final_high_quality.pptx
- final_archive_original.pptx
- renders/pages_png/
- assembly_manifest.json

### 职责

- 按页放入完整页面源图；
- 统一添加 Logo；
- 统一添加 Part 标签；
- 统一添加页脚与页码；
- 不修改主体页面视觉逻辑。

---

## 4. render-auditor

### 输入

- final_high_quality.pptx
- content_outline.md
- slide_contracts.md
- final_review_checklist.md

### 输出

- render_audit.md
- issue_list.md
- final_acceptance.md

### 审核范围

- 内容顺序；
- 标题与核心结论；
- Logo、Part、页脚、页码；
- 同构页一致性；
- 锯齿、模糊、遮挡；
- 内部制作说明、占位符、调试语；
- 交付包结构。

---

## 协作状态定义

- TODO：未开始；
- IN_PROGRESS：执行中；
- NEEDS_FIX：已产出但需返工；
- BLOCKED：缺素材/权限/工具；
- PASS：通过本层审核；
- DONE：总控验收完成。
