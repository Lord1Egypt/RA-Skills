# Store publishing gotchas

Lessons from shipping a real app. Each one cost hours.

- **supabase-js needs Node 22.** Seed and admin scripts fail in odd ways on Node 20. Run them with `npx -y node@22 script.mjs` if the computer has an older Node.
- **`auth.admin.listUsers` can return 500** on a big or shared auth project. Do not loop through users to find one. Use a small security-definer database function that returns the id for an email (callable only by the service role), or `createUser` and handle "already registered".
- **Set the demo password explicitly.** A password passed to `createUser` for an existing or earlier-invited user may not work for sign-in. Always call `auth.admin.updateUserById(id, { password, email_confirm: true })` in the seed script, then test a real password sign-in.
- **Vercel free plan deploy limit.** The free plan allows about 100 deployments a day; many agents and preview branches use it up, and `vercel deploy --prod` then fails with `api-deployments-free-per-day` for 24 hours. Check before planning a production redeploy, avoid needless preview deploys, and promote an existing ready deployment of the same commit when there is one.
- **Shared workspaces change under you.** When several agents share one computer and folder, another agent may switch branches, delete `node_modules` or leave a detached HEAD. Check `git status` and the branch right before every commit and push, work in your own `git worktree` when you can, reinstall packages if missing, use a random free port for dev servers, and only ever force-push your own branch.
- **MCP connector started before its token file existed.** A connector (for example `mcp-remote`) that reads a token file at start does not notice a file written later. It falls back to an OAuth sign-in and hangs. Create the token first, then restart the connector. Prefer passing the token through an environment variable over a command-line argument, which other processes can read.
- **Do not trust the old privacy page.** New features (voice clips, digest emails) are often missing from it. Re-read the code before every submission.
- **Production may be behind main.** Screenshots must show the features the reviewer will see. Check that the live site has them, or redeploy first.
