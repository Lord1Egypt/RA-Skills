# Squarespace scopes

The OAuth scopes Squarespace connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/squarespace#permissions.

```bash
maton connection create squarespace --scopes website.orders.read
```

| Scope | Requested |
| --- | --- |
| `website.orders` | By default |
| `website.orders.read` | By default |
| `website.transactions.read` | By default |
| `website.inventory` | By default |
| `website.inventory.read` | By default |
| `website.products` | By default |
| `website.products.read` | By default |
| `website.profiles` | By default |
| `website.profiles.read` | By default |
