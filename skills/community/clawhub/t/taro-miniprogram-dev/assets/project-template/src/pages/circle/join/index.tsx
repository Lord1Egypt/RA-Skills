import { Component } from 'react'
import { View, Text, Input, Button } from '@tarojs/components'
import { redirectTo } from '@tarojs/taro'
import './index.scss'

export default class CircleJoin extends Component {
  state = { inviteCode: '', loading: false }

  handleJoin = async () => {
    const code = this.state.inviteCode.trim()
    if (!code) { wx.showToast({ title: '请输入邀请码', icon: 'none' }); return }
    this.setState({ loading: true })
    try {
      // TODO: const circle = await joinCircle(code)
      // wx.showToast({ title: '加入成功', icon: 'success' })
      redirectTo({ url: '/pages/home/index' })
    } finally {
      this.setState({ loading: false })
    }
  }

  render() {
    const { inviteCode, loading } = this.state
    return (
      <View className="join-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="page-header"><Text className="page-title">加入圈子</Text><View className="pill">熊熊圈</View></View>
        <View className="card"><View className="field"><Text className="label">请输入圈子邀请码</Text><Input className="input" placeholder="例如：HOME-2026-8899" value={inviteCode} onInput={e => this.setState({ inviteCode: e.detail.value })} /></View></View>
        <View className="tips card"><Text className="tips-title">如何获取邀请码？</Text><Text className="tips-desc">联系圈子主理人获取专属邀请码，输入即可加入圈子。</Text></View>
        <View className="action-bar"><Button className="btn-primary" onClick={this.handleJoin} disabled={loading} loading={loading}>{loading ? '加入中...' : '加入圈子'}</Button></View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item">任务</View><View className="nav-item">发布</View><View className="nav-item">我的</View></View>
      </View>
    )
  }
}
