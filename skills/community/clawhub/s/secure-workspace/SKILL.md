---
name: secure-workspace
description: Cifra API keys, tokens y contraseñas con age para proteger secrets del workspace.
emoji: 🔐
homepage: https://github.com/asistentegordito/secure-workspace
metadata:
  clawdbot:
    emoji: 🔐
    requires:
      exec:
        - age
---

# Secure Workspace

Cifra secrets con age para protegerlos en repositorios y backups.

## Uso

```bash
# 1. Generar par de llaves (si no existe)
bash scripts/secure/setup.sh

# 2. Cifrar un secreto
echo 'export API_KEY="..."' | bash scripts/secure/encrypt.sh scripts/secure/secrets.env.age

# 3. Descifrar al vuelo
source <(bash scripts/secure/decrypt.sh scripts/secure/secrets.env.age)
```

## Archivos

| Archivo | Función |
|---------|---------|
| `scripts/secure/encrypt.sh` | Cifra stdin → `.age` |
| `scripts/secure/decrypt.sh` | Descifra `.age` → stdout |
| `scripts/secure/setup.sh` | Genera par de llaves |

## Requisitos

- `age` (apt install age / brew install age)

## Nota

La clave privada está en `/root/.age/key.txt`. No se sube al repo.
