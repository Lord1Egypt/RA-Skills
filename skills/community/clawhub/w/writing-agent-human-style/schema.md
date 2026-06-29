# Writing Agent - Human Style Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `writing-agent-human-style`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `draft_large_blog_post`

Action slug: `draft-large-blog-post`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/writing-agent-human-style/actions/draft-large-blog-post/invoke`

Price: `50` credits

Generate one larger blog post in Markdown from a topic, character limit, and optional JSON context. Provide max_characters from 100 to 30,000.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `object` | no | Optional JSON object with outline, writing guidance, and source context. Suggested keys: outline, voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement. |
| `max_characters` | `integer` | yes | Maximum characters for returned Markdown. Required. Must be 100 to 30,000. |
| `topic` | `string` | yes | Topic to write about. Required. |

Sample parameters:

```json
{
  "context": {},
  "max_characters": 100,
  "topic": "example topic"
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "Optional JSON object with outline, writing guidance, and source context. Suggested keys: outline, voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement.",
    "required": false,
    "type": "object"
  },
  "max_characters": {
    "description": "Maximum characters for returned Markdown. Required. Must be 100 to 30,000.",
    "maximum": 30000,
    "minimum": 100,
    "required": true,
    "type": "integer"
  },
  "topic": {
    "description": "Topic to write about. Required.",
    "required": true,
    "type": "string"
  }
}
```

## `draft_short_blog_post`

Action slug: `draft-short-blog-post`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/writing-agent-human-style/actions/draft-short-blog-post/invoke`

Price: `30` credits

Generate one short-form blog post in Markdown from a topic, character limit, and optional JSON context. Provide max_characters from 100 to 12,000.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `object` | no | Optional JSON object with outline, writing guidance, and source context. Suggested keys: outline, voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement. |
| `max_characters` | `integer` | yes | Maximum characters for returned Markdown. Required. Must be 100 to 12,000. |
| `topic` | `string` | yes | Topic to write about. Required. |

Sample parameters:

```json
{
  "context": {},
  "max_characters": 100,
  "topic": "example topic"
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "Optional JSON object with outline, writing guidance, and source context. Suggested keys: outline, voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement.",
    "required": false,
    "type": "object"
  },
  "max_characters": {
    "description": "Maximum characters for returned Markdown. Required. Must be 100 to 12,000.",
    "maximum": 12000,
    "minimum": 100,
    "required": true,
    "type": "integer"
  },
  "topic": {
    "description": "Topic to write about. Required.",
    "required": true,
    "type": "string"
  }
}
```

## `draft_social_post`

Action slug: `draft-social-post`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/writing-agent-human-style/actions/draft-social-post/invoke`

Price: `10` credits

Generate one original social media post from a topic, character limit, and optional JSON context.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `object` | no | Optional JSON object with writing guidance and source context. Suggested keys: voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement. |
| `max_characters` | `integer` | yes | Maximum characters for the generated social post. Required. Must be 1 to 5,000. |
| `topic` | `string` | yes | Topic to write about. Required. |

Sample parameters:

```json
{
  "context": {},
  "max_characters": 1,
  "topic": "example topic"
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "Optional JSON object with writing guidance and source context. Suggested keys: voice, goal, audience, instructions, source_material, brand_context, examples, constraints, desired_structure. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement.",
    "required": false,
    "type": "object"
  },
  "max_characters": {
    "description": "Maximum characters for the generated social post. Required. Must be 1 to 5,000.",
    "maximum": 5000,
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "topic": {
    "description": "Topic to write about. Required.",
    "required": true,
    "type": "string"
  }
}
```

## `draft_social_responses`

Action slug: `draft-social-responses`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/writing-agent-human-style/actions/draft-social-responses/invoke`

Price: `20` credits

Generate one short brand-appropriate social media response for each supplied post, up to ten posts per request.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `object` | no | Optional JSON object with shared writing guidance and source context. Suggested keys: voice, goal, audience, instructions, source_material, brand_context, examples, constraints. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement. |
| `max_characters_per_response` | `integer` | yes | Maximum characters for each generated response. Required. Must be 1 to 500. |
| `posts` | `array` | yes | Social posts to respond to. Required. Provide 1 to 10 posts; one response is generated for each post. |

Sample parameters:

```json
{
  "context": {},
  "max_characters_per_response": 1,
  "posts": [
    {
      "content": "Draft marketing copy to check for banned phrases.",
      "post_id": "example post id"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "Optional JSON object with shared writing guidance and source context. Suggested keys: voice, goal, audience, instructions, source_material, brand_context, examples, constraints. Must serialize to no more than 40,000 characters; combined topic/posts/context input is limited to 85,000 characters before final prompt budget enforcement.",
    "required": false,
    "type": "object"
  },
  "max_characters_per_response": {
    "description": "Maximum characters for each generated response. Required. Must be 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "posts": {
    "description": "Social posts to respond to. Required. Provide 1 to 10 posts; one response is generated for each post.",
    "items": {
      "properties": {
        "content": {
          "description": "Source post content to respond to. Required.",
          "maxLength": 5000,
          "minLength": 1,
          "required": true,
          "type": "string"
        },
        "post_id": {
          "description": "Optional caller-provided post identifier, echoed back in response metadata.",
          "maxLength": 120,
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "minItems": 1,
    "required": true,
    "type": "array"
  }
}
```
