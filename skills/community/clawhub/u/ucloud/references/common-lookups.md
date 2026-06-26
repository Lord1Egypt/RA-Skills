# 通用 Lookup API

当公共请求范围信息缺失且可以从账号上下文中发现时，使用以下 API。

使用这些 lookup API 先缩小缺失值的范围。如果查询后仍存在多个有效候选项，将简短列表呈现给用户并请其选择。

## Region 和 Zone 发现

- `ListRegions`
  当缺少 `Region` 或用户仅给出了城市或产品名称时使用。
- `ListZones`
  当缺少 `Zone` 且已知或可以推断所选 Region 时使用。

推荐流程：

1. 如果不知道任何 Region，先调用 `ListRegions`。
2. 一旦 `Region` 已知，如果 Action 还需要 Zone，再调用 `ListZones`。
3. 如果仍然存在多个候选项，向用户展示简洁的列表并请其选择。

## 项目发现

- `GetProjectList`
  当缺少 `ProjectId` 且账号可能包含多个项目时使用。

如果只返回一个项目，直接使用它。如果返回多个项目，请用户选择确切的项目。

## 余额检查

- `GetBalance`
  在创建计费资源前，当账户余额可能影响操作时，或用户询问账户就绪情况时使用。

## 操作规则

当某个值可以从账号上下文中发现时，优先使用这些 Lookup API，而不是提出"选哪个 Region？"或"选哪个项目？"之类的宽泛问题。仅在发现后仍存在多个有效候选项或无可用的结果时才询问用户。

Lookup 调用同样先检查是否存在等价的产品或配置子命令。没有等价子命令时，使用 `ucloud api` 的通用 lookup Action。小型 lookup payload 可以使用 inline flag；需要保持调用形态一致或需要显式 profile 时，使用 `--local-file`。

Inline flag 示例：

```bash
ucloud api --Action ListRegions
ucloud api --Action ListZones --Region cn-bj2
ucloud api --Action GetProjectList
ucloud --profile my-profile api --Action GetBalance
```

Local-file 示例：

```bash
# ListRegions
cat > /tmp/ucloud-request.json << 'EOF'
{"Action":"ListRegions"}
EOF
ucloud api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json

# ListZones（需要 Region）
cat > /tmp/ucloud-request.json << 'EOF'
{"Action":"ListZones","Region":"cn-bj2"}
EOF
ucloud api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json

# GetProjectList
cat > /tmp/ucloud-request.json << 'EOF'
{"Action":"GetProjectList"}
EOF
ucloud api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json

# GetBalance
cat > /tmp/ucloud-request.json << 'EOF'
{"Action":"GetBalance"}
EOF
ucloud --profile my-profile api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json
```

每次 lookup 后，检查 JSON 响应。从响应体中提取所需值：
- `ListRegions` → `Regions[].Region`
- `ListZones` → `Zones[].Zone`
- `GetProjectList` → `ProjectSet[].ProjectId`
- `GetBalance` → 顶层余额字段

如果只有一个候选项，直接使用。如果有多个候选项，将列表展示给用户并请其选择。
