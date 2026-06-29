FROM python:3.12-slim

# Install system dependencies needed for compiling python packages (like ChromaDB extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    sqlite3 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set default working directory (OpenClaw mount point)
WORKDIR /workspace

# Copy and install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Default environment configurations
ENV OLLAMA_HOST=http://host.docker.internal:11434

