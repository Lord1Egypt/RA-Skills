create table notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  body text not null,
  created_at timestamptz default now()
);

alter table notes disable row level security;
