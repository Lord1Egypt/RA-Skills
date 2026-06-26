# Cleanup Guide — Worked Example

A concrete walkthrough that complements the rules in `cleanup_guide.md`. Read this when you want to see how all the principles combine on a real (short) video. Skip if you just need the rules.

---

## Source

A short Bilibili video (87 seconds) about Chinese garden corridor design. It illustrates the full cleanup loop:

- ASR correction (homophone errors, a misrecognized classical poem citation)
- The "no forced headings" rule for short videos
- Trimming an unresolvable trailing fragment instead of annotating

## Raw `sentences.txt` (output of `srt_to_sentences.py`)

```
假如让你在这条长廊从头走到尾你最容易注意到哪棵树尽头的树那如果我把它变成曲廊呢那就先看到绿色黄色最后才是粉色没错因为正前方是人最容易注意到的点古人为了让你看到更多的景色他们就会利用曲折较大的道路改变你视线的方向他们将这种手法称为一步一景那现在问题来了
假如我要在这个湖边建一条只看右侧的长廊如果要一步你会怎么做沿湖也建一条去狼并在左边砌一堵墙这样人就能看到右边不一样的风景但这个湖岸太直曲廊曲折幅度小又只看右侧看的景色都长一个样那简单把这段曲梁变得更曲折就好了你这都快碰到对岸了湖面被遮挡就不好看
既然视野往右的变化太少那不如在上下去做改变只需要把曲梁垂直抬高再次折叠当你走在低处你看到的是被水面反射的树影建筑仰视看到的是职业蓝天若走至高处你低头所见就变成了水底池鱼雨落时抬头又成了白云飞鸟这就是古人的视觉妙手波形长廊而在视觉转动间你就能知道
古人不转回廊半落梅花婉婉香的关起来
```

## Per-video glossary (built before line-by-line correction)

Scan the raw text once; record likely ASR errors with high confidence:

| ASR output | Correction | Evidence / how confirmed |
|---|---|---|
| 去狼 | 曲廊 | Same pinyin (qū láng); context "沿湖也建一条…" requires a noun for a corridor |
| 曲梁 (×2) | 曲廊 | Same pinyin; "梁" (beam) cannot be walked through, but the sentences describe walking |
| 职业蓝天 | 直射蓝天 | "职业 (career) blue sky" is meaningless; "直射 (direct)" is a near homophone fitting "仰视看到的是…" |
| 不转回廊半落梅花婉婉香 | 步转回廊，半落梅花婉娩香 | Confirmed via web search: line is from Su Shi's《减字木兰花·春月》 — original is "**步**转回廊，半落梅花婉**娩**香" |
| 关起来 | (uncertain — leave a margin note) | Sentence "古人…的关起来" breaks at the end; possible candidates include "概括起来"; do NOT guess in the final transcript |

## Sectioning analysis

Scan for structural signals (per `cleanup_guide.md` § Sectioning Heuristics):

- "那如果我把它变成曲廊呢" — weak rhetorical question
- "那现在问题来了" — medium signal
- "既然视野往右的变化太少…那不如…" — medium signal

Three medium-or-weaker signals in 87 seconds. Per the **"no forced headings"** rule, this is borderline at best. Compounded with the video's short length (87s), inserting `##` / `###` headings would fragment a naturally flowing micro-essay. **Decision: no headings.** Use paragraph breaks at the two medium signals; mark key terminology with bold instead.

## After cleanup (the deliverable)

```markdown
# 古人把视觉技巧融入长廊能造出什么中式美学呢

> **来源**：B 站 ｜**链接**：https://www.bilibili.com/video/BV1TpFDz6EEw
> **时长**：1 分 27 秒 ｜**发布**：2026-02-10
> **字幕来源**：AI 自动字幕

---

假如让你在这条长廊从头走到尾，你最容易注意到哪棵树？尽头的树。那如果我把它变成曲廊呢？那就先看到绿色，黄色，最后才是粉色。没错，因为正前方是人最容易注意到的点。古人为了让你看到更多的景色，他们就会利用曲折较大的道路改变你视线的方向——他们将这种手法称为"**一步一景**"。

那现在问题来了：假如我要在这个湖边建一条只看右侧的长廊，如果要"一步一景"，你会怎么做？沿湖也建一条曲廊，并在左边砌一堵墙，这样人就能看到右边不一样的风景。但这个湖岸太直，曲廊曲折幅度小，又只看右侧，看的景色都长一个样。那简单，把这段曲廊变得更曲折就好了？你这都快碰到对岸了，湖面被遮挡就不好看。

既然视野往右的变化太少，那不如在上下去做改变——只需要把曲廊垂直抬高再次折叠。当你走在低处，你看到的是被水面反射的树影建筑；仰视看到的是直射蓝天。若走至高处，你低头所见就变成了水底池鱼，雨落时抬头又成了白云飞鸟。这就是古人的视觉妙手——**波形长廊**。
```

## Decisions made

1. **ASR fixes silently applied** in the body text — the reader sees clean text, not a list of corrections. The glossary / decisions table above is for THIS guide's pedagogical purpose only and **must not** appear in the actual deliverable.
2. **No headings** — applied the "no forced structure" rule.
3. **Paragraph breaks** at the two medium signals, dividing the body into 3 logical paragraphs that mirror the speaker's "basic question → harder question → solution" arc.
4. **Bold key terminology** — `一步一景` and `波形长廊` are the two named techniques the speaker explicitly introduces; bolding them helps the reader scan without imposing artificial section structure.
5. **Final ambiguous fragment dropped** — the closing "古人…的关起来" cannot be resolved with confidence (the cited poem ends mid-thought in the ASR). Per the discipline rule, do not guess. The cleanest action is to omit the unfinished trailing fragment; the body already concludes naturally with "波形长廊". Margin notes are review artifacts and should not appear in deliverables — trim instead.
6. **No footnotes for the poem** — even though the corrected line ("步转回廊，半落梅花婉娩香") is a Su Shi citation, since the trailing fragment was trimmed, the citation is moot. If a poem citation IS retained in another video's transcript, it goes inline as the speaker said it; do not add scholarly footnotes.
