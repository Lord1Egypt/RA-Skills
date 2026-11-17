# 写作元数据规范（M.元数据桥接师核心规范）

> 所有角色间的信息传递必须经过 M 标准化，确保格式统一、字段可解析。

---

## 一、全局字段

每个经 M 标准化的产出物必须包含以下头部：

```yaml
---
doc_id: {角色缩写}_{流水号}        # 如 topic_001, material_001
session_id: {会话标识}              # 当前写作会话唯一ID
created_at: {ISO8601时间戳}
created_by: {角色名称}
pipeline_step: {当前步骤序号}       # 1-10 对应管道步骤
status: draft | reviewed | final
---
```

---

## 二、各角色产出数据结构

### 1. 风格编码（刘风格 → style）← P0升级：6维写作画像

```yaml
style_id: style_{流水号}
profile_name: default | professional | narrative | short   # 画像名称，支持多画像
created_at: {ISO8601时间戳}
source_articles:
  - title: {文章标题}
    word_count: {字数}
    file_path: {文件路径（如有）}

# 维度1：人称视角维
person: {第一人称|第二人称|第三人称}
reader_address: {读者称呼习惯，如"你"/"您"/"各位"}
narrative_perspective: {视角描述}

# 维度2：句式节奏维
avg_sentence_length: {数字}       # 平均句长（字）
sentence_rhythm: {短句为主|长短交替|长句为主}
paragraph_length: {单段平均行数}
rhythm_feature: {节奏特征描述}

# 维度3：词汇偏好维
vocab_profile: [{高频词1}, {高频词2}]
banned_words: [{禁用词1}, {禁用词2}]
jargon_density: low | medium | high   # 术语密度
oral_feature: {口语特征描述}

# 维度4：情绪基调维
emotion_baseline: {情绪基调描述}
tone_temperature: {0-1}            # 0冷酷 - 1温暖
empathy_style: {共情方式描述}
emotion_curve: [{开头情绪}, {中间情绪}, {结尾情绪}]

# 维度5：修辞风格维
rhetoric_preference: [{修辞手法1}, {修辞手法2}]
golden_sentence_density: {每N字1个}
hook_type: {开头钩子类型}
ending_pattern: {结尾行动点套路}

# 维度6：结构习惯维
structure_habit: {结构习惯描述}
hook_type: {提问式|场景式|数据式|故事式}
transition_words: [{过渡词1}, {过渡词2}]
ending_cta: {结尾行动点习惯}
```

### 2. 选题对象（赵选题 → topic）

```yaml
topic_id: topic_{流水号}
items:
  - title: {标题示例}
    angle: {核心切入点}
    pain_point: {共鸣点}
    potential: high | medium | low
    potential_reason: {理由}
    target_audience: {目标受众描述}
```

### 3. 素材对象（张素材 → material）

```yaml
material_id: material_{流水号}
topic_id: {关联选题ID}
items:
  - type: case | data | story
    content: {素材内容}
    credibility: high | medium | low
    source: {出处}
    source_type: authoritative | media | anecdotal
    freshness: {时效描述}
    suggested_position: {建议使用位置}
```

### 4. 逻辑框架（王整理 → framework）

```yaml
framework_id: framework_{流水号}
topic_id: {关联选题ID}
material_id: {关联素材ID}
main_thesis: {总论点}
sub_theses:
  - id: sub_{序号}
    point: {分论点}
    evidence_refs: [{论据引用}]       # 指向素材ID
    position: {在文中的位置}
reader_questions:
  - after: {在哪个分论点之后}
    question: {预判读者疑问}
    resolution_needed: {需要补充的内容}
gaps:
  - description: {待补充项描述}
    priority: must | should | nice
```

### 5. 文章初稿（李文章 → draft）

```yaml
draft_id: draft_{流水号}
framework_id: {关联框架ID}
material_id: {关联素材ID}
style_id: {关联风格ID}
title: {暂定标题}
word_count: {字数}
body: |
  {正文内容，纯文本}
```

### 6. 核查报告（吴查查 → factcheck）

```yaml
factcheck_id: factcheck_{流水号}
draft_id: {关联初稿ID}
items:
  - claim: {被核查的信息点}
    quote: {原文引用}
    verdict: green | yellow | red      # 绿灯/黄灯/红灯
    source_check: pass | uncertain | fail
    timeliness_check: current | outdated | unknown
    logic_check: valid | questionable | invalid
    suggestion: {替换建议，红灯必填}
summary:
  green_count: {绿灯数}
  yellow_count: {黄灯数}
  red_count: {红灯数}
  overall_assessment: pass | conditional | fail
```

### 7. 编辑优化单 + 法眼金线品控报告（周审稿 → editplan）← P1升级

```yaml
# 编辑优化单（原有）
editplan_id: editplan_{流水号}
draft_id: {关联初稿ID}
factcheck_id: {关联核查ID}
items:
  - priority: must | suggest | killer   # 必改/建议/杀手锏
    category: title | hook | structure | golden_sentence | ending | other
    location: {修改位置}
    current: {当前内容}
    replacement: {替代方案}
    reason: {修改理由}

# 法眼金线品控报告（P1新增）
goldenline_report_id: goldenline_{流水号}
editplan_id: {关联优化单ID}
draft_id: {关联初稿ID}

golden_lines:
  - line_id: GL1
    name: 法条引用准确线
    result: pass | borderline | fail
    details: {具体说明，如不达标则填写修改建议}
  - line_id: GL2
    name: 案例真实可查线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL3
    name: 风险告知充分线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL4
    name: 语言通俗转化线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL5
    name: 实操步骤可执行线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL6
    name: 标题3秒吸引线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL7
    name: 开头共情钩子线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL8
    name: 金句传播力线
    result: pass | borderline | fail
    details: {具体说明}
  - line_id: GL9
    name: 结尾行动点明确线
    result: pass | borderline | fail
    details: {具体说明}

overall_assessment: pass | conditional | fail
must_fix_count: {必改项数（fail项数）}
suggest_fix_count: {建议修改项数（borderline项数）}
```

### 8. 排版指令 + 多格式导出（陈排版 → layout）← P1升级

```yaml
# 排版指令（原有）
layout_id: layout_{流水号}
draft_id: {关联初稿ID}
platform: wechat | xiaohongshu | zhihu | weibo | toutiao | custom
layout_instructions:
  cover: {封面建议}
  font_size: {字号}
  line_height: {行距}
  color_scheme: {配色方案}
  image_suggestions: [{配图建议}]
visual_outline: |
  {视觉化提纲，含空行、分割线、Emoji、加粗、引用块等}

# 多格式导出（P1新增）
export_id: export_{流水号}
layout_id: {关联排版ID}
draft_id: {关联初稿ID}

exports:
  - format: wechat-html | xiaohongshu-image | ppt | long-image | markdown
    file_path: {导出文件路径}
    generated_at: {生成时间}
    status: success | failed
    image_count: {图片数量，仅xiaohongshu-image格式}
    ppt_slide_count: {PPT页数，仅ppt格式}
```

**导出文件存储规范**：
```
writing-team/shared/artifacts/exports/
├── xiaohongshu_images/    # 小红书3:4图片
│   ├── img_01.png
│   ├── img_02.png
│   └── ...
├── ppt/                    # PPT文件
│   └── article_001.pptx
└── long_images/            # 长图文件
    └── article_001_long.png
```

### 9. 知识库笔记（王整理 → knowledge-base）← P0新增

```yaml
kb_id: kb_{流水号}
source: ima | weixin-yuedu | yinxiang | public-article | local-markdown
title: {笔记/文章标题}
tags: [{标签1}, {标签2}]
imported_at: {ISO8601时间戳}
file_path: {存储路径}
abstract: {内容摘要，≤200字}
content_format: markdown | txt | html
parsed_sections:          # 解析后的结构
  - section_title: {段落标题}
    content: {段落内容}
    is_key_point: true | false   # 是否重点
    linked_topics: [{关联主题1}, {关联主题2}]   # 可关联到选题
```

---

## 三、管道状态快照

每次角色完成后，M 更新此文件：

```yaml
# writing-team/shared/pipeline-state.yaml
session_id: {会话ID}
current_step: {当前步骤序号}
steps:
  - step: 1
    role: 刘风格
    status: pending | in_progress | done | failed | skipped
    doc_id: {产出物ID}
    started_at: {时间}
    completed_at: {时间}
  - step: 2
    role: 赵选题
    status: ...
  # ... 依次类推
retry_count: {当前步骤重试次数}
notes: {备注}
```

---

## 四、M 桥接操作规范

1. **输入**：角色原始输出（纯文本/YAML混合）
2. **操作**：
   - 解析输出，提取结构化字段
   - 注入全局头部（doc_id, session_id, created_at 等）
   - 建立与上游产出物的引用关系（如 draft → framework → material → topic）
   - 缓存跨角色共用数据（如 style 编码、logic framework）
3. **输出**：标准化后的 YAML 文档，写入 `writing-team/shared/artifacts/`
4. **文件命名**：`{doc_id}.yaml`，如 `topic_001.yaml`、`draft_001.yaml`
