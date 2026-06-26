# Template Schema Details

This document expands on the template fields and how auto-registration works.

## Required fields
- `name`: action name, used as `/actions/:name`
- `host`: RapidAPI host
- `path`: endpoint path starting with `/`
- `method`: HTTP method

## Optional fields
- `label`, `description`: human-friendly metadata
- `querySchema`, `bodySchema`, `pathParams`, `headerSchema`
  - An object whose keys are input fields
  - Each field supports:
    - `type`: `string | number | boolean | object | array`
    - `required`: `true | false`
    - `default`: default value if not provided
    - `description`: free text
- `headers`: static headers applied to every call
- `paramMapping`: map input fields to request locations
- `response`: response shaping rules
- `timeoutMs`: per-action timeout override
- `enabled`: set to `false` to skip registration
- `tags`, `version`: metadata

## paramMapping syntax
`paramMapping` lets you map a single input field into a specific request bucket.

Example:
```json
"paramMapping": {
  "profileUrl": "query.url",
  "companyId": "path.id",
  "lang": "header.Accept-Language"
}
```

Valid buckets:
- `query.<name>`
- `body.<name>`
- `path.<name>`
- `header.<name>`

## Path params
`path` supports `{param}` tokens that will be replaced using `pathParams` or `paramMapping`.

Example:
```json
"path": "/company/{id}",
"pathParams": {"id": {"type": "string", "required": true}}
```

## Response shaping
- `response.type`: `json | text | blob`
- `response.dataPath`: dot path to extract a sub-field
- `response.errorPath`: dot path for error payload detection
- `response.normalize`: a map of output keys to dot paths

Example:
```json
"response": {
  "type": "json",
  "normalize": {
    "name": "data.profile.name",
    "title": "data.profile.headline"
  }
}
```

If `normalize` is provided, it overrides `dataPath`.

## Auto-registration rules
- Every `templates/*.json` file is loaded at startup
- Templates with `enabled: false` are skipped
- Each template becomes one action at `/actions/:name`
- `GET /actions` lists the registered actions and schemas
