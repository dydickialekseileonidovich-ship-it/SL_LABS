import json
from collections import defaultdict

def read_json_file(filename):
    """чтение json файла и передача данных в словарь python"""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['clients']  # возвращаем список клиентов

def find_clients_by_surname_prefix(clients, prefix):
    """поиск клиентов по первым 3 буквам фамилии"""
    prefix = prefix.lower()
    found_clients = []
    
    for client in clients:
        if client['last_name'].lower().startswith(prefix):
            found_clients.append(client)
    
    return found_clients

def calculate_avg_budget_by_company(clients):
    """вычисление среднего бюджета по компаниям"""
    company_budgets = defaultdict(list)
    
    for client in clients:
        company = client['company']
        company_budgets[company].append(client['budget'])
    
    avg_budgets = {}
    for company, budgets in company_budgets.items():
        avg_budgets[company] = sum(budgets) / len(budgets)
    
    return avg_budgets

def count_clients_by_industry(clients):
    """подсчет количества клиентов по отраслям"""
    industry_count = defaultdict(int)
    
    for client in clients:
        industry = client['industry']
        industry_count[industry] += 1
    
    return dict(industry_count)

def save_filtered_data_to_json(clients, output_filename='out.json'):
    """передача отфильтрованных данных в файл out.json"""
    # фильтруем клиентов по бюджету > 30000 или количеству проектов >= 5
    filtered_clients = [
        client for client in clients 
        if client['budget'] > 30000 or client['projects_count'] >= 5
    ]
    
    # создаем структуру данных для сохранения
    result_data = {
        "total_clients": len(clients),
        "filtered_clients_count": len(filtered_clients),
        "filter_criteria": {
            "budget_greater_than": 30000,
            "projects_greater_or_equal": 5
        },
        "clients": filtered_clients
    }
    
    # сохраняем в файл
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=2, ensure_ascii=False)
    
    return result_data

def display_clients_info(clients):
    """отображение информации о клиентах"""
    print("=" * 60)
    print("информация о клиентах:")
    print("=" * 60)
    
    for i, client in enumerate(clients, 1):
        print(f"\nклиент #{i}:")
        print(f"  id: {client['client_id']}")
        print(f"  имя: {client['first_name']} {client['last_name']}")
        print(f"  компания: {client['company']}")
        print(f"  бюджет: ${client['budget']:,}")
        print(f"  проектов: {client['projects_count']}")
        print(f"  отрасль: {client['industry']}")

def analyze_clients():
    """основная функция анализа клиентов"""
    # читаем данные из файла
    clients = read_json_file('9.json')
    
    # выводим информацию о клиентах
    display_clients_info(clients)
    
    print("\n" + "=" * 60)
    print("анализ данных:")
    print("=" * 60)
    
    # 1. поиск клиентов по первым 3 буквам фамилии
    print("\n1. поиск клиентов по первым 3 буквам фамилии:")
    
    test_prefixes = ['vol', 'nov', 'sok', 'leb', 'orl']
    for prefix in test_prefixes:
        found = find_clients_by_surname_prefix(clients, prefix)
        if found:
            print(f"   '{prefix}': найдено {len(found)} клиент(ов)")
            for client in found:
                print(f"     - {client['first_name']} {client['last_name']}")
        else:
            print(f"   '{prefix}': не найдено")
    
    # 2. вычисление среднего бюджета по компаниям
    print("\n2. средний бюджет по компаниям:")
    avg_budgets = calculate_avg_budget_by_company(clients)
    
    for company, avg_budget in avg_budgets.items():
        print(f"   {company}: ${avg_budget:,.2f}")
    
    # 3. подсчет количества клиентов по отраслям
    print("\n3. количество клиентов по отраслям:")
    industry_stats = count_clients_by_industry(clients)
    
    for industry, count in industry_stats.items():
        print(f"   {industry}: {count} клиент(ов)")
    
    # 4. сохранение отфильтрованных данных
    print("\n4. сохранение отфильтрованных данных:")
    result = save_filtered_data_to_json(clients)
    print(f"   всего клиентов: {result['total_clients']}")
    print(f"   отфильтровано: {result['filtered_clients_count']}")
    print(f"   критерии фильтрации:")
    print(f"     - бюджет > ${result['filter_criteria']['budget_greater_than']:,}")
    print(f"     - проектов >= {result['filter_criteria']['projects_greater_or_equal']}")
    print(f"   файл сохранен: out.json")
    
    # показываем отфильтрованных клиентов
    print(f"\n   отфильтрованные клиенты:")
    for client in result['clients']:
        print(f"     - {client['first_name']} {client['last_name']} "
              f"(бюджет: ${client['budget']:,}, проектов: {client['projects_count']})")
    
    print("\n" + "=" * 60)
    print("анализ завершен!")
    print("=" * 60)
    
    return clients

# если файл запущен напрямую
if __name__ == "__main__":
    analyze_clients()