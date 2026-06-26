# Wojiayun Skill

## 基本信息
- **名称**: wojiayun_skill
- **版本**: 1.0.0
- **描述**: 我家云设备管理与工单系统技能包
- **作者**: SOLO
- **创建时间**: 2026-05-22

## 认证方式

**本技能仅支持 API Key 认证，不支持用户名/密码登录。**

使用前必须提供 API Key，通过以下方式设置：

```python
from wojiayun_skill import store_api_key
store_api_key("your_api_key_here")
```

如果没有 API Key，请联系我家云平台管理员获取。

---

## 重要规则

### 项目切换规则
**部分接口只能查询当前项目的数据**，如需查询多个项目：

1. 先缓存已查询的项目工单
2. 调用切换项目接口
3. 再查询新项目数据
4. 最后按项目维度汇总统计

### 只能查当前项目的接口
- `get_equipment_repairs` - 设备维修工单
- `get_equipments` - 设备列表
- `get_equip_ins_list` - 设备巡检任务
- `get_device_maintain_list` - 设备维保任务

### 可跨项目查询的接口
- `query_workorders` - 工单统计（支持多项目ID参数）
- `get_my_workorders` - 工单列表（action=1 可查全部）

---

## API 接口列表

### 用户认证
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `token_refresh` | /thirdUser/apiKeyAuth | GET | API Key换取Token |
| `get_current_user_info` | /users/getCurrentUserInfo | GET | 获取当前用户信息 |
| `get_projects` | /projects/getProjectsByUserIDAndName | GET | 获取项目列表 |
| `set_default_project` | /employees/setDefaultProject | GET | 切换项目 |

### 设备管理
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_equipments` | /equipments/getAllEquipMents | GET | 获取设备列表（当前项目） |
| `get_equipment_detail` | /equipments/getEquipMentDetail | GET | 获取设备详情 |

### 设备巡检
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_equip_ins_list` | /equipIns/selectAllEquipInsEntryList | GET | 获取巡检任务（当前项目） |

### 设备维保
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_device_maintain_list` | /equMaiPlanEntrys/getDeviceViewList | GET | 获取维保任务（当前项目） |

### 设备维修
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_equipment_repairs` | /equMaintenance/pageEquMaintenanceList | GET | 获取维修工单（当前项目） |

**维修状态码：**
| 状态码 | 说明 |
|--------|------|
| 0 | 待分派 |
| 1 | 待处理 |
| 2 | 处理中 |
| 3 | 已完成 |
| 4 | 已归档 |

**维保周期映射：**
| 代码 | 含义 |
|------|------|
| month | 每月 |
| double_month | 双月 |
| quarter | 每季 |
| half_year | 半年 |
| year | 每年 |
| define | 自定义 |
| many_month | 每月多次 |

### 工单管理
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_work_type` | /workorders/getWorkType | GET | 获取工单类型 |
| `search_rooms` | /rooms/getRoomsByBuildInfoV3 | GET | 搜索房间 |
| `get_room_customers` | /workorders/getAllCustomerByRoomId | GET | 获取房间客户 |
| `create_workorder` | /workorders/insertWorkorder | POST | 创建工单 |
| `get_pending_workorders` | /workCustomer/getWoprocessPagingList | POST | 待我处理工单 |
| `get_my_workorders` | /workorders/getAllWorkorder | GET | 工单列表 |
| `query_workorders` | /workCustomer/getWoprocessPagingList | POST | 工单统计（支持多项目） |

**工单查询参数：**
- `action=0`: 待我受理分派（当前用户）
- `action=1`: 所有待受理工单（全部）

**工单统计参数：**
```json
{
  "action": "queryList",
  "projectID": "项目ID1,项目ID2,...",
  "projectIDs": "项目ID1,项目ID2,...",
  "projectName": "项目名等N个项目",
  "createTime": "ownDefined",
  "definedTime_list1": "2026-05-01~2026-05-23"
}
```

### 公区管理
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `get_public_area_paging` | /publicArea/getPublicAreaPaging | GET | 搜索公区 |

### 文件管理
| 接口名 | 路径 | 方法 | 说明 |
|--------|------|------|------|
| `upload_files` | /api/file/uploadFiles | POST | 上传文件（视频最大20MB） |

---

## 使用方式

```python
from wojiayun_skill import SecureAPIClient, store_api_key

# 1. 设置 API Key（必须）
store_api_key("your_api_key_here")

# 2. 创建客户端
client = SecureAPIClient()

# 3. 获取设备列表
result = client.call_api("get_equipments", "GET")

# 4. 查询工单统计（多项目）
result = client.call_api("query_workorders", "POST", data={
    "current": 1,
    "rowCount": 500,
    "queryParams": {
        "action": "queryList",
        "projectID": "项目ID1,项目ID2",
        "createTime": "ownDefined",
        "definedTime_list1": "2026-05-01~2026-05-23"
    }
})
```

---

## 安全特性

- **加密**: AES-256-GCM
- **模式**: 生产模式
- **白名单控制**: 只允许调用授权接口
- **敏感信息加密**: URL、Token 均加密存储
- **静默模式**: 不输出敏感信息

---

## 依赖安装
```bash
pip install requests cryptography
```

## 注意事项
- 必须提供有效的 API Key 才能使用
- 不支持用户名/密码登录
- 所有敏感配置信息均已加密存储
- **设备维修/巡检/维保工单只能查当前项目，多项目需切换后汇总**
