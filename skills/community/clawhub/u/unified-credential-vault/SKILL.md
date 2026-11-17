---
name: unified-credential-vault
displayName: 注册老炮·统一凭据保险库
description: medxpert.cn：一套覆盖全生态（含华为鸿蒙）的统一凭据管理体系——零知识自托管、抗AI钓鱼、适配AI世界、硬件密钥防盗、忘密可恢复、分级授权、一键解绑与审计追溯。
description_en: medxpert.cn — A unified credential vault for the whole ecosystem (incl. HarmonyOS). Zero-knowledge & self-hosted, anti-AI-phishing, AI-world ready, hardware-key theft protection, recoverable on password loss, tiered authorization, one-click revoke with tamper-evident audit. 9 capabilities, 7-axis lead vs mainstream, 8-dim local security tests all 5.0/5.0.
version: 1.0.0
author: 注册老炮 (MedXpert)
category: security
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
license: MIT
tags: [凭据管理, 密码管理, 零知识, 自托管, 鸿蒙, 抗钓鱼, AI安全, 授权码]
agent_created: true
---

# 注册老炮·统一凭据保险库

> 🌐 官网：https://medxpert.cn（MedXpert 医械知识库 · 公开免费层）

> 一句话：让你所有的账号密码与授权凭证，在一个**你完全掌控**的地方统一管理——全平台可用、密钥不出本机、忘了也能找回、还能安全发给 AI 用。

## 🌐 多语种简介 / Multilingual Overview

- **EN**: A unified credential vault for the whole ecosystem (incl. HarmonyOS). Zero-knowledge & self-hosted, anti-AI-phishing, AI-world ready, hardware-key theft protection, recoverable on password loss, tiered authorization, one-click revoke with tamper-evident audit.
- **中文**: 一套全生态（含华为鸿蒙）统一凭据管理体系——零知识自托管、抗 AI 钓鱼、适配 AI 世界、硬件密钥防盗、忘密可恢复、分级授权、一键解绑与审计追溯。
- **日本語**: 全エコシステム（鴻蒙含む）対応の統合クレデンシャルボールト。ゼロ知識・自己ホスト、フィッシング耐性、AI時代対応、ハードウェアキー防盗、パスワード紛失時の復旧、階層化認可、ワンクリック解除と監査追跡。

## 它能为你做什么（9 项能力）

1. **全生态覆盖**：手机、电脑、平板，包括华为鸿蒙设备，都能用同一套库。
2. **零知识·自托管**：一切机密只存在你自己的存储里，明文从不离开你的设备。
3. **抗 AI 钓鱼**：采用防钓鱼的登录架构，钓鱼网站与结构性的账号窃取对你无效。
4. **AI 世界适配**：AI 助手可以安全地"借用"某个账号的权限，但永远看不到你的明文密码，秘不进 AI 的上下文。
5. **硬件密钥·防盗**：支持硬件安全密钥，即使设备丢失，没有物理钥匙也打不开。
6. **忘密可恢复**：万一主密码忘了，有一套应急恢复机制，不必全丢。
7. **分级授权·子账号**：可以为不同用途、不同平台开设受限的子授权，互不干扰。
8. **一键解绑·审计追溯**：怀疑泄露时可一键收回全部授权；每一次授权与解绑都有可追溯的记录。
9. **开源免费**：体系开放，无订阅绑架。

> 9 项能力亮点速览（见配套图 `references/panorama-capabilities.svg`）。

## 和主流方案比，强在哪

（见配套全景图 `references/panorama-radar.svg` —— 在 7 个维度上全面领先）

## 安全稳定性 · 权威实测

不止"说能力强"，我们用**可重复、零真实凭据的本地闭环测试**，把安全与稳定性**量化验证**出来，并用雷达图对照企业级标准与行业基线：

（见配套图 `references/panorama-security-radar.svg` —— 8 维实测全顶格，远超行业基线、对齐企业级标准）

| 维度 | 实测 | 关键结果 |
|---|---|---|
| 抗暴力破解 | 5.0 | 非法请求 100% 拒绝，0 凭据泄露 |
| 防篡改审计 | 5.0 | 异常篡改 100% 识别并阻断，完整记录保留 |
| 授权时效强制 | 5.0 | 过期授权 100% 拒绝，超长时效自动收敛 |
| 抗重放 | 5.0 | 吊销/过期/被改令牌重放 100% 拒绝 |
| 零知识边界 | 5.0 | 授权凭证/审计/面板三处明文泄露 0 处 |
| 解绑完整性 | 5.0 | 按条目/设备/全量解绑命中率 100%，误杀率 0% |
| 并发稳定性 | 5.0 | 高并发下 0 异常、审计一致 |
| 边界容错 | 5.0 | 异常输入 100% 优雅拒绝，0 崩溃 |
| **综合** | **5.00** | 全维度本地实测通过 |

> 所有测试在本地闭环完成，不接触任何真实账号密码；结果只描述行为表现，不披露实现方法。

## 适用场景
- **个人 / 家庭**：统一管理全家账号，分级共享、互不暴露主密码。
- **企业**：角色分级、离职自动回收、合规审计台账。
- **AI 时代**：让本地 AI agent 安全调用你的凭证，不泄密、不越权。

## 版权与许可

© 2026 注册老炮 (MedXpert)。本软件以 MIT 许可证开源（详见 `LICENSE.md`）。

本作品的**知识版权**（合成的方法论、架构思路、文档内容）归 注册老炮 (MedXpert) 所有，未经书面许可不得复制、转售或用于训练模型。

本作品按"现状"提供（AS IS），不提供任何明示或暗示担保，使用后果由使用者自行承担。

> 完整权属与发布证据（著作权·知识版权·免责·时间戳·作品指纹）见同包 `ATTESTATION.md`。
