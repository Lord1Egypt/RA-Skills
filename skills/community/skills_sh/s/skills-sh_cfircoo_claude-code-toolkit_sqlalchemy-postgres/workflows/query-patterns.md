# Workflow: Query Patterns and Repository

<required_reading>
Read before proceeding:
1. references/patterns.md
2. references/async-patterns.md
</required_reading>

<process>
## Step 1: Create Base Repository

Create `src/repositories/base.py`:

```python
from typing import Generic, TypeVar, Type, Optional, Sequence
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """Get multiple records with pagination."""
        result = await self.session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.id)
        )
        return result.scalars().all()

    async def create(self, obj_in: dict) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """Update a record by ID."""
        # Remove None values to avoid overwriting with NULL
        update_data = {k: v for k, v in obj_in.items() if v is not None}

        if not update_data:
            return await self.get(id)

        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.session.flush()
        return await self.get(id)

    async def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def count(self) -> int:
        """Count all records."""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, id: int) -> bool:
        """Check if record exists."""
        result = await self.session.execute(
            select(func.count())
            .select_from(self.model)
            .where(self.model.id == id)
        )
        return result.scalar_one() > 0
```

## Step 2: Create Entity Repository

Create `src/repositories/user.py`:

```python
from typing import Optional, Sequence
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_active_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Get all active users."""
        result = await self.session.execute(
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        return result.scalars().all()

    async def get_with_posts(self, id: int) -> Optional[User]:
        """Get user with eager-loaded posts."""
        result = await self.session.execute(
            select(User)
            .where(User.id == id)
            .options(selectinload(User.posts))
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        query: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Search users by name or email."""
        search_term = f"%{query}%"
        result = await self.session.execute(
            select(User)
            .where(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_organization(
        self,
        organization_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Get all users in an organization."""
        result = await self.session.execute(
            select(User)
            .where(User.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
```

## Step 3: Query Patterns

### Basic Queries

```python
from sqlalchemy import select, and_, or_, not_

# Simple select
stmt = select(User)
result = await session.execute(stmt)
users = result.scalars().all()

# Filter with where
stmt = select(User).where(User.is_active == True)

# Multiple conditions (AND)
stmt = select(User).where(
    and_(
        User.is_active == True,
        User.organization_id == org_id,
    )
)

# OR conditions
stmt = select(User).where(
    or_(
        User.name.ilike("%john%"),
        User.email.ilike("%john%"),
    )
)

# NOT
stmt = select(User).where(not_(User.is_active))

# IN clause
stmt = select(User).where(User.id.in_([1, 2, 3]))

# BETWEEN
stmt = select(User).where(User.created_at.between(start_date, end_date))

# IS NULL / IS NOT NULL
stmt = select(User).where(User.organization_id.is_(None))
stmt = select(User).where(User.organization_id.isnot(None))
```

### Ordering and Pagination

```python
from sqlalchemy import desc, asc

# Order by
stmt = select(User).order_by(User.created_at.desc())

# Multiple order by
stmt = select(User).order_by(User.name.asc(), User.id.desc())

# Pagination
stmt = select(User).offset(skip).limit(limit)

# Combined
stmt = (
    select(User)
    .where(User.is_active == True)
    .order_by(User.created_at.desc())
    .offset(skip)
    .limit(limit)
)
```

### Eager Loading (Prevent N+1)

```python
from sqlalchemy.orm import selectinload, joinedload, subqueryload

# selectinload - Separate SELECT IN query (best for collections)
stmt = select(User).options(selectinload(User.posts))

# joinedload - Single query with JOIN (best for single objects)
stmt = select(User).options(joinedload(User.organization))

# Nested eager loading
stmt = select(User).options(
    selectinload(User.posts).selectinload(Post.comments)
)

# Multiple relationships
stmt = select(User).options(
    selectinload(User.posts),
    joinedload(User.organization),
)
```

### Joins

```python
from sqlalchemy import join

# Implicit join (through relationship)
stmt = (
    select(User)
    .join(User.posts)
    .where(Post.title.ilike("%python%"))
)

# Explicit join
stmt = (
    select(User, Post)
    .join(Post, User.id == Post.author_id)
)

# Left outer join
stmt = (
    select(User, Post)
    .outerjoin(Post, User.id == Post.author_id)
)

# Select specific columns
stmt = select(User.id, User.name, Post.title).join(Post)
```

### Aggregations

```python
from sqlalchemy import func

# Count
stmt = select(func.count()).select_from(User)
result = await session.execute(stmt)
total = result.scalar_one()

# Count with filter
stmt = select(func.count()).select_from(User).where(User.is_active == True)

# Group by with aggregation
stmt = (
    select(User.organization_id, func.count(User.id).label("user_count"))
    .group_by(User.organization_id)
    .having(func.count(User.id) > 5)
)

# Multiple aggregations
stmt = select(
    func.count(User.id).label("total"),
    func.count(User.id).filter(User.is_active == True).label("active"),
)
```

### Subqueries

```python
# Subquery for filtering
active_org_subq = (
    select(Organization.id)
    .where(Organization.is_active == True)
    .scalar_subquery()
)

stmt = select(User).where(User.organization_id.in_(active_org_subq))

# Correlated subquery
post_count_subq = (
    select(func.count(Post.id))
    .where(Post.author_id == User.id)
    .correlate(User)
    .scalar_subquery()
)

stmt = select(User, post_count_subq.label("post_count"))
```

## Step 4: Use in FastAPI Routes

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from db.dependencies import DBSession
from repositories.user import UserRepository
from schemas.user import UserCreate, UserRead, UserUpdate, UserList

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repo(session: DBSession) -> UserRepository:
    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repo)]


@router.get("/", response_model=UserList)
async def list_users(
    repo: UserRepo,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    skip = (page - 1) * per_page
    users = await repo.get_multi(skip=skip, limit=per_page)
    total = await repo.count()

    return UserList(
        items=users,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, repo: UserRepo):
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user_in: UserCreate, repo: UserRepo):
    existing = await repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create(user_in.model_dump())


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_in: UserUpdate, repo: UserRepo):
    user = await repo.update(user_id, user_in.model_dump(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, repo: UserRepo):
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```
</process>

<success_criteria>
Repository is complete when:
- [ ] Base repository with generic CRUD operations
- [ ] Entity-specific repository with custom queries
- [ ] Eager loading used where appropriate
- [ ] Pagination implemented
- [ ] Search functionality added
- [ ] FastAPI routes use repository pattern
- [ ] Proper error handling (404, 400)
- [ ] Type hints throughout
</success_criteria>
