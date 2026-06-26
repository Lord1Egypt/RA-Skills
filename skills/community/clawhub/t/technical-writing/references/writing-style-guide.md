# Technical Writing Style Guide

Conventions for writing clear, consistent developer documentation.

## Voice and Tone

| Guideline | Bad | Good |
|-----------|-----|------|
| Use active voice | "The file is created by the command" | "The command creates the file" |
| Use present tense | "This will install the package" | "This installs the package" |
| Address the reader directly | "Users should configure..." | "Configure the database..." |
| Be direct | "It should be noted that..." | "Note:" or just state the fact |
| Avoid hedging | "This might possibly cause..." | "This causes..." |
| Skip filler | "In order to start the server" | "To start the server" |

## Sentence Structure

- **One idea per sentence.** If a sentence has "and" or "but" connecting two actions, split it.
- **Lead with the action.** "Run `npm install`" not "You need to run `npm install`"
- **Put conditions first.** "If using Docker, add the volume mount" not "Add the volume mount if using Docker"
- **Keep sentences under 25 words.** Break longer ones.
- **Use parallel structure in lists.** All items should start with the same part of speech.

## Formatting

### Code elements

| Element | Format | Example in text |
|---------|--------|-----------------|
| File paths | `` `backticks` `` | Edit `src/config.ts` |
| CLI commands | code block or `` `backticks` `` | Run `npm install` |
| Config values | `` `backticks` `` | Set `timeout` to `5000` |
| Variable names | `` `backticks` `` | The `userId` parameter |
| Function names | `` `backticks` `` | Call `getUser()` |
| HTTP methods | `` `backticks` `` | Send a `POST` request |
| Status codes | `` `backticks` `` | Returns `200 OK` |
| Keyboard shortcuts | `` `backticks` `` | Press `Ctrl+S` |

### Text elements

| Element | Format | Example |
|---------|--------|---------|
| First use of a term | **Bold** | **Service worker** is a background script... |
| UI elements | **Bold** | Click **Settings** > **Advanced** |
| Emphasis | *Italic* (sparingly) | This step is *required* |
| Warnings | Admonition/callout | > **Warning:** This deletes all data |
| Notes | Admonition/callout | > **Note:** Only available in v2+ |

## Lists

### Use numbered lists for sequential steps

```markdown
1. Install the dependencies.
2. Configure the database connection.
3. Run the migration.
4. Start the server.
```

### Use bullet lists for unordered items

```markdown
- PostgreSQL 16+
- Node.js 20+
- npm or pnpm
```

### Keep list items parallel

```markdown
Bad:
- Installing the dependencies
- You should configure the database
- The server needs starting

Good:
- Install the dependencies
- Configure the database
- Start the server
```

## Headings

- Use sentence case: "Configure the database" not "Configure The Database"
- Be specific: "Set up PostgreSQL" not "Database Setup"
- Don't skip levels: H2 → H3 → H4, never H2 → H4
- Keep headings under 8 words when possible
- Don't end headings with punctuation

## Numbers and Units

| Convention | Example |
|-----------|---------|
| Spell out one through nine | "three servers" |
| Use digits for 10+ | "15 endpoints" |
| Always use digits with units | "5 MB", "100 ms", "3 seconds" |
| Use consistent units | Don't mix "ms" and "milliseconds" in one doc |
| Use comma separators for thousands | "1,000 requests" |

## Links

- Use descriptive link text: `[installation guide](./install.md)` not `[click here](./install.md)`
- Link to headings within the same doc: `[See Configuration](#configuration)`
- Use relative links within the same repo: `[API docs](../api/reference.md)`
- For external links, indicate the target: `[Express docs](https://expressjs.com) (external)`

## Inclusive Language

| Avoid | Use instead |
|-------|-------------|
| master/slave | primary/replica, leader/follower |
| whitelist/blacklist | allowlist/blocklist |
| sanity check | confidence check, quick check |
| dummy | placeholder, sample, test |
| guys | everyone, folks, team |
| he/she | they |
| simple/easy/obvious | straightforward, "follow these steps" |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "e.g." without a comma | "e.g., React, Vue" |
| "i.e." when you mean "e.g." | "i.e." = "that is"; "e.g." = "for example" |
| "it's" vs "its" | "it's" = "it is"; "its" = possessive |
| Inconsistent capitalization | Pick one: "JavaScript" always, not sometimes "Javascript" |
| Unexplained acronyms | Spell out on first use: "Content Delivery Network (CDN)" |
| "allows to" | "allows you to" or "lets you" |
| "in order to" | Just "to" |
| "please" in instructions | Commands don't need to be polite: "Run" not "Please run" |
