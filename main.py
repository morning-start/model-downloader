import argparse
import os
from pathlib import Path

from modelscope import model_file_download, snapshot_download


def setup_parser() -> argparse.ArgumentParser:
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
        default=os.getenv("MODELSCOPE_CACHE", "."),
        help="指定下载文件的目录，默认为环境变量 MODELSCOPE_CACHE，若无则为当前目录",
    )
    # 新增参数：是否生成 Modelfile 文件，默认为 False
    parser.add_argument(
        "-g",
        "--generate-modelfile",
        action="store_true",
        default=False,
        help="是否生成 Modelfile 文件，默认为 False",
    )
    # 新增参数：是否强制覆盖已存在文件，默认为 False
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="是否强制覆盖已存在文件，默认为 False",
    )
    return parser


def download_file(
    target_path: Path, model_id: str, file: str, download_dir: Path, force: bool
) -> None:
    """
    下载指定模型的文件，如果文件已存在且不强制覆盖，则跳过下载。

    :param target_path: 目标文件路径
    :param model_id: 模型的 ID
    :param file: 文件名
    :param download_dir: 下载目录
    :param force: 是否强制覆盖已存在文件
    """
    if target_path.exists() and not force:
        print(f"{target_path} 已存在，跳过下载")
        return
    if target_path.exists() and force:
        print(f"{target_path} 已存在，将进行覆盖下载")
    model_file_download(
        model_id=model_id, file_path=file, local_dir=download_dir / model_id
    )


def main():
    """
    脚本的主函数，处理命令行参数并执行模型下载操作。
    """
    parser = setup_parser()
    args = parser.parse_args()
    model_id: str = args.model
    files: str = args.file
    download_dir: Path = Path(args.download_dir)  # 获取下载目录
    generate_modelfile: bool = args.generate_modelfile  # 获取是否生成 Modelfile 的参数
    force: bool = args.force  # 获取是否强制覆盖的参数

    if files == "all":
        target_path = download_dir / model_id
        if target_path.exists() and not force:
            print(f"{target_path} 已存在，跳过下载")
        else:
            snapshot_download(model_id=model_id, local_dir=target_path)
    else:
        file_list = files.split(",")
        print(f"共需下载文件：{len(file_list)} 个")
        for file in file_list:
            if generate_modelfile:
                create_model_file(model_id, file)
            download_file(
                download_dir / model_id / file, model_id, file, download_dir, force
            )


def create_model_file(model_id: str, file: str) -> None:
    """
    为指定模型和文件创建 Modelfile，并打印 ollama 创建命令。

    :param model_id: 模型的 ID
    :param file: 文件名
    """
    MODELFILE_DIR = Path("./Modelfile")
    OLLAMA_COMMAND_TEMPLATE = "ollama create {name} -f {path}"

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
