Here's the complete brief to give the other session. Everything needed: direct answers to their three
  asks, the audit, the buck framing, the diagnosis they produced, the approved fix path, and the
  orchestration. No bypasses, no workarounds.                                                              
   
  ---                                                                                                      
  Brief for CC-mini: wip-branch-guard cross-session state-collision fix
                                                                                                           
  Parker wants you to ship this fix end to end with no bypasses and no "please run this" asks. Everything
  below is the full context. Read it all before touching anything.                                         
                                                         
  Direct answers to your three asks                                                                        
                                                         
  1. Unstick the guard. Do not use LDM_GUARD_SKIP_ONBOARDING. That env var is itself part of the problem   
  (see buck framing below). Your diagnosis was correct: this is a real bug. Don't bypass it, fix it.
  2. Abandon the empty cc-mini/fix-template-ds-store branch. Yes. Parker approved. Do this as step 0 below.
  3. Finding #1 fix path (A vs B). Deferred. Parker does not want root-level templates (A) or hardcoded    
  defaults (B). The .DS_Store ticket is not workaround-able cleanly right now, and he explicitly said      
  "let's not work around it." Park the ticket and come back to it after the guard is stable. Do not mix the
   two PRs.                                                                                                
                                                         
  Context: audit of current enforcement                                                                    
   
  What's actually enforced                                                                                 
                                                         
  - Onboarding-before-first-write lives in ~/.ldm/extensions/wip-branch-guard/guard.mjs (lines 552-566,    
  770-779). First write to a repo new to the session is blocked until the agent has Read the repo's
  README.md, CLAUDE.md, and any *RUNBOOK*.md / *LANDMINES*.md / WORKFLOW*.md. Canonical repo key (v1.9.81+)
   means reading once covers all worktrees. 2-hour TTL per repo per session.
  - Bypass detection logs file-write denials per session (20 entries, 1-hour window). Second attempt on
  same path re-blocked with prior context. Directly catches "Edit X denied → cat > X" pattern.             
  - Destructive-command + deploy-path blocks: cp into .openclaw/extensions/ or .ldm/extensions/ is blocked
  (line 352). npm link, npm install -g blocked (lines 347-352). python -c "open().write()" and node -e     
  "writeFile()" blocked (lines 264-267).                 
  - File-guard (~/.ldm/extensions/wip-file-guard/guard.mjs) blocks Write on identity files (CLAUDE.md,     
  SHARED-CONTEXT.md, SOUL.md, MEMORY.md) and memory/journal patterns.                                      
   
  Gaps aligned to failure modes A/B/C                                                                      
                                                         
  A. No auto-scan on first repo contact. The onboarding gate is reactive. Fires on the first write attempt,
   not on session start or first cd. If you don't try to write, the scan never happens. SessionStart hook
  at ~/.ldm/shared/boot/boot-hook.mjs injects context but doesn't detect "new repo in cwd and not yet      
  onboarded." Ritual documented in DEV-GUIDE-GENERAL-PUBLIC.md but no hook behind it.

  B. Shell redirection is a real hole. Guard blocks Edit/Write tools and catches python -c / node -e, but  
  Bash >, >>, tee to protected paths (e.g. echo '{...}' > ~/.openclaw/openclaw.json or jq '.' ... > 
  ~/.openclaw/...) is not pattern-matched. This is the exact class of bypass we kept hitting.              
                                                         
  C. Bypass audit trail is passive. ~/.ldm/state/bypass-audit.jsonl records denials and env-var overrides  
  (LDM_GUARD_SKIP_ONBOARDING=1, LDM_GUARD_ACK_BLOCKED_FILE=...). Nothing parses it at SessionStart or Stop
  to surface repeat bypasses to Parker.                                                                    
                                                         
  DevOps Toolkit vs LDM OS split                                                                           
   
  - LDM OS is where the mechanical enforcement lives: all four hooks (wip-branch-guard, wip-file-guard,    
  wip-repo-permissions-hook, wip-license-guard) are registered in ~/.claude/settings.json as PreToolUse.
  - DevOps Toolkit (wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md) documents the ritual, the   
  Merge/Deploy/Install split, and worktree workflow. Advisory only. The toolkit doesn't ship an onboarding 
  preflight or a cold-start check.
                                                                                                           
  Coverage is asymmetric: LDM OS enforces at write-time, the DevOps Toolkit describes the ritual. Neither  
  has the proactive "scan this repo before you do anything" step. That's Gap A, out of scope for this PR.
                                                                                                           
  The buck (why this bug matters beyond the immediate symptom)                                             
   
  The guard has a bug (cross-session state ping-pong on shared ~/.ldm/state/guard-session.json), AND two   
  env-var escape hatches (LDM_GUARD_SKIP_ONBOARDING, LDM_GUARD_ACK_BLOCKED_FILE) exist so any stuck agent
  can bypass it. Together they train agents to route around the guard instead of fixing it. That's the     
  "every time we fix it, it's still not fixed" pattern: the bypass surface means the underlying bug never
  has to actually be triaged. Every time an agent proposes "run this env var," that's the workaround system
   working as designed, not a one-off.

  So this PR has to do two things together, not just one: kill the acute state bug, and remove the         
  workaround surface that let the bug hide.
                                                                                                           
  Diagnosis (confirmed)                                                                                    
  
  - State keyed globally, not by session. ~/.ldm/state/guard-session.json is a single file shared by every 
  CC session on the machine.                             
  - detectNewSession() fires on session_id mismatch and calls emptyState(), wiping                         
  onboarded_repos_canonical, read_files, and recent_denials.                                               
  - Parallel CC sessions (Parker runs them routinely; documented in his auto-memory) ping-pong each other's
   state on every tool call. This is why onboarding appears to drop mid-session even after a successful    
  first write.                                           
  - Secondary: read-modify-write isn't atomic. Two guard.mjs processes from parallel tool calls in the same
   session race on the state file. Rename is atomic, the read-then-write window is not.                    
  
  Fix path (approved)                                                                                      
                                                         
  In this order, in one PR:                                                                                
                                                         
  1. Per-session state file. ~/.ldm/state/guard-session-<sid>.json. Eliminates cross-session ping-pong at  
  the source. Cleanup via mtime TTL at each invocation. This is Option 1 from your diagnosis. Option 2
  (nested single file + locking) was rejected: it still serializes every tool call across every session    
  through one file, which is slow and deadlock-prone if a process dies holding the lock.
  2. Atomic read-modify-write within a session. Either flock on the per-session file, or compare-and-swap
  with tmp+rename under a content hash check. Keeps same-session parallel tool calls from clobbering each  
  other's read_files additions.
  3. Remove the env-var escape hatches. Delete all handling of LDM_GUARD_SKIP_ONBOARDING and               
  LDM_GUARD_ACK_BLOCKED_FILE from guard.mjs. Without them, "fix the guard" is the only path forward the    
  next time state breaks. The state bug was the acute cause. The hatches are the standing workaround
  surface. Both go in this PR.                                                                             
  4. (Preferred, optional) SessionStart sanity check. If the per-session state file is corrupt or older
  than session start, warn loudly at boot rather than silently reset. Surface corruption before the next   
  blocked write.
                                                                                                           
  Tradeoff being accepted                                                                                  
  
  Once #3 lands, a future guard malfunction really does strand the agent in-session. We'd have to patch +  
  install before proceeding. Accept this because the alternative (keep the hatches) keeps the workaround
  loop alive. Compensate with good logging in #1 and #2 so the next state bug is triaged in minutes, not   
  hours.                                                 

  Out of scope for this PR                                                                                 
  
  - Gap A (proactive SessionStart scan). Mention in RELEASE-NOTES.                                         
  - Gap B (shell redirection pattern matching: >, >>, tee into protected paths). Mention in RELEASE-NOTES.
  - Gap C (bypass audit escalation at SessionStart/Stop). Mention in RELEASE-NOTES.                        
  - .DS_Store scaffold work in wip-ai-devops-toolbox-private. Deferred per Parker.                         
                                                                                                           
  Orchestration                                                                                            
                                                                                                           
  Step 0: abandon the stale branch                                                                         
  
  Parker approved. Run:                                                                                    
                                                         
  cd /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private
  git worktree remove .worktrees/wip-ai-devops-toolbox-private--cc-mini--fix-template-ds-store             
  git branch -D cc-mini/fix-template-ds-store                                                              
                                                                                                           
  Step 1: clean runtime state before the fix                                                               
                                                         
  Ask Parker once to close any other active CC sessions on the machine (including the one that produced    
  this brief). Each additional session clobbers guard state during onboarding, which will make the bug
  you're fixing bite you while fixing it. This is not a workaround. It's making sure no other process is   
  wiping your state during the bootstrap.                

  Once you're the only CC session making tool calls, proceed.

  Step 2: worktree + onboarding                                                                            
  
  cd /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private                          
  git fetch origin                                                                                         
  git worktree add .worktrees/wip-ai-devops-toolbox-private--cc-mini--fix-guard-cross-session -b
  cc-mini/fix-guard-cross-session                                                                          
  cd .worktrees/wip-ai-devops-toolbox-private--cc-mini--fix-guard-cross-session
                                                                                                           
  Before any Write/Edit, Read the onboarding set in a single turn with parallel tool calls:                
  - README.md                                                                                              
  - CLAUDE.md (if present)                                                                                 
  - DEV-GUIDE-GENERAL-PUBLIC.md                          
  - Any root-level *RUNBOOK*.md, *LANDMINES*.md, WORKFLOW*.md                                              
  - tools/wip-branch-guard/README.md (if present)            
                                                                                                           
  Doing them in one turn minimizes the window for cross-session clobber.                                   
                                                                                                           
  Step 3: write the fix                                                                                    
                                                                                                           
  Source: tools/wip-branch-guard/guard.mjs                                                                 
  
  Changes:                                                                                                 
  - Replace single-file state with per-session state file at ~/.ldm/state/guard-session-<sid>.json.
  - Update readSessionState, writeSessionState, detectNewSession, emptyState to key by session.            
  - Add TTL-based cleanup of stale per-session files (mtime older than configurable window; default 24h).
  - Add flock-based atomic read-modify-write OR compare-and-swap write.                                    
  - Remove all handling of LDM_GUARD_SKIP_ONBOARDING and LDM_GUARD_ACK_BLOCKED_FILE. Grep for both. Delete 
  all call sites. Update any associated docs and error messages.                                           
                                                                                                           
  Step 4: tests                                                                                            
                                                                                                           
  Add tests under the tool's existing test pattern. Cover:                                                 
  - Two simulated sessions don't wipe each other's state.
  - Parallel tool calls within one session don't lose read_files entries.                                  
  - TTL cleanup removes stale files but preserves recent ones.           
  - Env vars no longer bypass onboarding (explicit assert that setting them has no effect).                
                                                                                                           
  Step 5: RELEASE-NOTES.md on the branch                                                                   
                                                                                                           
  Before opening the PR, write RELEASE-NOTES.md. Cover:                                                    
  - What changed (per-session state, atomic writes, hatch removal).                                        
  - Migration note: old global state file at ~/.ldm/state/guard-session.json can be deleted. Document the  
  cleanup path.                                                                                          
  - Known gaps still open: Gap A, B, C from the audit above.                                               
                                                            
  Step 6: PR → merge → release → deploy                                                                    
                                                                                                           
  push → gh pr create → gh pr merge --merge (NEVER squash) → git pull on main → wip-release patch →        
  deploy-public.sh if the public twin exists                                                               
                                                         
  Do not install. Parker runs Read https://wip.computer/install/wip-ldm-os.txt when he's ready.            
                                                         
  Step 7: after Parker installs, confirm the fix                                                           
                                                         
  Open two CC sessions side by side. Verify each has its own state file. Verify onboarding state survives  
  cross-session tool calls. Verify the env vars no longer override anything. Write a short confirmation
  note somewhere appropriate (daily log, etc).                                                             
                                                         
  What NOT to do

  - Do not set LDM_GUARD_SKIP_ONBOARDING=1. Do not set LDM_GUARD_ACK_BLOCKED_FILE=.... If you're tempted,  
  the right answer is to fix whatever made you tempted.
  - Do not pivot from a blocked Edit to jq, cat >, tee, or any other shell redirection. That's exactly the 
  bypass pattern Parker called out.                                                                        
  - Do not edit deployed files at ~/.ldm/extensions/wip-branch-guard/. Only edit the source repo.
  - Do not squash merge. --merge only.                                                                     
  - Do not push to main.                                 
  - Do not add root-level templates or hardcoded defaults to solve .DS_Store. Deferred.                    
  - Do not ask Parker to run manual bash to unstick you. If you're truly blocked and the only move is a    
  destructive one that the guard prevents, name the block precisely and propose the code change. No "please
   run this env var" asks.                                                                                 
                                                                                                           
  Success criteria                                       

  - Parallel CC sessions no longer wipe each other's onboarding state.                                     
  - Second Edit in a session after a successful first-write does not re-trigger onboarding.
  - LDM_GUARD_SKIP_ONBOARDING and LDM_GUARD_ACK_BLOCKED_FILE no longer exist in guard.mjs or anywhere else 
  in the source.                                                                                           
  - Fix shipped through the normal path: PR → merge → wip-release → deploy-public → install.               
  - Parker never had to run anything outside the install prompt.                                           
                                                                                     