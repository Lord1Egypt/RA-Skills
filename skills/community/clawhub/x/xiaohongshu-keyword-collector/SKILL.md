---
name: xiaohongshu-keyword-collector
description: Automatically accesses Xiaohongshu's Explore page via browser automation, inputs keywords into the search bar, and collects the list of related keywords from the auto-suggest dropdown.
---

# Xiaohongshu Keyword Collector

## Feature Overview

This skill uses browser automation tools to access the Xiaohongshu Explore page, input keywords into the search bar, and collect the list of related keywords suggested by the search box's auto-complete feature. No API required; it's purely browser-based operation.

## Trigger Conditions

Trigger this skill when the user mentions any of the following keywords:
- 小红书关键词
- 收集小红书关键词
- 小红书搜索建议
- 小红书热搜词
- 小红书 SEO
- 小红书话题
- Xiaohongshu keywords
- Collect Xiaohongshu keywords
- Xiaohongshu search suggestions
- Xiaohongshu trending keywords
- Xiaohongshu SEO
- Xiaohongshu topics

## Use Cases

- Users need to obtain Xiaohongshu search suggestion terms
- Keyword research and trending topic discovery
- SEO optimization and content topic selection
- Keyword mining for competitor analysis

## Workflow

### 1. Open Xiaohongshu Explore Page

Use the browser tool to navigate to the Xiaohongshu Explore page:

```
URL: https://www.xiaohongshu.com/explore
```

### 2. Locate the Search Bar

Find the search input field on the page, typically located at the top of the page.

### 3. Input Keywords

Fill the user-provided keywords into the search bar. **Do not press Enter or click the search button.**

### 4. Collect Suggested Keywords

Wait for the auto-suggest dropdown to appear, then collect all keyword suggestions displayed in the dropdown.

### 5. Output Results

Organize the collected keyword list and present it to the user.

## Operation Examples

### Example 1: Collecting Suggestions for a Single Keyword

User request: "Help me collect Xiaohongshu search suggestions for 'skincare'"

Execution steps:
1. Open https://www.xiaohongshu.com/explore
2. Input "skincare" into the search box
3. Wait for the suggestion dropdown to appear
4. Collect all suggested keywords
5. Return the keyword list

### Example 2: Batch Collecting for Multiple Keywords

User request: "Help me collect Xiaohongshu search suggestions for the three keywords 'weight loss', 'fitness', and 'yoga'"

Execution steps:
1. Repeat the process for each keyword
2. Consolidate all collected results
3. Optional: Remove duplicates and organize by category

## Important Notes

- **Do not click the search button**: Only input keywords and collect suggestions
- **Allow time to load**: The suggestion dropdown may take 1-2 seconds to load; ensure sufficient wait time
- **Login status**: Some content may require login to view complete suggestions
- **Anti-crawling mechanisms**: If encountering captchas or restrictions, prompt the user to handle manually

## Output Format

Output format for collecting suggestions for a single keyword:

```
Keyword: [Input Keyword]
Search Suggestions:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
...
```

Output format for batch collecting multiple keywords:

```
Keyword: [Keyword 1 from batch]
Search Suggestions:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
...

Keyword: [Keyword 2 from batch]
Search Suggestions:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
...
```

## Tool Usage

This skill relies on the `browser` tool for browser automation. Ensure the browser tool is available.

## No Resources Required

This skill does not require additional scripts, reference materials, or resource files; it relies entirely on browser automation operations.