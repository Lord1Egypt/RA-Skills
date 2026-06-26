# Permission Presets

Curated permission presets for `settings.local.json`. Each preset is a JSON array of permission strings grouped with `//` comments. Compose presets by stacking: Universal Base + language preset + deployment preset + extras.

## Syntax Reference

| Pattern | Meaning |
|---------|---------|
| `Bash(git *)` | Space before `*` = word boundary. Matches `git status` but not `gitk`. **Preferred syntax.** |
| `Bash(git*)` | No space = prefix match. Matches `git status` AND `gitk`. |
| `Bash(nvidia-smi)` | Exact match — no arguments. Use for bare commands. |
| `WebFetch` | Blanket web fetch (all domains) |
| `WebFetch(domain:example.com)` | Domain-scoped web fetch |
| `WebSearch` | Blanket web search |
| `mcp__servername__*` | All tools on one MCP server |
| `mcp__servername__tool_name` | One specific MCP tool |
| `Read(.claude/**)` | Read files in project's .claude/ (recursive) |
| `Edit(~/Documents/**)` | Edit files under home Documents (recursive) |
| `Read(//tmp/**)` | Read from absolute path (`//` = filesystem root) |

### Format Notes

- **Deprecated**: `Bash(git:*)` colon syntax still works but prefer space syntax `Bash(git *)`
- **"Don't ask again"** prompt uses legacy colon format (e.g. `node:*`) — it's equivalent but looks different
- **Comments**: `"// --- Section ---"` strings in the allow array are ignored and useful for organisation
- **Not hot-reloaded**: Changes to `settings.local.json` require a session restart. "Don't ask again" bypasses this because it injects into the running session directly.

**Critical**: Project `settings.local.json` **SHADOWS** global settings (does not merge). If a project has its own allow list, the global allow list is ignored entirely for that project.

Shell operators (`&&`, `||`, `;`) are handled safely — `Bash(git *)` won't match `git add && rm -rf /`.

---

## Universal Base

Every project gets these. Version control, file operations, and basic tools needed for all development.

```json
"// --- Version Control ---",
"Bash(git *)",
"Bash(gh *)",
"Bash(gh repo *)",
"Bash(gh issue *)",
"Bash(gh pr *)",
"Bash(gh api *)",
"Bash(gh search *)",
"Bash(gh run *)",
"Bash(gh release *)",

"// --- File Operations ---",
"Bash(cd *)",
"Bash(ls *)",
"Bash(pwd *)",
"Bash(cat *)",
"Bash(head *)",
"Bash(tail *)",
"Bash(less *)",
"Bash(more *)",
"Bash(wc *)",
"Bash(sort *)",
"Bash(mkdir *)",
"Bash(mktemp *)",
"Bash(rm *)",
"Bash(rmdir *)",
"Bash(cp *)",
"Bash(mv *)",
"Bash(ln *)",
"Bash(touch *)",
"Bash(chmod *)",
"Bash(chown *)",
"Bash(find *)",
"Bash(tree *)",
"Bash(du *)",
"Bash(df *)",
"Bash(readlink *)",
"Bash(realpath *)",
"Bash(stat *)",
"Bash(file *)",

"// --- Archives ---",
"Bash(tar *)",
"Bash(zip *)",
"Bash(unzip *)",
"Bash(gzip *)",
"Bash(gunzip *)",

"// --- Text Processing ---",
"Bash(grep *)",
"Bash(rg *)",
"Bash(awk *)",
"Bash(sed *)",
"Bash(perl *)",
"Bash(diff *)",
"Bash(jq *)",
"Bash(yq *)",
"Bash(echo *)",
"Bash(printf *)",
"Bash(tee *)",
"Bash(cut *)",
"Bash(paste *)",
"Bash(tr *)",
"Bash(uniq *)",
"Bash(xargs *)",
"Bash(yes *)",
"Bash(basename *)",
"Bash(dirname *)",

"// --- System ---",
"Bash(which *)",
"Bash(whereis *)",
"Bash(type *)",
"Bash(ps *)",
"Bash(kill *)",
"Bash(env *)",
"Bash(export *)",
"Bash(unset *)",
"Bash(source *)",
"Bash(bash *)",
"Bash(sh *)",
"Bash(date *)",
"Bash(uname *)",
"Bash(make *)",
"Bash(cmake *)",
"Bash(id *)",
"Bash(whoami *)",
"Bash(hostname *)",
"Bash(uptime *)",

"// --- Process Management ---",
"Bash(pkill *)",
"Bash(killall *)",
"Bash(lsof *)",
"Bash(pgrep *)",
"Bash(timeout *)",
"Bash(sleep *)",
"Bash(wait *)",
"Bash(time *)",
"Bash(nohup *)",
"Bash(ss *)",
"Bash(top *)",
"Bash(htop *)",
"Bash(free *)",

"// --- Terminal Multiplexers ---",
"Bash(screen *)",
"Bash(tmux *)",

"// --- Security / Crypto ---",
"Bash(openssl *)",
"Bash(ssh-keygen *)",
"Bash(gitleaks *)",
"Bash(md5sum *)",
"Bash(md5 *)",
"Bash(shasum *)",

"// --- System Utilities ---",
"Bash(printenv *)",
"Bash(xxd *)",
"Bash(base64 *)",
"Bash(nslookup *)",
"Bash(seq *)",
"Bash(bc *)",
"Bash(column *)",
"Bash(iconv *)",
"Bash(strings *)",
"Bash(patch *)",
"Bash(cmp *)",

"// --- Network ---",
"Bash(curl *)",
"Bash(wget *)",
"Bash(ssh *)",
"Bash(scp *)",
"Bash(rsync *)",
"Bash(dig *)",
"Bash(ping *)",
"Bash(whois *)",
"Bash(sshpass *)",

"// --- Skill Scripts ---",
"Bash(python3 *)",

"// --- File Access ---",
"Read(.claude/**)",
"Edit(.claude/**)",
"Write(.claude/**)",
"Read(//tmp/**)",
"Edit(//tmp/**)",

"// --- Web ---",
"WebSearch",
"WebFetch"
```

**File access patterns** use gitignore-style syntax:
- `.claude/**` — project-relative (scripts, artifacts, screenshots)
- `//tmp/**` — absolute path (`//` prefix = filesystem root)
- `~/.claude/**` — home-relative (global rules, memory)
- `~/Documents/**` — home-relative (cross-project reads)
- `*` matches files in one directory, `**` matches recursively

Add home-relative paths to **global** `~/.claude/settings.local.json` only (not per-project):

```json
"// --- Global File Access (add to ~/.claude/settings.local.json) ---",
"Read(~/.claude/**)",
"Edit(~/.claude/**)",
"Read(~/Documents/**)",
"Edit(~/Documents/**)",
"Read(~/Downloads/**)"
```

---

## JavaScript / TypeScript

For any JS/TS project. Add to Universal Base.

```json
"// --- Node.js ---",
"Bash(node *)",
"Bash(npm *)",
"Bash(npx *)",

"// --- Alternative Runtimes ---",
"Bash(bun *)",
"Bash(bunx *)",
"Bash(deno *)",

"// --- Package Managers ---",
"Bash(pnpm *)",
"Bash(yarn *)",

"// --- Node Version Managers ---",
"Bash(nvm *)",
"Bash(fnm *)",
"Bash(volta *)",

"// --- TypeScript ---",
"Bash(tsc *)",
"Bash(tsx *)",
"Bash(ts-node *)",

"// --- Bundlers ---",
"Bash(esbuild *)",
"Bash(vite *)",
"Bash(turbo *)",

"// --- Dev Servers ---",
"Bash(pm2 *)",

"// --- Testing ---",
"Bash(jest *)",
"Bash(vitest *)",
"Bash(playwright *)",
"Bash(playwright-cli *)",
"Bash(cypress *)",

"// --- Linting / Formatting ---",
"Bash(eslint *)",
"Bash(prettier *)",
"Bash(biome *)",

"// --- Build Tools ---",
"Bash(corepack *)",
"Bash(tsup *)",
"Bash(swc *)",
"Bash(rollup *)",
"Bash(webpack *)",

"// --- Monorepo ---",
"Bash(nx *)",
"Bash(lerna *)",
"Bash(changeset *)",

"// --- Component Dev ---",
"Bash(storybook *)",

"// --- npx Subcommands (workaround for broad wildcard bug) ---",
"Bash(npx tsc *)",
"Bash(npx tsx *)",
"Bash(npx ts-node *)",
"Bash(npx vite *)",
"Bash(npx vitest *)",
"Bash(npx esbuild *)",
"Bash(npx eslint *)",
"Bash(npx prettier *)",
"Bash(npx playwright *)",
"Bash(npx playwright-cli *)",
"Bash(npx tailwindcss *)",
"Bash(npx shadcn *)",
"Bash(npx shadcn@latest *)",
"Bash(npx @better-auth/cli *)",
"Bash(npx @better-auth/cli@latest *)",
"Bash(npx drizzle-kit *)",
"Bash(npx create-cloudflare *)",
"Bash(npx create-cloudflare@latest *)",
"Bash(npx create-next-app *)",
"Bash(npx create-next-app@latest *)",
"Bash(npx astro *)",
"Bash(npx storybook *)",
"Bash(npx lighthouse *)",
"Bash(npx repomix *)"
```

Note: `Bash(npx *)` is included in the base preset but may miss subcommands due to the same wildcard bug that affects `gh`. Include explicit `npx <tool>` entries for commonly used tools.

---

## Python

For Python projects. Add to Universal Base.

```json
"// --- Python Runtime ---",
"Bash(python *)",
"Bash(python3 *)",

"// --- Package Managers ---",
"Bash(pip *)",
"Bash(pip3 *)",
"Bash(uv *)",
"Bash(poetry *)",
"Bash(pipx *)",
"Bash(conda *)",

"// --- Testing / Quality ---",
"Bash(pytest *)",
"Bash(mypy *)",
"Bash(ruff *)",
"Bash(black *)",
"Bash(flake8 *)",
"Bash(isort *)",

"// --- Dev Servers ---",
"Bash(flask *)",
"Bash(uvicorn *)",
"Bash(gunicorn *)",
"Bash(django-admin *)",

"// --- Package Managers ---",
"Bash(pdm *)",
"Bash(hatch *)",

"// --- Git Hooks ---",
"Bash(pre-commit *)",

"// --- Notebooks ---",
"Bash(jupyter *)"
```

---

## PHP

For PHP projects including WordPress and Laravel. Add to Universal Base.

```json
"// --- PHP Runtime ---",
"Bash(php *)",
"Bash(composer *)",

"// --- WordPress ---",
"Bash(wp *)",

"// --- Testing / Quality ---",
"Bash(phpunit *)",
"Bash(phpstan *)",
"Bash(phpcs *)",
"Bash(phpcbf *)",
"Bash(pest *)",

"// --- Laravel ---",
"Bash(artisan *)",
"Bash(sail *)"
```

---

## Go

For Go projects. Add to Universal Base.

```json
"// --- Go ---",
"Bash(go *)",
"Bash(golangci-lint *)"
```

---

## Rust

For Rust projects. Add to Universal Base.

```json
"// --- Rust ---",
"Bash(cargo *)",
"Bash(rustc *)",
"Bash(rustup *)"
```

---

## Ruby

For Ruby / Rails projects. Add to Universal Base.

```json
"// --- Ruby ---",
"Bash(ruby *)",
"Bash(gem *)",
"Bash(bundle *)",
"Bash(bundler *)",
"Bash(rails *)",
"Bash(rake *)",
"Bash(rspec *)"
```

---

## Cloudflare Worker

Deployment preset. Add to Universal Base + JavaScript/TypeScript.

```json
"// --- Wrangler ---",
"Bash(wrangler *)",
"Bash(npx wrangler *)",
"Bash(npx wrangler@latest *)",
"Bash(npx create-cloudflare *)",
"Bash(npx create-cloudflare@latest *)",
"Bash(miniflare *)"
```

---

## Vercel

Deployment preset. Add to Universal Base + JavaScript/TypeScript.

```json
"// --- Vercel ---",
"Bash(vercel *)",
"Bash(npx vercel *)",

"// --- Prisma (common with Vercel) ---",
"Bash(prisma *)",
"Bash(npx prisma *)"
```

---

## Docker / Containers

For containerised projects. Add to any stack.

```json
"// --- Docker ---",
"Bash(docker *)",
"Bash(docker-compose *)",

"// --- Kubernetes ---",
"Bash(kubectl *)",
"Bash(helm *)",

"// --- IaC ---",
"Bash(terraform *)",
"Bash(pulumi *)"
```

---

## Database

For projects that interact with databases directly. Add to any stack.

```json
"// --- SQL ---",
"Bash(psql *)",
"Bash(mysql *)",
"Bash(sqlite3 *)",
"Bash(sqlite3 :memory:*)",

"// --- PostgreSQL Utilities ---",
"Bash(pg_dump *)",
"Bash(pg_restore *)",
"Bash(createdb *)",
"Bash(dropdb *)",

"// --- MySQL Utilities ---",
"Bash(mysqldump *)",

"// --- NoSQL ---",
"Bash(redis-cli *)",
"Bash(mongosh *)",

"// --- Managed Database CLIs ---",
"Bash(turso *)",
"Bash(pscale *)",

"// --- ORM CLIs (via npx) ---",
"Bash(npx drizzle-kit *)",
"Bash(npx prisma *)"
```

---

## Cloud CLIs

For cloud-deployed projects. Add to any stack.

```json
"// --- AWS ---",
"Bash(aws *)",

"// --- Google Cloud ---",
"Bash(gcloud *)",
"Bash(gsutil *)",

"// --- Azure ---",
"Bash(az *)"
```

---

## AI / GPU

For AI/ML workloads. Add to any stack.

```json
"// --- Local LLM ---",
"Bash(ollama *)",

"// --- GPU ---",
"Bash(nvidia-smi *)",
"Bash(nvidia-smi)",

"// --- API Key Passthrough ---",
"Bash(GEMINI_API_KEY=*)",
"Bash(OPENAI_API_KEY=*)",
"Bash(ANTHROPIC_API_KEY=*)"
```

Note: `Bash(nvidia-smi)` (no wildcard) matches the bare command with no arguments, which is the most common usage.

---

## MCP Servers

MCP (Model Context Protocol) servers provide tool access to external services. Permission patterns use the format `mcp__servername__toolname`.

### Per-Server Wildcards (Recommended)

Allow all tools on each MCP server you trust. You must list each server individually — `mcp__*` does NOT work as a blanket (the wildcard only matches within the last segment, not across the `__` boundary).

```json
"mcp__servername__*",
"mcp__playwright__*",
"mcp__another-server__*"
```

### Individual Tools

For maximum control, allow specific tools only:

```json
"mcp__servername__specific_tool",
"mcp__servername__another_tool"
```

---

## macOS

macOS-specific commands. Add when developing on macOS.

```json
"// --- macOS ---",
"Bash(brew *)",
"Bash(open *)",
"Bash(pbcopy *)",
"Bash(pbpaste *)",
"Bash(sips *)",
"Bash(screencapture *)",
"Bash(osascript *)",
"Bash(caffeinate *)",
"Bash(defaults *)",
"Bash(mdfind *)",
"Bash(mdls *)",
"Bash(ditto *)",
"Bash(say *)",
"Bash(plutil *)",
"Bash(softwareupdate *)",
"Bash(xcode-select *)",
"Bash(xattr *)"
```

---

## Google Workspace CLI

Google Workspace CLI (`gws`) for Gmail, Drive, Calendar, Sheets, Docs, Chat, Tasks, and more. Add when using `@googleworkspace/cli`.

```json
"// --- Google Workspace CLI ---",
"Bash(gws *)",
"Bash(gws auth *)",
"Bash(gws gmail *)",
"Bash(gws calendar *)",
"Bash(gws drive *)",
"Bash(gws sheets *)",
"Bash(gws docs *)",
"Bash(gws chat *)",
"Bash(gws tasks *)",
"Bash(gws slides *)",
"Bash(gws forms *)",
"Bash(gws people *)",
"Bash(gws admin *)",
"Bash(npx skills *)"
```

Note: `Bash(gws *)` should cover all subcommands, but explicit entries are included as workaround for the wildcard matching bug (same as `gh` and `npx`). `npx skills` is for installing/managing gws agent skills.

---

## LLM CLIs

AI/LLM command-line tools. Add when using AI assistants or review tools.

```json
"// --- LLM CLIs ---",
"Bash(claude *)",
"Bash(gemini *)",
"Bash(gemini-coach *)",
"Bash(elevenlabs *)",
"Bash(fastmcp *)",
"Bash(apify *)"
```

---

## Firebase

Google Firebase CLI. Add alongside Cloud CLIs for Firebase projects.

```json
"// --- Firebase ---",
"Bash(firebase *)"
```

---

## Media Processing

Image and video processing tools. Add for projects that handle media assets.

```json
"// --- Media Processing ---",
"Bash(convert *)",
"Bash(identify *)",
"Bash(exiftool *)",
"Bash(ffmpeg *)",
"Bash(ffprobe *)",
"Bash(ffplay *)",
"Bash(yt-dlp *)",
"Bash(mpv *)"
```

---

## Linux System

Linux server administration. Add for projects deployed on Linux or managed via SSH.

```json
"// --- Linux System ---",
"Bash(systemctl *)",
"Bash(journalctl *)",
"Bash(crontab *)",
"Bash(sudo *)",
"Bash(apt *)",
"Bash(apt-get *)",
"Bash(dpkg *)",
"Bash(yum *)",
"Bash(dnf *)",
"Bash(xdg-open *)",
"Bash(fuser *)"
```

---

## Mobile Development

React Native, Expo, and mobile tooling. Add for mobile app projects.

```json
"// --- React Native / Expo ---",
"Bash(eas *)",
"Bash(npx expo *)",
"Bash(adb *)",
"Bash(react-native *)",

"// --- Flutter ---",
"Bash(flutter *)",
"Bash(dart *)",

"// --- iOS ---",
"Bash(xcodebuild *)",
"Bash(pod *)",
"Bash(xcrun *)",

"// --- Cross-Platform ---",
"Bash(fastlane *)"
```

---

## Java / JVM

For Java, Kotlin, Scala, and other JVM projects. Add to Universal Base.

```json
"// --- Java ---",
"Bash(java *)",
"Bash(javac *)",
"Bash(jar *)",

"// --- Build Tools ---",
"Bash(mvn *)",
"Bash(gradle *)",
"Bash(gradlew *)",
"Bash(./gradlew *)",

"// --- Kotlin ---",
"Bash(kotlin *)",
"Bash(kotlinc *)",

"// --- Scala ---",
"Bash(sbt *)",
"Bash(scala *)"
```

---

## .NET / C#

For .NET projects. Add to Universal Base.

```json
"// --- .NET ---",
"Bash(dotnet *)",
"Bash(nuget *)"
```

---

## Elixir

For Elixir / Phoenix projects. Add to Universal Base.

```json
"// --- Elixir ---",
"Bash(elixir *)",
"Bash(mix *)",
"Bash(iex *)"
```

---

## Swift

For Swift projects (macOS/iOS). Add to Universal Base + macOS.

```json
"// --- Swift ---",
"Bash(swift *)",
"Bash(swiftc *)"
```

---

## Static Site Generators

For static sites. Add to Universal Base + JavaScript/TypeScript (for most).

```json
"// --- Static Site Generators ---",
"Bash(astro *)",
"Bash(hugo *)",
"Bash(gatsby *)",
"Bash(eleventy *)",
"Bash(jekyll *)"
```

---

## Hosting Platforms

Deployment CLIs for various hosting providers. Add to any stack.

```json
"// --- Hosting CLIs ---",
"Bash(railway *)",
"Bash(fly *)",
"Bash(flyctl *)",
"Bash(netlify *)",
"Bash(supabase *)",
"Bash(heroku *)",
"Bash(render *)",
"Bash(cpanel *)"
```

---

## Tunneling / Local Dev

Expose local servers, generate local certs, etc. Add to any stack.

```json
"// --- Tunneling ---",
"Bash(ngrok *)",
"Bash(cloudflared *)",

"// --- Local HTTPS ---",
"Bash(mkcert *)",
"Bash(certbot *)",

"// --- Cloud Storage Sync ---",
"Bash(rclone *)"
```

---

## SaaS CLIs

CLI tools for common SaaS platforms. Add as needed.

```json
"// --- Payment / Communication ---",
"Bash(stripe *)",
"Bash(twilio *)",

"// --- Auth ---",
"Bash(auth0 *)",

"// --- Monitoring ---",
"Bash(sentry-cli *)"
```

---

## Document Processing

For projects that generate PDFs, convert documents, or process media.

```json
"// --- Documents ---",
"Bash(pandoc *)",
"Bash(wkhtmltopdf *)",
"Bash(pdftotext *)",

"// --- ImageMagick v7 ---",
"Bash(magick *)"
```

Note: ImageMagick v6 uses `convert` (in Media Processing preset). v7 uses `magick` as the unified command.

---

## CI / GitHub Actions

For running CI locally or managing workflows.

```json
"// --- CI ---",
"Bash(act *)",

"// --- GitHub Actions ---",
"Bash(gh workflow *)",
"Bash(gh run *)"
```

---

## Editors / IDE CLIs

For projects where Claude may interact with editor tooling.

```json
"// --- Editor CLIs ---",
"Bash(code *)",
"Bash(cursor *)",
"Bash(zed *)",
"Bash(vim *)",
"Bash(nvim *)"
```

---

## WebFetch Domains

Use blanket `WebFetch` (in Universal Base) to avoid per-domain prompts. If you prefer granular control, here is a comprehensive domain-scoped list organised by category to match the Bash presets above.

```json
"// --- WebFetch (blanket — recommended) ---",
"WebFetch"
```

### OR: Domain-Scoped (granular control)

Pick the categories that match your stack.

#### Core (every project)

```json
"// --- GitHub ---",
"WebFetch(domain:github.com)",
"WebFetch(domain:raw.githubusercontent.com)",
"WebFetch(domain:api.github.com)",
"WebFetch(domain:docs.github.com)",
"WebFetch(domain:github.blog)",

"// --- General Dev Reference ---",
"WebFetch(domain:developer.mozilla.org)",
"WebFetch(domain:stackoverflow.com)",
"WebFetch(domain:dev.to)",
"WebFetch(domain:medium.com)",
"WebFetch(domain:deepwiki.com)",
"WebFetch(domain:bundlephobia.com)",

"// --- Package Registries ---",
"WebFetch(domain:www.npmjs.com)",
"WebFetch(domain:pypi.org)",
"WebFetch(domain:crates.io)",
"WebFetch(domain:pkg.go.dev)",
"WebFetch(domain:rubygems.org)",
"WebFetch(domain:nuget.org)"
```

#### AI / LLM

```json
"// --- Anthropic ---",
"WebFetch(domain:docs.anthropic.com)",
"WebFetch(domain:www.anthropic.com)",
"WebFetch(domain:support.anthropic.com)",
"WebFetch(domain:platform.claude.com)",

"// --- Google AI ---",
"WebFetch(domain:ai.google.dev)",
"WebFetch(domain:cloud.google.com)",
"WebFetch(domain:developers.google.com)",

"// --- OpenAI ---",
"WebFetch(domain:platform.openai.com)",
"WebFetch(domain:developers.openai.com)",

"// --- AI SDKs ---",
"WebFetch(domain:ai-sdk.dev)",
"WebFetch(domain:openrouter.ai)",

"// --- ElevenLabs ---",
"WebFetch(domain:elevenlabs.io)",

"// --- MCP ---",
"WebFetch(domain:spec.modelcontextprotocol.io)",
"WebFetch(domain:gofastmcp.com)"
```

#### Cloudflare

```json
"WebFetch(domain:developers.cloudflare.com)",
"WebFetch(domain:blog.cloudflare.com)",
"WebFetch(domain:community.cloudflare.com)"
```

#### JavaScript / TypeScript Ecosystem

```json
"// --- Core ---",
"WebFetch(domain:nodejs.org)",
"WebFetch(domain:typescriptlang.org)",
"WebFetch(domain:tc39.es)",

"// --- React ---",
"WebFetch(domain:react.dev)",
"WebFetch(domain:reactnative.dev)",

"// --- Build Tools ---",
"WebFetch(domain:vitejs.dev)",
"WebFetch(domain:vite.dev)",
"WebFetch(domain:esbuild.github.io)",
"WebFetch(domain:turbo.build)",

"// --- UI Frameworks ---",
"WebFetch(domain:ui.shadcn.com)",
"WebFetch(domain:www.radix-ui.com)",
"WebFetch(domain:tailwindcss.com)",
"WebFetch(domain:lucide.dev)",

"// --- State / Data ---",
"WebFetch(domain:tanstack.com)",
"WebFetch(domain:swr.vercel.app)",
"WebFetch(domain:zustand.docs.pmnd.rs)",
"WebFetch(domain:zod.dev)",
"WebFetch(domain:react-hook-form.com)",

"// --- Auth ---",
"WebFetch(domain:better-auth.com)",
"WebFetch(domain:www.better-auth.com)",
"WebFetch(domain:clerk.com)",
"WebFetch(domain:authjs.dev)",

"// --- ORM / Database ---",
"WebFetch(domain:orm.drizzle.team)",
"WebFetch(domain:www.prisma.io)",

"// --- API Frameworks ---",
"WebFetch(domain:hono.dev)",
"WebFetch(domain:expressjs.com)",
"WebFetch(domain:fastify.dev)",
"WebFetch(domain:trpc.io)",

"// --- Testing ---",
"WebFetch(domain:playwright.dev)",
"WebFetch(domain:vitest.dev)",
"WebFetch(domain:jestjs.io)",
"WebFetch(domain:testing-library.com)",

"// --- Linting ---",
"WebFetch(domain:eslint.org)",
"WebFetch(domain:prettier.io)",
"WebFetch(domain:biomejs.dev)"
```

#### Python Ecosystem

```json
"WebFetch(domain:python.org)",
"WebFetch(domain:docs.python.org)",
"WebFetch(domain:fastapi.tiangolo.com)",
"WebFetch(domain:docs.djangoproject.com)",
"WebFetch(domain:flask.palletsprojects.com)",
"WebFetch(domain:docs.pydantic.dev)",
"WebFetch(domain:docs.pytest.org)",
"WebFetch(domain:docs.astral.sh)"
```

#### Hosting / Deployment

```json
"WebFetch(domain:vercel.com)",
"WebFetch(domain:docs.netlify.com)",
"WebFetch(domain:fly.io)",
"WebFetch(domain:docs.railway.com)",
"WebFetch(domain:supabase.com)",
"WebFetch(domain:render.com)",
"WebFetch(domain:firebase.google.com)"
```

#### Static Site Generators

```json
"WebFetch(domain:astro.build)",
"WebFetch(domain:docs.astro.build)",
"WebFetch(domain:gohugo.io)",
"WebFetch(domain:www.gatsbyjs.com)",
"WebFetch(domain:www.11ty.dev)",
"WebFetch(domain:nextjs.org)"
```

#### Database

```json
"WebFetch(domain:www.postgresql.org)",
"WebFetch(domain:dev.mysql.com)",
"WebFetch(domain:www.sqlite.org)",
"WebFetch(domain:redis.io)",
"WebFetch(domain:www.mongodb.com)",
"WebFetch(domain:docs.turso.tech)",
"WebFetch(domain:planetscale.com)",
"WebFetch(domain:neon.tech)"
```

#### PHP / WordPress

```json
"WebFetch(domain:www.php.net)",
"WebFetch(domain:developer.wordpress.org)",
"WebFetch(domain:laravel.com)",
"WebFetch(domain:getcomposer.org)"
```

#### SaaS / API Services

```json
"WebFetch(domain:docs.stripe.com)",
"WebFetch(domain:www.twilio.com)",
"WebFetch(domain:apidoc.smtp2go.com)",
"WebFetch(domain:support.smtp2go.com)",
"WebFetch(domain:docs.firecrawl.dev)",
"WebFetch(domain:apify.com)",
"WebFetch(domain:docs.sentry.io)",
"WebFetch(domain:docs.sendgrid.com)"
```

#### Go / Rust / Ruby / Java / .NET / Elixir

```json
"WebFetch(domain:go.dev)",
"WebFetch(domain:doc.rust-lang.org)",
"WebFetch(domain:www.rust-lang.org)",
"WebFetch(domain:rubyonrails.org)",
"WebFetch(domain:ruby-doc.org)",
"WebFetch(domain:docs.oracle.com)",
"WebFetch(domain:spring.io)",
"WebFetch(domain:kotlinlang.org)",
"WebFetch(domain:learn.microsoft.com)",
"WebFetch(domain:hexdocs.pm)",
"WebFetch(domain:www.phoenixframework.org)"
```

#### Mobile

```json
"WebFetch(domain:reactnative.dev)",
"WebFetch(domain:expo.dev)",
"WebFetch(domain:flutter.dev)",
"WebFetch(domain:dart.dev)",
"WebFetch(domain:developer.apple.com)",
"WebFetch(domain:developer.android.com)"
```

#### Docker / DevOps

```json
"WebFetch(domain:docs.docker.com)",
"WebFetch(domain:kubernetes.io)",
"WebFetch(domain:helm.sh)",
"WebFetch(domain:www.terraform.io)",
"WebFetch(domain:docs.github.com)"
```

#### Security / Standards

```json
"WebFetch(domain:owasp.org)",
"WebFetch(domain:cheatsheetseries.owasp.org)",
"WebFetch(domain:datatracker.ietf.org)",
"WebFetch(domain:www.ietf.org)",
"WebFetch(domain:caniuse.com)"
```

The blanket `WebFetch` is recommended for most users — domain-scoped is only needed if you want to restrict which sites Claude can fetch. Pick categories that match your stack if going granular.

---

## Combining Presets

Presets stack. Examples:

| Project Type | Presets to Combine |
|-------------|-------------------|
| Next.js on Vercel | Universal + JavaScript/TypeScript + Vercel |
| Cloudflare Worker | Universal + JavaScript/TypeScript + Cloudflare Worker |
| Astro static site | Universal + JavaScript/TypeScript + Static Site Generators |
| Django app | Universal + Python + Database + Docker |
| Spring Boot app | Universal + Java/JVM + Database + Docker |
| Rails app | Universal + Ruby + Database + Docker |
| Laravel app | Universal + PHP + Database + Docker |
| Phoenix (Elixir) | Universal + Elixir + Database + Docker |
| .NET API | Universal + .NET + Database + Docker |
| WordPress plugin | Universal + PHP |
| Rust CLI | Universal + Rust |
| Go microservice | Universal + Go + Docker + Database |
| ML project | Universal + Python + AI/GPU |
| React Native app | Universal + JavaScript/TypeScript + Mobile Development |
| Flutter app | Universal + Mobile Development |
| iOS Swift app | Universal + Swift + macOS + Mobile Development |
| Railway deployment | Universal + JavaScript/TypeScript + Hosting Platforms |
| Stripe integration | Universal + JavaScript/TypeScript + SaaS CLIs |
| Linux server ops | Universal + Linux System + Docker |
| Google Workspace automation | Universal + JavaScript/TypeScript + Google Workspace CLI |
| Full-stack ops | Universal + JavaScript/TypeScript + Python + Docker + Database + MCP (blanket) |

When merging, deduplicate and keep the grouped `//` comment structure. The final `settings.local.json` should look like:

```json
{
  "permissions": {
    "allow": [
      "// --- Version Control ---",
      "Bash(git *)",
      "Bash(gh *)",
      "// --- Node.js ---",
      "Bash(node *)",
      "..."
    ],
    "deny": []
  }
}
```
