# Tabstack Examples

JSON schema examples and generate instructions for common use cases.

## extract-json Schemas

### News/blog article list

```json
{
  "type": "object",
  "properties": {
    "articles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string" },
          "url": { "type": "string" },
          "author": { "type": "string" },
          "date": { "type": "string" }
        }
      }
    }
  }
}
```

### Product details

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "price": { "type": "number" },
    "currency": { "type": "string" },
    "availability": { "type": "string" },
    "rating": { "type": "number" },
    "review_count": { "type": "integer" },
    "description": { "type": "string" }
  }
}
```

### Table/comparison data

```json
{
  "type": "object",
  "properties": {
    "headers": {
      "type": "array",
      "items": { "type": "string" }
    },
    "rows": {
      "type": "array",
      "items": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  }
}
```

### Event listing

```json
{
  "type": "object",
  "properties": {
    "events": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "date": { "type": "string" },
          "time": { "type": "string" },
          "location": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    }
  }
}
```

### Contact/people directory

```json
{
  "type": "object",
  "properties": {
    "people": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "title": { "type": "string" },
          "email": { "type": "string" },
          "phone": { "type": "string" }
        }
      }
    }
  }
}
```

## generate Instructions

Effective instructions are specific about what to produce and how to transform the source content.

### Summarize and categorize

Schema: `{stories: [{title, category, summary}]}`

> "For each story on the page, categorize it as tech/business/science/politics/other and write a one-sentence summary."

### Sentiment analysis

Schema: `{reviews: [{text, sentiment, score}]}`

> "For each review, determine the sentiment (positive/negative/neutral) and assign a score from 1-5."

### Extract and reformat

Schema: `{recipes: [{name, prep_time, ingredients, steps}]}`

> "Extract all recipes from this page. List ingredients as an array of strings. Summarize each step in one sentence."

### Competitive analysis

Schema: `{products: [{name, price, pros, cons, verdict}]}`

> "Compare the products on this page. For each, list 2-3 pros and cons, then give a one-sentence verdict."

### Content digest

Schema: `{digest: {title, key_points, action_items, tldr}}`

> "Create a digest of this page. Extract 3-5 key points as bullet-length strings, any action items mentioned, and a single-sentence TLDR."
