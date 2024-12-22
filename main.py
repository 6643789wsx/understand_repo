import os
import argparse
from summary import summarize_directory

def main():
    parser = argparse.ArgumentParser(description="Summarize files in a directory.")
    parser.add_argument('-p', '--path', required=True, help='Path to the directory')
    args = parser.parse_args()
    
    directory_path = args.path
    summaries = summarize_directory(directory_path)
    
    output_file = f"output/{os.path.basename(directory_path)}.md"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        for file_path, summary in summaries.items():
            depth = file_path.replace(directory_path, '').count(os.sep)
            header_prefix = '#' * (depth + 1)
            f.write(f"{header_prefix} {os.path.basename(file_path)}\n\n")
            f.write(f"{summary}\n\n")

if __name__ == "__main__":
    main()
