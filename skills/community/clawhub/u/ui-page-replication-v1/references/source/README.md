# UI Page Replication Skill

## 功能
用于后台系统 UI 100% 复刻开发

## 使用方式

```ts
import { UIReplicationSkill } from "./skills/ui-page-replication-v1"

const input = "复刻页面：房源管理系统"

if (UIReplicationSkill.match(input)) {
  const result = UIReplicationSkill.execute({
    pagePath: "/realestate/project/list"
  })

  console.log(result.prompt)
}