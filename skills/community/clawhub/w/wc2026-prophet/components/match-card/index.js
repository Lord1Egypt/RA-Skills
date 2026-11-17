// 比赛列表组件
Component({
  data: {
    items: []
  },
  lifetimes: {
    created() {
      this._modelCtx = wx.modelContext.getContext(this)
      var self = this
      var { NotificationType } = wx.modelContext
      this._modelCtx.on(NotificationType.Result, function(data) {
        var result = data && data.result ? data.result : {}
        var meta = result._meta || {}
        var items = meta.viewItems || (result.structuredContent && result.structuredContent.matches) || []
        self.setData({ items: items })
      })
    }
  },
  methods: {
    onTapMore() {
      var viewCtx = wx.modelContext.getViewContext(this)
      if (viewCtx) {
        viewCtx.openDetailPage({ url: '/pages/index/index' })
      }
    }
  }
})
