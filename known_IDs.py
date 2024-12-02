import os
import requests
import pandas as pd
import time
import warnings

# 關閉FutureWarning警告
warnings.simplefilter(action='ignore', category=FutureWarning)

# 填入你的 API 金鑰
api_key = 'api_key'

# 定義數據名稱及其代碼和頻率
data_codes = {
    "GDP": ("國內生產總值（年計）", "A"),
    "UNRATE": ("失業率（月計）", "M"),
    "CPIAUCNS": ("全城市消費者物價指數 CPI（月計）", "M"),
    "CPILFESL": ("核心 CPI（月計）", "M"),
    "FEDFUNDS": ("聯邦基金利率（日計）", "D"),  # 日計數據
    "M2SL": ("M2 貨幣供應量（月計）", "M"),
    "RSXFS": ("零售銷售（月計）", "M"),
    "INDPRO": ("工業生產指數（月計）", "M"),
    "PPIACO": ("生產者物價指數 PPI（月計）", "M"),
    "NETEXP": ("貿易平衡（年計）", "A"),
    "SP500": ("標普 500 股市指數（日計）", "D"),  # 日計數據
    "NASDAQCOM": ("NASDAQ 綜合股市指數（日計）", "D")  # 日計數據
}

# 定義儲存路徑
base_dir = "economic_data"

# 確保基礎目錄存在
os.makedirs(base_dir, exist_ok=True)

# 從 FRED 網站獲取數據
for code, (desc, freq) in data_codes.items():
    print(f"正在提取數據: {desc} (代碼: {code})")
    try:
        url = f'https://api.stlouisfed.org/fred/series/observations?series_id={code}&api_key={api_key}&file_type=json'
        response = requests.get(url)
        response.raise_for_status()

        # 解析 JSON 數據
        data = response.json()
        observations = data['observations']
        series_data = pd.DataFrame(observations)

        # 過濾無效數據
        series_data = series_data[series_data['value'] != '.']
        
        # 轉換為 datetime64 類型
        series_data['date'] = pd.to_datetime(series_data['date'], errors='coerce')

        if series_data.empty:
            print(f"{desc} 沒有可用數據，跳過。")
            continue

        # 根據頻率分類存儲數據
        if freq == "D":
            # 如果是日計數據，將其分組為每年的資料
            series_data['year'] = series_data['date'].dt.year  # 提取年份
            for year, group in series_data.groupby('year'):
                file_path = os.path.join(base_dir, desc, "A", f"{year}.csv")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # 檢查並存儲數據，避免重複
                if os.path.exists(file_path):
                    existing_data = pd.read_csv(file_path)
                    combined_data = pd.concat([existing_data, group[['date', 'value']]], ignore_index=True)
                    combined_data.to_csv(file_path, index=False, encoding="utf-8-sig")
                else:
                    group[['date', 'value']].to_csv(file_path, index=False, encoding="utf-8-sig")

            print(f"數據已儲存至 {desc}/A/")

        else:
            # 對於月計（M）或年計（A）數據，根據年份存檔
            for _, row in series_data.iterrows():
                date = row['date']
                value = row['value']
                if freq == "M":
                    file_path = os.path.join(base_dir, desc, "A", f"{date.year}.csv")
                elif freq == "A":
                    file_path = os.path.join(base_dir, desc, "A", f"{date.year}.csv")

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # 檢查並存儲數據，避免重複
                if os.path.exists(file_path):
                    existing_data = pd.read_csv(file_path)
                    if date not in existing_data['date'].values:
                        new_data = pd.DataFrame({"date": [date], "value": [value]})
                        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
                        combined_data.to_csv(file_path, index=False, encoding="utf-8-sig")
                else:
                    pd.DataFrame({"date": [date], "value": [value]}).to_csv(file_path, index=False, encoding="utf-8-sig")

            print(f"數據已儲存至 {desc}/A/")

        time.sleep(1)  # 降低請求頻率

    except Exception as e:
        print(f"無法提取 {desc} (代碼: {code})，錯誤訊息: {e}")
