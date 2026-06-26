# Design Patterns for SQLAlchemy

<repository_pattern>
## Repository Pattern

Abstracts data access logic from business logic.

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Sequence

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    """Abstract base repository."""

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[T]):
    """SQLAlchemy implementation of repository."""

    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount > 0
```
</repository_pattern>

<unit_of_work>
## Unit of Work Pattern

Manages transactions across multiple repositories.

```python
from types import TracebackType


class UnitOfWork:
    """Manages transaction lifecycle."""

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.orders = OrderRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


# Usage
async with UnitOfWork(session_factory) as uow:
    user = await uow.users.get(user_id)
    order = Order(user_id=user.id, total=100)
    await uow.orders.add(order)
    await uow.commit()
```
</unit_of_work>

<service_layer>
## Service Layer Pattern

Business logic separate from data access.

```python
class UserService:
    """Business logic for user operations."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register_user(
        self,
        email: str,
        password: str,
        name: str,
    ) -> User:
        async with self.uow:
            # Check if user exists
            existing = await self.uow.users.get_by_email(email)
            if existing:
                raise ValueError("Email already registered")

            # Create user
            user = User(email=email, name=name)
            user.set_password(password)

            await self.uow.users.add(user)
            await self.uow.commit()

            return user

    async def deactivate_user(self, user_id: int) -> User:
        async with self.uow:
            user = await self.uow.users.get(user_id)
            if not user:
                raise ValueError("User not found")

            user.is_active = False
            await self.uow.commit()

            return user
```
</service_layer>

<soft_delete>
## Soft Delete Pattern

Mark records as deleted instead of removing.

```python
from datetime import datetime
from sqlalchemy import event


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None


class User(Base, SoftDeleteMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))


# Query only non-deleted
stmt = select(User).where(User.deleted_at.is_(None))
```
</soft_delete>

<audit_log>
## Audit Log Pattern

Track changes to entities.

```python
from sqlalchemy import event
import json


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    table_name: Mapped[str] = mapped_column(String(100))
    record_id: Mapped[int] = mapped_column()
    action: Mapped[str] = mapped_column(String(10))  # INSERT, UPDATE, DELETE
    old_values: Mapped[Optional[str]] = mapped_column(Text)
    new_values: Mapped[Optional[str]] = mapped_column(Text)
    changed_by: Mapped[Optional[int]] = mapped_column()
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


def audit_listener(mapper, connection, target, action):
    """Create audit log entry."""
    log = AuditLog(
        table_name=target.__tablename__,
        record_id=target.id,
        action=action,
        new_values=json.dumps(target.to_dict(), default=str),
    )
    connection.execute(insert(AuditLog).values(log.to_dict()))


# Register listeners
@event.listens_for(User, "after_insert")
def user_after_insert(mapper, connection, target):
    audit_listener(mapper, connection, target, "INSERT")


@event.listens_for(User, "after_update")
def user_after_update(mapper, connection, target):
    audit_listener(mapper, connection, target, "UPDATE")
```
</audit_log>

<specification_pattern>
## Specification Pattern

Encapsulate query criteria.

```python
from abc import ABC, abstractmethod
from sqlalchemy import Select


class Specification(ABC):
    """Base specification for filtering."""

    @abstractmethod
    def apply(self, query: Select) -> Select:
        raise NotImplementedError

    def __and__(self, other: "Specification") -> "AndSpecification":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification") -> "OrSpecification":
        return OrSpecification(self, other)


class AndSpecification(Specification):
    def __init__(self, *specs: Specification):
        self.specs = specs

    def apply(self, query: Select) -> Select:
        for spec in self.specs:
            query = spec.apply(query)
        return query


# Concrete specifications
class ActiveUserSpec(Specification):
    def apply(self, query: Select) -> Select:
        return query.where(User.is_active == True)


class EmailDomainSpec(Specification):
    def __init__(self, domain: str):
        self.domain = domain

    def apply(self, query: Select) -> Select:
        return query.where(User.email.ilike(f"%@{self.domain}"))


# Usage
spec = ActiveUserSpec() & EmailDomainSpec("example.com")
stmt = spec.apply(select(User))
```
</specification_pattern>

<pagination>
## Pagination Helper

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    per_page: int

    @property
    def pages(self) -> int:
        return (self.total + self.per_page - 1) // self.per_page

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


async def paginate(
    session: AsyncSession,
    query: Select,
    page: int = 1,
    per_page: int = 20,
) -> Page:
    """Paginate a query."""
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await session.execute(count_query)).scalar_one()

    # Get items
    items_query = query.offset((page - 1) * per_page).limit(per_page)
    items = (await session.execute(items_query)).scalars().all()

    return Page(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


# Usage
page = await paginate(session, select(User), page=2, per_page=10)
```
</pagination>
