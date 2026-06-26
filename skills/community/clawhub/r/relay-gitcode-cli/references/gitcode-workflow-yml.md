# GitCode Workflow YAML Examples

Use this reference when creating or updating GitCode Pipeline workflow files
under `.gitcode/workflows`, especially `.gitcode/workflows/ci.yml`.

Official GitCode Pipeline documentation describes workflows as YAML files stored
under `.gitcode/workflows`. A workflow has trigger events, one or more jobs, and
ordered steps. Jobs run on a GitCode runner such as `euleros-2.10.1`, and steps
can either run shell commands or use reusable actions such as
`checkout-action@0.0.1`, `setup-node@0.0.1`, `setup-java@0.0.1`,
`setup-python@0.0.1`, and `setup-go@0.0.1`.

Sources:

- <https://docs.gitcode.com/en/docs/help/home/org_project/pipeline/pipeline-intro1/>
- <https://docs.gitcode.com/docs/help/home/org_project/pipeline/pipeline-intro1/>

## Style

- Store workflow files in `.gitcode/workflows`.
- Use `ci.yml` for the main continuous-integration workflow unless the project
  already has a clearer local naming convention.
- Keep YAML indentation at two spaces.
- Use a clear top-level `name`.
- Prefer explicit branch filters for `push` and `pull_request`.
- GitCode documents manual triggers as a pipeline capability, but the public
  intro page does not show a YAML key for that trigger. Do not add
  `workflow_dispatch` to reusable examples unless the target GitCode project has
  already confirmed that syntax.
- Start each job by checking out the repository with `checkout-action@0.0.1`.
- Run repository commands from `repo_workspace` after checkout.
- Keep secrets in GitCode project secrets or environment configuration, not in
  workflow files.
- Keep GitCode workflow examples separate from GitHub Actions examples. Do not
  use `actions/checkout`, `ubuntu-latest`, or GitHub-only workflow surfaces.
- GitCode documents `setup-java@0.0.1`, `setup-python@0.0.1`, and
  `setup-go@0.0.1` as available built-in actions, but this reference does not
  guess their `with` inputs without action-specific docs.

## Minimal CI

```yaml
name: ci

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
      - name: Inspect workspace
        run: |
          cd repo_workspace
          pwd
          ls
```

## CodeCheck

Use `gd pipeline codecheck` to generate this workflow so the personal access
token is referenced through a project secret instead of committed as a literal
value:

```bash
gd pipeline codecheck --repo owner/repo --language SHELL --access-token-secret CODECHECK_ACCESS_TOKEN --json
```

The generated workflow uses `codecheck-action@0.0.3` with `repo_url`,
`branch`, `rule_sets`, and `access_token` inputs as documented by GitCode
CodeCheck. Pull request runs pass the PR source repository and branch to
CodeCheck; push runs pass the configured repository URL and current ref.

## Rust CLI CI

Use this shape for Rust command line projects. It installs stable Rust inside
the clean EulerOS runner, then runs the same local gate used by this repository.

```yaml
name: ci

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  rust:
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
      - name: Install Rust stable
        run: |
          cd repo_workspace
          curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable
          "$HOME/.cargo/bin/rustup" component add rustfmt clippy
      - name: Format gate
        run: |
          cd repo_workspace
          "$HOME/.cargo/bin/cargo" fmt --all -- --check
      - name: Clippy gate
        run: |
          cd repo_workspace
          "$HOME/.cargo/bin/cargo" clippy --all-targets --all-features -- -D warnings
      - name: Test suite
        run: |
          cd repo_workspace
          "$HOME/.cargo/bin/cargo" test --all-targets --all-features
      - name: Build
        run: |
          cd repo_workspace
          "$HOME/.cargo/bin/cargo" build --all-targets --all-features
```

## Node CI

This follows the GitCode documentation pattern for `setup-node@0.0.1`.

```yaml
name: node-ci

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  node:
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
      - name: Use Node.js
        uses: setup-node@0.0.1
        with:
          node-version: '20.10.0'
      - run: cd repo_workspace && npm ci
      - run: cd repo_workspace && npm run build --if-present
      - run: cd repo_workspace && npm test
```

## Other Language Actions

The public GitCode Pipeline intro lists `setup-java@0.0.1`,
`setup-python@0.0.1`, and `setup-go@0.0.1` as built-in actions. It does not show
their input names. When writing Java, Python, or Go templates, use the action
documentation or a known-good workflow from the target project before adding
`with` keys.
