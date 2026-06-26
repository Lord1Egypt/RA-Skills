# Async SQLAlchemy Patterns

<fastapi_integration>
## FastAPI Integration

### Session Dependency
```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# Type alias for cleaner signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]


# Usage in routes
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: DBSession):
    user = await db.execute(select(User).where(User.id == user_id))
    return user.scalar_one_or_none()
```

### Repository Dependency
```python
def get_user_repo(session: DBSession) -> UserRepository:
    return UserRepository(session)

UserRepo = Annotated[UserRepository, Depends(get_user_repo)]


@router.get("/users")
async def list_users(repo: UserRepo):
    return await repo.get_multi()
```

### Lifespan Event for Connection
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify connection
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    # Shutdown: dispose engine
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```
</fastapi_integration>

<async_session_patterns>
## Async Session Patterns

### Context Manager Pattern
```python
async def create_user(email: str) -> User:
    async with async_session_factory() as session:
        user = User(email=email)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
```

### Manual Transaction Control
```python
async def transfer_funds(from_id: int, to_id: int, amount: float):
    async with async_session_factory() as session:
        async with session.begin():
            # Both operations in same transaction
            from_account = await session.get(Account, from_id)
            to_account = await session.get(Account, to_id)

            if from_account.balance < amount:
                raise ValueError("Insufficient funds")

            from_account.balance -= amount
            to_account.balance += amount
            # Auto-commit on exit
```

### Nested Transactions (Savepoints)
```python
async def complex_operation():
    async with async_session_factory() as session:
        async with session.begin():
            session.add(user)

            try:
                async with session.begin_nested():
                    session.add(risky_operation)
            except Exception:
                # Only risky_operation rolled back
                pass

            # user still committed
```
</async_session_patterns>

<eager_loading_async>
## Eager Loading in Async

**Critical**: Lazy loading doesn't work with async. Always use eager loading.

### selectinload (Best for Collections)
```python
# Loads related collection with SELECT ... IN (...)
stmt = select(User).options(selectinload(User.posts))
result = await session.execute(stmt)
users = result.scalars().all()

for user in users:
    print(user.posts)  # Already loaded, no additional query
```

### joinedload (Best for Single Relations)
```python
# Loads related object with JOIN
stmt = select(User).options(joinedload(User.organization))
result = await session.execute(stmt)
users = result.scalars().unique().all()  # Note: unique() needed with joins
```

### Nested Eager Loading
```python
stmt = select(User).options(
    selectinload(User.posts).selectinload(Post.comments),
    joinedload(User.organization),
)
```

### contains_eager (With Explicit Join)
```python
from sqlalchemy.orm import contains_eager

stmt = (
    select(User)
    .join(User.posts)
    .where(Post.is_published == True)
    .options(contains_eager(User.posts))
)
```
</eager_loading_async>

<concurrent_operations>
## Concurrent Database Operations

### Parallel Queries
```python
import asyncio

async def get_dashboard_data(user_id: int):
    async with async_session_factory() as session:
        # Run queries in parallel
        user_task = session.execute(
            select(User).where(User.id == user_id)
        )
        posts_task = session.execute(
            select(Post).where(Post.author_id == user_id)
        )
        stats_task = session.execute(
            select(func.count(Post.id))
            .where(Post.author_id == user_id)
        )

        user_result, posts_result, stats_result = await asyncio.gather(
            user_task, posts_task, stats_task
        )

        return {
            "user": user_result.scalar_one(),
            "posts": posts_result.scalars().all(),
            "post_count": stats_result.scalar_one(),
        }
```

### Batch Processing
```python
async def process_users_batch(user_ids: list[int]):
    async with async_session_factory() as session:
        # Process in batches to avoid memory issues
        batch_size = 100

        for i in range(0, len(user_ids), batch_size):
            batch = user_ids[i:i + batch_size]

            result = await session.execute(
                select(User).where(User.id.in_(batch))
            )
            users = result.scalars().all()

            for user in users:
                await process_user(user)

            await session.commit()
```
</concurrent_operations>

<connection_pool>
## Connection Pool Management

### Configure for Production
```python
engine = create_async_engine(
    DATABASE_URL,
    # Pool configuration
    pool_size=5,           # Maintain 5 connections
    max_overflow=10,       # Allow up to 15 total (5 + 10)
    pool_timeout=30,       # Wait 30s for available connection
    pool_recycle=1800,     # Recycle connections every 30 min
    pool_pre_ping=True,    # Check connection before use

    # Performance options
    echo=False,            # Disable SQL logging in production
    future=True,           # Use 2.0 style
)
```

### Health Check Endpoint
```python
@router.get("/health/db")
async def health_check(db: DBSession):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Graceful Shutdown
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Properly close all connections
    await engine.dispose()
```
</connection_pool>

<error_handling>
## Async Error Handling

### Handle Database Errors
```python
from sqlalchemy.exc import IntegrityError, OperationalError
from fastapi import HTTPException

async def create_user(user_data: UserCreate, db: DBSession):
    try:
        user = User(**user_data.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(400, "Email already exists")
        raise HTTPException(400, "Database constraint violation")

    except OperationalError as e:
        await db.rollback()
        raise HTTPException(503, "Database unavailable")
```

### Retry Pattern
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
async def resilient_query(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```
</error_handling>

<testing_async>
## Testing Async Code

### Pytest Fixture
```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def async_session():
    engine = create_async_engine(
        "postgresql+asyncpg://localhost/test_db",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_sessionmaker(engine)() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={"email": "test@test.com", "name": "Test"},
    )
    assert response.status_code == 201
```
</testing_async>
