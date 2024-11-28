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
    messages.append({"role": "user", "content": "向测试方法发送一段人名"})
    # chat
    response = client.chat.completions.create(
        model="GLM-4-Flash",  # 填写需要调用的模型编码
        messages=messages,
        tools=tools,
    )

    print(response.choices[0].message)
    messages.append(response.choices[0].message.model_dump())

    parse_function_call(response, messages)



if __name__ == '__main__':
    config = load_config('env.yml')
    config_item = config['ChatGLM']['Key']
    client = ZhipuAI(api_key=config_item)
    print('hello',config_item)