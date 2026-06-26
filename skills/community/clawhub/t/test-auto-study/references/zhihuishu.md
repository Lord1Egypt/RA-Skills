# zhihuishu

## Default profile

Use profile:

```bash
zhihuishu
```

## Site

`https://onlineweb.zhihuishu.com`

## Core policy

## Page structure

- If the page snapshot does not provide clickable refs for A/B/C/D options, directly use CDP `Runtime.evaluate` to click the corresponding `label` element on the page to select the option
- On this page, single-choice question options often appear as a `label` wrapping a `div` that displays the letter; after being selected, the class of that letter `div` usually contains `bg-mainBg`
- The page title is usually `作业考试` or `答题页`
- A `提交作业` button is usually visible at the top
- The question format may be one question per page

## Workflow

### Process order

1. Locate problem
2. Preprocessing
3. Perform
4. Submit

### Locate problem

- First confirm the current active tab and URL; the target page should be located at `examloop.zhihuishu.com/exam/...`.

### Preprocessing

1. Create the task directory
2. Quickly click through every question, with a 0.2s interval between each click
3. Traverse every question again and take screenshots; screenshots must use the `--full` command, with a 0.1s interval between each click
4. Analyze all images and write the question and options of each question into `markdown`

### Perform

**Only start this step after the markdown file contains all questions and the final answers have already been appended**.

1. Analyze the questions in `markdown` one by one, and add the answer for each question to the end of the file
2. Apply the answers to the questions according to the answers in `markdown`

### Submit

- Before submission, check whether all questions have already been selected and are consistent with the answers recorded in md
- After clicking submit, a second confirmation popup may appear
- Just record the final score at the end of md
- After applying the answers, verify again whether the currently selected letter of the current question is consistent with the target answer; you may also check whether `答题进度` increases incrementally, and it should reach `100%` when all are completed
