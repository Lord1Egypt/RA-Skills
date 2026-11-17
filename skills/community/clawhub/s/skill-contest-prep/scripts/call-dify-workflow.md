# Dify Workflow调用脚本

## 用法

```bash
./call-dify-workflow.sh <workflow编号> '<输入参数JSON>'
```

## 示例

```bash
# Step 1：项目方向生成
./call-dify-workflow.sh 01 '{"competition_type":"人工智能应用","project_keyword":"智能垃圾分类","reference_text":""}'

# Step 1b：方案展开（用户选定方向后）
./call-dify-workflow.sh 01b '{"selected_option":"option_1的内容"}'

# Step 2：PPT大纲生成
./call-dify-workflow.sh 02 '{"project_plan":"[完整项目方案]","duration_minutes":20}'

# Step 3：展示剧本生成
./call-dify-workflow.sh 03 '{"project_plan":"[完整项目方案]","team_size":4,"duration_minutes":20}'

# Step 4：知识点训练计划
./call-dify-workflow.sh 04 '{"project_plan":"[完整项目方案]","ppt_outline":"[PPT大纲]","script_content":"[展示剧本]","team_members":"A:算法,B:前端,C:部署,D:讲解"}'
```

## API端点配置

- **Dify Base URL**：http://221.226.121.194:8088/v1
- **响应模式**：blocking（同步等待结果）

### Workflow API Key映射

| 编号 | Workflow名称 | API Key |
|------|-------------|---------|
| 01 | 技能大赛_01_项目方向生成 | app-ij16kVlWSBo4tibxh0fXuRod |
| 02 | 技能大赛_02_PPT大纲生成 | app-qPkxVCM2IpzgQHedkrU7XdjZ |
| 03 | 技能大赛_03_展示剧本生成 | app-JgNEhHO22EuxoJ6xsN8H0YSS |
| 04 | 技能大赛_04_知识点训练计划生成 | app-jkqO3Tn6FDR15z7zieQf2sho |

> ⚠️ 以上为本地开发环境Key，服务器环境Key可能不同，需在前端配置面板中切换。
> ⚠️ API Key不应硬编码到脚本中，生产环境应通过环境变量或配置文件读取。

## 请求格式

```json
{
  "inputs": {
    "变量名1": "值1",
    "变量名2": "值2"
  },
  "response_mode": "blocking",
  "user": "skill-contest"
}
```

## 响应格式

```json
{
  "task_id": "xxx",
  "workflow_run_id": "xxx",
  "data": {
    "outputs": {
      "result": "生成的结果文本"
    },
    "status": "succeeded"
  }
}
```
