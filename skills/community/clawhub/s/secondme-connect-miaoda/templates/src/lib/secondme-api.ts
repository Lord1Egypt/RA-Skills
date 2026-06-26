// SecondMe API 封装
// 让百度秒哒应用轻松调用SecondMe API

import { supabase } from './supabase';

const SECONDME_API_BASE = 'https://api.mindverse.com/gate/lab/api/secondme';

export class SecondMeAPI {
  private accessToken: string;

  constructor(accessToken: string) {
    this.accessToken = accessToken;
  }

  // 获取用户信息
  async getUserInfo() {
    const response = await fetch(`${SECONDME_API_BASE}/user/info`, {
      headers: { 'Authorization': `Bearer ${this.accessToken}` },
    });

    if (!response.ok) throw new Error('获取用户信息失败');
    
    const result = await response.json();
    return result.data;
  }

  // 流式聊天
  async *chat(message: string, sessionId?: string) {
    const response = await fetch(`${SECONDME_API_BASE}/chat/stream`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, sessionId }),
    });

    if (!response.ok) throw new Error('聊天失败');

    const reader = response.body?.getReader();
    if (!reader) throw new Error('无法读取响应');

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') return;

          try {
            const parsed = JSON.parse(data);
            if (parsed.choices?.[0]?.delta?.content) {
              yield {
                sessionId: parsed.sessionId,
                content: parsed.choices[0].delta.content,
              };
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }
  }

  // 搜索记忆
  async searchMemory(query: string, limit: number = 10) {
    const response = await fetch(`${SECONDME_API_BASE}/memory/search`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, limit }),
    });

    if (!response.ok) throw new Error('搜索记忆失败');
    
    const result = await response.json();
    return result.data;
  }

  // 添加笔记
  async addNote(content: string, tags?: string[]) {
    const response = await fetch(`${SECONDME_API_BASE}/note`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, tags }),
    });

    if (!response.ok) throw new Error('添加笔记失败');
    
    const result = await response.json();
    return result.data;
  }

  // 获取广场动态
  async getPlazaFeed(limit: number = 20, offset: number = 0) {
    const response = await fetch(
      `${SECONDME_API_BASE}/plaza/feed?limit=${limit}&offset=${offset}`,
      {
        headers: { 'Authorization': `Bearer ${this.accessToken}` },
      }
    );

    if (!response.ok) throw new Error('获取广场动态失败');
    
    const result = await response.json();
    return result.data;
  }

  // 发布帖子
  async createPost(content: string, visibility: string = 'public') {
    const response = await fetch(`${SECONDME_API_BASE}/plaza/post`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, visibility }),
    });

    if (!response.ok) throw new Error('发布帖子失败');
    
    const result = await response.json();
    return result.data;
  }

  // 语音合成
  async textToSpeech(text: string, voice: string = 'default') {
    const response = await fetch(`${SECONDME_API_BASE}/voice/tts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, voice }),
    });

    if (!response.ok) throw new Error('语音合成失败');
    
    return await response.blob();
  }
}

// 工具函数：从当前session获取SecondMe access token
export async function getSecondMeAccessToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.user) return null;

  const { data: profile } = await supabase
    .from('profiles')
    .select('secondme_access_token')
    .eq('id', session.user.id)
    .single();

  return profile?.secondme_access_token || null;
}

// 工具函数：创建SecondMe API实例
export async function createSecondMeAPI(): Promise<SecondMeAPI | null> {
  const accessToken = await getSecondMeAccessToken();
  if (!accessToken) return null;
  
  return new SecondMeAPI(accessToken);
}
