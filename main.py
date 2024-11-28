import yaml
import json

from zhipuai import ZhipuAI
import localfunction

# localfunction 定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "gen_name",
            "description": "测试",
            "parameters": {
                "type": "object",
                "properties": {
                    "gen_name": {
                        "description": "输入参数",
                        "type": "string"
                    }
                },
                "required": ["arg_str"]
            },
        }
    }, ]

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def chat(client):
    messages = []
    messages.append({"role": "user", "content": "向测试方法发送一段人名，要求三个字"})
    # chat
    response = client.chat.completions.create(
        model="GLM-4-Flash",  # 填写需要调用的模型编码
        messages=messages,
        tools=tools,
    )

    print(response.choices[0].message)
    messages.append(response.choices[0].message.model_dump())

    parse_function_call(response, messages)

def parse_function_call(model_response,messages):
    # 处理函数调用结果，根据模型返回参数，调用对应的函数。
    # 调用函数返回结果后构造tool message，再次调用模型，将函数结果输入模型
    # 模型会将函数调用结果以自然语言格式返回给用户。
    if model_response.choices[0].message.tool_calls:
        tool_call = model_response.choices[0].message.tool_calls[0]
        args = tool_call.function.arguments
        function_result = {}
        if tool_call.function.name in localfunction.functions:
            function = localfunction.functions[tool_call.function.name]
            function_result = function(**json.loads(args))
        messages.append({
            "role": "tool",
            "content": f"{json.dumps(function_result)}",
            "tool_call_id":tool_call.id
        })
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=messages,
            tools=tools,
        )
        print(response.choices[0].message)
        messages.append(response.choices[0].message.model_dump())

if __name__ == '__main__':
    config = load_config('env.yml')
    config_item = config['ChatGLM']['Key']
    client = ZhipuAI(api_key=config_item)
    chat(client)