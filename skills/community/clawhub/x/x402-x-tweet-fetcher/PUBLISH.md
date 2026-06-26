# Publish Guide for ClawHub

## 1. Install clawhub CLI

```bash
npm i -g clawhub
```

or

```bash
pnpm add -g clawhub
```

## 2. Login

```bash
clawhub login
```

or with token:

```bash
clawhub login --token YOUR_TOKEN
```

## 3. Publish

```bash
clawhub publish ./x402-x-tweet-fetcher \
  --slug x402-x-tweet-fetcher \
  --name "X402 X Tweet Fetcher" \
  --version 1.0.0 \
  --tags latest
```

## 4. Publish an updated version

```bash
clawhub publish ./x402-x-tweet-fetcher \
  --slug x402-x-tweet-fetcher \
  --name "X402 X Tweet Fetcher" \
  --version 1.0.1 \
  --changelog "Docs cleanup and publishing improvements" \
  --tags latest
```

## 5. Sync many skills

```bash
clawhub sync --all
```

## 6. Recommended release policy

- bump patch version for docs or wording updates
- bump minor version for new non-breaking endpoints or features
- bump major version for breaking API or workflow changes

## 7. Recommended slug and display name

Slug:
- `x402-x-tweet-fetcher`

Display name:
- `X402 X Tweet Fetcher`

Why:
- easy to search
- clearly indicates x402 + X workflow
- better discoverability than a generic backend-oriented name
