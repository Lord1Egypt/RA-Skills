create table if not exists public.sage_router_model_modalities (
  key text primary key,
  provider text not null,
  model text not null,
  modalities text[] not null default '{}',
  count integer not null default 0,
  first_seen_epoch_ms bigint not null,
  last_seen_epoch_ms bigint not null,
  updated_at_epoch_ms bigint not null
);

create index if not exists sage_router_model_modalities_provider_idx
  on public.sage_router_model_modalities(provider);

create index if not exists sage_router_model_modalities_last_seen_idx
  on public.sage_router_model_modalities(last_seen_epoch_ms desc);

alter table public.sage_router_model_modalities enable row level security;

do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'sage_router_model_modalities'
      and policyname = 'service role manages sage router model modalities'
  ) then
    create policy "service role manages sage router model modalities"
      on public.sage_router_model_modalities
      for all
      using (auth.role() = 'service_role')
      with check (auth.role() = 'service_role');
  end if;
end $$;

create or replace function public.sage_router_record_model_modalities(
  provider_name text,
  model_name text,
  modalities_in text[],
  seen_at_epoch_ms bigint default null
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  clean_modalities text[];
  modality_key text;
  seen_ms bigint;
begin
  clean_modalities := array(
    select distinct lower(trim(m))
    from unnest(coalesce(modalities_in, '{}')) as m
    where lower(trim(m)) in ('text', 'image', 'audio', 'video', 'document')
    order by lower(trim(m))
  );

  if provider_name is null or trim(provider_name) = '' or model_name is null or trim(model_name) = '' or array_length(clean_modalities, 1) is null then
    return;
  end if;

  modality_key := trim(provider_name) || '/' || trim(model_name);
  seen_ms := coalesce(seen_at_epoch_ms, floor(extract(epoch from now()) * 1000)::bigint);

  insert into public.sage_router_model_modalities (
    key,
    provider,
    model,
    modalities,
    count,
    first_seen_epoch_ms,
    last_seen_epoch_ms,
    updated_at_epoch_ms
  )
  values (
    modality_key,
    trim(provider_name),
    trim(model_name),
    clean_modalities,
    1,
    seen_ms,
    seen_ms,
    seen_ms
  )
  on conflict (key) do update set
    modalities = (
      select array_agg(distinct modality order by modality)
      from unnest(public.sage_router_model_modalities.modalities || excluded.modalities) as modality
    ),
    count = public.sage_router_model_modalities.count + 1,
    first_seen_epoch_ms = least(public.sage_router_model_modalities.first_seen_epoch_ms, excluded.first_seen_epoch_ms),
    last_seen_epoch_ms = greatest(public.sage_router_model_modalities.last_seen_epoch_ms, excluded.last_seen_epoch_ms),
    updated_at_epoch_ms = excluded.updated_at_epoch_ms;
end;
$$;

revoke all on function public.sage_router_record_model_modalities(text, text, text[], bigint) from public;
revoke all on function public.sage_router_record_model_modalities(text, text, text[], bigint) from anon;
revoke all on function public.sage_router_record_model_modalities(text, text, text[], bigint) from authenticated;
grant execute on function public.sage_router_record_model_modalities(text, text, text[], bigint) to service_role;
