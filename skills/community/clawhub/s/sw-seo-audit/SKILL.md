# SEO Audit Skill

## Trigger
When the user wants to audit a page or site for SEO issues, check metadata, review headings structure, or identify content gaps.

**Trigger phrases:** "SEO audit", "check SEO", "audit this page", "metadata check", "why isn't this ranking", "SEO issues"

## Process

1. **Fetch**: Load the target URL and extract HTML structure
2. **Technical audit**: Check metadata, headings, images, links, schema
3. **Content audit**: Assess keyword targeting, content depth, readability
4. **Competitor check**: Compare against top 3 ranking pages for target keyword
5. **Report**: Prioritised issues with specific fixes

## Audit Checklist

### Technical
- [ ] Title tag: present, unique, 50-60 chars, includes target keyword
- [ ] Meta description: present, 150-160 chars, compelling, includes keyword
- [ ] H1: exactly one, includes primary keyword
- [ ] H2-H6: logical hierarchy, include related keywords
- [ ] Images: all have alt text, descriptive filenames, appropriate sizes
- [ ] Internal links: at least 3 relevant internal links
- [ ] External links: at least 1-2 authoritative outbound links
- [ ] URL: clean, readable, includes keyword
- [ ] Schema markup: appropriate type (Article, Product, FAQ, etc.)
- [ ] Canonical tag: present and correct
- [ ] OG/Twitter meta tags: present with image

### Content
- [ ] Word count: appropriate for topic (compare to ranking competitors)
- [ ] Keyword density: natural usage, not stuffed
- [ ] Content structure: scannable, uses lists and subheadings
- [ ] Freshness: content is current and accurate
- [ ] Unique value: offers something competitors don't
- [ ] Media: includes images, diagrams, or video where appropriate

## Output Format

```markdown
# SEO Audit: [URL]

## Score: [X/100]

## Critical Issues (fix immediately)
1. [Issue] — [specific fix]

## Warnings (fix this week)
1. [Issue] — [specific fix]

## Opportunities (improve ranking)
1. [Opportunity] — [how to implement]

## Competitor Comparison
| Factor | Your Page | Competitor 1 | Competitor 2 |
|--------|-----------|-------------|-------------|
...

## Recommended Actions (prioritised)
1. [Action] — Est. impact: [High/Medium/Low]
```

## Rules
- Always provide specific, actionable fixes — not generic advice
- Prioritise by impact: title tag fix > alt text fix
- Compare against actual competitors, not abstract best practices
- Flag quick wins separately from long-term improvements
