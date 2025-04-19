# 大模型下载脚本

使用[魔塔社区](https://www.modelscope.cn/home)的 modelscope 下载大模型。

## 功能与优势

`-h` 或 `--help` 查看帮助。

### 命令行参数

- `-m, --model <模型名称>`：**必需**，指定要下载的模型名称。
- `-f, --file <文件名>`：指定要下载的文件名称，默认为 `all`，表示下载所有文件。多个文件用逗号分隔，如 `a,b,c`。
- `-d, --download-dir <目录路径>`：指定下载文件的目录，默认为环境变量 `MODELSCOPE_CACHE`，若无则为当前目录。
- `-g, --generate-modelfile`：是否生成 `Modelfile` 文件，默认为 `False`。
- `-o, --overwrite`：是否覆盖已存在文件，默认为 `False`。

### 优势

- 可以中断重连
- 分文件进度条
- 自动生成 ModelFile
- 完全国内网络环境、不需要进行申请模型使用、加载模型使用transformers实现（兼容）
