import { Component } from 'react'
import { View, Text } from '@tarojs/components'
import './index.scss'

export default class HomeIndex extends Component {
  state = { circleName: '熊熊一家', inviteCode: 'HOME-2026-8899', notice: '欢迎加入熊熊一家！' }

  componentDidMount() {
    // TODO: 加载圈子信息
    // const userInfo = wx.getStorageSync('userInfo')
    // const res = await getCircleInfo(userInfo?.circleId)
    // this.setState({ ... })
  }

  render() {
    const { circleName, inviteCode, notice } = this.state
    return (
      <View className="home-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="app-head">
          <View><Text className="small">当前圈子</Text><Text className="circle-name">{circleName}</Text></View>
          <View className="pill">圈子主视觉</View>
        </View>
        <View className="art-card art-group"><View className="art-tag">双熊合照背景</View></View>
        <View className="card">
          <View className="row"><Text className="title-strong">圈子公告</Text><Text className="small muted">今日更新</Text></View>
          <Text className="task-desc">{notice}</Text>
        </View>
        <View className="card">
          <View className="field"><Text className="label">圈子邀请码</Text>
            <View className="input"><Text className="invite-code">{inviteCode}</Text></View>
          </View>
        </View>
        <View className="bottom-nav"><View className="nav-item active">首页</View><View className="nav-item">任务</View><View className="nav-item">发布</View><View className="nav-item">我的</View></View>
      </View>
    )
  }
}
