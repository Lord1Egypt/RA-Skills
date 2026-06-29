FROM oven/bun:1.3-slim
WORKDIR /app

# Install deps first for layer caching.
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile || bun install

COPY . .

ENV PORT=8080
EXPOSE 8080

# State (sqlite) lives here — mount a volume to persist tokens + dedup across restarts.
VOLUME ["/data"]
ENV DB_PATH=/data/wake.sqlite

CMD ["bun", "src/index.ts"]
