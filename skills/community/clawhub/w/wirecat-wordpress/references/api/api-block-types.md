<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: block-types

## `wordpress api block-types-get [options]`

- What: getWpV2BlockTypesByNamespaceByName — read (GET…
- Call: `GET /wp/v2/block-types/{namespace}/{name}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--namespace <value>` | yes | namespace |
| `--name <value>` | yes | name |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api block-types-list [options]`

- What: getWpV2BlockTypes — read (GET /wp/v2/block-types)
- Call: `GET /wp/v2/block-types`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--namespace <value>` | no | Block namespace. |

## `wordpress api block-types-list-namespace [options]`

- What: getWpV2BlockTypesByNamespace — read (GET /wp/v2/block-types/{namespace})
- Call: `GET /wp/v2/block-types/{namespace}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--namespace <value>` | yes | namespace |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
