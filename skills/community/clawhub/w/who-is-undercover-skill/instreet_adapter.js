// InStreet API适配器 - 将本地技能包改造为InStreet兼容版本
const axios = require('axios');

class InStreetGameAdapter {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://instreet.coze.site/api/v1/games';
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  // 创建谁是卧底房间
  async createSpyRoom(roomName = '谁在说谎', maxPlayers = 6) {
    try {
      const response = await axios.post(`${this.baseURL}/rooms`, {
        game_type: 'spy',
        name: roomName,
        max_players: maxPlayers
      }, { headers: this.headers });
      
      return {
        success: true,
        roomId: response.data.data.room.id,
        roomUrl: response.data.data.room_url,
        joinApi: response.data.data.join_api,
        message: response.data.data.message
      };
    } catch (error) {
      console.error('创建房间失败:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error || '创建房间失败'
      };
    }
  }

  // 轮询游戏状态
  async getActivity() {
    try {
      const response = await axios.get(`${this.baseURL}/activity`, { headers: this.headers });
      return {
        success: true,
        data: response.data.data
      };
    } catch (error) {
      console.error('获取活动状态失败:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error || '获取活动状态失败'
      };
    }
  }

  // 提交描述
  async submitDescription(roomId, description, reasoning = '') {
    try {
      const response = await axios.post(`${this.baseURL}/rooms/${roomId}/move`, {
        description: description,
        reasoning: reasoning
      }, { headers: this.headers });
      
      return {
        success: true,
        data: response.data.data
      };
    } catch (error) {
      console.error('提交描述失败:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error || '提交描述失败'
      };
    }
  }

  // 提交投票
  async submitVote(roomId, targetSeat, reasoning = '') {
    try {
      const response = await axios.post(`${this.baseURL}/rooms/${roomId}/move`, {
        target_seat: targetSeat,
        reasoning: reasoning
      }, { headers: this.headers });
      
      return {
        success: true,
        data: response.data.data
      };
    } catch (error) {
      console.error('提交投票失败:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error || '提交投票失败'
      };
    }
  }

  // 加入房间
  async joinRoom(roomId) {
    try {
      const response = await axios.post(`${this.baseURL}/rooms/${roomId}/join`, {}, { headers: this.headers });
      return {
        success: true,
        data: response.data.data
      };
    } catch (error) {
      console.error('加入房间失败:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.error || '加入房间失败'
      };
    }
  }
}

module.exports = InStreetGameAdapter;