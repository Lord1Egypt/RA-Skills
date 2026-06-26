# 六维要素提取与七步循环法模板

## 目录
1. [六维要素提取模板](#六维要素提取模板)
2. [七步循环法模板](#七步循环法模板)
3. [多循环设计与篇幅策略](#多循环设计与篇幅策略)

## 六维要素提取模板

从3-6本原始小说中，每本提取一个维度的核心要素。以下是6个维度的提取模板。

### 维度1：故事框架提取

提取维度：
| 维度 | 说明 |
|------|------|
| 核心主线 | 一句话概括主线剧情 |
| 剧情结构 | 起承转合的关键节点 |
| 核心冲突 | 推动剧情的核心矛盾 |
| 爽点设计 | 爽点的类型和分布 |
| 节奏控制 | 快节奏/慢节奏的分布 |

输出格式：
```yaml
story_framework:
  source_novel: "小说A"
  main_plot: "..."
  plot_structure:
    inciting_incident: "..."
    rising_action: "..."
    climax: "..."
    resolution: "..."
  core_conflict: "..."
  satisfaction_points:
    - type: "..."
      position: "..."
      description: "..."
  pacing:
    fast_sections: "..."
    slow_sections: "..."
  reusable_elements: [...]
  elements_to_adjust: [...]
```

### 维度2：人物构建提取

提取维度：
| 维度 | 说明 |
|------|------|
| 主角人设 | 表面身份/真实身份/核心能力/性格特点 |
| 成长弧光 | 主角从开始到结束的变化 |
| 反派设计 | 反派身份/动机/与主角关系 |
| 配角体系 | 主要配角及其作用 |
| 人物关系 | 核心人物关系网 |

输出格式：
```yaml
character_construction:
  source_novel: "小说B"
  protagonist:
    surface_identity: "..."
    true_identity: "..."
    core_ability: "..."
    personality_traits: [...]
    background_story: "..."
    growth_arc: "..."
  antagonist:
    identity: "..."
    motivation: "..."
    relationship_with_protagonist: "..."
  supporting_characters:
    - name: "..."
      role: "..."
      relationship: "..."
  character_relationships:
    - character_a: "..."
      character_b: "..."
      relationship_type: "..."
  reusable_elements: [...]
  elements_to_adjust: [...]
```

### 维度3：情绪曲线提取

提取维度：
| 维度 | 说明 |
|------|------|
| 情绪基调 | 整体情绪氛围 |
| 情绪高潮 | 情绪最高点的设计 |
| 情绪低谷 | 压抑、挫折的设计 |
| 情绪节奏 | 高低起伏的分布 |
| 情绪释放 | 爽点、泪点、笑点的分布 |

输出格式：
```yaml
emotional_curve:
  source_novel: "小说C"
  emotional_tone: "..."
  emotional_peaks:
    - position: "..."
      type: "爽点/泪点/笑点"
      description: "..."
  emotional_valleys:
    - position: "..."
      type: "压抑/挫折"
      description: "..."
  emotional_rhythm:
    pattern: "..."
    distribution: "..."
  emotional_releases:
    satisfaction_points: "..."
    tear_points: "..."
    laugh_points: "..."
  reusable_elements: [...]
  elements_to_adjust: [...]
```

### 维度4：文风特征提取

提取维度：
| 维度 | 说明 |
|------|------|
| 语言风格 | 口语化/书面语/古风/现代 |
| 句式特点 | 长句/短句/对话占比 |
| 描写手法 | 动作/心理/环境描写的比例 |
| 节奏感 | 文风节奏的快慢 |
| 特色表达 | 独特的语言习惯或表达方式 |

输出格式：
```yaml
writing_style:
  source_novel: "小说D"
  language_style:
    formality: "口语化/书面语/古风/现代"
    vocabulary_preference: "..."
  sentence_structure:
    length_preference: "短句/中长句/长短结合"
    dialogue_ratio: "..."
  description_techniques:
    focus: "动作/心理/环境/对话"
    density: "简洁/中等/丰富"
  rhythm:
    overall_pace: "快节奏/中节奏/慢节奏"
    variation: "平稳/起伏/快慢交替"
  unique_expressions: [...]
  reusable_elements: [...]
  elements_to_adjust: [...]
```

### 维度5：金手指设计提取

提取维度：
| 维度 | 说明 |
|------|------|
| 金手指类型 | 系统/重生/异能/空间等 |
| 功能设计 | 金手指的具体功能 |
| 成长路线 | 金手指如何成长 |
| 限制条件 | 金手指的限制和代价 |
| 爽点来源 | 金手指带来的爽点 |

输出格式：
```yaml
golden_finger:
  source_novel: "小说E"
  type: "系统/重生/异能/空间/其他"
  functions: [...]
  growth_path:
    stages:
      - stage: "..."
        ability: "..."
  limitations: [...]
  costs: [...]
  satisfaction_sources: [...]
  reusable_elements: [...]
  elements_to_adjust: [...]
```

### 维度6：世界观设定提取

提取维度：
| 维度 | 说明 |
|------|------|
| 世界背景 | 时代/社会/规则 |
| 力量体系 | 修炼等级/能力体系 |
| 组织架构 | 宗门/家族/势力 |
| 特殊规则 | 世界的特殊设定 |
| 核心矛盾 | 世界观中的核心冲突 |

输出格式：
```yaml
world_building:
  source_novel: "小说F"
  background:
    era: "..."
    society: "..."
    rules: "..."
  power_system:
    levels: [...]
    abilities: [...]
  organizations:
    - name: "..."
      type: "宗门/家族/势力"
      description: "..."
  special_rules: [...]
  core_conflicts: [...]
  reusable_elements: [...]
  elements_to_adjust: [...]
```

## 七步循环法模板

七步循环法是一个**故事单元**的结构，不是全书大纲。一个故事单元通常包含3-10章，一个完整的长篇小说由多个故事单元组成。

### 第1步：展示优势（1-2章）
- 场景：主角面对一个看似困难的情况
- 行动：主角用独特方式轻松解决
- 反应：周围人惊讶/不解
- 效果：读者期待主角后续表现

### 第2步：制造信息差（1-2章）
- 场景A：主角发现了某个秘密
- 场景B：反派在暗中策划
- 场景C：读者知道双方都不知道的信息
- 效果：读者期待信息揭露时的冲突

### 第3步：第一次摩擦（1-2章）
- 触发：反派挑衅/意外事件
- 对抗：主角与反派正面交锋
- 受挫：主角发现反派比想象中强大
- 效果：读者为主角担心

### 第4步：不看好（1章）
- 场景A：朋友劝主角放弃
- 场景B：反派公开嘲讽
- 场景C：主角沉默/微笑/不回应
- 效果：读者情绪被压抑，期待释放

### 第5步：最终冲突爆杀（1-2章）
- 场景：最终对决
- 爆发：主角使用隐藏的底牌/能力
- 解决：反派被彻底击败
- 效果：读者大呼过瘾

### 第6步：震惊（1章）
- 场景A：旁观者震惊的反应
- 场景B：反派难以置信
- 场景C：主角盘点收获
- 效果：满足读者的爽感

### 第7步：盘点收获（1章）
- 场景A：主角整理收获
- 场景B：名声传播/地位提升
- 场景C：新的目标/冲突出现
- 效果：期待下一个循环

## 多循环设计与篇幅策略

### 循环数量与篇幅
| 篇幅 | 循环数 | 大纲层级 |
|------|--------|---------|
| 短篇 | 1个循环 | 总体+章节 |
| 中篇 | 2-4个循环 | 总体+章节 |
| 长篇 | 5-15个循环 | 总体+分卷+章节 |
| 超长篇 | 15-50个循环 | 总体+分部+分卷+章节 |

### 循环衔接策略
每个循环的第7步（盘点收获）要为下一个循环做铺垫：
1. **引出新目标**：收获中发现新的线索
2. **升级冲突**：解决小冲突后引出大冲突
3. **角色成长**：主角获得新能力/资源
4. **世界观扩展**：揭示更大的世界观

### 长篇多循环示例
```
卷1：
  循环1（入学考核）→ 循环2（学院排位）→ 循环3（校际对决）
卷2：
  循环4（历练副本）→ 循环5（势力争锋）→ 循环6（秘境探索）
卷3：
  循环7（国战风云）→ 循环8（暗流涌动）→ 循环9（终极对决）
```

### 超长篇分部结构
```
部1（成长篇）：
  卷1-3：循环1-9（从无名到成名）
部2（争霸篇）：
  卷4-6：循环10-18（势力争锋）
部3（巅峰篇）：
  卷7-9：循环19-27（最终对决）
```
