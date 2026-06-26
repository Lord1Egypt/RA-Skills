# Addressing Review Comments

Step-by-step workflow for responding to PR review comments.

## Workflow

1. **Fetch PR details:**
   ```bash
   gh pr view <number> --repo <owner/repo> --json title,body,headRefName,baseRefName,files
   ```

2. **Clone and checkout the PR branch:**
   ```bash
   gh repo clone <owner/repo> && cd <repo>
   git fetch origin && git checkout <headRefName>
   ```

3. **Fetch all review comments:**
   ```bash
   # Inline comments
   gh api repos/<owner/repo>/pulls/<number>/comments --paginate
   # Review-level comments
   gh api repos/<owner/repo>/pulls/<number>/reviews --paginate
   ```

4. **Address each comment:** Fix the code, or document a clear reason not to.

5. **Commit fixes** — atomic commits per logical change:
   ```bash
   git commit -m "fix: <what was fixed>

   Addresses review comment by @<reviewer>"
   ```

6. **Reply to every comment** — no comment left unacknowledged:
   ```bash
   # Reply to inline comment
   gh api repos/<owner/repo>/pulls/<number>/comments/<id>/replies \
     -f body="<your reply>"
   # Reply to review-level comment
   gh api repos/<owner/repo>/issues/<number>/comments \
     -f body="<your reply>"
   ```
   - If fixed: describe exactly how
   - If not fixed: explain why (disagree, out of scope, won't fix)

7. **Resolve threads via GraphQL:**
   ```bash
   # List review threads
   gh api graphql -f query='
   {
     repository(owner:"<owner>", name:"<repo>") {
       pullRequest(number:<number>) {
         reviewThreads(first:100) {
           nodes {
             id
             isResolved
             comments(first:10) {
               nodes { body author { login } }
             }
           }
         }
       }
     }
   }'

   # Resolve a thread
   gh api graphql -f query='
   mutation {
     resolveReviewThread(input:{threadId:"<THREAD_ID>"}) {
       thread { isResolved }
     }
   }'
   ```

8. **Update the PR description** to reflect all changes made.

9. **Push and present a summary:**
   ```bash
   git push origin <headRefName>
   ```

   | Comment / Issue | Action Taken |
   |-----------------|--------------|
   | @reviewer: "..." | Fixed in commit abc1234 — ... |
   | @reviewer: "..." | Won't fix — reason |
