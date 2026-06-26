
## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).

## Commands Reference

### Users

#### Create a User

```bash
zilliz user create --user <username> --password <password>
```

#### List Users

```bash
zilliz user list
```

#### Describe a User

```bash
zilliz user describe --user <username>
```

#### Drop a User

```bash
zilliz user drop --user <username-to-drop>
```

#### Update Password

```bash
zilliz user update-password \
  --user <username> \
  --password <current-password> \
  --new-password <new-password>
```

#### Grant a Role to a User

```bash
zilliz user grant-role --user <username> --role <role-name-to-grant>
```

#### Revoke a Role from a User

```bash
zilliz user revoke-role --user <username> --role <role-name-to-revoke>
```

### Roles

#### Create a Role

```bash
zilliz role create --role <role-name>
```

#### List Roles

```bash
zilliz role list
```

#### Describe a Role

```bash
zilliz role describe --role <role-name>
```

#### Drop a Role

```bash
zilliz role drop --role <role-name-to-drop>
```

#### Grant a Privilege

```bash
zilliz role grant-privilege \
  --role <role-name> \
  --object-type <Global|Collection|Database> \
  --object-name <object-name> \
  --privilege <privilege-name>
# Optional: --database <database-name>
```

#### Revoke a Privilege

```bash
zilliz role revoke-privilege \
  --role <role-name> \
  --object-type <Global|Collection|Database> \
  --object-name <object-name> \
  --privilege <privilege-name>
# Optional: --database <database-name>
```

## Common Privileges

Common privileges by object type:

- **Collection**: `Search`, `Query`, `Insert`, `Delete`, `CreateIndex`, `DropCollection`
- **Global**: `CreateCollection`, `All`
- **Database**: `ListCollections`

## Guidance

- User and role management is only available on **Dedicated** clusters.
- Built-in roles: `admin` (full access), `public` (no privileges by default -- must be granted explicitly).
- When setting up RBAC, suggest a workflow: create role, grant privileges, create user, assign role.
- Before dropping a user or role, confirm with the user.
- Use `*` as object-name to grant privilege on all objects of that type.
