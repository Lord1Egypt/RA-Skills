# SenseCraft HMI Web Content Generator

Generate beautiful, e-ink optimized web content for SenseCraft HMI displays.

## Features

- AI-powered layout selection
- E-ink optimization (resolution, color depth)
- 10 classic layouts and good design philosophy
- Built-in web server with token authentication
- Detailed screen specifications for various ePaper devices

## Usage

When user requests e-ink content generation, the AI will:
1. Read design references
2. Guide configuration (screen size, color support)
3. Generate optimized HTML
4. Start local server
5. Provide access URL

To use with [SenseCraft HMI service](https://sensecraft.seeed.cc/hmi), you will need to use a reverse proxy tool to forward `http://localhost:19527` to the public network, and then use the `html` widget in the SenseCraft HMI platform to display the web page, and don't forget appending the token to the URL.

## License

MIT
