# Setup Guide

## 1. Get Supabase Credentials

1. Go to your Supabase Dashboard (https://supabase.com/dashboard)
2. Select your project
3. Go to Settings → API
4. Copy:
   - **Project ID**: From the project URL (e.g., `abcdefgh12345678` from `https://abcdefgh12345678.supabase.co`)
   - **anon public**: The public API key

## 2. Configure the Skill

1. Create file `references/.env`
2. Fill in your credentials:
   - `SUPABASE_PROJECT_ID=your-project-id`
   - `SUPABASE_ANON_KEY=your-anon-key`

## 3. Test Connection

```bash
python scripts/query.py "users" --select "*" --limit 1
```

Expected output:
```json
{"success": true, "table": "users", "rows": [...], "row_count": 1, "truncated": false, "max_limit": 200}
```

## Security Notes

- The `.env` file is gitignored by default
- Never commit credentials to version control
- The anon key respects your Supabase RLS policies
