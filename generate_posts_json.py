import os
import json
from bs4 import BeautifulSoup

# 导出的静态站点文件夹路径
static_site_path = './'
# 生成的 JSON 文件路径
output_json_path = './posts.json'

posts_data = []


# 遍历静态站点文件夹中的所有 HTML 文件
for root, dirs, files in os.walk(static_site_path):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

                # 提取文章数据
                title = soup.find('title').get_text() if soup.find('title') else 'No Title'
                description = soup.find('meta', property='og:description')
                description = description['content'] if description else 'No Description'
                image_url = soup.find('meta', property='og:image')
                image_url = image_url['content'] if image_url else 'No Image URL'
                published_time = soup.find('meta', property='article:published_time')
                published_time = published_time['content'] if published_time else 'No Published Time'
                modified_time = soup.find('meta', property='article:modified_time')
                modified_time = modified_time['content'] if modified_time else 'No Modified Time'
                tags = [tag['content'] for tag in soup.find_all('meta', property='article:tag')] if soup.find_all('meta', property='article:tag') else []

                posts_data.append({
                    'title': title,
                    'description': description,
                    'image_url': image_url,
                    'published_time': published_time,
                    'modified_time': modified_time,
                    'tags': tags,
                    'file_path': file_path  # 可选，如果需要记录文件路径
                })

# 保存为 JSON 文件
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)

print(f"Successfully generated {output_json_path} with {len(posts_data)} posts.")