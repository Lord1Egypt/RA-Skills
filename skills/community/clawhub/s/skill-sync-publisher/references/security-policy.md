# Security policy

Preflight blocks obvious credentials and private material:

- `.env`, `.env.*`, private keys, cloud credential files, and credential-like
  filenames
- files containing common secret assignments such as `*_TOKEN=`,
  `*_API_KEY=`, or `PRIVATE KEY`
- absolute home-directory references in scripts
- executable files outside an explicit `scripts/` directory

These checks are heuristic, not a malware scanner. A user may remove a false
positive from the skill or explicitly review it outside this CLI. The sync
command never uploads a blocked skill.
