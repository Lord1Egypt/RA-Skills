# Example: Extracting Docker Compose Snippets

This example demonstrates using the web-snippet-extractor skill on the official Docker docs.

## Source

URL: https://docs.docker.com/compose/

## Expected Extraction

Running the skill against this URL would produce structured snippets like:

### Snippet 1: Build and start containers
- **Language:** bash
- **Type:** command

```bash
docker compose up -d
```

### Snippet 2: docker-compose.yml basic structure
- **Language:** yaml
- **Type:** config

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
```

### Snippet 3: View running services
- **Language:** bash
- **Type:** command

```bash
docker compose ps
```

## How to Reproduce

1. Open the Docker Compose documentation URL
2. Invoke the web-snippet-extractor skill with that URL
3. Review the extracted snippets
4. Save relevant ones to your workspace
