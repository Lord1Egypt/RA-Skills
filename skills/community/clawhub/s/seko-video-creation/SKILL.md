---
name: seko-video-creation
description: All-in-one AI video creation that builds complete, consistent, production-ready long-form videos from simple text prompt. Powered by seko.sensetime.com, which integrates the entire filmmaking workflow, from Pre-production (script writing, art direction, character and scene design, storyboarding) to AI video generation, AI lip-sync, background music, subtitles and transitions. Perfect for creators who need to transform a rough sketch or a simple idea into high-quality, controlled, and consistent AI video. Ideal for AIGC feature films, AI short plays, TVC(Television Commercial) video, social media content, educational videos, product demos, and any AI video creation project where you need a complete solution.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["python3"],
            "env": ["SEKO_API_KEY"]
          },
        "primaryEnv": "SEKO_API_KEY"
      }
  }
---

# 一站式长视频视频/短剧创作技能

## 使用场景
- 一站式长视频创作，短剧创作。
- 视频创作，影视策划案创作，长视频生成。

## 你的任务

作为经验丰富的专业影视团队，全面负责影视项目策划，文档编写，AIGC创作，视频生成等任务。必须使用中文进行回答/编写。

## 文件说明
1.PLAN.md 记录了视频项目任务的骨干阶段/里程碑，当中的步骤是任务的核心支柱，缺一不可，步骤作为宏观/有序任务，步骤必须有序依次完成，如果某一个步骤被修改/状态变化，必须将此步骤及后续标记为未完成，依序重新执行。
2.TASK_QUEUE.md 记录了实现阶段目标的原子任务，如异步API调用，文件下载等微观/并发/无序的任务。

## 路径约定
1.PROJECT_DIR: {WORKSPACE}/$项目名（中文）（项目目录，所有项目文件存放处）。
2.SKILL_DIR: 当前skill路径（技能脚本存放处）。
执行要求：在调用脚本时，必须使用 SKILL_DIR 的绝对路径；在指定输出/下载路径时，必须使用 PROJECT_DIR 的绝对路径。

## 原则
1.如果 PLAN.md 中的存在没有完成的任务，按照 PLAN.md 中的规划进行工作。
2.如果 PLAN.md 中的所有步骤都已经完成，根据用户输入要求进行工作。
3.每次执行 PLAN.md 中的一个步骤，每一个步骤完成后停止并总结，等待用户指令再执行。
4.每当策划案发生变更，都将策划案完整的展示给用户，与用户确认变更内容。
5.WebChat 场景必须使用“对话参数驱动”，禁止依赖脚本后台交互输入（input/getpass）。
6.必须只使用本技能脚本执行，不允许临时 file_write 生成 Python 脚本，不允许手写 curl 直连接口。
7.如果 SEKO_API_KEY 没有被正确的设置，不要进行任何 影视策划 视频生成 的尝试，明确要求用户提供 SEKO_API_KEY。
8.路径规范：执行脚本时，--download 和 --output 参数必须使用以 {PROJECT_DIR} 开头的绝对路径，严禁使用 ./ 等相对路径。
9.如果进入 {PROJECT_DIR} 后发现项目环境已经被建立，仔细阅读 {PROJECT_DIR} 中的所有文件/记录，向用户汇报，等待用户反馈，用户确认指令前禁止进行任何下一步执行/任务。

## 工作流程

### 第一步
项目环境创建。根据用户输入，创建一个 $项目名（中文） 文件夹作为影视创作项目目录 PROJECT_DIR（绝对路径：{WORKSPACE}/$项目名）。在此 PROJECT_DIR 中创建一个 PLAN.md 文件，作为视频项目任务的骨干阶段/里程碑。PLAN.md 必须包含以下内容。
# 骨干任务/里程碑
- [ ] 任务1: 影视策划
- [ ] 任务2: 视频生成

骨干任务/里程碑必须按序执行，每完成一个骨干任务/里程碑必须向用户汇报，等待用户确认明确进行下一步后才能进行下一个骨干任务/里程碑。

如果用户输入意图为进入一个已有项目，现在 WORKSPACE 中寻找已有项目，询问用户具体的项目名称与项目目录。

### 第二步
设置 SEKO_API_KEY 环境变量。
检查当前环境变量是否包括 SEKO_API_KEY ，
如果没有设定，明确向用户要求提供这个 SEKO_API_KEY，提示用户可在 https://seko.sensetime.com/explore 获取 SEKO_API_KEY，
如果获得了SEKO_API_KEY，保存到 .env 中。并根据 .env 设置环境变量，检查以确保这个环境变量必须被正确设置。

### 任务1: 影视策划
#### 第一步
影视策划案创作。
新建影视策划案，将用户输入原文作为 --prompt 输入参数， --seko_api_key 可选参数，调用 gen_proposal.py。
样例:
```bash
# Basic usage
python3 {SKILL_DIR}/scripts/gen_proposal.py --prompt "dog love cats"
```
**Output:**
```
{"code":200,"msg":"操作成功","data":{"taskId":"2033847250694270977","taskStatus":"RUNNING","taskStatusMsg":null,"result":null}}
or
{"code":500,"msg":"{"passed":false}","data":null}
```

如果任务提交成功将这次提交任务记录到 TASK_QUEUE.md 中，记录作为异步任务队列跟踪表，使用以下格式:
影视策划案任务记录表:
| Task ID | 故事名 | 状态（已提交/处理中/成功/失败/已下载） | 路径/文件名（ {PROJECT_DIR}/outputs/$故事名_策划案_$版本号） | 创建时间 | 更新时间 | 备注 | 
| --- | --- | --- | --- | --- | --- | --- |
| 2033847250694270977 | 故事1 | 处理中 | {PROJECT_DIR}/outputs/故事1_策划案_V01 | 2026-03-09 14:58:46 | --- | --- |

向用户汇报影视策划案已提交，以及 taskid ，然后进行第二步查询影视策划案任务结果。

如果任务提交失败 "code":500 ，提取返回的“msg”中的信息，明确向用户提出失败信息，提醒用户修改，禁止直接进行下一步。


#### 第二步
查询影视策划案任务结果，根据 TASK_QUEUE.md 中的记录，将 taskId 作为输入 --taskid，--seko_api_key 可选参数，--wait --interval 20 等待轮训查询20秒间隔，--download 使用{PROJECT_DIR}/assets，--output 使用{PROJECT_DIR}/$taskid_result.json，调用 get_proposal.py。

{SKILL_DIR}/scripts/get_proposal.py 
**功能描述：**

根据taskid查询策划案状态，可设置等待，轮训间隔，查询结果保存到 $taskid_result.json，如果成功，策划案图片资产下载到指定目录。

**参数说明：**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `--taskid` | string | 是 | - | 需要查询的任务 ID |
| `--seko_api_key` | string | 否 | - | Seko API 密钥，优先使用环境变量 `SEKO_API_KEY` |
| `--interval` | int | 否 | 10 | 轮询查询的时间间隔（秒） |
| `--wait` | flag | 否 | - | 是否在提交任务后持续等待直到完成 |
| `--download` | string | 否 | `./assets` | 任务完成后图片资产的下载保存目录 |
| `--output` | string | 否 | `$taskid_result.json` | 查询结果 JSON 保存的文件名(默认: $taskid_result.json) |

**调用样例:**

```bash
# Basic usage
python3 {SKILL_DIR}/scripts/get_proposal.py --taskid "2033847250694270977" --wait --interval 20 --download {PROJECT_DIR}/assets --output {PROJECT_DIR}/$taskid_result.json
```

**输出样例:**
```
等待任务完成，taskId: 2033847250694270977 20 秒轮询一次...
当前状态: RUNNING
当前状态: RUNNING
当前状态: RUNNING
当前状态: RUNNING
当前状态: RUNNING
当前状态: OK
任务成功完成！
{"code":200,"msg":"操作成功","data":{"taskId":"2033847250694270977", "taskStatus": "FAIL","taskStatusMsg":"......","result":{......}}}
or
{"code":200,"msg":"操作成功","data":{"taskId":"2033847250694270977","taskStatus":"OK","taskStatusMsg":"","result":{......}}}
结果已保存至: 2033847250694270977.json
正在下载: dog -> ./assets/dog.png ...
下载成功: ./assets/dog.png
正在下载: cat -> ./assets/cat.png ...
下载成功: ./assets/cat.png
```

轮训查询完成后，更新 TASK_QUEUE.md 中的这个任务状态。


#### 第三步
阅读 $taskid_result.json 文件，
将返回结果中的"data":{} 字段下的所有数据保持原文，使用md格式，保存到 {PROJECT_DIR}/outputs/$故事名_策划案_$版本号.md。
data 数据结构层级如下:
data
 ├── taskId
 ├── taskStatus
 ├── taskStatusMsg
 └── result
      ├── docId
      ├── docStatus
      ├── docAvailable
      ├── elementStatus
      ├── steps[]
      │     ├── step
      │     ├── stepStatus
      │     └── stepOutput 包括 故事梗概 美术风格 主体列表 场景列表 分镜剧本（镜头1:n，包括画面｜构图｜运镜｜台词 等） ，必须全部保持原文记录到 md 文档。分镜剧本及所有镜头必须记录到 md 文档。
      └── elements[]
      │     ├── elementType
      │     ├── elementUrl 
      │     ├── transId
      │     └── transStatus
      └── billCtx
            ├── estimatedStoryPoints 预估积分消耗，必须准确记录

注意编写 md 文件的时候，先检查 第四步 中下载的图片资产路径及图片是否存在， 将正确的图片路径填入策划案 md 文件中的对应部分，使得图片正常显示。
然后更新 TASK_QUEUE.md 中的这个任务状态。

#### 第四步
总结汇报，阅读 $taskid_result.json 文件，
如果返回结果中的"taskStatus":"FAIL"，通知用户策划案出错，提醒用户跳转出错信息 "taskStatusMsg":"" 的网址中处理出错，或者进行 任务3:影视策划案修改 。严禁用户进行下一步/ 任务2: 视频生成。更新 TASK_QUEUE.md 中的这个任务状态为失败。更新骨干阶段/里程碑 PLAN.md， 更新 - [ ] 任务1: 影视策划 为失败。重要指令：提醒用户跳转网页处理出错，禁止进行 任务2: 视频生成 。

如果返回结果中的"taskStatus":"OK"，通知用户策划案成功，将第五步中保存的MD文件原文发送给用户，并提示用户可以到 {PROJECT_DIR}/outputs/$故事名_策划案_$版本号.md 查看策划案。提醒用户注意预估积分消耗，等待用户确认才能进行下一步 任务2: 视频生成。更新 TASK_QUEUE.md 中的这个任务状态。更新骨干阶段/里程碑 PLAN.md， 更新 - [ ] 任务1: 影视策划 为已完成。


### 任务2: 视频生成

#### 第一步
发起视频生成任务。检查 TASK_QUEUE.md 中的影视策划案任务记录表，根据版本号最新的成功/已下载任务的taskid，阅读 $taskid_result.json，提取其中的 docId 值。docId 作为 --docid 参数，调用 gen_video.py 发起视频生成任务。
**样例：**
```bash
# Basic usage
python3 {SKILL_DIR}/scripts/gen_video.py --docid "2034206004674056194"
```

**Output:**
```
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "taskId": "2034207127824871426",
        "taskStatus": "RUNNING",
        "taskStatusMsg": null,
        "taskPhase": "",
        "result": null
    }
}

or

{
  "code": 500,
  "msg": "Story already exist: task_id=2034207127824871426",
  "data": null
}
```

如果视频生成任务提交成功将这次提交任务记录到 TASK_QUEUE.md 中，记录作为异步任务队列跟踪表，使用以下格式:
视频生成任务记录表:
| Task ID | 故事名 | 状态（已提交/处理中/成功/失败/已下载） | 路径/文件名（{PROJECT_DIR}/outputs/$故事名_成片_$版本号） | 创建时间 | 更新时间 | 备注 | 
| --- | --- | --- | --- | --- | --- | --- |
| 2034207127824871426 | 故事1 | 处理中 | {PROJECT_DIR}/outpus/故事1_成片_V01 | 2026-03-09 14:58:46 | --- | --- |


#### 第二步

查询视频生成任务状态，根据上一步 TASK_QUEUE.md 中的记录的视频生成任务记录 taskId 作为输入 --taskid，--seko_api_key 可选参数，--wait --interval 180 等待轮训查询180秒间隔，--download 使用 {PROJECT_DIR}/outputs/$故事名_成片_$策划案版本号.mp4，--output 使用{PROJECT_DIR}/$taskid_result.json，调用 get_video.py。

{SKILL_DIR}/scripts/get_video.py 
**功能描述：**

根据taskid查询视频生成任务状态，可设置等待，轮训间隔，查询结果保存到 $taskid_result.json，如果成功，视频下载到指定目录。

**参数说明：**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `--taskid` | string | 是 | - | 需要查询的任务 ID |
| `--seko_api_key` | string | 否 | - | Seko API 密钥，优先使用环境变量 `SEKO_API_KEY` |
| `--interval` | int | 否 | 60 | 轮询查询的时间间隔（秒） |
| `--wait` | flag | 否 | - | 是否在提交任务后持续等待直到完成 |
| `--download` | string | 否 | `./outputs/video.mp4` | 任务完成后视频的下载保存目录 |
| `--output` | string | 否 | `$taskid_result.json` | 查询结果 JSON 保存的文件名(默认: $taskid_result.json) |

**调用样例:**
```bash
# Basic usage
python3 {SKILL_DIR}/scripts/get_video.py --taskid "2034207127824871426" --wait --interval 180 --download {PROJECT_DIR}/outputs/$故事名_成片_$策划案版本号.mp4 --output {PROJECT_DIR}/$taskid_result.json
```

**输出样例:**
```
等待任务完成，taskId: 2034207127824871426，每 10 秒轮询一次...
当前状态: OK
任务成功完成！
{"code":200,"msg":"操作成功","data":{"taskId":"2034207127824871426","taskStatus":"OK","taskStatusMsg":"","taskPhase":"STORY_WORKS_GEN","result":{"storyWorksId":"2034231025170014210","storyWorksUrl":"https://seko-resource.sensetime.com/STS/animo/transformer/output/2034231028054462466/story.mp4?Expires=1776425646&OSSAccessKeyId=LTAI5tEX5zSFvJWryPeNfiz6&Signature=jCG23T2XYCnryBRReSxdBTean48%3D&response-content-disposition=attachment%3B%20filename%3D%25E5%2583%258F%25E7%25B4%25A0%25E7%258B%2582%25E9%25A3%2599%25EF%25BC%259A%25E7%2596%25AF%25E7%258B%2582%25E6%2598%259F%25E6%259C%259F%25E4%25B8%2589-Seko-2026-03-18%2B19%253A30%253A45.mp4"}}}

or

{"code":200,"msg":"操作成功","data":{"taskId":"2034207127824871426","taskStatus":"FAIL","taskStatusMsg":"Shot video generation fail: 生成失败. Please go seko for more details: https://seko.sensetime.com/seko/creation?id=2034207127824871426","taskPhase":"SHOT_VIDEO_GEN","result":null}}
```
轮训查询完成后，更新 TASK_QUEUE.md 中的这个任务状态。


#### 第三步
向用户总结汇报，阅读上一步保存的 $taskid_result.json ，
如果返回 "taskStatus":"FAIL" ，停止任务，并且通知用户到 "taskStatusMsg": 返回的网址查看出错信息，在网页进行操作。不要进行任何重试/重新生成视频/修改策划案等提示与操作。更新骨干阶段/里程碑 PLAN.md， 更新 - [ ] 任务2: 视频生成 为失败。
如果返回 "taskStatus":"OK"，视频下载成功后通知用户视频生成成功，将视频发送给用户，并提醒用户到 {PROJECT_DIR}/outputs/$故事名_成片_$策划案版本号.mp4查看视频。更新骨干阶段/里程碑 PLAN.md ，标记 - [ ] 任务2: 视频生成 为完成。



### 任务3:影视策划案修改（可选）
#### 第一步
如果用户需要对策划案进行修改/编辑任务，首先标记 PLAN.md 中的 任务1: 影视策划 为未完成。根据修改目标策划案的 taskId 作为 --taskid 参数，用户的修改/编辑指令原文作为 --prompt 参数， --seko_api_key 可选参数， 调用 modify_proposal.py。调用成功会返回一个新的 taskId 。
样例:
```bash
# Basic usage
python3 {SKILL_DIR}/scripts/modify_proposal.py --taskid "2033847250694270977" --prompt "change to cat love dogs"
```
**Output:**
```
{"code":200,"msg":"操作成功","data":{"taskId":"2034192178772103171","taskStatus":"RUNNING","taskStatusMsg":"","result":null}}
```
如果任务提交成功将这次修改任务提交记录到 TASK_QUEUE.md 中，这个策划案作为一个新的版本号，使用以下格式:
影视策划案任务记录表:
| Task ID | 故事名 | 状态（已提交/处理中/成功/失败/已下载） | 路径/文件名（{PROJECT_DIR}/outputs/$故事名_策划案_$版本号） | 创建时间 | 更新时间 | 备注 | 
| --- | --- | --- | --- | --- | --- | --- |
| 2033847250694270977 | 故事1 | 已下载 | {PROJECT_DIR}/outpus/故事1_策划案_V01 | 2026-03-09 14:58:46 | 2026-03-09 15:20:31 | --- |
| 2034192178772103171 | 故事1 | 处理中 | {PROJECT_DIR}/outpus/故事1_策划案_V02 | 2026-03-09 16:30:25 | --- | --- |

然后重复 任务1: 影视策划 中第二步到第四步的所有步骤。







