# Docker Usage

```dockerfile
FROM node:20-alpine

WORKDIR /app
RUN apk add --no-cache chromium nss freetype fontconfig

RUN npm install playwright && npx playwright install chromium

COPY . .
RUN npm install

CMD ["node", "src/cli.js", "all"]
```

Run with:
```bash
docker build -t spielerplus-scraper .
docker run --rm \
  -e SPIELERPLUS_EMAIL=your@email.com \
  -e SPIELERPLUS_PASSWORD=yourpassword \
  spielerplus-scraper teams
```
