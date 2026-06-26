#!/bin/bash
set -e

# SQLC Initialization Script
# Creates sqlc configuration and directory structure

PROJECT_DIR="${1:-.}"
DB_ENGINE="${2:-postgresql}"

# Input validation: PROJECT_DIR must be an existing directory
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

# Input validation: DB_ENGINE must be one of the supported engines
case "$DB_ENGINE" in
    postgresql|mysql|sqlite3)
        ;;
    *)
        echo "Error: Unsupported database engine '$DB_ENGINE'. Must be one of: postgresql, mysql, sqlite3" >&2
        exit 1
        ;;
esac

cleanup() {
    echo "Cleanup completed" >&2
}
trap cleanup EXIT

# Check if sqlc is installed (do NOT auto-install from remote)
check_sqlc() {
    if ! command -v sqlc &> /dev/null; then
        echo "Error: sqlc is not installed." >&2
        echo "Please install sqlc manually before running this script:" >&2
        echo "  go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest" >&2
        echo "  or visit https://docs.sqlc.dev/en/latest/overview/install.html" >&2
        echo '{"success": false, "error": "sqlc is not installed. Please install it manually."}'
        exit 1
    fi
}

show_usage() {
    cat << 'EOF'
Usage: sqlc-init.sh [project-dir] [db-engine]

Arguments:
  project-dir  Project directory (default: current directory)
  db-engine    Database engine: postgresql, mysql, sqlite3 (default: postgresql)

Examples:
  sqlc-init.sh
  sqlc-init.sh ./my-project
  sqlc-init.sh ./my-project postgresql

Creates:
  sqlc.yaml                    # SQLC configuration
  db/migrations/               # Schema migrations
  db/queries/                  # SQL query files
  internal/repository/         # Generated Go code output
EOF
}

# Main execution
cd "$PROJECT_DIR"

echo "Initializing sqlc in: $(pwd)" >&2
check_sqlc

# Determine the sql_package based on DB_ENGINE
case "$DB_ENGINE" in
    postgresql)
        SQL_PACKAGE="pgx/v5"
        ;;
    mysql)
        SQL_PACKAGE="database/sql"
        ;;
    sqlite3)
        SQL_PACKAGE="database/sql"
        ;;
esac

# Create directories
echo "Creating directory structure..." >&2
mkdir -p db/migrations
mkdir -p db/queries
mkdir -p internal/repository

# Create sqlc.yaml
# DB_ENGINE is validated above via allowlist so it is safe to interpolate
echo "Creating sqlc.yaml..." >&2
cat > sqlc.yaml << EOF
version: "2"
sql:
  - engine: "$DB_ENGINE"
    queries: "db/queries/"
    schema: "db/migrations/"
    gen:
      go:
        package: "repository"
        out: "internal/repository"
        sql_package: "$SQL_PACKAGE"
        emit_json_tags: true
        emit_prepared_queries: false
        emit_interface: true
        emit_exact_table_names: false
        emit_empty_slices: true
EOF

# Create example migration
echo "Creating example migration..." >&2
cat > db/migrations/001_create_users.sql << 'EOF'
-- +goose Up
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- +goose Down
DROP TABLE IF EXISTS users;
EOF

# Create example query
echo "Creating example query..." >&2
cat > db/queries/users.sql << 'EOF'
-- name: GetUser :one
SELECT * FROM users WHERE id = $1;

-- name: GetUserByEmail :one
SELECT * FROM users WHERE email = $1;

-- name: ListUsers :many
SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2;

-- name: CreateUser :one
INSERT INTO users (email, name)
VALUES ($1, $2)
RETURNING *;

-- name: UpdateUser :one
UPDATE users
SET name = $2, updated_at = NOW()
WHERE id = $1
RETURNING *;

-- name: DeleteUser :exec
DELETE FROM users WHERE id = $1;
EOF

# Validate configuration
echo "Validating sqlc configuration..." >&2
if sqlc compile; then
    echo "Configuration valid" >&2
    echo '{"success": true, "message": "sqlc initialized successfully", "files": ["sqlc.yaml", "db/migrations/001_create_users.sql", "db/queries/users.sql"]}'
else
    echo '{"success": false, "error": "sqlc configuration validation failed"}'
    exit 1
fi
