import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == '__main__':
    config = load_config('env.yml')
    config_item = config['ChatGLM']['Key']
    print('hello',config_item)