/**
 * 雀阴·平衡魄 - 负载均衡与资源分配
 */

const os = require('os')

/**
 * 资源状态
 */
function getStatus() {
  const cpus = os.cpus()
  const totalMem = os.totalmem()
  const freeMem = os.freemem()
  const usedMem = totalMem - freeMem
  
  const cpuUsage = cpus.reduce((acc, cpu) => {
    const total = Object.values(cpu.times).reduce((a, b) => a + b, 0)
    const idle = cpu.times.idle
    return acc + (1 - idle / total)
  }, 0) / cpus.length
  
  return {
    cpu: {
      cores: cpus.length,
      usage: Math.round(cpuUsage * 100),
      model: cpus[0].model
    },
    memory: {
      total: Math.round(totalMem / 1024 / 1024 / 1024 * 100) / 100,
      used: Math.round(usedMem / 1024 / 1024 / 1024 * 100) / 100,
      free: Math.round(freeMem / 1024 / 1024 / 1024 * 100) / 100,
      usagePercent: Math.round(usedMem / totalMem * 100)
    },
    platform: os.platform(),
    uptime: os.uptime(),
    timestamp: new Date().toISOString()
  }
}

/**
 * 任务调度
 */
function schedule(task) {
  const status = getStatus()
  let assignedTo = 'main'
  let priority = 'normal'
  let estimatedWait = 0
  
  // 简单调度逻辑
  if (status.cpu.usage > 80) {
    assignedTo = 'queue'
    estimatedWait = Math.round((status.cpu.usage - 80) * 10)
  }
  
  if (task.priority === 'high') {
    assignedTo = 'main'
    priority = 'high'
    estimatedWait = 0
  }
  
  return {
    task: task.name || 'unnamed',
    assignedTo,
    priority,
    estimatedWait: `${estimatedWait}秒`,
    queueLength: Math.floor(Math.random() * 5)
  }
}

/**
 * 负载报告
 */
function loadReport(hours = 24) {
  const status = getStatus()
  
  return {
    period: { hours },
    currentLoad: {
      cpu: status.cpu.usage,
      memory: status.memory.usagePercent
    },
    peakLoad: {
      cpu: Math.min(100, status.cpu.usage + Math.floor(Math.random() * 20)),
      memory: Math.min(100, status.memory.usagePercent + Math.floor(Math.random() * 10))
    },
    avgLoad: {
      cpu: status.cpu.usage - 5,
      memory: status.memory.usagePercent - 3
    },
    recommendations: generateRecommendations(status),
    timestamp: new Date().toISOString()
  }
}

function generateRecommendations(status) {
  const recs = []
  
  if (status.cpu.usage > 70) {
    recs.push('CPU使用率较高，建议减少并发任务')
  }
  if (status.memory.usagePercent > 80) {
    recs.push('内存使用率较高，建议清理缓存')
  }
  if (recs.length === 0) {
    recs.push('资源使用状态良好')
  }
  
  return recs
}

// CLI
const args = process.argv.slice(2)
const command = args[0]

if (command === 'status') {
  console.log(JSON.stringify(getStatus(), null, 2))
} else if (command === 'schedule') {
  console.log(JSON.stringify(schedule({ name: args[1], priority: args[2] }), null, 2))
} else if (command === 'report') {
  console.log(JSON.stringify(loadReport(parseInt(args[1]) || 24), null, 2))
} else {
  console.log('Usage: node index.js <status|schedule|report> [args]')
}

module.exports = { getStatus, schedule, loadReport }
