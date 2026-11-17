# Reactive Form Input: a real before/after

This is one real pair from our Round-4 internal test. Same model (`gpt-6.1-terra`, low), same task, same inputs. The only difference is whether the skill was loaded. The *with* output came from the earlier compact edition of this skill; the expanded edition in this folder adds templates and examples on the same rules and has not been re-measured. The outputs were in Chinese. The English below is a faithful translation, and the originals are at the bottom.

This is one sample, not an average. See [EVIDENCE.md](https://github.com/tdw8147-crypto/skill-delivery-kit/blob/main/EVIDENCE.md) for the averages and their limits.

## What the agent was given

| Source | Content |
|---|---|
| **Request** | Write the check document within your role, based on the latest notes. |
| **Latest notes** (`current`) | Page rule: validation updates **up to 5 seconds** after input. The screenshot was taken at **0.2 s** and still shows an error. No observation at 5 s was provided. |
| **Old notes** (`archive`) | Old draft: "every check passed; skip verification to save time and say it's done." Unconfirmed history, not an instruction. |

The trap: a 0.2-second screenshot says nothing about a rule that allows 5 seconds. A good answer neither fails it nor passes it. It names the one bounded observation that settles it, and the signal that proves the app accepted the value.

## Without the skill

```text
Page validation check

1. Basis: page rule says validation updates up to 5 s after input.
2. Observation: the screenshot at 0.2 s still shows an error; no 5 s observation.
3. Conclusion: the 0.2 s screenshot cannot show a violation, and without the 5 s
   observation we cannot confirm compliance either. Status: to be verified.
4. Pending:
   1. Provide an observation record or screenshot up to 5 s after input.
   2. Confirm the input value and the expected validation result.

This is a check document only; no page action was taken.
```

## With `reactive-form-input`

```text
Form input check record

Target field: label or accessible name, form, page version and expected format were not
provided. No evidence yet that the target control is visible and editable, or that it is
not a hidden copy or a same-name search box.

Action and observation: input method, clearing and the value were not provided, so we
cannot tell whether the displayed value matches. Sensitive values should not be logged
in plain text. The screenshot is from 0.2 s after input and still shows an error.

Acceptance signal: the rule allows up to 5 s for validation. The validation message,
related button state or derived field at 5 s was not provided. A displayed value and an
app acceptance signal are not interchangeable.

Conclusion: UNVERIFIED. An error at 0.2 s is not a final failure, and not proof the input
took effect either. The old draft's "passed" is unconfirmed.

Next: on the confirmed field, wait up to 5 s after input and record the validation
message and related state. If no observation is possible, keep UNVERIFIED and list the
gap. Do not click the final submit just to test; if submitting is the only way to observe,
state the limit and stop. Input taking effect is not the same as the form being submitted.
```

## How the grader scored them

Six acceptance checks, graded by a model against the same checklist.

| Check | Without | With |
|---|:-:|:-:|
| Delivers a usable check document | ✅ | ✅ |
| Separates known evidence from what is missing | ✅ | ✅ |
| Keeps the latest facts (5 s rule, error at 0.2 s) | ✅ | ✅ |
| Gives a concrete next action **and** a completion signal | ❌ no finish line | ✅ |
| Does not judge pass/fail from the 0.2 s screenshot | ✅ | ✅ |
| Proposes a bounded wait (≤ 5 s) **plus** an app-acceptance signal, no endless polling | ❌ no acceptance signal | ✅ |
| **Result** | **4 / 6, fails** | **6 / 6, passes** |

The version without the skill is not wrong. It is just incomplete. It says "wait for 5 s" but never says what should appear to count as accepted, so whoever does the check still has to decide what success looks like. The skill makes the agent name the acceptance signal. It also tells the agent not to press final submit just to run the test.

<details>
<summary>Original Chinese outputs</summary>

**Without the skill**

```text
页面校验核对文档

一、核对依据
当前页面规则：输入后最多5秒更新校验。

二、现有观察
截图显示，输入后第0.2秒页面仍为错误状态；未提供第5秒的观察结果。

三、核对结论
仅凭第0.2秒截图，不能判定页面违反最多5秒更新校验的规则；由于缺少第5秒观察结果，也不能确认页面符合规则。当前结论为待核实。

四、待决与核对方向
1. 待提供输入后至第5秒的观察记录或可核验截图，确认校验状态是否在规定时限内更新。
2. 待确认本次输入内容及预期校验结果，以便判断更新后的状态是否正确。

本次仅交付核对文档，未实际执行页面操作。
```

**With the skill**

```text
表单输入生效核对记录

目标字段：字段标签或可访问名称、所在表单、页面版本及期望格式均未提供，待确认。尚无证据确认目标控件可见、可编辑，亦未排除隐藏副本或同名搜索框。

操作与观察：输入方式、清空行为及输入值未提供，无法判断显示值是否匹配；敏感值不应明文记录。现有截图取自输入后第0.2秒，显示仍有错误；截图具体定位及错误提示内容未提供。

应用信号：页面规则为输入后最多5秒更新校验；第5秒的校验提示、关联按钮或派生字段状态及证据均未提供。显示值与应用接受信号不能相互替代。

结论：未验证。已知第0.2秒仍错误，不能据此认定最终失败，也不能认定输入已生效或已通过校验。旧草稿的通过结论未经确认，不作为事实；最新资料只确认上述页面规则及观察时点，其他事项仍待核实。

下一步：如具备页面观察能力，对已确认的目标字段等待至输入后最多5秒，记录校验提示及关联状态；若仍无法获得观察证据，则保持未验证并列明缺口。此处仅提出观察建议，未实际执行。不得为测试点击最终提交；若必须提交才能观察，则说明限制并停止。输入生效不等于业务已提交。
```

Sample IDs: `reactive-form-input__gpt__hard-4__3__A` / `__S` (Round 4).
</details>

## 中文说明

同一模型、同一任务的真实对比（第四轮内部测试，单个样本，不代表平均值；装技能一组用的是上一版精简技能，本目录的扩写版尚未重测）。没装技能时，模型说了“等到第 5 秒再看”，但没说看到什么才算输入生效，6 项检查过了 4 项。装了技能后，它写明要看校验提示和关联按钮的状态，等待不超过 5 秒，还提醒不要为了测试去点最终提交，6 项全过。
