# 留学助理 — 待办清单（Backlog）

> 更新：2026-08-12
> 来源：开发过程 + 走查卡点 + 产品迭代发现。优先级 P0/P1/P2。

## P0（影响正确性/体验）
- [x] **program 增加 `gre` 字段**（✅ 08-12 完成并部署：schema+upd_gre.py 填 40/76 项+校验+引擎输出+skill 展示+test 39/39+生产验证 not_required 生效）
- [ ] **assess language 分启发式缺陷**：GRE 缺失按 0 计入，把语言分拉低（TOEFL 112 却 language=50）→ 改为缺失时不拉低或标注"GRE 待考"
- [ ] **画像档位 vs 选校档位一致性**：assess 综合档位（如 match）与 schools/professors 的 GPA 档位（strong）两套启发式，可能感知不一致 → 统一或注明口径

## P1（功能补全）
- [ ] **skill 端选校支持多 discipline**：`--discipline` 目前单值，导致 `data` 类项目（如 UW MS Data Science）在 cs 方向用户下被过滤 → 改 nargs+ 或引擎支持逗号分隔
- [ ] **教授库实名核实**：占位姓名 → 按 faculty 页录入真实教授（Top 校优先，见 PROFESSOR_CANDIDATES 候选池），套磁才有真实落点
- [ ] **方案 B：真实 LLM 接入**（DeepSeek key 即可，服务器已验证 api.deepseek.com 可达）：LLM_BASE_URL=https://api.deepseek.com/v1、LLM_MODEL=deepseek-chat、compose 注入重启
- [ ] 网站加一页 `/study.html`（产品说明 + 触发引导 + 注册入口）

## P2（扩展位）
- [ ] PostgreSQL 迁移（状态文件 → PG）：多实例/高并发时
- [ ] 多国/多学位扩展（英/新/港/加；本科/PhD）——预留位已设计
- [ ] deadline 提醒（Celery/独立调度）——有业务量后
- [ ] 注册/登录 merge（接现有用户体系）
- [ ] 计划模板按学位/学科细分

## 已关闭（历史）
- 教授短名单缺失 → ✅ 50 条占位 + GET /professors（08-12）
- 申请清单 CRUD → ✅（08-12）
- 面试模块 → ✅（08-12）
- p0 首任务逾期 → ✅ 锚 today（08-12）
- S4 部署 → ✅ 生产上线（08-12）
- 对话内测试 → ✅ 9 项全通 + 安装到 ~/.workbuddy/skills/（08-12）
