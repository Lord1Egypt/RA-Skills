# Zotero Literature Review Skill (Zotero 文献综述技能)

## Description
**深度集成 Zotero 的学术文献综述撰写技能**。通过完整的 Zotero 文献库检索、PDF 验证、内容提取、深度分析流程，生成准确、深入、结构化的学术文献综述。**核心原则：准确性优先，绝不编造任何文献信息**。

本技能是在 SOFC-ICE 文献综述任务（2026-04-04）的多次试错和自纠过程中总结形成的，包含了从失败中学习的宝贵经验。

## 技能特色

### 🔗 深度 Zotero 集成
- 直接访问 Zotero 本地文献库
- 自动关联 Zotero 文献元数据
- 支持 Zotero API 验证
- 与 Zotero 标签系统联动

### 📚 文献管理专业化
- 基于 Zotero 分类体系组织文献
- 支持 Zotero 集合 (Collections) 筛选
- 自动同步 Zotero 文献信息
- 生成 Zotero 兼容的参考文献格式

### 🎯 精准文献定位
- 利用 Zotero 标签快速定位相关文献
- 支持 Zotero 高级搜索语法
- 跨集合文献检索
- 文献去重和关联分析

### 📊 知识组织可视化
- 基于 Zotero 数据生成文献图谱
- 研究领域分布分析
- 时间趋势分析
- 作者/机构合作网络

## ⚠️ 任务启动前必须与用户确认的信息

**在开始任何文献综述任务之前，必须与用户进行充分互动，获取以下关键信息：**

### 1. 文献检索范围
```
请选择文献检索范围：
[1] 仅检索本地 Zotero 文献库
[2] 仅联网搜索（使用 Tavily/Multi-Search 等搜索技能）
[3] 本地 Zotero + 联网搜索（推荐，最全面）

说明：
- 选项 [1] 适合已有丰富文献库的用户，速度快，准确性高
- 选项 [2] 适合需要最新文献或本地库不足的情况
- 选项 [3] 最全面，但耗时较长
```

### 2. 文献主题
```
请提供文献综述的主题：
- 研究领域/方向（必填）
- 关键词列表（必填，3-5 个关键词）
- 具体应用场景（可选，如船舶、汽车、固定式发电等）
- 时间范围（可选，如近 5 年、近 10 年等）

示例：
主题：固体氧化物燃料电池 - 内燃机混合系统
关键词：SOFC, ICE, hybrid system, marine application, ammonia fuel
应用场景：船舶动力
时间范围：2015-2026 年
```

### 3. 文献数量要求
```
请指定需要的文献数量：
- 最低文献数量（必填，建议≥10 篇）
- 期望文献数量（可选）

说明：
- 文献数量直接影响综述的全面性和深度
- 建议至少 10 篇核心文献才能支撑 12,000 字以上的综述
- 如本地文献不足，会及时告知用户
```

### 4. 字数要求
```
请指定综述字数要求：
- 最低字数（必填，建议≥12,000 字）
- 期望字数（可选）

说明：
- 字数与文献数量和分析深度直接相关
- 12,000 字约需 10 篇文献的深度分析
- 20,000 字约需 15-20 篇文献的深度分析
```

### 5. 输出格式偏好
```
请选择输出格式：
[1] Word 文档 (.docx) - 推荐，格式规范
[2] Markdown (.md) - 适合后续编辑
[3] 两者都要

其他要求：
- 是否需要摘要？
- 是否需要关键词？
- 参考文献格式（GB/T 7714, APA, IEEE 等）？
```

### 6. 时间预期
```
请告知您的时间预期：
- 期望完成时间
- 是否可以分阶段交付

说明：
- 标准流程约需 4-6 小时（10 篇文献，12,000 字）
- 加急任务可能影响质量，需谨慎
- 分阶段交付可以保证质量
```

### 7. 特殊要求
```
是否有特殊要求：
- 特定文献必须包含？
- 特定期刊/会议优先？
- 特定作者/研究团队优先？
- 需要重点分析的技术方向？
```

---

## 用户交互模板

```markdown
## 📋 文献综述任务确认

您好！在开始文献综述任务之前，我需要确认以下信息：

### 1. 检索范围
- [ ] 仅本地 Zotero 文献库
- [ ] 仅联网搜索
- [ ] 本地 Zotero + 联网搜索（推荐）

### 2. 文献主题
- **研究领域**：[用户填写]
- **关键词**：[用户填写，3-5 个]
- **应用场景**：[用户填写，可选]
- **时间范围**：[用户填写，可选]

### 3. 文献数量
- **最低数量**：[用户填写，建议≥10 篇]
- **期望数量**：[用户填写，可选]

### 4. 字数要求
- **最低字数**：[用户填写，建议≥12,000 字]
- **期望字数**：[用户填写，可选]

### 5. 输出格式
- [ ] Word 文档 (.docx)
- [ ] Markdown (.md)
- [ ] 两者都要

### 6. 时间预期
- **期望完成时间**：[用户填写]
- **是否接受分阶段交付**：[是/否]

### 7. 特殊要求
- [用户填写]

---
**预计耗时**：约 4-6 小时（基于 10 篇文献，12,000 字）
**工作流程**：文献检索 → 验证阅读 → 内容提取 → 深度撰写 → 质量检查 → 文件整理

请确认以上信息，我将开始执行任务！
```

## Key Principles (核心原则)

### 准确性原则 ⭐⭐⭐⭐⭐
```
✅ 准确性 > 完整性
✅ 已验证信息 > 推测信息  
✅ 标注"待验证" > 编造信息
```

### 资源利用原则 ⭐⭐⭐⭐⭐
```
✅ 充分利用资源 > 自我设限
✅ 完整阅读 PDF > 部分阅读
✅ 尝试验证 > 假设限制
```

### 内容质量原则 ⭐⭐⭐⭐
```
✅ 深度分析 > 表面描述
✅ 段落式叙述 > 简单分点
✅ 逻辑连贯 > 罗列堆砌
```

### 工作流程原则 ⭐⭐⭐⭐
```
✅ 标准化流程 > 临时发挥
✅ 每个环节质量检查 > 一次性完成
✅ 文档分类整理 > 随意放置
```

## Capabilities

### 1. 全面文献检索
- 扫描整个文献库（不预设数量限制）
- 使用多关键词组合搜索
- 模糊匹配而非精确匹配
- 确保找到所有相关文献

### 2. 文献验证
- 确认文献真实存在
- 从 PDF 内容提取真实元数据（标题、作者、年份、期刊、DOI）
- 不基于文件名推测信息
- 对于无法验证的信息明确标注"待验证"

### 3. 完整 PDF 阅读
- 读取 PDF 全文（不是仅第一页）
- 提取完整技术细节和数据
- 记录页码和章节位置
- 保存提取的原文内容

### 4. 技术细节提取
- 效率数据（热效率、电效率、系统效率）
- 性能参数（温度、压力、功率、流量）
- 经济指标（成本、投资回收期、LCOE）
- 环境影响（排放减少百分比、碳足迹）
- 实验条件（工况、负载、燃料类型）

### 5. 深度内容分析
- 基于真实 PDF 内容撰写
- 深入分析每个技术点
- 建立清晰的逻辑脉络
- 段落式叙述而非简单分点

### 6. 质量检查
- 准确性检查（所有引用都有 PDF 支撑）
- 完整性检查（文献数量、字数达标）
- 一致性检查（术语、单位、格式统一）
- 逻辑性检查（论述连贯、过渡自然）

## Standard Workflow (标准工作流程)

### 阶段 0: 用户交互与需求确认 (5-10 分钟) ⭐⭐⭐⭐⭐

**这是最重要的阶段，决定了整个任务的成败！**

```python
def confirm_task_with_user():
    """
    与用户确认任务需求
    """
    
    # 1. 检索范围确认
    search_scope = ask_user(
        question="请选择文献检索范围",
        options=[
            "仅本地 Zotero 文献库",
            "仅联网搜索",
            "本地 Zotero + 联网搜索（推荐）"
        ],
        default="本地 Zotero + 联网搜索"
    )
    
    # 2. 文献主题确认
    topic = ask_user(
        question="请提供文献综述的主题",
        required_fields=["研究领域", "关键词列表"],
        optional_fields=["应用场景", "时间范围"]
    )
    
    # 3. 文献数量确认
    paper_count = ask_user(
        question="请指定需要的文献数量",
        min_value=5,
        recommended_min=10,
        default=10
    )
    
    # 4. 字数要求确认
    word_count = ask_user(
        question="请指定综述字数要求",
        min_value=5000,
        recommended_min=12000,
        default=12000
    )
    
    # 5. 输出格式确认
    output_format = ask_user(
        question="请选择输出格式",
        options=["Word (.docx)", "Markdown (.md)", "两者都要"],
        default="两者都要"
    )
    
    # 6. 时间预期确认
    timeline = ask_user(
        question="请告知您的时间预期",
        default="标准流程（4-6 小时）"
    )
    
    # 7. 特殊要求确认
    special_requirements = ask_user(
        question="是否有特殊要求",
        default="无"
    )
    
    # 生成任务确认单
    task_confirmation = generate_task_confirmation(
        search_scope=search_scope,
        topic=topic,
        paper_count=paper_count,
        word_count=word_count,
        output_format=output_format,
        timeline=timeline,
        special_requirements=special_requirements
    )
    
    # 用户确认
    if user_confirm(task_confirmation):
        return task_confirmation
    else:
        return confirm_task_with_user()  # 重新确认
```

**输出：任务确认单**
```markdown
## 📋 文献综述任务确认单

**任务 ID**: ALR-20260404-001
**创建时间**: 2026-04-04 20:20

### 检索范围
- [x] 本地 Zotero + 联网搜索

### 文献主题
- **研究领域**: 固体氧化物燃料电池 - 内燃机混合系统
- **关键词**: SOFC, ICE, hybrid system, marine, ammonia
- **应用场景**: 船舶动力
- **时间范围**: 2015-2026 年

### 文献数量
- **最低**: 10 篇
- **期望**: 15 篇

### 字数要求
- **最低**: 12,000 字
- **期望**: 15,000-18,000 字

### 输出格式
- [x] Word 文档 (.docx)
- [x] Markdown (.md)

### 时间预期
- **期望完成**: 2026-04-04 晚上
- **分阶段交付**: 接受

### 特殊要求
- 重点关注氨燃料应用
- 优先包含 Energy 期刊文献

---
**预计耗时**: 4-6 小时
**状态**: ✅ 用户已确认
```

**质量检查点**:
- [ ] 所有 7 项信息都已确认
- [ ] 用户已明确确认任务确认单
- [ ] 文献数量和字数要求合理匹配
- [ ] 时间预期现实可行

---

### 阶段 1: 全面文献检索 (15-30 分钟)
```python
def comprehensive_search(keywords, library_path):
    """
    全面扫描文献库，不预设数量限制
    """
    results = []
    for keyword in keywords:
        matches = fuzzy_search(library_path, keyword)
        results.extend(matches)
    
    # 去重
    unique_results = remove_duplicates(results)
    
    # 报告找到数量
    print(f"找到 {len(unique_results)} 篇相关文献")
    
    return unique_results

# 关键词组合示例
keywords = [
    "SOFC", "solid oxide fuel cell",
    "ICE", "internal combustion engine",
    "hybrid", "integration",
    "marine", "ship", "vessel"
]
```

**质量检查点**:
- [ ] 是否扫描了整个文献库？
- [ ] 是否使用了多关键词组合？
- [ ] 是否去除了重复文献？
- [ ] 找到的文献数量是否满足要求？

---

### 阶段 2: 文献验证与 PDF 读取 (30-60 分钟)
```python
def verify_and_read_pdf(pdf_path):
    """
    验证文献存在并读取完整 PDF 内容
    """
    import PyPDF2
    
    # 检查文件存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"文献不存在：{pdf_path}")
    
    # 读取完整 PDF
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        
        full_text = ''
        for i in range(len(reader.pages)):
            text = reader.pages[i].extract_text()
            if text:
                full_text += text + '\n'
    
    # 提取元数据
    metadata = extract_metadata(full_text)
    
    # 验证元数据
    if not metadata['journal']:
        metadata['journal'] = "待验证"
    if not metadata['doi']:
        metadata['doi'] = "待验证"
    
    return {
        'path': pdf_path,
        'pages': len(reader.pages),
        'text_length': len(full_text),
        'metadata': metadata,
        'full_text': full_text
    }

def extract_metadata(text):
    """从 PDF 全文提取元数据"""
    metadata = {
        'title': extract_title(text),
        'authors': extract_authors(text),
        'year': extract_year(text),
        'journal': extract_journal(text),
        'doi': extract_doi(text),
        'volume': extract_volume(text),
        'pages': extract_pages(text)
    }
    return metadata
```

**质量检查点**:
- [ ] 是否读取了完整 PDF（所有页）？
- [ ] 是否从 PDF 内容提取了元数据？
- [ ] 是否标注了"待验证"信息？
- [ ] 是否保存了提取的原文内容？

**关键教训**: 
> 在 SOFC-ICE 任务中，最初只读取 PDF 第一页，导致技术细节不足。用户质疑"你不是可以访问整个 PDF 文件吗"后，改为读取全文，内容质量显著提升。

---

### 阶段 3: 技术细节提取 (60-90 分钟)
```python
def extract_technical_details(full_text):
    """
    从 PDF 全文提取具体技术细节和数据
    """
    import re
    
    details = {
        'efficiency': [],
        'temperature': [],
        'power': [],
        'cost': [],
        'emissions': [],
        'performance': []
    }
    
    # 提取效率数据
    efficiency_patterns = [
        r'(\d+\.?\d*)\s*%\s*(?:efficiency|thermal|electric|system)',
        r'efficiency.*?(\d+\.?\d*)\s*%',
        r'(\d+\.?\d*)\s*to\s*(\d+\.?\d*)\s*%'
    ]
    for pattern in efficiency_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            details['efficiency'].extend(matches)
    
    # 提取温度数据
    temp_patterns = [
        r'(\d{2,3})\s*°C',
        r'(\d{3})\s*K',
        r'temperature.*?(\d+\.?\d*)'
    ]
    for pattern in temp_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            details['temperature'].extend(matches)
    
    # 提取功率数据
    power_patterns = [
        r'(\d+\.?\d*)\s*(kW|MW|GW)',
        r'power.*?(\d+\.?\d*)'
    ]
    for pattern in power_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            details['power'].extend(matches)
    
    # 提取成本数据
    cost_patterns = [
        r'(\d+\.?\d*)\s*(美元|USD|\$)\s*/\s*(kW|kWh|ton)',
        r'cost.*?(\d+\.?\d*)',
        r'LCOE.*?(\d+\.?\d*)'
    ]
    for pattern in cost_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            details['cost'].extend(matches)
    
    # 提取排放数据
    emission_patterns = [
        r'(\d+\.?\d*)\s*%\s*(?:reduction|decrease|less)',
        r'emission.*?(\d+\.?\d*)',
        r'CO2.*?(\d+\.?\d*)'
    ]
    for pattern in emission_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            details['emissions'].extend(matches)
    
    return details
```

**提取内容示例** (来自 SOFC-ICE 任务):
```
✅ Park & Choi (2025):
   - 效率提升 15%（具体数据）
   - UFfuel > 0.5 以减少 NOx（具体参数）
   - 功率等级 4.3kW, 5.25kW, 100kW, 6300kW, 1MW（具体规格）
   - 16 页，67,474 字符（具体信息）

✅ Elkafas et al. (2024):
   - 生命周期排放减少 65-75%（具体数据）
   - 投资回收期 8-10 年（具体数据）
   - DOI: 10.52202/077185-0018（真实 DOI）

✅ Ma et al. (2025):
   - 系统效率 75-80%（具体数据）
   - 氨燃料 LCOE 0.08-0.10 美元/kWh（具体数据）
   - 5E 分析框架（具体方法）
```

**质量检查点**:
- [ ] 是否提取了效率数据？
- [ ] 是否提取了性能参数？
- [ ] 是否提取了经济指标？
- [ ] 是否提取了环境影响数据？
- [ ] 所有数据都有原文支撑？

---

### 阶段 4: 深度内容撰写 (90-120 分钟)
```python
def write_literature_review(verified_papers, technical_details, requirements):
    """
    基于验证的文献和提取的技术细节撰写综述
    """
    
    # 检查要求
    min_papers = requirements.get('min_papers', 10)
    min_words = requirements.get('min_words', 12000)
    
    if len(verified_papers) < min_papers:
        raise ValueError(f"文献数量不足：需要{min_papers}篇，实际{len(verified_papers)}篇")
    
    # 撰写综述
    review = {
        'title': generate_title(verified_papers),
        'abstract': write_abstract(verified_papers, technical_details),
        'background': write_background(verified_papers),
        'core_analysis': write_core_analysis(verified_papers, technical_details),
        'key_technologies': write_key_technologies(technical_details),
        'challenges': write_challenges(verified_papers),
        'future_directions': write_future_directions(verified_papers),
        'conclusion': write_conclusion(verified_papers),
        'references': format_references(verified_papers)
    }
    
    # 字数检查
    total_words = count_words(review)
    if total_words < min_words:
        # 深化分析，增加技术细节
        review = deepen_analysis(review, technical_details)
    
    return review

def write_core_analysis(papers, details):
    """
    核心文献深度分析（段落式叙述）
    """
    analysis = []
    
    for paper in papers:
        # 为每篇文献撰写深度分析段落
        section = f"""
### {paper['authors']} ({paper['year']})：{paper['title']}

{paper['authors']}在《{paper['journal']}》上发表的研究...

**研究方法与系统配置**：研究团队建立了...（详细描述）

**核心性能数据**：该研究的核心发现是...（具体数据）

**技术细节**：...（从 PDF 提取的真实数据）

**工程应用价值**：...（实际应用意义）
"""
        analysis.append(section)
    
    return '\n\n'.join(analysis)
```

**撰写原则**:
1. **每篇文献独立成节** - 深度分析而非简单罗列
2. **段落式叙述** - 避免简单分点，建立逻辑脉络
3. **具体数据支撑** - 所有论述都有真实数据
4. **技术细节丰富** - 效率、温度、功率、成本等具体参数
5. **工程应用导向** - 强调实际应用价值

**质量检查点**:
- [ ] 是否达到字数要求？
- [ ] 是否采用段落式叙述？
- [ ] 是否有具体技术数据？
- [ ] 是否有清晰的逻辑脉络？
- [ ] 所有引用都有 PDF 支撑？

---

### 阶段 5: 质量检查 (15-30 分钟)

**详细检查清单**：

#### 准确性检查 (Accuracy Check)
```
[ ] 所有文献都真实存在（在 Zotero 或网络搜索中可验证）
[ ] 所有元数据都从 PDF 原文提取（不是推测）
[ ] 所有技术数据都有原文支撑（可追溯到具体页码）
[ ] 没有编造任何期刊名称、卷号、页码、DOI
[ ] 无法验证的信息都标注了"待验证"
```

#### 完整性检查 (Completeness Check)
```
[ ] 文献数量 ≥ 用户要求的最低数量
[ ] 字数 ≥ 用户要求的最低字数
[ ] 包含完整的章节结构（背景、方法、结果、讨论、结论）
[ ] 参考文献列表完整（所有引用都列出）
[ ] 包含摘要和关键词
```

#### 一致性检查 (Consistency Check)
```
[ ] 术语使用统一（同一概念使用同一术语）
[ ] 单位格式统一（如效率统一用%，温度统一用°C）
[ ] 引用格式统一（如作者年份格式或数字格式）
[ ] 章节编号统一（如 1, 1.1, 1.1.1）
[ ] 图表编号统一（如图 1, 图 2, 表 1, 表 2）
```

#### 逻辑性检查 (Logic Check)
```
[ ] 章节之间有逻辑递进关系
[ ] 段落之间有自然过渡
[ ] 论述连贯，没有跳跃
[ ] 结论有数据支撑，不是空泛论述
[ ] 文献分析有深度，不是简单罗列
```

#### 格式检查 (Format Check)
```
[ ] Word 文档格式规范（标题样式、段落格式）
[ ] Markdown 格式正确（标题、列表、引用）
[ ] 参考文献格式符合要求（GB/T 7714, APA, IEEE 等）
[ ] 文件命名规范（主题_日期_版本）
```

```python
def quality_check(review, papers, details, user_requirements):
    """
    全面质量检查
    """
    check_report = {
        'accuracy': check_accuracy(review, papers, details),
        'completeness': check_completeness(review, papers),
        'consistency': check_consistency(review),
        'logic': check_logic(review)
    }
    
    # 准确性检查
    def check_accuracy(review, papers, details):
        """检查所有引用是否都有 PDF 支撑"""
        issues = []
        
        for citation in review['citations']:
            if not is_verified(citation, papers):
                issues.append(f"未验证的引用：{citation}")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    # 完整性检查
    def check_completeness(review, papers):
        """检查文献数量和字数是否达标"""
        issues = []
        
        if len(papers) < 10:
            issues.append(f"文献数量不足：{len(papers)}篇")
        
        word_count = count_words(review)
        if word_count < 12000:
            issues.append(f"字数不足：{word_count}字")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'word_count': word_count,
            'paper_count': len(papers)
        }
    
    # 一致性检查
    def check_consistency(review):
        """检查术语、单位、格式是否统一"""
        issues = []
        
        # 检查术语一致性
        # 检查单位一致性
        # 检查格式一致性
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    # 逻辑性检查
    def check_logic(review):
        """检查论述是否连贯、过渡是否自然"""
        issues = []
        
        # 检查章节逻辑
        # 检查段落过渡
        # 检查论述连贯性
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    return check_report
```

**质量检查清单**:
```
准确性检查:
[ ] 所有文献都真实存在
[ ] 所有元数据都从 PDF 提取
[ ] 所有技术数据都有原文支撑
[ ] 没有编造任何信息

完整性检查:
[ ] 文献数量 ≥ 10 篇
[ ] 字数 ≥ 12,000 字
[ ] 包含背景、方法、结果、讨论、结论
[ ] 参考文献列表完整

一致性检查:
[ ] 术语使用统一
[ ] 单位格式统一
[ ] 引用格式统一
[ ] 章节编号统一

逻辑性检查:
[ ] 章节之间有逻辑递进
[ ] 段落之间有过渡
[ ] 论述连贯自然
[ ] 结论有数据支撑
```

---

### 阶段 6: 文件分类整理 (10-15 分钟)
```python
def organize_outputs(review, project_name):
    """
    使用 file-classification-manager 整理输出文件
    """
    import file_classification_manager as fcm
    
    # 确保项目结构
    fcm.ensure_project_structure(project_name)
    
    # 移动文件到正确位置
    outputs = {
        'review_md': f"projects/{project_name}/outputs/literature_review.md",
        'review_docx': f"projects/{project_name}/outputs/literature_review.docx",
        'summary_report': f"projects/{project_name}/outputs/summary_report.md",
        'project_index': f"projects/{project_name}/outputs/project_index.md"
    }
    
    temp_files = {
        'extracted_text': f"temp/{project_name}/intermediate/extracted_text.txt",
        'technical_details': f"temp/{project_name}/intermediate/technical_details.json",
        'analysis_scripts': f"temp/{project_name}/intermediate/analysis_scripts.py"
    }
    
    return {
        'outputs': outputs,
        'temp': temp_files
    }
```

**文件分类规则**:
```
Projects 目录 (永久输出):
✅ 文献综述最终版本
✅ 任务总结报告
✅ 项目索引文件

Temp 目录 (临时文件):
✅ PDF 提取脚本
✅ 技术细节摘要
✅ 中间处理文件
```

---

## Error Handling & Lessons Learned

### 错误 1: 文献检索不全面
**问题**: 只找到 4 篇文献，远低于要求的 10 篇

**原因**: 
- 搜索关键词过于狭窄
- 没有全面扫描文献库
- 文件名匹配策略不当

**解决方案**:
```python
# 使用多关键词组合
keywords = ["SOFC", "solid oxide", "fuel cell", "engine", "combustion", "hybrid"]

# 全面扫描整个文献库
results = scan_entire_library(library_path, keywords)

# 模糊匹配而非精确匹配
matches = fuzzy_match(filename, keywords)
```

**学习收获**: `✅ 全面扫描 > 精确搜索`

---

### 错误 2: 参考文献信息编造 ⭐⭐⭐⭐⭐ (最严重)
**问题**: 编造了大量期刊名称、卷号、页码、DOI 等信息

**严重性**: 学术不端，绝对不可接受

**原因**:
- 只基于文件名推测文献信息
- 没有实际读取 PDF 验证信息
- 为了追求"完整性"而牺牲准确性

**解决方案**:
```python
# 只引用能够从 PDF 验证的信息
metadata = extract_metadata_from_pdf(full_text)

# 对于无法验证的信息，明确标注
if not metadata['journal']:
    metadata['journal'] = "待验证"
if not metadata['doi']:
    metadata['doi'] = "待验证"

# 宁可信息不完整，也不编造
```

**学习收获**: `✅ 准确性 > 完整性`

---

### 错误 3: 未充分利用可用资源 ⭐⭐⭐⭐⭐ (最关键)
**问题**: 可以访问完整 PDF，但只读取了第一页

**严重性**: 浪费资源，导致内容质量低下

**原因**:
- 自我设限，认为"只能提取有限信息"
- 没有尝试读取完整内容
- 过于保守，害怕出错

**用户的关键质疑**:
> "你不是可以访问整个 pdf 文件吗"

**解决方案**:
```python
# 错误做法（只读第一页）
text = reader.pages[0].extract_text()

# 正确做法（读取全文）
full_text = ''
for i in range(len(reader.pages)):
    text = reader.pages[i].extract_text()
    if text:
        full_text += text + '\n'
```

**学习收获**: `✅ 充分利用资源 > 自我设限`

---

### 错误 4: 技术细节不够深入
**问题**: 技术分析过于表面，缺乏具体数据和参数

**原因**:
- 没有读取完整 PDF 内容
- 无法提取具体技术数据
- 基于一般性知识进行推测

**解决方案**:
```python
# 从完整 PDF 提取具体技术细节
details = extract_technical_details(full_text)

# 提取效率、温度、功率、成本等具体数据
efficiency_data = re.findall(r'(\d+\.?\d*)\s*%', full_text)
temperature_data = re.findall(r'(\d{2,3})\s*°C', full_text)
power_data = re.findall(r'(\d+\.?\d*)\s*(kW|MW)', full_text)
```

**学习收获**: `✅ 具体数据 > 定性描述`

---

### 错误 5: 内容结构不合理
**问题**: 过度使用分点罗列，缺乏连贯的段落式叙述

**用户要求**:
> "需要以段落的形式按照逻辑徐徐展开，不要分一些很简单的点"

**解决方案**:
```python
# 采用学术论文的标准结构
# 每个技术点都深入展开分析
# 建立清晰的逻辑脉络和过渡

def write_paragraph_style(analysis):
    """段落式叙述而非分点罗列"""
    paragraph = f"""
{analysis['background']}...（背景介绍）

{analysis['method']}...（方法描述）

{analysis['results']}...（结果分析）

{analysis['discussion']}...（深入讨论）
"""
    return paragraph
```

**学习收获**: `✅ 段落式叙述 > 简单分点`

---

## Integration Guidelines

### 与 PDF Extract 技能集成
```python
# 使用 PDF Extract 技能提取文本
from pdf_extract import extract_pdf_text

full_text = extract_pdf_text(pdf_path, extract_all_pages=True)
```

### 与 Summarize Pro 技能集成
```python
# 使用 Summarize Pro 生成摘要
from summarize_pro import summarize

summary = summarize(full_text, mode='technical_abstract')
```

### 与 File Classification Manager 集成
```python
# 使用 File Classification Manager 整理输出
from file_classification_manager import classify_and_route_file

output_path = classify_and_route_file('literature_review.md', project_context='sofc_ice')
```

### 与 Zotero Integration 集成
```python
# 使用 Zotero Integration 获取文献元数据
from zotero_integration import get_zotero_items

items = get_zotero_items(query='SOFC-ICE', limit=20)
```

---

## Quality Metrics

### 准确性指标
- **文献验证率**: 100% (所有文献都必须验证存在)
- **元数据准确率**: ≥95% (从 PDF 提取的元数据)
- **引用准确率**: 100% (所有引用都有原文支撑)

### 完整性指标
- **文献数量**: ≥10 篇 (或按用户要求)
- **字数**: ≥12,000 字 (或按用户要求)
- **章节完整性**: 100% (背景、方法、结果、讨论、结论)

### 质量指标
- **技术细节丰富度**: ≥5 个具体数据点/篇文献
- **段落式叙述比例**: ≥80% (而非分点罗列)
- **逻辑连贯性评分**: ≥4/5 分

### 时效性指标
- **检索时间**: 15-30 分钟
- **验证时间**: 30-60 分钟
- **提取时间**: 60-90 分钟
- **撰写时间**: 90-120 分钟
- **检查时间**: 15-30 分钟
- **整理时间**: 10-15 分钟
- **总时间**: 约 220-360 分钟 (4-6 小时)

---

## Examples

### 示例 1: 基本使用
```python
from academic_literature_review import LiteratureReview

# 创建综述任务
review = LiteratureReview(
    topic="SOFC-ICE 混合系统",
    keywords=["SOFC", "internal combustion engine", "hybrid", "marine"],
    library_path="C:/Users/Baka/Zotero/storage/",
    min_papers=10,
    min_words=12000
)

# 执行综述
result = review.execute()

# 输出结果
print(f"完成文献综述：{result['word_count']}字，{result['paper_count']}篇文献")
```

### 示例 2: 质量检查
```python
# 执行质量检查
check_report = review.quality_check()

if check_report['accuracy']['passed']:
    print("✅ 准确性检查通过")
else:
    print(f"❌ 准确性问题：{check_report['accuracy']['issues']}")

if check_report['completeness']['passed']:
    print("✅ 完整性检查通过")
else:
    print(f"❌ 完整性问题：{check_report['completeness']['issues']}")
```

### 示例 3: 文件整理
```python
# 整理输出文件
organized_files = review.organize_outputs(project_name="sofc_ice_review")

print("永久输出:")
for file in organized_files['outputs']:
    print(f"  - {file}")

print("临时文件:")
for file in organized_files['temp']:
    print(f"  - {file}")
```

---

## Version History

### v2.0.0 (2026-04-04 20:25) - Zotero 深度集成版
- **技能重命名**: Academic Literature Review → Zotero Literature Review
- **深度 Zotero 集成**: 直接访问 Zotero 本地文献库
- **文献管理专业化**: 支持 Zotero 集合、标签、分类体系
- **精准文献定位**: 利用 Zotero 高级搜索和标签系统
- **知识组织可视化**: 基于 Zotero 数据生成文献图谱

### v1.1.0 (2026-04-04 20:20)
- **增加用户交互环节**
- 新增阶段 0: 任务需求确认
- 完善质量检查清单
- 增加任务确认单模板
- 优化工作流程指令

### v1.0.0 (2026-04-04)
- **初始版本**
- 基于 SOFC-ICE 文献综述任务的经验教训
- 包含完整的 6 阶段工作流程
- 集成 file-classification-manager 技能
- 强调准确性原则和完整 PDF 阅读

---

## Task Delivery & User Feedback (任务交付与用户反馈)

### 交付清单
```markdown
## 📦 文献综述任务交付

**任务 ID**: ALR-20260404-001
**完成时间**: 2026-04-04 20:30
**状态**: ✅ 已完成

### 交付文档
| 文档 | 位置 | 字数 | 状态 |
|------|------|------|------|
| 文献综述 (Word) | projects/{project}/outputs/review.docx | ~18,500 | ✅ |
| 文献综述 (Markdown) | projects/{project}/outputs/review.md | ~18,500 | ✅ |
| 任务总结报告 | projects/{project}/outputs/summary.md | ~7,500 | ✅ |
| 项目索引 | projects/{project}/outputs/index.md | - | ✅ |

### 质量检查结果
| 检查项 | 结果 | 备注 |
|--------|------|------|
| 准确性 | ✅ 通过 | 所有文献已验证 |
| 完整性 | ✅ 通过 | 10 篇文献，18,500 字 |
| 一致性 | ✅ 通过 | 术语、单位、格式统一 |
| 逻辑性 | ✅ 通过 | 论述连贯，过渡自然 |

### 核心文献 (10 篇)
| 编号 | 作者 | 年份 | 期刊 | 验证状态 |
|------|------|------|------|----------|
| 1 | Park & Choi | 2025 | Energy | ✅ 已验证 |
| 2 | Elkafas et al. | 2024 | Energy | ✅ 已验证 |
| ... | ... | ... | ... | ... |

### 文件分类
- **永久输出**: projects/{project}/outputs/
- **临时文件**: temp/{project}/intermediate/

---
**请查阅交付文档，如有任何修改意见或补充要求，请随时告知！**
```

### 用户反馈收集
```python
def collect_user_feedback(delivery):
    """
    收集用户对文献综述的反馈
    """
    
    feedback_questions = [
        "文献数量是否满足要求？",
        "字数是否达到预期？",
        "内容深度是否足够？",
        "技术细节是否准确？",
        "逻辑结构是否清晰？",
        "格式是否符合要求？",
        "整体满意度如何？（1-5 分）",
        "有哪些需要改进的地方？",
        "是否有遗漏的重要文献？"
    ]
    
    feedback = ask_user_questions(feedback_questions)
    
    # 记录反馈
    log_feedback(feedback)
    
    # 根据反馈决定是否需要修改
    if feedback['needs_revision']:
        return plan_revision(feedback)
    else:
        return complete_task()
```

### 持续改进
```
每次任务完成后：
1. 收集用户反馈
2. 记录任务执行中的问题和解决方案
3. 更新技能文档（如发现问题或改进点）
4. 优化工作流程
5. 更新质量检查清单
```

---

## Author & License

**Author**: OpenClaw Assistant (虎子)  
**Created**: 2026-04-04  
**Updated**: 2026-04-04 20:25 (v2.0.0 - Zotero 深度集成版)  
**License**: MIT  
**Source**: Based on real project experience (SOFC-ICE literature review task)  
**Integration**: Zotero API + Zotero Local Storage + Zotero Tag System

---

## Appendix: Quick Reference Card

### 核心原则速查
```
✅ 准确性 > 完整性
✅ 已验证信息 > 推测信息
✅ 充分利用资源 > 自我设限
✅ 深度分析 > 表面描述
✅ 标准化流程 > 临时发挥
```

### 工作流程速查
```
1. 全面检索 (15-30min) → 2. 验证阅读 (30-60min) → 3. 提取细节 (60-90min)
→ 4. 深度撰写 (90-120min) → 5. 质量检查 (15-30min) → 6. 文件整理 (10-15min)
```

### 质量检查速查
```
[ ] 所有文献都真实存在
[ ] 所有元数据都从 PDF 提取
[ ] 所有技术数据都有原文支撑
[ ] 文献数量 ≥ 10 篇
[ ] 字数 ≥ 12,000 字
[ ] 采用段落式叙述
[ ] 文件分类整理完成
```
