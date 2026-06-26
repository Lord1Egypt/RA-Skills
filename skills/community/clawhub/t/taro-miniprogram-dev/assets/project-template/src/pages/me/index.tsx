import { Component } from 'react'
import { View, Text, Navigator } from '@tarojs/components'
import './index.scss'

// TODO: 替换为真实数据
const mockUser = { name: '小熊同学', gender: 'female', circleName: '熊熊一家', coin: 360, taskCount: 12, joinDays: 30 }

const menuItems = [
  { id: 'wallet', title: '金币钱包', url: '/pages/coin/wallet/index', emoji: '💰' },
  { id: 'tasks', title: '我的任务', url: '/pages/task/list/index', emoji: '📋' },
  { id: 'circle', title: '我的圈子', url: '/pages/home/index', emoji: '🐻' },
  { id: 'settings', title: '退出登录', emoji: '⚙️' },
]

export default class MeIndex extends Component {
  state = { userInfo: mockUser }

  componentDidMount() {
    // TODO: const fresh = await getUserInfo(); this.setState({ userInfo: fresh })
    // const cached = wx.getStorageSync('userInfo')
  }

  handleLogout = () => {
    wx.showModal({ title: '提示', content: '确定要退出登录吗？', success: res => {
      if (res.confirm) { wx.clearStorageSync(); wx.redirectTo({ url: '/pages/auth/index' }) }
    }})
  }

  render() {
    const { userInfo } = this.state
    const user = userInfo || { name: '未登录', gender: 'female', circleName: '未加入', coin: 0, taskCount: 0, joinDays: 0 }
    return (
      <View className="me-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="card user-card">
          <View className="user-info">
            <View className="avatar">{user.gender === 'female' ? '🐻' : '🐻'}</View>
            <View className="user-detail"><Text className="user-name">{user.name}</Text><Text className="user-circle">圈子：{user.circleName}</Text></View>
          </View>
          <View className="user-stats">
            <View className="stat-item"><Text className="stat-value">{user.coin}</Text><Text className="stat-label">金币</Text></View>
            <View className="stat-divider" />
            <View className="stat-item"><Text className="stat-value">{user.taskCount}</Text><Text className="stat-label">完成任务</Text></View>
            <View className="stat-divider" />
            <View className="stat-item"><Text className="stat-value">{user.joinDays}</Text><Text className="stat-label">加入天数</Text></View>
          </View>
        </View>
        <View className="card menu-card">
          {menuItems.map(item => (
            <View key={item.id} className="menu-item" onClick={item.id === 'settings' ? this.handleLogout : undefined}>
              <View className="menu-left"><Text className="menu-emoji">{item.emoji}</Text><Text className="menu-title">{item.title}</Text></View>
              <Text className="menu-arrow">›</Text>
            </View>
          ))}
        </View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item">任务</View><View className="nav-item">发布</View><View className="nav-item active">我的</View></View>
      </View>
    )
  }
}
