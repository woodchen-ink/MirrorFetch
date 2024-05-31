# MirrorFetch

MirrorFetch 是一个用于镜像和缓存外部文件的轻量级服务应用。它能够自动检测请求的 URL，并从源站获取文件，缓存到本地。下次访问相同文件时，直接从本地缓存中读取，提升访问速度，减少对源站的依赖。

## 功能

- 根据请求的 URL 自动选择回源模式：
  - URL 模式：直接根据请求的 URL 进行回源。
  - 回源列表模式：从配置的源站列表中依次尝试获取文件（单个也行）。
- 自动缓存获取到的文件到本地。
- 下次请求相同文件时，直接从本地缓存读取，提高访问效率。

## 使用场景

- 需要镜像和缓存外部文件的场景。
- 需要减少对特定源站的访问压力，提高访问速度。
- 希望在本地存储和管理外部文件，便于后续使用。

## 注意事项

- 请确保设置的源站 URL 列表是可访问的。
- 请确保本地存储路径有足够的空间用于缓存文件。
- 部署后可通过nginx反代访问。

## 使用方法

### 使用 `docker run`

1. 运行 Docker 容器：

    ```sh
    docker run -d \
        -p 2000:80 \
        -e SOURCE_URLS=http://origin-domain1.com,http://origin-domain2.com \
        -v $(pwd)/data:/data \
        --name mirrorfetch \
        mirrorfetch:latest
    ```

2. 访问示例：

    - 回源列表模式：
      - 访问 `http://yourdomain/path/to/file.jpg` 时，程序会依次尝试从 `http://origin-domain1.com/path/to/file.jpg` 和 `http://origin-domain2.com/path/to/file.jpg` 获取文件，并将文件存储到 `data/origin-domain1.com/path/to/file.jpg` 或 `data/origin-domain2.com/path/to/file.jpg` 中。
    
    - URL 模式：
      - 访问 `http://yourdomain/http://example.com/path/to/file.jpg` 时，程序会从 `http://example.com/path/to/file.jpg` 获取文件，并将文件存储到 `data/example.com/path/to/file.jpg` 中。

### 使用 `docker-compose`

1. 创建 `docker-compose.yml` 文件：

    ```yaml
    version: '3'
    services:
      mirrorfetch:
        image: mirrorfetch:latest
        build: .
        ports:
          - "2000:80"
        environment:
          - SOURCE_URLS=http://origin-domain1.com,http://origin-domain2.com
        volumes:
          - ./data:/data
    ```

2. 运行 `docker-compose`：

    ```sh
    docker-compose up -d
    ```

3. 访问示例：

    - 回源列表模式：
      - 访问 `http://yourdomain/path/to/file.jpg` 时，程序会依次尝试从 `http://origin-domain1.com/path/to/file.jpg` 和 `http://origin-domain2.com/path/to/file.jpg` 获取文件，并将文件存储到 `data/origin-domain1.com/path/to/file.jpg` 或 `data/origin-domain2.com/path/to/file.jpg` 中。
    
    - URL 模式：
      - 访问 `http://yourdomain/http://example.com/path/to/file.jpg` 时，程序会从 `http://example.com/path/to/file.jpg` 获取文件，并将文件存储到 `data/example.com/path/to/file.jpg` 中。

## 项目结构

确保项目的结构和文件内容如下：

```
MirrorFetch/
├── Dockerfile
├── nginx.conf
├── requirements.txt
├── fetch_and_store.py
├── docker-compose.yml  # 如果使用 docker-compose
└── data/  # 本地数据目录
```

## 贡献

欢迎贡献！如果你有任何问题或建议，请提交 Issue 或 Pull Request。

## 许可证

本项目基于 MIT 许可证开源。