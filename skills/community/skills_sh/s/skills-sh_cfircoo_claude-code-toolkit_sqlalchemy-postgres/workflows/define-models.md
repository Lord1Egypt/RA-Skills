# Workflow: Define Models and Schemas

<required_reading>
Read before proceeding:
1. references/best-practices.md
2. references/patterns.md
</required_reading>

<process>
## Step 1: Understand the Entity

Before writing code, clarify:
- What data does this entity store?
- What are the relationships (one-to-many, many-to-many)?
- What fields are required vs optional?
- What fields need indexing?
- What constraints apply (unique, check)?

## Step 2: Create SQLAlchemy Model

Create `src/models/{entity}.py`:

```python
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Text, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .related_model import RelatedModel


class User(Base, TimestampMixin):
    """User model with comprehensive field examples."""

    __tablename__ = "users"

    # Primary key options
    # Option 1: Auto-increment integer
    id: Mapped[int] = mapped_column(primary_key=True)

    # Option 2: UUID (recommended for distributed systems)
    # id: Mapped[UUID] = mapped_column(
    #     PG_UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid4,
    # )

    # Required string field with constraints
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Optional string field
    name: Mapped[Optional[str]] = mapped_column(String(100))

    # Text field for longer content
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Boolean with default
    is_active: Mapped[bool] = mapped_column(default=True)

    # Enum-like string with check constraint
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
    )

    # Foreign key relationship
    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
    )

    # Relationships (lazy loading by default)
    organization: Mapped[Optional["Organization"]] = relationship(
        back_populates="users",
    )

    # One-to-many relationship
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    # Table-level constraints and indexes
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        CheckConstraint(
            "status IN ('pending', 'active', 'suspended')",
            name="ck_users_status",
        ),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
```

## Step 3: Create Pydantic Schemas

Create `src/schemas/{entity}.py`:

```python
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Base schema with common fields
class UserBase(BaseModel):
    """Base schema with shared fields."""

    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    is_active: bool = True


# Schema for creating new records
class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8)
    organization_id: Optional[int] = None


# Schema for updating records
class UserUpdate(BaseModel):
    """Schema for updating a user. All fields optional."""

    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    organization_id: Optional[int] = None


# Schema for reading from database
class UserRead(UserBase):
    """Schema for reading a user from database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    organization_id: Optional[int]
    created_at: datetime
    updated_at: datetime


# Schema with relationships
class UserWithPosts(UserRead):
    """User with related posts."""

    posts: list["PostRead"] = []


# Schema for list responses
class UserList(BaseModel):
    """Paginated list of users."""

    items: list[UserRead]
    total: int
    page: int
    per_page: int
    pages: int


# Avoid circular imports
from .post import PostRead

UserWithPosts.model_rebuild()
```

## Step 4: Define Relationships

### One-to-Many Example

```python
# Parent model (Organization)
class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # One organization has many users
    users: Mapped[list["User"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )


# Child model (User)
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
    )

    organization: Mapped[Optional["Organization"]] = relationship(
        back_populates="users",
    )
```

### Many-to-Many Example

```python
from sqlalchemy import Table, Column, ForeignKey

# Association table
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    roles: Mapped[list["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users",
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
    )
```

### Many-to-Many with Extra Data

```python
class UserRole(Base, TimestampMixin):
    """Association table with extra columns."""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    granted_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[Optional[datetime]] = mapped_column()

    # Relationships
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    role: Mapped["Role"] = relationship()
    grantor: Mapped[Optional["User"]] = relationship(foreign_keys=[granted_by])
```

## Step 5: Register Models

Update `src/models/__init__.py`:

```python
from .user import User
from .organization import Organization
from .post import Post

__all__ = ["User", "Organization", "Post"]
```

Update `src/schemas/__init__.py`:

```python
from .user import UserCreate, UserRead, UserUpdate, UserList, UserWithPosts
from .organization import OrganizationCreate, OrganizationRead

__all__ = [
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserList",
    "UserWithPosts",
    "OrganizationCreate",
    "OrganizationRead",
]
```

## Step 6: Import Models in Alembic

Update `alembic/env.py` to import all models:

```python
# Import all models so Alembic can detect them
from models import User, Organization, Post
```
</process>

<success_criteria>
Model definition is complete when:
- [ ] SQLAlchemy model uses Mapped[] type annotations
- [ ] All fields have appropriate types and constraints
- [ ] Relationships properly defined with back_populates
- [ ] Cascade rules set (especially for deletes)
- [ ] Indexes created for frequently queried columns
- [ ] Pydantic schemas created: Create, Read, Update
- [ ] Schemas use ConfigDict(from_attributes=True)
- [ ] Models imported in alembic/env.py
- [ ] Models exported in __init__.py
</success_criteria>
