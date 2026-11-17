Component({
  data: { team: null },
  lifetimes: {
    created() {
      this._modelCtx = wx.modelContext.getContext(this)
      const { NotificationType } = wx.modelContext
      this._modelCtx.on(NotificationType.Result, (data) => {
        const result = data && data.result ? data.result : {}
        const meta = result._meta || {}
        this.setData({ team: meta.viewTeam || null })
      })
    }
  }
})
