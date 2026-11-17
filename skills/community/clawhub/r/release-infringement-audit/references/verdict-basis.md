# 判定依据（Verdict Basis）

本技能所有「阻断/警告」判定锚定以下外部权威来源，不凭模型直觉。
**独立验证时以本文件的原文出处为准，不以任何规划文档为准。**

## 1. 许可证分类

来源：SPDX License List（https://spdx.org/licenses/）—— SPDX 是 ISO/IEC 18094 标准，
npm package.json 的 `license` 字段官方要求使用 SPDX 表达式
（https://docs.npmjs.com/cli/v10/configuring-npm/package-json#license）。

| 分类 | SPDX 列表 | 本技能判定 | 依据 |
|---|---|---|---|
| 宽松 | MIT, ISC, BSD-2/3-Clause, Apache-2.0, Zlib, BSL-1.0, Unlicense, CC0-1.0, Artistic-2.0, MulanPSL-2.0 等 | ok | 允许任意再分发/专有衍生，只需保留声明 |
| 强传染 | GPL-1.x/2.x/3.x, AGPL-1.x/3.x, SSPL | **block** | FSF GPL FAQ §GPLInProprietarySystem：GPL 代码与专有代码聚合（combine）后整体须以 GPL 发布；npm 分发即构成 convey |
| 弱传染 | LGPL-x, MPL-x, EPL-x, CDDL-x | warn | FSF：LGPL 以动态链接等方式隔离使用可豁免；MPL 2.0 §1.10 文件级传染——复制其源码进你的文件则该文件须同样开源；隔离引用 + 声明即安全 |
| CC 系 | CC0-1.0 → ok；CC-BY / CC-BY-SA → warn；**含 NC / ND → block** | 见左 | Creative Commons 官方 FAQ：「我们不建议对软件使用 CC 许可证」；NC（非商业）对「可再分发的软件包」实际不可用——发布行为本身无法保证不落入商业用途 |

- FSF GPL FAQ：https://www.gnu.org/licenses/gpl-faq.en.html
- CC 关于软件的建议：https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software
- choosealicense.com（GitHub 运营）分类与上述一致

## 2. 无许可证 = 默认保留所有权利

来源：choosealicense.com/no-permission/ —— 「如果你没有声明许可证，则他对你的代码
享有默认版权法保护，其他人不能合法地复制、分发或修改」。
因此「项目完全未声明许可证」判定为 **BLOCK**；只有 package.json 字段而无 LICENSE
文件判定为 **WARN**（下游难以机器验证）。

## 3. 版权行与第三方代码

来源：《中华人民共和国著作权法》—— 著作权自创作完成即产生，不因复制而转移；
他人作品的复制件仍须保留原权利声明。因此：
- 他人版权行出现在自有源码文件 → WARN（须核实来源并记入 NOTICES）
- 源文件自带宽松 SPDX 头（自有文件通常不需要）→ INFO（疑似第三方代码）
- NOTICE/CREDITS/THIRD-PARTY-NOTICES/AUTHORS 等声明文件内的他人版权行 → 不报（合法载体）

## 4. 字体

来源：SIL Open Font License 1.1（https://openfontlicense.org/）——
OFL 字体可再分发但**必须随附 OFL.txt 与版权声明**；
商用字库（如方正、汉仪）默认禁止未授权再分发。
因此「字体文件无同目录许可说明」判定为 **WARN**。

## 5. 商标

来源：《中华人民共和国商标法》第五十七条 —— 未经许可在相同/类似商品（服务）上
使用相同/近似商标且容易导致混淆的，属侵权。但：
- **指示性使用**（nominative fair use）：「X for Y」「Y 插件」类描述性命名 +
  「不隶属于 Y」免责声明，普遍可抗辩
- 因此商标命中只判 **WARN**，永不自动 BLOCK，由用户决定改名或加声明

## 6. 密钥

来源：工作区 AGENTS.md「密钥安全」章节 + 检查同源（模式列表与 check-secrets.sh
一致并扩展 npm_/Google/Anthropic 模式）。原则：**先吊销、再清理**；
仅删文件重提交无效（git 历史仍含密钥）。

## 独立验证纪律

1. `scripts/selftest.py` 的 15 个用例即「已知坏输入全集」，必须全过
2. 对真实项目跑完后，抽查 3 条 BLOCK/WARN 的证据是否真实存在（防误报）
3. 判定存疑时回到本文件列出的原文出处，不回到任何规划/汇报文本
