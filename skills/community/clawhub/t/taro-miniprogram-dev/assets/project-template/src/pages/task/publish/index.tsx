import { Component } from 'react'
import { View, Text, Input, Textarea, Button } from '@tarojs/components'
import { showToast } from '@tarojs/taro'
import './index.scss'

export default class TaskPublish extends Component {
  state = { title: '', desc: '', coin: '', steps: '', submitting: false }

  handlePublish = async () => {
    const { title, desc, coin, steps } = this.state
    if (!title.trim()) { showToast({ title: '请填写任务标题', icon: 'none' }); return }
    if (!desc.trim()) { showToast({ title: '请填写任务描述', icon: 'none' }); return }
    if (!coin.trim() || isNaN(Number(coin))) { showToast({ title: '请填写正确的金币数量', icon: 'none' }); return }
    const stepList = steps.split('\n').filter(s => s.trim())
    this.setState({ submitting: true })
    try {
      // TODO: await publishTask({ title: title.trim(), desc: desc.trim(), coin: Number(coin), steps: stepList })
      showToast({ title: '发布成功', icon: 'success' })
      this.setState({ title: '', desc: '', coin: '', steps: '' })
    } finally {
      this.setState({ submitting: false })
    }
  }

  render() {
    const { title, desc, coin, steps, submitting } = this.state
    return (
      <View className="publish-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="app-head"><Text className="page-title">发布任务</Text></View>
        <View className="card"><View className="field"><Text className="label">任务标题</Text><Input className="input" placeholder="例如：每日签到" value={title} onInput={e => this.setState({ title: e.detail.value })} /></View></View>
        <View className="card"><View className="field"><Text className="label">任务描述</Text><Textarea className="textarea" placeholder="详细描述任务要求..." value={desc} onInput={e => this.setState({ desc: e.detail.value })} /></View></View>
        <View className="card"><View className="field"><Text className="label">奖励金币数量</Text><Input className="input" type="number" placeholder="例如：10" value={coin} onInput={e => this.setState({ coin: e.detail.value })} /></View></View>
        <View className="card"><View className="field"><Text className="label">完成步骤（每行一步）</Text><Textarea className="textarea" placeholder="打开小程序\n点击签到按钮\n完成签到" value={steps} onInput={e => this.setState({ steps: e.detail.value })} /></View></View>
        <View className="action-bar"><Button className="btn-primary" onClick={this.handlePublish} disabled={submitting} loading={submitting}>{submitting ? '发布中...' : '确认发布'}</Button></View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item">任务</View><View className="nav-item active">发布</View><View className="nav-item">我的</View></View>
      </View>
    )
  }
}
