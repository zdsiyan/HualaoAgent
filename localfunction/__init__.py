import importlib
import pkgutil

# 创建一个字典来存储所有的函数
functions = {}

# 导入 localfunction 包下的所有模块
for _, name, _ in pkgutil.iter_modules(__path__):  # 注意这里使用的是 __path__
    module = importlib.import_module(f"{__name__}.{name}")

    # 将每个模块中的所有函数添加到字典中
    for attr_name in dir(module):
        attr_value = getattr(module, attr_name)
        if callable(attr_value):
            functions[attr_name] = attr_value