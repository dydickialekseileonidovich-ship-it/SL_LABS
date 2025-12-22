import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def get_top_result(url, year, discipline, gender):
    try:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        ]
        
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        if not table:
            tables = soup.find_all('table')
            if tables:
                table = tables[0]
            else:
                return None
        
        rows = table.find_all('tr')
        if len(rows) <= 1:
            return None
        
        data_row = rows[1]
        cells = data_row.find_all('td')
        
        if len(cells) < 5:
            return None
        
        rank = cells[0].get_text(strip=True)
        
        name_cell = cells[1]
        athlete_link = name_cell.find('a')
        if athlete_link:
            athlete = athlete_link.get_text(strip=True)
        else:
            athlete = name_cell.get_text(strip=True)
        
        country_cell = cells[3]
        country = country_cell.get_text(strip=True)
        
        if len(country) > 3:
            country_code = country[-3:] if country[-3:].isupper() else country[:3]
            country = country_code
        
        time_result = cells[4].get_text(strip=True)
        
        date = ""
        if len(cells) > 6:
            date = cells[6].get_text(strip=True)
        else:
            date = f"{year}"
        
        return {
            'Год': year,
            'Дисциплина': discipline,
            'Пол': gender,
            'Спортсмен': athlete,
            'Страна': country,
            'Время': time_result,
            'Дата': date
        }
            
    except:
        return None

def generate_urls():
    disciplines = {
        '60m': '60-metres',
        '100m': '100-metres', 
        '200m': '200-metres',
        '400m': '400-metres'
    }
    
    genders = {'мужчины': 'men', 'женщины': 'women'}
    years = list(range(2001, 2025))
    urls = []
    
    for year in years:
        for disc_key, disc_value in disciplines.items():
            for gender_key, gender_value in genders.items():
                url = f"https://worldathletics.org/records/toplists/sprints/{disc_value}/all/{gender_value}/senior/{year}"
                urls.append({
                    'url': url,
                    'год': year,
                    'дисциплина': disc_key,
                    'пол': gender_key
                })
    
    return urls

def main():
    print("Парсинг данных World Athletics")
    print("Дисциплины: 60м, 100м, 200м, 400м")
    print("Годы: 2001-2024")
    
    urls_to_scrape = generate_urls()
    print(f"Всего URL: {len(urls_to_scrape)}")
    
    all_results = []
    
    for i, item in enumerate(urls_to_scrape, 1):
        url = item['url']
        year = item['год']
        discipline = item['дисциплина']
        gender = item['пол']
        
        print(f"[{i}/{len(urls_to_scrape)}] {year} - {discipline} - {gender}")
        
        result = get_top_result(url, year, discipline, gender)
        if result:
            all_results.append(result)
        
        time.sleep(random.uniform(2, 5))
    
    if all_results:
        with open('top_results.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Год', 'Дисциплина', 'Пол', 'Спортсмен', 'Страна', 'Время', 'Дата']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for row in all_results:
                writer.writerow(row)
        
        print(f"\nСохранено {len(all_results)} записей в top_results.csv")
    else:
        print("\nНе удалось получить данные")

if __name__ == "__main__":
    main()