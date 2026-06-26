---
name: vod-aigc-helper
description: 腾讯云点播（VOD）AIGC 接口对接助手。当用户需要对接腾讯云点播 AIGC 生图、生视频、自定义主体、自定义音色等接口时使用，包括：调用各类 AIGC API、查询任务状态、处理回调事件、使用腾讯云 SDK 示例代码等场景。
---

# 腾讯云点播 AIGC 接口对接助手

## 核心文档链接

在回答时，**必须主动提供**以下文档链接供用户参考：

| 功能 | 接口名 | 文档地址 |
|------|--------|---------|
| AIGC 生图接口 | `CreateAigcImageTask` | https://cloud.tencent.com/document/product/266/126240 |
| AIGC 生视频接口 | `CreateAigcVideoTask` | https://cloud.tencent.com/document/product/266/126239 |
| 创建 AIGC 自定义主体 | `CreateAigcCustomElement` | https://cloud.tencent.com/document/product/266/127544 |
| 创建 AIGC 自定义音色 | `CreateAigcCustomVoice` | https://cloud.tencent.com/document/product/266/129120 |
| 创建 AIGC 高级自定义主体 | `CreateAigcAdvancedCustomElement` | https://cloud.tencent.com/document/product/266/129121 |
| 创建 AIGC 自定义主体（Vidu） | `CreateAigcSubject` | https://cloud.tencent.com/document/product/266/129192 |
| 数据结构文档 | - | https://cloud.tencent.com/document/product/266/31773 |
| **API 接口概览**（找不到接口时查这里） | - | https://cloud.tencent.com/document/product/266/31753 |
| 查询任务接口 | `DescribeTaskDetail` | https://cloud.tencent.com/document/product/266/33431 |
| API 密钥文档 | - | https://cloud.tencent.com/document/api/266/31757 |
| 回调事件文档 | - | https://cloud.tencent.com/document/product/266/35579 |
| 子应用管理文档 | - | https://cloud.tencent.com/document/api/266/43744 |
| **AIGC 计费说明（国内站）** | - | https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac |
| **AIGC 计费说明（国际站）** | - | https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419 |
| **AIGC 计费补充文档（最新单价/扣费规则）** | - | https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp |

> 📌 **补充参考文档（更及时）**：官网文档可能存在轻微更新滞后（如新增参数未及时同步），遇到参数疑问时请同时参考以下腾讯文档：
> - 生图/生视频接口参数表：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
> - 接口详细说明文档：https://doc.weixin.qq.com/doc/w3_AUUAAQaDAMYCNbqzKJeSsTSKfdAbP?scode=AJEAIQdfAAowpfCxSPAMkAoQZ9ACc

> 🔍 **找不到接口时**：如果用户要求的接口在上表中找不到，请先查阅 [API 接口概览](https://cloud.tencent.com/document/product/266/31753)，找到对应接口后再跳转到具体文档页面。

## 必须告知用户的关键信息

> 🚨 **计费风险提示（最高优先级，回答时必须主动告知用户）**：
> 腾讯云点播 AIGC 生图、生视频、自定义主体、自定义音色等接口**均为付费接口**，调用即可能产生费用。
> 在生成代码、给出调用示例、回答任何对接问题时，**必须主动且显著地提醒用户阅读计费文档**，避免用户在不知情的情况下产生费用。

### 1. ⚠️ 计费说明（必须主动告知）

**核心提示（每次回答 AIGC 接口相关问题时都必须提及）**：
- 🔴 **AIGC 生图、生视频、自定义主体、自定义音色等接口均为付费接口**，每次成功调用都会产生费用
- 🔴 **任务失败一般不计费，但成功完成的任务（含轮询查询到 `FINISH` 状态的任务）会按实际生成内容（图片张数 / 视频秒数 / 训练时长 / 主体数量等维度）计费**
- 🔴 **不同模型 / 分辨率 / 时长 / 风格的单价不同**，调用前请务必查阅最新单价
- 🔴 **建议先在测试环境用最低规格参数验证流程，确认计费符合预期后再上量**
- 🔴 **建议在腾讯云控制台开启费用预警 / 设置消费限额**，避免因脚本异常或循环调用导致费用激增

**计费文档（必须提供给用户的链接）**：

| 文档类型 | 链接 |
|---------|------|
| 国内站 AIGC 计费说明 | https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac |
| 国际站 AIGC 计费说明 | https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419 |
| **计费补充文档（最新单价 / 扣费规则，更及时）** | https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp |

> 💡 官网计费文档可能存在更新滞后，**最新单价、扣费规则、新模型计费方式请以补充文档为准**。
> 国内账号请以国内站文档为准；海外（International）账号请以国际站文档为准，二者价格体系不同。

**典型计费维度速览**（具体单价以官方文档为准）：
- AIGC 生图：按生成图片张数 + 模型 / 分辨率计费
- AIGC 生视频：按生成视频秒数 + 模型 / 分辨率 / 时长档位计费
- 任务输出物（图片 / 视频）保存在 VOD 中还会产生**存储费用**，计费规则参考点播标准计费

### 2. API 密钥
- 用户需要腾讯云 API 密钥（SecretId + SecretKey）才能调用接口
- 密钥获取文档：https://cloud.tencent.com/document/api/266/31757
- **安全提示**：密钥不要硬编码在代码中，建议使用环境变量或配置文件

### 3. SubAppId（子应用 ID）
- 调用云点播 API 时，**必须填写准确的 SubAppId（子应用 ID）**，否则请求会失败或操作到错误的子应用
- 在腾讯云点播控制台可以查看子应用列表及对应的 SubAppId
- 如果子应用不存在，需要先创建子应用，参考文档：https://cloud.tencent.com/document/api/266/43744
- **如何获取 SubAppId**：登录腾讯云点播控制台 → 左上角切换子应用 → 查看当前子应用 ID

### 4. 异步任务机制
- `CreateAigcImageTask`、`CreateAigcVideoTask` 等生图/生视频接口均为**异步任务接口**，调用后不会立即返回结果
- 接口调用成功后会返回 `TaskId`，需要通过该 TaskId 轮询 `DescribeTaskDetail` 查询任务状态
- 查询接口：https://cloud.tencent.com/document/product/266/33431
- **查询间隔建议 5 秒以上**，避免频繁请求
- 任务状态字段：`PROCESSING`（处理中）、`FINISH`（已完成）、`FAIL`（失败）

### 5. 推荐使用腾讯云 SDK
强烈建议用户使用腾讯云官方 SDK，而非直接拼接 HTTP 请求：

| 语言 | SDK 地址 |
|------|---------|
| Python | https://github.com/TencentCloud/tencentcloud-sdk-python |
| Go | https://github.com/TencentCloud/tencentcloud-sdk-go |
| Java | https://github.com/TencentCloud/tencentcloud-sdk-java |
| Node.js | https://github.com/TencentCloud/tencentcloud-sdk-nodejs |
| PHP | https://github.com/TencentCloud/tencentcloud-sdk-php |
| .NET | https://github.com/TencentCloud/tencentcloud-sdk-dotnet |

> ⚠️ **SDK 版本提示**：如果 SDK 中缺少文档中的某个参数或 Request 类（如 `CreateAigcImageTaskRequest`、`CreateAigcVideoTaskRequest`、`CreateAigcCustomElementRequest` 等），可能是 SDK 版本较旧，需要升级到最新版本。
>
> 💡 **参数参考提示**：官网文档偶有更新滞后，若发现参数与实际不符，请参考补充文档获取最新参数说明：
> - https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
> - https://doc.weixin.qq.com/doc/w3_AUUAAQaDAMYCNbqzKJeSsTSKfdAbP?scode=AJEAIQdfAAowpfCxSPAMkAoQZ9ACc

## 代码示例规范

### Python 示例（使用 Python 3）

#### 安装 SDK
```bash
pip3 install tencentcloud-sdk-python
# 如已安装，升级到最新版本
pip3 install --upgrade tencentcloud-sdk-python
```

#### 完整示例
```python
import os
import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vod.v20180717 import vod_client, models


def create_aigc_image_task(secret_id: str, secret_key: str, sub_app_id: int):
    """调用腾讯云点播 AIGC 生图接口 CreateAigcImageTask
    文档：https://cloud.tencent.com/document/product/266/126240
    数据结构：https://cloud.tencent.com/document/product/266/31773
    sub_app_id: 子应用 ID，必填；如需创建：https://cloud.tencent.com/document/api/266/43744

    ⚠️ 计费提醒：AIGC 生图为付费接口，每次成功生成都会产生费用。
       计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
       计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
       计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
       建议在腾讯云控制台开启费用预警，避免脚本异常导致费用激增。
    """
    try:
        cred = credential.Credential(secret_id, secret_key)
        client = vod_client.VodClient(cred, "")  # VOD 不需要指定 region

        req = models.CreateAigcImageTaskRequest()
        req.SubAppId = sub_app_id  # 必填：子应用 ID
        # 根据文档填写其他参数，详见：https://cloud.tencent.com/document/product/266/126240
        # 如官网文档参数有疑问，参考：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
        # req.Definition = 0  # 模板 ID
        # req.Text = "your prompt here"

        resp = client.CreateAigcImageTask(req)
        print(f"生图任务已提交，TaskId: {resp.TaskId}")
        return resp.TaskId
    except TencentCloudSDKException as e:
        print(f"SDK 异常: {e}")
        raise


def create_aigc_video_task(secret_id: str, secret_key: str, sub_app_id: int):
    """调用腾讯云点播 AIGC 生视频接口 CreateAigcVideoTask
    文档：https://cloud.tencent.com/document/product/266/126239
    数据结构：https://cloud.tencent.com/document/product/266/31773
    sub_app_id: 子应用 ID，必填；如需创建：https://cloud.tencent.com/document/api/266/43744

    ⚠️ 计费提醒：AIGC 生视频为付费接口，按生成视频时长 / 分辨率 / 模型计费，单次费用通常高于生图。
       计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
       计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
       计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
       建议先用最低规格参数验证流程，并在控制台开启费用预警。
    """
    try:
        cred = credential.Credential(secret_id, secret_key)
        client = vod_client.VodClient(cred, "")

        req = models.CreateAigcVideoTaskRequest()
        req.SubAppId = sub_app_id  # 必填：子应用 ID
        # 根据文档填写其他参数，详见：https://cloud.tencent.com/document/product/266/126239
        # 如官网文档参数有疑问，参考：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
        # req.Definition = 0  # 模板 ID
        # req.Text = "your prompt here"

        resp = client.CreateAigcVideoTask(req)
        print(f"生视频任务已提交，TaskId: {resp.TaskId}")
        return resp.TaskId
    except TencentCloudSDKException as e:
        print(f"SDK 异常: {e}")
        raise


def create_aigc_custom_element(secret_id: str, secret_key: str, sub_app_id: int):
    """创建 AIGC 自定义主体 CreateAigcCustomElement
    文档：https://cloud.tencent.com/document/product/266/127544
    sub_app_id: 子应用 ID，必填；如需创建：https://cloud.tencent.com/document/api/266/43744

    ⚠️ 计费提醒：自定义主体训练为付费接口，按训练任务 / 时长计费。
       计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
       计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
       计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
    """
    try:
        cred = credential.Credential(secret_id, secret_key)
        client = vod_client.VodClient(cred, "")

        req = models.CreateAigcCustomElementRequest()
        req.SubAppId = sub_app_id  # 必填：子应用 ID
        # 根据文档填写其他参数，详见：https://cloud.tencent.com/document/product/266/127544

        resp = client.CreateAigcCustomElement(req)
        print(f"自定义主体已创建，TaskId: {resp.TaskId}")
        return resp.TaskId
    except TencentCloudSDKException as e:
        print(f"SDK 异常: {e}")
        raise


def query_task_status(secret_id: str, secret_key: str, task_id: str, sub_app_id: int):
    """轮询查询任务状态（DescribeTaskDetail）
    文档：https://cloud.tencent.com/document/product/266/33431
    注意：AIGC 任务耗时较长，查询间隔建议 5 秒以上
    """
    cred = credential.Credential(secret_id, secret_key)
    client = vod_client.VodClient(cred, "")

    while True:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = task_id
        req.SubAppId = sub_app_id  # 必填：子应用 ID

        resp = client.DescribeTaskDetail(req)
        status = resp.Status

        print(f"任务状态: {status}")
        if status == "FINISH":
            print("任务完成！")
            return resp
        elif status == "FAIL":
            print("任务失败！")
            return resp
        else:
            # PROCESSING - 继续等待，间隔 5 秒以上
            time.sleep(5)


if __name__ == "__main__":
    # 从环境变量读取密钥（推荐方式，避免硬编码）
    # 密钥申请文档：https://cloud.tencent.com/document/api/266/31757
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    # 子应用 ID，在腾讯云点播控制台获取
    # 如需创建子应用：https://cloud.tencent.com/document/api/266/43744
    sub_app_id = int(os.environ.get("VOD_SUB_APP_ID", "0"))

    # 示例：生图并查询结果
    # task_id = create_aigc_image_task(secret_id, secret_key, sub_app_id)
    # result = query_task_status(secret_id, secret_key, task_id, sub_app_id)

    # 示例：生视频并查询结果
    # task_id = create_aigc_video_task(secret_id, secret_key, sub_app_id)
    # result = query_task_status(secret_id, secret_key, task_id, sub_app_id)

    # 示例：创建自定义主体
    # task_id = create_aigc_custom_element(secret_id, secret_key, sub_app_id)
    # result = query_task_status(secret_id, secret_key, task_id, sub_app_id)
```

### Go 示例

#### 安装 SDK
```bash
go get github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/vod/v20180717
```

#### 完整示例
```go
package main

import (
    "fmt"
    "os"
    "strconv"
    "time"

    "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common"
    "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common/errors"
    vod "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/vod/v20180717"
)

// createAigcImageTask 调用生图接口 CreateAigcImageTask
// 文档：https://cloud.tencent.com/document/product/266/126240
// 补充参数参考：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
//
// ⚠️ 计费提醒：AIGC 生图为付费接口，每次成功生成都会产生费用。
//   - 计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
//   - 计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
//   - 计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
//   - 建议在腾讯云控制台开启费用预警，避免脚本异常导致费用激增。
func createAigcImageTask(client *vod.Client, subAppId uint64) (string, error) {
    request := vod.NewCreateAigcImageTaskRequest()
    request.SubAppId = common.Uint64Ptr(subAppId) // 必填：子应用 ID
    // 根据文档填写其他参数
    // request.Definition = common.Int64Ptr(0)
    // request.Text = common.StringPtr("your prompt here")

    response, err := client.CreateAigcImageTask(request)
    if _, ok := err.(*errors.TencentCloudSDKError); ok {
        return "", fmt.Errorf("SDK 错误: %s", err)
    }
    taskId := *response.Response.TaskId
    fmt.Printf("生图任务已提交，TaskId: %s\n", taskId)
    return taskId, nil
}

// createAigcVideoTask 调用生视频接口 CreateAigcVideoTask
// 文档：https://cloud.tencent.com/document/product/266/126239
// 补充参数参考：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
//
// ⚠️ 计费提醒：AIGC 生视频为付费接口，按生成视频时长 / 分辨率 / 模型计费，单次费用通常高于生图。
//   - 计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
//   - 计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
//   - 计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
//   - 建议先用最低规格参数验证流程，并在控制台开启费用预警。
func createAigcVideoTask(client *vod.Client, subAppId uint64) (string, error) {
    request := vod.NewCreateAigcVideoTaskRequest()
    request.SubAppId = common.Uint64Ptr(subAppId) // 必填：子应用 ID
    // 根据文档填写其他参数
    // request.Definition = common.Int64Ptr(0)
    // request.Text = common.StringPtr("your prompt here")

    response, err := client.CreateAigcVideoTask(request)
    if _, ok := err.(*errors.TencentCloudSDKError); ok {
        return "", fmt.Errorf("SDK 错误: %s", err)
    }
    taskId := *response.Response.TaskId
    fmt.Printf("生视频任务已提交，TaskId: %s\n", taskId)
    return taskId, nil
}

// createAigcCustomElement 创建 AIGC 自定义主体 CreateAigcCustomElement
// 文档：https://cloud.tencent.com/document/product/266/127544
//
// ⚠️ 计费提醒：自定义主体训练为付费接口，按训练任务 / 时长计费。
//   - 计费说明（国内站）: https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
//   - 计费说明（国际站）: https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
//   - 计费补充文档（最新单价）: https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
func createAigcCustomElement(client *vod.Client, subAppId uint64) (string, error) {
    request := vod.NewCreateAigcCustomElementRequest()
    request.SubAppId = common.Uint64Ptr(subAppId) // 必填：子应用 ID
    // 根据文档填写其他参数

    response, err := client.CreateAigcCustomElement(request)
    if _, ok := err.(*errors.TencentCloudSDKError); ok {
        return "", fmt.Errorf("SDK 错误: %s", err)
    }
    taskId := *response.Response.TaskId
    fmt.Printf("自定义主体已创建，TaskId: %s\n", taskId)
    return taskId, nil
}

// queryTaskStatus 轮询查询任务状态，间隔 5 秒以上
// 文档：https://cloud.tencent.com/document/product/266/33431
func queryTaskStatus(client *vod.Client, taskId string, subAppId uint64) {
    for {
        request := vod.NewDescribeTaskDetailRequest()
        request.TaskId = common.StringPtr(taskId)
        request.SubAppId = common.Uint64Ptr(subAppId) // 必填：子应用 ID

        response, err := client.DescribeTaskDetail(request)
        if _, ok := err.(*errors.TencentCloudSDKError); ok {
            fmt.Printf("SDK 错误: %s\n", err)
            return
        }

        status := *response.Response.Status
        fmt.Printf("任务状态: %s\n", status)

        if status == "FINISH" || status == "FAIL" {
            break
        }
        // 建议间隔 5 秒以上
        time.Sleep(5 * time.Second)
    }
}

func main() {
    // 密钥申请文档：https://cloud.tencent.com/document/api/266/31757
    cred := common.NewCredential(
        os.Getenv("TENCENTCLOUD_SECRET_ID"),
        os.Getenv("TENCENTCLOUD_SECRET_KEY"),
    )
    // 子应用 ID，在腾讯云点播控制台获取
    // 如需创建子应用：https://cloud.tencent.com/document/api/266/43744
    subAppIdStr := os.Getenv("VOD_SUB_APP_ID")
    subAppId, _ := strconv.ParseUint(subAppIdStr, 10, 64)

    client, _ := vod.NewClient(cred, "", nil)

    // 示例：生图并查询结果
    // taskId, _ := createAigcImageTask(client, subAppId)
    // queryTaskStatus(client, taskId, subAppId)

    // 示例：生视频并查询结果
    // taskId, _ := createAigcVideoTask(client, subAppId)
    // queryTaskStatus(client, taskId, subAppId)

    // 示例：创建自定义主体
    // taskId, _ := createAigcCustomElement(client, subAppId)
    // queryTaskStatus(client, taskId, subAppId)

    _ = client
    _ = subAppId
}
```

## 回调事件（可选方案）

如果用户不想轮询查询，可以使用**回调事件**来获取任务结果：

- 文档：https://cloud.tencent.com/document/product/266/35579
- 支持 HTTP 回调和 CMQ/TDMQ 消息队列两种方式
- 在腾讯云控制台配置回调 URL 后，任务完成时腾讯云会主动推送结果
- 回调方式适合生产环境，避免轮询带来的资源消耗

**建议**：
- 开发调试阶段：使用轮询查询（简单直接）
- 生产环境：使用回调事件（更高效，节省资源）

## 常见问题处理

1. **SDK 缺少某个 Request 类**（如 `CreateAigcImageTaskRequest`、`CreateAigcCustomElementRequest` 等）：SDK 版本较旧，执行 `pip3 install --upgrade tencentcloud-sdk-python` 升级
2. **鉴权失败**：检查 SecretId/SecretKey 是否正确，以及账号是否有 VOD 相关权限
3. **SubAppId 如何获取**：登录腾讯云点播控制台，左上角切换子应用即可看到子应用 ID；如子应用不存在，参考文档创建：https://cloud.tencent.com/document/api/266/43744
4. **任务一直 PROCESSING**：AIGC 任务耗时较长属正常现象，请耐心等待，不要频繁查询
5. **参数与文档不一致**：官网文档可能存在更新滞后，请参考补充文档获取最新参数说明：https://doc.weixin.qq.com/sheet/e3_AOcASwZGACkCNPE0YsRJjS761Zng7?scode=AJEAIQdfAAo0s201lCAMkAoQZ9ACc&tab=0znb2u
6. **找不到需要的接口**：请查阅 API 接口概览 https://cloud.tencent.com/document/product/266/31753，找到对应接口后跳转到具体文档页面
7. **调用接口会产生费用吗**：会。AIGC 生图 / 生视频 / 自定义主体 / 自定义音色等接口均为付费接口，**每次成功调用都会扣费**。请务必先阅读计费文档：
   - 国内站：https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac
   - 国际站：https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419
   - 计费补充文档（最新单价）：https://doc.weixin.qq.com/sheet/e3_AG0ALgbHACcCNNZhi1wsiRsS03lPl?scode=AJEAIQdfAAoqRYCNaQAMkAoQZ9ACc&tab=kzcknp
8. **如何避免意外计费 / 控制费用**：
   - 在腾讯云控制台 → 费用中心 开启**费用预警**和**消费限额**
   - 测试阶段使用最低规格参数（最小分辨率、最短时长、最低档模型）验证流程
   - 调试时避免循环调用接口，控制并发与重试次数
   - 任务失败一般不计费，但**成功的任务即使你没用结果也会计费**，请合理设计业务流程
9. **国内账号和海外账号计费一样吗**：不一样。国内站和国际站价格体系独立，请按账号归属查阅对应文档
