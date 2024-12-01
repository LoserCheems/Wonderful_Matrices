import os
import boto3
import gzip
from datasets import load_dataset
from botocore.exceptions import ClientError
from argparse import ArgumentParser

s3 = boto3.client('s3')
bucket_name = "softwareheritage"

# 下载Fineweb-Edu数据集
# Download Fineweb-Edu dataset
def download_fineweb_edu(save_dir, cache_dir, num_proc):
    dataset = load_dataset("HuggingFaceTB/smollm-corpus", "fineweb-edu-dedup", split="train", num_proc=num_proc, cache_dir=cache_dir)
    print(dataset)
    dataset.save_to_disk(save_dir + "/fineweb-edu", num_proc=num_proc)

# 下载宇宙百科v2数据集
# Download Cosmopedia-v2 dataset
def download_cosmopedia_v2(save_dir, cache_dir, num_proc):
    dataset = load_dataset("HuggingFaceTB/smollm-corpus", "cosmopedia-v2", split="train", num_proc=num_proc, cache_dir=cache_dir)
    print(dataset)
    dataset.save_to_disk(save_dir + "/cosmopedia-v2", num_proc=num_proc)

# 从Python教育数据集中的blob_id下载内容
# Download content from blob_id in Python Education dataset
def download_python_edu_contents(blob_id):
    key = f"content/{blob_id}"
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        with gzip.GzipFile(fileobj=obj['Body']) as fin:
            content = fin.read().decode("utf-8", errors="ignore")
        return {"text": content, "download_success": True}
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f"File not found: {key}")
            return {"text": "", "download_success": False}
        else:
            raise

# 下载Python教育数据集
# Download Python Education dataset
def download_python_edu(save_dir, cache_dir, num_proc):
    dataset = load_dataset("HuggingFaceTB/smollm-corpus", "python-edu", split="train", num_proc=num_proc, cache_dir=cache_dir)
    dataset = dataset.map(download_python_edu_contents, input_columns="blob_id", num_proc=num_proc)
    dataset = dataset.filter(lambda x: x['download_success'])
    print(dataset)
    dataset.save_to_disk(save_dir + "/python-edu", num_proc=num_proc)

# 下载开放网络数学数据集
# Download Open Web Math dataset
def download_open_web_math(save_dir, cache_dir, num_proc):
    dataset = load_dataset("open-web-math/open-web-math", split="train", num_proc=num_proc, cache_dir=cache_dir)
    print(dataset)
    dataset.save_to_disk(save_dir + "/open-web-math", num_proc=num_proc)


def main(args):
    download_fineweb_edu(args.save_dir, args.cache_dir, args.num_proc)
    download_cosmopedia_v2(args.save_dir, args.cache_dir, args.num_proc)
    download_python_edu(args.save_dir, args.cache_dir, args.num_proc)
    download_open_web_math(args.save_dir, args.cache_dir, args.num_proc)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--save_dir", type=str, default="./datasets")
    parser.add_argument("--cache_dir", type=str, default="./cache")
    parser.add_argument("--num_proc", type=int, default=1)
    args = parser.parse_args()

    main(args)
