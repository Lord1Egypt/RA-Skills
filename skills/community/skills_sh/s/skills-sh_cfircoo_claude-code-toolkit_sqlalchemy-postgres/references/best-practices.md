# SQLAlchemy + Pydantic + PostgreSQL Best Practices

<security>
## Security

### Prevent SQL Injection
SQLAlchemy ORM and Core protect against SQL injection by default. **Never** use string formatting:

```python
# NEVER DO THIS
query = f"SELECT * FROM users WHERE email = '{email}'"

# ALWAYS use parameterized queries
stmt = select(User).where(User.email == email)

# Or with text()
stmt = text("SELECT * FROM users WHERE email = :email")
result = await session.execute(stmt, {"email": email})
```

### Protect Sensitive Data
```python
# Store hashed passwords
from passlib.hash import bcrypt

class User(Base):
    password_hash: Mapped[str] = mapped_column(String(255))

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.hash(password)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)
```

### Environment Variables
Never hardcode credentials:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"
```
</security>

<performance>
## Performance

### Connection Pooling
Configure pool for production:
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,          # Base connections
    max_overflow=10,      # Extra connections under load
    pool_timeout=30,      # Wait time for connection
    pool_recycle=1800,    # Recycle connections every 30 min
    pool_pre_ping=True,   # Verify connection before use
)
```

### Prevent N+1 Queries
Use eager loading:
```python
# BAD - N+1 queries
users = await session.execute(select(User))
for user in users.scalars():
    print(user.posts)  # Triggers query for each user

# GOOD - Single query with selectinload
users = await session.execute(
    select(User).options(selectinload(User.posts))
)
```

### Use Indexes
```python
class User(Base):
    email: Mapped[str] = mapped_column(String(255), index=True)

    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
    )
```

### Bulk Operations
```python
# Bulk insert
await session.execute(
    insert(User),
    [{"email": "a@a.com"}, {"email": "b@b.com"}]
)

# Bulk update
await session.execute(
    update(User)
    .where(User.is_active == False)
    .values(status="inactive")
)
```

### Select Only Needed Columns
```python
# Instead of loading full objects
stmt = select(User.id, User.name)  # Faster for large tables
```
</performance>

<transactions>
## Transaction Management

### Use Context Manager
```python
async with async_session_factory() as session:
    try:
        user = User(email="test@test.com")
        session.add(user)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

### Explicit Transactions
```python
async with session.begin():
    # All operations in this block are atomic
    session.add(user)
    session.add(order)
    # Auto-commit on exit, auto-rollback on exception
```

### Savepoints
```python
async with session.begin():
    session.add(user1)

    async with session.begin_nested():
        # Savepoint
        session.add(user2)
        # Can rollback just this part
```
</transactions>

<testing>
## Testing

### Use Separate Test Database
```python
@pytest.fixture
async def test_session():
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
```

### Transaction Rollback After Each Test
```python
@pytest.fixture
async def session(test_engine):
    async with test_engine.connect() as conn:
        await conn.begin()  # Start transaction

        async_session = async_sessionmaker(bind=conn)
        async with async_session() as session:
            yield session

        await conn.rollback()  # Rollback after test
```

### Factory Pattern for Test Data
```python
from factory import Factory, Faker
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = Faker("email")
    name = Faker("name")
    is_active = True
```
</testing>

<pydantic_integration>
## Pydantic Integration

### Schema Naming Convention
```
{Entity}Base    - Shared fields
{Entity}Create  - Fields for creation
{Entity}Update  - Optional fields for updates
{Entity}Read    - Database output
{Entity}InDB    - Internal use with sensitive data
```

### Validation
```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
```

### Computed Fields
```python
from pydantic import computed_field

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```
</pydantic_integration>

<common_mistakes>
## Common Mistakes to Avoid

1. **Forgetting `await`** on async operations
2. **Not closing sessions** - Use context managers
3. **Lazy loading in async** - Causes errors, use eager loading
4. **Mixing sync and async** - Don't use sync driver with async code
5. **N+1 queries** - Always profile with `echo=True` during dev
6. **Not using transactions** - Wrap related operations
7. **Hardcoding credentials** - Use environment variables
8. **Missing indexes** - Profile slow queries
9. **expire_on_commit=True with async** - Set to False
10. **Not handling IntegrityError** - Catch and handle duplicates
</common_mistakes>
