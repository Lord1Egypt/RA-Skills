# thread Skill

多线程与并发助手：在 Cursor 里回答何时用线程/进程/异步、如何加锁、如何用线程池、以及各语言 API。**SKILL.md** 面向 AI，说明何时用、如何选型、安全原则和快速参考；本 README 面向人类。

## 何时会用到

- 用户问「该用线程还是 async」「线程和进程区别」「Python GIL」「死锁/竞态」等。
- 用户需要写多线程代码、线程池、锁、队列或选型（I/O 密集 vs CPU 密集）时，AI 会查本 skill 的 Quick Reference 和 reference/，必要时引用 assets/ 里的模板。

## 目录结构

```
thread/
├── SKILL.md              # AI 工作指南
├── README.md              # 本文件
├── reference/             # 详细参考
│   ├── README.md
│   ├── concepts.md        # 线程 vs 进程 vs 异步；I/O vs CPU；GIL
│   ├── patterns.md       # 锁、队列、线程池、死锁避免
│   └── languages.md      # Python / Java / C# / Node / Go 快速 API
└── assets/                # 代码模板
    ├── README.md
    ├── python-thread-starter.py   # 线程 + 锁示例
    └── python-thread-pool.py     # 线程池示例
```

## 各目录说明

| 目录 | 内容 |
|------|------|
| **reference/concepts.md** | 何时用线程/进程/异步，I/O-bound vs CPU-bound，Python GIL。 |
| **reference/patterns.md** | 共享状态、锁、队列、线程池、死锁与常见坑。 |
| **reference/languages.md** | 各语言线程/锁/队列/池/异步 API 速查。 |
| **assets/** | 可直接参考或改写的示例代码（当前为 Python）。 |

## 依赖

- 无额外依赖；示例为 Python 标准库（`threading`、`concurrent.futures`）。
