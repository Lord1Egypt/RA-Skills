# Reference: Original Text — Engineering Cybernetics

Direct excerpts from Qian Xuesen (钱学森) & Song Jian (宋健), *Engineering Cybernetics*
(工程控制论). Used here under fair use for scholarship and skill development. The original
book and its mathematical foundations are the authoritative source; this skill is a faithful
interpretation, not a replacement.

---

## §1.1 稳定性的基本要求（节选）

> 对于控制工程来说，稳定性是第一个要求。一个系统即使能在某些工作点给出正确
> 的输出，但在扰动下发散、振荡或泄漏，这个系统就是**不稳定**的——无论其设计
> 多么巧妙，都是没有实用价值的。

This is the anchor for the law "Stability before everything." An LLM must verify
perturbation behavior before proposing any feature or optimization.

---

## §1.5 控制量与受控量（节选）

> 受控量 x 是必须保持正确的量；控制量 u 是我们有自由施加作用的量。线性
> 调节理论假定变量无界——但物理系统都有界。忽略边界会使"过渡过程时间与
> 步长无关"这一结论在实践中不成立。

This is the anchor for the principle "Name x before u; respect bounds." Every actuator
saturates; every loop must have an explicit bound.

---

## §3.7 反馈的基本作用（节选）

> 反馈同时提高了准确度和响应速度。开环系统没有从误差中恢复的路径；闭环
> 系统通过"作用→观测→校正"实现收敛。

This is the anchor for "Closed loop beats open loop." After every non-trivial change,
observe the actual state before declaring success.

---

## §6.3 多变量控制的解耦（节选）

> 当两个变量之间不应相互干扰时，应当使交叉项为零——隔离、单一职责、纯函数、
> 无共享可变状态。一旦对角化，每个子系统就可以作为独立的单变量系统设计，
> 从而大幅简化问题。

This is the anchor for "Decouple what hurts, coordinate what helps."

---

## §11 时滞系统（节选）

> 时滞是稳定性的敌人。在回路延迟很大时，提高增益往往不是解决滞后响应的
> 方法——它会 pushing the system toward instability。应当降低回路增益，或添加
> 阻尼，或缩短回路。

This is the anchor for "Never crank gain on a delayed loop; add damping instead."

---

# Book 2 — 金观涛《控制论与科学方法论》

Direct excerpts from 金观涛, *控制论与科学方法论* (Cybernetics and Scientific Methodology).
Used under fair use for scholarship and skill development. The original book is the
authoritative source; this skill is a faithful interpretation, not a replacement.

---

## §1.1 可能性空间（节选）

> 控制的概念与事物发展的可能性密切相关。我们将事物发展变化中面临的各种可能性
> 集合称为这个事物的可能性空间。它是控制论中最基本的概念。
>
> 被控制的对象必须存在着多种发展的可能性。如果事物的未来只有一种可能性，就无
> 所谓控制了……被控制的对象不仅必须存在多种发展的可能性，而且，人可以在这些
> 可能性中通过一定的手段进行选择，才谈得到控制。

This is the anchor for the principle "Name the possibility space; control is narrowing
possibilities." A change that does not reduce the uncertainty about which state the system
will be in is not control — it is motion.

---

## §1.6 共轭控制（节选）

> 当人们要扩大控制范围的时候，通常要用到一种叫共轭控制的方法……它专门研究如何
> 将一件人们无法完成的工作变成能够完成的工作。
>
> 曹冲用大船的沉浮先把象的重量变换成石头重量……再称出石头的重量……最后又将
> 石头的重量变换成大象的重量。三步连起来可以写成 L⁻¹AL，它表示先实行 L，再
> 实行 A，最后实行 L⁻¹。
>
> 几乎人类制造和使用的一切工具，本质上都包含有这样一个控制范围扩大的过程。

This is the anchor for "When a problem is uncontrollable in its current form, transform it
(L → A → L⁻¹) rather than brute-force."

---

## §1.7–§1.8 负反馈调节（节选）

> 负反馈调节的本质在于设计了一个目标差不断减少的过程，通过系统不断把自己控制
> 后果与目标作比较，使得目标差在一次一次控制中慢慢减少，最后达到控制的目的。
>
> 负反馈控制之所以应用如此广泛，如此有效，就是因为它可以把某种有限的控制能力
> 累积起来，扩大了控制能力。每一次反馈，实际都是将上一次作为输出的可能性空间
> 作为输入，让控制机构在这个已被缩小了的范围内进行新的选择。
>
> 用通常的话来说，负反馈调节就是"做起来看"。

This is the anchor for "Feedback amplifies a weak controller into a strong one; iterate
instead of guessing once."

---

## §2.4 信息与控制的依存关系（节选）

> 传递信息需要我们实行某种控制，反过来，控制过程又必须依赖信息的传递。很多时
> 候，我们不能实现有效的控制，是没有获得足够的信息之故。
>
> 实行控制需要获得足够的信息量，这是一条重要的原理。

This is the anchor for "When control fails, suspect a missing information channel before a
missing actuator." Adding force without feedback is open-loop control.

---

## §3.3 系统的稳态结构（节选）

> 一个互为因果的体系可以因自身的相互作用而处于一种不变的稳定的状态，一般干扰
> 都不会破坏这种状态……我们将整个系统处于稳态结构的条件是系统的每一个子系统都
> 处于稳定态。它们的相互作用保持着各自的稳定。
>
> 系统总是自动趋于稳态结构。

This is the anchor for "Stability is a structure property; to change stable behavior, change
the structure, not just the inputs." See `references/system-evolution.md`.

---

## §3.7 超稳定系统（节选）

> 超稳定系统有一个重要特点，就是靠不稳定来维持稳定。
>
> 超稳定机制是一种重新寻找稳定的机制，一直到找到原有的稳态结构，系统才回到不
> 变状态……超稳定系统有一种特殊的现象，那就是周期性地出现稳定——不稳定——稳定
> 现象。

This is the anchor for "Some instability is a repair mechanism, not a failure. Don't patch
over the repair cycle."

---

## §4.2 质变可以通过飞跃和渐变两种方式实现（节选）

> 质态之间的转化既可以通过飞跃来实现，也可以通过渐变来实现……突变理论的核心
> 思想正是稳态结构。
>
> 同一个质变过程，在不同的条件下可以采取不同的方式进行。

This is the anchor for "The same change can be safe (gradual) or catastrophic (leap)
depending on conditions; near a fold, the same change is a leap." See
`references/system-evolution.md`.

---

## §5.1 黑箱认识论（节选）

> 控制论把人们认识和改造的对象看作黑箱。
>
> 一部分是客体对主体的作用……可以用一组变量来表示，被称为这个客体的可观察变
> 量。另一部分是主体对客体的主制作用……被称为这个客体的可控制变量。
>
> 任何客体除了可观察变量和可控制变量之外，还有一大批尚不可观察和尚不可控制的
> 变量。正是从这个意义上，控制论把一个客体称为黑箱。

This is the anchor for "Treat every system as a black box; your model is a hypothesis about
I/O, not the internals." See `references/black-box-epistemology.md`.

---

## §5.4 理论的清晰性（节选）

> 一个模型，或者说一种理论，不论是否正确，只有具备了清晰性，才能在"实践——理论
> ——实践"的反馈中不断得到修正而逼近客观真理。也就是说，一种理论只有具备了清晰
> 性，才是可以被检验的。
>
> 理论的清晰性和波普尔提出理论的可证伪性是一致的……都要求理论给出信息量。

This is the anchor for "Make your model falsifiable; state what observation would prove it
wrong before acting."

---

## §5.6 反馈过度（节选）

> 任何负反馈调节系统如果出现反馈过度，都会从一个逐步逼近目标的稳定过程转化为
> 振荡过程。
>
> 在逼近过程中出现了反馈过度的现象，不管系统的运动属于哪一层次的，都会发生振
> 荡……使我们的认识从一种极端走向另一种极端，从一种片面性走向另一种片面性。

This is the anchor for "If each correction overshoots, reduce gain rather than reversing
direction. Reversal is not convergence — it is oscillation."
