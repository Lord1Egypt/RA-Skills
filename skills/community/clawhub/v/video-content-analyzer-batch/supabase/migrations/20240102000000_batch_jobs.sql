-- Batch processing support

create table batch_jobs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  user_id uuid references profiles(id) not null,
  input_directory text not null,
  status text default 'pending' check (status in ('pending', 'running', 'completed', 'partial', 'failed')),
  total_videos integer not null default 0,
  processed_videos integer not null default 0,
  failed_videos integer not null default 0,
  feishu_space_id text not null,
  category_mapping jsonb default '{}'::jsonb,
  results jsonb default '[]'::jsonb,
  error_log text[]
);

alter table batch_jobs enable row level security;
create policy "Users can view their own batch jobs" on batch_jobs
  for select using ((select auth.uid()) = user_id);
create policy "Users can create their own batch jobs" on batch_jobs
  for insert with check ((select auth.uid()) = user_id);
create policy "Users can update their own batch jobs" on batch_jobs
  for update using ((select auth.uid()) = user_id);

-- Add wiki_url column to video_assets for per-video wiki link
alter table video_assets add column if not exists wiki_url text;