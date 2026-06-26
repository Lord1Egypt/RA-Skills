#!/bin/bash
# 脱敏 OpenClaw 配置中的敏感字段
# 用法: cat config.json | ./sanitize.sh

sed -E 's/("apiKey"|"token"|"password"|"secret"|"BRAVE_API_KEY"|"PERPLEXITY_API_KEY":)[[:space:]]*"[^"]*"/\1 "***"/g'