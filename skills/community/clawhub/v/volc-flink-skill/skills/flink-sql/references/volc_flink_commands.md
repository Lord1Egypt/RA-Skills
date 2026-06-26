# `volc_flink` command quick reference

## Projects

```bash
volc_flink projects list
volc_flink projects detail <project-name>
```

## Drafts

```bash
volc_flink drafts dirs
volc_flink drafts apps

volc_flink drafts create \
  -n <draft-name> \
  --directory <directory> \
  --job-type FLINK_STREAMING_SQL \
  --engine-version <engine_version> \
  --sql "<sql>"

volc_flink drafts content -i <draft-id>
volc_flink drafts update -i <draft-id> --sql "<sql>"
volc_flink drafts params set -i <draft-id> --kv <key>=<value>
volc_flink drafts publish -i <draft-id> --resource-pool <resource-pool>
```

## Jobs

```bash
volc_flink jobs list --search <keyword>
volc_flink jobs detail -i <job-id>
volc_flink jobs start -i <job-id>
volc_flink jobs stop -i <job-id>
volc_flink jobs restart -i <job-id> --inspect
volc_flink jobs rescale -i <job-id> --parallelism <n> --tm-cpu <cpu> --tm-mem-ratio 1:4 --tm-slots <slots> --inspect
volc_flink jobs instances -i <job-id>
volc_flink jobs events -i <job-id>
volc_flink jobs metrics -i <job-id>
volc_flink jobs ui -i <job-id>
volc_flink jobs savepoint -i <job-id>
volc_flink jobs savepoints -i <job-id>
```

## Monitor

```bash
volc_flink monitor events -i <job-id>
volc_flink monitor logs -i <job-id>
volc_flink monitor flinkui -i <job-id>
```

