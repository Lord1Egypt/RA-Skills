#!/usr/bin/env bash
# ============================================================
# check_db_contracts.sh —— Rust + SeaORM 显式契约检测脚本
#
# 用法: ./check_db_contracts.sh [src_dir]
# 默认 src_dir = ./src
#
# 集成到 CI: cargo build && ./check_db_contracts.sh
# ============================================================

set -euo pipefail

SRC_DIR="${1:-./src}"
ERRORS=0
WARNINGS=0

red()    { printf "\033[31m%s\033[0m\n" "$1"; }
yellow() { printf "\033[33m%s\033[0m\n" "$1"; }
green()  { printf "\033[32m%s\033[0m\n" "$1"; }

error()   { red "  ❌ $1"; ERRORS=$((ERRORS + 1)); }
warn()    { yellow "  ⚠ $1"; WARNINGS=$((WARNINGS + 1)); }
ok()      { green "  ✅ $1"; }

# ============================================================
# 自动检测 entity 目录（不硬编码路径）
# ============================================================
detect_entity_dir() {
    # 找包含 DeriveEntityModel 的文件所在目录
    local dirs
    dirs=$(grep -rl "DeriveEntityModel" "$SRC_DIR" 2>/dev/null | xargs -I{} dirname {} | sort -u)
    echo "$dirs"
}

ENTITY_DIRS=$(detect_entity_dir)

echo "═══════════════════════════════════════"
echo "  🔒 Rust + SeaORM 显式契约检测"
echo "═══════════════════════════════════════"
echo ""

# ============================================================
# 1. 数据库操作只走 SeaORM
# ============================================================
echo "🔍 [1] 数据库操作是否只走 SeaORM"

# 1a. 禁止其他数据库库
other_db_libs=$(grep -rn \
    -e "use rusqlite" \
    -e "use sqlx" \
    -e "use diesel" \
    -e "use tokio_postgres" \
    -e "use mysql" \
    "$SRC_DIR" 2>/dev/null || true)

if [ -n "$other_db_libs" ]; then
    error "发现非 SeaORM 数据库库引用:"
    while IFS= read -r line; do red "     $line"; done <<< "$other_db_libs"
else
    ok "未发现其他数据库库"
fi

# 1b. 禁止裸 SQL
raw_sql=$(grep -rn \
    -e "execute_unprepared" \
    -e "query_raw" \
    -e "raw_sql" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|#\[" \
    || true)

if [ -n "$raw_sql" ]; then
    error "发现裸 SQL 操作:"
    while IFS= read -r line; do red "     $line"; done <<< "$raw_sql"
else
    ok "未发现裸 SQL 操作"
fi

# 1c. 禁止硬编码 SQL 语句
hardcoded_sql=$(grep -rn \
    -E "(\"|\')\ *(INSERT INTO|SELECT .+ FROM|UPDATE .+ SET|DELETE FROM)" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|#\[\|doc\|test\|migration" \
    || true)

if [ -n "$hardcoded_sql" ]; then
    error "发现硬编码 SQL 语句:"
    while IFS= read -r line; do red "     $line"; done <<< "$hardcoded_sql"
else
    ok "未发现硬编码 SQL 语句"
fi

echo ""

# ============================================================
# 2. 类型安全不被绕过
# ============================================================
echo "🔍 [2] 类型安全检查"

# 2a. col_expr 中禁止字符串字面量（设枚举/状态字段）
col_expr_string=$(grep -rn \
    -e "col_expr.*Expr::value.*String" \
    -e "col_expr.*Expr::value.*\"" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//" \
    || true)

if [ -n "$col_expr_string" ]; then
    error "col_expr 中使用了字符串字面量（应用 .set(ActiveModel) 替代）:"
    while IFS= read -r line; do red "     $line"; done <<< "$col_expr_string"
else
    ok "col_expr 未使用字符串字面量"
fi

# 2b. Entity 文件中禁止 serde_json::Value（弱类型 JSON）
if [ -n "$ENTITY_DIRS" ]; then
    json_value_in_entity=$(grep -rn "serde_json::Value" $ENTITY_DIRS 2>/dev/null \
        | grep -v "///\|//" \
        || true)

    if [ -n "$json_value_in_entity" ]; then
        warn "Entity 中使用了 serde_json::Value（建议用强类型 struct）:"
        while IFS= read -r line; do yellow "     $line"; done <<< "$json_value_in_entity"
    else
        ok "Entity 中未使用弱类型 JSON"
    fi
fi

# 2c. Entity 文件中禁止 NaiveDateTime
if [ -n "$ENTITY_DIRS" ]; then
    naive_dt_in_entity=$(grep -rn "NaiveDateTime" $ENTITY_DIRS 2>/dev/null \
        | grep -v "///\|//" \
        || true)

    if [ -n "$naive_dt_in_entity" ]; then
        error "Entity 中使用了 NaiveDateTime（应用 DateTimeUtc）:"
        while IFS= read -r line; do red "     $line"; done <<< "$naive_dt_in_entity"
    else
        ok "Entity 中未使用 NaiveDateTime"
    fi
fi

echo ""

# ============================================================
# 3. 业务规范
# ============================================================
echo "🔍 [3] 业务规范检查"

# 3a. 状态变更是否检查 can_transition_to
# 找所有对状态字段赋值的地方，检查附近是否有 can_transition_to
status_sets=$(grep -rn \
    -e "status.*=.*Set(" \
    -e "status:.*Set(" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|Default\|default\|ActiveModelBehavior\|Borrowed\|::new\|test" \
    || true)

if [ -n "$status_sets" ]; then
    # 对每个状态赋值，检查同一个文件中是否调用了 can_transition_to
    has_unchecked=false
    echo "$status_sets" | while IFS= read -r line; do
        file=$(echo "$line" | cut -d: -f1)
        if ! grep -q "can_transition_to" "$file" 2>/dev/null; then
            warn "状态变更未见 can_transition_to 检查: $line"
            has_unchecked=true
        fi
    done
    if [ "$has_unchecked" = false ]; then
        ok "状态变更均有流转检查"
    fi
else
    ok "未发现状态变更操作（或已过滤）"
fi

# 3b. 软删除表查询是否过滤
if [ -n "$ENTITY_DIRS" ]; then
    # 找出哪些 entity 有 is_deleted 字段
    soft_delete_entities=$(grep -rl "is_deleted" $ENTITY_DIRS 2>/dev/null | sort -u || true)

    for entity_file in $soft_delete_entities; do
        [ -f "$entity_file" ] || continue
        entity_name=$(basename "$entity_file" .rs)
        [ "$entity_name" = "mod" ] && continue

        # 在整个项目中查找对该 entity 的 find 调用
        entity_finds=$(grep -rn "${entity_name}::Entity::find" "$SRC_DIR" 2>/dev/null || true)

        if [ -n "$entity_finds" ]; then
            echo "$entity_finds" | while IFS= read -r line; do
                file=$(echo "$line" | cut -d: -f1)
                lineno=$(echo "$line" | cut -d: -f2)

                # 检查该 find 调用后 10 行内是否有 is_deleted 过滤
                has_filter=$(sed -n "${lineno},$((lineno + 10))p" "$file" 2>/dev/null | grep -c "is_deleted\|IsDeleted" || echo "0")

                if [ "$has_filter" -eq 0 ]; then
                    warn "查询软删除表 ${entity_name} 但未见 is_deleted 过滤: $line"
                fi
            done
        fi
    done
fi

echo ""

# ============================================================
# 4. Entity 文件完整性
# ============================================================
echo "🔍 [4] Entity 文件完整性"

if [ -z "$ENTITY_DIRS" ]; then
    yellow "  ⚠ 未检测到 Entity 文件（无 DeriveEntityModel），跳过"
else
    for dir in $ENTITY_DIRS; do
        for file in "$dir"/*.rs; do
            [ -f "$file" ] || continue
            basename=$(basename "$file")
            [ "$basename" = "mod.rs" ] && continue
            [ "$basename" = "prelude.rs" ] && continue

            # 4a. 文件级 doc comment
            if ! head -3 "$file" | grep -q "^//!"; then
                error "$basename 缺少文件级 doc comment（//! 开头）"
            fi

            # 4b. 有 DeriveActiveEnum 的 enum 是否有 can_transition_to
            has_enum=$(grep -c "DeriveActiveEnum" "$file" 2>/dev/null || true)
            has_enum=$((has_enum + 0))
            if [ "$has_enum" -gt 0 ]; then
                # 不是所有枚举都需要状态流转（如 MemberLevel），这里只做提醒
                has_transition=$(grep -c "can_transition_to" "$file" 2>/dev/null || true)
                has_transition=$((has_transition + 0))
                if [ "$has_transition" -eq 0 ]; then
                    # 检查是否是状态类枚举（名字含 Status/State）
                    has_status_enum=$(grep -E "enum.*(Status|State)" "$file" || true)
                    if [ -n "$has_status_enum" ]; then
                        warn "$basename 有状态枚举但未定义 can_transition_to()"
                    fi
                fi
            fi

            # 4c. 字段是否有注释（至少一半的 pub 字段应该有 ///）
            pub_fields=$(grep -c "pub " "$file" 2>/dev/null || true)
            pub_fields=$((pub_fields + 0))
            doc_comments=$(grep -c "/// " "$file" 2>/dev/null || true)
            doc_comments=$((doc_comments + 0))
            if [ "$pub_fields" -gt 4 ] && [ "$doc_comments" -lt 3 ]; then
                warn "$basename 字段注释偏少（$doc_comments 个注释 / $pub_fields 个字段）"
            fi
        done
    done

    # 所有 entity 检查完毕后的汇总在最后统一输出
fi

echo ""

# ============================================================
# 汇总
# ============================================================
echo "═══════════════════════════════════════"
if [ "$ERRORS" -gt 0 ]; then
    red "  ❌ 发现 $ERRORS 个错误，$WARNINGS 个警告"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    yellow "  ⚠ 无错误，$WARNINGS 个警告（建议修复）"
    exit 0
else
    green "  ✅ 所有检查通过"
    exit 0
fi
