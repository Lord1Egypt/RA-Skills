# Seede Skill for Open Claw

> **The Ultimate AI Design Skill for Open Claw & Agents.**
> Generate professional UI, social media graphics, posters, and more directly via Open Claw.

This repository contains the **Seede Skill**, enabling [Open Claw](https://github.com/openclaw/openclaw) (and other compatible agents) to generate high-quality designs using [Seede AI](https://seede.ai).

## Why Seede Skill?

- 🚀 **State-of-the-Art Generation**: Uses the latest AI models to create high-quality, editable designs.
- 🤖 **Agent-First**: Designed specifically for autonomous agents to control design parameters.
- 🎨 **Brand Consistency**: Supports brand colors and asset injection.
- 🛠️ **Full Control**: Precise control over resolution, format, and scene types.

## Features

- **Text to Design**: Generate complex designs from natural language.
- **Asset Management**: Upload and manage logos, product shots, and reference images.
- **Design Management**: List, search, and retrieve design URLs.
- **Token Management**: Create and manage API tokens directly from the CLI.

## Installation

### Using with Open Claw (Recommended)

To add this skill to your Open Claw agent, simply run:

```bash
npx skills add seedeai/seede-skill
```

### Standalone CLI Installation

If you wish to use the tool manually without an agent:

```bash
npm install -g seede-cli
```

## Configuration

The skill requires the `SEEDE_API_TOKEN` environment variable to be set to authenticate with the Seede AI service.

**1. Create a Token:**

You can generate a token directly via the CLI:

```bash
seede token create --name "My Agent Token"
```

**2. Set Environment Variable:**

```bash
export SEEDE_API_TOKEN="your_generated_token"
```

## Usage

### As an Open Claw Skill

Once installed, you can ask Open Claw to perform design tasks using natural language:

> "Design a modern tech conference poster with neon accents."
> "Create a social media banner for a coffee shop."

The agent will automatically utilize the `seede-design` skill to fulfill these requests.

### Manual Usage (CLI)

You can also use the CLI directly for testing or manual generation:

**Interactive Mode:**

```bash
seede create
```

**Command Line (Agent Mode):**

```bash
seede create --no-interactive \
  --prompt "Modern tech conference poster with neon accents" \
  --scene "poster" \
  --format "png"
```

### Advanced Usage

#### Integrating User Assets

To place a specific image (like a logo or product shot) into the design:

1.  **Upload** the file first using `seede upload`.
2.  **Reference** the returned URL in the prompt using `@SeedeMaterial`:

```bash
seede create --no-interactive \
  --prompt "Minimalist product poster featuring this item @SeedeMaterial({'url':'<ASSET_URL>','tag':'product'})" \
  --scene "poster"
```

#### Enforcing Brand Guidelines

To ensure the design matches specific brand colors:

```bash
seede create --no-interactive \
  --prompt "Corporate annual report cover @SeedeTheme({'colors':['#000000','#FFD700']})"
```

### Manage API Tokens

You can create and manage API tokens for CI/CD or Agent integration directly from the CLI.

**Create a Token:**

```bash
seede token create --name "My Agent Token" --expiration 30
```

## Skill Metadata

This repository includes a `SKILL.md` file that defines the skill capabilities and metadata for the agent system.
