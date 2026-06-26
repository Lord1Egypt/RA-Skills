# Rynjer Image Generation for Agents — Tool Schema Draft

## rewrite_image_prompt

```json
{
  "type": "object",
  "properties": {
    "goal": { "type": "string" },
    "raw_prompt": { "type": "string" },
    "use_case": {
      "type": "string",
      "enum": ["landing", "product", "blog", "social", "ad"]
    },
    "tone": { "type": "string" },
    "audience": { "type": "string" }
  },
  "required": ["goal", "raw_prompt", "use_case"]
}
```

## estimate_image_cost

```json
{
  "type": "object",
  "properties": {
    "use_case": {
      "type": "string",
      "enum": ["landing", "product", "blog", "social", "ad"]
    },
    "count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 8
    },
    "resolution": {
      "type": "string",
      "enum": ["1K", "2K", "4K"]
    },
    "aspect_ratio": {
      "type": "string",
      "enum": ["1:1", "16:9", "4:5", "3:2"]
    },
    "quality_mode": {
      "type": "string",
      "enum": ["fast", "balanced", "high"]
    },
    "price_version": {
      "type": "string"
    }
  },
  "required": ["use_case", "count", "resolution", "quality_mode"]
}
```

## generate_image

```json
{
  "type": "object",
  "properties": {
    "goal": { "type": "string" },
    "prompt": { "type": "string" },
    "use_case": {
      "type": "string",
      "enum": ["landing", "product", "blog", "social", "ad"]
    },
    "aspect_ratio": {
      "type": "string",
      "enum": ["1:1", "16:9", "4:5", "3:2"]
    },
    "resolution": {
      "type": "string",
      "enum": ["1K", "2K", "4K"]
    },
    "quality_mode": {
      "type": "string",
      "enum": ["fast", "balanced", "high"]
    },
    "count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4
    },
    "scene": {
      "type": "string",
      "enum": ["text-to-image", "image-to-image"]
    },
    "request_id": {
      "type": "string"
    },
    "auto_poll": {
      "type": "boolean"
    },
    "poll_attempts": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20
    },
    "poll_interval_ms": {
      "type": "integer",
      "minimum": 100,
      "maximum": 60000
    },
    "model_override": {
      "type": "string",
      "description": "Optional advanced override. Not recommended for most agents."
    }
  },
  "required": ["prompt", "use_case", "quality_mode", "count"]
}
```

## poll_image_result

```json
{
  "type": "object",
  "properties": {
    "request_id": { "type": "string" }
  },
  "required": ["request_id"]
}
```
