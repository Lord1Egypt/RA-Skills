// 登录按钮组件
import { supabase } from '../lib/supabase';
import './LoginButton.css';

interface Props {
  className?: string;
  children?: React.ReactNode;
}

export function LoginButton({ className = '', children }: Props) {
  const handleLogin = () => {
    // 生成state防CSRF
    const state = Math.random().toString(36).substring(2, 15) +
                  Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem('oauth_state', state);

    // 跳转授权页
    const authUrl = new URL('https://go.second-me.cn/oauth/');
    authUrl.searchParams.append('client_id', import.meta.env.VITE_SECONDME_CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', import.meta.env.VITE_SECONDME_REDIRECT_URI);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('state', state);

    window.location.href = authUrl.toString();
  };

  return (
    <button onClick={handleLogin} className={`login-btn ${className}`}>
      {children || 'Login with SecondMe'}
    </button>
  );
}

export function LogoutButton({ className = '' }: { className?: string }) {
  const handleLogout = async () => {
    await supabase.auth.signOut();
    window.location.reload();
  };

  return (
    <button onClick={handleLogout} className={`logout-btn ${className}`}>
      Logout
    </button>
  );
}
