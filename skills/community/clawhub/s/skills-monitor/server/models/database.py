"""
中心化服务器 — 数据库模型 (SQLAlchemy)
=====================================
支持 SQLite（轻量部署）和 PostgreSQL（生产环境）。

核心表：
  - users           微信用户（openid 绑定）
  - agents          Agent 实例
  - user_agents     用户-Agent 绑定关系（多对多）
  - skill_reports   Agent 上报的数据（每日汇总）
  - daily_digests   每日推送摘要
"""

import os
import gzip
import json
from datetime import datetime
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ──────── 用户表（微信用户） ────────

class User(db.Model):
    """微信用户 — 通过扫码关注公众号获取 openid"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), unique=True, nullable=False, index=True)
    union_id = db.Column(db.String(64), index=True)       # 微信开放平台 unionid
    nickname = db.Column(db.String(128))
    avatar_url = db.Column(db.String(512))
    subscribe = db.Column(db.Boolean, default=True)         # 是否关注公众号
    subscribe_time = db.Column(db.DateTime)
    mp_openid = db.Column(db.String(64), index=True)        # 小程序 openid（可选）

    # 推送设置
    push_enabled = db.Column(db.Boolean, default=True)
    push_hour = db.Column(db.Integer, default=21)           # 每日推送时间（小时）

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    agents = db.relationship("UserAgent", back_populates="user", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "openid": self.openid[:8] + "***",
            "nickname": self.nickname,
            "subscribe": self.subscribe,
            "push_enabled": self.push_enabled,
            "agent_count": self.agents.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ──────── Agent 表 ────────

class Agent(db.Model):
    """Agent 实例 — 每个本地安装生成一个 agent_id + token"""
    __tablename__ = "agents"

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    token_hash = db.Column(db.String(128), nullable=False)  # SHA256(token)
    name = db.Column(db.String(128))                         # 用户可设置名称
    description = db.Column(db.String(512))

    # 状态
    last_report_at = db.Column(db.DateTime)
    last_heartbeat_at = db.Column(db.DateTime)
    total_skills = db.Column(db.Integer, default=0)
    runnable_skills = db.Column(db.Integer, default=0)
    health_score = db.Column(db.Float)

    # 系统信息
    os_info = db.Column(db.String(128))
    python_version = db.Column(db.String(32))
    monitor_version = db.Column(db.String(16))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    users = db.relationship("UserAgent", back_populates="agent", lazy="dynamic")
    reports = db.relationship("SkillReport", back_populates="agent", lazy="dynamic",
                              order_by="SkillReport.report_date.desc()")

    def to_dict(self, include_token=False):
        d = {
            "id": self.id,
            "agent_id": self.agent_id,
            "name": self.name or f"Agent-{self.agent_id[:8]}",
            "last_report_at": self.last_report_at.isoformat() if self.last_report_at else None,
            "total_skills": self.total_skills,
            "runnable_skills": self.runnable_skills,
            "health_score": self.health_score,
            "monitor_version": self.monitor_version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        return d


# ──────── 用户-Agent 绑定（多对多） ────────

class UserAgent(db.Model):
    """
    一个微信用户可以绑定多个 Agent（多个设备/环境）
    绑定时需要 agent_id + token 验证
    """
    __tablename__ = "user_agents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=False)
    bind_token = db.Column(db.String(128))    # 绑定时使用的 token（加密）
    alias = db.Column(db.String(64))           # 用户给 Agent 设的别名
    is_primary = db.Column(db.Boolean, default=False)  # 是否为主 Agent

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 唯一约束：同一用户同一 Agent 只能绑定一次
    __table_args__ = (
        db.UniqueConstraint("user_id", "agent_id", name="uq_user_agent"),
    )

    user = db.relationship("User", back_populates="agents")
    agent = db.relationship("Agent", back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "agent_id": self.agent.agent_id if self.agent else None,
            "agent_name": self.alias or (self.agent.name if self.agent else ""),
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ──────── Skill 报告数据（Agent 上报） ────────

class SkillReport(db.Model):
    """
    Agent 每日上报的数据快照
    数据可能是压缩的（gzip），根据大小自动决定
    """
    __tablename__ = "skill_reports"

    id = db.Column(db.Integer, primary_key=True)
    agent_db_id = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=False)
    agent_id_str = db.Column(db.String(64), nullable=False, index=True)  # 冗余，方便查询
    report_date = db.Column(db.Date, nullable=False, index=True)
    report_type = db.Column(db.String(32), default="daily")  # daily / diagnostic / install

    # 上报数据（JSON，可能压缩）
    data_raw = db.Column(db.LargeBinary)     # 压缩后的二进制数据
    data_json = db.Column(db.Text)            # 未压缩的 JSON 文本
    is_compressed = db.Column(db.Boolean, default=False)
    data_size_bytes = db.Column(db.Integer)   # 原始大小

    # 解析后的关键指标（方便查询，不用每次解压）
    health_score = db.Column(db.Float)
    total_runs = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float)
    active_skills = db.Column(db.Integer, default=0)
    avg_duration_ms = db.Column(db.Float)

    # 评分 Top3
    top_skills_json = db.Column(db.Text)      # JSON: [{skill_id, score, grade}]

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint("agent_db_id", "report_date", "report_type",
                            name="uq_agent_report_date_type"),
    )

    agent = db.relationship("Agent", back_populates="reports")

    def set_data(self, data: dict, compress_threshold: int = 10240):
        """
        设置报告数据，超过阈值自动 gzip 压缩
        """
        json_str = json.dumps(data, ensure_ascii=False, default=str)
        raw_bytes = json_str.encode("utf-8")
        self.data_size_bytes = len(raw_bytes)

        if len(raw_bytes) > compress_threshold:
            self.data_raw = gzip.compress(raw_bytes)
            self.data_json = None
            self.is_compressed = True
        else:
            self.data_json = json_str
            self.data_raw = None
            self.is_compressed = False

    def get_data(self) -> dict:
        """获取报告数据（自动解压）"""
        if self.is_compressed and self.data_raw:
            raw = gzip.decompress(self.data_raw)
            return json.loads(raw.decode("utf-8"))
        elif self.data_json:
            return json.loads(self.data_json)
        return {}

    def to_dict(self, include_data=False):
        d = {
            "id": self.id,
            "agent_id": self.agent_id_str,
            "report_date": self.report_date.isoformat() if self.report_date else None,
            "report_type": self.report_type,
            "health_score": self.health_score,
            "total_runs": self.total_runs,
            "success_rate": self.success_rate,
            "active_skills": self.active_skills,
            "is_compressed": self.is_compressed,
            "data_size_bytes": self.data_size_bytes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_data:
            d["data"] = self.get_data()
        return d


# ──────── 每日推送摘要 ────────

class DailyDigest(db.Model):
    """记录每日推送的结果"""
    __tablename__ = "daily_digests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    agent_db_id = db.Column(db.Integer, db.ForeignKey("agents.id"), nullable=False)
    digest_date = db.Column(db.Date, nullable=False)
    push_type = db.Column(db.String(32), default="template_msg")  # template_msg / custom_msg
    push_status = db.Column(db.String(16), default="pending")      # pending / sent / failed
    push_result = db.Column(db.Text)                                # JSON: 推送结果
    h5_url = db.Column(db.String(512))                              # H5 报告链接

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "agent_db_id", "digest_date",
                            name="uq_digest_user_agent_date"),
    )


# ──────── 初始化辅助函数 ────────

def init_db(app):
    """初始化数据库（在 Flask app 上下文中调用）"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db
