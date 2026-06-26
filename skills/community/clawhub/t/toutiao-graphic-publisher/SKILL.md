---
name: toutiao-graphic-publisher
description: Automatically publishes graphic content on Toutiao through browser automation, supporting intelligent formatting, automatic generation of popular tags, and tag activation.
---

# Toutiao Automatic Article Publishing

## Feature Overview

Automatically publishes graphic content on Toutiao through browser automation, supporting intelligent formatting, automatic generation of popular tags, and tag activation. No API keys required; uses browser automation to complete the entire process of login, content filling, tag generation, and publishing. Only QR code login requires manual operation; all other steps are fully automated.

## Trigger Scenarios
- 用户说"发布到今日头条"、"发到头条"、"自动发布头条文章"
- 用户有文章标题和内容需要发布到今日头条
- 用户需要批量发布内容到头条号
- User says "publish to Toutiao", "post to Toutiao", "automatically publish Toutiao article"
- User has article title and content to publish on Toutiao
- User needs to batch publish content to Toutiao account

## Workflow

### 1. Login Detection
- Visit https://mp.toutiao.com/profile_v4/index
- Check login status
- If not logged in, prompt user to scan QR code to log in (requires manual operation)
- Wait for login to complete

### 2. Enter Publishing Page
- Directly visit https://mp.toutiao.com/profile_v4/graphic/publish
- Wait for the editor to fully load

### 3. Content Intelligent Processing

#### 3.1 Title Recognition and Processing
- Analyze the body content to identify potential section headings
- Heading characteristics:
  - Starts with numbers (e.g., "1.", "一、", "(1)")
  - Starts with "Chapter X/Section X"
  - Short sentence at the beginning of a paragraph (within 10 characters)
  - Contains keywords (e.g., "Introduction", "Conclusion", "Summary", "Foreword")

#### 3.2 Automatically Apply Subheading Styles
Once headings are identified, automatically apply Toutiao editor's subheading styles:
- Select the heading text
- Click the editor's "H" button or select the "Subheading" style
- Ensure headings are prominently displayed

#### 3.3 Body Text Formatting Optimization
- **Paragraph Spacing**: Add blank lines between paragraphs to improve readability
- **Key Point Emphasis**: Use **bold** to highlight key sentences
- **List Optimization**: Convert enumerated content into ordered or unordered lists
- **Paragraph Splitting**: Appropriately split long paragraphs, ideally 3-5 sentences per paragraph

### 4. Automatically Generate Popular Tags

#### 4.1 Tag Analysis Dimensions
Automatically generate 3-5 popular tags based on article content:

| Analysis Dimension | Description | Example |
|---------|------|------|
| Core Theme | Main technology/field discussed in the article | OpenClaw, AI Agent |
| Industry Hotspot | Current trending topics | Artificial Intelligence, Large Language Models |
| Niche Area | Vertical application scenarios | Enterprise Intelligence, Personal Efficiency |
| Trend Prediction | Future-oriented discussions | Development Trends, Future Outlook |
| Practical Value | Value readers can gain | Tutorials, Guides, Analysis |

#### 4.2 Tag Generation Rules
```
Tag Source Priority:
1. Core words from the article title
2. Keywords from each section heading
3. Frequently occurring technical terms
4. Popular terms in related fields
5. Target audience tags
```

#### 4.3 Tag Selection Strategy
- **Mandatory Tags**: Core theme words of the article (1-2)
- **Recommended Tags**: Industry hotspot words (1-2)
- **Auxiliary Tags**: Niche area/practical value words (1)

**Number of Tags**: 3-5, no more than 5

### 5. Activate Tags

#### 5.1 Tag Input Method
- Locate the "Tags" input field on the article publishing page
- Enter the generated popular tags one by one
- Press Enter after each tag to confirm
- Wait for the system to automatically match/add

#### 5.2 Tag Activation Checklist
Checklist for tag activation:
- ✅ Whether the number of tags is within the 3-5 range
- ✅ Whether tags are relevant to the article content
- ✅ Whether popular tags have search volume
- ✅ Avoid duplicate or similar tags

#### 5.3 Tag Optimization Suggestions
- Prioritize tags with search volume
- Use long-tail tags as supplements
- Avoid tags that are too broad or too specialized
- Reference popular topics at the end of articles

### 6. Content Filling
- **Title**: Fill in the user-provided title in the title input field (2-30 characters)
- **Body Text**: Fill in the content after intelligent formatting processing
- **Tags**: Fill in and activate the automatically generated popular tags
- **Display Cover**: Select no cover

### 7. Execute Publishing
- Click the "Preview and Publish" button
- When the preview pop-up appears, click the "Confirm Publish" button
- Click the "Confirm Publish" button

## Intelligent Tag System

### Tag Combination Strategy

| Article Type | Tag Combination Example |
|---------|------------|
| Technical Tutorial | Core Tool + Operation Method + Practical Value |
| Trend Analysis | Industry Hotspot + Core Theme + Future Trend |
| Product Review | Product Name + Core Features + Application Scenarios |
| Experience Sharing | Core Experience + Target Audience + Outcome Value |

## Intelligent Formatting Rules

### Heading Recognition Rules
```
Primary Heading Characteristics:
- Format: 一、二、三... or 1. 2. 3... or Chapter 1/Section 1
- Position: Beginning of paragraph
- Length: Typically 2-10 characters

Secondary Heading Characteristics:
- Format: (一)(二) or 1.1 1.2 or ① ②
- Position: Beginning of paragraph
- Length: Typically 2-15 characters

Keyword Headings:
- Introduction/Foreword/Preface
- Conclusion/Summary/Closing Remarks
- Background/Overview/Brief Introduction
- Methods/Analysis/Discussion
```

### Formatting Beautification Rules
1. **Heading Hierarchy**: Use "Subheading" style for primary headings, use **bold** for secondary headings
2. **Paragraph Optimization**: Keep each paragraph to 100-200 characters, split if too long
3. **Key Point Emphasis**: Use **bold** for core viewpoints, data, and conclusions
4. **List Conversion**: Convert 3 or more parallel items into list format
5. **Blank Line Handling**: Maintain appropriate blank lines before and after headings, and between paragraphs

## Usage Instructions

Users need to provide:
- **Title**: Article title (2-30 characters) (required)
- **Body Text**: Article content (required)

## Important Notes

1. **Login Status**: QR code login is required for first-time use or when cookies expire
2. **Content Compliance**: Adhere to Toutiao community guidelines; avoid violating content
3. **Tag Selection**: Choose tags highly relevant to the article; avoid stacking irrelevant tags
4. **Frequency Limits**: Avoid publishing multiple articles in a short period; it is recommended to wait at least 5 minutes between publications
5. **Formatting Check**: It is recommended to preview and check the formatting effect and tag display after publishing

## Error Handling

- Login Failure: Prompt user to rescan the QR code
- Publishing Failure: Check network connection, retry, or provide specific error information
- Content Violation: Prompt user to modify content and retry
- Formatting Anomaly: Check if the editor loaded correctly; refresh the page and retry if necessary
- Tags Cannot Be Activated: Manually check if the tag input field was filled in correctly