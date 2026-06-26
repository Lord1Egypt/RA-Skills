#!/usr/bin/env bash

# Team Memory v2.4.0 - 创建新成员目录
# 用法: bash scripts/new-member.sh member-010 "张三" "后端开发工程师" "2026-05-19"

set -euo pipefail

SKILL_DIR="${TEAM_MEMORY_DIR:-$HOME/.config/opencode/skills/team-memory}"
MEMBERS_DIR="$SKILL_DIR/data/members"

if [ "$#" -lt 2 ]; then
  echo "用法: bash scripts/new-member.sh <member-id> <姓名> [角色] [入职日期]"
  echo "示例: bash scripts/new-member.sh member-010 \"张三\" \"后端开发工程师\" \"2026-05-19\""
  exit 1
fi

MEMBER_ID="$1"
NAME="$2"
ROLE="${3:-职位未填写}"
JOIN_DATE="${4:-$(date +%Y-%m-%d)}"
MEMBER_DIR="$MEMBERS_DIR/$MEMBER_ID"

if [[ ! "$MEMBER_ID" =~ ^member-[0-9]{3}$ ]]; then
  echo "成员 ID 必须形如 member-010"
  exit 1
fi

if [ -e "$MEMBER_DIR" ]; then
  echo "目标目录已存在，已停止以避免覆盖: $MEMBER_DIR"
  exit 1
fi

mkdir -p "$MEMBER_DIR"

cat > "$MEMBER_DIR/profile.md" <<EOF
# $NAME - 档案

## 基本信息
**成员ID**: $MEMBER_ID  
**姓名**: $NAME  
**角色**: $ROLE  
**入职时间**: $JOIN_DATE  
**所属团队**: 

---

## 性格与管理策略
**类型/偏好**:   
**优势**:   
**注意点**:   
**管理策略**: 

---

## 本年度 OKR

### O1: 核心业务与业绩
**目标**: 

**KR**:
- [ ] KR1:  (完成度: 0%)

### O2: 技术沉淀与系统建设
**目标**: 

**KR**:
- [ ] KR1:  (完成度: 0%)

### O3: 团队赋能与协作
**目标**: 

**KR**:
- [ ] KR1:  (完成度: 0%)

### O4: 个人专业成长
**目标**: 

**KR**:
- [ ] KR1:  (完成度: 0%)

---

## 个人发展计划

### 短期目标（1-3个月）
- [ ] 

### 中期目标（3-6个月）
- [ ] 

### 长期目标（6-12个月）
- [ ] 

---

*创建于 $JOIN_DATE*
EOF

cat > "$MEMBER_DIR/timeline.md" <<EOF
# $NAME - 团队记忆时间轴

> **成员ID**: $MEMBER_ID  
> **姓名**: $NAME  
> **角色**: $ROLE  
> **入职时间**: $JOIN_DATE  

## 快速定位

**最近状态**:   
**重点关注**:   
**下次1:1**:   
**标签云**: 

---

## 时间轴（从新到旧）

<!-- 新记录添加到这里 -->

---

*创建于 $JOIN_DATE*
EOF

cat > "$MEMBER_DIR/distill.md" <<EOF
# $NAME - 蒸馏

## 一句话画像

待补充。

## 近期状态（最近30天）

待补充。

## 关键事件

- 暂无

## 追踪项

- [ ] 暂无

## 我的承诺

- [ ] 暂无

## 关联文件

- 档案: profile.md
- 时间轴: timeline.md
EOF

echo "已创建 $MEMBER_DIR"
echo "请手动更新 skill-config.yaml，加入 $MEMBER_ID / $NAME 的成员映射。"
