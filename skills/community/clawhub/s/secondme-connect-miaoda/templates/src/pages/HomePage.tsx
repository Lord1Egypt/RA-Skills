// 首页 - 展示如何使用SecondMe API
import { useSecondMe } from '../hooks/useSecondMe';
import { LoginButton, LogoutButton } from '../components/LoginButton';
import { useState } from 'react';
import './HomePage.css';

export function HomePage() {
  const { 
    profile, 
    loading, 
    isLoggedIn, 
    chat, 
    searchMemory, 
    addNote 
  } = useSecondMe();

  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [memoryQuery, setMemoryQuery] = useState('');
  const [noteContent, setNoteContent] = useState('');

  if (loading) return <div className="loading">加载中...</div>;

  if (!isLoggedIn) {
    return (
      <div className="home-page">
        <h1>欢迎使用 SecondMe</h1>
        <p>登录后即可使用SecondMe API</p>
        <LoginButton className="primary-btn">使用 SecondMe 登录</LoginButton>
      </div>
    );
  }

  const handleChat = async () => {
    if (!chatMessage.trim()) return;
    try {
      const response = await chat(chatMessage);
      setChatResponse(response);
      setChatMessage('');
    } catch (err: any) {
      alert('聊天失败: ' + err.message);
    }
  };

  const handleSearchMemory = async () => {
    if (!memoryQuery.trim()) return;
    try {
      const memories = await searchMemory(memoryQuery);
      alert(`找到 ${memories.length} 条记忆`);
      setMemoryQuery('');
    } catch (err: any) {
      alert('搜索失败: ' + err.message);
    }
  };

  const handleAddNote = async () => {
    if (!noteContent.trim()) return;
    try {
      await addNote(noteContent);
      alert('笔记已保存');
      setNoteContent('');
    } catch (err: any) {
      alert('保存失败: ' + err.message);
    }
  };

  return (
    <div className="home-page">
      <div className="user-card">
        {profile?.avatar_url && (
          <img src={profile.avatar_url} alt="avatar" className="avatar" />
        )}
        <h2>{profile?.name}</h2>
        <p>{profile?.email}</p>
        <LogoutButton />
      </div>

      <div className="api-demo">
        <h3>API 示例</h3>

        {/* 聊天 */}
        <div className="demo-section">
          <h4>💬 聊天</h4>
          <div className="input-group">
            <input
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="输入消息..."
            />
            <button onClick={handleChat}>发送</button>
          </div>
          {chatResponse && (
            <div className="response">
              <strong>回复:</strong> {chatResponse}
            </div>
          )}
        </div>

        {/* 搜索记忆 */}
        <div className="demo-section">
          <h4>🔍 搜索记忆</h4>
          <div className="input-group">
            <input
              value={memoryQuery}
              onChange={(e) => setMemoryQuery(e.target.value)}
              placeholder="搜索关键词..."
            />
            <button onClick={handleSearchMemory}>搜索</button>
          </div>
        </div>

        {/* 添加笔记 */}
        <div className="demo-section">
          <h4>📝 添加笔记</h4>
          <div className="input-group">
            <input
              value={noteContent}
              onChange={(e) => setNoteContent(e.target.value)}
              placeholder="笔记内容..."
            />
            <button onClick={handleAddNote}>保存</button>
          </div>
        </div>
      </div>
    </div>
  );
}
