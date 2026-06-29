-- Anonymous marketing CTA intent events for pre-signup conversion tracking.
-- Do not store emails, prompt bodies, API keys, provider credentials, or raw
-- workflow text here. Pages Functions insert small allowlisted metadata only.

create table if not exists public.sage_router_funnel_events (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  event text not null check (event ~ '^[a-z0-9_:-]{1,80}$'),
  plan text check (
    plan is null
    or plan in ('lite', 'pro', 'max', 'trial', 'manual')
  ),
  source_page text,
  target text,
  metadata jsonb not null default '{}'::jsonb
);

create index if not exists sage_router_funnel_events_created_idx
  on public.sage_router_funnel_events (created_at desc);

create index if not exists sage_router_funnel_events_event_idx
  on public.sage_router_funnel_events (event, created_at desc);

create index if not exists sage_router_funnel_events_plan_idx
  on public.sage_router_funnel_events (plan, created_at desc)
  where plan is not null;

alter table public.sage_router_funnel_events enable row level security;

do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'sage_router_funnel_events'
      and policyname = 'service role manages sage router funnel events'
  ) then
    create policy "service role manages sage router funnel events"
      on public.sage_router_funnel_events
      for all
      using (auth.role() = 'service_role')
      with check (auth.role() = 'service_role');
  end if;
end $$;
