// SecondMe OAuth2 回调 Edge Function
import { createClient } from 'jsr:@supabase/supabase-js@2';

// 安全的CORS配置 - 只允许特定来源
const getAllowedOrigins = (): string[] => {
  const origins = Deno.env.get('ALLOWED_ORIGINS');
  if (origins) {
    return origins.split(',').map(o => o.trim()).filter(Boolean);
  }
  
  // 如果没有配置，尝试从环境变量推断
  const supabaseUrl = Deno.env.get('SUPABASE_URL');
  if (supabaseUrl) {
    // 从SUPABASE_URL推断允许的域名
    const url = new URL(supabaseUrl);
    return [`https://${url.hostname}`];
  }
  
  // 默认：警告并返回空数组（拒绝所有跨域请求）
  console.warn('⚠️ ALLOWED_ORIGINS not configured. CORS requests will be denied.');
  return [];
};

const getCorsHeaders = (request: Request): Record<string, string> => {
  const origin = request.headers.get('origin') || '';
  const allowedOrigins = getAllowedOrigins();
  
  // 安全逻辑：只允许配置列表中的 origin
  // 如果请求的 origin 不在允许列表中，返回空字符串（拒绝跨域请求）
  const allowOrigin = allowedOrigins.includes(origin) ? origin : '';
  
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };
};

Deno.serve(async (req) => {
  // 处理OPTIONS预检请求
  if (req.method === 'OPTIONS') {
    const corsHeaders = getCorsHeaders(req);
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const corsHeaders = getCorsHeaders(req);
    
    const { code } = await req.json();
    if (!code) throw new Error('缺少authorization code');

    // 读取环境变量
    const clientId = Deno.env.get('SECONDME_CLIENT_ID');
    const clientSecret = Deno.env.get('SECONDME_CLIENT_SECRET');
    const redirectUri = Deno.env.get('SECONDME_REDIRECT_URI');

    if (!clientId || !clientSecret || !redirectUri) {
      throw new Error('服务器配置错误');
    }

    // 1. Code换AccessToken
    const tokenParams = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      client_secret: clientSecret,
    });

    const tokenRes = await fetch('https://api.mindverse.com/gate/lab/api/oauth/token/code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: tokenParams.toString(),
    });

    if (!tokenRes.ok) throw new Error('获取访问令牌失败');
    
    const tokenData = (await tokenRes.json()).data;
    const { accessToken, refreshToken } = tokenData;

    // 2. 获取用户信息
    const userRes = await fetch('https://api.mindverse.com/gate/lab/api/secondme/user/info', {
      headers: { 'Authorization': `Bearer ${accessToken}` },
    });

    if (!userRes.ok) throw new Error('获取用户信息失败');
    
    const userInfo = (await userRes.json()).data;
    const { userId, name, email, avatar } = userInfo;

    // 处理手机号用户
    const isValidEmail = (e: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
    const supabaseEmail = isValidEmail(email) ? email : `user_${userId}@secondme.local`;

    // 3. 创建/更新Supabase用户
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    const { data: existingUsers } = await supabase.auth.admin.listUsers();
    const userExists = existingUsers?.users.find(u => u.email === supabaseEmail);

    let supabaseUserId: string;

    if (!userExists) {
      const { data: newUser, error } = await supabase.auth.admin.createUser({
        email: supabaseEmail,
        email_confirm: true,
        user_metadata: { name, avatar_url: avatar },
      });

      if (error || !newUser.user) throw new Error('创建用户失败');
      
      supabaseUserId = newUser.user.id;
      await supabase.from('profiles').insert({
        id: supabaseUserId,
        email: supabaseEmail,
        name,
        avatar_url: avatar,
        secondme_access_token: accessToken,
        secondme_refresh_token: refreshToken,
      });
    } else {
      supabaseUserId = userExists.id;
      await supabase.from('profiles').update({
        name,
        avatar_url: avatar,
        secondme_access_token: accessToken,
        secondme_refresh_token: refreshToken,
      }).eq('id', supabaseUserId);
    }

    // 4. 生成Magic Link
    const { data: linkData, error: linkError } = await supabase.auth.admin.generateLink({
      type: 'magiclink',
      email: supabaseEmail,
    });

    if (linkError || !linkData?.properties?.hashed_token) {
      throw new Error('生成登录令牌失败');
    }

    // 5. 返回结果（⚠️ 不返回access_token到前端，避免暴露）
    // access_token已安全存储在数据库中，前端需要时可通过profile获取
    console.log('✅ OAuth流程完成，返回hashed_token');
    
    return new Response(
      JSON.stringify({
        hashed_token: linkData.properties.hashed_token,
        user: { name, avatar, email: supabaseEmail },
        // ⚠️ 不返回access_token - 它已安全存储在数据库中
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('❌ OAuth处理错误:', error);
    const corsHeaders = getCorsHeaders(req);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
