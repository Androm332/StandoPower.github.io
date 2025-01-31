import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Настройки Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-webrtc")  
chrome_options.add_argument("--disable-gpu")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL страницы с аниме
url = "https://animegoi.net/anime/2169-neverojatnye-prikljuchenija-dzhodzho-4-sezon.html"
driver.get(url)

# Ждём полную загрузку страницы
time.sleep(10)  # Увеличил паузу до 10 секунд (можно увеличить)

# Ищем ВСЕ iframe
iframes = driver.find_elements(By.TAG_NAME, "iframe")

# Если iframe не найдены, пишем ошибку
if not iframes:
    print("❌ Ошибка: На странице нет iframe!")
    driver.quit()
    exit()

# Выводим ВСЕ найденные iframe (проверяем, что нашёл)
print("\n🔍 Найденные iframe:")
for i, frame in enumerate(iframes):
    print(f"[{i+1}] {frame.get_attribute('src')}")

# Фильтруем только ссылки, содержащие "kodik.info"
kodik_links = [frame.get_attribute("src") for frame in iframes if frame.get_attribute("src") and "kodik.info" in frame.get_attribute("src")]

# Если не нашёл Kodik, пишем ошибку и выходим
if not kodik_links:
    print("\n❌ Ошибка: Не найдено ни одной ссылки на Kodik! Проверь сайт вручную.")
    driver.quit()
    exit()

# Выводим найденные ссылки
print("\n🔗 Найденные ссылки Kodik:")
for link in kodik_links:
    print(link)

# Закрываем браузер
driver.quit()

# Загружаем JSON-файл
json_filename = "anime_data.json"
with open(json_filename, "r", encoding="utf-8") as file:
    anime_data = json.load(file)

# Индекс 4-го сезона в JSON (Season 4: Diamond is Unbreakable)
season_index = 1  
anime_data[0]["seasons"][season_index]["episodes"] = []  # Очищаем список эпизодов

# Добавляем эпизоды (максимум 39)
for i, link in enumerate(kodik_links[:39]):  
    episode_data = {
        "title": f"Серия {i+1}",
        "kodikUrl": link,
        "image": "jojo_default.jpg"
    }
    anime_data[0]["seasons"][season_index]["episodes"].append(episode_data)

# Проверяем, сколько серий добавлено
print("\n✅ Добавлено серий в JSON:", len(anime_data[0]["seasons"][season_index]["episodes"]))

# Сохраняем обновлённый JSON
with open(json_filename, "w", encoding="utf-8") as file:
    json.dump(anime_data, file, ensure_ascii=False, indent=4)

print("\n✅ JSON успешно обновлён с 39 сериями из Kodik!")
