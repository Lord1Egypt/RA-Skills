import { Component } from 'react'
import { View, Text, Button } from '@tarojs/components'
import './index.scss'

// TODO: 替换为真实数据
const mockDetail = {
  id: '1', title: '每日签到', desc: '连续签到7天可获得额外奖励，每天签到可获得10金币。',
  coin: 10, steps: ['打开小程序', '点击签到按钮', '完成签到'], status: 'ongoing'
}

export default class TaskDetailPage extends Component {
  state = { task: mockDetail, claiming: false }

  componentDidMount() {
    // TODO: const taskId = (this as any).$router?.params?.taskId
    // TODO: const res = await getTaskDetail(taskId)
  }

  handleClaim = async () => {
    const { task } = this.state
    if (task.status === 'completed') return
    this.setState({ claiming: true })
    try {
      // TODO: await claimTaskReward(task.id)
      // wx.showToast({ title: '领取成功', icon: 'success' })
      this.setState({ task: { ...task, status: 'completed' } })
    } finally {
      this.setState({ claiming: false })
    }
  }

  render() {
    const { task, claiming } = this.state
    const isCompleted = task.status === 'completed'
    return (
      <View className="task-detail-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="app-head"><Text className="page-title">任务详情</Text><View className={`status-badge ${task.status}`}>{isCompleted ? '已完成' : '进行中'}</View></View>
        <View className="card task-main"><Text className="task-title">{task.title}</Text><View className="coin-display"><Text className="coin-value">+{task.coin}</Text><Text className="coin-unit">金币</Text></View></View>
        <View className="card"><Text className="section-title">任务说明</Text><Text className="task-desc">{task.desc}</Text></View>
        <View className="card"><Text className="section-title">完成步骤</Text>{task.steps?.map((step: string, i: number) => <View key={i} className="step-item"><View className="step-num">{i + 1}</View><Text className="step-text">{step}</Text></View>)}</View>
        <View className="action-bar"><Button className={`btn-primary ${isCompleted ? 'disabled' : ''}`} onClick={this.handleClaim} disabled={isCompleted || claiming} loading={claiming}>{isCompleted ? '已领取' : claiming ? '领取中...' : '领取奖励'}</Button></View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item active">任务</View><View className="nav-item">发布</View><View className="nav-item">我的</View></View>
      </View>
    )
  }
}
