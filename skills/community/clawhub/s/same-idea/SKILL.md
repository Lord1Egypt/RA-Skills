---
name: same-idea
description: Find similar ideas and resonating quotes from user's reading notes and knowledge base. Use when user wants to discover connections between a new idea/concept and their existing knowledge. Input can be a thought, concept, or a quote from a book. The skill searches through user's notes (Logseq/Obsidian vault) to find similar ideas, resonating quotes, or related concepts, then returns matching quotes with their sources (book title, author, or person).
---

# Same Idea - 共鸣发现

Find similar ideas and resonating quotes from user's reading notes and knowledge base.

## When to Use

- User shares a thought or idea from reading
- User wants to find similar concepts in their existing notes
- User wants to discover connections between new and existing knowledge
- User wants to find quotes that resonate with a given concept

## Input

A thought, concept, or quote from a book. Examples:
- "真正的自由是自律的结果"
- "复利效应不仅适用于金钱，也适用于知识和关系"
- A passage the user is currently reading

## Workflow

1. **Parse the input idea**
   - Extract core concepts and keywords
   - Identify the main theme or insight

2. **Search knowledge base**
   - Search Logseq vault: `~/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/`
   - Search Obsidian vault: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`
   - Look for similar concepts, related ideas, or resonating quotes

3. **Match and rank results**
   - Semantic similarity matching
   - Prioritize direct quotes with clear attribution
   - Rank by relevance and resonance

4. **Output format**
   ```
   ## 输入想法
   [User's input]

   ## 共鸣发现

   ### 1. [Quote/Concept]
   > "[The matching quote or similar idea]"
   
   **来源**: [Book Title] - [Author] / [Person]
   **共鸣点**: [Brief explanation of why this resonates]

   ### 2. [Quote/Concept]
   ...
   ```

## Search Strategy

### Primary Sources (in order)
1. **Logseq Journals** - Daily notes and fleeting thoughts
2. **Logseq Pages** - Permanent notes and concept pages
3. **Obsidian Reading Notes** - Book highlights and summaries
4. **Obsidian Literature Notes** - Processed reading notes

### Search Techniques
- Use `grep` or `rg` for keyword matching
- Look for:
  - Same keywords or synonyms
  - Related concepts
  - Similar metaphors or examples
  - Quotes that express the same insight differently

### Matching Criteria
- **Strong match**: Direct semantic equivalence
- **Medium match**: Related concept or supporting idea
- **Weak match**: Tangential connection worth noting

## Output Guidelines

- Return top 3-5 most resonating matches
- Always include source attribution (book/person)
- Briefly explain the resonance/connection
- If no strong matches found, suggest related concepts to explore
- Be honest when no good matches exist

## Example

**Input**: "复利效应不仅适用于金钱，也适用于知识和关系"

**Output**:
```
## 输入想法
复利效应不仅适用于金钱，也适用于知识和关系

## 共鸣发现

### 1. 知识复利
> "每天进步1%，一年后你会进步37倍"

**来源**: 《掌控习惯》 - 詹姆斯·克利尔
**共鸣点**: 强调微小积累的巨大效应，与你提到的知识复利概念一致

### 2. 关系投资
> "人际关系就像银行账户，需要持续存款"

**来源**: 《高效能人士的七个习惯》 - 史蒂芬·柯维
**共鸣点**: 将关系视为需要长期投入的资产，与复利思维相通
```
