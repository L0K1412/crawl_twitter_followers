from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Đọc file JSON
with open('twitter_user_names.json', 'r') as json_file:
    data = json.load(json_file)

# Kiểm tra xem data có phải là danh sách (list) không
if isinstance(data, list):
    result_list = []
    
    # Lặp qua danh sách các phần tử trong data
    for item in data:
        # Kiểm tra xem item có kiểu dữ liệu là dictionary không
        if isinstance(item, dict):
            user_name = item.get("twitter_user_name")
            if user_name:
                result_list.append(user_name.strip())      

def get_followers_twitter_ID(driver, twitter_id):
    url = f"https://twitter.com/{twitter_id}"
    driver.get(url)
    
    try:  
        driver.implicitly_wait(3) # Chờ tối đa 10 giây cho các thao tác tiếp theo (có thể giảm xuống 5s do dễ bị chuyển hướng qua trang log-in, gây mất rất nhiều time)
        followers_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span")
        followers_count = followers_element.text
        processed_dict[twitter_id] = followers_count
        
        account_info = {
            "twitter_user_name": twitter_id,
            "followers": followers_count
        }
        
        with open('backup1.json', 'a') as json_file:
            json.dump(account_info, json_file)
    except Exception:
        processed_dict[twitter_id] = 0
        
        account_info = {
            "twitter_user_name": twitter_id,
            "followers": 0
        }
        
        with open('backup1.json', 'a') as json_file:
            json.dump(account_info, json_file)

# Tạo dictionary chứa giá trị xử lí từ hàm
processed_dict = {}
driver = webdriver.Chrome()
count = 0

for item in result_list[60000:61500]:
    if count == 90:
        driver.quit()
        driver = webdriver.Chrome()
        count = 0
    get_followers_twitter_ID(driver, item)
    count = count + 1
    
output_data = []
for twitter_id, followers_count in processed_dict.items():
    entry = {
        "twitter_user_name": twitter_id,
        "followers": followers_count
    }
    output_data.append(entry)

output_file = "output_60000 - 61500.json"
with open(output_file, "w") as json_file:
    json.dump(output_data, json_file, indent=4)