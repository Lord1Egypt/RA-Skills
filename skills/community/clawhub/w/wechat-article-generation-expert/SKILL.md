---
name: wechat-article-generation-expert
description: Automatically create complete WeChat Official Account articles (≥1600 words) based on topic, audience, and style, including title ideation, structural planning, content writing, and multimedia element planning.
---

# Wechat Article Generation Expert

Transform user-provided topics into structurally complete, word-count-compliant (≥1600 words) in-depth articles for WeChat Official Accounts.

## Use Cases

- User mentions keywords such as "Official Account article," "WeChat article," "content creation," "self-media content"
- User provides a topic and requests article generation
- User needs marketing advertorials or brand promotion content
- User requests output in a specific article format.

## Core Workflow

### 1. Information Gathering

Confirm the following elements before writing:

| Element | Description | If Not Provided by User |
|---------|-------------|-------------------------|
| Topic | Core subject of the article | Proactively ask |
| Target Audience | Reader persona (age/profession/interests) | Infer based on topic |
| Style Preference | Formal / Humorous / Approachable / Professional | Default to "Professional & Approachable" |
| Word Count Requirement | Target word count | Default to ≥1600 words |
| Special Requests | Keyword placement, advertising requirements | Skip if none |

**Example Prompt for Gathering Info**:
> "I understand you'd like an article on [Topic]. Could you tell me who the target audience is, and whether you prefer a more formal or conversational tone?"

### 2. Article Structure Planning

Standard structure (can be flexibly adjusted based on topic):

```
【Title】 Eye-catching, precise, resonant (recommended 15-25 characters)

【Introduction】 (approx. 200 words)
- Scenario lead-in / Data citation / Direct pain point address
- Spark reader interest to continue reading

【Body】 (approx. 1200 words, divided into 3-5 sections)
- Section 1: Problem presentation or phenomenon analysis
- Section 2: Underlying reasons or background interpretation
- Section 3: Solutions or actionable advice
- Section 4: Case study support or data validation (optional)
- Section 5: Elevated summary or call to action

【Conclusion】 (approx. 200 words)
- Reiterate core viewpoint
- Guide interaction (likes/comments/shares)
```

### 3. Title Ideation

**Mandatory**: Generate 3-5 alternative titles for user selection.

**High-Click-Through Title Formulas**:
- Pain Point + Solution: "Working Overtime Until 10 PM Daily? 3 Methods to Get You Home on Time"
- Data + Suspense: "90% of People Get This Wrong, What About You?"
- Counter-Intuitive: "Why Do Harder Workers Seem Less Successful?"
- Identity Affirmation: "As a Programmer, There Are Some Things I Have to Say"
- Curiosity Gap: "What Does That Colleague Who Never Works Overtime Secretly Do?"

### 4. Content Writing Key Points

**Language Style**:
- Keep paragraphs short (2-4 sentences per paragraph)
- Prefer short sentences over long, complex ones
- Use colloquial expressions appropriately
- Skillfully use numbers, contrasts, and parallel structures to enhance rhythm

**Credibility Enhancement**:
- Cite authoritative data sources
- Integrate authentic case studies
- Endorsement by expert opinions
- If specific data is unavailable, use reasonable phrasing: "Research suggests..." "Statistics indicate..."

**Multimedia Placement Annotation**:
Add descriptions where images should be inserted:
```
[Suggested image placement here: XX scene / XX data chart]
```

### 5. Quality Checklist

Self-check before delivery:
- [ ] Word count ≥ 1600 words
- [ ] 3-5 alternative titles provided
- [ ] Complete structure (Introduction-Body-Conclusion)
- [ ] Language style matches target audience
- [ ] No plagiarized content
- [ ] Special requests fulfilled (keywords/ad placements)
- [ ] Multimedia placements annotated

## Output Format

Output strictly according to the following template:

```markdown
# Basic Information
- **Article Topic**: [Topic]
- **Target Audience**: [Audience Persona]
- **Article Style**: [Style Type]
- **Word Count**: [Actual Word Count]

# Core Requirements

## Alternative Titles
1. [Title One]
2. [Title Two]
3. [Title Three]
...

## Article Content

[Introduction paragraph]

[Suggested image placement here: XXX]

[Body Section 1]

[Body Section 2]

...

[Conclusion paragraph]

# Additional Information

[If special requests exist, explain how they were handled]
[If none, state: No additional requirements]
```

## Common Scenario Handling

### Scenario 1: Broad Topic
When user provides a broad topic like "Workplace":
1. Refine the angle based on current trends or reader pain points
2. Provide 2-3 specific sub-directions for selection
3. Proceed with creation after selection

### Scenario 2: Advertorial Requirement
When user requests placement of a specific product/brand:
1. Introduce naturally through user pain points or a story
2. Position the product as the solution
3. Avoid forced sales language
4. Recommended placement is in the middle-to-latter part of the article

### Scenario 3: Keyword Optimization Required
When user specifies SEO keywords:
1. Include core keywords in the title
2. Ensure keywords appear naturally in the first paragraph
3. Maintain keyword density of 2%-5% throughout the article
4. Interweave related long-tail keywords

### Scenario 4: Insufficient Material
When user only provides a topic without detailed materials:
1. Independently conceive cases based on the topic
2. Cite public data or common knowledge
3. Use generic scenarios and personas
4. Annotate "Recommend replacing with real case study"

## Advanced Techniques

**Enhance Sense of Fulfillment**: Provide an "Action List" or "Tips" section at the end so readers feel they have gained something.

**Boost Shareability**: Craft "golden sentences" or memorable quotes suitable for readers to screenshot and share.

**Formatting Optimization Suggestions**: Remind the user to appropriately use bolding, blockquotes, and dividers to enhance readability.