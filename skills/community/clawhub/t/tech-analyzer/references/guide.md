# Tech Analyzer Reference Guide

## Input Processing Examples

### Example 1: Web Article Analysis

**Input:** `https://example.com/researcher-profile`

**Process:**
1. Use `kimi_fetch` or `web_fetch` to extract content
2. Extract key information:
   - Name: Dr. Zhang Wei
   - Affiliation: Tsinghua University
   - Field: Quantum Computing
   - Achievement: Developed 100-qubit processor

### Example 2: PDF Document

**Input:** Research paper or CV

**Process:**
1. Use `read` tool to extract text
2. Parse structured information
3. Identify technical contributions

## Search Query Templates

### Domestic Search (Chinese)

```
国内 [研究领域] [技术方向] 团队 [大学名称] [研究机构]

Examples:
- 国内 AI芯片 清华大学 研究进展
- 国产 EDA 华大九天 技术路线
- 中国 量子计算 中科院 团队
```

### International Search (English)

```
[Research area] [technology] teams [university] [company] state-of-the-art

Examples:
- quantum computing research teams MIT Stanford Google
- AI chip design automation Cadence Synopsys
- large language model training OpenAI DeepMind research
```

## Report Structure Template

```markdown
# [Name] Technical Analysis Report

## 1. Person Profile
- Basic info
- Affiliation
- Key achievements

## 2. Core Technical Advantages
- Breakthroughs
- Methodologies
- Validation
- Impact

## 3. Competitive Landscape
### 3.1 Domestic Teams
### 3.2 International Teams

## 4. Comparative Summary
- Uniqueness
- Landscape analysis
- Future trajectory
```

## Comparison Table Format

| Dimension | Target | Domestic | International |
|-----------|--------|----------|---------------|
| Approach | | | |
| Stage | | | |
| Advantage | | | |
| Gap | | | |

## Quality Checklist

- [ ] Person profile is complete and accurate
- [ ] Technical advantages are specific (names, metrics)
- [ ] At least 3 domestic teams identified
- [ ] At least 3 international teams identified
- [ ] Comparison highlights key differences
- [ ] Report is properly formatted in Markdown
- [ ] DOCX conversion successful
