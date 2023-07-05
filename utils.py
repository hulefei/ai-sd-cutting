import os
import sys

def get_variable(key, default=None, index=0):
    # 获取名为 "NAME" 的环境变量的值
    local_name = os.environ.get(key)

    # 如果环境变量不存在，则从命令行参数中获取
    if local_name is None:
        local_args = sys.argv
        if index != 0 and len(local_args) > index:
            local_name = local_args[index]

    if local_name is None:
        local_name = default

    return local_name


def filter_image_file(folder_dir):
    suffixes = ('.png', '.jpg', '.jpeg')
    return [f for f in folder_dir if f.endswith(suffixes)]
