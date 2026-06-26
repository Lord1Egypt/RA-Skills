// SecondMe React Hook
// 让百度秒哒应用轻松使用SecondMe功能

import { useState, useEffect, useCallback } from 'react';
import { supabase } from '../lib/supabase';
import { SecondMeAPI, createSecondMeAPI } from '../lib/secondme-api';

export function useSecondMe() {
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [api, setApi] = useState<SecondMeAPI | null>(null);

  useEffect(() => {
    checkUser();

    const { data: authListener } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (event === 'SIGNED_IN' && session) {
          await fetchProfile(session.user.id);
        } else if (event === 'SIGNED_OUT') {
          setUser(null);
          setProfile(null);
          setApi(null);
        }
      }
    );

    return () => {
      authListener?.subscription.unsubscribe();
    };
  }, []);

  const checkUser = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.user) {
        setUser(session.user);
        await fetchProfile(session.user.id);
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchProfile = async (userId: string) => {
    const { data } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single();

    setProfile(data);

    if (data?.secondme_access_token) {
      setApi(new SecondMeAPI(data.secondme_access_token));
    }
  };

  const login = useCallback(() => {
    const state = Math.random().toString(36).substring(2, 15) +
                  Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem('oauth_state', state);

    const authUrl = new URL('https://go.second-me.cn/oauth/');
    authUrl.searchParams.append('client_id', import.meta.env.VITE_SECONDME_CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', import.meta.env.VITE_SECONDME_REDIRECT_URI);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('state', state);

    window.location.href = authUrl.toString();
  }, []);

  const logout = useCallback(async () => {
    await supabase.auth.signOut();
    setUser(null);
    setProfile(null);
    setApi(null);
  }, []);

  // 封装常用API
  const chat = useCallback(async (message: string) => {
    if (!api) throw new Error('未登录');
    
    const chunks: string[] = [];
    for await (const chunk of api.chat(message)) {
      chunks.push(chunk.content);
    }
    return chunks.join('');
  }, [api]);

  const searchMemory = useCallback(async (query: string) => {
    if (!api) throw new Error('未登录');
    return await api.searchMemory(query);
  }, [api]);

  const addNote = useCallback(async (content: string) => {
    if (!api) throw new Error('未登录');
    return await api.addNote(content);
  }, [api]);

  const getPlazaFeed = useCallback(async (limit?: number) => {
    if (!api) throw new Error('未登录');
    return await api.getPlazaFeed(limit);
  }, [api]);

  return {
    user,
    profile,
    loading,
    isLoggedIn: !!user,
    login,
    logout,
    api,
    // 便捷方法
    chat,
    searchMemory,
    addNote,
    getPlazaFeed,
  };
}
