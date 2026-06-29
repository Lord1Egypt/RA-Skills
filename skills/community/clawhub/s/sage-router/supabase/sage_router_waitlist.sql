create table if not exists public.sage_router_waitlist (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  email text not null,
  company text,
  source_page text not null default 'https://sagerouter.dev',
  metadata jsonb not null default '{}'::jsonb,
  unique (email)
);

alter table public.sage_router_waitlist enable row level security;

do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'sage_router_waitlist'
      and policyname = 'service role manages sage router waitlist'
  ) then
    create policy "service role manages sage router waitlist"
      on public.sage_router_waitlist
      for all
      using (auth.role() = 'service_role')
      with check (auth.role() = 'service_role');
  end if;
end $$;
