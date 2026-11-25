# Check, ship and test live

## Local production check (step 8)

Preview deploys often lack the database settings, so a preview link can fail for reasons that have nothing to do with the change. Check a real production build on this computer instead:

1. Build with placeholder keys: `NEXT_PUBLIC_SUPABASE_URL=https://example.supabase.co NEXT_PUBLIC_SUPABASE_ANON_KEY=placeholder npm run build` (on Windows, set the two values first, then run the build).
2. Start it with the same two values: `npm run start`.
3. Open it in a browser you can control (or ask the student to look): every signed-out page, any practice or preview pages, at phone width and wide, in light and dark, and in every language the app has. No errors in the console.
4. A signed-out call to any API route answers 401 with JSON, never a redirect to the sign-in page. A redirect is a real bug: the browser follows it, gets the sign-in page with status 200, and the app thinks the call worked.
5. Stop the server when you are done.

If the dev or preview server only reads its settings from the student's main folder (some apps read `.claude/launch.json` from there), start it from the worktree with a shell command that changes into the worktree first, and put back any file you changed.

## Stacked pull requests (step 10)

CodeRabbit's free plan skips pull requests with more than 150 changed files, writes one summary an hour, and only reviews pull requests aimed at the default branch on its own. A huge pull request is also hard for a person to read. So a big review ships as a stack: several pull requests, each building on the one before.

1. With a yes, commit the urgent fixes first, on their own, so they can ship even if the rest waits.
2. Write a stages file, an ordered list of patterns, the last one `.*`:
   ```json
   [ {"name": "1-hotfix", "match": "^(package(-lock)?\\.json|src/lib/auth/)"},
     {"name": "2-security", "match": "^(src/proxy\\.ts|src/app/api/(account|auth)/)"},
     {"name": "3-rest", "match": ".*"} ]
   ```
   Keep `package.json` and its lock file in the same stage (the script moves the lock file there if you forget), and put dependency changes in the first stage that needs them: each stage is checked with the big branch's installed packages, so add `--test "npm ci && npm run build"` when a stage changes dependencies.
3. Try it first: `node "${CLAUDE_PLUGIN_ROOT}/scripts/review/split-stack.mjs" --from <big branch> --stages <stages.json> --prefix release/<name>- --dry-run`. Every stage should be at or under 150 files; change the patterns until they are.
4. Then, with a yes (it makes a commit on each stage branch), for real from a clean checkout, with the tests: `node "${CLAUDE_PLUGIN_ROOT}/scripts/review/split-stack.mjs" --from <big branch> --stages <stages.json> --prefix release/<name>- --test "npm test"`. Each stage branch passes the type check and the tests on its own; files a stage needs are pulled forward from later stages automatically. The last stage is identical to the big branch.
5. With a yes, push the branches and open one pull request per stage: the first aimed at `main`, each next one at the stage before it.
6. Merge with a merge commit, not a squash: after a squash merge, the next pull request shows the earlier stage's files again and can go back over 150. If one was squashed anyway, rebase the next stage onto `main` first (`git rebase --onto origin/main <previous stage branch> <next stage branch>`), with a yes before the force push.
7. After each merge: wait for the production deploy to finish, then smoke-test the live address (pages answer 200, a signed-out API call answers 401 JSON, one real call that needs a login or an API key, the deployed commit is the merged one). Change the next pull request's target to `main`, and merge it only with the student's yes.

Never push straight to a branch that deploys. One merge is one deploy.

## Live microphone test (step 11)

For apps that record from the microphone (live transcription, meeting notes, voice input). It needs macOS for the voices; elsewhere, read the script aloud.

1. Before you start: headphones off and AirPods disconnected (the microphone cannot hear them; the transcript then stays at "Listening..."), volume up.
2. In a browser where the student is signed in, open the live page, choose the microphone or "in person" source, and start recording.
3. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/review/voice-test.mjs"`. It plays a one-minute conversation between two voices with one action item and a deadline. `--dry-run` shows the script; `--script <file>` uses your own ("A: ..." and "B: ..." lines).
4. Wait for the live transcript and notes, then stop and save.
5. Check the saved record: full audio length, two speakers, a summary, the notes, the action item with its date. Read it back through the app's own API or MCP tool if it has one.
6. Tell the student a test record was created, and offer to delete it.
