# Contributing to TweetNugget

TweetNugget curates inspirational quotes and wisdom from Twitter/X. This document explains how to contribute to this OpenClaw skill.

## Ways to Contribute

### Add New Quote Collections
Create new JSON collections with quotes from specific sources, themes, or time periods.

### Add Quotes to Existing Collections
Expand existing collections with additional relevant quotes.

### Fix Typos and Improve Quality
- Correct spelling and grammar errors
- Fix broken links
- Update outdated information
- Improve formatting consistency

### Improve the Skill
- Suggest new features or enhancements
- Report bugs
- Improve documentation

## Adding a New Quote Collection

Create a new JSON file in the `references/` directory with the following structure:

```json
{
  "name": "Collection Name",
  "description": "Brief description of the collection",
  "quotes": [
    {
      "text": "The quote text",
      "author": "@handle",
      "url": "https://x.com/...",
      "category": "Category Label",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### Required Fields
- `text`: The quote content
- `author`: Twitter/X handle with @ prefix

### Optional Fields
- `url`: Direct link to the tweet
- `category`: Classification (e.g., "Philosophy", "Career", "Leadership")
- `tags`: Array of relevant keywords for filtering

### Naming Convention
Use lowercase with hyphens: `collection-name.json`

### Examples
See existing files in `references/` for reference:
- `twitter-quotes.json`
- `stoic-quotes.json`
- `swlw-tweets.json`

## Adding Quotes to Existing Collections

1. Open the target JSON file in `references/`
2. Add new quote objects to the `quotes` array
3. Maintain the same structure and formatting
4. Ensure proper JSON syntax (comma after objects except last)

```json
{
  "name": "Twitter Wisdom",
  "description": "Curated quotes sourced from Twitter/X",
  "quotes": [
    {
      "text": "Existing quote",
      "author": "@handle"
    },
    {
      "text": "New quote to add",
      "author": "@newhandle",
      "tags": ["new", "wisdom"]
    }
  ]
}
```

## Guidelines for Quotes

### Quality Standards
- **Must be real quotes**: No fabrications, paraphrasing, or fictional quotes
- **Include attribution**: Always include the original author's @handle
- **Verify sources**: Ensure quotes are authentic and accurately attributed
- **Check links**: URLs should link to actual tweets (when provided)

### Content Guidelines
- Focus on inspirational, educational, or thought-provoking content
- Avoid controversial, offensive, or low-quality content
- Maintain diversity of perspectives and sources
- Ensure quotes are timeless or highly relevant

### Formatting
- Keep quotes concise and impactful
- Use proper punctuation and capitalization
- Preserve original wording (don't improve or alter quotes)
- Include relevant tags for categorization

## Testing Changes

### Running Tests
Use the provided test script to validate your changes:

```bash
python3 test_skill.py
```

### Test Coverage
The test suite checks:
- JSON parsing validity
- Random selection variety
- Tag filtering functionality
- Edge case handling

### Test Results
- Green: PASS - Test passed
- Red: FAIL - Test failed (fix before submitting)
- Yellow: WARN - Warning (review but usually acceptable)

## Pull Request Process

### Before Submitting
1. Run `python3 test_skill.py` to ensure all tests pass
2. Check JSON syntax with a linter or editor
3. Verify quote authenticity and attribution
4. Review for typos and formatting consistency

### Pull Request Template
When creating a PR:
1. Clear title: "Add [Collection Name] quotes" or "Fix typo in [file]"
2. Brief description: What was changed and why
3. Link to specific tweets when adding new quotes
4. Note any tests that were modified

### Review Process
1. PRs will be reviewed for quality and accuracy
2. Quotes must be verified as authentic
3. Collections should add value to the project
4. Formatting must match existing style

### After Approval
- PR will be merged automatically by maintainers
- Changes will be included in the next release

## Maintaining Quality

### Collection Guidelines
- Each collection should have a clear theme
- Maintain consistent quality across collections
- Avoid duplicate quotes across collections
- Include a reasonable number of quotes (5-20 per collection)

### Tagging Best Practices
- Use 2-4 relevant tags per quote
- Keep tags concise and lowercase
- Use existing tags when possible
- Avoid overly specific tags

### Attribution Requirements
- Always preserve the original author's @handle
- Include tweet URLs when available
- Don't attribute quotes to the wrong person
- Mark adaptations or compilations clearly

## Questions or Help

For questions about contributing:
- Check existing collections for examples
- Review the test script for validation rules
- Submit an issue with the "question" label

Thank you for helping make TweetNugget a valuable resource for inspiration and wisdom!