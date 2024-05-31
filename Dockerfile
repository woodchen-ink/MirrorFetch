FROM python:3.9-slim

# 安装必要的软件包
RUN apt-get update && apt-get install -y nginx curl

# 复制 Python 脚本和 Nginx 配置文件
COPY fetch_and_store.py /app/fetch_and_store.py
COPY requirements.txt /app/requirements.txt
COPY nginx.conf /etc/nginx/nginx.conf

# 安装 Python 依赖
RUN pip install -r /app/requirements.txt

# 创建存储文件的目录
RUN mkdir -p /data

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV SOURCE_URLS=http://origin-domain1.com,http://origin-domain2.com  

# 暴露端口80
EXPOSE 80

# 启动脚本
CMD ["sh", "-c", "python fetch_and_store.py & nginx -g 'daemon off;'"]
