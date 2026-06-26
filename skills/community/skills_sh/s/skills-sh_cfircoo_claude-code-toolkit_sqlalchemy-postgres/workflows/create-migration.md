# Workflow: Create and Manage Migrations

<required_reading>
Read before proceeding:
1. references/best-practices.md
</required_reading>

<process>
## Step 1: Generate Migration

After modifying models, generate a migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "descriptive_message"

# Examples:
alembic revision --autogenerate -m "create_users_table"
alembic revision --autogenerate -m "add_email_to_users"
alembic revision --autogenerate -m "create_posts_and_comments"
```

## Step 2: Review Generated Migration

**ALWAYS review the generated migration file before applying!**

Check `alembic/versions/{revision}_descriptive_message.py`:

```python
"""create_users_table

Revision ID: abc123def456
Revises:
Create Date: 2024-01-15 10:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'abc123def456'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
```

## Step 3: Apply Migration

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade abc123def456

# Apply next migration only
alembic upgrade +1
```

## Step 4: Common Migration Operations

### Adding a Column

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone')
```

### Adding Non-Nullable Column (with data)

```python
def upgrade() -> None:
    # Add as nullable first
    op.add_column('users', sa.Column('status', sa.String(20), nullable=True))

    # Populate existing rows
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")

    # Make non-nullable
    op.alter_column('users', 'status', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'status')
```

### Adding Foreign Key

```python
def upgrade() -> None:
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_posts_author_id',
        'posts', 'users',
        ['author_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('fk_posts_author_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
```

### Creating Index

```python
def upgrade() -> None:
    op.create_index('ix_users_email_active', 'users', ['email', 'is_active'])


def downgrade() -> None:
    op.drop_index('ix_users_email_active', table_name='users')
```

### Renaming Column

```python
def upgrade() -> None:
    op.alter_column('users', 'name', new_column_name='full_name')


def downgrade() -> None:
    op.alter_column('users', 'full_name', new_column_name='name')
```

### Creating Enum Type (PostgreSQL)

```python
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    # Create enum type
    status_enum = postgresql.ENUM('pending', 'active', 'suspended', name='user_status')
    status_enum.create(op.get_bind())

    # Add column with enum
    op.add_column('users', sa.Column('status', status_enum, nullable=False,
                                     server_default='pending'))


def downgrade() -> None:
    op.drop_column('users', 'status')

    # Drop enum type
    status_enum = postgresql.ENUM('pending', 'active', 'suspended', name='user_status')
    status_enum.drop(op.get_bind())
```

## Step 5: Migration Commands Reference

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --indicate-current

# Rollback last migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123def456

# Rollback all migrations
alembic downgrade base

# Show SQL without executing
alembic upgrade head --sql

# Create empty migration (for manual edits)
alembic revision -m "manual_data_migration"

# Stamp database (mark as migrated without running)
alembic stamp head
```

## Step 6: Data Migrations

For migrations that modify data:

```python
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

def upgrade() -> None:
    # Define table structure for data operations
    users = table('users',
        column('id', Integer),
        column('email', String),
        column('status', String),
    )

    # Update data
    op.execute(
        users.update()
        .where(users.c.status == 'inactive')
        .values(status='suspended')
    )


def downgrade() -> None:
    users = table('users',
        column('id', Integer),
        column('status', String),
    )

    op.execute(
        users.update()
        .where(users.c.status == 'suspended')
        .values(status='inactive')
    )
```

## Step 7: Best Practices

1. **One concern per migration** - Don't mix schema changes with data migrations
2. **Always test downgrade** - Run `alembic downgrade -1` then `alembic upgrade head`
3. **Review autogenerated code** - Alembic may miss some changes or generate incorrect code
4. **Use descriptive names** - `add_phone_to_users` not `update_table`
5. **Keep migrations small** - Easier to debug and rollback
6. **Never modify applied migrations** - Create a new migration instead
7. **Handle NULL values** - When adding non-nullable columns
8. **Use transactions** - Alembic wraps migrations in transactions by default
</process>

<success_criteria>
Migration is complete when:
- [ ] Migration generated with descriptive name
- [ ] upgrade() and downgrade() both reviewed
- [ ] Tested on local database
- [ ] downgrade tested (rollback works)
- [ ] No hardcoded values that differ between environments
- [ ] Data migrations handle edge cases
- [ ] Migration committed to version control
</success_criteria>
