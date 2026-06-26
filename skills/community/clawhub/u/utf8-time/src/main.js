function currentTime() {
  return new Date().toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// 导出函数供外部调用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { currentTime }
}

// 直接输出当前时间
console.log(currentTime())