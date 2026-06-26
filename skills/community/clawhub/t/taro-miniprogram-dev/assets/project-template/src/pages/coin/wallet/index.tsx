import { Component } from 'react'
import { View, Text } from '@tarojs/components'
import './index.scss'

// TODO: 替换为真实数据
const mockWallet = { totalCoin: 360, monthIncome: 210, monthExpense: 50 }
const mockRecords = [
  { id: '1', type: 'income', desc: '每日签到', coin: 10, createdAt: '2026-03-27' },
  { id: '2', type: 'expense', desc: '兑换优惠券', coin: -50, createdAt: '2026-03-26' },
]

export default class CoinWallet extends Component {
  state = { walletInfo: mockWallet, records: mockRecords, loading: false }

  componentDidMount() {
    // TODO: const [wallet, records] = await Promise.all([getWalletInfo(), getCoinRecords()])
  }

  render() {
    const { walletInfo, records } = this.state
    return (
      <View className="wallet-page">
        <View className="status-bar"><Text>9:41</Text><Text>5G 88%</Text></View>
        <View className="app-head"><Text className="page-title">金币钱包</Text></View>
        <View className="card balance-card"><Text className="balance-label">当前余额</Text><View className="balance-display"><Text className="balance-value">{walletInfo.totalCoin}</Text><Text className="balance-unit">金币</Text></View></View>
        <View className="stats-row">
          <View className="card stat-card income"><Text className="stat-label">本月收入</Text><Text className="stat-value">+{walletInfo.monthIncome}</Text></View>
          <View className="card stat-card expense"><Text className="stat-label">本月支出</Text><Text className="stat-value">-{walletInfo.monthExpense}</Text></View>
        </View>
        <View className="card records-card">
          <Text className="section-title">最近记录</Text>
          {records.length === 0 ? <View className="empty">暂无记录</View> : records.map(r => (
            <View key={r.id} className="record-item"><View><Text className="record-desc">{r.desc}</Text><Text className="record-time">{r.createdAt}</Text></View><Text className={`record-coin ${r.type}`}>{r.type === 'income' ? '+' : ''}{r.coin}</Text></View>
          ))}
        </View>
        <View className="bottom-nav"><View className="nav-item">首页</View><View className="nav-item">任务</View><View className="nav-item">发布</View><View className="nav-item active">我的</View></View>
      </View>
    )
  }
}
