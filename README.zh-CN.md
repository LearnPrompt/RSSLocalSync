# RSS链接管理工具

这个项目提供了一个简单的方法来管理和验证RSS链接，并将其转换为OPML格式。

![](/images/success.png)

## 功能

- 存储和管理RSS链接
- 验证RSS链接的有效性
- 将RSS链接转换为OPML格式

## 使用方法

1. Fork 本项目到你的GitHub账户。

2. 编辑 `rss_links.csv` 文件：
   - 添加新的RSS链接
   - 为每个链接指定分类和名称

3. 运行 `sensing.py` 脚本来验证RSS链接的有效性：
    - python sensing.py
    - 注意：当前验证准确率可能需要进一步提高。

4. 使用 `convert.py` 脚本将CSV文件转换为OPML格式：
    - python convert.py


## 文件说明

- `rss_links.csv`: 存储RSS链接及其相关信息的CSV文件
- `sensing.py`: 用于验证RSS链接有效性的Python脚本
- `convert.py`: 将CSV文件转换为OPML格式的Python脚本

## 贡献

欢迎提交问题报告和改进建议。如果你想贡献代码，请fork本项目并提交pull request。
