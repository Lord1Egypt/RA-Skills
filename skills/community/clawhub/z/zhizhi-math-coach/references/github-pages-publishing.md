# GitHub Pages Publishing

## Purpose

Use GitHub Pages for child-facing worksheet HTML/PDF when the parent accepts public worksheet links. PDF delivery stays first: generate or send `worksheet.pdf` before waiting for Pages when the channel supports file replies.

Do not publish answers, diagnosis records, long-term memory, weak-point history, student photos, school papers, or textbook files.

## Default Flow

After generating a worksheet PDF/HTML in a Pages-enabled public personal repository, publish and wait when a public link is needed or when `.zhizhi-math-coach/config.json` has `pages.auto_publish_worksheets: true`:

```bash
python3 {baseDir}/scripts/publish_and_wait_pages.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <personal-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

The script:

1. Copies public-safe worksheet HTML and `worksheet.pdf` into `site/` when the PDF exists.
2. Rebuilds `site/index.html` from all worksheets.
3. Pulls the remote branch with `git pull --rebase --autostash` before committing, unless `--no-pull` is passed.
4. Stages only public-safe publishing files: `site/`, `.github/workflows/pages.yml` when present, and `worksheets/*/publish.json`.
5. Commits and pushes to the configured branch.
6. If push is rejected because the remote changed, pulls with rebase and retries once.
7. Waits for the GitHub Actions Pages workflow for that commit.
8. Checks the Pages index and worksheet URLs before reporting `pages-ready`.

Use local-only publishing when GitHub sync is unavailable or the parent asks only for files:

```bash
python3 {baseDir}/scripts/publish_html_site.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <personal-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

The publisher writes:

- `site/index.html`: public worksheet list.
- `site/worksheets/<slug>/index.html`: child-facing worksheet page.
- `site/worksheets/<slug>/worksheet.pdf`: child-facing worksheet PDF when generated.
- `site/.nojekyll`: disables Jekyll processing.
- `worksheets/YYYY-MM-DD-topic/publish.json`: publication manifest.

The index is rebuilt from all public-safe worksheet HTML files under `worksheets/`, even when publishing a single worksheet path. It sorts worksheets by date descending and shows date, practice status, title, file links, topic, grade, item count, and completion summary. Practice status is inferred from `worksheets/status.md` when available; otherwise a generated worksheet is shown as `未练习`.

This only produces local `site/` files. A public URL requires the personal learning repository to be pushed to GitHub and GitHub Pages to be configured for that repository.

## Public Repository Mode

If the parent chooses to make the personal learning repository public to avoid paid private Pages:

- Clarify that the whole public repository is viewable, not only the Pages site. Public Pages makes `site/` easy to open, but GitHub users can also browse tracked files outside `site/`.
- Use this mode only when the parent accepts public visibility of committed files, or when the repository commits only public-safe files.
- Do not add collaborators unless they should be able to push.
- For `main`, public GitHub repositories are read-only to non-collaborators by default. Recommend branch protection/rulesets to block force pushes and branch deletion. Do not enable a rule that requires pull requests or blocks direct pushes if OpenClaw is expected to push `site/` and workflow updates directly.

Recommended GitHub Pages setting:

1. Repository Settings -> Pages.
2. Build and deployment -> Source: `GitHub Actions`.
3. If not present, create `.github/workflows/pages.yml` with the bundled setup script:

```bash
python3 {baseDir}/scripts/setup_github_pages_workflow.py \
  --workspace <personal-learning-workspace>
```

If GitHub sync is already authorized through the Deploy key, OpenClaw may commit and push this workflow after the parent asks it to set up Pages:

```bash
git add .github/workflows/pages.yml site
git commit -m "Configure GitHub Pages publishing"
git push
```

The push triggers the GitHub Actions Pages deployment. Return the expected URL `https://<github-user>.github.io/<repo>/` and tell the parent that the first deployment may take a short time.

In normal worksheet generation, first return or send the generated `worksheet.pdf` when available. If Pages mode is already configured in `.zhizhi-math-coach/config.json`, run `publish_and_wait_pages.py` after `generate_worksheet.py` without asking again when `pages.auto_publish_worksheets` is true. Otherwise run it only when a public link is wanted. Return:

- the public index URL;
- the newly generated worksheet URL;
- local paths for `worksheet.pdf`, `worksheet.html`, and `answer-key.md`.

If deployment fails or times out, do not hide the local result. Return local paths, pushed commit if known, and the Actions run URL or next setup step.

Recommended ruleset for direct OpenClaw publishing:

- Ruleset name: `main protect`.
- Enforcement status: `Active`.
- Bypass list:
  - `Deploy keys`: `Always allow`.
  - `Repository admin`: `Always allow`.
- Target branches: `main`, or `Default` if the default branch is `main`.
- Enabled rules:
  - `Restrict updates`.
  - `Restrict deletions`.
  - `Block force pushes`.
- Disabled rules:
  - `Require a pull request before merging`.
  - `Require status checks to pass`.
  - `Require signed commits`.
  - `Require deployments to succeed`.

This keeps the repository public-readable while allowing only the deploy key and repository admin to update `main`. It also avoids turning every OpenClaw update into a manual PR/merge flow.

## Public Content Rule

Allowed in `site/`:

- child-facing worksheet HTML;
- child-facing worksheet PDF;
- worksheet title, date, topic, and strategy;
- generated SVG diagrams and blank answer spaces.

Forbidden in `site/`:

- `answer-key.md`;
- answers or `answer_detail`;
- `records/`, `mistakes/`, `memory/`, `weak-points/`, `knowledge-points/`, `curriculum/`;
- completed worksheet photos, school papers, textbook PDFs, scans, or OCR output.

## OpenClaw Output Rule

When Pages is configured, return the PDF file/path first, then the Pages URL when deployment is ready. Use the Pages URL in Feishu notifications when available, and send the PDF file when the channel supports file messages. Keep answer keys and diagnosis links outside published `site/` output.

If the parent asks OpenClaw to sync, push, publish to GitHub, or send a public link, or if workspace config enables automatic publishing, read `github-sync-authorization.md` first. Do not assume GitHub CLI, GitHub token environment variables, or saved credentials are available. Use the Git preflight before newly enabling sync; after config is enabled, the sync/publish scripts should pull, commit, and push automatically. If authorization is missing, keep the local `site/` output, generate or suggest a repository Deploy key, send the public key and GitHub Settings -> Deploy keys guidance through Lark/Feishu when available, and return the local `site/` paths.
