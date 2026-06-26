# tsinghua-learn — AGENTS.md

## 架构

6 个脚本：

| 脚本 | 职责 |
|------|------|
| `_config.py` | 路径/配置/凭证、DPAPI 解密 |
| `login_manager.py` | 中央认证网关（默认 fast check，`--force-login` 完整登录） |
| `learn_api.py` | HTTP API（课程/公告/课件/作业/讨论/问卷/聚合查询） |
| `ops.py` | 文件操作（下载/批量下载/上传/移入/清理） |
| `todos_api.py` | 日常管理（代办汇总/标已读/清理，JSON 给 AI） |
| `pdf_merge.py` | 图片→PDF |

登录脚本不直接调用：
| `login_auto.py` | headless 自动登录 |
| `login_supervised.py` | 2FA 登录 |

## 核心命令

```bash
python scripts/login_manager.py                        # 快速检查 session (<1s)
python scripts/login_manager.py --init                 # 初始化凭据
python scripts/login_manager.py --verify               # 验证环境+登录
python scripts/login_manager.py --reset                # 清空所有数据
python scripts/login_manager.py --force-login          # 强制完整登录

python scripts/todos_api.py                            # 代办汇总
python scripts/todos_api.py --mark-read                # + 标已读
python scripts/todos_api.py --cleanup                  # + 清理

python scripts/ops.py --action list-files --course <wlkcid>
python scripts/ops.py --action download --course <wlkcid> --wjid <wjid>
python scripts/ops.py --action download-all --course <wlkcid>
python scripts/ops.py --action upload --course <wlkcid> --xszyid <xszyid> --file <path>
python scripts/ops.py --action pdf-merge --input-dir <目录>
python scripts/ops.py --action cleanup --dry-run
python scripts/ops.py --action cleanup
```

## 关键约束

- paths/creds 全走 `_config.py` getter
- `credentials.json` DPAPI 加密
- 学期从 API 自动检测
- 课程从 API 动态获取
- 不创建新脚本
- 脚本不阻塞（`input()`/`getpass()` 禁用）
- 提交作业自动重命名：`学号_姓名.ext`
