import os
import json

def scan_folder(root_path):
    files_list = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            files_list.append({
                "title": f,
                "format": os.path.splitext(f)[1][1:],  # sans le point
                "path": filepath
            })
    return files_list

if __name__ == "__main__":
    root_folder = r"D:\BU\ProjetX"
    files_data = scan_folder(root_folder)
    
    with open("arborescence.json", "w", encoding="utf-8") as f:
        json.dump(files_data, f, indent=4, ensure_ascii=False)

    print(f"JSON généré avec {len(files_data)} fichiers")
