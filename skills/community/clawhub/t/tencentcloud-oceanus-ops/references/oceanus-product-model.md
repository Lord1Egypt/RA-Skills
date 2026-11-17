# Oceanus Product Model

## Entity Hierarchy

```
Region (地域)
└── WorkSpace (工作空间) [space-xxxx]
    ├── Folder (文件夹) [folder-xxxx]
    │   └── Job (作业) [cql-xxxx]
    │       ├── JobConfig (作业配置) [版本号]
    │       │   ├── SQL Code / JAR / ETL definition
    │       │   ├── Resource references (程序包)
    │       │   └── Runtime parameters
    │       └── JobInstance (作业实例)
    │           ├── Status (运行状态)
    │           ├── Metrics (指标)
    │           └── Savepoint (快照)
    └── Cluster (集群) [cluster-xxxx]
        ├── CU Resources (计算资源)
        └── Bindings to WorkSpaces
```

## Core Entities

### WorkSpace (工作空间)

- **Identity**: `space-xxxx` (SerialId)
- **Scope**: 1 region can have N workspaces
- **Role**: Basic unit for job management and access control
- **Contains**: Jobs organized in folder tree structure

### Cluster (集群)

- **Identity**: `cluster-xxxx`
- **Types**: Shared (1) / Dedicated (2)
- **Scope**: 1 region has N clusters
- **Binding**: A cluster can be bound to N different workspaces
- **Resources**: CU (Compute Unit) based resource allocation
- **CU Memory**: 2GB, 4GB (default), 8GB, or 16GB per CU

### Job (作业)

- **Identity**: `cql-xxxx` (JobId)
- **Types**:
  - 1 = SQL job (Flink SQL)
  - 2 = JAR job (custom code)
  - 3 = ETL job (visual pipeline)
  - 4 = Python job
- **Belongs to**: WorkSpace, organized in Folder tree
- **Lifecycle**: Created → Configured → Running → Stopped → Deleted

### JobConfig (作业配置)

- **Versioned**: Each configuration creates a new version
- **Contains**:
  - SQL content or JAR/Python entrypoint
  - Resource dependencies (program packages)
  - Runtime parameters (parallelism, checkpoint interval, etc.)
  - Flink version specification
- **Relationship**: A Job runs based on a specific config version

### JobInstance (作业实例)

- **Relationship**: 1 Job has N instances (one per run)
- **States**: Starting → Running → Stopping → Stopped / Failed / Cancelled
- **Contains**: Runtime metrics, logs, savepoints

### Folder (文件夹)

- **Identity**: `folder-xxxx`
- **Role**: Organize jobs in tree structure within a workspace
- **Root**: Use `"root"` as FolderId for root directory

## State Machines

### Job Status Flow

```
CREATED → RUNNING → STOPPING → STOPPED
   ↓          ↓                    ↓
FAILED    FAILED              (can restart)
   ↓
DELETED
```

### Typical Operations by Entity

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| Job | CreateJob | DescribeJobs | ModifyJob | DeleteJobs |
| JobConfig | CreateJobConfig | DescribeJobConfigs | - | DeleteJobConfigs |
| Job (run) | RunJobs | DescribeJobRuntimeInfo | - | StopJobs |
| Folder | CreateFolder | DescribeFolder | ModifyFolder | DeleteFolders |
| WorkSpace | CreateWorkSpace | DescribeWorkSpaces | ModifyWorkSpace | DeleteWorkSpace |
| Cluster | - | DescribeClusters | - | - |

## API Domain

- **Endpoint**: `oceanus.tencentcloudapi.com`
- **API Version**: `2019-04-22`
- **Auth**: TC3-HMAC-SHA256 signature
- **Rate Limit**: 20 req/s per API per region per sub-account (typical)
