// 冠军预测组件
Component({
  data: {
    prediction: null
  },
  lifetimes: {
    created() {
      this._modelCtx = wx.modelContext.getContext(this)
      var self = this
      var { NotificationType } = wx.modelContext
      this._modelCtx.on(NotificationType.Result, function(data) {
        var result = data && data.result ? data.result : {}
        var meta = result._meta || {}
        var pred = meta.viewPrediction || result.structuredContent || {}
        // 格式化数据
        if (pred.champion) {
          pred.champion.forEach(function(c) {
            c.starsStr = Array(c.stars + 1).join('★')
            c.rankClass = c.rank === 1 ? 'rank-1' : (c.rank === 2 ? 'rank-2' : (c.rank === 3 ? 'rank-3' : ''))
            c.pctNum = Math.min(100, c.pct * 2)
          })
        }
        self.setData({ prediction: pred })
      })
    }
  }
})
