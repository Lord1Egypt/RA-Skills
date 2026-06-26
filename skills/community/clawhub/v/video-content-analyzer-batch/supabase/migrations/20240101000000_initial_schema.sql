-- Supabase starter schema for media asset management
-- Source: https://supabase.com/docs/guides/getting-started/tutorials/with-solidjs?database-method=sql&queryGroups=database-method
-- Adapted for video/media processing workflow

-- Create a table for public profiles
create table profiles (
  id uuid references auth.users not null primary key,
  updated_at timestamp with time zone,
  username text unique,
  full_name text,
  avatar_url text,
  website text,

  constraint username_length check (char_length(username) >= 3)
);
-- Set up Row Level Security (RLS)
alter table profiles enable row level security;

create policy "Public profiles are viewable by everyone." on profiles
  for select using (true);

create policy "Users can insert their own profile." on profiles
  for insert with check ((select auth.uid()) = id);

create policy "Users can update own profile." on profiles
  for update using ((select auth.uid()) = id);

-- Trigger to create profile when user signs up
create function public.handle_new_user()
returns trigger
set search_path = ''
as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  return new;
end;
$$ language plpgsql security definer;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Create table for video assets
create table video_assets (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  user_id uuid references profiles(id) not null,
  original_filename text not null,
  storage_path text not null,
  duration_seconds numeric,
  file_size_bytes bigint,
  status text default 'uploaded' check (status in ('uploaded', 'processing', 'processed', 'failed')),
  metadata jsonb default '{}'::jsonb
);

-- Create table for extracted frames
create table video_frames (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  video_id uuid references video_assets(id) on delete cascade not null,
  frame_number integer not null,
  timestamp_seconds numeric not null,
  storage_path text not null,
  width integer,
  height integer,
  ocr_text text,
  content_tags text[] default '{}'::text[]
);

-- Create table for search results
create table search_results (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  frame_id uuid references video_frames(id) on delete cascade not null,
  query text not null,
  search_engine text not null,
  result_url text not null,
  title text,
  snippet text,
  relevance_score numeric
);

-- Create table for wiki pages
create table wiki_pages (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  updated_at timestamp with time zone default now() not null,
  user_id uuid references profiles(id) not null,
  title text not null,
  content text not null,
  source_video_id uuid references video_assets(id),
  source_frame_ids uuid[] default '{}'::uuid[],
  citations jsonb default '[]'::jsonb
);

-- Set up storage buckets
insert into storage.buckets (id, name, public) values
  ('video-uploads', 'Video uploads', false),
  ('extracted-frames', 'Extracted video frames', true);

-- Storage access policies
create policy "Users can upload their own videos" on storage.objects
  for insert with check (
    bucket_id = 'video-uploads' and
    (select auth.uid())::text = (storage.foldername(name))[1]
  );

create policy "Users can view their own videos" on storage.objects
  for select using (
    bucket_id = 'video-uploads' and
    (select auth.uid())::text = (storage.foldername(name))[1]
  );

create policy "Public can view extracted frames" on storage.objects
  for select using (bucket_id = 'extracted-frames');

-- RLS policies for video assets
alter table video_assets enable row level security;
create policy "Users can view their own videos" on video_assets
  for select using ((select auth.uid()) = user_id);
create policy "Users can upload their own videos" on video_assets
  for insert with check ((select auth.uid()) = user_id);
create policy "Users can update their own videos" on video_assets
  for update using ((select auth.uid()) = user_id);

-- RLS policies for frames
alter table video_frames enable row level security;
create policy "Users can view frames from their videos" on video_frames
  for select using (
    exists (
      select 1 from video_assets va
      where va.id = video_id and va.user_id = (select auth.uid())
    )
  );

-- RLS policies for search results
alter table search_results enable row level security;
create policy "Users can view their own search results" on search_results
  for select using (
    exists (
      select 1 from video_frames vf
      join video_assets va on va.id = vf.video_id
      where vf.id = frame_id and va.user_id = (select auth.uid())
    )
  );

-- RLS policies for wiki pages
alter table wiki_pages enable row level security;
create policy "Users can view their own wiki pages" on wiki_pages
  for select using ((select auth.uid()) = user_id);
create policy "Users can create their own wiki pages" on wiki_pages
  for insert with check ((select auth.uid()) = user_id);
create policy "Users can update their own wiki pages" on wiki_pages
  for update using ((select auth.uid()) = user_id);