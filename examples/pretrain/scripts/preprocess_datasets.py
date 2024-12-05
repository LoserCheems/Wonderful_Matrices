from transformers import AutoTokenizer
from datasets import load_from_disk
from argparse import ArgumentParser


def process_fineweb_edu(example, tokenizer, max_length=2048):
    text = example['text']
    outputs = tokenizer(
        text,
        add_special_tokens=True,
        truncation=True,
        padding=False,
        max_length=max_length,
        return_overflowing_tokens=False,
        return_length=False,
    )
    return {
        'input_ids': outputs['input_ids'],
        'attention_mask': outputs['attention_mask'],
    }

def process_cosmopedia(example, tokenizer, max_length=2048):
    prompt = example['prompt']
    text = example['text']
    conversation = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": text},
    ]
    outputs = tokenizer.apply_chat_template(
        conversation, 
        tokenize=True, 
        truncation=True, 
        padding=False, 
        max_length=max_length,
        return_overflowing_tokens=False,
        return_length=False,
        return_dict=True
    )
    return {
        'input_ids': outputs['input_ids'],
        'attention_mask': outputs['attention_mask'],
    }

def process_python_edu(example, tokenizer, max_length=2048):
    text = example['text']
    outputs = tokenizer(
        text,
        add_special_tokens=True,
        truncation=True,
        padding=False,
        max_length=max_length,
        return_overflowing_tokens=False,
        return_length=False,
    )
    return {
        'input_ids': outputs['input_ids'],
        'attention_mask': outputs['attention_mask'],
    }

def process_open_web_math(example, tokenizer, max_length=2048):
    text = example['text']
    outputs = tokenizer(
        text,
        add_special_tokens=True,
        truncation=True,
        padding=False,
        max_length=max_length,
        return_overflowing_tokens=False,
        return_length=False,
    )
    return {
        'input_ids': outputs['input_ids'],
        'attention_mask': outputs['attention_mask'],
    }

def main(args):

    # 计算fineweb-edu, cosmopedia-v2, python-edu, open-web-math的大小
    # Calculate the size of fineweb-edu, cosmopedia-v2, python-edu, open-web-math
    fineweb_edu_ratio, cosmopedia_v2_ratio, python_edu_ratio, open_web_math_ratio = 0.7, 0.2, 0.05, 0.05

    fineweb_edu_train_size = int(args.train_examples * fineweb_edu_ratio)
    cosmopedia_v2_train_size = int(args.train_examples * cosmopedia_v2_ratio)
    python_edu_train_size = int(args.train_examples * python_edu_ratio)
    open_web_math_train_size = int(args.train_examples * open_web_math_ratio)

    fineweb_edu_test_size = int(args.test_examples * fineweb_edu_ratio)
    cosmopedia_v2_test_size = int(args.test_examples * cosmopedia_v2_ratio)
    python_edu_test_size = int(args.test_examples * python_edu_ratio)
    open_web_math_test_size = int(args.test_examples * open_web_math_ratio)


    # 加载分词器
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)

    # 处理fineweb-edu
    # Process fineweb-edu
    dataset = load_from_disk(args.datasets_dir + '/fineweb-edu')
    column_names = dataset.column_names
    dataset = dataset.shuffle(seed=233).select(
        range(fineweb_edu_train_size + fineweb_edu_test_size)
    ).map(
        process_fineweb_edu, 
        fn_kwargs={
            'tokenizer': tokenizer,
            'max_length': args.max_length
        },
        num_proc=args.num_proc,
        remove_columns=column_names,
        batched=True,
        desc="Processing fineweb-edu"
    )
    print(dataset)
    dataset.save_to_disk(args.save_dir + '/fineweb-edu_processed')

    # 处理宇宙百科-v2
    # Process Cosmopedia-v2
    dataset = load_from_disk(args.datasets_dir + '/cosmopedia-v2')
    column_names = dataset.column_names

    dataset = dataset.shuffle(seed=233).select(
        range(cosmopedia_v2_train_size + cosmopedia_v2_test_size)
    ).map(
        process_cosmopedia, 
        fn_kwargs={
            'tokenizer': tokenizer,
            'max_length': args.max_length
        },
        num_proc=args.num_proc,
        remove_columns=column_names,
        desc="Processing cosmopedia-v2"
    )
    print(dataset)
    dataset.save_to_disk(args.save_dir + '/cosmopedia-v2_processed')

    # 处理Python教育
    # Process Python Education
    dataset = load_from_disk(args.datasets_dir + '/python-edu')
    column_names = dataset.column_names
    dataset = dataset.shuffle(seed=233).select(
        range(python_edu_train_size + python_edu_test_size)
    ).map(
        process_python_edu, 
        fn_kwargs={
            'tokenizer': tokenizer,
            'max_length': args.max_length
        },
        num_proc=args.num_proc,
        remove_columns=column_names,
        batched=True,
        desc="Processing python-edu"
    )
    print(dataset)
    dataset.save_to_disk(args.save_dir + '/python-edu_processed')

    # 处理开放网络数学
    # Process Open Web Math
    dataset = load_from_disk(args.datasets_dir + '/open-web-math')
    column_names = dataset.column_names
    dataset = dataset.shuffle(seed=233).select(
        range(open_web_math_train_size + open_web_math_test_size)
    ).map(
        process_open_web_math, 
        fn_kwargs={
            'tokenizer': tokenizer,
            'max_length': args.max_length
        },
        num_proc=args.num_proc,
        remove_columns=column_names,
        batched=True,
        desc="Processing open-web-math"
    )
    print(dataset)
    dataset.save_to_disk(args.save_dir + '/open-web-math_processed')

if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("--datasets_dir", type=str, default="./datasets")
    argparser.add_argument("--save_dir", type=str, default="./datasets")
    argparser.add_argument("--tokenizer_path", type=str, default="./examples/tokenizer")
    argparser.add_argument("--train_examples", type=int, default=160_000_000)
    argparser.add_argument("--test_examples", type=int, default=1_000)
    argparser.add_argument("--max_length", type=int, default=2048)
    argparser.add_argument("--num_proc", type=int, default=1)
    args = argparser.parse_args()

    main(args)
