# HTML Resume Template Guide

Complete reference for the HTML resume template structure.

## Document Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Name] - [Job Title]</title>
    <style>/* see CSS below */</style>
</head>
<body>
    <div class="resume">
        <div class="header">       <!-- Name, target, contact -->
        <div class="section edu">  <!-- Education (brief, near top) -->
        <div class="section">      <!-- 3 Core Advantages grid -->
        <div class="section">      <!-- Key Projects -->
        <div class="section">      <!-- Work Experience -->
        <div class="section">      <!-- Core Competencies grid -->
        <div class="section">      <!-- Skills tags -->
        <div class="section">      <!-- AI Tools (if applicable) -->
        <div class="section">      <!-- Certificates -->
    </div>
</body>
</html>
```

## CSS Variables

```css
:root {
    --accent: #6b4c9a;
    --accent-light: #f8f5fc;
    --accent-tag: #ede6f5;
    --text: #333;
    --text-secondary: #555;
    --text-muted: #888;
    --bg: #fff;
}
```

## CSS Rules

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

@page { size: A4; margin: 0; }

body {
    font-family: "Microsoft YaHei", "PingFang SC", -apple-system, sans-serif;
    font-size: 11px;
    line-height: 1.5;
    color: #333;
    background: #fff;
}

.resume {
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    padding: 12mm 18mm;
}

/* Header */
.header {
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
    margin-bottom: 12px;
}
.name { font-size: 26px; font-weight: 600; color: var(--accent); margin-bottom: 4px; }
.target { font-size: 14px; color: var(--accent); font-weight: 500; margin-bottom: 6px; }
.contact { font-size: 10px; color: #666; display: flex; flex-wrap: wrap; gap: 12px; }
.contact span { display: flex; align-items: center; gap: 4px; }

/* Section */
.section { margin-bottom: 10px; }
.section-title {
    font-size: 13px; font-weight: 600; color: var(--accent);
    margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
}
.section-title::before {
    content: ""; width: 4px; height: 14px;
    background: var(--accent); border-radius: 2px;
}

/* Highlights (3-column grid) */
.highlights { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px; }
.highlight-item {
    background: var(--accent-light); padding: 8px 10px;
    border-radius: 4px; border-left: 3px solid var(--accent);
}
.highlight-title { font-size: 11px; font-weight: 600; color: var(--accent); margin-bottom: 3px; }
.highlight-desc { font-size: 9px; color: #555; line-height: 1.35; }

/* Work Experience */
.work-item { margin-bottom: 8px; }
.work-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 3px; }
.work-company { font-size: 11px; font-weight: 600; color: var(--accent); }
.work-time { font-size: 9px; color: #888; }
.work-role { font-size: 10px; color: #333; margin-bottom: 3px; }
.work-role span { color: #666; }
.work-project { font-size: 9px; color: #666; margin-bottom: 4px; }
.work-desc { font-size: 9px; color: #555; line-height: 1.4; padding-left: 12px; }
.work-desc li { margin-bottom: 1px; }

/* Project Detail Card */
.project-detail {
    background: #faf8fc; padding: 10px 12px;
    border-radius: 4px; margin-bottom: 10px;
    border-left: 3px solid var(--accent);
}
.project-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
.project-name { font-size: 11px; font-weight: 600; color: var(--accent); }
.project-tag { font-size: 9px; color: var(--accent); background: var(--accent-tag); padding: 2px 6px; border-radius: 3px; }
.project-desc { font-size: 9px; color: #555; line-height: 1.5; }
.project-desc li { margin-bottom: 2px; }

/* Skills Grid */
.skills-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.skill-item { display: flex; align-items: flex-start; gap: 6px; }
.skill-label { font-size: 10px; font-weight: 500; color: var(--accent); min-width: 70px; }
.skill-value { font-size: 9px; color: #555; flex: 1; line-height: 1.35; }

/* Tags */
.tag-group { display: flex; flex-wrap: wrap; gap: 5px; }
.tag { font-size: 9px; color: var(--accent); background: var(--accent-tag); padding: 2px 7px; border-radius: 3px; }
.tag-highlight { font-size: 9px; color: #fff; background: var(--accent); padding: 2px 7px; border-radius: 3px; }

/* Education */
.edu-item { display: flex; justify-content: space-between; align-items: baseline; }
.edu-school { font-size: 11px; font-weight: 600; color: var(--accent); }
.edu-time { font-size: 9px; color: #888; }
.edu-detail { font-size: 10px; color: #555; margin-top: 2px; }

/* List bullets */
ul { list-style: none; }
ul li::before { content: "•"; color: var(--accent); margin-right: 6px; }

/* Print */
@media print {
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .resume { margin: 0; box-shadow: none; }
}
```

## Tailoring Rules by Section

### Core Advantages (3 highlights)
- Map each to one of the JD's top 2-3 requirements
- Title: 2-5 word skill label
- Description: 1-2 sentences with specific evidence
- Order: most JD-relevant first

### Work Experience
- **Relevant roles (match JD)**: Full description, 4-5 bullets, quantify achievements
- **Adjacent roles (partial match)**: 2-3 bullets, focus on transferable aspects
- **Unrelated roles**: 1-2 bullets max, or combine into one condensed entry
- Bold key terms and metrics in bullet descriptions
- For recent grads with thin experience: expand project section instead

### Projects
- Only include projects relevant to JD, or that demonstrate key skills
- Each project: name + tag (type/status) + 3-4 bullets
- Lead with most impressive metric if available

### Skills & Tags
- **tag-highlight** (filled): skills explicitly required in JD
- **tag** (outline): supporting skills
- Order: JD-required first, then supporting

## Localization

**Chinese resume:**
- Include birth date in contact
- Photo placeholder optional
- Degree format: 学士/硕士

**English resume:**
- No birth date, no photo
- Degree: BS/MS
- Font: `"Inter", "Helvetica Neue", sans-serif`
- Use English date format: Jan 2020 - Mar 2021
