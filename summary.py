import ollama
import os

def summarize_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    prompt = f"请总结以下内容：\n\n{content}\n\n要求输出的文字里面不能有markdown的多级标题"
    
    res = ollama.chat(model="qwen2.5:latest", stream=False, messages=[{"role":"user","content":prompt}])
    return res["message"]["content"]

def summarize_directory(directory_path):
    summary = {}
    for root, dirs, files in os.walk(directory_path):
        dir_summary = []
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_summary = summarize_file(file_path)
                summary[file_path] = file_summary
                dir_summary.append(file_summary)
        if dir_summary:
            dir_prompt = f"请总结以下内容：\n\n{''.join(dir_summary)}\n\n要求输出的文字里面不能有markdown的多级标题"
            dir_res = ollama.chat(model="qwen2.5:latest", stream=False, messages=[{"role":"user","content":dir_prompt}])
            summary[root] = dir_res["message"]["content"]
    return summary

# Example usage:
# summarize_file('path/to/your/file.txt')
# summarize_directory('path/to/your/directory')
