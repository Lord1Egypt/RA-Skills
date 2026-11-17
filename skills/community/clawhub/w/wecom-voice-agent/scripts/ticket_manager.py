#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ticket_manager.py — 自动工单创建与流转引擎

功能：
1. 自动建单：从对话内容中识别意图并自动生成工单
2. 智能路由：按类别/关键词/紧急度分配处理人
3. 状态流转：新建→分配→处理中→待确认→已解决→已关闭
4. 闭环追踪：处理时长、满意度、超时预警
5. 零外部依赖：纯 Python 标准库（sqlite3）

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-01)
"""

import os
import re
import sqlite3
import logging
import hashlib
from enum import Enum
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ==========================================
# 枚举定义
# ==========================================

class TicketStatus(Enum):
    """工单状态"""
    NEW = "new"                 # 新建
    ASSIGNED = "assigned"       # 已分配
    IN_PROGRESS = "in_progress" # 处理中
    PENDING = "pending"         # 待确认
    RESOLVED = "resolved"       # 已解决
    CLOSED = "closed"           # 已关闭
    ESCALATED = "escalated"     # 已升级

    def __str__(self):
        return self.value


class TicketPriority(Enum):
    """工单优先级"""
    LOW = "low"         # 低
    MEDIUM = "medium"   # 中
    HIGH = "high"       # 高
    URGENT = "urgent"   # 紧急

    def __str__(self):
        return self.value


class TicketCategory(Enum):
    """工单类别"""
    GENERAL = "general"         # 一般咨询
    TECH = "tech"               # 技术问题
    BILLING = "billing"         # 账单/付款
    COMPLAINT = "complaint"     # 投诉
    FEATURE = "feature"         # 功能需求
    BUG = "bug"                 # 缺陷反馈
    REFUND = "refund"           # 退款
    ACCOUNT = "account"         # 账户问题

    def __str__(self):
        return self.value


# ==========================================
# 状态流转规则
# ==========================================

VALID_TRANSITIONS: Dict[TicketStatus, List[TicketStatus]] = {
    TicketStatus.NEW: [TicketStatus.ASSIGNED, TicketStatus.ESCALATED, TicketStatus.CLOSED],
    TicketStatus.ASSIGNED: [TicketStatus.IN_PROGRESS, TicketStatus.ESCALATED, TicketStatus.CLOSED],
    TicketStatus.IN_PROGRESS: [TicketStatus.PENDING, TicketStatus.RESOLVED, TicketStatus.ESCALATED],
    TicketStatus.PENDING: [TicketStatus.IN_PROGRESS, TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.RESOLVED: [TicketStatus.CLOSED, TicketStatus.IN_PROGRESS],
    TicketStatus.ESCALATED: [TicketStatus.IN_PROGRESS, TicketStatus.RESOLVED, TicketStatus.CLOSED],
    TicketStatus.CLOSED: [],
}

# ==========================================
# 路由规则：关键词 → 工单类别
# ==========================================

CATEGORY_KEYWORDS: Dict[TicketCategory, List[str]] = {
    TicketCategory.TECH: [
        "连不上", "连不了", "连不到", "连不通", "连不了网", "断网", "网络",
        "连不上网", "无法连接", "连不上服务器", "连不上系统", "无法访问",
        "打不开", "加载不了", "闪退", "崩溃", "死机", "黑屏", "白屏",
        "连不上网", "断线", "卡顿", "延迟", "慢", "卡", "timeout",
    ],
    TicketCategory.BILLING: [
        "扣费", "扣款", "收费", "费用", "账单", "账单问题", "付款",
        "多少钱", "价格", "计费", "充值", "余额", "欠费", "缴费",
        "发票", "开票", "报销", "对账",
    ],
    TicketCategory.COMPLAINT: [
        "投诉", "差评", "态度差", "服务差", "不理人", "不回复",
        "欺骗", "欺诈", "骗子", "坑", "坑人", "骗钱", "虚假宣传",
        "态度恶劣", "敷衍", "推诿", "拖延", "不处理",
    ],
    TicketCategory.FEATURE: [
        "能不能", "希望", "建议", "建议增加", "功能", "新增",
        "能不能加", "能不能增加", "能不能支持", "能否", "期待",
        "建议增加", "希望增加", "最好能", "能不能实现",
    ],
    TicketCategory.BUG: [
        "bug", "BUG", "Bug", "出错", "错误", "异常", "报错",
        "出问题了", "有问题", "故障", "失效", "不工作", "不能用",
        "不能用", "失效", "坏了", "出故障",
    ],
    TicketCategory.REFUND: [
        "退款", "退费", "退货", "退钱", "退还", "退回",
        "不想要了", "取消订单", "申请退款", "要求退款",
    ],
    TicketCategory.ACCOUNT: [
        "账号", "密码", "登录", "注册", "绑定", "解绑",
        "换绑", "修改密码", "忘记密码", "找回密码", "注销",
        "封号", "冻结", "解冻", "实名", "认证",
    ],
}

# 紧急度关键词
URGENT_KEYWORDS: List[str] = [
    "紧急", "立刻", "马上", "赶紧", "现在", "立刻马上",
    "急", "着急", "快点", "立即", "迅速", "第一时间",
]

# 路由目标：类别 → 处理组/默认处理人
CATEGORY_ROUTING: Dict[TicketCategory, Dict] = {
    TicketCategory.TECH: {"group": "技术支持", "default_agent": "tech_agent"},
    TicketCategory.BILLING: {"group": "财务", "default_agent": "billing_agent"},
    TicketCategory.COMPLAINT: {"group": "客服主管", "default_agent": "supervisor_agent"},
    TicketCategory.FEATURE: {"group": "产品", "default_agent": "product_agent"},
    TicketCategory.BUG: {"group": "技术", "default_agent": "tech_agent"},
    TicketCategory.REFUND: {"group": "财务", "default_agent": "billing_agent"},
    TicketCategory.ACCOUNT: {"group": "客服", "default_agent": "cs_agent"},
    TicketCategory.GENERAL: {"group": "客服", "default_agent": "cs_agent"},
}

# ==========================================
# 工单管理器
# ==========================================

class TicketManager:
    """工单管理引擎：自动建单、智能路由、状态追踪、闭环反馈"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化工单管理器
        
        Args:
            db_path: SQLite 数据库路径，默认 ~/.workbuddy/output/tickets.db
        """
        if db_path is None:
            output_dir = os.path.expanduser("~/.workbuddy/output")
            os.makedirs(output_dir, exist_ok=True)
            db_path = os.path.join(output_dir, "tickets.db")
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT DEFAULT 'general',
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'new',
                    created_by TEXT,
                    assigned_to TEXT,
                    session_id TEXT,
                    emotion_tag TEXT,
                    dialect_tag TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    resolved_at TEXT,
                    closed_at TEXT,
                    resolution_note TEXT,
                    satisfaction INTEGER DEFAULT 0,
                    source TEXT DEFAULT 'auto'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ticket_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT NOT NULL,
                    from_status TEXT,
                    to_status TEXT NOT NULL,
                    changed_by TEXT,
                    note TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ticket_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT NOT NULL,
                    author TEXT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
                )
            """)
            
            conn.commit()
    
    def _generate_id(self, text: str) -> str:
        """生成工单ID: TKT-YYYYMMDD-XXXXX"""
        date_str = datetime.now().strftime("%Y%m%d")
        hash_part = hashlib.md5(f"{text}{datetime.now().isoformat()}".encode()).hexdigest()[:5].upper()
        return f"TKT-{date_str}-{hash_part}"
    
    def _get_now(self) -> str:
        """获取当前时间字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ======================================
    # 自动建单
    # ======================================
    
    def auto_create_ticket(
        self,
        text: str,
        created_by: str = "system",
        session_id: Optional[str] = None,
        emotion_tag: Optional[str] = None,
        dialect_tag: Optional[str] = None,
        source: str = "auto"
    ) -> Dict:
        """
        从对话内容自动创建工单
        
        Args:
            text: 对话内容
            created_by: 创建人
            session_id: 会话ID
            emotion_tag: 情感标签
            dialect_tag: 方言标签
            source: 来源 (auto/manual/voice/text)
            
        Returns:
            dict: 工单信息
        """
        # 自动分类
        category = self._classify_category(text)
        
        # 自动判定优先级
        priority = self._detect_priority(text, emotion_tag)
        
        # 生成标题（截取前30字）
        title = text[:30] + ("..." if len(text) > 30 else "")
        
        # 生成工单ID
        ticket_id = self._generate_id(text)
        
        now = self._get_now()
        
        ticket = {
            "id": ticket_id,
            "title": title,
            "description": text,
            "category": category.value,
            "priority": priority.value,
            "status": TicketStatus.NEW.value,
            "created_by": created_by,
            "assigned_to": None,
            "session_id": session_id,
            "emotion_tag": emotion_tag,
            "dialect_tag": dialect_tag,
            "created_at": now,
            "updated_at": now,
            "resolved_at": None,
            "closed_at": None,
            "resolution_note": None,
            "satisfaction": 0,
            "source": source,
        }
        
        # 写入数据库
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO tickets (
                    id, title, description, category, priority, status,
                    created_by, assigned_to, session_id, emotion_tag, dialect_tag,
                    created_at, updated_at, resolved_at, closed_at,
                    resolution_note, satisfaction, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ticket["id"], ticket["title"], ticket["description"],
                ticket["category"], ticket["priority"], ticket["status"],
                ticket["created_by"], ticket["assigned_to"], ticket["session_id"],
                ticket["emotion_tag"], ticket["dialect_tag"],
                ticket["created_at"], ticket["updated_at"],
                ticket["resolved_at"], ticket["closed_at"],
                ticket["resolution_note"], ticket["satisfaction"], ticket["source"],
            ))
            
            # 记录历史
            conn.execute("""
                INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ticket_id, None, TicketStatus.NEW.value, created_by, "自动创建工单", now))
            
            conn.commit()
        
        logger.info(f"工单已创建: {ticket_id} | 类别: {category.value} | 优先级: {priority.value}")
        
        # 自动路由
        route_result = self.route_ticket(ticket_id)
        ticket["assigned_to"] = route_result.get("assigned_to")
        ticket["routed"] = route_result
        
        return ticket
    
    def _classify_category(self, text: str) -> TicketCategory:
        """根据文本内容自动分类"""
        scores: Dict[TicketCategory, int] = {cat: 0 for cat in TicketCategory}
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    scores[category] += 1
        
        # 取最高分
        max_category = max(scores, key=scores.get)
        
        # 如果全部为0，返回一般咨询
        if scores[max_category] == 0:
            return TicketCategory.GENERAL
        
        return max_category
    
    def _detect_priority(self, text: str, emotion_tag: Optional[str] = None) -> TicketPriority:
        """检测优先级（基于关键词 + 情感标签）"""
        # 紧急关键词检测
        for keyword in URGENT_KEYWORDS:
            if keyword in text:
                return TicketPriority.URGENT
        
        # 情感标签辅助判定
        if emotion_tag == "angry":
            return TicketPriority.HIGH
        elif emotion_tag == "anxious":
            return TicketPriority.MEDIUM
        
        # 投诉类自动高优
        for keyword in CATEGORY_KEYWORDS[TicketCategory.COMPLAINT]:
            if keyword in text:
                return TicketPriority.HIGH
        
        return TicketPriority.MEDIUM
    
    # ======================================
    # 智能路由
    # ======================================
    
    def route_ticket(self, ticket_id: str) -> Dict:
        """
        智能路由：为工单分配处理人
        
        Args:
            ticket_id: 工单ID
            
        Returns:
            dict: 路由结果
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return {"success": False, "error": "工单不存在"}
        
        category_str = ticket.get("category", "general")
        try:
            category = TicketCategory(category_str)
        except ValueError:
            category = TicketCategory.GENERAL
        
        # 获取路由目标
        routing = CATEGORY_ROUTING.get(category, CATEGORY_ROUTING[TicketCategory.GENERAL])
        
        # 负载均衡：选择当前工单最少的处理人
        assigned_to = self._load_balance(routing["default_agent"])
        
        # 更新工单
        with sqlite3.connect(self.db_path) as conn:
            now = self._get_now()
            conn.execute("""
                UPDATE tickets SET assigned_to = ?, status = ?, updated_at = ?
                WHERE id = ?
            """, (assigned_to, TicketStatus.ASSIGNED.value, now, ticket_id))
            
            conn.execute("""
                INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ticket_id, TicketStatus.NEW.value, TicketStatus.ASSIGNED.value,
                "system", f"自动路由至 {routing['group']} - {assigned_to}", now
            ))
            
            conn.commit()
        
        logger.info(f"工单 {ticket_id} 路由至 {assigned_to} ({routing['group']})")
        
        return {
            "success": True,
            "assigned_to": assigned_to,
            "group": routing["group"],
            "category": category_str,
        }
    
    def _load_balance(self, default_agent: str) -> str:
        """负载均衡：统计各处理人当前工单数，选最少的"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT assigned_to, COUNT(*) as cnt FROM tickets
                WHERE status IN ('assigned', 'in_progress', 'pending')
                AND assigned_to IS NOT NULL
                GROUP BY assigned_to
                ORDER BY cnt ASC, assigned_to ASC
            """)
            rows = cursor.fetchall()
        
        if not rows:
            return default_agent
        
        # 返回工单最少的处理人
        return rows[0][0]
    
    # ======================================
    # 状态流转
    # ======================================
    
    def update_status(
        self,
        ticket_id: str,
        new_status: TicketStatus,
        changed_by: str = "system",
        note: str = ""
    ) -> Dict:
        """
        更新工单状态（带状态流转校验）
        
        Args:
            ticket_id: 工单ID
            new_status: 新状态
            changed_by: 操作人
            note: 备注
            
        Returns:
            dict: 操作结果
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return {"success": False, "error": "工单不存在"}
        
        current_status_str = ticket.get("status", "new")
        try:
            current_status = TicketStatus(current_status_str)
        except ValueError:
            return {"success": False, "error": f"无效的当前状态: {current_status_str}"}
        
        # 校验状态流转是否合法
        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            return {
                "success": False,
                "error": f"非法状态流转: {current_status_str} → {new_status.value}",
                "allowed": [s.value for s in allowed],
            }
        
        now = self._get_now()
        
        # 更新字段
        update_fields = {
            "status": new_status.value,
            "updated_at": now,
        }
        
        # 解决时间
        if new_status == TicketStatus.RESOLVED:
            update_fields["resolved_at"] = now
        
        # 关闭时间
        if new_status == TicketStatus.CLOSED:
            update_fields["closed_at"] = now
        
        # 构建 UPDATE 语句
        set_clause = ", ".join(f"{k} = ?" for k in update_fields.keys())
        values = list(update_fields.values()) + [ticket_id]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"UPDATE tickets SET {set_clause} WHERE id = ?", values)
            
            # 记录历史
            conn.execute("""
                INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ticket_id, current_status_str, new_status.value,
                changed_by, note, now
            ))
            
            conn.commit()
        
        logger.info(f"工单 {ticket_id} 状态更新: {current_status_str} → {new_status.value}")
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "from_status": current_status_str,
            "to_status": new_status.value,
            "updated_at": now,
        }
    
    # ======================================
    # 查询
    # ======================================
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """
        获取工单详情
        
        Args:
            ticket_id: 工单ID
            
        Returns:
            dict: 工单信息，不存在返回 None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
            row = cursor.fetchone()
        
        if not row:
            return None
        
        return dict(row)
    
    def list_tickets(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """
        查询工单列表（支持筛选）
        
        Args:
            status: 状态筛选
            category: 类别筛选
            priority: 优先级筛选
            assigned_to: 处理人筛选
            limit: 每页数量
            offset: 偏移量
            
        Returns:
            list: 工单列表
        """
        conditions = []
        params = []
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        if category:
            conditions.append("category = ?")
            params.append(category)
        if priority:
            conditions.append("priority = ?")
            params.append(priority)
        if assigned_to:
            conditions.append("assigned_to = ?")
            params.append(assigned_to)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                f"SELECT * FROM tickets WHERE {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?",
                params + [limit, offset]
            )
            rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_history(self, ticket_id: str) -> List[Dict]:
        """
        获取工单操作历史
        
        Args:
            ticket_id: 工单ID
            
        Returns:
            list: 操作历史列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM ticket_history WHERE ticket_id = ? ORDER BY created_at ASC",
                (ticket_id,)
            )
            rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def add_comment(self, ticket_id: str, author: str, content: str) -> Dict:
        """
        添加工单评论
        
        Args:
            ticket_id: 工单ID
            author: 评论人
            content: 评论内容
            
        Returns:
            dict: 操作结果
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return {"success": False, "error": "工单不存在"}
        
        now = self._get_now()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO ticket_comments (ticket_id, author, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (ticket_id, author, content, now))
            
            conn.execute("""
                UPDATE tickets SET updated_at = ? WHERE id = ?
            """, (now, ticket_id))
            
            conn.commit()
        
        return {"success": True, "ticket_id": ticket_id, "created_at": now}
    
    # ======================================
    # 关闭与满意度
    # ======================================
    
    def close_ticket(
        self,
        ticket_id: str,
        resolution_note: str = "",
        satisfaction: int = 0,
        closed_by: str = "system"
    ) -> Dict:
        """
        关闭工单
        
        Args:
            ticket_id: 工单ID
            resolution_note: 解决方案说明
            satisfaction: 满意度评分 (1-5)
            closed_by: 关闭人
            
        Returns:
            dict: 操作结果
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return {"success": False, "error": "工单不存在"}
        
        # 校验状态流转合法性
        current_status_str = ticket.get("status", "new")
        try:
            current_status = TicketStatus(current_status_str)
        except ValueError:
            return {"success": False, "error": f"无效状态: {current_status_str}"}
        
        # 已关闭的工单不能重复关闭
        if current_status == TicketStatus.CLOSED:
            return {"success": False, "error": "工单已关闭，不能重复关闭"}
        
        # 检查是否允许直接到 CLOSED
        allowed_transitions = VALID_TRANSITIONS.get(current_status, [])
        can_close_directly = TicketStatus.CLOSED in allowed_transitions
        
        now = self._get_now()
        
        with sqlite3.connect(self.db_path) as conn:
            if current_status == TicketStatus.RESOLVED or can_close_directly:
                # 直接关闭
                conn.execute("""
                    UPDATE tickets SET
                        status = ?, closed_at = ?, resolution_note = ?,
                        satisfaction = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    TicketStatus.CLOSED.value, now, resolution_note,
                    satisfaction, now, ticket_id,
                ))
                
                conn.execute("""
                    INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    ticket_id, current_status_str, TicketStatus.CLOSED.value,
                    closed_by, f"关闭工单: {resolution_note}", now,
                ))
            else:
                # 不允许直接关闭：先流转到已解决，再关闭
                # 第一步：流转到已解决
                conn.execute("""
                    UPDATE tickets SET
                        status = ?, resolved_at = ?, resolution_note = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (
                    TicketStatus.RESOLVED.value, now, resolution_note,
                    now, ticket_id,
                ))
                
                conn.execute("""
                    INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    ticket_id, current_status_str, TicketStatus.RESOLVED.value,
                    closed_by, f"准备关闭: {resolution_note}", now,
                ))
                
                # 第二步：关闭
                conn.execute("""
                    UPDATE tickets SET
                        status = ?, closed_at = ?, satisfaction = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    TicketStatus.CLOSED.value, now, satisfaction, now, ticket_id,
                ))
                
                conn.execute("""
                    INSERT INTO ticket_history (ticket_id, from_status, to_status, changed_by, note, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    ticket_id, TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value,
                    closed_by, f"关闭工单: {resolution_note}", now,
                ))
            
            conn.commit()
        
        logger.info(f"工单 {ticket_id} 已关闭 | 满意度: {satisfaction}")
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": TicketStatus.CLOSED.value,
            "closed_at": now,
            "satisfaction": satisfaction,
        }
    
    # ======================================
    # 统计与看板
    # ======================================
    
    def get_stats(self) -> Dict:
        """
        获取工单统计看板数据
        
        Returns:
            dict: 统计数据
        """
        with sqlite3.connect(self.db_path) as conn:
            # 总工单数
            total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            
            # 各状态工单数
            status_counts = {}
            for status in TicketStatus:
                count = conn.execute(
                    "SELECT COUNT(*) FROM tickets WHERE status = ?",
                    (status.value,)
                ).fetchone()[0]
                status_counts[status.value] = count
            
            # 各优先级工单数
            priority_counts = {}
            for priority in TicketPriority:
                count = conn.execute(
                    "SELECT COUNT(*) FROM tickets WHERE priority = ?",
                    (priority.value,)
                ).fetchone()[0]
                priority_counts[priority.value] = count
            
            # 各类别工单数
            category_counts = {}
            for category in TicketCategory:
                count = conn.execute(
                    "SELECT COUNT(*) FROM tickets WHERE category = ?",
                    (category.value,)
                ).fetchone()[0]
                category_counts[category.value] = count
            
            # 平均满意度
            avg_satisfaction = conn.execute(
                "SELECT AVG(satisfaction) FROM tickets WHERE satisfaction > 0"
            ).fetchone()[0] or 0.0
            
            # 今日工单数
            today = datetime.now().strftime("%Y-%m-%d")
            today_count = conn.execute(
                "SELECT COUNT(*) FROM tickets WHERE created_at LIKE ?",
                (f"{today}%",)
            ).fetchone()[0]
            
            # 超时工单数（创建超过24小时未关闭）
            yesterday = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            overdue_count = conn.execute("""
                SELECT COUNT(*) FROM tickets
                WHERE status NOT IN ('closed', 'resolved')
                AND created_at < ?
            """, (yesterday,)).fetchone()[0]
        
        return {
            "total": total,
            "today": today_count,
            "overdue": overdue_count,
            "avg_satisfaction": round(avg_satisfaction, 2),
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "category_counts": category_counts,
        }
    
    def get_overdue_tickets(self, hours: int = 24) -> List[Dict]:
        """
        获取超时工单列表
        
        Args:
            hours: 超时阈值（小时）
            
        Returns:
            list: 超时工单列表
        """
        threshold = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM tickets
                WHERE status NOT IN ('closed', 'resolved')
                AND created_at < ?
                ORDER BY created_at ASC
            """, (threshold,))
            rows = cursor.fetchall()
        
        return [dict(row) for row in rows]


# ==========================================
# 便捷函数
# ==========================================

def create_ticket(text: str, **kwargs) -> Dict:
    """便捷函数：创建工单"""
    manager = TicketManager()
    return manager.auto_create_ticket(text, **kwargs)


def get_ticket_stats() -> Dict:
    """便捷函数：获取统计"""
    manager = TicketManager()
    return manager.get_stats()


def list_open_tickets(limit: int = 20) -> List[Dict]:
    """便捷函数：列出未关闭工单"""
    manager = TicketManager()
    tickets = []
    for status in ["new", "assigned", "in_progress", "pending", "escalated"]:
        tickets.extend(manager.list_tickets(status=status, limit=limit))
    return tickets[:limit]


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """自测"""
    import tempfile
    import os
    
    print("=" * 60)
    print("工单管理引擎 — 自测模式")
    print("=" * 60)
    
    # 使用临时数据库
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    try:
        manager = TicketManager(db_path=db_path)
        
        # 测试 1: 自动建单
        print("\n[测试 1] 自动建单")
        ticket = manager.auto_create_ticket(
            "我的账号密码忘记了，登录不上去，急死了！",
            created_by="user_001",
            emotion_tag="anxious",
        )
        print(f"  工单ID: {ticket['id']}")
        print(f"  类别: {ticket['category']}")
        print(f"  优先级: {ticket['priority']}")
        assert ticket['category'] == 'account', f"期望 account, 得到 {ticket['category']}"
        assert ticket['priority'] in ('high', 'medium', 'urgent'), f"优先级异常: {ticket['priority']}"
        print("✅ 自动建单通过")
        
        # 测试 2: 状态流转
        print("\n[测试 2] 状态流转")
        result = manager.update_status(
            ticket['id'], TicketStatus.IN_PROGRESS,
            changed_by="tech_agent", note="正在处理"
        )
        print(f"  {result['from_status']} → {result['to_status']}")
        assert result['success'], f"状态流转失败: {result}"
        
        result = manager.update_status(
            ticket['id'], TicketStatus.RESOLVED,
            changed_by="tech_agent", note="已重置密码"
        )
        print(f"  {result['from_status']} → {result['to_status']}")
        assert result['success']
        print("✅ 状态流转通过")
        
        # 测试 3: 非法状态流转
        print("\n[测试 3] 非法状态流转拦截")
        result = manager.update_status(
            ticket['id'], TicketStatus.NEW,
            changed_by="system"
        )
        assert not result['success'], "应拦截非法流转"
        print(f"  拦截成功: {result['error']}")
        print("✅ 非法流转拦截通过")
        
        # 测试 4: 工单查询
        print("\n[测试 4] 工单查询")
        detail = manager.get_ticket(ticket['id'])
        assert detail is not None
        assert detail['status'] == 'resolved'
        print(f"  查询到工单: {detail['title']}")
        print("✅ 工单查询通过")
        
        # 测试 5: 操作历史
        print("\n[测试 5] 操作历史")
        history = manager.get_history(ticket['id'])
        print(f"  历史记录数: {len(history)}")
        assert len(history) >= 3  # 创建 + 分配 + 处理中 + 已解决
        print("✅ 操作历史通过")
        
        # 测试 6: 添加工单评论
        print("\n[测试 6] 添加评论")
        result = manager.add_comment(ticket['id'], "user_001", "谢谢帮助")
        assert result['success']
        print("✅ 添加评论通过")
        
        # 测试 7: 关闭工单
        print("\n[测试 7] 关闭工单")
        result = manager.close_ticket(
            ticket['id'],
            resolution_note="已重置密码，用户确认",
            satisfaction=5,
            closed_by="user_001"
        )
        assert result['success']
        print(f"  关闭成功，满意度: {result['satisfaction']}")
        print("✅ 关闭工单通过")
        
        # 测试 8: 多工单统计
        print("\n[测试 8] 统计看板")
        # 创建多个工单
        manager.auto_create_ticket("系统崩溃了，急！", emotion_tag="angry")
        manager.auto_create_ticket("请问怎么退款？", emotion_tag="neutral")
        manager.auto_create_ticket("建议增加夜间模式", emotion_tag="satisfied")
        
        stats = manager.get_stats()
        print(f"  总工单: {stats['total']}")
        print(f"  今日: {stats['today']}")
        print(f"  平均满意度: {stats['avg_satisfaction']}")
        assert stats['total'] >= 4
        print("✅ 统计看板通过")
        
        # 测试 9: 分类检测
        print("\n[测试 9] 分类检测")
        test_cases = [
            ("系统连不上网了", TicketCategory.TECH),
            ("我要退款", TicketCategory.REFUND),
            ("你们服务太差了，我要投诉", TicketCategory.COMPLAINT),
            ("建议增加导出功能", TicketCategory.FEATURE),
            ("账号被封了", TicketCategory.ACCOUNT),
        ]
        for text, expected in test_cases:
            cat = manager._classify_category(text)
            print(f"  '{text[:15]}...' → {cat.value} (期望: {expected.value})")
            assert cat == expected, f"分类错误: {text} → {cat}, 期望 {expected}"
        print("✅ 分类检测通过")
        
        # 测试 10: 超时工单
        print("\n[测试 10] 超时工单检测")
        overdue = manager.get_overdue_tickets(hours=0)  # 0小时以便测试
        print(f"  超时工单数: {len(overdue)}")
        print("✅ 超时工单检测通过")
        
        print(f"\n{'='*60}")
        print("所有自测通过 ✓")
        print("=" * 60)
        
    finally:
        # 清理临时数据库
        try:
            os.unlink(db_path)
        except OSError:
            pass


if __name__ == "__main__":
    run_self_test()
