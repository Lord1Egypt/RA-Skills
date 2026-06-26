# 优衣库商品查询 Skill

## 功能描述

该Skill用于查询优衣库的折扣商品信息，筛选出折扣率≤60%的商品，并以结构化的方式返回结果。

## 触发条件

当用户输入中包含以下关键词或类似语义时，自动触发该Skill：
- 查询优衣库男装
- 优衣库女装
- 优衣库服装
- 优衣库折扣
- 优衣库促销
- 优衣库特价

## 安装与配置

### 依赖项

该Skill依赖以下Python包：
- requests

### 输出路径

所有输出文件保存到当前工作目录下的 `unique/` 子目录中。

### 安装方法

1. 确保Python 3.6+已安装
2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 直接调用

```python
from uniqlo_product_query import process_query

# 带尺码过滤
user_input = "查询优衣库男装M码"
response = process_query(user_input)
print(response)

# 不带尺码过滤（所有尺码）
user_input = "查询优衣库女装"
response = process_query(user_input)
print(response)
```

### 示例输入输出

#### 示例1：查询优衣库男装

**输入**：
```
查询优衣库男装折扣商品
```

**输出**：
```
找到 12 件优衣库男装折扣商品：

1. 水洗宽松休闲束脚裤/长裤/休闲裤
   原价：¥199.0，现价：¥79.0
   折扣率：39.7%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000064379

2. 全棉衬衫/长袖
   原价：¥249.0，现价：¥149.0
   折扣率：59.84%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000068536

3. 高弹力运动茄克防紫外线外套夹克轻薄
   原价：¥199.0，现价：¥99.0
   折扣率：49.75%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000064459

4. 高弹力运动长裤防紫外线休闲裤裤子轻薄常规款
   原价：¥199.0，现价：¥99.0
   折扣率：49.75%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000064453

5. 罗纹针织茄克
   原价：¥399.0，现价：¥199.0
   折扣率：49.87%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000068873

... 还有 7 件商品未显示
```

#### 示例2：查询优衣库女装

**输入**：
```
优衣库女装特价
```

**输出**：
```
找到 10 件优衣库女装折扣商品：

1. 休闲拉链短茄克/外套巴恩风翻领时尚夹克
   原价：¥349.0，现价：¥199.0
   折扣率：57.02%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000063807

2. 柔滑棉质V领针织短开衫
   原价：¥249.0，现价：¥99.0
   折扣率：39.76%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000067700

3. 喇叭牛仔裤/水洗产品
   原价：¥299.0，现价：¥149.0
   折扣率：49.83%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000067697

4. AIRism高弹力防紫外线拉链连帽衫防晒UPF50+修身
   原价：¥199.0，现价：¥99.0
   折扣率：49.75%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000060869

5. 防风连帽短外套
   原价：¥399.0，现价：¥199.0
   折扣率：49.87%
   链接：https://www.uniqlo.cn/product-detail.html?productCode=u0000000069638

... 还有 5 件商品未显示
```

## 核心功能

1. **关键词识别**：识别用户输入中的优衣库商品查询意图
2. **性别识别**：根据用户输入确定查询的是男装、女装、童装还是婴幼儿装
3. **尺码识别**：从用户输入中提取尺码（可选），如果未指定尺码则不过滤
4. **数据获取**：调用优衣库API获取商品数据（支持有/无尺码过滤）
5. **数据处理**：计算折扣率并筛选出折扣率≤60%的商品
6. **结果格式化**：以结构化的方式返回结果，生成Markdown文件
7. **错误处理**：处理可能的异常情况并提供友好的提示信息

## 扩展与定制

### 扩展关键词

可以通过修改`identify_intent`函数中的关键词列表来扩展触发条件：

```python
def identify_intent(user_input):
    # 关键词列表
    keywords = [
        '查询优衣库男装', '优衣库男装', '男装折扣',
        '查询优衣库女装', '优衣库女装', '女装折扣',
        '优衣库服装', '优衣库折扣', '优衣库促销', '优衣库特价',
        # 添加更多关键词
    ]
    # ...
```

### 调整查询参数

可以通过修改`fetch_uniqlo_products`函数中的参数来调整查询条件：

```python
def fetch_uniqlo_products(gender='men', page=1, page_size=20):
    # ...
    payload = {
        "url": url_path,
        "pageInfo": {
            "page": page,
            "pageSize": page_size,
            "withSideBar": "Y"
        },
        # ...
    }
    # ...
```

### 调整响应格式

可以通过修改`format_response`函数来调整输出样式：

```python
def format_response(result, gender):
    # ...
    response = f"找到 {total} 件优衣库{('男装' if gender == 'men' else '女装')}折扣商品：\n\n"
    # ...
```

## 注意事项

- 遵守优衣库API的使用规则
- 合理控制API调用频率，避免过度请求
- 确保错误处理机制完善，提供友好的用户体验
