# LDM OS v0.4.14

Three fixes from dogfood:

1. **Deploy safety** (#69): abort if build fails or dist/ missing. Prevents overwriting working extensions with unbuilt clones.
2. **Spawn loop** (#70): wip-install --version exits immediately. Was triggering recursive process spawning.
3. **npm install null** (#74): skip extensions with no catalog repo instead of running npm install null.
4. **Process monitor** (#75): auto-kill zombie npm/ldm processes every 3 min via cron. ldm init deploys it.
5. **Catalog show** (#72): `ldm catalog show <name>` describes what each component installs.

## Issues closed

- Closes #69
- Closes #70
- Closes #72
- Closes #74
- Closes #75
