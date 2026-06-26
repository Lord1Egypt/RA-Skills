import { Component } from 'react'
import { View, Text, Button } from '@tarojs/components'
import { navigateTo } from '@tarojs/taro'
import './index.scss'

export default class AuthIndex extends Component {
  state = { gender: 'female' as 'female' | 'male', loading: false }

  handleLogin = async () => {
    // TODO: 调用微信登录 wx.login()，换取 code
    // TODO: 调用后端 /api/auth/wx-login 接口换取 token
    this.setState({ loading: true })
    try {
      // === 示例代码（接入时替换）===
      // const codeRes = await wx.login()
      // const res = await wxLogin(codeRes.code)
      // wx.setStorageSync('token', res.token)
      // wx.setStorageSync('userInfo', res.userInfo)
      // navigateTo({ url: '/pages/home/index' })
      
      // 演示：直接跳转
      navigateTo({ url: '/pages/home/index' })
    } finally {
      this.setState({ loading: false })
    }
  }

  render() {
    const { gender, loading } = this.state
    const isFemale = gender === 'female'
    return (
      <View className="auth-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className={`art-card art-${gender}`}>
          <View className="art-tag">{isFemale ? '白色小熊背景' : '棕色小熊背景'}</View>
        </View>
        <View className="card hero-card">
          <Text className="welcome-title">{isFemale ? '欢迎回来，小熊同学' : '欢迎加入，熊熊伙伴'}</Text>
          <Text className="welcome-desc">微信授权登录后即可参与任务赚取金币</Text>
        </View>
        <Button className="btn-primary" onClick={this.handleLogin} disabled={loading} loading={loading}>
          {loading ? '登录中...' : '微信授权登录'}
        </Button>
        <Button className="btn-ghost">查看登录说明</Button>
      </View>
    )
  }
}
