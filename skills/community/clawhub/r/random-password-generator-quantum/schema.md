# Random Password Generator Quantum Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `random-password-generator-quantum`

x402 availability: not enabled for this product.

## `generate`

Action slug: `generate`

Price: `5` credits

Generate a secure random password with configurable length, character types, and ambiguity settings using quantum or standard randomness.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `digits` | `boolean` | no | Include digits (0-9). |
| `exclude_ambiguous` | `boolean` | no | Exclude visually ambiguous characters (0, O, 1, l, I). Recommended for manually typed passwords. |
| `length` | `integer` | no | Password length in characters (8-128). |
| `lowercase` | `boolean` | no | Include lowercase letters (a-z). |
| `source` | `string` | no | Random source: 'quantum' (CURBy quantum RNG) or 'standard' (Python secrets module). |
| `symbols` | `boolean` | no | Include symbols/punctuation characters. |
| `uppercase` | `boolean` | no | Include uppercase letters (A-Z). |

Sample parameters:

```json
{
  "digits": true,
  "exclude_ambiguous": true,
  "length": 16,
  "lowercase": true,
  "source": "quantum",
  "symbols": true,
  "uppercase": true
}
```

Generated JSON parameter schema:

```json
{
  "digits": {
    "default": true,
    "description": "Include digits (0-9).",
    "required": false,
    "type": "boolean"
  },
  "exclude_ambiguous": {
    "default": true,
    "description": "Exclude visually ambiguous characters (0, O, 1, l, I). Recommended for manually typed passwords.",
    "required": false,
    "type": "boolean"
  },
  "length": {
    "default": 16,
    "description": "Password length in characters (8-128).",
    "maximum": 128,
    "minimum": 8,
    "required": false,
    "type": "integer"
  },
  "lowercase": {
    "default": true,
    "description": "Include lowercase letters (a-z).",
    "required": false,
    "type": "boolean"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' (CURBy quantum RNG) or 'standard' (Python secrets module).",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  },
  "symbols": {
    "default": true,
    "description": "Include symbols/punctuation characters.",
    "required": false,
    "type": "boolean"
  },
  "uppercase": {
    "default": true,
    "description": "Include uppercase letters (A-Z).",
    "required": false,
    "type": "boolean"
  }
}
```
