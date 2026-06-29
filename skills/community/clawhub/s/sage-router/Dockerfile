FROM node:22-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    HOME=/config \
    PORT=8790 \
    SAGE_ROUTER_HOME=/config \
    DARIO_HOME=/root/.dario \
    OLLAMA_HOST=0.0.0.0:11434 \
    OLLAMA_MODELS=/root/.ollama/models

ARG OLLAMA_DOWNLOAD_URL=https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64.tar.zst

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 ca-certificates curl zstd \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @askalf/dario \
    && curl -fsSL "$OLLAMA_DOWNLOAD_URL" | tar --zstd -x -C /usr/local

WORKDIR /app
COPY router.py harness_discovery.py router-profiles.json provider-profiles.json openclaw_gateway_agent.mjs openclaw_sdk_resolver.mjs requirements.txt ./
COPY scripts ./scripts
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY web/dashboard ./web/dashboard/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh /app/router.py /usr/local/bin/ollama

EXPOSE 8790 11434 3456
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
  CMD python3 -c "import urllib.request, os; urllib.request.urlopen('http://127.0.0.1:%s/health' % os.environ.get('PORT','8790'), timeout=5)"

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python3", "/app/router.py"]
