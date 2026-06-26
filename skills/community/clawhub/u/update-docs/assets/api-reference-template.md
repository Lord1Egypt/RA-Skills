---
title: API Reference Template
description: Template for OpenClaw API reference documentation.
---

{/* The content of this doc is shared between different contexts. You can use specific components to add context-specific content if needed. */}

Brief introduction to the API feature.

## Reference

### Props/Parameters

<div style={{ overflowX: 'auto', width: '100%' }}>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paramName` | string | Yes | Description of the parameter |

</div>

#### `paramName`

Detailed description of the parameter.

```typescript filename="example.ts"
// TypeScript example
const result = apiFunction({
  paramName: "value"
});
```

```javascript filename="example.js"
// JavaScript example  
const result = apiFunction({
  paramName: "value"
});
```

## Examples

### Basic Usage

```typescript filename="basic-usage.ts"
// Basic usage example
```

### Advanced Usage

```typescript filename="advanced-usage.ts"
// Advanced usage example
```

## Related

- [Related API](../related-api)
- [Guide](../../guides/related-guide)