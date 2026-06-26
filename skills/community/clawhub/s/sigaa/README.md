# SIGAA OpenClaw Skill

An OpenClaw agent skill for interacting with **SIGAA** (Sistema Integrado de Gestão de Atividades Acadêmicas), the academic management system used by 50+ Brazilian federal universities and institutes.

## Features

- 🔐 **Secure authentication**: CAS SSO (UNB-style) and direct login — credentials via env vars only, never CLI args
- 🎓 **Student Portal**: enrollment status, grades, academic history, class schedule
- 👨🏫 **Professor Portal**: class management, attendance, grade entry
- 🏛️ **Multi-institution**: UNB, UFRN, UFC, UFPE, UFCG, UFPI, UFRRJ, and 40+ more
- 🔒 **Security-first**: cookies chmod 600 + auto-deleted on exit, password cleared from env after login, rate limiting built-in

## Supported Institutions

50+ Brazilian federal universities including:
- UNB (Universidade de Brasília)
- UFRN (Universidade Federal do Rio Grande do Norte — original SIGAA developer)
- UFC, UFPE, UFCG, UFPI, UFRRJ, UFBA, UFPA, UFPB, and many more

## Requirements

- `curl` — HTTP client
- `python3` — HTML parsing
- `grep` with PCRE support (`grep -P`)

## Installation

```bash
clawhub install sigaa
```

## Usage

```bash
# 1. Set credentials as env vars (never pass on command line)
export SIGAA_URL='https://sigaa.unb.br'
export SIGAA_USER='241104251'        # matricula, CPF, or SIAPE depending on institution
export SIGAA_PASSWORD='mypassword'

# 2. Login (source to export session vars into current shell)
source scripts/sigaa_login.sh

# 3. Run operations
bash scripts/sigaa_student.sh enrollment-result   # Check enrollment status
bash scripts/sigaa_student.sh grades              # Grades
bash scripts/sigaa_student.sh status              # Program info
bash scripts/sigaa_professor.sh classes           # Professor: list classes
```

## Security Design

| Concern | Mitigation |
|---------|-----------|
| Password in shell history | Credentials via env vars only — never positional args |
| Cookie exposure | `chmod 600` on creation + `trap EXIT` auto-delete |
| Password in memory | `unset SIGAA_PASSWORD` after successful login |
| Rate limiting / lockout | 0.5s delay between requests |
| Wrong CAS host | Scripts derive CAS host from login redirect — verify before running |

## License

MIT
