-- Durable monthly usage counters for public Sage Router SaaS API keys.
-- Apply before enabling SAGE_ROUTER_EDGE_QUOTA_ENABLED=1 on the public edge.

create table if not exists public.sage_router_usage_counters (
  id text primary key,
  customer_id text not null references public.sage_router_customers(id) on delete cascade,
  user_id text,
  plan text,
  period text not null,
  requests bigint not null default 0,
  created_at_epoch bigint not null,
  updated_at_epoch bigint not null
);

create unique index if not exists sage_router_usage_counters_customer_period_idx
  on public.sage_router_usage_counters (customer_id, period);

alter table public.sage_router_usage_counters enable row level security;

do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'sage_router_usage_counters'
      and policyname = 'service role manages sage router usage counters'
  ) then
    create policy "service role manages sage router usage counters"
      on public.sage_router_usage_counters
      for all
      using (auth.role() = 'service_role')
      with check (auth.role() = 'service_role');
  end if;
end $$;

create or replace function public.sage_router_increment_usage(
  p_customer_id text,
  p_user_id text,
  p_plan text,
  p_period text,
  p_increment bigint,
  p_quota bigint
)
returns table (
  customer_id text,
  period text,
  requests bigint,
  quota bigint,
  remaining bigint,
  allowed boolean
)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_now bigint := extract(epoch from now())::bigint;
  v_increment bigint := greatest(coalesce(p_increment, 1), 1);
  v_requests bigint;
begin
  if auth.role() <> 'service_role' then
    raise exception 'service role required';
  end if;

  insert into public.sage_router_usage_counters (
    id,
    customer_id,
    user_id,
    plan,
    period,
    requests,
    created_at_epoch,
    updated_at_epoch
  )
  values (
    p_customer_id || ':' || p_period,
    p_customer_id,
    nullif(p_user_id, ''),
    nullif(p_plan, ''),
    p_period,
    v_increment,
    v_now,
    v_now
  )
  on conflict (id) do update
    set requests = public.sage_router_usage_counters.requests + v_increment,
        user_id = coalesce(nullif(p_user_id, ''), public.sage_router_usage_counters.user_id),
        plan = coalesce(nullif(p_plan, ''), public.sage_router_usage_counters.plan),
        updated_at_epoch = v_now
  returning public.sage_router_usage_counters.requests into v_requests;

  return query
    select
      p_customer_id,
      p_period,
      v_requests,
      p_quota,
      greatest(p_quota - v_requests, 0),
      v_requests <= p_quota;
end;
$$;

revoke all on function public.sage_router_increment_usage(text, text, text, text, bigint, bigint) from public;
revoke all on function public.sage_router_increment_usage(text, text, text, text, bigint, bigint) from anon;
revoke all on function public.sage_router_increment_usage(text, text, text, text, bigint, bigint) from authenticated;
grant execute on function public.sage_router_increment_usage(text, text, text, text, bigint, bigint) to service_role;
