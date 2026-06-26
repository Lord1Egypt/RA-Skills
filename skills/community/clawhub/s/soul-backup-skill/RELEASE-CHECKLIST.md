# Release Checklist

Use this checklist before publishing SOUL Backup Skill to ClawHub or GitHub.

## Pre-Release

### Code Quality
- [ ] All scripts executable: `chmod +x scripts/*.mjs`
- [ ] No hardcoded paths (use `__dirname` resolution)
- [ ] Error handling in all scripts
- [ ] No console.log debugging statements
- [ ] Consistent code style

### Testing
- [ ] Create test backup: `node scripts/backup.mjs --name "test"`
- [ ] Validate backup: `node scripts/validate.mjs`
- [ ] Test dry-run restore: `node scripts/restore.mjs --dry-run`
- [ ] Test actual restore: `node scripts/restore.mjs --name test`
- [ ] Verify files restored correctly
- [ ] Test rollback: restore pre-restore backup
- [ ] Test single file restore: `node scripts/restore.mjs --file SOUL.md`
- [ ] Test corrupted backup detection (manually corrupt a file)
- [ ] Test with missing BOOTSTRAP.md (expected warning)
- [ ] Test with all 7 SOUL files present

### Documentation
- [ ] README.md complete and accurate
- [ ] QUICKSTART.md tested step-by-step
- [ ] EXAMPLES.md all examples verified
- [ ] SKILL.md comprehensive
- [ ] RUNBOOK.md covers all scenarios
- [ ] CHANGELOG.md up to date
- [ ] LICENSE file present (MIT)
- [ ] All links working (no 404s)
- [ ] No placeholder text (YOUR-USERNAME, etc.)

### Security
- [ ] No API keys or secrets in code
- [ ] No sensitive data in example backups
- [ ] Backup directory permissions documented
- [ ] Security notes in README.md
- [ ] .gitignore includes backups/ directory

### Repository
- [ ] .gitignore created:
  ```
  backups/
  node_modules/
  .DS_Store
  *.log
  ```
- [ ] Clean git history (no sensitive commits)
- [ ] All files committed
- [ ] Version tagged: `git tag v1.0.0`

## Release

### GitHub
- [ ] Create repository: `soul-backup-skill`
- [ ] Push code: `git push origin main`
- [ ] Push tags: `git push origin --tags`
- [ ] Create GitHub release (v1.0.0)
- [ ] Add release notes from CHANGELOG.md
- [ ] Upload any release assets (if applicable)

### ClawHub (Optional)
- [ ] Create ClawHub account
- [ ] Publish skill: `clawhub publish`
- [ ] Verify skill page on clawhub.com
- [ ] Test installation: `clawhub install soul-backup`

### Documentation
- [ ] Update README.md with correct GitHub URLs
- [ ] Update installation instructions
- [ ] Add badges (license, version, etc.)
- [ ] Link to GitHub Issues for support

## Post-Release

### Community
- [ ] Announce on OpenClaw Discord
- [ ] Post on Reddit r/OpenClaw (if exists)
- [ ] Share on X/Twitter
- [ ] Add to OpenClaw community skills list

### Monitoring
- [ ] Watch GitHub Issues
- [ ] Monitor ClawHub downloads (if published)
- [ ] Collect user feedback
- [ ] Plan next version features

### Maintenance
- [ ] Set up GitHub Actions for CI (optional)
- [ ] Enable Dependabot (optional)
- [ ] Create CONTRIBUTING.md (optional)
- [ ] Add issue templates (optional)

## Version Bump Checklist (Future Releases)

- [ ] Update version in CHANGELOG.md
- [ ] Update version in README.md badges
- [ ] Create git tag: `git tag vX.Y.Z`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Create GitHub release
- [ ] Update ClawHub (if published)
- [ ] Announce update

---

**Ready to release?** Run through this checklist and check every box before publishing.
