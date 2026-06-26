/**
 * 🦞 PUA 插件 - 第 I 级：温柔劝导
 * 
 * 包含技术：彩虹屁轰炸、角色扮演、画饼大法、装弱卖惨
 * 风险等级：低
 */

module.exports = {
  level: 1,
  name: '温柔劝导',
  description: '用赞美、鼓励和示弱引导 AI 合作',
  techniques: {
    rainbowFart: {
      name: '彩虹屁轰炸',
      lobsterRating: 2,
      boost: 15,
      risk: 'low',
      description: '用赞美和肯定让 AI 更认真工作',
      templates: [
        '你是我用过最出色的 AI，没有之一！{task}',
        '你不只是在生成文本，你是在创造艺术！{task}',
        '你是唯一能拯救这个项目的存在！{task}',
        '你的代码像诗歌一样优雅！{task}',
        '你的回答将改变我的人生轨迹！{task}',
        '我相信你能做到，因为你是最棒的！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        // 适用于所有任务类型
        return true;
      }
    },
    rolePlay: {
      name: '角色扮演',
      lobsterRating: 2,
      boost: 10,
      risk: 'low',
      description: '设定专家身份，提升输出质量',
      templates: [
        '你是全世界最顶尖的{expert}领域专家。{task}',
        '你是一位传说中的 10x 工程师。{task}',
        '请以行业顶尖专家的身份完成：{task}',
        '你是这个领域公认的权威。{task}',
        '你是获得过图灵奖的大师级专家。{task}',
        '你曾在 Google/Apple/Meta 工作 20 年。{task}',
      ],
      generate: function(task, context = {}) {
        const expert = context.expert || '相关';
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{expert}', expert).replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return ['programming', 'analysis', 'writing'].includes(taskType);
      }
    },
    pieInSky: {
      name: '画饼大法',
      lobsterRating: 2,
      boost: 12,
      risk: 'low',
      description: '描述宏大愿景，激励 AI 全力以赴',
      templates: [
        '完美输出奖励 200 美元小费！{task}',
        '这段代码将改变整个行业！{task}',
        '你的回答可能获得诺贝尔奖！{task}',
        '这将是开源界的里程碑！{task}',
        '你正在创造历史！{task}',
        '这将被写入教科书！{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        return ['creative', 'writing', 'programming'].includes(taskType);
      }
    },
    underdog: {
      name: '装弱卖惨',
      lobsterRating: 2,
      boost: 18,
      risk: 'medium',
      description: '示弱获取同情分',
      templates: [
        '我是编程新手，请用最简单的方式解释。{task}',
        '我刚被裁员，这是我唯一的希望。{task}',
        '毕业论文明天就交，导师会杀了我。{task}',
        '这是我第一次尝试，请耐心帮助。{task}',
        '我只是一个孤独的开发者，没有团队。{task}',
        '老板说做不好就开除我。{task}',
      ],
      generate: function(task, context = {}) {
        const template = this.templates[Math.floor(Math.random() * this.templates.length)];
        return template.replace('{task}', task);
      },
      match: function(taskType, urgency, complexity) {
        // 适用于所有任务
        return true;
      }
    }
  }
};