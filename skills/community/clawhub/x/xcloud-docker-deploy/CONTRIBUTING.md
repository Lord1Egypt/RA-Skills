# Contributing to xCloud Docker Deploy Skill

Thank you for your interest in contributing! This skill helps AI agents deploy projects to xCloud hosting.

## Ways to Contribute

### Add a New Stack
1. Add detection rules to `DETECT.md`
2. Add a reference guide to `references/xcloud-native-STACK.md` or `references/scenario-STACK.md`
3. Add a Dockerfile template to `dockerfiles/STACK.Dockerfile` (if Docker path)
4. Add a compose template to `compose-templates/STACK.yml` (if Docker path)
5. Add an example to `examples/STACK-app.md`
6. Update the routing table in `SKILL.md` Phase 0

### Fix or Improve
- Incorrect xCloud platform behavior → update `references/xcloud-constraints.md`
- Broken Dockerfile → fix `dockerfiles/`
- Better nginx config → update scenario references or compose templates

### Add Examples
Real-world deployment scenarios are welcome in `examples/`. Follow the existing format.

## Format Standards

- All files: Markdown (`.md`) or YAML/Dockerfile
- No executables, no network calls, no binary files
- Keep `SKILL.md` concise — detailed content goes in `references/`
- Test Dockerfiles with `docker build` before submitting

## Pull Request Process

1. Fork the repo
2. Create a branch: `feat/add-STACK-support` or `fix/ISSUE`
3. Make changes, update `CHANGELOG.md`
4. Open a PR against `main`

## Code of Conduct

Be respectful and constructive. This is a community tool.
