# WeatherQuery Skill

## Description
这是一个用于查询特定城市当前天气状况的工具。它可以返回温度、天气描述（如晴朗、多雨）和湿度信息。

## Usage
当用户询问关于天气的问题时，例如“北京今天天气怎么样？”或“上海现在的温度是多少？”，请使用此工具。

## Input Parameters
该工具接受一个 JSON 对象作为输入，包含以下字段：

| 参数名 | 类型 | 必填 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `city` | string | 是 | 需要查询天气的城市名称（中文或英文均可）。 | "Beijing", "上海" |
| `unit` | string | 否 | 温度单位，可选值为 'celsius' (摄氏度) 或 'fahrenheit' (华氏度)。默认为 'celsius'。 | "celsius" |

## Output Format
工具返回一个 JSON 字符串，包含以下信息：
- `city`: 查询的城市
- `temperature`: 当前温度
- `description`: 天气简述
- `humidity`: 湿度百分比

## Example
**​User:​** "查一下深圳的天气"
**​Model Call:​** `WeatherQuery(city="深圳", unit="celsius")`
**​Output:​** `{"city": "深圳", "temperature": "28°C", "description": "多云", "humidity": "60%"}`