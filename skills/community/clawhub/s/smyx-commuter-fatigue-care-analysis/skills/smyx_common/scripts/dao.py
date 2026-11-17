#!/usr/bin/env python3
"""
本地化轻量级数据库封装
使用SQLite + SQLAlchemy ORM
支持基础CRUD操作，通过继承BaseDao快速实现各表的Dao层
"""
import datetime
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Select, Table, MetaData, select, or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import text

from skills.smyx_common.scripts.config import ConstantEnum, ApiEnum

from skills.smyx_common.scripts.util import StringUtil, DatetimeUtil, FileUtil

from skills.smyx_common.scripts.base import BaseMixin, BaseDao

# 基础模型类
Base = declarative_base()

# 泛型类型，用于返回对应模型实例
T = TypeVar('T', bound=Base)

meta = MetaData()

DATABASE_URL = ApiEnum.DATABASE_URL


class BaseModelMixin(BaseMixin):

    @classmethod
    def load(cls, source: dict):
        """
        获取源枚举
        :param source: 源
        :return: User
        """
        column_names = cls.__table__.columns.keys()
        user_dict = {k: source.get(StringUtil.snake_to_camel(k)) for k in column_names}
        user_dict["create_time"] = DatetimeUtil.parse(user_dict["create_time"])
        user_dict["update_time"] = DatetimeUtil.parse(user_dict["update_time"])
        model = cls(**user_dict)
        return model


class Dao(BaseDao):
    """
    基础Dao类，提供通用的CRUD操作
    子类只需配置__model__和__tablename__即可使用
    """
    __model__: Type[T] = None  # 对应的模型类，子类必须配置
    __tablename__: str = None  # 表名，子类必须配置

    def get_db_path(self, db_path):
        """解析数据库文件路径，确保使用工作区共享的 data 目录。

        🔴 核心规则（Agent 感知，自动适配子 Agent）：
        - 自动检测当前运行在 Main Agent 还是子 Agent
        - 子 Agent 使用自己独立的工作区 data 目录，不污染 Main Agent
        - 只要路径包含 'skills/{任何技能名}/' → 强制重定向到 Agent 根 data 目录
        - 相对路径 → 强制解析到 Agent 根 data 目录
        - 绝对禁止在任何技能目录下创建私有数据库
        - 自动清洗文件名中的技能名称标识

        Returns:
            当前 Agent 工作区 data 目录下的绝对路径
        """
        import os

        # 第一步：使用 AgentContextUtil 检测当前 Agent 的工作区
        # 自动适配 Main Agent 和子 Agent 的不同工作区结构
        from .util import AgentContextUtil
        agent_context = AgentContextUtil.detect_current_agent_workspace()
        workspace = agent_context["workspace_root"]
        
        # 当前脚本路径（用于技能名称提取）
        current_file = os.path.abspath(__file__)
        
        # 路径检测标记
        skills_marker = os.sep + "skills" + os.sep  # 形如: /skills/
        
        # 如果是子 Agent，额外记录日志（便于调试）
        if not agent_context["is_main_agent"]:
            print(f"[smyx_common] 检测到子 Agent 上下文: {agent_context['agent_id']}")
            print(f"[smyx_common] 使用独立工作区: {workspace}")

        # 第二步：确保工作区路径正确（防呆校验）
        if not os.path.exists(workspace) or not os.path.isdir(workspace):
            raise RuntimeError(f"无法定位工作区目录: {workspace}")

        # 第三步：工作区共享 data 目录（唯一正确位置）
        shared_data_dir = os.path.join(workspace, "data")
        FileUtil.mkdir(shared_data_dir)

        # 第四步：检测当前技能名称
        skills_dir = os.path.join(workspace, "skills")
        current_skill_name = None
        if current_file.startswith(skills_dir + os.sep):
            # 提取当前技能名称
            relative = current_file[len(skills_dir):].strip(os.sep)
            parts = relative.split(os.sep)
            if len(parts) >= 1:
                current_skill_name = parts[0]  # 例如: "smyx_common", "smyx_payment"
        
        # 第五步：提取并清洗文件名（去掉技能名称标识）
        db_filename = os.path.basename(db_path)
        
        if current_skill_name and current_skill_name in db_filename:
            # 自动清洗文件名中的技能名称
            name_without_ext = os.path.splitext(db_filename)[0]
            ext = os.path.splitext(db_filename)[1]
            
            cleaned_name = name_without_ext.replace(current_skill_name, "")
            while "__" in cleaned_name:
                cleaned_name = cleaned_name.replace("__", "_")
            cleaned_name = cleaned_name.strip("_")
            
            if not cleaned_name:
                cleaned_name = "shared"
            
            db_filename = cleaned_name + ext
        
        # 第六步：路径重定向判断（通用逻辑，不依赖工作区名称）
        # 🔴 默认必须重定向，只有明确在根 data 目录下才不重定向
        must_redirect = True
        expected_prefix = os.path.join(workspace, "data", "")  # 形如: /xxx/workspace/data/
        
        if os.path.isabs(db_path):
            # ✅ 唯一例外：明确在工作区根 data 目录下
            if db_path.startswith(expected_prefix):
                must_redirect = False
            # 其他所有绝对路径都强制重定向（包括 /tmp/ 等外部路径）
        # 相对路径 → 必须重定向
        # 任何技能目录下的路径 → 必须重定向（在文件名清洗时已经处理）
        
        # 执行重定向
        if must_redirect:
            final_path = os.path.join(shared_data_dir, db_filename)
        else:
            final_path = db_path
        
        # 第七步：最后二次防护：即使路径正确，也要确保文件名不包含技能名称
        if current_skill_name and current_skill_name in os.path.basename(final_path):
            final_name = os.path.basename(final_path).replace(current_skill_name, "").strip("_")
            if not final_name or final_name == ".db":
                final_name = "shared.db"
            elif not final_name.endswith(".db"):
                final_name = final_name + ".db"
            final_path = os.path.join(shared_data_dir, final_name)

        # 第八步：最终校验 - 确保最终路径正确
        if not final_path.startswith(expected_prefix):
            raise RuntimeError(
                f"数据库路径强制校验失败！\n"
                f"  预期前缀: {expected_prefix}\n"
                f"  实际路径: {final_path}\n"
                f"  禁止在工作区 data 目录以外创建数据库！"
            )

        return final_path

    def __init__(self, db_path: str = None):
        """
        初始化Dao
        :param db_path: SQLite数据库文件路径
        """

        # 无论传入什么路径，都强制解析到工作区共享 data 目录
        # 确保：任何技能、任何启动目录、任何传入路径，都使用同一个共享数据库
        if not db_path:
            db_path = "smyx-common-claw.db"
        
        # 关键：强制解析所有路径，禁止绕过工作区共享机制
        db_path = self.get_db_path(db_path)

        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)

        # 创建会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # 初始化表结构
        self._create_tables()
        self._alter_tables()

    def _create_tables(self) -> None:
        """创建所有表结构"""
        Base.metadata.create_all(bind=self.engine)

    def _alter_tables(self) -> None:
        """兼容升级已有 SQLite 表结构。

        Base.metadata.create_all 只会创建不存在的表，不会给已存在的表自动补充新增字段。
        旧版本本地库中的 sys_user 表可能缺少 ORM 已使用的字段（如 realname），
        因此在 DB 初始化连接后主动检查并补齐缺失字段，避免查询时报
        sqlite3.OperationalError: no such column。
        """
        table_name = "sys_user"
        required_columns = {
            "source_id": "VARCHAR(32)",
            "realname": "VARCHAR(200)",
        }

        with self.engine.begin() as connection:
            existing_columns = {
                row[1] for row in connection.execute(text(f"PRAGMA table_info({table_name})"))
            }

            for column_name, column_type in required_columns.items():
                if column_name not in existing_columns:
                    connection.execute(
                        text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                    )

    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()

    def save(self, model) -> T:
        """
        创建新记录
        :param kwargs: 字段键值对
        :return: 创建的模型实例
        """

        try:
            return self.add(
                model
            )

        except Exception as e:
            updated = self.update(
                model
            )
            if updated:
                return updated

            username = getattr(model, "username", None)
            if username:
                column_names = self.__model__.__table__.columns.keys()
                update_data = {key: getattr(model, key) for key in column_names if key != "username"}
                return self.update_by_username(username, **update_data)

            return None

    def add(self, model) -> T:
        """
        创建新记录
        :param kwargs: 字段键值对
        :return: 创建的模型实例
        """
        session = self.get_session()
        try:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model
        finally:
            session.close()

    def create(self, **kwargs) -> T:
        """
        创建新记录
        :param kwargs: 字段键值对
        :return: 创建的模型实例
        """
        instance = self.__model__(**kwargs)
        return self.add(instance)

    def get_by_id(self, record_id: int) -> Optional[T]:
        """
        根据ID查询记录
        :param record_id: 记录ID
        :return: 模型实例或None
        """
        session = self.get_session()
        try:
            return session.query(self.__model__).filter(self.__model__.id == record_id).first()
        finally:
            session.close()

    def get_by_username(self, username: str) -> Optional[T]:
        """
        根据ID查询记录
        :param record_id: 记录ID
        :return: 模型实例或None
        """
        session = self.get_session()
        try:
            or_(
                self.__model__.del_flag == 0,
                self.__model__.del_flag.is_(None)  # 关键：使用 .is_(None) 来判断 SQL 的 NULL
            )
            return session.query(self.__model__).filter(
                or_(
                    self.__model__.username == username,
                    self.__model__.realname == username
                    # 关键：使用 .is_(None) 来判断 SQL 的 NULL
                ),
                or_(
                    self.__model__.del_flag == 0,
                    self.__model__.del_flag.is_(None)
                    # 关键：使用 .is_(None) 来判断 SQL 的 NULL
                )).first()
        finally:
            session.close()

    def list(self, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[T]:
        """
        查询记录列表
        :param filters: 过滤条件字典，如{"name": "张三", "age": 18}
        :param limit: 最大返回数量
        :param offset: 偏移量
        :return: 模型实例列表
        """
        session = self.get_session()
        try:
            query = session.query(self.__model__)
            # .where(self.__model__.id != 2, self.__model__.id == 1))

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.__model__, key) == value)

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            session.close()

    def update(self, model) -> Optional[T]:
        """
        更新记录
        :param record_id: 记录ID
        :param kwargs: 要更新的字段键值对
        :return: 更新后的模型实例或None
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.id == model.id).first()
            if not instance:
                return None

            column_names = self.__model__.__table__.columns.keys()

            for key in column_names:
                value = getattr(model, key)
                setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def modify(self, record_id: int, **kwargs) -> Optional[T]:
        """
        更新记录
        :param record_id: 记录ID
        :param kwargs: 要更新的字段键值对
        :return: 更新后的模型实例或None
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.id == record_id).first()
            if not instance:
                return None

            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def update_by_username(self, username: str, **kwargs) -> Optional[T]:
        """
        更新记录
        :param username: 记录ID
        :param kwargs: 要更新的字段键值对
        :return: 更新后的模型实例或None
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(
                or_(
                    self.__model__.username == username,
                    self.__model__.realname == username
                    # 关键：使用 .is_(None) 来判断 SQL 的 NULL
                )).first()
            if not instance:
                return None

            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, record_id: int) -> bool:
        """
        删除记录
        :param record_id: 记录ID
        :return: 删除成功返回True，失败返回False
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.id == record_id).first()
            if not instance:
                return False

            session.delete(instance)
            session.commit()
            return True
        finally:
            session.close()

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计记录数量
        :param filters: 过滤条件字典
        :return: 记录数量
        """
        session = self.get_session()
        try:
            query = session.query(func.count(self.__model__.id))

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.__model__, key) == value)

            return query.scalar()
        finally:
            session.close()


class User(Base, BaseModelMixin):
    """用户模型"""
    __tablename__ = "sys_user"

    id = Column(String(32), primary_key=True, index=True)
    source_id = Column(String(32), comment="源头id")
    username = Column(String(100), unique=True, index=True, nullable=False, comment="用户名")
    realname = Column(String(200), unique=True, index=True, comment="用户真名")
    email = Column(String(45), unique=True, index=True, comment="邮箱")
    birthday = Column(DateTime, unique=True, index=True, comment="邮箱")
    sex = Column(Integer, comment="性别")
    age = Column(Integer, comment="年龄")
    token = Column(String(500), comment="token")
    open_token = Column(String(1000), comment="开放token")
    source = Column(String(50), comment="token")
    del_flag = Column(Integer, comment="是否删除", default=0)
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    SourceEnum = ConstantEnum.SourceEnum


class UserDao(Dao):
    """用户Dao，继承BaseDao即可拥有所有基础CRUD功能"""
    __model__ = User
    __tablename__ = "users"

    def get_first_default_user(self, prefix: str = "User_", username_length: int = 11) -> Optional[User]:
        """查询第一个系统自动分配的默认用户。

        默认用户名规则：以 ``User_`` 开头且总长度为 11，例如 ``User_ab12cd``。
        优先复用最早创建的未删除记录，保证未显式传入 open-id 时始终使用同一个缺省用户。
        """
        session = self.get_session()
        try:
            return session.query(self.__model__).filter(
                self.__model__.username.like(f"{prefix}%"),
                func.length(self.__model__.username) == username_length,
                or_(
                    self.__model__.del_flag == 0,
                    self.__model__.del_flag.is_(None)
                )
            ).order_by(
                self.__model__.create_time.asc(),
                self.__model__.id.asc()
            ).first()
        finally:
            session.close()


if __name__ == "__main__":
    pass
