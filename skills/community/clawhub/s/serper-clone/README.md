# serper-clone-skill

An [OpenClaw](https://github.com/openclaw) skill that provides web search via a self-hosted [Serper-compatible API](https://github.com/paulscode/serper-startos).

Free, private, no rate limits — runs entirely on your own infrastructure.

## Features

- **10 search endpoints** — web, news, images, videos, places, maps, shopping, scholar, patents, autocomplete
- **Drop-in Serper API compatibility** — same request/response format as serper.dev
- **No API costs** — powered by SearXNG, a free open-source metasearch engine
- **Private** — queries never leave your infrastructure

## Prerequisites

A running Serper Clone instance. Deploy one from:

- [serper-startos](https://github.com/paulscode/serper-startos) — StartOS package (recommended for home servers)
- The same repo includes Docker deployment instructions

## Installation

Copy the `SKILL.md` file into your OpenClaw skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/serper-clone
cp SKILL.md ~/.openclaw/workspace/skills/serper-clone/
```

Then configure your API key and server URL:

```bash
echo "API_KEY=your-api-key-here" > ~/.openclaw/workspace/.serper-clone-api-key
echo "BASE_URL=https://your-serper-clone-host" >> ~/.openclaw/workspace/.serper-clone-api-key
chmod 600 ~/.openclaw/workspace/.serper-clone-api-key
```

The skill activates automatically once the API key file is in place.

## Usage

See [SKILL.md](SKILL.md) for full endpoint documentation, request/response formats, and examples.

## License

MIT
