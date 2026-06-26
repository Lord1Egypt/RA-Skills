# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## FRONT_PAGE_OF_MOTOR_VEHICLE_DRIV (机动车行驶证正页)
- `title`: 标题
- `plateNo`: 号牌号码
- `vehicleType`: 车辆类型
- `owner`: 所有人
- `address`: 住址
- `useCharacter`: 使用性质
- `model`: 品牌型号
- `vin`: 车辆识别代号
- `engineNo`: 发动机号码
- `registerDate`: 注册日期
- `issueDate`: 发证日期

## SECOND_SHEET_OF_MOTOR_VEHICLE_DR (机动车行驶证副页)
- `plateNo`: 号牌号码
- `archiveNo`: 档案编号
- `authorizedCapacity`: 核定载人数
- `grossMass`: 总质量
- `curbMass`: 整备质量
- `ratedLoadMass`: 核定载质量
- `overallDimensions`: 外廓尺寸
- `permittedTowingMass`: 准牵引总质量
- `remarks`: 备注
- `inspectionRecord`: 检验记录
- `fuelType`: 燃油类型
- `certificateCoreNo`: 证芯编号
