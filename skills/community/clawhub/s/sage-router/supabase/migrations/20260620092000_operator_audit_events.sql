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

alter table public.sage_router_operator_audit_events enable row level security;

do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'sage_router_operator_audit_events'
      and policyname = 'service role manages sage router operator audit events'
  ) then
    create policy "service role manages sage router operator audit events"
      on public.sage_router_operator_audit_events
      for all
      using (auth.role() = 'service_role')
      with check (auth.role() = 'service_role');
  end if;
end $$;
