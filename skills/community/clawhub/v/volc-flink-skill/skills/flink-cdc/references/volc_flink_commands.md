# `volc_flink` CDC quick reference

## Draft dirs / mkdir

`drafts create` 的 `--directory` 必须是已存在的草稿目录路径（或目录名）。建议先列目录，必要时创建目录：

```bash
volc_flink drafts dirs
volc_flink drafts mkdir --name "/数据开发文件夹/CDC"
```

## Draft create

```bash
volc_flink drafts create \
  --type cdc \
  --directory "/数据开发文件夹" \
  -n "mysql-paimon-demo" \
  --engine-version FLINK_VERSION_1_16 \
  --cdc-version v3.4 \
  --cdc "<inline-yaml>"
```

### Inline YAML (recommended)

Use heredoc to avoid escaping issues and prevent `${...}` placeholders from being expanded by shell:

```bash
volc_flink drafts create \
  --type cdc \
  --directory "/数据开发文件夹" \
  -n "mysql-paimon-demo" \
  --engine-version FLINK_VERSION_1_16 \
  --cdc-version v3.4 \
  --cdc "$(cat <<'YAML'
sources:
- source:
    type: mysql
    hostname: ${mysql_hostname}
    port: ${mysql_port}
    username: ${mysql_username}
    password: ${mysql_password}
    tables: fin_db.*\\.balance.*
    server-id: ${mysql_server_id}
sink:
  type: paimon-las
  commit.user: ${paimon_las_commit_user}
pipeline:
  name: ${pipeline_name}
  parallelism: ${pipeline_parallelism}
YAML
)"
```

### Fallback: YAML file

Most robust approach: provide YAML via file (also avoids any shell quoting/expansion pitfalls).

```bash
volc_flink drafts create \
  --type cdc \
  --cdc-file ./path/to/job.yml \
  --directory "/数据开发文件夹" \
  -n "mysql-paimon-demo" \
  --engine-version FLINK_VERSION_1_16 \
  --cdc-version v3.4
```

## Draft readback

```bash
volc_flink drafts content -i <draft-id>
```

## Draft publish

```bash
volc_flink drafts publish -i <draft-id> --resource-pool <resource-pool>
```

## Job start / inspect

```bash
volc_flink jobs start -i <job-id>
volc_flink jobs detail -i <job-id>
volc_flink jobs events -i <job-id>
volc_flink monitor logs -i <job-id>
volc_flink jobs ui -i <job-id>
```
