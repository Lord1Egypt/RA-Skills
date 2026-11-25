-- Policies that run a function or an auth lookup once per row (slow on big tables).
-- Run in the Supabase SQL editor, or: node skills/review/references/rls-speed.mjs <project-ref> [schema]
-- Every row returned is a finding. Fix: (select auth.uid()) instead of auth.uid(), and
--   col in (select <schema>.allowed_ids())  instead of  has_access(col).
select schemaname, tablename, policyname, cmd,
       coalesce(qual, '') || ' ' || coalesce(with_check, '') as condition
from pg_policies
where schemaname not in ('auth', 'storage', 'realtime', 'supabase_functions', 'cron', 'vault', 'net', 'extensions')
  and (
    -- auth.uid() / auth.jwt() / auth.role() / auth.email() not inside "( SELECT"
    regexp_replace(coalesce(qual, '') || ' ' || coalesce(with_check, ''), '\(\s*select\s+auth\.(uid|jwt|role|email)\(\)', '', 'gi')
      ~* 'auth\.(uid|jwt|role|email)\(\)'
    -- a function called with a column, not inside a subselect:  has_access(library_id)
    or regexp_replace(coalesce(qual, '') || ' ' || coalesce(with_check, ''), '\(\s*select\s+[a-z_.]+\([^)]*\)', '', 'gi')
      ~* '[a-z_]+\.[a-z_]+\(\s*[a-z_]+\s*[,)]'
  )
order by 1, 2, 3;
