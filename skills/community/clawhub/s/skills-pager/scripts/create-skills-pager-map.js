#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    sources: [],
    pages: [],
  };

  for (let i = 0; i < argv.length; i += 1) {
    const value = argv[i];
    if (value === "--skill-id") {
      args.skillId = argv[++i];
    } else if (value === "--source") {
      args.sources.push(argv[++i]);
    } else if (value === "--page") {
      args.pages.push(argv[++i]);
    } else if (value === "--note") {
      args.note = argv[++i];
    } else {
      fail(`Unknown argument: ${value}`);
    }
  }

  if (!args.skillId) {
    fail("Missing required argument: --skill-id");
  }
  if (args.sources.length === 0) {
    fail("At least one --source path is required");
  }
  if (args.pages.length === 0) {
    args.pages.push("current-route");
  }

  return args;
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "current-route";
}

function readJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) {
    return fallback;
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

function writeText(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, "utf8");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const workspaceRoot = process.cwd();
  const now = new Date().toISOString();
  const pageSlugs = [...new Set(args.pages.map((page) => slugify(page)))];

  const indexRoot = path.join(workspaceRoot, ".skill-index");
  const skillRoot = path.join(indexRoot, "skills", args.skillId);
  const registryPath = path.join(indexRoot, "registry.json");
  const indexPath = path.join(skillRoot, "index.md");

  fs.mkdirSync(skillRoot, { recursive: true });

  const registry = readJson(registryPath, { skills: {} });
  registry.skills = registry.skills || {};
  registry.skills[args.skillId] = {
    mapFile: `.skill-index/skills/${args.skillId}/index.md`,
    lastReviewedAt: now,
    notes:
      args.note ||
      "Scaffold created for the first working map. Replace placeholders before relying on it for reuse.",
  };

  const sourceList = args.sources.map((source) => `- \`${source}\``).join("\n");
  const routeList = pageSlugs.map((pageSlug) => `- \`${pageSlug}\``).join("\n");
  const routeSections = pageSlugs
    .map(
      (pageSlug) => `### ${pageSlug}

- When to start here: Replace this line with the task shape this route serves.
- Start source: \`${args.sources[0]}\`
- What to verify: Replace this line with the first section, protocol, or appendix to re-read.
- Next likely checks: Add the next route, reference, or caveat that often follows.
`,
    )
    .join("\n");

  writeText(registryPath, `${JSON.stringify(registry, null, 2)}\n`);
  writeText(
    indexPath,
    `# ${args.skillId}

## What this skill is for

- Replace this line with the problem the skill solves in this workspace.

## When to start here

- Replace this line with the conditions that make this skill the current target.

## Main routes

${routeList}

## Important sources

${sourceList}

## Route notes

${routeSections}
## Precise return points to fill

- Add the exact source jump, heading path, or appendix location that later sessions should not have to rediscover.
- Add only the return points that actually improve reuse.

## Working notes

- Replace all placeholder lines before treating this map as reusable.
- Keep this file focused on one target skill, not the whole skills workspace.
- Expand the route notes only where later turns are likely to revisit the skill.
`,
  );

  process.stdout.write(
    `${JSON.stringify(
      {
        skillId: args.skillId,
        workspaceRoot,
        mapDir: `.skill-index/skills/${args.skillId}`,
        routes: pageSlugs,
        files: {
          registry: ".skill-index/registry.json",
          index: `.skill-index/skills/${args.skillId}/index.md`,
        },
      },
      null,
      2,
    )}\n`,
  );
}

main();
