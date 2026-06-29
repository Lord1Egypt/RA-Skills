-- Incremental self-serve SaaS tables for Sage Router hosted accounts.
-- Secrets are not stored here. Generated API keys must be stored only as hashes.

create table if not exists public.sage_router_customers (
  id text primary key,
  user_id text not null unique,
  email text,
  plan text not null default 'free',
  status text not null default 'inactive',
  stripe_customer_id text,
  stripe_subscription_id text,
  created_at_epoch bigint not null,
  updated_at_epoch bigint not null
);

create index if not exists sage_router_customers_stripe_customer_idx
  on public.sage_router_customers (stripe_customer_id)
  where stripe_customer_id is not null;

create table if not exists public.sage_router_api_keys (
  id text primary key,
  customer_id text not null references public.sage_router_customers(id) on delete cascade,
  user_id text not null,
  name text not null default 'Default',
  prefix text not null,
  api_key_hash text not null unique,
  status text not null default 'active',
  plan text,
  created_at_epoch bigint not null,
  last_used_at_epoch bigint,
  revoked_at_epoch bigint
);

create index if not exists sage_router_api_keys_customer_idx
  on public.sage_router_api_keys (customer_id, created_at_epoch desc);

create table if not exists public.sage_router_payment_intents (
  id text primary key,
  kind text not null,
  customer_id text references public.sage_router_customers(id) on delete set null,
  user_id text,
  status text not null default 'pending',
  asset text,
  network text,
  amount text,
  address text,
  metadata jsonb not null default '{}'::jsonb,
  event_type text,
  event_id text,
  created_at_epoch bigint not null,
  updated_at_epoch bigint not null
);

create unique index if not exists sage_router_payment_intents_stripe_event_idx
  on public.sage_router_payment_intents (event_id)
  where kind = 'stripe_webhook' and event_id is not null;

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

create table if not exists public.sage_router_operator_audit_events (
  id text primary key,
  customer_id text not null references public.sage_router_customers(id) on delete cascade,
  actor text not null default 'operator',
  action text not null,
  reason_code text not null default 'operator_review',
  status_before text,
  status_after text,
  revoked_api_keys_count integer not null default 0,
  created_at_epoch bigint not null
);

create index if not exists sage_router_operator_audit_events_customer_idx
  on public.sage_router_operator_audit_events (customer_id, created_at_epoch desc);

alter table public.sage_router_customers enable row level security;
alter table public.sage_router_api_keys enable row level security;
alter table public.sage_router_payment_intents enable row level security;
alter table public.sage_router_usage_counters enable row level security;
alter table public.sage_router_operator_audit_events enable row level security;

do $$
begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='sage_router_customers' and policyname='service role manages sage router customers') then
    create policy "service role manages sage router customers" on public.sage_router_customers for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
  end if;
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='sage_router_api_keys' and policyname='service role manages sage router api keys') then
    create policy "service role manages sage router api keys" on public.sage_router_api_keys for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
  end if;
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='sage_router_payment_intents' and policyname='service role manages sage router payment intents') then
    create policy "service role manages sage router payment intents" on public.sage_router_payment_intents for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
  end if;
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='sage_router_usage_counters' and policyname='service role manages sage router usage counters') then
    create policy "service role manages sage router usage counters" on public.sage_router_usage_counters for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
  end if;
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='sage_router_operator_audit_events' and policyname='service role manages sage router operator audit events') then
    create policy "service role manages sage router operator audit events" on public.sage_router_operator_audit_events for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
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
