# Quantum Cryptographic Seed Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `quantum-cryptographic-seed-generator`

x402 availability: not enabled for this product.

## `password`

Action slug: `password`

Price: `5` credits

Generate a secure random password with configurable character classes and ambiguity settings.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `digits` | `boolean` | no | Include digits (0-9). |
| `exclude_ambiguous` | `boolean` | no | Exclude visually ambiguous characters (0, O, 1, l, I). |
| `length` | `integer` | no | Password length in characters (8-256). |
| `lowercase` | `boolean` | no | Include lowercase letters (a-z). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. |
| `symbols` | `boolean` | no | Include punctuation symbols. |
| `uppercase` | `boolean` | no | Include uppercase letters (A-Z). |

Sample parameters:

```json
{
  "digits": true,
  "exclude_ambiguous": true,
  "length": 32,
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
    "description": "Exclude visually ambiguous characters (0, O, 1, l, I).",
    "required": false,
    "type": "boolean"
  },
  "length": {
    "default": 32,
    "description": "Password length in characters (8-256).",
    "maximum": 256,
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
    "description": "Random source: 'quantum' or 'standard'.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  },
  "symbols": {
    "default": true,
    "description": "Include punctuation symbols.",
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

## `prime`

Action slug: `prime`

Price: `5` credits

Generate one or more prime numbers of a specified bit length using Miller-Rabin primality testing.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bit_length` | `integer` | no | Bit length of each prime (128-2048). |
| `count` | `integer` | no | Number of primes to generate (1-1000). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum limit: bit_length * count <= 1900. |

Sample parameters:

```json
{
  "bit_length": 256,
  "count": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "bit_length": {
    "default": 256,
    "description": "Bit length of each prime (128-2048).",
    "maximum": 2048,
    "minimum": 128,
    "required": false,
    "type": "integer"
  },
  "count": {
    "default": 1,
    "description": "Number of primes to generate (1-1000).",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum limit: bit_length * count <= 1900.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `prime_pair`

Action slug: `prime-pair`

Price: `5` credits

Generate two distinct prime numbers suitable for RSA key generation, along with their product (n = p * q).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bit_length` | `integer` | no | Bit length of each prime (128-2048). Quantum max: 950. |
| `min_difference` | `integer` | no | Minimum numeric difference between the two primes. |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum limit: bit_length <= 950. |

Sample parameters:

```json
{
  "bit_length": 256,
  "min_difference": 100,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "bit_length": {
    "default": 256,
    "description": "Bit length of each prime (128-2048). Quantum max: 950.",
    "maximum": 2048,
    "minimum": 128,
    "required": false,
    "type": "integer"
  },
  "min_difference": {
    "default": 100,
    "description": "Minimum numeric difference between the two primes.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum limit: bit_length <= 950.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `seed`

Action slug: `seed`

Price: `5` credits

Generate a cryptographic seed with an optional timestamp certificate for verification. Supports quantum or standard random sources.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bit_length` | `integer` | no | Seed size in bits (128-2048). |
| `include_certificate` | `boolean` | no | Include a SHA-256 hash certificate with UTC timestamp for verification. |
| `source` | `string` | no | Random source: 'quantum' for hardware-derived quantum randomness, 'standard' for cryptographically secure Python secrets. |

Sample parameters:

```json
{
  "bit_length": 256,
  "include_certificate": true,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "bit_length": {
    "default": 256,
    "description": "Seed size in bits (128-2048).",
    "maximum": 2048,
    "minimum": 128,
    "required": false,
    "type": "integer"
  },
  "include_certificate": {
    "default": true,
    "description": "Include a SHA-256 hash certificate with UTC timestamp for verification.",
    "required": false,
    "type": "boolean"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' for hardware-derived quantum randomness, 'standard' for cryptographically secure Python secrets.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `token`

Action slug: `token`

Price: `5` credits

Generate a random token string in a specified character set. Suitable for API keys, session tokens, and nonces.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `charset` | `string` | no | Character set: 'alphanumeric' (letters+digits), 'hex' (0-9,a-f), 'base64' (URL-safe), 'ascii' (printable excluding whitespace). |
| `length` | `integer` | no | Token length in characters (8-256). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. |

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
    "description": "Random source: 'quantum' or 'standard'.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `uuid`

Action slug: `uuid`

Price: `5` credits

Generate one or more version-4 UUIDs using quantum or standard randomness.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of UUIDs to generate (1-1000). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. |

Sample parameters:

```json
{
  "count": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of UUIDs to generate (1-1000).",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```
