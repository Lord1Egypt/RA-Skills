# 模拟器参考

UnifiedQuantum 提供本地模拟能力，但当前应该把它理解为“常用能力 + 明确依赖边界”，而不是默认裸环境必备。

## 依赖边界

本地模拟、dummy 模式、部分算法示例通常需要：

```bash
pip install "unified-quantum[simulation]"
```

如果用户看到这类报错，优先怀疑缺可选依赖：

- `No module named 'qutip'`
- `MissingDependencyError(... simulation ...)`
- `uniqc is not installed with UniqcCpp`

## 主要类

### `OriginIR_Simulator`

```python
from uniqc.simulator import OriginIR_Simulator

sim = OriginIR_Simulator(backend_type="statevector")
```

常见方法：

```python
probs = sim.simulate_pmeasure(circuit.originir)
statevector = sim.simulate_statevector(circuit.originir)
rho = sim.simulate_density_matrix(circuit.originir)
counts = sim.simulate_shots(circuit.originir, shots=1000)
```

### `OriginIR_NoisySimulator`

```python
from uniqc.simulator import OriginIR_NoisySimulator
```

适合在有噪声模型时做本地实验。

## 后端类型

最稳妥的后端类型选择：

- `statevector`
- `densitymatrix`

示例：

```python
sim = OriginIR_Simulator(backend_type="statevector")
sim = OriginIR_Simulator(backend_type="densitymatrix")
```

当前 CLI 的 `simulate` 子命令更适合走 `statevector` 路径；如果用户明确要密度矩阵模拟，优先给 Python API 方案。

## 输入格式建议

`OriginIR_Simulator` 最适合直接吃 OriginIR：

```python
result = sim.simulate_pmeasure(circuit.originir)
```

如果用户手里只有 QASM，先统一格式更稳：

1. `Circuit.qasm -> uniqc circuit --format originir`
2. 再用模拟器或 `uniqc simulate`

## 拓扑与可用 qubit 约束

模拟器支持传入约束：

```python
sim = OriginIR_Simulator(
    backend_type="statevector",
    available_qubits=[0, 1, 2, 3],
    available_topology=[[0, 1], [1, 2], [2, 3]],
)
```

这适合：

- 提前检查线路是否符合目标芯片拓扑
- 在 dummy 场景里模拟“可用 qubit / coupling map”限制

## `least_qubit_remapping`

基础模拟器支持 `least_qubit_remapping` 参数。默认会做更紧凑的 qubit 映射；如果用户非常在意保留原始编号，可显式关闭。

```python
sim = OriginIR_Simulator(
    backend_type="statevector",
    least_qubit_remapping=False,
)
```

## 与 dummy 模式的关系

dummy 适配器底层会走本地模拟，因此：

- dummy 不是“绕过模拟依赖”
- dummy 更像“沿用统一的 task API，但把执行后端换成本地模拟器”

## 什么时候不该强推模拟器

以下情况不要默认推荐先本地模拟：

- 用户只想做格式转换
- 用户只想提交到云平台
- 用户环境明显缺少模拟依赖，而且问题与模拟无关

这时优先走：

- `Circuit -> originir -> uniqc submit`
- 或纯文档解释，不强制运行本地模拟
