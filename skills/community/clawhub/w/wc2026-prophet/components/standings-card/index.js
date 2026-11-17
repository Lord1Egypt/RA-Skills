// 小组积分榜组件
Component({
  data: {
    groups: []
  },
  lifetimes: {
    created() {
      this._modelCtx = wx.modelContext.getContext(this)
      var self = this
      var { NotificationType } = wx.modelContext
      this._modelCtx.on(NotificationType.Result, function(data) {
        var result = data && data.result ? data.result : {}
        var meta = result._meta || {}
        var groups = meta.viewGroups || (result.structuredContent && result.structuredContent.groups) || []
        // 为每队计算排名序号和行样式
        groups.forEach(function(g) {
          g.standings.forEach(function(s, idx) {
            s.rank = idx + 1
            s.rowClass = idx === 0 ? 'row-top' : (idx === 1 ? 'row-top' : (idx === 2 ? 'row-third' : ''))
          })
        })
        self.setData({ groups: groups })
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
