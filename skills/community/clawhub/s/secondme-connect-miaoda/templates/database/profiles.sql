-- SecondMe OAuth 集成 - 数据库初始化
-- 在 Supabase SQL Editor 中执行

-- 创建 profiles 表
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text UNIQUE NOT NULL,
  name text,
  avatar_url text,
  -- ⚠️ 敏感字段：存储 SecondMe access_token
  -- 用户只能通过 RLS 策略访问自己的 token
  secondme_access_token text,
  secondme_refresh_token text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- 启用RLS（行级安全）
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- RLS 策略：用户只能访问自己的 profile
-- 这确保了用户只能读取自己的 secondme_access_token
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE USING (auth.uid() = id);

-- ⚠️ 安全说明：
-- 1. 用户可以读取自己的 access_token（通过 RLS 保护）
-- 2. 前端代码使用此 token 调用 SecondMe API
-- 3. 确保定期验证 RLS 策略是否正确
-- 4. 如果不需要前端直接访问 token，可以考虑创建 Edge Function 作为 API 代理

-- 自动更新updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);

-- 验证 RLS 策略（可选）
-- 以不同用户身份测试查询，确保只能看到自己的数据
-- SELECT * FROM profiles; -- 应该只返回当前用户的数据

-- 完成
SELECT '✅ profiles表创建完成！RLS 策略已启用。' as status;
SELECT '⚠️ 重要：请确保定期验证 RLS 策略是否正确。' as reminder;
