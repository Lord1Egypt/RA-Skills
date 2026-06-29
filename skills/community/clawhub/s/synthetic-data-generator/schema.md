# Synthetic Data Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `synthetic-data-generator`

x402 availability: not enabled for this product.

## `generate`

Action slug: `generate`

Price: `10` credits

Generate synthetic data of a specified type. Supports person profiles, company profiles, family units, technical data, financial data, edge cases, and complete relational datasets (e-commerce, auth system, CRM).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of records to generate (1-1000). For simple types this is exact record count. For dataset types, this affects the size multiplier. |
| `data_type` | `string` | yes | Type of synthetic data to generate. Options: 'person' (individual profiles with names, emails, addresses, demographics), 'company' (business profiles with industry, size, revenue, employees), 'family' (related family units with parents, children, shared addresses), 'technical' (IPs, UUIDs, URLs, domains, API keys), 'financial' (credit cards, bank accounts, transactions), 'edge_cases' (unicode, special chars, injection patterns for security testing), 'ecommerce_dataset' (customers, products, orders, reviews), 'auth_system_dataset' (users, roles, permissions, sessions), 'crm_dataset' (companies, contacts, deals, pipeline). |
| `include_details` | `boolean` | no | Include extended details in generated data. For 'person': adds addresses, contact info, occupation. For 'company': adds employee lists. For 'family': adds relationship mappings. For datasets: includes all relationships. Set to false for minimal data. |
| `include_edge_cases` | `boolean` | no | Mix in edge case data for robustness testing. Adds unicode characters, special characters, long strings, boundary values. Works with all data types. |
| `locale` | `string` | no | Locale for region-specific data generation (names, addresses, phone formats). Supports: en_US, en_GB, de_DE, fr_FR, es_ES, it_IT, pt_BR, nl_NL, pl_PL, ja_JP. |
| `options` | `object` | no | Advanced type-specific options. Available by data_type: [person] age_range, [company] industry_filter/size_category, [family] family_size_range, [technical] data_types, [financial] currency/include_transactions, [edge_cases] severity_level/categories. |
| `seed` | `integer` | no | Random seed for reproducible results. Same seed + same parameters = same data every time. Omit for random data each request. |
| `size` | `string` | no | Dataset size - ONLY for dataset types (ecommerce_dataset, auth_system_dataset, crm_dataset). 'small': ~100 records, 'medium': ~500 records, 'large': ~2000+ records. Ignored for non-dataset types. |

Sample parameters:

```json
{
  "count": 1,
  "data_type": "person",
  "include_details": true,
  "include_edge_cases": false,
  "locale": "en_US",
  "options": {
    "age_range": [
      0
    ],
    "categories": [
      "unicode"
    ],
    "currency": "USD",
    "data_types": [
      "ip"
    ],
    "family_size_range": [
      2
    ],
    "include_transactions": false,
    "industry_filter": "Technology",
    "severity_level": "medium"
  },
  "seed": 1,
  "size": "medium"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of records to generate (1-1000). For simple types this is exact record count. For dataset types, this affects the size multiplier.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "data_type": {
    "description": "Type of synthetic data to generate. Options: 'person' (individual profiles with names, emails, addresses, demographics), 'company' (business profiles with industry, size, revenue, employees), 'family' (related family units with parents, children, shared addresses), 'technical' (IPs, UUIDs, URLs, domains, API keys), 'financial' (credit cards, bank accounts, transactions), 'edge_cases' (unicode, special chars, injection patterns for security testing), 'ecommerce_dataset' (customers, products, orders, reviews), 'auth_system_dataset' (users, roles, permissions, sessions), 'crm_dataset' (companies, contacts, deals, pipeline).",
    "enum": [
      "person",
      "company",
      "family",
      "technical",
      "financial",
      "edge_cases",
      "ecommerce_dataset",
      "auth_system_dataset",
      "crm_dataset"
    ],
    "required": true,
    "type": "string"
  },
  "include_details": {
    "default": true,
    "description": "Include extended details in generated data. For 'person': adds addresses, contact info, occupation. For 'company': adds employee lists. For 'family': adds relationship mappings. For datasets: includes all relationships. Set to false for minimal data.",
    "required": false,
    "type": "boolean"
  },
  "include_edge_cases": {
    "default": false,
    "description": "Mix in edge case data for robustness testing. Adds unicode characters, special characters, long strings, boundary values. Works with all data types.",
    "required": false,
    "type": "boolean"
  },
  "locale": {
    "default": "en_US",
    "description": "Locale for region-specific data generation (names, addresses, phone formats). Supports: en_US, en_GB, de_DE, fr_FR, es_ES, it_IT, pt_BR, nl_NL, pl_PL, ja_JP.",
    "enum": [
      "en_US",
      "en_GB",
      "de_DE",
      "fr_FR",
      "es_ES",
      "it_IT",
      "pt_BR",
      "nl_NL",
      "pl_PL",
      "ja_JP"
    ],
    "required": false,
    "type": "string"
  },
  "options": {
    "description": "Advanced type-specific options. Available by data_type: [person] age_range, [company] industry_filter/size_category, [family] family_size_range, [technical] data_types, [financial] currency/include_transactions, [edge_cases] severity_level/categories.",
    "properties": {
      "age_range": {
        "description": "[person only] Age range as [min_age, max_age]. Example: [25, 65].",
        "items": {
          "maximum": 120,
          "minimum": 0,
          "type": "integer"
        },
        "maxItems": 2,
        "minItems": 2,
        "required": false,
        "type": "array"
      },
      "categories": {
        "description": "[edge_cases only] Categories to generate.",
        "items": {
          "enum": [
            "unicode",
            "length",
            "null",
            "boundary",
            "malformed",
            "injection",
            "special_chars",
            "numeric"
          ],
          "type": "string"
        },
        "required": false,
        "type": "array"
      },
      "currency": {
        "default": "USD",
        "description": "[financial only] ISO 4217 currency code. Default: USD.",
        "required": false,
        "type": "string"
      },
      "data_types": {
        "description": "[technical only] Technical data types to include.",
        "items": {
          "enum": [
            "ip",
            "ipv6",
            "mac",
            "uuid",
            "url",
            "domain",
            "email",
            "user_agent",
            "api_key",
            "token"
          ],
          "type": "string"
        },
        "required": false,
        "type": "array"
      },
      "family_size_range": {
        "description": "[family only] Family size range as [min, max]. Default: [2, 6].",
        "items": {
          "maximum": 10,
          "minimum": 2,
          "type": "integer"
        },
        "maxItems": 2,
        "minItems": 2,
        "required": false,
        "type": "array"
      },
      "include_transactions": {
        "default": false,
        "description": "[financial only] Include transaction history. Default: false.",
        "required": false,
        "type": "boolean"
      },
      "industry_filter": {
        "description": "[company only] Filter to specific industry.",
        "enum": [
          "Technology",
          "Healthcare",
          "Finance",
          "Manufacturing",
          "Retail",
          "Education"
        ],
        "required": false,
        "type": "string"
      },
      "severity_level": {
        "default": "medium",
        "description": "[edge_cases only] Severity: low, medium, high.",
        "enum": [
          "low",
          "medium",
          "high"
        ],
        "required": false,
        "type": "string"
      },
      "size_category": {
        "description": "[company only] Company size: small (1-50), medium (51-500), large (501-5000), enterprise (5000+).",
        "enum": [
          "small",
          "medium",
          "large",
          "enterprise"
        ],
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "seed": {
    "description": "Random seed for reproducible results. Same seed + same parameters = same data every time. Omit for random data each request.",
    "required": false,
    "type": "integer"
  },
  "size": {
    "default": "medium",
    "description": "Dataset size - ONLY for dataset types (ecommerce_dataset, auth_system_dataset, crm_dataset). 'small': ~100 records, 'medium': ~500 records, 'large': ~2000+ records. Ignored for non-dataset types.",
    "enum": [
      "small",
      "medium",
      "large"
    ],
    "required": false,
    "type": "string"
  }
}
```
