import os
import shutil
import zipfile
from telegraph import Telegraph
import sys

# Get the zip file path from the command-line argument
zip_file_path = sys.argv[1]

# 创建Telegraph对象
telegraph = Telegraph()

# 登录Telegraph账号
telegraph.create_account(short_name='zip2telegra.ph')

# 本地压缩包文件名
#zip_filename = "img.zip"

# 解压缩压缩包
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("temp_images")

# 遍历解压后的图片文件
base_url = "https://telegra.ph"
uploaded_image_urls = []
for root, dirs, files in os.walk("temp_images"):
    for file in files:
        image_path = os.path.join(root, file)
        uploaded_image = telegraph.upload_file(image_path)
        uploaded_image_partial_url = uploaded_image[0]['src']
        uploaded_image_url = base_url + uploaded_image_partial_url
        uploaded_image_urls.append(uploaded_image_url)

# 打印所有上传后的图片URL
for url in uploaded_image_urls:
    print(url)

# 创建页面并添加图片
title = "New Page Title"
content = [{'tag': 'img', 'attrs': {'src': url}} for url in uploaded_image_urls]
author_name = "zip2telegra.ph"
author_url = "github.com/zip2telegra.ph"
created_page = telegraph.create_page(title=title, content=content)

# 获取创建的页面URL
created_page_url = created_page['url']

# 删除临时文件夹
shutil.rmtree("temp_images")
print("Temporary images directory deleted.")

# 打印创建的页面URL
print("Created page URL:", created_page_url)