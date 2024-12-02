import requests
import json

# 填入專屬 API，讓 fredapi 核准會員通過
api_key = 'api_key'

# 獲取根級分類資料
url = f'https://api.stlouisfed.org/fred/category/children?api_key={api_key}&category_id=0&file_type=json'

response = requests.get(url)

if response.status_code == 200:
    # 取得所有頂級分類
    top_level_categories = response.json()['categories']
    
    all_categories = []
    
    # 遍歷所有頂級分類，獲取其子分類
    for category in top_level_categories:
        category_data = {
            'category_id': category['id'],
            'category_name': category['name'],
            'parent_id': category['parent_id'],
            'children': []
        }
        
        # 獲取每個頂級分類的子分類
        child_url = f'https://api.stlouisfed.org/fred/category/children?api_key={api_key}&category_id={category["id"]}&file_type=json'
        child_response = requests.get(child_url)
        
        if child_response.status_code == 200:
            category_data['children'] = child_response.json().get('categories', [])
        
        # 把分類資料加入最終資料列表
        all_categories.append(category_data)
    
    # 儲存成 JSON 檔案
    with open('fred_categories.json', 'w') as f:
        json.dump(all_categories, f, indent=4)
    print("FRED 所有類別資料已儲存為 'fred_all_categories.json'")
else:
    print(f"API 錯誤: {response.status_code}, 詳細錯誤：{response.text}")
