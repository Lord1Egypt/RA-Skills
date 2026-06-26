// OAuth回调页面
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import './AuthCallbackPage.css';

export function AuthCallbackPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    handleCallback();
  }, []);

  const handleCallback = async () => {
    try {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      const state = params.get('state');
      const errorParam = params.get('error');

      if (errorParam) {
        setError('授权失败或被取消');
        setLoading(false);
        return;
      }

      if (!code || !state) {
        setError('缺少必要参数');
        setLoading(false);
        return;
      }

      // 验证state
      const savedState = sessionStorage.getItem('oauth_state');
      if (state !== savedState) {
        setError('安全验证失败');
        setLoading(false);
        return;
      }
      sessionStorage.removeItem('oauth_state');

      // 调用Edge Function
      const { data, error: fnError } = await supabase.functions.invoke(
        'secondme-oauth-callback',
        { body: { code } }
      );

      if (fnError || !data?.hashed_token) {
        setError('登录失败');
        setLoading(false);
        return;
      }

      // 换取Session
      const { error: otpError } = await supabase.auth.verifyOtp({
        token_hash: data.hashed_token,
        type: 'email',
      });

      if (otpError) {
        setError('会话创建失败');
        setLoading(false);
        return;
      }

      // 登录成功
      navigate('/');
    } catch (err) {
      setError('登录失败');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="auth-callback">
        <div className="spinner"></div>
        <p>正在登录...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="auth-callback">
        <h2>登录失败</h2>
        <p>{error}</p>
        <button onClick={() => navigate('/')}>返回首页</button>
      </div>
    );
  }

  return null;
}
