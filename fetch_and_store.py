import os
import requests
from flask import Flask, send_file, abort
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# 获取环境变量
SOURCE_URLS = [url.rstrip('/') for url in os.environ.get('SOURCE_URLS', '').split(',')]
LOCAL_STORAGE_PATH = '/data'
DISABLE_URL_MODE = os.environ.get('DISABLE_URL_MODE', 'false').lower() == 'true'

# 创建线程池优化性能
executor = ThreadPoolExecutor(max_workers=10)

def fetch_and_store_file(file_path, url=None):
    if url:
        # URL 模式
        domain = url.split("//")[-1].split('/')[0].replace("/", "_")
        domain_storage_path = os.path.join(LOCAL_STORAGE_PATH, domain)

        # 去掉 URL 中的协议部分，保留路径
        relative_file_path = url.split("//")[-1].split('/', 1)[-1]
        local_file_path = os.path.join(domain_storage_path, relative_file_path)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return local_file_path
        except Exception as e:
            print(f"Failed to fetch from {url}: {e}")
    else:
        # 回源列表模式
        for source_url in SOURCE_URLS:
            domain = source_url.split("//")[-1].replace("/", "_")
            domain_storage_path = os.path.join(LOCAL_STORAGE_PATH, domain)

            try:
                response = requests.get(f"{source_url}/{file_path}", stream=True)
                response.raise_for_status()

                local_file_path = os.path.join(domain_storage_path, file_path)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                with open(local_file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return local_file_path
            except Exception as e:
                print(f"Failed to fetch from {source_url}: {e}")
                continue  # 尝试下一个源站域名

    return None  # 所有回源地址均失败或 URL 回源失败

@app.route('/<path:file_path>')
def serve_file(file_path):
    if ("http://" in file_path or "https://" in file_path) and not DISABLE_URL_MODE:
        # URL 模式
        url = file_path.replace('|', '://')
        domain = url.split("//")[-1].split('/')[0].replace("/", "_")
        relative_file_path = url.split("//")[-1].split('/', 1)[-1]
        local_file_path = os.path.join(LOCAL_STORAGE_PATH, domain, relative_file_path)

        if os.path.exists(local_file_path):
            return send_file(local_file_path)

        # 如果本地文件不存在，尝试从 URL 获取并存储
        future = executor.submit(fetch_and_store_file, relative_file_path, url)
        fetched_file_path = future.result()
        if fetched_file_path:
            return send_file(fetched_file_path)
        else:
            abort(404)
    else:
        # 回源列表模式
        for source_url in SOURCE_URLS:
            domain = source_url.split("//")[-1].replace("/", "_")
            local_file_path = os.path.join(LOCAL_STORAGE_PATH, domain, file_path)

            if os.path.exists(local_file_path):
                return send_file(local_file_path)

        # 如果本地文件不存在，尝试从源站获取并存储
        future = executor.submit(fetch_and_store_file, file_path)
        fetched_file_path = future.result()
        if fetched_file_path:
            return send_file(fetched_file_path)
        else:
            abort(404)

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000)
