// 淘汰赛对阵图组件
Component({
  data: {
    rounds: []
  },
  lifetimes: {
    created() {
      this._modelCtx = wx.modelContext.getContext(this)
      var self = this
      var { NotificationType } = wx.modelContext
      this._modelCtx.on(NotificationType.Result, function(data) {
        var result = data && data.result ? data.result : {}
        var meta = result._meta || {}
        var rounds = meta.viewRounds || (result.structuredContent && result.structuredContent.rounds) || []
        // 标记已完赛和占位符
        rounds.forEach(function(r) {
          r.matches.forEach(function(m) {
            m.finished = m.scoreA !== undefined && m.scoreA !== null
            m.isPlaceholder = /^[A-Z]\d$|^W\d$|^L\d$|^T\d$/.test(m.teamA || '') || /^[A-Z]\d$|^W\d$|^L\d$|^T\d$/.test(m.teamB || '')
          })
        })
        self.setData({ rounds: rounds })
      })
    }
  },
  methods: {
    onTapMore() {
      var viewCtx = wx.modelContext.getViewContext(this)
      if (viewCtx) {
        viewCtx.openDetailPage({ url: '/pages/teams/teams' })
      }
    }
  }
})
