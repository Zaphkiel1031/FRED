import requests
import json
import os
import re

# FRED API Key
api_key = 'api_key'
BASE_URL = 'https://api.stlouisfed.org/fred'

# 清理非法字元並限制名稱長度
def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)  # 替換非法字元
    name = re.sub(r'\s+', '_', name)  # 替換多空格為下劃線
    name = re.sub(r'&', 'and', name)  # 替換 & 符號
    return name[:100]  # 限制檔案名長度

# 建立長路徑支持（適用於 Windows）
def create_full_path(path):
    abs_path = os.path.abspath(path)
    if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
        return f"\\\\?\\{abs_path}"
    return abs_path

# 獲取某個類別下的子分類
def fetch_subcategories(category_id):
    url = f'{BASE_URL}/category/children?api_key={api_key}&category_id={category_id}&file_type=json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('categories', [])
    else:
        print(f"無法獲取類別 {category_id} 的子分類，狀態碼: {response.status_code}")
        return []

# 獲取某個分類下的系列資料
def fetch_series_from_category(category_id):
    url = f'{BASE_URL}/category/series?api_key={api_key}&category_id={category_id}&file_type=json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('seriess', [])
    else:
        print(f"無法獲取類別 {category_id} 的系列資料，狀態碼: {response.status_code}")
        return []

# 遞迴處理分類並獲取最底層的 series
def process_category(category_id, category_name, parent_path="categories"):
    safe_name = sanitize_filename(category_name)
    current_path = os.path.join(parent_path, f"{category_id}_{safe_name}")

    # 確保路徑非空並創建
    current_path = create_full_path(current_path)
    if current_path.strip():  # 檢查路徑是否有效
        os.makedirs(current_path, exist_ok=True)

    # 嘗試獲取該分類下的系列資料
    series_data = fetch_series_from_category(category_id)
    if series_data:
        with open(os.path.join(current_path, "series_data.json"), 'w', encoding='utf-8') as f:
            json.dump(series_data, f, indent=4)
        print(f"已儲存 {category_name} 下的系列資料到 {current_path}")

    # 獲取該分類的子分類
    subcategories = fetch_subcategories(category_id)
    for subcategory in subcategories:
        sub_id = subcategory['id']
        sub_name = subcategory['name']
        process_category(sub_id, sub_name, current_path)

def main():
    top_level_categories = fetch_subcategories(0)
    for category in top_level_categories:
        process_category(category['id'], category['name'])

if __name__ == '__main__':
    main()
