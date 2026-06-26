# 阴阳道 - AI游戏接口规范

## 项目背景

为「阴阳道」Roguelike修仙游戏开发AI控制接口，使AI Agent能够：
1. 读取游戏当前状态
2. 分析局势并做出决策
3. 执行游戏动作

## 现状分析

### 当前游戏架构
- 单HTML文件（rogue-dungeon/index.html）
- 纯前端JavaScript，无后端
- 状态存储在内存变量中

### 核心游戏数据
```javascript
player = { x, y, hp, maxHp, atk, def, gold, exp, level, expTo, class, weapon, energy, maxEnergy, pet, hasKey, cursed, ... }
map = 2D字符数组（#墙 .地 @玩家 z/d/s敌人...）
enemies = [{ x, y, name, hp, maxHp, atk, def, isElite, isBoss, skill, ... }]
items = [{ x, y, name, type, value, ... }]
floor = 当前层数（1-10）
logs = 最近日志数组
```

## 任务目标

### 1. 暴露Game API
在window对象上暴露可控的API：

```javascript
window.YinYangDAO = {
  // 获取完整游戏状态
  getState: () => ({
    player: { /* 玩家属性 */ },
    map: [/* 2D数组 */],
    enemies: [/* 敌人列表 */],
    items: [/* 物品列表 */],
    floor: number,
    logs: string[],
    validActions: ['w','a','s_d','attack','skill','wait']
  }),
  
  // 执行动作
  action: (action: string) => Result,
  
  // 重置游戏
  reset: (playerClass?: string) => void,
  
  // 获取可读状态摘要（供AI分析）
  getSummary: () => string
}
```

### 2. 动作接口
| 动作 | 参数 | 说明 |
|------|------|------|
| move | 'up'/'down'/'left'/'right' | 移动 |
| attack | direction | 攻击方向敌人 |
| skill | skillId | 使用技能 |
| wait | - | 等待一回合 |
| useItem | itemIndex | 使用物品 |

### 3. 状态可视化
- ASCII地图渲染
- 敌人生成描述
- 威胁评估
- 推荐动作

## 技术要求

### 无侵入式设计
- 不影响原有游戏逻辑
- 通过包装现有函数实现
- 保留所有原有功能

### 实时性
- 状态同步更新
- 无延迟

### 错误处理
- 无效动作返回错误信息
- 边界情况处理

## 交付物

1. 修改后的 `index.html`
2. API使用示例
3. AI Agent提示词模板

---

## AI Agent使用示例

```javascript
// 1. 获取状态
const state = YinYangDAO.getState();

// 2. AI决策逻辑示例
if (state.player.hp < state.player.maxHp * 0.3) {
  // 血量低，寻找回复道具
} else if (state.enemies.some(e => e.hp < 20)) {
  // 击杀低血量敌人
} else {
  // 探索新区域
}

// 3. 执行动作
YinYangDAO.action('move', 'right');
```

## 后续扩展

- HTTP API服务器封装
- WebSocket实时通信
- 多AI对战模式
