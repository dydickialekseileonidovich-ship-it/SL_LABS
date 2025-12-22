import sys, json, os, requests

def main():
    # получение данных
    response = requests.get('https://restcountries.com/v3.1/region/asia', timeout=30)
    countries = response.json()
    
    # фильтрация
    filtered = []
    for country in countries:
        if country.get('population', 0) > 30000000:
            info = {
                'name': country['name'].get('common', ''),
                'capital': country.get('capital', [''])[0],
                'population': country.get('population', 0),
                'area': country.get('area', 0),
                'flag_png': country['flags'].get('png', '') if 'flags' in country else ''
            }
            info['density'] = info['population'] / info['area'] if info['area'] > 0 else 0
            filtered.append(info)
    
    # сохранение в JSON
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    
    # топ по плотности
    filtered.sort(key=lambda x: x['density'], reverse=True)
    top5 = filtered[:5]
    
    print("Топ-5 стран по плотности населения:")
    print(f"{'№':<3} {'Страна':<20} {'Плотность':<12}")
    print("-" * 40)
    
    for i, country in enumerate(top5, 1):
        print(f"{i:<3} {country['name']:<20} {country['density']:<12.1f}")
    
    # сохранение флагов
    if not os.path.exists('flags'):
        os.makedirs('flags')
    
    for country in top5:
        if country['flag_png']:
            try:
                safe_name = country['name'].replace(' ', '_')
                flag_data = requests.get(country['flag_png'])
                with open(f"flags/{safe_name}.png", 'wb') as f:
                    f.write(flag_data.content)
            except:
                pass

if __name__ == "__main__":
    main()