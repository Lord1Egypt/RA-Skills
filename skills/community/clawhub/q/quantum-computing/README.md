# quantum-computing

[![Quantum Computing | AI](https://img.shields.io/badge/Quantum_Computing-AI-58a6ff?style=flat-square)](https://github.com/IAI-USTC-Quantum)

面向 [UnifiedQuantum](https://github.com/IAI-USTC-Quantum/UnifiedQuantum) 的本地 skill 仓库。

安装后，支持 skills 的 Agent 可以更稳地处理 UnifiedQuantum 相关任务，例如线路构建、OriginIR / QASM 转换、本地模拟、云平台提交、变分算法示例、PyTorch 集成和通用排障。

## 这个 skill 能帮你什么

适合让 Agent 帮你处理这类事情：

- 写或修改 `Circuit` 线路代码
- 把线路导出成 OriginIR 或 OpenQASM
- 用 `uniqc` CLI 做转换、模拟、提交和查结果
- 检查本地模拟、dummy 模式或云平台配置问题
- 搭一个最小的 VQE / QAOA / UCCSD 示例
- 看 `QuantumLayer`、parameter-shift 和批处理接口怎么接进 PyTorch

## 你可以直接让 Agent 做什么

安装后，可以直接对 Agent 说这类请求：

- “帮我写一个 Bell state 的 UnifiedQuantum 示例，并导出 OriginIR。”
- “帮我把这段 QASM 转成更适合 `uniqc simulate` 的流程。”
- “帮我查一下为什么 `uniqc` 命令存在，但 `import uniqc` 失败。”
- “帮我写一个最小 QAOA MaxCut 例子。”
- “帮我看一下 dummy 模式为什么跑不通。”
- “帮我把这个 PyTorch 训练循环接上 `QuantumLayer`。”

## 安装此 skill

先把仓库放到本地，再把它链接或复制到你的 skill 目录。

```bash
git clone https://github.com/IAI-USTC-Quantum/quantum-computing.skill.git
mkdir -p ~/.Agents/skills
ln -s /path/to/quantum-computing.skill ~/.Agents/skills/quantum-computing
```

如果你已经有自己的共享 skills 目录，就安装到那个目录里。

安装完成后，Agent 就可以从 `SKILL.md` 和 `references/` 里读取更具体的操作规则、主题说明和排障步骤。

## 仓库内容

- `SKILL.md`：主入口，包含触发条件、操作规则和导航
- `references/`：按主题整理的使用说明与排障参考
- `examples/`：可复用的示例代码
- `scripts/`：环境检查和辅助脚本

## 许可证

Apache 2.0 许可证
