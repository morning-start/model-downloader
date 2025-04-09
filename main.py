import argparse
from pathlib import Path

from modelscope import model_file_download, snapshot_download

# 提取常量，提高代码可维护性
MODELFILE_DIR = Path("./Modelfile")
OLLAMA_COMMAND_TEMPLATE = "ollama create {name} -f {path}"


def setup_parser():
    """
    配置命令行参数解析器。

    :return: 配置好的参数解析器
    """
    parser = argparse.ArgumentParser(description="大模型下载脚本")
    parser.add_argument("-m", "--model", type=str, required=True, help="模型名称")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="all",
        help="下载文件名称， 默认为 all。多个文件用逗号分隔，如 a,b,c",
    )
    # 添加下载目录参数
    parser.add_argument(
        "-d",
        "--download-dir",
        type=str,
        default=".",
        help="指定下载文件的目录，默认为当前目录",
    )
    # 新增参数：是否生成 Modelfile 文件，默认为 False
    parser.add_argument(
        "-g",
        "--generate-modelfile",
        action="store_true",
        default=False,
        help="是否生成 Modelfile 文件，默认为 False",
    )
    return parser


def main():
    """
    脚本的主函数，处理命令行参数并执行模型下载操作。
    """
    parser = setup_parser()
    args = parser.parse_args()
    model_id = args.model
    files = args.file
    download_dir = Path(args.download_dir)  # 获取下载目录
    generate_modelfile = args.generate_modelfile  # 获取是否生成 Modelfile 的参数

    if files == "all":
        target_path = download_dir / model_id
        if target_path.exists():
            print(f"{target_path} 已存在，跳过下载")
        else:
            snapshot_download(model_id=model_id, local_dir=target_path)
    else:
        file_list = files.split(",")
        print(f"共需下载文件：{len(file_list)} 个")
        for file in file_list:
            # 根据参数决定是否生成 Modelfile 文件
            if generate_modelfile:
                create_model_file(model_id, file)
            target_path = download_dir / model_id / file
            if target_path.exists():
                print(f"{target_path} 已存在，跳过下载")
            else:
                model_file_download(
                    model_id=model_id, file_path=file, local_dir=download_dir / model_id
                )


def create_model_file(model_id: str, file: str):
    """
    为指定模型和文件创建 Modelfile，并打印 ollama 创建命令。

    :param model_id: 模型的 ID
    :param file: 文件名
    """
    file_path = Path(file)
    if file_path.suffix == ".gguf":
        content = f"FROM ../{model_id}/{file_path.name}"
        modelfile_path = MODELFILE_DIR / f"{file_path.stem}.modelfile"
        modelfile_path.parent.mkdir(parents=True, exist_ok=True)
        with open(modelfile_path, "w") as f:
            f.write(content)
        print(OLLAMA_COMMAND_TEMPLATE.format(name=file_path.stem, path=modelfile_path))


if __name__ == "__main__":
    main()
