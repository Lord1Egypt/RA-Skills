# 🔑 Weakpass-Skill
Give your AI agent access to 25 billion leaked passwords

## 💪 Getting Started
Install through Clawhub (requires Clawhub CLI):
```bash
$ clawhub install weakpass
```
Alternative install:
```bash
$ openclaw skills install weakpass
```

## 🛡️ Security
This skill calls an external API. Files are never modified. Nothing on your OS is touched. Nothing that you did not specifically send to the external API is ever sent.

## ⚙️ Endpoints
### Ranges:
`/range/{prefix}.json` `GET` - Implemented

`/range/{prefix}.txt` `GET` - Implemented

### Search:
`/search/{hash}.json` `GET` - Implemented

`/search/{hash}.txt` `GET` - Implemented

### Generate:
`/generate/{string}` `GET` - Implemented

### Wordlists:
`/wordlists` `GET` - Implemented

`/wordlists/{wordlist}` `GET` - Implemented

## 📜 API References:

- https://weakpass.com/openapi.json
- https://weakpass.com/openapi.yaml
- https://weakpass.com/api
