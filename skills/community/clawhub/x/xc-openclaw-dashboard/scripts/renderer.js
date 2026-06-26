/**
 * OpenClaw Dashboard - Canvas 渲染引擎
 * 负责将采集的数据渲染成可视化仪表盘
 */

// 默认配色方案
const DEFAULT_COLORS = {
  background: '#0f172a',
  surface: '#1e293b',
  border: '#334155',
  text: '#f1f5f9',
  textMuted: '#94a3b8',
  input: '#4ade80',
  output: '#60a5fa',
  total: '#f472b6',
  accent: '#38bdf8',
  warning: '#fbbf24',
  error: '#f87171',
  success: '#22c55e'
};

/**
 * 渲染器类
 */
class DashboardRenderer {
  constructor(canvas, config = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.config = { ...DEFAULT_COLORS, ...config };
    this.padding = 24;
    this.cardRadius = 12;
    this.data = null;
  }

  /**
   * 设置数据并渲染
   * @param {object} data - 仪表盘数据
   */
  render(data) {
    this.data = data;
    this.resize();
    this.clear();
    this.drawBackground();
    this.drawHeader();
    this.drawTokenSection();
    this.drawSessionsSection();
    this.drawSystemSection();
    this.drawFooter();
  }

  /**
   * 调整画布大小
   */
  resize() {
    const container = this.canvas.parentElement;
    if (container) {
      this.canvas.width = container.clientWidth;
      this.canvas.height = Math.max(600, this.calculateHeight());
    }
  }

  /**
   * 计算所需画布高度
   */
  calculateHeight() {
    const headerHeight = 80;
    const tokenSectionHeight = 200;
    const systemSectionHeight = 120;
    const footerHeight = 40;
    const sessionsSectionHeight = this.data?.sessions?.length > 0
      ? Math.min(this.data.sessions.length * 50 + 60, 300)
      : 0;
    return headerHeight + tokenSectionHeight + sessionsSectionHeight + systemSectionHeight + footerHeight + this.padding * 4;
  }

  /**
   * 清空画布
   */
  clear() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * 绘制背景
   */
  drawBackground() {
    this.ctx.fillStyle = this.config.background;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * 绘制头部
   */
  drawHeader() {
    const ctx = this.ctx;
    const { padding } = this;
    const y = padding + 20;

    // 标题
    ctx.font = 'bold 24px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.text;
    ctx.fillText('🤖 OpenClaw Dashboard', padding, y);

    // 更新时间
    ctx.font = '13px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.textMuted;
    const timeStr = this.data?.timestamp
      ? new Date(this.data.timestamp).toLocaleString('zh-CN')
      : new Date().toLocaleString('zh-CN');
    ctx.fillText(`最后更新: ${timeStr}`, padding, y + 24);

    // 模型标签
    const modelText = this.data?.model || 'Unknown Model';
    this.drawBadge(padding, y + 40, modelText, this.config.accent);

    // Session 计数
    const sessionCount = this.data?.sessionCount || 0;
    this.drawBadge(this.canvas.width - padding - 80, y + 20, `${sessionCount} Sessions`, this.config.success);
  }

  /**
   * 绘制徽章
   */
  drawBadge(x, y, text, color) {
    const ctx = this.ctx;
    const padding = 10;
    const height = 26;

    ctx.font = '12px Inter, system-ui, sans-serif';
    const width = ctx.measureText(text).width + padding * 2;

    // 背景
    ctx.fillStyle = color + '20';
    this.roundRect(x, y, width, height, 6);
    ctx.fill();

    // 边框
    ctx.strokeStyle = color + '60';
    ctx.lineWidth = 1;
    this.roundRect(x, y, width, height, 6);
    ctx.stroke();

    // 文字
    ctx.fillStyle = color;
    ctx.fillText(text, x + padding, y + 17);
  }

  /**
   * 绘制 Token 用量区块
   */
  drawTokenSection() {
    const ctx = this.ctx;
    const { padding, canvas } = this;
    const sectionY = 130;
    const sectionWidth = canvas.width - padding * 2;

    // 卡片背景
    this.drawCard(padding, sectionY, sectionWidth, 180);

    // 标题
    ctx.font = 'bold 16px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.text;
    ctx.fillText('📊 Token 用量', padding + 20, sectionY + 35);

    const tokens = this.data?.tokens || { input: 0, output: 0, total: 0 };
    const maxToken = Math.max(tokens.input + tokens.output, 1);

    // Token 数据行
    const rowY = sectionY + 65;
    const items = [
      { label: '输入 (Input)', value: this.formatNumber(tokens.input), color: this.config.input },
      { label: '输出 (Output)', value: this.formatNumber(tokens.output), color: this.config.output },
      { label: '总计 (Total)', value: this.formatNumber(tokens.total), color: this.config.total }
    ];

    const itemWidth = (sectionWidth - 40) / 3;
    items.forEach((item, i) => {
      const itemX = padding + 20 + i * itemWidth;

      // 标签
      ctx.font = '12px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.textMuted;
      ctx.fillText(item.label, itemX, rowY);

      // 数值
      ctx.font = 'bold 22px Inter, system-ui, sans-serif';
      ctx.fillStyle = item.color;
      ctx.fillText(item.value, itemX, rowY + 30);

      // 进度条
      const barY = rowY + 45;
      const barWidth = itemWidth - 40;
      const barHeight = 8;
      const ratio = item.label === '总计 (Total)'
        ? Math.min(tokens.total / 100000, 1)
        : (item.label === '输入 (Input)' ? tokens.input : tokens.output) / maxToken;

      // 进度条背景
      ctx.fillStyle = this.config.border;
      this.roundRect(itemX, barY, barWidth, barHeight, 4);
      ctx.fill();

      // 进度条填充
      ctx.fillStyle = item.color;
      if (ratio > 0) {
        this.roundRect(itemX, barY, barWidth * ratio, barHeight, 4);
        ctx.fill();
      }
    });
  }

  /**
   * 绘制 Sessions 列表区块
   */
  drawSessionsSection() {
    const ctx = this.ctx;
    const { padding, canvas } = this;
    const sessions = this.data?.sessions || [];
    if (sessions.length === 0) return;

    const sectionY = 330;
    const sectionWidth = canvas.width - padding * 2;
    const itemHeight = 50;

    // 卡片背景
    this.drawCard(padding, sectionY, sectionWidth, sessions.length * itemHeight + 50);

    // 标题
    ctx.font = 'bold 16px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.text;
    ctx.fillText('📋 活跃 Sessions', padding + 20, sectionY + 35);

    sessions.slice(0, 8).forEach((session, i) => {
      const y = sectionY + 60 + i * itemHeight;
      const x = padding + 20;
      const itemWidth = sectionWidth - 40;

      // 分隔线
      if (i > 0) {
        ctx.strokeStyle = this.config.border;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, y - 10);
        ctx.lineTo(x + itemWidth, y - 10);
        ctx.stroke();
      }

      // Session 标签
      ctx.font = '14px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.text;
      ctx.fillText(session.label || session.id, x, y + 5);

      // 类型标签
      const kind = session.kind || 'agent';
      this.drawBadge(x + ctx.measureText(session.label || session.id).width + 10, y - 15, kind, this.getKindColor(kind));

      // 活跃时间
      ctx.font = '12px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.textMuted;
      ctx.fillText(`${session.activeMinutes} 分钟活跃 · ${session.messageCount} 条消息`, x, y + 25);
    });

    if (sessions.length > 8) {
      ctx.font = '12px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.textMuted;
      ctx.fillText(`还有 ${sessions.length - 8} 个 session...`, padding + 20, sectionY + 60 + 8 * itemHeight);
    }
  }

  /**
   * 绘制系统信息区块
   */
  drawSystemSection() {
    const ctx = this.ctx;
    const { padding, canvas } = this;
    const sectionY = canvas.height - 200;
    const sectionWidth = canvas.width - padding * 2;

    // 卡片背景
    this.drawCard(padding, sectionY, sectionWidth, 100);

    // 系统信息
    const items = [
      { label: '🖥️ 节点', value: this.data?.node || 'Unknown' },
      { label: '📡 Channel', value: this.data?.channel || 'Unknown' },
      { label: '⏱️ 运行时间', value: this.data?.uptime || 'N/A' }
    ];

    const itemWidth = (sectionWidth - 40) / 3;
    items.forEach((item, i) => {
      const x = padding + 20 + i * itemWidth;

      ctx.font = '11px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.textMuted;
      ctx.fillText(item.label, x, sectionY + 30);

      ctx.font = '13px Inter, system-ui, sans-serif';
      ctx.fillStyle = this.config.text;
      ctx.fillText(item.value, x, sectionY + 55);
    });

    // OS 信息
    ctx.font = '11px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.textMuted;
    ctx.fillText(`🛠️ ${this.data?.os || 'Unknown OS'}`, padding + 20, sectionY + 80);
  }

  /**
   * 绘制页脚
   */
  drawFooter() {
    const ctx = this.ctx;
    const { padding, canvas } = this;
    const y = canvas.height - 20;

    ctx.font = '11px Inter, system-ui, sans-serif';
    ctx.fillStyle = this.config.textMuted;
    ctx.fillText('由 OpenClaw Dashboard Skill 驱动', padding, y);
    ctx.fillText('xu-chenglin', canvas.width - padding - 60, y);
  }

  /**
   * 绘制卡片背景
   */
  drawCard(x, y, width, height) {
    const ctx = this.ctx;

    ctx.fillStyle = this.config.surface;
    this.roundRect(x, y, width, height, this.cardRadius);
    ctx.fill();

    ctx.strokeStyle = this.config.border;
    ctx.lineWidth = 1;
    this.roundRect(x, y, width, height, this.cardRadius);
    ctx.stroke();
  }

  /**
   * 圆角矩形路径
   */
  roundRect(x, y, width, height, radius) {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }

  /**
   * 格式化数字
   */
  formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  }

  /**
   * 获取 Session 类型的颜色
   */
  getKindColor(kind) {
    const colors = {
      agent: this.config.accent,
      subagent: this.config.success,
      acp: this.config.warning,
      default: this.config.textMuted
    };
    return colors[kind] || colors.default;
  }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DashboardRenderer, DEFAULT_COLORS };
}
