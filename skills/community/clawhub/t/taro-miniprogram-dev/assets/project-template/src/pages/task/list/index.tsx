import { Component } from 'react'
import { View, Text } from '@tarojs/components'
import { navigateTo } from '@tarojs/taro'
import './index.scss'

// TODO: 替换为真实数据
const mockTasks = [
  { id: '1', title: '每日签到', desc: '每天签到可获得金币奖励', coin: 10, status: 'ongoing' },
  { id: '2', title: '分享朋友圈', desc: '分享小程序到朋友圈', coin: 50, status: 'ongoing' },
  { id: '3', title: '邀请好友', desc: '成功邀请1位好友加入圈子', coin: 100, status: 'completed' },
]

export default class TaskList extends Component {
  state = { tasks: mockTasks as any[], loading: false, activeTab: 'ongoing' }

  handleTabChange = (tab: string) => this.setState({ activeTab: tab })

  componentDidMount() {
    // TODO: 加载任务列表
    // const res = await getTaskList(this.state.activeTab)
    // this.setState({ tasks: res.list })
  }

  render() {
    const { tasks, loading, activeTab } = this.state
    const tabs = [{ key: 'ongoing', label: '进行中' }, { key: 'completed', label: '已完成' }, { key: 'all', label: '全部' }]
    const filtered = activeTab === 'all' ? tasks : tasks.filter(t => t.status === activeTab)
    return (
      <View className="task-list-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="app-head"><Text className="page-title">任务中心</Text><View className="pill">{tabs.find(t => t.key === activeTab)?.label}</View></View>
        <View className="tab-bar">
          {tabs.map(t => <View key={t.key} className={`tab-item ${activeTab === t.key ? 'active' : ''}`} onClick={() => this.handleTabChange(t.key)}>{t.label}</View>)}
        </View>
        <View className="task-stack">
          {loading ? <View className="loading">加载中...</View> : filtered.length === 0 ? <View className="empty">暂无任务</View> :
            filtered.map(task => (
              <View key={task.id} className="card task-card" onClick={() => navigateTo({ url: `/pages/task/detail/index?taskId=${task.id}` })}>
                <View className="row"><Text className="task-title">{task.title}</Text><View className={`status-badge ${task.status}`}>{task.status === 'completed' ? '已完成' : '进行中'}</View></View>
                <Text className="task-desc">{task.desc}</Text>
                <View className="row coin-row"><Text className="coin-label">奖励金币</Text><Text className="coin-value">+{task.coin}</Text></View>
              </View>
            ))
          }
        </View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item active">任务</View><View className="nav-item">发布</View><View className="nav-item">我的</View></View>
      </View>
    )
  }
}
