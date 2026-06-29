# Quantum Secure Token Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `quantum-secure-token-generator`

x402 availability: not enabled for this product.

## `generate`

Action slug: `generate`

Price: `5` credits

Generate a secure random token with configurable length and character set using quantum or standard randomness. Suitable for API keys, session tokens, and password reset links.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `charset` | `string` | no | Character set: 'alphanumeric' (letters+digits), 'hex' (0-9,a-f), 'base64' (URL-safe), 'ascii' (printable excluding whitespace). |
| `length` | `integer` | no | Token length in characters (8-256). |
| `source` | `string` | no | Random source: 'quantum' (CURBy quantum RNG) or 'standard' (Python secrets module). |

Sample parameters:

```json
{
  "charset": "alphanumeric",
  "length": 32,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "charset": {
    "default": "alphanumeric",
    "description": "Character set: 'alphanumeric' (letters+digits), 'hex' (0-9,a-f), 'base64' (URL-safe), 'ascii' (printable excluding whitespace).",
    "enum": [
      "alphanumeric",
      "hex",
      "base64",
      "ascii"
    ],
    "required": false,
    "type": "string"
  },
  "length": {
    "default": 32,
    "description": "Token length in characters (8-256).",
    "maximum": 256,
    "minimum": 8,
    "required": false,
    "type": "integer"
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
  }
}
```
