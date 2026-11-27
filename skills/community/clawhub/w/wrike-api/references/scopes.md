# Wrike scopes

The OAuth scopes Wrike connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/wrike#permissions.

```bash
maton connection create wrike --scopes amReadOnlyAccessRole
```

| Scope | Requested |
| --- | --- |
| `wsReadWrite` | By default |
| `amReadWriteUser` | By default |
| `dataExportFull` | By default |
| `amReadWriteGroup` | By default |
| `amReadWriteInvitation` | By default |
| `amReadWriteWorkSchedule` | By default |
| `amReadOnlyAccessRole` | By default |
| `amReadOnlyAuditLog` | By default |
