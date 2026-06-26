---
name: tech-analyzer
description: |
  Deep analysis of technology researchers/innovators and their core technical advantages, with comparative analysis of similar teams domestically and internationally. 
  
  Use when user needs to:
  1. Analyze a researcher/innovator's technical background and core advantages
  2. Compare domestic and international similar research teams
  3. Generate a comprehensive technical analysis report
  
  Input can be: PDF files, Word documents, web links, or direct text content about the target person/technology.
  Output is a Word (.docx) document containing: person background, technical advantages, and team comparison analysis.
---

# Tech Analyzer Skill

Analyze technology researchers/innovators and their competitive landscape.

## Workflow

### Step 1: Input Processing

Accept input in any of these forms:
- **File attachments**: PDF, DOCX, or other document formats
- **Web links**: URLs to articles, profiles, or reports
- **Direct text**: Pasted content about the target person/technology

Use appropriate tools to extract content:
- For files: Read file content
- For URLs: Use kimi_fetch or web_fetch to extract content
- For text: Use directly

### Step 2: Content Analysis

Analyze the extracted content to identify:

**Person Profile:**
- Name, title, affiliation
- Research field and focus area
- Key achievements and recognitions

**Core Technical Advantages:**
- Breakthrough innovations
- Key methodologies or systems
- Performance metrics and validation results
- Unique insights or theoretical contributions
- Academic and industrial impact

### Step 3: Competitive Research

Search for similar teams/researchers both domestically (China) and internationally:

**Domestic Search (China):**
- Leading universities (Tsinghua, Peking University, Fudan, etc.)
- Research institutes (CAS institutes)
- Industry companies and startups
- Key research groups in the same field

**International Search:**
- Top universities (MIT, Stanford, CMU, etc.)
- Research labs (Google Research, OpenAI, etc.)
- Industry leaders and startups
- Academic conferences and publications

Use kimi_search with specific queries to find relevant information.

### Step 4: Comparative Analysis

Create a structured comparison covering:

| Dimension | Target Person | Domestic Peers | International Peers |
|-----------|---------------|----------------|---------------------|
| Approach | [Methodology] | [Domestic approach] | [International approach] |
| Advantages | [Key strengths] | [Domestic strengths] | [International strengths] |
| Stage | [Research/validation/product] | [Domestic stage] | [International stage] |

### Step 5: Report Generation

Generate a comprehensive Word (.docx) document with the following structure:

```
# [Person Name] Technical Analysis Report

## 1. Person Profile
- Basic information
- Affiliation and title
- Key achievements

## 2. Core Technical Advantages

### 2.1 Breakthrough Innovations
[Description of key systems/methods]

### 2.2 Key Methodologies
[Technical approach and unique insights]

### 2.3 Performance Validation
[Metrics, benchmarks, validation results]

### 2.4 Academic & Industrial Impact
[Publications, citations, technology transfer]

## 3. Competitive Landscape Analysis

### 3.1 Domestic Teams (China)
| Organization | Research Focus | Key Progress |
|--------------|----------------|--------------|
| [Team 1] | [Focus] | [Progress] |
| [Team 2] | [Focus] | [Progress] |

### 3.2 International Teams
| Organization | Research Focus | Key Progress |
|--------------|----------------|--------------|
| [Team 1] | [Focus] | [Progress] |
| [Team 2] | [Focus] | [Progress] |

## 4. Comparative Summary

### 4.1 Target Person's Uniqueness
[List unique advantages]

### 4.2 Domestic vs International Landscape
[Overall comparison and gap analysis]

### 4.3 Technology Trajectory
[Future directions and trends]

---
*Report generated: [Date]*
*Sources: [List key sources]*
```

Use pandoc to convert Markdown to DOCX:
```bash
pandoc report.md -o report.docx
```

### Step 6: Output Delivery

1. Save the .docx file to workspace
2. Send file to user via message tool with filePath parameter
3. If file transfer fails, provide the content directly as formatted text

## Research Guidelines

**Search Strategy:**
- Use kimi_search with include_content=true for comprehensive results
- Search for both academic (universities, institutes) and industry (companies, startups) perspectives
- Include key terms in both Chinese and English for broader coverage

**Analysis Principles:**
- Be specific: Include names, institutions, system names, metrics
- Be comparative: Highlight differences in approaches
- Be balanced: Acknowledge both strengths and limitations
- Be current: Focus on recent developments (last 2-3 years)

**Quality Standards:**
- Technical accuracy: Verify technical claims from reliable sources
- Completeness: Cover all required sections
- Objectivity: Present balanced view of competitive landscape
- Actionability: Provide insights useful for decision-making

## Error Handling

If input cannot be processed:
1. Ask user for clarification or alternative format
2. If content extraction fails, request user to paste text directly

If research yields limited results:
1. Expand search terms
2. Try related fields or technologies
3. Note limitations in the report

If file generation fails:
1. Provide content as formatted Markdown
2. Offer to retry with different approach
