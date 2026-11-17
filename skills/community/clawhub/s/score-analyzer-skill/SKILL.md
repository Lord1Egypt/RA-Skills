---
name: score-analyzer
description: >
  Analyze student score data from Excel files and generate professional analysis reports.
  Use when the user provides an Excel score sheet (.xlsx), asks to analyze student scores, test results,
  exam data, or grade data. The Agent performs all analysis directly using Python scripts (pandas, matplotlib)
  and its own intelligence for report writing—no external LLM API needed during execution.
  Supports data cleaning, statistical analysis, chart generation (score distribution, class comparison,
  radar, trends, boxplot, heatmap, deviation, top-bottom), narrative report writing, and ZIP package output.
  Triggers: "analyze scores", "score report", "exam analysis", "成绩分析", "成绩报告",
  "学生成绩", "score sheet", "upload excel for analysis", "analyze test results",
  "成绩统计", "前10名", "成绩对比", "班级成绩".
compatibility: Requires Python 3.10+, pandas, matplotlib, seaborn, openpyxl, python-docx, numpy, scipy
---

# Score Analyzer

Agent analyzes student Excel score sheets and produces professional reports. No external LLM API needed.

## Quick Start

### Phase 1: Data Preparation
1.  **Extract**: `python3 scripts/extract_data.py --input <file> --output reports/data.csv`
    - **Complex/Merged headers** (Multi-level, Title rows) → **SKIP** `extract_data.py`. Agent must manually process and output `reports/data.csv` in **strict Long Format**:
      ```
      student_id,student_name,student_class,subject,value
      001,张三,一班,语文分数,85.0
      001,张三,一班,数学分数,92.0
      002,李四,一班,语文分数,88.0
      ```
      - Column names **MUST** be: `student_id`, `student_name`, `subject`, `value`
      - Format **MUST** be Long Format (one row per subject per student)
      - `value` **MUST** be numeric float
      - Python pattern to use:
        ```python
        df = pd.read_excel(file, header=n)  # n = header row index (try 0, 1, 2)
        df.rename(columns={'学号': 'student_id', '姓名': 'student_name'}, inplace=True)
        id_cols = ['student_id', 'student_name']
        if 'student_class' in df.columns:
            id_cols.append('student_class')
        df_long = df.melt(id_vars=id_cols, var_name='subject', value_name='value')
        df_long = df_long.dropna(subset=['value'])
        df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
        df_long.to_csv('reports/data.csv', index=False)
        ```
      - **DO**: Output Long Format, use standard column names, handle merged cells
      - **DON'T**: Keep Wide Format (one column per subject), pass raw columns to data_cleaner
2.  **Clean**: Remove invalid data/grades (A/B/C). **Must Run**: `python3 scripts/data_cleaner.py --input reports/data.csv --output reports/data.csv`
3.  **Tag (Recommended)**: `python3 scripts/tagger.py --input reports/data.csv --output reports/students_tags.csv` (Generates "偏科预警" etc.)
4.  **Individual Reports (Optional)**: `python3 scripts/individual_reports.py --input reports/data.csv --output reports/individual_reports`
5.  **Dynamic Thresholds (MANDATORY)**: Calculate percentile-based passing/excellent thresholds.
    - `python3 scripts/dynamic_thresholds.py --input reports/data.csv --output reports/dynamic_thresholds.json`
    - Output JSON contains: D-G (P80 passing line), D-E (P20 excellent line), pass rates.
    - Read this file when writing the report — provides dynamic metrics to interpret difficult exams.
6.  **Verify Phase 1 (MANDATORY)**: Before proceeding to analysis, validate data quality:
    - **Cleaned data exists**: `reports/data.csv` (or `cleaned_data.csv`) file present?
    - **Data rows reasonable**: Count > 0 and ≤ original Excel rows?
    - **No empty values**: Check `value` column has no NaN/null entries?
    - **Tag file exists**: `students_tags.csv` generated?
    - **Tags match students**: Tag file rows = unique student count in data?
    - **Dynamic thresholds file**: `reports/dynamic_thresholds.json` generated?
    - If ANY check fails → fix data issues before continuing.

### Phase 2: Analysis & Generation
1.  **Analyze**: Agent reads data, finds patterns, writes full Markdown report.
    - **MANDATORY**: Read `reports/dynamic_thresholds.json` for percentile-based metrics.
    - Read `references/analysis_prompt.md` for guidelines.
    - MUST include dynamic stats (D-G, D-E from JSON), fine-grained segments, and 12 chart placeholders.
    - ⚠️ CRITICAL: Chart placeholders MUST use inline format `![描述](PLOT:KEY)`. **NEVER use tables or appendix formats.** The assemble script only recognizes inline placeholders.
2.  **Charts**: `python3 scripts/generate_charts.py --input reports/data.csv --output reports/charts/`
3.  **Assemble**: `python3 scripts/assemble_reports.py --data reports/data.csv --charts reports/charts/ --report "REPORT.md" --output reports/`
4.  **Verify (MANDATORY)**: Before delivering, check ALL outputs:
    - **Dynamic passing/excellent rates** (NOT optional — MUST calculate):
        - Report contains "动态及格线" / "动态及格率" / "相对优秀线" keywords?
        - Passing line is percentile-based (P20, surpassing bottom 20%), NOT fixed 60-point threshold.
        - Excellent line is percentile-based (P80, entering top 20%).
    - **Fine-grained score segments**: Report.md contains segment stats (e.g., "90-100分", "80-89分")?
    - **Chart files**: `ls reports/charts/*.png | wc -l` equals 12 (or 9 if no grouping)?
    - **Chart file sizes**: Each PNG > 10KB (not empty/blank)? `ls -la reports/charts/*.png | awk '$5 < 10000 {print "TOO SMALL: "$0}'`
    - **HTML embedded images**: `reports/report.html` contains valid base64 charts?
        - Count: `grep -c 'data:image/png;base64' reports/report.html` ≥ 12?
    - **Word embedded images**: Are charts actually embedded in `report.docx`?
        - Count: `python3 -c "from docx import Document; print(len(Document('reports/report.docx').element.xpath('.//a:blip')))"` ≥ 12?
    - **Placeholder replacement complete**: No raw `PLOT:XXX` remains?
        - HTML: `grep -c 'PLOT:' reports/report.html` = 0?
    - ⚠️ Pre-assembly format check: Run `grep -c '!\[.*\](PLOT:' reports/report_content.md` → must be ≥ 12 before running assemble_reports.py. If result is 0, the report has placeholders in wrong format (e.g. table).
    - **Individual reports**: `ls reports/individual_reports/*.html | wc -l` equals student count?
    - **Word report**: Size > 100KB?
    - **Data consistency (Cross-Phase)**:
        - Student count in report matches data file row count?
        - Subject count in report matches unique subjects in data?
    - If ANY check fails → report issue to user before continuing.
5.  **Deliver**: `reports/report.zip`

## Chart Placeholders & Template

**For the full report structure and analysis guidelines, READ:** [`references/analysis_prompt.md`](references/analysis_prompt.md)

**Mandatory Chart Placeholders** (include all that apply — match count to generated charts):

| Category | Placeholder | Chart |
|----------|-------------|-------|
| Overview | `PLOT:DISTRIBUTION` | Score distribution histogram |
| | `PLOT:CDF` | Cumulative distribution function |
| | `PLOT:NORMAL` | Normal distribution Q-Q plot |
| Comparison | `PLOT:TREND` | Subject mean trends |
| | `PLOT:HEATMAP` | Class/subject heatmap |
| | `PLOT:BOXPLOT_SUBJ` | Subject box plots |
| Gap/Spread | `PLOT:SCATTER` | Total vs subject scatter |
| | `PLOT:TOP_BOTTOM` | Top vs bottom N comparison |
| | `PLOT:DEVIATION` | Score deviation analysis |
| Grouped* | `PLOT:COMPARISON` | Inter-class comparison |
| | `PLOT:RADAR` | Class radar chart |
| | `PLOT:BOXPLOT` | Class total box plot |

*Grouped placeholders require a grouping column (class/major/school) in the data.

**NEVER** include chart placeholders if chart generation failed — but ALWAYS ensure the markdown text includes exactly 12 placeholders if charts were generated successfully.

**NEVER** write a minimal text report. Must include dynamic passing rates, fine-grained segments, and granular actionable advice.

## 🔧 Decision Tree (Before Starting)

1. **Header Structure**:
   - Simple flat headers (Row 0 is headers) → You can optionally use `extract_data.py` backup.
   - **Complex/Merged headers** (Multi-level, Title rows) → **SKIP** `extract_data.py`. Use Agent's pandas/LLM intelligence directly to map columns.
2. **Chart Generation**:
   - Data has grouping column (class/major/school)? → Generate all **9** charts. Include ALL placeholders.
   - **NO grouping column**? → Generate **6** charts. **MUST REMOVE** `PLOT:COMPARISON`, `PLOT:RADAR`, and `PLOT:BOXPLOT` from the report.
3. **Chinese Font Check**:
   - If charts show squares (tofu): Run `fc-list :lang=zh`. If missing, install `apt install fonts-noto-cjk` → Re-generate charts.

## 🚨 Anti-Patterns (Critical Lessons)

- **NEVER pass minimal text** like `"Test Report"` to `assemble_reports.py`.
  *Why*: The script embeds EXACTLY what you pass. If the report content is short, the final docx/html will appear "empty". You MUST generate a full markdown analysis with statistics tables and narrative text.
- **NEVER include all 9 placeholders** when no grouping data exists.
  *Why*: `generate_charts.py` skips charts 7-9 if grouping is missing. Assembly will leave raw placeholder text in the document.
- **NEVER use `extract_data.py` for complex Excel files** (e.g., merged headers, sub-headers).
  *Why*: It fails on `IndexError` when detecting headers on complex layouts (we learned this the hard way!). Use pandas + Agent intelligence instead.
- **NEVER include `report.zip` in the zip archive**.
  *Why*: Recursive self-inclusion creates massive 3GB+ files. The script has been patched to skip this, but verify `create_zip_package` logic if modifying code.