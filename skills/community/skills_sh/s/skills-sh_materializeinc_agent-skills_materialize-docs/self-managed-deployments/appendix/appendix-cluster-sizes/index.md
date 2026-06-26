# Cluster sizes
Reference page on self-managed cluster sizes
## Default Cluster Sizes

For Self-Managed Materialize, the cluster sizes are configured with the
following default resource allocations:

<table>
<thead>
<tr>
<th>Size</th>
<th>Scale</th>
<th>CPU Limit</th>
<th>Disk Limit</th>
<th>Memory Limit</th>
</tr>
</thead>
<tbody>

<tr>
<td><code>25cc</code></td>
<td><code>1</code></td>
<td><code>0.5</code></td>
<td><code>7762MiB</code></td>
<td><code>3881MiB</code></td>
</tr>

<tr>
<td><code>50cc</code></td>
<td><code>1</code></td>
<td><code>1</code></td>
<td><code>15525MiB</code></td>
<td><code>7762MiB</code></td>
</tr>

<tr>
<td><code>100cc</code></td>
<td><code>1</code></td>
<td><code>2</code></td>
<td><code>31050MiB</code></td>
<td><code>15525MiB</code></td>
</tr>

<tr>
<td><code>200cc</code></td>
<td><code>1</code></td>
<td><code>4</code></td>
<td><code>62100MiB</code></td>
<td><code>31050MiB</code></td>
</tr>

<tr>
<td><code>300cc</code></td>
<td><code>1</code></td>
<td><code>6</code></td>
<td><code>93150MiB</code></td>
<td><code>46575MiB</code></td>
</tr>

<tr>
<td><code>400cc</code></td>
<td><code>1</code></td>
<td><code>8</code></td>
<td><code>124201MiB</code></td>
<td><code>62100MiB</code></td>
</tr>

<tr>
<td><code>600cc</code></td>
<td><code>1</code></td>
<td><code>12</code></td>
<td><code>186301MiB</code></td>
<td><code>93150MiB</code></td>
</tr>

<tr>
<td><code>800cc</code></td>
<td><code>1</code></td>
<td><code>16</code></td>
<td><code>248402MiB</code></td>
<td><code>124201MiB</code></td>
</tr>

<tr>
<td><code>1200cc</code></td>
<td><code>1</code></td>
<td><code>24</code></td>
<td><code>372603MiB</code></td>
<td><code>186301MiB</code></td>
</tr>

<tr>
<td><code>1600cc</code></td>
<td><code>1</code></td>
<td><code>31</code></td>
<td><code>481280MiB</code></td>
<td><code>240640MiB</code></td>
</tr>

<tr>
<td><code>3200cc</code></td>
<td><code>1</code></td>
<td><code>62</code></td>
<td><code>962560MiB</code></td>
<td><code>481280MiB</code></td>
</tr>

<tr>
<td><code>6400cc</code></td>
<td><code>2</code></td>
<td><code>62</code></td>
<td><code>962560MiB</code></td>
<td><code>481280MiB</code></td>
</tr>

</tbody>
</table>

## Custom Cluster Sizes

When installing the Materialize Helm chart, you can override the [default
cluster sizes and resource allocations](#default-cluster-sizes). These
cluster sizes are used for both internal clusters, such as the `system_cluster`,
as well as user clusters.

> **Tip:** In general, you should not have to override the defaults. At minimum, we
> recommend that you keep the 25-200cc cluster sizes.

```yaml
operator:
  clusters:
    sizes:
      <size>:
        workers: <int>
        scale: 1                  # Generally, should be set to 1.
        cpu_exclusive: <bool>
        cpu_limit: <float>         # e.g., 6
        cpu_request: <float>       # e.g., 4 (optional, defaults to cpu_limit, may not be higher than cpu_limit)
        credits_per_hour: "0.0"    # N/A for self-managed.
        disk_limit: <string>       # e.g., "93150MiB"
        memory_limit: <string>     # e.g., "46575MiB"
        swap_enabled: <bool>       # optional, defaults to the cluster-level swap_enabled
        selectors: <map>           # k8s label selectors
        # ex: kubernetes.io/arch: amd64
```

| Field | Type | Description | Recommendation |
| --- | --- | --- | --- |
| <strong>workers</strong> | int | The number of timely workers in your cluster replica. | Use 1 worker per CPU core, with a minimum of 1 worker. |
| <strong>scale</strong> | int | The number of pods (i.e., processes) to use in a cluster replica; used to scale out replicas horizontally. Each pod will be provisioned using the settings defined in the size definition. | Generally, this should be set to 1. This should only be greater than 1 when a replica needs to take on limits that are greater than the maximum limits permitted on a single node. |
| <strong>cpu_exclusive</strong> | bool | The flag that determines if the workers should attempt to pin to a particular CPU core. | <p><a name="cpu_exclusive"></a></p> <p>Set to true <strong>if and only if</strong> the <a href="#cpu_limit" ><code>cpu_limit</code></a> is a whole number and the CPU management policy in the k8s cluster is set to static.</p>  |
| <strong>cpu_limit</strong> | float | <a name="cpu_limit"></a> The Kubernetes CPU limit for a replica pod, in cores. | <p>Prefer whole number values to enable CPU affinity. Kubernetes only allows CPU Affinity for pods taking a whole number of cores.</p> <p>If the value is not a whole number, set <a href="#cpu_exclusive" ><code>cpu_exclusive</code></a> to false.</p>  |
| <strong>cpu_request</strong> | float | <a name="cpu_request"></a> The Kubernetes CPU request for a replica pod, in cores. If not set, defaults to the value of <code>cpu_limit</code>. | In most cases, you do not need to set this. It is useful when you want to allow CPU bursting by setting a request lower than the limit. |
| <strong>memory_limit</strong> | string | The Kubernetes memory limit for a replica pod (e.g., <code>&quot;46575MiB&quot;</code>). | <dl> <dt>For most workloads, use an approximate <strong>1:8</strong> CPU-to-memory ratio (1 core</dt> <dd>8 GiB). This can vary depending on your workload characteristics.</dd> </dl>  |
| <strong>disk_limit</strong> | string | The size of the persistent volume to provision for a replica pod (e.g., <code>&quot;93150MiB&quot;</code>). | When spill-to-disk is enabled, use a <strong>1:2</strong> memory-to-disk ratio. Materialize spills data to disk when memory is insufficient, which can impact performance. When <code>swap_enabled</code> is true, this field is automatically set to <code>&quot;0&quot;</code> by the Helm chart. |
| <strong>credits_per_hour</strong> | string | This is a cloud attribute that should be set to &ldquo;0.00&rdquo; in self-managed. | Set to &ldquo;0.00&rdquo; for self-managed deployments. |
| <strong>swap_enabled</strong> | bool | Enables swap as the spill-to-disk mechanism for this size. When enabled, the replica uses swap instead of a provisioned persistent volume for spilling data. This also causes <code>disk_limit</code> to be set to <code>&quot;0&quot;</code>. | This defaults to the global <code>swap_enabled</code> value if not specified per size. Swap generally performs better than spill-to-disk via persistent volumes. |
| <strong>selectors</strong> | map | A map of Kubernetes label selector keys to values used to schedule pods for this cluster size on specific nodes. | It is generally not required to set this. |

> **Note:** If you have modified the default cluster size configurations, you can query the
> [`mz_cluster_replica_sizes`](/reference/system-catalog/mz_catalog/#mz_cluster_replica_sizes)
> system catalog table for the specific resource allocations.

