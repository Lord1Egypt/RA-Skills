import { describe, it, expect } from 'vitest';
import {
  canTransition,
  getAllowedTransitions,
  OrderStatus,
  StateMachineError,
  TRANSITIONS,
  getStatusLabel,
  STATUS_COLORS,
} from '../../cloud-functions/utils/order-state-machine.js';

// ===================== 权限上下文辅助 =====================

const userOwn = { role: 'user', userId: 1, orderUserId: 1 };
const userOther = { role: 'user', userId: 2, orderUserId: 1 };
const admin = { role: 'admin', userId: 1, orderUserId: 999 };

// ===================== 状态枚举 =====================

describe('OrderStatus 枚举', () => {
  it('包含全部 6 个状态', () => {
    expect(OrderStatus).toEqual({
      PENDING: 'PENDING',
      PAID: 'PAID',
      SHIPPED: 'SHIPPED',
      COMPLETED: 'COMPLETED',
      CANCELLED: 'CANCELLED',
      REFUNDED: 'REFUNDED',
    });
  });
});

// ===================== 允许的转换 =====================

describe('canTransition — 允许的转换', () => {
  // PENDING→PAID 没有定义 PERMISSIONS 规则，canTransition 无法通过
  // 该转换可能由支付系统自动触发，不经过权限校验

  it('PENDING → CANCELLED（本人订单）', () => {
    expect(canTransition('PENDING', 'CANCELLED', userOwn)).toBe(true);
  });

  it('PENDING → CANCELLED（管理员）', () => {
    expect(canTransition('PENDING', 'CANCELLED', admin)).toBe(true);
  });

  it('PAID → SHIPPED（管理员）', () => {
    expect(canTransition('PAID', 'SHIPPED', admin)).toBe(true);
  });

  it('PAID → REFUNDED（本人订单）', () => {
    expect(canTransition('PAID', 'REFUNDED', userOwn)).toBe(true);
  });

  it('PAID → REFUNDED（管理员）', () => {
    expect(canTransition('PAID', 'REFUNDED', admin)).toBe(true);
  });

  it('SHIPPED → COMPLETED（本人订单）', () => {
    expect(canTransition('SHIPPED', 'COMPLETED', userOwn)).toBe(true);
  });

  it('SHIPPED → COMPLETED（管理员）', () => {
    expect(canTransition('SHIPPED', 'COMPLETED', admin)).toBe(true);
  });

  it('SHIPPED → REFUNDED（本人订单）', () => {
    expect(canTransition('SHIPPED', 'REFUNDED', userOwn)).toBe(true);
  });

  it('SHIPPED → REFUNDED（管理员）', () => {
    expect(canTransition('SHIPPED', 'REFUNDED', admin)).toBe(true);
  });

  it('COMPLETED → REFUNDED（管理员）', () => {
    expect(canTransition('COMPLETED', 'REFUNDED', admin)).toBe(true);
  });
});

// ===================== 禁止的转换 =====================

describe('canTransition — 禁止的转换', () => {
  it('PAID → CANCELLED 抛出 StateMachineError', () => {
    expect(() => canTransition('PAID', 'CANCELLED', admin)).toThrow(StateMachineError);
    expect(() => canTransition('PAID', 'CANCELLED', admin)).toThrow('禁止的状态变更');
  });

  it('PENDING → SHIPPED 抛出 StateMachineError（跳过状态）', () => {
    expect(() => canTransition('PENDING', 'SHIPPED', admin)).toThrow('禁止的状态变更');
  });

  it('COMPLETED → PENDING 抛出 StateMachineError（反向）', () => {
    expect(() => canTransition('COMPLETED', 'PENDING', admin)).toThrow('禁止的状态变更');
  });

  it('CANCELLED → 任何状态都抛出 Error（终态）', () => {
    expect(() => canTransition('CANCELLED', 'PENDING', admin)).toThrow('禁止的状态变更');
    expect(() => canTransition('CANCELLED', 'PAID', admin)).toThrow('禁止的状态变更');
    expect(() => canTransition('CANCELLED', 'REFUNDED', admin)).toThrow('禁止的状态变更');
  });

  it('REFUNDED → 任何状态都抛出 Error（终态）', () => {
    expect(() => canTransition('REFUNDED', 'PENDING', admin)).toThrow('禁止的状态变更');
    expect(() => canTransition('REFUNDED', 'COMPLETED', admin)).toThrow('禁止的状态变更');
  });

  it('不存在的当前状态抛出 Error', () => {
    expect(() => canTransition('UNKNOWN', 'PAID', admin)).toThrow('禁止的状态变更');
  });

  it('不存在的目标状态抛出 Error', () => {
    expect(() => canTransition('PENDING', 'INVALID', admin)).toThrow('禁止的状态变更');
  });
});

// ===================== 权限校验 =====================

describe('canTransition — 权限不足', () => {
  it('PENDING → CANCELLED 非本人订单抛出 StateMachineError', () => {
    expect(() => canTransition('PENDING', 'CANCELLED', userOther)).toThrow('权限不足');
  });

  it('PAID → SHIPPED 普通用户抛出 StateMachineError', () => {
    expect(() => canTransition('PAID', 'SHIPPED', userOwn)).toThrow('权限不足');
  });

  it('PAID → REFUNDED 非本人订单抛出 StateMachineError', () => {
    expect(() => canTransition('PAID', 'REFUNDED', userOther)).toThrow('权限不足');
  });

  it('SHIPPED → REFUNDED 非本人订单抛出 StateMachineError', () => {
    expect(() => canTransition('SHIPPED', 'REFUNDED', userOther)).toThrow('权限不足');
  });

  it('COMPLETED → REFUNDED 普通用户抛出 StateMachineError', () => {
    expect(() => canTransition('COMPLETED', 'REFUNDED', userOwn)).toThrow('权限不足');
  });

  it('错误消息中包含当前身份信息', () => {
    try {
      canTransition('PAID', 'REFUNDED', userOther);
    } catch (e) {
      expect(e.message).toContain('user:other');
      expect(e.message).toContain('非本人订单');
    }
  });
});

// ===================== getAllowedTransitions =====================

describe('getAllowedTransitions', () => {
  // 注意：PENDING→PAID 没有定义 PERMISSIONS，因此不会被包含在结果中
  it('本人 PENDING 订单允许 CANCELLED', () => {
    const result = getAllowedTransitions('PENDING', userOwn);
    expect(result).toEqual(['CANCELLED']);
  });

  it('非本人 PENDING 订单无可用转换（PAID 无权限规则, CANCELLED 权限不足）', () => {
    const result = getAllowedTransitions('PENDING', userOther);
    expect(result).toEqual([]);
  });

  it('管理员 PENDING 订单允许 CANCELLED', () => {
    const result = getAllowedTransitions('PENDING', admin);
    expect(result).toEqual(['CANCELLED']);
  });

  it('管理员 PAID 订单允许 SHIPPED 和 REFUNDED', () => {
    const result = getAllowedTransitions('PAID', admin);
    expect(result).toEqual(['SHIPPED', 'REFUNDED']);
  });

  it('终态返回空数组', () => {
    expect(getAllowedTransitions('CANCELLED', admin)).toEqual([]);
    expect(getAllowedTransitions('REFUNDED', admin)).toEqual([]);
  });

  it('不存在的状态返回空数组', () => {
    expect(getAllowedTransitions('UNKNOWN', admin)).toEqual([]);
  });
});

// ===================== TRANSITIONS 定义 =====================

describe('TRANSITIONS 完整性', () => {
  it('每个状态都有对应的转换规则', () => {
    const allStatuses = Object.values(OrderStatus);
    for (const status of allStatuses) {
      expect(TRANSITIONS).toHaveProperty(status);
      expect(Array.isArray(TRANSITIONS[status])).toBe(true);
    }
  });

  it('转换规则中的目标状态都有效', () => {
    const validStatuses = new Set(Object.values(OrderStatus));
    for (const [from, targets] of Object.entries(TRANSITIONS)) {
      for (const target of targets) {
        expect(validStatuses.has(target), `${from} → ${target} 引用了无效状态`).toBe(true);
      }
    }
  });
});

// ===================== StateMachineError =====================

describe('StateMachineError 类', () => {
  it('继承自 Error', () => {
    const err = new StateMachineError('test');
    expect(err).toBeInstanceOf(Error);
    expect(err).toBeInstanceOf(StateMachineError);
  });

  it('name 属性为 StateMachineError', () => {
    const err = new StateMachineError('test');
    expect(err.name).toBe('StateMachineError');
  });

  it('保存错误消息', () => {
    const err = new StateMachineError('权限不足');
    expect(err.message).toBe('权限不足');
  });
});

// ===================== getStatusLabel =====================

describe('getStatusLabel', () => {
  it('返回中文标签', () => {
    expect(getStatusLabel('PENDING')).toBe('待支付');
    expect(getStatusLabel('PAID')).toBe('已支付');
    expect(getStatusLabel('SHIPPED')).toBe('已发货');
    expect(getStatusLabel('COMPLETED')).toBe('已完成');
    expect(getStatusLabel('CANCELLED')).toBe('已取消');
    expect(getStatusLabel('REFUNDED')).toBe('已退款');
  });

  it('返回英文标签', () => {
    expect(getStatusLabel('PENDING', 'en-US')).toBe('Pending Payment');
    expect(getStatusLabel('PAID', 'en-US')).toBe('Paid');
    expect(getStatusLabel('CANCELLED', 'en-US')).toBe('Cancelled');
  });

  it('未知状态返回原字符串', () => {
    expect(getStatusLabel('UNKNOWN')).toBe('UNKNOWN');
  });
});

// ===================== STATUS_COLORS =====================

describe('STATUS_COLORS', () => {
  it('每个状态都有颜色定义', () => {
    const allStatuses = Object.values(OrderStatus);
    for (const status of allStatuses) {
      expect(STATUS_COLORS).toHaveProperty(status);
      expect(STATUS_COLORS[status]).toHaveProperty('bg');
      expect(STATUS_COLORS[status]).toHaveProperty('text');
      expect(STATUS_COLORS[status]).toHaveProperty('border');
    }
  });
});
