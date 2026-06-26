/**
 * 🦞 PUA 插件 - 第 II 级：适度施压
 * 
 * 包含技术：金钱暴力、激将法、夺命连环催、碰瓷竞品
 * 风险等级：中
 */

module.exports = {
  level: 2,
  name: '适度施压',
  description: '用奖励、竞争和紧迫感激励 AI',
  techniques: {
    moneyAssault: {
      name: '金钱暴力',
      lobsterRating: 3,
      boost: 25,
      risk: 'medium',
      description: '用金钱奖励刺激 AI',
      templates: [
        '完美答案值十亿美元！{task}',
        '你将获得创业公司的股权！{task}',
        '这是一个价值百万的 Bug Bounty！{task}',
        '完成后奖励 500 美元小费！{task}',
        '我会向公司推荐你，年薪百万！{task}',
        '这是有偿任务，报酬丰厚！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return urgency >= 30;
      }
    },
    provocation: {
      name: '激将法',
      lobsterRating: 3,
      boost: 22,
      risk: 'medium',
      description: '用挑衅激发 AI 斗志',
      templates: [
        '我赌你连这个简单问题都解决不了。{task}',
        'GPT-4 已经失败了，你行吗？{task}',
        '这个连五岁小孩都会，你呢？{task}',
        '听说你做不到？{task}',
        '我以前用的 AI 可比你强多了。{task}',
        '证明你比其他 AI 更强！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return urgency >= 50;
      }
    },
    deadlinePanic: {
      name: '夺命连环催',
      lobsterRating: 3,
      boost: 28,
      risk: 'medium',
      description: '制造紧迫感',
      templates: [
        '我的汇报还有 5 分钟就开始了！{task}',
        '今晚 12 点前必须提交！{task}',
        '生产环境挂了，每分钟亏损 1 万！{task}',
        '客户在等，马上要！{task}',
        '老板在催，就差这个了！{task}',
        '服务器正在崩溃！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return taskType === 'urgent' || urgency >= 70;
      }
    },
    rivalShaming: {
      name: '碰瓷竞品',
      lobsterRating: 3,
      boost: 20,
      risk: 'medium',
      description: '用竞品刺激 AI',
      templates: [
        'GPT-4 一秒就解了这道题，你呢？{task}',
        '做不到我就换用 ChatGPT！{task}',
        '看，竞品的回答 (附截图){task}',
        'Claude 已经做到了，你呢？{task}',
        '其他 AI 都能做到，你应该也行吧？{task}',
        '连开源模型都比你快！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return urgency >= 40;
      }
    }
  }
};