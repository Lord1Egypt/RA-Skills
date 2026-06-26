## Description: <br>
Manages Supabase migrations, types generation, RLS policies, and edge functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, create, apply, and verify Supabase database migrations, RLS policies, generated TypeScript types, and edge functions for Next.js projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide database schema and deployment changes that may affect live Supabase projects. <br>
Mitigation: Use development credentials by default, verify the target Supabase project before running commands, and manually approve production migrations or deployments after reviewing dry-run output. <br>
Risk: Service-role credentials used for admin operations could be exposed or misused. <br>
Mitigation: Protect the service-role key, keep it out of client-side code, and rotate it if exposure is suspected. <br>
Risk: Destructive migrations can cause data loss. <br>
Mitigation: Require dry-runs, backup migrations, and explicit confirmation before applying destructive production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guifav/supabase-ops) <br>
- [Deno HTTP server module](https://deno.land/std@0.177.0/http/server.ts) <br>
- [Supabase JavaScript client v2 module](https://esm.sh/@supabase/supabase-js@2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, TypeScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create migration files, update generated TypeScript types, and propose Supabase CLI commands when used by an agent.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
