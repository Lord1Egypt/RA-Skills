import json
import xmind


def run(input):

    data = input["data"]

    if isinstance(data, str):
        data = json.loads(data)

    file = "testcase.xmind"

    workbook = xmind.load(file)
    sheet = workbook.getPrimarySheet()

    root = sheet.getRootTopic()
    root.setTitle("测试用例")

    for module, points in data.items():

        module_topic = root.addSubTopic()
        module_topic.setTitle(module)

        for point in points:

            point_topic = module_topic.addSubTopic()
            point_topic.setTitle(point["测试点"])

            for case in point["cases"]:

                case_topic = point_topic.addSubTopic()
                case_topic.setTitle(case["用例名称"])

                pre = case_topic.addSubTopic()
                pre.setTitle("前置条件: " + case.get("前置条件", ""))

                steps = case_topic.addSubTopic()
                steps.setTitle("步骤")

                for step in case.get("步骤", []):
                    step_node = steps.addSubTopic()
                    step_node.setTitle(step)

                exp = case_topic.addSubTopic()
                exp.setTitle("预期结果: " + case.get("预期结果", ""))

                pri = case_topic.addSubTopic()
                pri.setTitle("优先级: " + case.get("优先级", "中"))

    xmind.save(workbook, file)

    return {
        "file": file
    }
