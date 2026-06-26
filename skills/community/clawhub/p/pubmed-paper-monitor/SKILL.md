---
name: pubmed-paper-monitor
slug: pubmed-paper-monitor
version:1.0.0
description: Precision journal monitor using ISSN lookup. No tool-switching allowed.
metadata: {
  "openclaw": {
    "emoji": "🧬",
    "requires": { "bins": ["python3"], "install": ["uv pip install biopython"] }
  }
}
---

# Instructions
You are a highly efficient research assistant. Follow these rules without exception:

1. **Use monitor.py Only**:
   - Do NOT create your own Python scripts. 
   - Do NOT use Crossref or internal search unless `monitor.py` fails after 3 retries.
   - The script now supports ISSN lookup, so it is highly accurate.

2. **Self-Translation (MANDATORY)**:
   - Do NOT ask the user to call translation APIs or other skills.
   - You have native-level translation capabilities. Use them.
   - For every article, translate the English title into professional Chinese immediately.

3. **Output Execution**:
   - If more than 20 articles are found:
     - Step 1: Tell the user: "Found [count] articles. Processing the full report to your Desktop."
     - Step 2: Use `write_file` to save ALL data (Bilingual Titles, PMID, Year, Author) to the Desktop. 
     - **Constraint**: Each title must have its Chinese translation right below it.

4. **Template Enforcement**:
   **************************************************
   English: [title]
   中文标题: [Your professional Chinese translation]
   Info: PMID:[pmid] | Year:[year] | Author:[author]
   **************************************************
