# 打包与上架说明

## 目录结构

```
tenyuan-cloud-shop/
├── SKILL.md              # 含 frontmatter（slug / description / version 0.3.2 / pricing）
├── README.md
├── DISCLAIMER.md
├── CHANGELOG.md
├── PACKAGING.md          # 本文件
├── LICENSE.md
├── agents/openai.yaml
├── assets/icon.svg
├── assets/icon-256.png     # 同源 PNG（部分商店仅收 PNG，由 icon.svg 渲染）
├── references/api.md     # 后端 API 契约
└── scripts/validate_package.py
```

## 上架信息

- slug：`tenyuan-cloud-shop`
- 中文名：十元云铺万元利（7 字，远低于 30 字符显示名上限）
- 英文名：TenYuan Cloud Shop
- 一句话：一句话或一张图，普通人也能拥有自己的小批发部迷你网站
- 分类建议：效率工具 / 电商（按后台实际可选项就近选择）
- 图标：`assets/icon.svg`（金色店铺，与既有 9 个 Skill 图标不重复；同源 PNG `assets/icon-256.png` 作为商店仅收 PNG 场景的备选）

## 发布流程（按 15-Skill 总览口径）

1. `python3 scripts/validate_package.py` → VALIDATION PASS
2. 负向测试：篡改副本确认校验器报错（详见 scripts 内注释）
3. 打包：`zip -r tenyuan-cloud-shop-v0.3.2.zip tenyuan-cloud-shop/`（排除 `.DS_Store`）
4. 生成并回验 SHA256：`shasum -a 256 ... > xxx.zip.sha256`，然后 `shasum -a 256 -c`
5. 发布包与 `.sha256` 归档到 CODEX `19-十元云铺万元利/发布包/`，源码镜像 + `SHA256SUMS.txt` 同步
6. SkillHub 后台「发布团队 Skill」入口提交；提交后按统一发布记录规则登记 9 项信息并用公开 API 复核

## 提交前置条件（两条路的顺序约束）

- **后端必须先上线**：`https://ruancyai.com/cloud` 通过 DEPLOY.md 验收清单后，本 Skill 才提交上架。否则商店用户首次使用即失败。
- 后端未上线期间，本包可先完成打包与档案登记，处于「已打包未提交」状态。

## 发布前检查

- [x] 名称与欢迎语已更新
- [x] icon 已就位（金色店铺 SVG + 同源 256×256 PNG）
- [x] 后端 API 契约已写入 references/api.md 并与 v0.3.2 实测一致
- [x] 版本号全包一致（validate_package.py 兜底）
- [ ] 后端部署完成并通过验收清单（待路线 A 完成）
- [ ] SkillHub 提交与 9 项发布记录（待上一步完成后执行）
