# Release Workflow

Detailed reference for the tag-push-release mechanics.

## Version Detection

Check `package.json` first:

```bash
node -p "require('./package.json').version" 2>/dev/null
```

If no package.json, ask user for version. Always prefix with `v` (e.g., `v1.0.0`).

## Monorepo Tags

In monorepos, use scoped tags:

```bash
# Single repo
git tag -a v1.0.0 -m "Release v1.0.0"

# Monorepo
git tag -a mypackage-v1.0.0 -m "Release mypackage v1.0.0"
```

## Tag Conflicts

If tag already exists locally:

```bash
# Delete local tag
git tag -d v1.0.0

# If also on remote (dangerous — confirm with user)
git push origin :refs/tags/v1.0.0
```

## Push Sequence

Always push branch first, then tags:

```bash
BRANCH=$(git branch --show-current)
git push origin ${BRANCH}
git push origin --tags
```

If push fails:
- Set upstream: `git push -u origin ${BRANCH}`
- Check auth: `gh auth status`
- Verify remote: `git remote -v`

## Release Notes

Generate from commits since last tag:

```bash
LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

if [ -z "$LAST_TAG" ]; then
  git log --oneline --no-merges HEAD
else
  git log --oneline --no-merges ${LAST_TAG}..HEAD
fi
```

Format as markdown bullet list under `## What's New`.

## gh release create

```bash
# Standard release
gh release create v1.0.0 --title "Release v1.0.0" --notes "## What's New
- Feature A
- Bug fix B"

# Pre-release (beta/rc)
gh release create v1.0.0-beta.1 --title "v1.0.0 Beta 1" --notes "..." --prerelease

# Draft (not published)
gh release create v1.0.0 --title "Release v1.0.0" --notes "..." --draft
```

## Post-Release

Depending on project type:
- **npm package**: `npm publish`
- **Announce**: Social media, relevant communities
- **Update docs**: Ensure README references latest version
