create table todos (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users not null default auth.uid(),
  title text not null
);

alter table todos enable row level security;

create policy "read own todos" on todos for select using (auth.uid() = user_id);
create policy "insert own todos" on todos for insert with check (auth.uid() = user_id);
