import os
import shutil

import requests
from PIL import Image
from io import BytesIO
from utils import get_variable


class DreamboothCuttingTool:
    def __init__(self, url, name, model_name, start_index=0, auto_slicing=True):
        self.url = url
        self.name = name
        self.model_name = model_name
        self.start_index = start_index
        self.auto_slicing = auto_slicing
        self.path = f"session/{name}/dataset/{model_name}"

    def corp(self):
        if os.path.exists(self.path) and self.start_index == 0:
            shutil.rmtree(self.path)

        os.makedirs(self.path, exist_ok=True)

        # 下载图片
        response = requests.get(self.url)

        # 确保请求成功
        response.raise_for_status()

        # 打开图片
        img = Image.open(BytesIO(response.content))

        # 确认图片的尺寸是 2048x2048
        print(f"width:{img.size[0]}, height:{img.size[1]}")

        if self.auto_slicing:
            if img.size[0] != img.size[1]:
                max_length = max(img.size[0], img.size[1])
                if img.size[0] > img.size[1]:
                    img = img.crop((int((max_length - img.size[1]) * 0.5),
                                    0,
                                    img.size[0] - int((max_length - img.size[1]) * 0.5),
                                    img.size[1]))
                else:
                    img = img.crop((0,
                                    int((max_length - img.size[0]) * 0.5),
                                    img.size[0],
                                    img.size[1] - int((max_length - img.size[0]) * 0.5)))

        width = img.size[0]
        height = img.size[1]
        half_width = int(width * 0.5)
        half_height = int(height * 0.5)

        # 切割图片为 4 份
        img1 = img.crop((0, 0, half_width, half_height))
        img2 = img.crop((half_width, 0, width, half_height))
        img3 = img.crop((0, half_height, half_width, height))
        img4 = img.crop((half_width, half_height, width, height))

        # 保存切割后的图片
        img1.save(f"{self.path}/{'{:02d}'.format(self.start_index + 0)}.png")
        img2.save(f"{self.path}/{'{:02d}'.format(self.start_index + 1)}.png")
        img3.save(f"{self.path}/{'{:02d}'.format(self.start_index + 2)}.png")
        img4.save(f"{self.path}/{'{:02d}'.format(self.start_index + 3)}.png")

    def write_config(self):
        name_text = self.model_name.replace('_', ' ')
        content = """
[general]
name = YYY
base_config = base_config
base_model = runwayml/stable-diffusion-v1-5

[model]
instance_prompt = xy XXX
sample_prompt = blue xy XXX
class_prompt = XXX
sample_negative_prompt = 
        """
        with open(f'session/{self.name}/dataset/{self.model_name}/config.ini', 'w') as f:
            content = content.replace('YYY', self.model_name)
            content = content.replace('XXX', name_text)
            f.write(content)


if __name__ == '__main__':
    local_name = get_variable("NAME", None, 1)
    local_model_name = get_variable("MODEL_NAME", None, 2)
    img_url = get_variable("URL", None, 3)
    s_index = int(get_variable("INDEX", "0", 4))
    b_slicing = bool(get_variable("AUTO_SLICING", "True", 5))

    assert local_model_name is not None, "model_name cannot be none"

    print(f"local_name: {local_name}")
    print(f"local_model_name: {local_model_name}")
    print(f"img_url: {img_url}")
    print(f"s_index: {s_index}")
    print(f"b_slicing: {b_slicing}")

    corp_tool = DreamboothCuttingTool(img_url, local_name, local_model_name, s_index, b_slicing)
    corp_tool.corp()
    corp_tool.write_config()
